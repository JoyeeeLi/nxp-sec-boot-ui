/*===========================================================================*/
/**
 *
 * Filename           : e_hsm.c
 * Author             : Marouene Boubakri <marouene.boubakri@nxp.com>
 * Description        : HSM engine for OpenSSL
 * Creation Date      : 23.05.2018,
 * Version            : 1.0.0
 *

@verbatim
=============================================================================

    Copyright 2018 NXP

Presence of a copyright notice is not an acknowledgement of publication.
This software file listing contains information of NXP that is of a
confidential and proprietary nature and any viewing or use of this file is
prohibited without specific written permission from NXP

=============================================================================
@endverbatim */

#ifndef _E_HSM_H_
#define _E_HSM_H_

/* Number of NID's that exist in OpenSSL 1.0.0a */
#define NUM_NID 893

#include <openssl/engine.h>
#include <cryptoki.h>

#if OPENSSL_VERSION_NUMBER < 0x10100000L
#define OLDER_OPENSSL
#endif

#define HSM_CMD_MODULE_PATH		(ENGINE_CMD_BASE)
#define HSM_CMD_SLOT_ID		(ENGINE_CMD_BASE + 1)
#define HSM_CMD_PIN		(ENGINE_CMD_BASE + 2)
#define HSM_CMD_LOAD_CERT		(ENGINE_CMD_BASE + 3)

struct _token {
	struct _token *token_next; /* next token in list of all tokens */
	CK_SLOT_ID slot_id; /* slot ID of this token */
	CK_BYTE_PTR pin; /*slot pin for this token */
	int hsm_implemented_ciphers[NUM_NID];
	int hsm_implemented_digests[NUM_NID];
};

struct _token *hsm_token_list;
struct _token *hsm_token;

enum alg_type {
	alg_rsa = 1,
	alg_des,
	alg_tdes,
	alg_sha,
	alg_dh,
	alg_aes,
	alg_ripemd,
	alg_ssl3,
	alg_md5,
	alg_rand,
	alg_sha224,
	alg_sha256,
	alg_sha384,
	alg_sha512
};

struct token_session {
	struct _token *token;
	CK_SESSION_HANDLE session;
};

struct hsm_digest_ctx {
	int alg;
	int len;
	struct _token *token;
	CK_SESSION_HANDLE session;
};

struct ecdsa_method {
    const char *name;
    ECDSA_SIG *(*ecdsa_do_sign) (const unsigned char *dgst, int dgst_len,
                                 EC_KEY *eckey);
    int (*ecdsa_sign_setup) (EC_KEY *eckey, BN_CTX *ctx, BIGNUM **kinv,
                             BIGNUM **r);
    int (*ecdsa_do_verify) (const unsigned char *dgst, int dgst_len,
                            const ECDSA_SIG *sig, EC_KEY *eckey);
# if 0
    int (*init) (EC_KEY *eckey);
    int (*finish) (EC_KEY *eckey);
# endif
    int flags;
    void *app_data;
};


typedef struct ecdsa_method ECDSA_METHOD;

#endif
