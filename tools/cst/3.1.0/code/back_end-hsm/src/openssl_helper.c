/*===========================================================================*/
/**
    @file    openssl_helper.c

    @brief   Provide functions to backward support OpenSSL 1.0.2.

@verbatim
=============================================================================

    Copyright 2018 NXP

Presence of a copyright notice is not an acknowledgement of publication.
This software file listing contains information of NXP that is of a
confidential and proprietary nature and any viewing or use of this file is
prohibited without specific written permission from NXP

=============================================================================
@endverbatim */

/*===========================================================================
                                INCLUDE FILES
=============================================================================*/
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/ecdsa.h>

/*===========================================================================
                                FUNCTIONS
=============================================================================*/

#if (OPENSSL_VERSION_NUMBER < 0x10100000L)

static void *
OPENSSL_zalloc(size_t num)
{
    void *ret = OPENSSL_malloc(num);

    if (ret != NULL) {
        memset(ret, 0, num);
    }
    return ret;
}

void
ECDSA_SIG_get0(const ECDSA_SIG *sig, const BIGNUM **pr, const BIGNUM **ps)
{
    if (pr != NULL) {
        *pr = sig->r;
    }
    if (ps != NULL) {
        *ps = sig->s;
    }
}

int
ECDSA_SIG_set0(ECDSA_SIG *sig, BIGNUM *r, BIGNUM *s)
{
    if (r == NULL || s == NULL) {
        return 0;
    }
    BN_clear_free(sig->r);
    BN_clear_free(sig->s);
    sig->r = r;
    sig->s = s;
    return 1;
}

void
EVP_MD_CTX_free(EVP_MD_CTX *ctx)
{
    EVP_MD_CTX_cleanup(ctx);
    OPENSSL_free(ctx);
}

EVP_MD_CTX *
EVP_MD_CTX_new(void)
{
    return OPENSSL_zalloc(sizeof(EVP_MD_CTX));
}

EC_KEY *
EVP_PKEY_get0_EC_KEY(EVP_PKEY *pkey)
{
    return (pkey->pkey.ec);
}

RSA *
EVP_PKEY_get0_RSA(EVP_PKEY *pkey)
{
    if (pkey->type != EVP_PKEY_RSA) {
        return NULL;
    }
    return pkey->pkey.rsa;
}

void
RSA_get0_key(const RSA *r, const BIGNUM **n, const BIGNUM **e, const BIGNUM **d)
{
    if (n != NULL) {
        *n = r->n;
    }
    if (e != NULL) {
        *e = r->e;
    }
    if (d != NULL) {
       *d = r->d;
    }
}

#endif

/*===========================================================================
                               GLOBAL FUNCTIONS
=============================================================================*/

/*--------------------------
  openssl_initialize
---------------------------*/

void
openssl_initialize(void)
{
#if defined _WIN32 || defined __CYGWIN__
    /* Required to avoid OpenSSL runtime errors on Win32 platforms */
    /* See: https://www.openssl.org/docs/faq.html#PROG3 */
    OPENSSL_malloc_init();
#endif

#if (OPENSSL_VERSION_NUMBER < 0x10100000L)
    ERR_load_crypto_strings();
    OpenSSL_add_all_algorithms();
#endif
}
