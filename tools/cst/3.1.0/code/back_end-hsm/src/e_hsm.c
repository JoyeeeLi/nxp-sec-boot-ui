/*===========================================================================*/
/**
 @file    e_hsm.c

 @brief   Implements a built-in OpenSSL engine to provide a backend replacement
 for Code-Signing Tool to support Hardware Security Module (HSM).  
 It plugs in alternative implementations for OpenSSL to perform cryptographic 
 operations requested to sign codes for the NXP High Assurance Boot (HAB) 
 and Advanced  High Assurance Boot (AHAB).

 The engine re-writes an implementation of RSA private encrypt function, 
 ECDSA sign function and how public certificates and private keys are loaded
 from the HSM to the appropriate data structure X509, RSA, EVP_PKEY and EC_KEY. 
 
 Optionally SHA digest functions can be re-written also to be performed at the HSM level.

 @verbatim
 =============================================================================

    Copyright 2018 NXP

Presence of a copyright notice is not an acknowledgement of publication.
This software file listing contains information of NXP that is of a
confidential and proprietary nature and any viewing or use of this file is
prohibited without specific written permission from NXP

 =============================================================================
 @endverbatim */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <assert.h>
#include <dlfcn.h>
#include <sys/types.h>
#include <unistd.h>
#include <openssl/e_os2.h>
#include <openssl/ossl_typ.h>
#include <openssl/engine.h>
#include <openssl/err.h>
#include <openssl/bn.h>
#include <openssl/pem.h>
#include <openssl/rsa.h>
#include <openssl/ecdsa.h>
#include <openssl/objects.h>

#ifndef OPENSSL_NO_HW
#ifndef OPENSSL_NO_HW_HSM
#include <cryptoki.h>
#include <e_hsm_err.h>
#include <e_hsm.h>
#include <pkcs-11v2-20a3.h>

#ifdef OLDER_OPENSSL
#define MD_DATA(ctx) ((struct hsm_digest_ctx *)(ctx->md_data))
#else
#define MD_DATA(ctx) ((struct hsm_digest_ctx *)(EVP_MD_CTX_md_data(ctx)))
#endif

#ifdef HSM_DEBUG
#define dbg_fprintf(args...) do { fprintf(stderr, args); fflush(stderr); } while (0)
#else
#define dbg_fprintf(args...)
#endif
/* Engine id & name used when creating the ENGINE */
static const char *engine_hsm_id = "hsm";
static const char *engine_hsm_name =
  "Hardware Security Module engine support";
/* Pointer to a CK_FUNCTION_LIST structure containing the function pointers to the standard PKCS#11 cryptoki library functions. */
static CK_FUNCTION_LIST_PTR pFunctionList = NULL;
/* Name of C_GetFunctionList function */
static const char HSM_GET_FUNCTION_LIST[] = "C_GetFunctionList";
#define SSL_SIG_LENGTH	36
#define KEY_STORE 1
static CK_BBOOL true = TRUE;
static CK_BBOOL false = FALSE;

#ifndef OPENSSL_NO_RSA
/* Index for add handler of private key to RSA */
static int rsa_privkey_idx = -1;
/* Index for add handler of session to RSA */
static int rsa_session_idx = -1;
#endif

#ifndef OPENSSL_NO_ECDSA
/* Index for add handler of private key to ECDSA */
static int ecdsa_privkey_idx = -1;
static int ecdsa_session_idx = -1;
#endif

/* Initialization flag */
static int HSM_Initialized = 0;

/* DSO handle used for loading and unloading Cryptoki library library. */
void *hsm_dso = NULL;

/* DSO file name or path. .so on Linux or .dll on windows */
char *HSM_LIBNAME = NULL;

#if defined(WIN32)
#define DLOPEN_FLAG RTLD_LAZY
#else
#define DLOPEN_FLAG (RTLD_NOW | RTLD_LOCAL)
#endif

/* The definitions for control commands specific to this engine */
static const ENGINE_CMD_DEFN hsm_cmd_defns[] = { {HSM_CMD_MODULE_PATH,
						  "MODULE_PATH",
						  "Specifies the path to the 'pkcs#11' shared library",
						  ENGINE_CMD_FLAG_STRING},
  {HSM_CMD_SLOT_ID, "SLOT_ID",
   "Specifies the slot containing the token to use",
   ENGINE_CMD_FLAG_NUMERIC}, {HSM_CMD_PIN, "PIN", "Specifies the PIN",
			      ENGINE_CMD_FLAG_STRING}, {HSM_CMD_LOAD_CERT,
							"LOAD_CERT",
							"Load certificate from token",
							ENGINE_CMD_FLAG_STRING},
  {0, NULL,
   NULL, 0}
};

/* Engine constructor */
ENGINE *engine_hsm (void);
/* Needed if the ENGINE is being compiled into a self-contained shared-library. */
static int bind_hsm (ENGINE * e);

/* Initialisation function */
static int hsm_init (ENGINE * e);
static int hsm_finish (ENGINE * e);
static int hsm_ctrl (ENGINE * e, int cmd, long i, void *p, void (*f) ());
/* Destructor (complements the "engine_hsm()" constructor) */
static int hsm_destroy (ENGINE * e);

/* RSA functions */
#ifndef OPENSSL_NO_RSA
static int hsm_RSA_private_encrypt (int flen, const unsigned char *from,
				    unsigned char *to, RSA * rsa,
				    int padding);
static int hsm_RSA_init (RSA * rsa);
static int hsm_RSA_finish (RSA * rsa);
#endif

/* ECDSA functions */
#ifndef OPENSSL_NO_ECDSA
int hsm_ECDSA_sign_setup (EC_KEY * eckey, BN_CTX * ctx_in, BIGNUM ** kinvp,
			  BIGNUM ** rp);
static ECDSA_SIG *hsm_ECDSA_sign (const unsigned char *dgst, int dgst_len,
				  const BIGNUM * kinv, const BIGNUM * rp,
				  EC_KEY * ecdsa);
#endif

/* Digest functions */
static inline int hsm_digest_init (EVP_MD_CTX * ctx, int alg);
static int hsm_digest_update (EVP_MD_CTX * ctx, const void *in, size_t len);
static int hsm_digest_copy (EVP_MD_CTX * out, const EVP_MD_CTX * in);
static int hsm_digest_finish (EVP_MD_CTX * ctx, unsigned char *md);
static inline int hsm_digest_cleanup (EVP_MD_CTX * ctx);
/* SHA initialization functions */
static inline int hsm_sha1_init (EVP_MD_CTX * ctx);
static inline int hsm_sha224_init (EVP_MD_CTX * ctx);
static inline int hsm_sha256_init (EVP_MD_CTX * ctx);
static inline int hsm_sha384_init (EVP_MD_CTX * ctx);
static inline int hsm_sha512_init (EVP_MD_CTX * ctx);

static int pre_init_hsm (ENGINE * e);
static int hsm_engine_digests (ENGINE * e, const EVP_MD ** digest,
			       const int **nids, int nid);
/* Hex string decoder */
static unsigned char *hex2bin (const char *hexstr, size_t * size);
/* Token and session management */
struct token_session *hsm_get_session (void);
void hsm_register_token (ENGINE * e, struct _token *tok);
struct _token *hsm_add_token (CK_SLOT_ID slot_id);

/* Wrapper for hsm_find_certificate */
int load_certificate (ENGINE * e, void *p);
/* Public certificate loader. It loads cert by id in DER format and convert it to PEM */
static X509 *hsm_find_certificate (ENGINE * e, const char *cert_id);
/* Private key loader. It only loads exponent and modulus together with object handler on token */
static EVP_PKEY *hsm_load_privkey (ENGINE *, const char *key_id,
				   UI_METHOD * ui_method,
				   void *callback_data);

#define HSM_MAX_ALGS 20


#ifdef OPENSSL_NO_DYNAMIC_ENGINEX
/* engine constructor */
ENGINE *
engine_hsm (void)
{
  hsm_token_list = NULL;
  hsm_token = NULL;
  dbg_fprintf ("%s\n", __FUNCTION__);
  ENGINE *ret = ENGINE_new ();
  if (!ret)
    {
      return NULL;
    }
  if (!bind_helper (ret))
    {
      ENGINE_free (ret);
      return NULL;
    }
  return ret;
}

void
ENGINE_load_hsm (void)
{
  ENGINE *toadd = engine_hsm ();
  dbg_fprintf ("%s\n", __FUNCTION__);
  if (!toadd)
    return;
  ENGINE_add (toadd);
  ENGINE_free (toadd);
  ERR_clear_error ();
}
#else
static int
bind_helper (ENGINE * e, const char *id)
{
  dbg_fprintf ("%s\n", __FUNCTION__);
  if ((NULL != id) && (strcmp (id, engine_hsm_id) != 0))
    return 0;
  return (bind_hsm (e));
}

IMPLEMENT_DYNAMIC_CHECK_FN ()IMPLEMENT_DYNAMIC_BIND_FN (bind_helper)
#endif
     static int
       num_digest_nids = 0;
#ifdef OLDER_OPENSSL

     const EVP_MD
       hsm_sha1 = { NID_sha1, NID_sha1WithRSAEncryption,
       SHA_DIGEST_LENGTH, EVP_MD_FLAG_PKEY_METHOD_SIGNATURE, hsm_sha1_init,
       hsm_digest_update, hsm_digest_finish, hsm_digest_copy,
       hsm_digest_cleanup, EVP_PKEY_RSA_method, SHA_CBLOCK,
       sizeof (struct hsm_digest_ctx)
     };

const EVP_MD hsm_sha224 = { NID_sha224, NID_sha224WithRSAEncryption,
  SHA224_DIGEST_LENGTH, EVP_MD_FLAG_PKEY_METHOD_SIGNATURE,
  hsm_sha224_init, hsm_digest_update, hsm_digest_finish, hsm_digest_copy,
  hsm_digest_cleanup, EVP_PKEY_RSA_method, SHA256_CBLOCK,
  sizeof (struct hsm_digest_ctx)
};

const EVP_MD hsm_sha256 = { NID_sha256, NID_sha256WithRSAEncryption,
  SHA256_DIGEST_LENGTH, EVP_MD_FLAG_PKEY_METHOD_SIGNATURE,
  hsm_sha256_init, hsm_digest_update, hsm_digest_finish, hsm_digest_copy,
  hsm_digest_cleanup, EVP_PKEY_RSA_method, SHA256_CBLOCK,
  sizeof (struct hsm_digest_ctx)
};

const EVP_MD hsm_sha384 = { NID_sha384, NID_sha384WithRSAEncryption,
  SHA384_DIGEST_LENGTH, EVP_MD_FLAG_PKEY_METHOD_SIGNATURE,
  hsm_sha384_init, hsm_digest_update, hsm_digest_finish, hsm_digest_copy,
  hsm_digest_cleanup, EVP_PKEY_RSA_method, SHA512_CBLOCK,
  sizeof (struct hsm_digest_ctx)
};

const EVP_MD hsm_sha512 = { NID_sha512, NID_sha512WithRSAEncryption,
  SHA512_DIGEST_LENGTH, EVP_MD_FLAG_PKEY_METHOD_SIGNATURE,
  hsm_sha512_init, hsm_digest_update, hsm_digest_finish, hsm_digest_copy,
  hsm_digest_cleanup, EVP_PKEY_RSA_method, SHA512_CBLOCK,
  sizeof (struct hsm_digest_ctx)
};

#else

#define DECLARE_DIGEST_EVP(dig, len, enc)				      \
	static EVP_MD *dig##_md = NULL;						      \
	static const EVP_MD *hsm_##dig(void)					      \
	{									      \
		if (dig##_md == NULL) {						      \
			EVP_MD *md;						      \
			if (( md = EVP_MD_meth_new(NID_##dig,			      \
							NID_##dig##WithRSA##enc)) == NULL     \
					|| !EVP_MD_meth_set_result_size(md, len##_DIGEST_LENGTH)   \
					|| !EVP_MD_meth_set_input_blocksize(md, len##_CBLOCK)      \
					|| !EVP_MD_meth_set_app_datasize(md, 		      \
						sizeof(struct hsm_digest_ctx))     \
					|| !EVP_MD_meth_set_flags(md, 0)			      \
					|| !EVP_MD_meth_set_init(md, hsm_##dig##_init)	      \
					|| !EVP_MD_meth_set_update(md, hsm_digest_update)	      \
					|| !EVP_MD_meth_set_final(md, hsm_digest_finish)	      \
					|| !EVP_MD_meth_set_copy(md, hsm_digest_copy)	      \
					|| !EVP_MD_meth_set_cleanup(md, hsm_digest_cleanup)) {  \
				EVP_MD_meth_free(md);				      \
				md = NULL;					      \
			}							      \
			dig##_md = md;						      \
		}								      \
		return dig##_md;						      \
	}									      \
	\
	static void hsm_##dig##_destroy(void)				      \
	{									      \
		EVP_MD_meth_free(dig##_md);					      \
		dig##_md = NULL;						      \
	}

DECLARE_DIGEST_EVP (sha1, SHA, Encryption)
DECLARE_DIGEST_EVP (sha224, SHA256, Encryption)
DECLARE_DIGEST_EVP (sha256, SHA256, Encryption)
DECLARE_DIGEST_EVP (sha384, SHA512, Encryption)
DECLARE_DIGEST_EVP (sha512, SHA512, Encryption)
#endif
#ifndef OPENSSL_NO_RSA
#ifdef OLDER_OPENSSL
/*To sign images for HAB it is enough to implement rsa_priv_encrypt interface */
     static RSA_METHOD hsm_rsa = { "PKCS#11 RSA", NULL,	/* rsa_pub_encrypt */
       NULL,			/* rsa_pub_decrypt */
       hsm_RSA_private_encrypt,	/* rsa_priv_encrypt */
       NULL,			/* rsa_priv_decrypt */
       NULL,			/* rsa_mod_exp */
       NULL,			/* bn_mod_exp */
       hsm_RSA_init,		/* init */
       hsm_RSA_finish,		/* finish */
       RSA_FLAG_SIGN_VER,	/* flags */
       NULL,			/* app_data */
       NULL,			/* rsa_sign */
       NULL,			/* rsa_verify */
       NULL			/* rsa_generate_key */
     };
#else
     static RSA_METHOD *hsm_rsa = NULL;
#endif

/*RSA_METHOD *HSM_RSA(void)
{
return(&hsm_rsa);
}*/
#endif

#ifndef OPENSSL_NO_ECDSA
#ifdef OLDER_OPENSSL
     static ECDSA_METHOD hsm_ecdsa = { "PKCS#11 ECDSA", hsm_ECDSA_sign,
       hsm_ECDSA_sign_setup, NULL,	/* cdsa_do_verify */
#if 0
       NULL,			/* init */
       NULL,			/* finish */
#endif
       0,			/* flags */
       NULL			/* app_data */
     };
#else
     static ECDSA_METHOD *hsm_ecdsa = NULL;
#endif



#if OPENSSL_VERSION_NUMBER >= 0x10100000L && !defined(LIBRESSL_VERSION_NUMBER)
     static EC_KEY_METHOD *hsm_ec_meth = NULL;
#endif

/*ECDSA_METHOD *HSM_ECDSA(void)
{
return(&hsm_ecdsa);
}*/
#endif

/* fork handler */
     void hsm_atfork_init (void)
{
  dbg_fprintf ("hsm_atfork_init: called (pid %d)\n", getpid ());
  HSM_Initialized = 0;
}

/* On error, exit with error message and token return value */
#define hsm_die(fn, reason, rv) \
	{ \
		char errbuf[20]; \
		hsm_err(fn, reason); \
		sprintf(errbuf, "%lx", rv); \
		ERR_add_error_data(2, "HSM CK_RV=0x", errbuf); \
	}

struct token_session *
hsm_get_session (void)
{
  CK_RV rv;
  struct token_session *wrapper;

  dbg_fprintf ("%s\n", __FUNCTION__);

  if (!hsm_token)
    {
      hsm_err (HSM_F_GETSESSION, HSM_R_NO_SLOT_SELECTED);
      return NULL;
    }

  wrapper = OPENSSL_malloc (sizeof (struct token_session));
  if (!wrapper)
    {
      hsm_err (HSM_F_GETSESSION, HSM_R_MALLOC_FAILURE);
      return NULL;
    }
  wrapper->token = hsm_token;

  if (!HSM_Initialized)
    {
      rv = pFunctionList->C_Initialize (NULL);
      if (rv != CKR_OK && rv != CKR_CRYPTOKI_ALREADY_INITIALIZED)
	{
	  hsm_die (HSM_F_GETSESSION, HSM_R_INITIALIZE, rv);
	  return NULL;
	}
      HSM_Initialized = 1;
    }

  rv = pFunctionList->C_OpenSession (wrapper->token->slot_id,
				     CKF_SERIAL_SESSION | CKF_RW_SESSION,
				     NULL_PTR, NULL_PTR, &wrapper->session);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_GETSESSION, HSM_R_OPENSESSION, rv);
      return NULL;
    }

  if (wrapper->token->pin)
    {
      rv = pFunctionList->C_Login (wrapper->session, CKU_USER,
				   (CK_UTF8CHAR *) wrapper->token->pin,
				   (CK_ULONG) strlen (wrapper->token->pin));

      if (rv != CKR_OK && rv != CKR_USER_ALREADY_LOGGED_IN)
	{
	  hsm_die (HSM_F_GETSESSION, HSM_R_LOGIN, rv);
	  return NULL;
	}
    }

  return wrapper;
}

/* needed if the ENGINE is being compiled into a self-contained shared-library. */
static int
bind_hsm (ENGINE * e)
{

  int ret = 0;

  dbg_fprintf ("%s\n", __FUNCTION__);

  ERR_load_hsm_strings ();

  if (!ENGINE_set_id (e, engine_hsm_id)
      || !ENGINE_set_name (e, engine_hsm_name)
      || !ENGINE_set_ctrl_function (e, hsm_ctrl)
      || !ENGINE_set_init_function (e, hsm_init)
      || !ENGINE_set_cmd_defns (e, hsm_cmd_defns)
      || !ENGINE_set_destroy_function (e, hsm_destroy)
      || !ENGINE_set_finish_function (e, hsm_finish)
#ifdef USE_HSM_DIGESTS
      || !ENGINE_set_digests (e, hsm_engine_digests)
#endif
    )
    {
      dbg_fprintf ("bind_hsm failed\n");
      goto end;
    }
  ret = 1;
end:return ret;
}

#ifdef ENGINE_DYNAMIC_SUPPORT
static int
bind_helper (ENGINE * e, const char *id)
{
  dbg_fprintf ("%s\n", __FUNCTION__);

  if (id && (strcmp (id, engine_hsm_id) != 0))
    return 0;
  if (!bind_hsm (e))
    return 0;
  return 1;
}

IMPLEMENT_DYNAMIC_CHECK_FN ()IMPLEMENT_DYNAMIC_BIND_FN (bind_helper)
#else
ENGINE *
engine_hsm (void)
{

  dbg_fprintf ("%s\n", __FUNCTION__);

  ENGINE *ret = ENGINE_new ();
  if (!ret)
    return NULL;
  if (!bind_hsm (ret))
    {
      ENGINE_free (ret);
      return NULL;
    }

  return ret;
}

void
ENGINE_load_hsm (void)
{
  dbg_fprintf ("%s\n", __FUNCTION__);

  ENGINE *e_hsm = engine_hsm ();
  if (!e_hsm)
    return;
  ENGINE_add (e_hsm);
  ENGINE_free (e_hsm);
  ERR_clear_error ();
}
#endif

static int
get_hsm_digests (const int **retnids)
{
  static int nids[HSM_MAX_ALGS];
  int i, count = 0, *hsm_implemented_digests;

  dbg_fprintf ("%s\n", __FUNCTION__);

  if (hsm_token)
    hsm_implemented_digests = hsm_token->hsm_implemented_digests;
  else
    {
      hsm_err (HSM_F_GET_HSM_DIGESTS, HSM_R_NO_SLOT_SELECTED);
      return 0;
    }

  memset (nids, 0, sizeof (nids));
  *retnids = NULL;

  for (i = 0; i < NUM_NID; i++)
    {
      if (hsm_implemented_digests[i])
	{
	  nids[count++] = i;
	}
    }

  if (count)
    *retnids = nids;

  return count;
}

static int
hsm_engine_digests (ENGINE * e, const EVP_MD ** digest,
		    const int **nids, int nid)
{
  int ret = 1;

  dbg_fprintf ("%s\n", __FUNCTION__);
  if (!digest)
    {
      return get_hsm_digests (nids);
    }
  if (!hsm_token)
    {
      hsm_err (HSM_F_ENGINE_DIGESTS, HSM_R_NO_SLOT_SELECTED);
      return 0;
    }
  if (hsm_token->hsm_implemented_digests[nid])
    {
      switch (nid)
	{
	case NID_sha1:
#ifdef OLDER_OPENSSL
	  *digest = &hsm_sha1;
#else
	  *digest = hsm_sha1 ();
#endif
	  break;
	case NID_sha224:
#ifdef OLDER_OPENSSL
	  *digest = &hsm_sha224;
#else
	  *digest = hsm_sha224 ();
#endif
	  break;
	case NID_sha256:
#ifdef OLDER_OPENSSL
	  *digest = &hsm_sha256;
#else
	  *digest = hsm_sha256 ();
#endif
	  break;
	case NID_sha384:
#ifdef OLDER_OPENSSL
	  *digest = &hsm_sha384;
#else
	  *digest = hsm_sha384 ();
#endif
	  break;
	case NID_sha512:
#ifdef OLDER_OPENSSL
	  *digest = &hsm_sha512;
#else
	  *digest = hsm_sha512 ();
#endif
	  break;
	default:
	  *digest = NULL;
	  ret = 0;
	  break;
	}
    }
  return ret;
}

static const char *
get_HSM_LIBNAME (void)
{
  dbg_fprintf ("%s\n", __FUNCTION__);
  if (HSM_LIBNAME)
    return HSM_LIBNAME;
}

static void
free_HSM_LIBNAME (void)
{
  dbg_fprintf ("%s\n", __FUNCTION__);
  if (HSM_LIBNAME)
    OPENSSL_free ((void *) HSM_LIBNAME);
  HSM_LIBNAME = NULL;
}

long
set_HSM_LIBNAME (const char *name)
{
  dbg_fprintf ("%s\n", __FUNCTION__);
  free_HSM_LIBNAME ();
  return ((HSM_LIBNAME = BUF_strdup (name)) != NULL ? 1 : 0);
}

void
hsm_register_token (ENGINE * e, struct _token *tok)
{
  CK_RV rv;
  CK_ULONG mech_cnt;
  CK_MECHANISM_TYPE_PTR mech_list;
  int i;

  dbg_fprintf ("%s\n", __FUNCTION__);

  if (!tok)
    return;

  rv = pFunctionList->C_GetMechanismList (tok->slot_id, NULL_PTR, &mech_cnt);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_ADDTOKEN, HSM_R_GETMECHANISMLIST, rv);
      goto err;
    }

  mech_list =
    (CK_MECHANISM_TYPE_PTR) OPENSSL_malloc (mech_cnt *
					    sizeof (CK_MECHANISM_TYPE));
  if (mech_list == NULL)
    {
      hsm_die (HSM_F_ADDTOKEN, HSM_R_MALLOC_FAILURE, rv);
      goto err;
    }

  rv = pFunctionList->C_GetMechanismList (tok->slot_id, mech_list, &mech_cnt);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_ADDTOKEN, HSM_R_GETMECHANISMLIST, rv);
      goto err_free;
    }

  for (i = 0; i < mech_cnt; i++)
    {
      switch (mech_list[i])
	{
	case CKM_RSA_PKCS_KEY_PAIR_GEN:
	case CKM_RSA_PKCS:
	case CKM_RSA_9796:
	case CKM_RSA_X_509:
	case CKM_RSA_PKCS_OAEP:
	case CKM_RSA_X9_31:
	case CKM_RSA_X9_31_KEY_PAIR_GEN:
	case CKM_MD5_RSA_PKCS:
#ifndef OPENSSL_NO_RSA
	  dbg_fprintf ("%s: registering RSA\n", __FUNCTION__);
#ifdef OLDER_OPENSSL
	  ENGINE_set_RSA (e, &hsm_rsa);
#else
	  ENGINE_set_RSA (e, hsm_rsa);
	  hsm_rsa = RSA_meth_new ("PKCS#11 RSA", 0);
	  if (hsm_rsa == NULL)
	    {
	      dbg_fprintf ("%s: registering RSA failed\n", __FUNCTION__);
	      goto err;
	    }
	  RSA_meth_set_priv_enc (hsm_rsa, hsm_RSA_private_encrypt);
	  RSA_meth_set_init (hsm_rsa, hsm_RSA_init);
	  RSA_meth_set_finish (hsm_rsa, hsm_RSA_finish);
#endif
	  ENGINE_set_load_privkey_function (e, hsm_load_privkey);

#endif
	  break;
	case CKM_ECDSA:
	case CKM_ECDSA_SHA1:
	case CKM_ECDSA_SHA224:
	case CKM_ECDSA_SHA256:
	case CKM_ECDSA_SHA384:
	case CKM_ECDSA_SHA512:
#ifndef OPENSSL_NO_ECDSA
	  dbg_fprintf ("%s: registering ECDSA\n", __FUNCTION__);
#ifdef OLDER_OPENSSL
	  ENGINE_set_ECDSA (e, &hsm_ecdsa);
#else

#if OPENSSL_VERSION_NUMBER >= 0x10100000L && !defined(LIBRESSL_VERSION_NUMBER)

	  int (*orig_sign) (int, const unsigned char *, int, unsigned char *,
			    unsigned int *, const BIGNUM *, const BIGNUM *,
			    EC_KEY *) = NULL;

	  hsm_ec_meth =
	    EC_KEY_METHOD_new ((EC_KEY_METHOD *) EC_KEY_OpenSSL ());
	  EC_KEY_METHOD_get_sign (hsm_ec_meth, &orig_sign, NULL, NULL);
	  EC_KEY_METHOD_set_sign (hsm_ec_meth, orig_sign, NULL,
				  hsm_ECDSA_sign);
	  ENGINE_set_EC (e, hsm_ec_meth);

#else
	  ENGINE_set_ECDSA (e, hsm_ecdsa);
	  hsm_ecdsa = ECDSA_METHOD_new (NULL);
	  if (hsm_ecdsa == NULL)
	    {
	      dbg_fprintf ("%s: registering ECDSA failed\n", __FUNCTION__);
	      goto err;
	    }
	  ECDSA_METHOD_set_name (hsm_ecdsa, "PKCS#11 ECDSA");
	  ECDSA_METHOD_set_sign (hsm_ecdsa, hsm_ECDSA_sign);
	  ECDSA_METHOD_set_sign_setup (hsm_ecdsa, hsm_ECDSA_sign_setup);
#endif
#endif
	  ENGINE_set_load_privkey_function (e, hsm_load_privkey);
#endif
	  break;
	case CKM_SHA_1:
	  tok->hsm_implemented_digests[NID_sha1] = 1;
	  num_digest_nids++;
	  break;
	case CKM_SHA_1_HMAC:
	case CKM_SHA_1_HMAC_GENERAL:
	  tok->hsm_implemented_digests[NID_hmacWithSHA1] = 1;
	  num_digest_nids++;
	  break;
	case CKM_PBA_SHA1_WITH_SHA1_HMAC:
	case CKM_SHA1_KEY_DERIVATION:
	case CKM_SHA1_RSA_PKCS:
	  tok->hsm_implemented_digests[NID_sha1WithRSAEncryption] = 1;
	  num_digest_nids++;
	  break;

	case CKM_SHA224:
	  tok->hsm_implemented_digests[NID_sha224] = 1;
	  num_digest_nids++;
	  break;
	case CKM_SHA224_KEY_DERIVATION:
	case CKM_SHA224_RSA_PKCS:
	  tok->hsm_implemented_digests[NID_sha224WithRSAEncryption] = 1;
	  num_digest_nids++;
	  break;

	case CKM_SHA256:
	  tok->hsm_implemented_digests[NID_sha256] = 1;
	  num_digest_nids++;
	  break;
	case CKM_SHA256_KEY_DERIVATION:
	case CKM_SHA256_RSA_PKCS:
	  tok->hsm_implemented_digests[NID_sha256WithRSAEncryption] = 1;
	  num_digest_nids++;
	  break;

	case CKM_SHA384:
	  tok->hsm_implemented_digests[NID_sha384] = 1;
	  num_digest_nids++;
	  break;
	case CKM_SHA384_KEY_DERIVATION:
	case CKM_SHA384_RSA_PKCS:
	  tok->hsm_implemented_digests[NID_sha384WithRSAEncryption] = 1;
	  num_digest_nids++;
	  break;
	case CKM_SHA512:
	  tok->hsm_implemented_digests[NID_sha512] = 1;
	  num_digest_nids++;
	  break;
	case CKM_SHA512_KEY_DERIVATION:
	case CKM_SHA512_RSA_PKCS:
	  tok->hsm_implemented_digests[NID_sha512WithRSAEncryption] = 1;
	  num_digest_nids++;
	  break;
	default:
	  break;
	}
    }

err_free:OPENSSL_free (mech_list);
err:return;
}

struct _token *
hsm_add_token (CK_SLOT_ID slot_id)
{
  struct _token *new_tok =
    (struct _token *) OPENSSL_malloc (sizeof (struct _token));

  dbg_fprintf ("%s\n", __FUNCTION__);
  if (new_tok == NULL)
    {
      hsm_err (HSM_F_ADDTOKEN, HSM_R_MALLOC_FAILURE);
      return NULL;
    }

  memset (new_tok, 0, sizeof (struct _token));
  new_tok->slot_id = slot_id;
  new_tok->pin = NULL;

  new_tok->token_next = hsm_token_list;
  hsm_token_list = new_tok;

  return new_tok;
}

static int
pre_init_hsm (ENGINE * e)
{

  CK_C_GetFunctionList p;
  CK_RV rv = CKR_OK;
  CK_INFO Info;
  CK_SLOT_ID_PTR pSlotList;
  CK_ULONG ulSlotCount;
  CK_SLOT_INFO slotInfo;
  struct _token *tok;
  int i;

  dbg_fprintf ("%s\n", __FUNCTION__);
  if (hsm_dso)
    {
      hsm_err (HSM_F_PREINIT, HSM_R_ALREADY_LOADED);
      goto err;
    }

  hsm_dso = dlopen (get_HSM_LIBNAME (), DLOPEN_FLAG);

  if (hsm_dso == NULL)
    {
      hsm_err (HSM_F_PREINIT, HSM_R_DSO_FAILURE);
      goto err;
    }

  p = (CK_C_GetFunctionList) dlsym (hsm_dso, HSM_GET_FUNCTION_LIST);
  if (!p)
    {
      hsm_err (HSM_F_PREINIT, HSM_R_DSO_FAILURE);
      goto err;
    }

  rv = p (&pFunctionList);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_PREINIT, HSM_R_DSO_FAILURE, rv);
      goto err;
    }

  rv = pFunctionList->C_Initialize (NULL);
  if ((rv != CKR_OK) && (rv != CKR_CRYPTOKI_ALREADY_INITIALIZED))
    {
      hsm_die (HSM_F_PREINIT, HSM_R_INITIALIZE, rv);
      goto err;
    }

  rv = pFunctionList->C_GetInfo (&Info);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_PREINIT, HSM_R_GETINFO, rv);
      pFunctionList->C_Finalize (NULL);
      goto err;
    }

  /* get a list of slots in the system */
  rv = pFunctionList->C_GetSlotList (TRUE, NULL_PTR, &ulSlotCount);
  if ((rv != CKR_OK) || (ulSlotCount == 0))
    {
      hsm_die (HSM_F_PREINIT, HSM_R_GETSLOTLIST, rv);
    }
  else
    {
      pSlotList =
	(CK_SLOT_ID_PTR) OPENSSL_malloc (ulSlotCount * sizeof (CK_SLOT_ID));
      if (pSlotList != NULL)
	{
	  rv = pFunctionList->C_GetSlotList (TRUE, pSlotList, &ulSlotCount);
	  if (rv != CKR_OK)
	    {
	      hsm_die (HSM_F_PREINIT, HSM_R_GETSLOTLIST, rv);
	      pFunctionList->C_Finalize (NULL);
	      OPENSSL_free (pSlotList);
	      goto err;
	    }

	  for (i = 0; i < ulSlotCount; i++)
	    {
	      rv = pFunctionList->C_GetSlotInfo (pSlotList[i], &slotInfo);
	      if (rv != CKR_OK)
		{
		  hsm_die (HSM_F_PREINIT, HSM_R_GETSLOTINFO, rv);
		  pFunctionList->C_Finalize (NULL);
		  OPENSSL_free (pSlotList);
		  goto err;
		}

	      tok = hsm_add_token (pSlotList[i]);
	      hsm_register_token (e, tok);
	    }
	  OPENSSL_free (pSlotList);
	}
    }

  /* Indicate that we finished with the Cryptoki library */
  pFunctionList->C_Finalize (NULL);
  dlclose (hsm_dso);
  hsm_dso = NULL;

  return 1;

err:if (hsm_dso)
    dlclose (hsm_dso);
  hsm_dso = NULL;
  return 0;
}

/*Initialisation function */
static int
hsm_init (ENGINE * e)
{
  CK_C_GetFunctionList p;
  CK_RV rv = CKR_OK;
  CK_INFO Info;
  CK_SLOT_ID_PTR pSlotList;
  CK_ULONG ulSlotCount;
  CK_SLOT_INFO slotInfo;
  struct _token *tok;
  int i;

  dbg_fprintf ("%s\n", __FUNCTION__);
  if (hsm_dso)
    {
      hsm_err (HSM_F_INIT, HSM_R_ALREADY_LOADED);
      goto err;
    }
  /* Attempt to load PKCS#11 library */
  hsm_dso = dlopen (get_HSM_LIBNAME (), DLOPEN_FLAG);

  if (hsm_dso == NULL)
    {
      hsm_err (HSM_F_INIT, HSM_R_DSO_FAILURE);
      goto err;
    }

  p = (CK_C_GetFunctionList) dlsym (hsm_dso, HSM_GET_FUNCTION_LIST);
  if (!p)
    {
      hsm_err (HSM_F_INIT, HSM_R_DSO_FAILURE);
      goto err;
    }

  rv = p (&pFunctionList);

  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_INIT, HSM_R_DSO_FAILURE, rv);
      goto err;
    }

  rv = pFunctionList->C_Initialize (NULL_PTR);
  if ((rv != CKR_OK) && (rv != CKR_CRYPTOKI_ALREADY_INITIALIZED))
    {
      hsm_die (HSM_F_INIT, HSM_R_INITIALIZE, rv);
      goto err;
    }

  rv = pFunctionList->C_GetInfo (&Info);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_INIT, HSM_R_GETINFO, rv);
      pFunctionList->C_Finalize (NULL);
      goto err;
    }

  rv = pFunctionList->C_GetSlotList (TRUE, NULL_PTR, &ulSlotCount);
  if ((rv != CKR_OK) || (ulSlotCount == 0))
    {
      hsm_die (HSM_F_INIT, HSM_R_GETSLOTLIST, rv);
    }
  else
    {
      pSlotList =
	(CK_SLOT_ID_PTR) OPENSSL_malloc (ulSlotCount * sizeof (CK_SLOT_ID));
      if (pSlotList != NULL)
	{
	  rv = pFunctionList->C_GetSlotList (TRUE, pSlotList, &ulSlotCount);
	  if (rv != CKR_OK)
	    {
	      hsm_die (HSM_F_INIT, HSM_R_GETSLOTLIST, rv);
	      pFunctionList->C_Finalize (NULL);
	      OPENSSL_free (pSlotList);
	      goto err;
	    }

	  for (i = 0; i < ulSlotCount; i++)
	    {
	      rv = pFunctionList->C_GetSlotInfo (pSlotList[i], &slotInfo);
	      if (rv != CKR_OK)
		{
		  hsm_die (HSM_F_INIT, HSM_R_GETSLOTINFO, rv);
		  pFunctionList->C_Finalize (NULL);
		  OPENSSL_free (pSlotList);
		  goto err;
		}

	      tok = hsm_add_token (pSlotList[i]);
	      hsm_register_token (e, tok);
	    }
	  OPENSSL_free (pSlotList);
	}
    }

#ifndef OPENSSL_NO_RSA
  if (rsa_privkey_idx == -1)
    rsa_privkey_idx = RSA_get_ex_new_index (0, NULL, NULL, NULL, NULL);
  if (rsa_session_idx == -1)
    rsa_session_idx = RSA_get_ex_new_index (0, NULL, NULL, NULL, NULL);
#endif

#ifndef OPENSSL_NO_ECDSA
  if (ecdsa_privkey_idx == -1)
#ifdef OLDER_OPENSSL
    ecdsa_privkey_idx = ECDSA_get_ex_new_index (0, NULL, NULL, NULL, 0);
#else
    ecdsa_privkey_idx = EC_KEY_get_ex_new_index (0, NULL, NULL, NULL, 0);
#endif
  if (ecdsa_session_idx == -1)
#ifdef OLDER_OPENSSL
    ecdsa_session_idx = ECDSA_get_ex_new_index (0, NULL, NULL, NULL, 0);
#else
    ecdsa_session_idx = EC_KEY_get_ex_new_index (0, NULL, NULL, NULL, 0);
#endif
#endif

  if (hsm_token_list == NULL)
    hsm_err (HSM_F_INIT, HSM_R_NOTOKENS);

  HSM_Initialized = 1;

  pthread_atfork (NULL, NULL, (void (*)()) hsm_atfork_init);

  return 1;

err:if (hsm_dso)
    {
      dlclose (hsm_dso);
    }
  hsm_dso = NULL;
  return 0;
}

/* Destructor (complements the "engine_hsm()" constructor) */
static int
hsm_destroy (ENGINE * e)
{
  dbg_fprintf ("%s\n", __FUNCTION__);

#ifndef OLDER_OPENSSL
  hsm_sha1_destroy ();
  hsm_sha224_destroy ();
  hsm_sha256_destroy ();
  hsm_sha384_destroy ();
  hsm_sha512_destroy ();
#endif

  free_HSM_LIBNAME ();
  ERR_unload_hsm_strings ();
  return 1;
}

static int
hsm_finish (ENGINE * e)
{
  struct _token *tmp;
  struct token_session *wrapper = NULL;
  dbg_fprintf ("%s\n", __FUNCTION__);

  if (hsm_dso == NULL)
    {
      hsm_err (HSM_F_FINISH, HSM_R_NOT_LOADED);
      goto err;
    }
  assert (pFunctionList != NULL);

  while (hsm_token_list)
    {
      tmp = hsm_token_list->token_next;
      OPENSSL_free (hsm_token_list);
      hsm_token_list = tmp;
    }

  pFunctionList->C_Finalize (NULL);

  if (dlclose (hsm_dso))
    {
      hsm_err (HSM_F_FINISH, HSM_R_DSO_FAILURE);
      goto err;
    }
  hsm_dso = NULL;
  pFunctionList = NULL;

  wrapper = hsm_get_session ();
  OPENSSL_free (wrapper);

  return 1;

err:hsm_dso = NULL;
  pFunctionList = NULL;
  return 0;
}

/* Loads a certificate by its ID */
int
load_certificate (ENGINE * e, void *p)
{
  struct
  {
    const char *certid;
    X509 *cert;
  } *parms = p;

  dbg_fprintf ("%s\n", __FUNCTION__);
  if (parms->cert != NULL)
    return 0;
  parms->cert = hsm_find_certificate (e, parms->certid);
  if (parms->cert == NULL)
    return 0;

  return 1;
}

static int
hsm_ctrl (ENGINE * e, int cmd, long i, void *p, void (*f) ())
{
  int initialized = ((hsm_dso == NULL) ? 0 : 1);
  struct _token *tok;

  dbg_fprintf ("%s\n", __FUNCTION__);
  switch (cmd)
    {
    case HSM_CMD_MODULE_PATH:
      if (p == NULL)
	{
	  hsm_err (HSM_F_CTRL, ERR_R_PASSED_NULL_PARAMETER);
	  return 0;
	}
      if (initialized)
	{
	  /*hsm_err(HSM_F_CTRL, HSM_R_ALREADY_LOADED);
	     return 0; */
	}
      if (!set_HSM_LIBNAME ((const char *) p))
	return 0;
      return pre_init_hsm (e);
    case HSM_CMD_SLOT_ID:
      tok = hsm_token_list;
      while (tok)
	{
	  dbg_fprintf ("slot %ld found\n", tok->slot_id);
	  if (tok->slot_id == i)
	    {
	      hsm_token = tok;
	      dbg_fprintf ("slot %ld selected\n", i);
	      return 1;
	    }
	  tok = tok->token_next;
	}
      hsm_err (HSM_F_CTRL, HSM_R_TOKEN_NOT_AVAILABLE);
      return 0;
    case HSM_CMD_PIN:
      if (p == NULL)
	{
	  hsm_err (HSM_F_CTRL, ERR_R_PASSED_NULL_PARAMETER);
	  return 0;
	}
      if (!hsm_token)
	{
	  hsm_err (HSM_F_CTRL, HSM_R_NO_SLOT_SELECTED);
	  return 0;
	}
      hsm_token->pin = OPENSSL_strdup (p);
      break;
    case HSM_CMD_LOAD_CERT:
      if (p == NULL)
	{
	  hsm_err (HSM_F_CTRL, ERR_R_PASSED_NULL_PARAMETER);
	  return 0;
	}
      return load_certificate (e, p);
    default:
      break;
    }
  /*hsm_err(HSM_F_CTRL, HSM_R_CTRL_COMMAND_NOT_IMPLEMENTED); */

  return 0;
}

EVP_PKEY *
hsm_find_privkey (CK_SESSION_HANDLE session, CK_BYTE_PTR * key_id,
		  CK_ULONG key_len)
{

  EVP_PKEY *pkey = NULL;
  CK_OBJECT_HANDLE hKey = CK_INVALID_HANDLE;
  CK_ULONG matches;
  CK_RV rv;
  CK_ULONG exp_size = 0, mod_size = 0;
  CK_BYTE_PTR mod = NULL;
  CK_BYTE_PTR exp = NULL;
  int i;
  CK_ULONG kt;
  BIGNUM *bnN = NULL;
  BIGNUM *bnE = NULL;

  CK_OBJECT_CLASS oKey = CKO_PRIVATE_KEY;

  CK_ATTRIBUTE findobj_tmple[] = { {CKA_CLASS, &oKey, sizeof (CK_OBJECT_CLASS)}
  ,
  {CKA_ID, (void *) key_id, key_len}
  };

  CK_ATTRIBUTE key_type[] = { {CKA_CLASS, &oKey, sizeof (oKey)}
  , {
     CKA_KEY_TYPE, &kt, sizeof (kt)}
  };

  CK_ULONG ulCount = sizeof (findobj_tmple) / sizeof (CK_ATTRIBUTE);

  dbg_fprintf ("%s\n", __FUNCTION__);

  rv = pFunctionList->C_FindObjectsInit (session, findobj_tmple, ulCount);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDKEY, HSM_R_FINDOBJECTSINIT, rv);
      goto err;
    }

  rv = pFunctionList->C_FindObjects (session, &hKey, 1, &matches);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDKEY, HSM_R_FINDOBJECTS, rv);
      goto err;
    }

  rv = pFunctionList->C_FindObjectsFinal (session);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDKEY, HSM_R_FINDOBJECTSFINAL, rv);
      goto err;
    }

  dbg_fprintf ("Find: %d count: %ld\n", rv, matches);

  if (!matches)
    {
      dbg_fprintf ("Key not found on token\n");
      goto err;
    }

  /* get key type */
  ulCount = sizeof (key_type) / sizeof (CK_ATTRIBUTE);
  rv = pFunctionList->C_GetAttributeValue (session, hKey, key_type, ulCount);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDKEY, HSM_R_GETATTRIBUTVALUE, rv);
      goto err;
    }

  if (kt == CKK_RSA)
    {
      CK_ATTRIBUTE pub_rsa_attrs[] = {
	{CKA_PUBLIC_EXPONENT, exp, exp_size}
	, {CKA_MODULUS, mod,
	   mod_size}
      };
      RSA *rsa = RSA_new ();
      ulCount = sizeof (pub_rsa_attrs) / sizeof (CK_ATTRIBUTE);
      /*to pass X509_check_private_key we need to fill RSA with public key parameters */
      rv = pFunctionList->C_GetAttributeValue (session, hKey, pub_rsa_attrs,
					       ulCount);
      if (rv != CKR_OK)
	{
	  hsm_die (HSM_F_FINDKEY, HSM_R_GETATTRIBUTVALUE, rv);
	  goto err;
	}
      exp = (CK_BYTE_PTR) OPENSSL_malloc (pub_rsa_attrs[0].ulValueLen);
      mod = (CK_BYTE_PTR) OPENSSL_malloc (pub_rsa_attrs[1].ulValueLen);
      pub_rsa_attrs[0].pValue = exp;
      pub_rsa_attrs[1].pValue = mod;

      rv = pFunctionList->C_GetAttributeValue (session, hKey, pub_rsa_attrs,
					       ulCount);

      if (rv != CKR_OK)
	{
	  hsm_die (HSM_F_FINDKEY, HSM_R_GETATTRIBUTVALUE, rv);
	  goto err;
	}
      if ((bnE = BN_bin2bn (pub_rsa_attrs[0].pValue,
			    pub_rsa_attrs[0].ulValueLen, NULL)) == NULL)
	{
	  hsm_die (HSM_F_FINDKEY, HSM_R_BIGNUM, rv);
	  goto err;
	}

      if ((bnN = BN_bin2bn (pub_rsa_attrs[1].pValue,
			    pub_rsa_attrs[1].ulValueLen, NULL)) == NULL)
	{
	  hsm_die (HSM_F_FINDKEY, HSM_R_BIGNUM, rv);
	  goto err;
	}
#ifdef OLDER_OPENSSL
      rsa->e = bnE;
      rsa->n = bnN;
#else
      if (!RSA_set0_key (rsa, bnN, bnE, NULL))
	{
	  hsm_die (HSM_F_FINDKEY, HSM_R_BIGNUM, rv);
	  goto err;
	}
#endif
      RSA_set_ex_data (rsa, rsa_privkey_idx, (void *) hKey);
      pkey = EVP_PKEY_new ();
      EVP_PKEY_set1_RSA (pkey, rsa);
#ifdef HSM_DEBUG
      fprintf (stdout, "e: %s\n", BN_bn2dec (bnE));
      fprintf (stdout, "n: %s\n", BN_bn2dec (bnN));
#endif
    }
  else if (kt == CKK_EC)
    {
      CK_ATTRIBUTE ecdsa_pub[] = { {CKA_ID, NULL, 0}
      , {CKA_CLASS,
	 &oKey, sizeof (oKey)}
      , {CKA_KEY_TYPE, &kt, sizeof (kt)}
      };
      CK_ATTRIBUTE ecdsa_attrs[] = { {CKA_EC_PARAMS, NULL, 0}
      , {
	 CKA_EC_POINT, NULL, 0}
      };
      CK_OBJECT_HANDLE hPbKey;
      CK_ULONG found;
      oKey = CKO_PUBLIC_KEY;

      if (((rv = pFunctionList->C_GetAttributeValue (session, hKey,
						     ecdsa_pub, 1)) == CKR_OK)
	  && ((ecdsa_pub[0].pValue = OPENSSL_malloc (ecdsa_pub[0].ulValueLen))
	      != NULL)
	  &&
	  ((rv =
	    pFunctionList->C_GetAttributeValue (session, hKey, ecdsa_pub,
						1)) == CKR_OK)
	  && ((rv = pFunctionList->C_FindObjectsInit (session, ecdsa_pub, 3))
	      == CKR_OK)
	  &&
	  ((rv =
	    pFunctionList->C_FindObjects (session, &hPbKey, 1,
					  &found)) == CKR_OK)
	  && ((rv = pFunctionList->C_FindObjectsFinal (session)) == CKR_OK)
	  &&
	  ((rv =
	    pFunctionList->C_GetAttributeValue (session, hPbKey, ecdsa_attrs,
						2)) == CKR_OK)
	  &&
	  ((ecdsa_attrs[0].pValue =
	    OPENSSL_malloc (ecdsa_attrs[0].ulValueLen)) != NULL)
	  &&
	  ((ecdsa_attrs[1].pValue =
	    OPENSSL_malloc (ecdsa_attrs[1].ulValueLen)) != NULL)
	  &&
	  ((rv =
	    pFunctionList->C_GetAttributeValue (session, hPbKey, ecdsa_attrs,
						2)) == CKR_OK))
	{

	  const unsigned char *ptr1 = ecdsa_attrs[0].pValue;
	  const unsigned char *ptr2 = ecdsa_attrs[1].pValue;
	  CK_ULONG len1 = ecdsa_attrs[0].ulValueLen;
	  CK_ULONG len2 = ecdsa_attrs[1].ulValueLen;
	  ASN1_OCTET_STRING *point = NULL;
	  EC_KEY *ecdsa = NULL;

	  /* Fill pirvate key with public key parameters to pass the certificate/private key consistency check later */
	  if ((point = d2i_ASN1_OCTET_STRING (NULL, &ptr2, len2)))
	    {
	      /* Pointing to OCTET STRING content */
	      ptr2 = point->data;
	      len2 = point->length;
	    }
	  else
	    {
	      /* No OCTET STRING */
	      ptr2 = ecdsa_attrs[1].pValue;
	    }

	  if ((d2i_ECParameters (&ecdsa, &ptr1, len1) == NULL)
	      || (o2i_ECPublicKey (&ecdsa, &ptr2, len2) == NULL))
	    {
	      EC_KEY_free (ecdsa);
	      ecdsa = NULL;
	    }

	  EC_KEY_set_private_key (ecdsa, BN_value_one ());

	  if (point)
	    {
	      ASN1_STRING_free (point);
	    }

	  if (ecdsa)
	    {
	      if ((pkey = EVP_PKEY_new ()) != NULL)
		{

#ifdef OLDER_OPENSSL
		  ECDSA_set_ex_data (ecdsa, ecdsa_privkey_idx, hKey);
#else
		  EC_KEY_set_ex_data (ecdsa, ecdsa_privkey_idx, hKey);
#endif
		  EVP_PKEY_set1_EC_KEY (pkey, ecdsa);
		}
	    }
	}

    }				// else if (kt == CKK_EC)
err:return pkey;
}

/* Public certificate loader. It loads cert by id in DER format and convert it to PEM */
static X509 *
hsm_find_certificate (ENGINE * e, const char *cert_id)
{
  X509 *x509 = NULL;
  BIO *cbio = NULL;
  struct token_session *wrapper = NULL;
  CK_SESSION_HANDLE hSession = NULL;
  CK_OBJECT_CLASS ObjClass = CKO_CERTIFICATE;
  CK_ULONG cert_size = 0;
  CK_ULONG ulCount = 0;
  CK_OBJECT_HANDLE hCert = CK_INVALID_HANDLE;
  CK_RV rv;
  CK_ULONG matches;
  CK_BYTE_PTR cert_der = NULL;
  unsigned char *hcert_id = NULL;
  size_t hcert_idlen;

  CK_ATTRIBUTE findobj_tmple[] = { {CKA_CLASS, &ObjClass, sizeof (ObjClass)}
  , {
     CKA_ID, (void *) 0, 0}
  };

  CK_ATTRIBUTE attrval_tmple[] = { {CKA_VALUE, cert_der, cert_size}, {CKA_ID,
								      (void *)
								      0, 0}
  };

  dbg_fprintf ("%s\n", __FUNCTION__);

  if (hSession == CK_INVALID_HANDLE || !hSession)
    {
      wrapper = hsm_get_session ();
      if (!wrapper)
	return 0;
      hSession = wrapper->session;
    }

  ulCount = sizeof (findobj_tmple) / sizeof (CK_ATTRIBUTE);

  hcert_id = hex2bin (cert_id, &hcert_idlen);
  findobj_tmple[1].pValue = hcert_id;
  findobj_tmple[1].ulValueLen = hcert_idlen;

  rv =
    pFunctionList->C_FindObjectsInit (wrapper->session, findobj_tmple,
				      ulCount);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDCERT, HSM_R_FINDOBJECTSINIT, rv);
      goto err;
    }

  rv = pFunctionList->C_FindObjects (wrapper->session, &hCert, 1, &matches);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDCERT, HSM_R_FINDOBJECTS, rv);
      goto err;
    }

  if (!matches)
    {
      dbg_fprintf ("Cert %s not found on token\n", cert_id);
      hsm_die (HSM_F_FINDCERT, HSM_R_FINDOBJECTS, rv);
      goto err;
    }

  ulCount = sizeof (attrval_tmple) / sizeof (CK_ATTRIBUTE);

  rv =
    pFunctionList->C_GetAttributeValue (wrapper->session, hCert,
					attrval_tmple, ulCount);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDCERT, HSM_R_GETATTRIBUTVALUE, rv);
      goto err;
    }

  cert_der = (CK_BYTE_PTR) OPENSSL_malloc (attrval_tmple[0].ulValueLen);
  attrval_tmple[0].pValue = cert_der;

  rv =
    pFunctionList->C_GetAttributeValue (wrapper->session, hCert,
					attrval_tmple, ulCount);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDCERT, HSM_R_GETATTRIBUTVALUE, rv);
      goto err;
    }

  if ((cbio =
       BIO_new_mem_buf (cert_der, attrval_tmple[0].ulValueLen)) == NULL)
    {
      goto err;
    }
  if (!d2i_X509_bio (cbio, &x509))
    goto err;
#ifdef HSM_DEBUG
  PEM_write_X509 (stdout, x509);
#endif
  rv = pFunctionList->C_FindObjectsFinal (wrapper->session);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_FINDCERT, HSM_R_FINDOBJECTSFINAL, rv);
      goto err;
    }
err:BIO_free (cbio);
  return x509;

}

static EVP_PKEY *
hsm_load_privkey (ENGINE * e, const char *key_id,
		  UI_METHOD * ui_method, void *callback_data)
{

  EVP_PKEY *pkey = NULL;
  RSA *rsa = NULL;
  unsigned char *hkey_id;
  size_t hkey_idlen;

  dbg_fprintf ("%s\n", __FUNCTION__);

  if (!key_id)
    goto err;

  struct token_session *wrapper = NULL;
  CK_SESSION_HANDLE session = CK_INVALID_HANDLE;
  wrapper = hsm_get_session ();
  if (!wrapper)
    return 0;
  dbg_fprintf ("%d: created new session\n", __LINE__);
  session = wrapper->session;
  hkey_id = hex2bin (key_id, &hkey_idlen);
  pkey = hsm_find_privkey (session, (CK_BYTE_PTR *) hkey_id,
			   (CK_ULONG) hkey_idlen);
err:return pkey;
}

static int
hsm_RSA_init (RSA * rsa)
{
  struct token_session *wrapper;

  dbg_fprintf ("%s\n", __FUNCTION__);

  wrapper = hsm_get_session ();
  if (wrapper)
    RSA_set_ex_data (rsa, rsa_session_idx, (void *) wrapper->session);

  RSA_blinding_off (rsa);

  return 1;
}

static int
hsm_RSA_finish (RSA * rsa)
{
  CK_RV rv;

  struct token_session *wrapper = NULL;
  CK_SESSION_HANDLE session;
  int err = 0;

  dbg_fprintf ("%s\n", __FUNCTION__);
#ifdef OLDER_OPENSSL
  if (rsa->_method_mod_n != NULL)
    BN_MONT_CTX_free (rsa->_method_mod_n);
  if (rsa->_method_mod_p != NULL)
    BN_MONT_CTX_free (rsa->_method_mod_p);
  if (rsa->_method_mod_q != NULL)
    BN_MONT_CTX_free (rsa->_method_mod_q);
#endif

  session = (CK_SESSION_HANDLE) RSA_get_ex_data (rsa, rsa_session_idx);

  if (session == CK_INVALID_HANDLE || !session)
    {
      wrapper = hsm_get_session ();
      if (!wrapper)
	return 0;
      session = wrapper->session;
    }

  rv = pFunctionList->C_CloseSession (session);
  RSA_set_ex_data (rsa, rsa_session_idx, (void *) CK_INVALID_HANDLE);
  err = 1;
out:
  return err;
}

static int
hsm_RSA_private_encrypt (int flen, const unsigned char *from,
			 unsigned char *to, RSA * rsa, int padding)
{
  CK_ULONG ulSignatureLen = 0;
  CK_RV rv;
  CK_MECHANISM Mechanism_rsa = { CKM_RSA_PKCS, NULL, 0 };
  CK_MECHANISM *pMechanism = &Mechanism_rsa;
  CK_OBJECT_HANDLE hpkey = CK_INVALID_HANDLE;
  struct token_session *wrapper = NULL;
  CK_SESSION_HANDLE session;

  dbg_fprintf ("%s\n", __FUNCTION__);

  if (padding != RSA_PKCS1_PADDING)
    {
      hsm_err (HSM_F_RSA_PRIV_ENC, HSM_R_UNKNOWN_PADDING_TYPE);
      return -1;
    }

  session = (CK_SESSION_HANDLE) RSA_get_ex_data (rsa, rsa_session_idx);
  if (session == CK_INVALID_HANDLE || !session)
    {
      wrapper = hsm_get_session ();
      if (!wrapper)
	return 0;

      dbg_fprintf ("%d: created new session\n", __LINE__);
      session = wrapper->session;
      RSA_set_ex_data (rsa, rsa_session_idx, (void *) session);
    }

  hpkey = (CK_OBJECT_HANDLE) RSA_get_ex_data (rsa, rsa_privkey_idx);
  if (hpkey == CK_INVALID_HANDLE)
    {
      hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGNINIT, rv);
      goto out;
    }

  if (hpkey != CK_INVALID_HANDLE)
    {
      rv = pFunctionList->C_SignInit (session, pMechanism, hpkey);
      if (rv != CKR_OK)
	{
	  hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGNINIT, rv);
	  ulSignatureLen = -1;
	  goto out;
	}

      rv = pFunctionList->C_Sign (session, (unsigned char *) from, flen,
				  NULL_PTR, &ulSignatureLen);
      if (rv != CKR_OK)
	{
	  hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGN, rv);
	  ulSignatureLen = -1;
	  goto out;
	}

      rv = pFunctionList->C_Sign (session, (unsigned char *) from, flen, to,
				  &ulSignatureLen);
      if (rv != CKR_OK)
	{
	  hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGN, rv);
	  ulSignatureLen = -1;
	  goto out;
	}

    }

out:
  return ulSignatureLen;
}

static inline int
get_mech (int alg, EVP_CIPHER_CTX * ctx)
{
  switch (alg)
    {
    case alg_sha:
      return CKM_SHA_1;
    case alg_sha224:
      return CKM_SHA224;
    case alg_sha256:
      return CKM_SHA256;
    case alg_sha384:
      return CKM_SHA384;
    case alg_sha512:
      return CKM_SHA512;
    default:
      return -1;
    }
}

int
hsm_ECDSA_sign_setup (EC_KEY * eckey, BN_CTX * ctx_in, BIGNUM ** kinvp,
		      BIGNUM ** rp)
{
  struct token_session *wrapper;
  dbg_fprintf ("%s\n", __FUNCTION__);
  wrapper = hsm_get_session ();
  if (wrapper)
    {
#ifdef OLDER_OPENSSL
      ECDSA_set_ex_data (eckey, ecdsa_session_idx, (void *) wrapper->session);
#else
      EC_KEY_set_ex_data (eckey, ecdsa_session_idx,
			  (void *) wrapper->session);
#endif
    }

  return 1;
}

static ECDSA_SIG *
hsm_ECDSA_sign (const unsigned char *dgst, int dgst_len,
		const BIGNUM * kinv, const BIGNUM * rp, EC_KEY * ecdsa)
{

  CK_MECHANISM mech = { CKM_ECDSA, NULL_PTR, 0 };
  CK_ULONG tlen = 0;
  CK_RV rv;
  CK_OBJECT_HANDLE hpkey = CK_INVALID_HANDLE;
  struct token_session *wrapper = NULL;
  CK_SESSION_HANDLE session;
  CK_BYTE_PTR buf = NULL;
  ECDSA_SIG *rval;
  BIGNUM *r, *s;
  int nlen;

  dbg_fprintf ("%s\n", __FUNCTION__);

#ifdef OLDER_OPENSSL
  session = (CK_SESSION_HANDLE) ECDSA_get_ex_data (ecdsa, ecdsa_session_idx);
#else
  session = (CK_SESSION_HANDLE) EC_KEY_get_ex_data (ecdsa, ecdsa_session_idx);
#endif

  if (session == CK_INVALID_HANDLE || !session)
    {
      wrapper = hsm_get_session ();
      if (!wrapper)
	return NULL;

      dbg_fprintf ("%d: created new session\n", __LINE__);
      session = wrapper->session;
#ifdef OLDER_OPENSSL
      ECDSA_set_ex_data (ecdsa, ecdsa_session_idx, (void *) session);
#else
      EC_KEY_set_ex_data (ecdsa, ecdsa_session_idx, (void *) session);
#endif

    }

#ifdef OLDER_OPENSSL
  hpkey = (CK_OBJECT_HANDLE) ECDSA_get_ex_data (ecdsa, ecdsa_privkey_idx);
#else
  hpkey = (CK_OBJECT_HANDLE) EC_KEY_get_ex_data (ecdsa, ecdsa_privkey_idx);
#endif

  if (hpkey == CK_INVALID_HANDLE)
    {
      hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGNINIT, rv);
      return NULL;
    }

  if (((rv = pFunctionList->C_SignInit (session, &mech, hpkey)) != CKR_OK))
    {
      hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGNINIT, rv);
      return NULL;
    }
  /* Make a call to C_Sign to find out the size of the signature */
  rv = pFunctionList->C_Sign (session, (CK_BYTE *) dgst, dgst_len, NULL,
			      &tlen);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGN, rv);
      return NULL;
    }

  if ((buf = OPENSSL_malloc (tlen)) == NULL)
    {
      hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_MALLOC_FAILURE, rv);
      return NULL;
    }

  rv =
    pFunctionList->C_Sign (session, (CK_BYTE *) dgst, dgst_len, buf, &tlen);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGN, rv);
      OPENSSL_free (buf);
      return NULL;
    }

  nlen = tlen / 2;
  r = BN_new ();
  s = BN_new ();
  BN_bin2bn (&buf[0], nlen, r);
  BN_bin2bn (&buf[nlen], nlen, s);
#ifdef HSM_DEBUG
  fprintf (stdout, "r: %s\n", BN_bn2dec (r));
  fprintf (stdout, "s: %s\n", BN_bn2dec (s));
#endif
  if ((rval = ECDSA_SIG_new ()) != NULL)
    {
#ifdef OLDER_OPENSSL
      rval->r = r;
      rval->s = s;
#else
      if (!ECDSA_SIG_set0 (rval, r, s))
	{
	  hsm_die (HSM_F_RSA_PRIV_ENC, HSM_R_SIGN, rv);
	  rval = NULL;
	}
#endif
    }
  OPENSSL_free (buf);
  return rval;

}

static inline int
hsm_sha1_init (EVP_MD_CTX * ctx)
{
  return hsm_digest_init (ctx, alg_sha);
}

static inline int
hsm_sha224_init (EVP_MD_CTX * ctx)
{
  return hsm_digest_init (ctx, alg_sha224);
}

static inline int
hsm_sha256_init (EVP_MD_CTX * ctx)
{
  return hsm_digest_init (ctx, alg_sha256);
}

static inline int
hsm_sha384_init (EVP_MD_CTX * ctx)
{
  return hsm_digest_init (ctx, alg_sha384);
}

static inline int
hsm_sha512_init (EVP_MD_CTX * ctx)
{
  return hsm_digest_init (ctx, alg_sha512);
}

static inline int
hsm_digest_init (EVP_MD_CTX * ctx, int alg)
{
  CK_RV rv;
  struct token_session *wrapper = NULL;

  dbg_fprintf ("%s\n", __FUNCTION__);

  wrapper = hsm_get_session ();

  if (!wrapper)
    return 0;

  MD_DATA (ctx)->token = wrapper->token;
  MD_DATA (ctx)->session = wrapper->session;

  dbg_fprintf ("%s, alg = %d\n", __FUNCTION__, alg);

  MD_DATA (ctx)->alg = alg;

  CK_MECHANISM_TYPE mech = get_mech (MD_DATA (ctx)->alg, NULL);
  CK_MECHANISM mechanism = { mech, NULL, 0 };

  rv = pFunctionList->C_DigestInit (MD_DATA (ctx)->session, &mechanism);
  if (rv != CKR_OK)
    {

      hsm_die (HSM_F_DIGESTFINISH, HSM_R_DIGESTINIT, rv);
      pFunctionList->C_CloseSession (MD_DATA (ctx)->session);
      return 0;
    }

  return 1;
}

static int
hsm_digest_update (EVP_MD_CTX * ctx, const void *in, size_t len)
{
  CK_RV rv;

  dbg_fprintf ("%s\n", __FUNCTION__);
  if (!MD_DATA (ctx))
    {
      hsm_err (HSM_F_DIGESTUPDATE, HSM_R_PASSED_NULL_PARAMETER);
      return 0;
    }

  rv =
    pFunctionList->C_DigestUpdate (MD_DATA (ctx)->session, (CK_BYTE_PTR) in,
				   len);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_DIGESTUPDATE, HSM_R_DIGESTUPDATE, rv);
      return 0;
    }

  MD_DATA (ctx)->len += len;

  return 1;
}

static int
hsm_digest_finish (EVP_MD_CTX * ctx, unsigned char *md)
{
  CK_ULONG len = EVP_MD_CTX_size (ctx);
  CK_RV rv;
  int ret = 0, i;

  dbg_fprintf ("%s\n", __FUNCTION__);

  rv = pFunctionList->C_DigestFinal (MD_DATA (ctx)->session, md, &len);
  if (rv != CKR_OK)
    {
      hsm_die (HSM_F_DIGESTFINISH, HSM_R_DIGESTFINAL, rv);
      goto out_endsession;
    }

  ret = 1;

out_endsession:pFunctionList->C_CloseSession (MD_DATA (ctx)->session);
  MD_DATA (ctx)->session = CK_INVALID_HANDLE;
  return ret;
}

static int
hsm_digest_copy (EVP_MD_CTX * dst, const EVP_MD_CTX * src)
{
  CK_RV rv;
  CK_ULONG opstatelen;
  CK_BYTE_PTR opstate;

  /*if (EVP_MD_CTX_test_flags(src, EVP_MD_CTX_FLAG_NO_INIT))
     return 1; */

  dbg_fprintf ("%s\n", __FUNCTION__);

  /* get a copy of the cryptographic operations state of a session from src context */
  rv = pFunctionList->C_GetOperationState (MD_DATA (src)->session, NULL_PTR,
					   &opstatelen);
  if (rv != CKR_OK && rv != CKR_FUNCTION_NOT_SUPPORTED)
    {
      hsm_die (HSM_F_DIGESTCOPY, HSM_R_DIGESTUPDATE, rv);
      return 0;
    }

  opstate = (CK_BYTE_PTR) OPENSSL_malloc (opstatelen);
  rv = pFunctionList->C_GetOperationState (MD_DATA (src)->session, opstate,
					   &opstatelen);
  if (rv != CKR_OK && rv != CKR_FUNCTION_NOT_SUPPORTED)
    {
      hsm_die (HSM_F_DIGESTCOPY, HSM_R_DIGESTUPDATE, rv);
      return 0;
    }

  /* init a new session for the dst context */
  rv = hsm_digest_init (dst, MD_DATA (src)->alg);

  /* restore the cryptographic activities of a session to dst context */
  rv = pFunctionList->C_SetOperationState (MD_DATA (dst)->session, opstate,
					   opstatelen, 0, 0);
  if (rv != CKR_OK && rv != CKR_FUNCTION_NOT_SUPPORTED)
    {
      hsm_die (HSM_F_DIGESTCOPY, HSM_R_DIGESTUPDATE, rv);
      return 0;
    }

  OPENSSL_free (opstate);

  return 1;
}

static inline int
hsm_digest_cleanup (EVP_MD_CTX * ctx)
{
  return 1;
}

void hsm_engine_destructor (void) __attribute__ ((destructor));

void
hsm_engine_destructor (void)
{
  struct _token *tmp;

  dbg_fprintf ("%s\n", __FUNCTION__);
  while (hsm_token_list)
    {
      tmp = hsm_token_list->token_next;
      OPENSSL_free (hsm_token_list);
      hsm_token_list = tmp;
    }
}

/*Objects IDs are specified as hex string we need to convert them to byte array for the token */
static unsigned char *
hex2bin (const char *hexstr, size_t * size)
{
  size_t hexstrLen = strlen (hexstr);
  size_t bytesLen = hexstrLen / 2;
  unsigned char *bytes = (unsigned char *) OPENSSL_malloc (bytesLen);

  int count = 0;
  const char *pos = hexstr;

  for (count = 0; count < bytesLen; count++)
    {
      sscanf (pos, "%2hhx", &bytes[count]);
      pos += 2;
    }

  if (size != NULL)
    *size = bytesLen;

  return bytes;
}

#endif
#endif
