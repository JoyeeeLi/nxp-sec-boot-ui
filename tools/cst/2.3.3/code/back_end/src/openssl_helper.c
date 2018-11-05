/*===========================================================================*/
/**
    @file    openssl_helper.c

    @brief   Provide helper functions to ease openssl tasks. Mainly to
                provide common code for several tools.

@verbatim
=============================================================================

              Freescale Semiconductor Confidential Proprietary
        (c) Freescale Semiconductor, Inc. 2011, 2012. All rights reserved.

Presence of a copyright notice is not an acknowledgement of
publication. This software file listing contains information of
Freescale Semiconductor, Inc. that is of a confidential and
proprietary nature and any viewing or use of this file is prohibited
without specific written permission from Freescale Semiconductor, Inc.

=============================================================================
Revision History:

                    Modification Date   Tracking
Author               (dd-mmm-yyyy)      Number     Description of Changes
---------------      -------------     ----------  -----------------------
Fareed Mohammed       07-Apr-2011      ENGR140621  Initial Version
Auger Florent         18-Jul-2012      ENGR169493  Added the new function:
                                                   print_version()
Fareed Mohammed       10-Sep-2012      ENGR169497  Add encryption support
=============================================================================
Portability:

These definitions are customised for 32 bit cores of either endianness.

=============================================================================
@endverbatim */

/*===========================================================================
                                INCLUDE FILES
=============================================================================*/
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <openssl/bio.h>
#include <openssl/x509.h>
#include <openssl/x509v3.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include "openssl_helper.h"
#include "version.h"
#include <openssl/rand.h>

/*===========================================================================
                               LOCAL CONSTANTS
=============================================================================*/

/*===========================================================================
                                 LOCAL MACROS
=============================================================================*/

/*===========================================================================
                  LOCAL TYPEDEFS (STRUCTURES, UNIONS, ENUMS)
=============================================================================*/

/*===========================================================================
                          LOCAL FUNCTION PROTOTYPES
=============================================================================*/

/*===========================================================================
                               LOCAL FUNCTIONS
=============================================================================*/

/*===========================================================================
                               GLOBAL FUNCTIONS
=============================================================================*/

/*--------------------------
  openssl_initialize
---------------------------*/

void
openssl_initialize()
{
    ERR_load_crypto_strings();
    OpenSSL_add_all_algorithms();
}


/*--------------------------
  generate_hash
---------------------------*/

uint8_t *
generate_hash(const uint8_t *buf, size_t msg_bytes, const char *hash_alg,
              size_t *hash_bytes)
{
    const EVP_MD *type;                /**< Mesage digest type*/
    EVP_MD_CTX   ctx;                  /**< Message digest context */
    uint8_t      *hash_mem_ptr = NULL; /**< location of result buffer */
    unsigned int  tmp;

    if (!(type = EVP_get_digestbyname(hash_alg)))
    {
        return NULL;
    }

    if (!(hash_mem_ptr = (uint8_t *)malloc(EVP_MAX_MD_SIZE)))
    {
        return NULL;
    }


    EVP_DigestInit(&ctx, type);
    EVP_DigestUpdate(&ctx, buf, msg_bytes);
    EVP_DigestFinal(&ctx, hash_mem_ptr, &tmp);

    *hash_bytes = tmp;

    return hash_mem_ptr;
}

/*--------------------------
  get_bn
---------------------------*/

uint8_t*
get_bn(const BIGNUM *a, size_t *bytes)
{
    uint8_t *byte_array = NULL; /**< Resulting big number byte array */
    uint8_t x;                  /**< Temp. variable for extracting ebig num. */
    int32_t i;                  /**< Loop index */
    uint32_t j;                 /**< Loop index */
    uint32_t k = 0;             /**< Byte array index */
    uint32_t z = 0;             /**< Temp. variable for extracting ebig num. */

    byte_array = malloc(a->top * sizeof(BN_ULONG));
    if (byte_array == NULL)
    {
        return NULL;
    }

    /* Extract bytes from BIGNUM struct */
    for (i = a->top-1; i >= 0; i--)
    {
        for (j = sizeof(BN_ULONG); j > 0 ; j--)
        {
            x = (a->d[i] >> ((j-1)*8)) & 0xFF;
            /* Strip leading zeros */
            if (z || (x != 0))
            {
                byte_array[k++] = x;
                z = 1;
#ifdef DEBUG
                printf("%d 0x%02x\n", k-1, byte_array[k-1]);
#endif
            }
        }
    }

    *bytes = k;
    return byte_array;
}


/*--------------------------
  unix_time
---------------------------*/

uint32_t
unix_time(const char* x509_time)
{
    uint32_t year = 0;       /**< year */
    uint32_t month = 0;      /**< month */
    uint32_t day = 0;        /**< day */
    uint32_t hour = 0;       /**< hour */
    uint32_t minute = 0;     /**< minute */
    uint32_t second = 0;     /**< second */
    uint32_t unix_time = 0;  /**< resulting unix time */
    char     temp[5];        /**< temp array for char conversion */
    uint32_t idx = 0;        /**< index into X509_time string */

    if (x509_time)
    {
        /* String from X.509 certificate must have one of the following
         * formats: YYMMDDHHMMSSZ or YYYYMMDDHHMMSSZ
         */
        if (strlen(x509_time) == X509_UTCTIME_STRING_BYTES)
        {
            temp[0] = x509_time[idx++];
            temp[1] = x509_time[idx++];
            temp[2] = '\0';
            temp[3] = '\0';
            year = atoi(temp);
            if (year < 50)
            {
                year = year + 2000;
            }
            else
            {
                year = year + 1900;
            }
        }
        else if (strlen(x509_time) == X509_GENTIME_STRING_BYTES)
        {
            temp[0] = x509_time[idx++];
            temp[1] = x509_time[idx++];
            temp[2] = x509_time[idx++];
            temp[3] = x509_time[idx++];
            temp[4] = '\0';
            year = atoi(temp);
        }
        /* Invalid time string length */
        else
        {
            return unix_time;
        }

        temp[0] = x509_time[idx++];
        temp[1] = x509_time[idx++];
        temp[2] = 0;
        temp[3] = 0;
        month = atoi(temp);

        temp[0] = x509_time[idx++];
        temp[1] = x509_time[idx++];
        day = atoi(temp);

        temp[0] = x509_time[idx++];
        temp[1] = x509_time[idx++];
        hour = atoi(temp);

        temp[0] = x509_time[idx++];
        temp[1] = x509_time[idx++];
        minute = atoi(temp);

        temp[0] = x509_time[idx++];
        temp[1] = x509_time[idx++];
        second = atoi(temp);

        /* Convert to unix time */
        year -= month < 3;
        month += month < 3 ? 10 : -2;
        unix_time = year/400 - year/100 + year/4
            + year*365 + month*367/12 + day
            - 719499;
        unix_time = unix_time * 86400
            + hour * 3600
            + minute * 60
            + second;
    }

    return unix_time;
}

/*--------------------------
  sign_data
---------------------------*/

uint8_t*
sign_data(const EVP_PKEY *skey, const BUF_MEM *bptr, hash_alg_t hash_alg,
          size_t *sig_bytes)
{
    EVP_MD_CTX   *ctx = EVP_MD_CTX_create(); /**< Signature context */
    uint8_t      *sig_buf = NULL;            /**< Location of sig. array */
    const EVP_MD *hash_type = NULL;          /**< Hash digest algorithm type */
    unsigned int  tmp_sig_bytes;
#ifdef DEBUG
    uint32_t i;                              /**< Loop index */
#endif

    if (ctx)
    {
        tmp_sig_bytes = EVP_PKEY_size((EVP_PKEY *)skey);
        sig_buf = malloc(tmp_sig_bytes);

        /* Determine OpenSSL hash digest type */
        if (hash_alg == SHA_1)
        {
            hash_type = EVP_sha1();
        }
        else if (hash_alg == SHA_256)
        {
            hash_type = EVP_sha256();
        }
        else
        {
            EVP_MD_CTX_destroy(ctx);
            return NULL;
        }

        if ((sig_buf != NULL) &&
            ( (EVP_SignInit_ex(ctx, hash_type, NULL) != CST_SUCCESS) ||
              (EVP_SignUpdate(ctx, bptr->data, bptr->length) != CST_SUCCESS) ||
              (EVP_SignFinal(ctx, sig_buf, &tmp_sig_bytes, (EVP_PKEY *)skey)
               != CST_SUCCESS) ))
        {
            *sig_bytes = tmp_sig_bytes;
            EVP_MD_CTX_destroy(ctx);
            return NULL;
        }

        *sig_bytes = tmp_sig_bytes;

#ifdef DEBUG
        printf("Signature bytes = %d\n", tmp_sig_bytes);
        if (sig_buf)
        {
            for (i = 0; i < tmp_sig_bytes; i++)
            {
                printf("%d) 0x%02x\n", i, sig_buf[i]);
            }
        }
#endif

        EVP_MD_CTX_destroy(ctx);
    }
    return sig_buf;
}

/*--------------------------
  write_cert_file
---------------------------*/
cst_status_t
write_cert_file(const char *filename, const BIO *data)
{
    BIO *wtls_file = NULL;   /**< Resulting output file */
    BUF_MEM *bptr;           /**< OpenSSL BIO memory buffer ptr */

    wtls_file = BIO_new_file(filename, "wb");
    if (wtls_file == NULL)
    {
        return CST_FAILURE;;
    }

    BIO_get_mem_ptr((BIO *)data, &bptr);

    if (bptr == NULL)
    {
        BIO_free(wtls_file);
        return CST_FAILURE;
    }

    BIO_write(wtls_file, bptr->data, bptr->length);
    BIO_free(wtls_file);
    return CST_SUCCESS;
}

/*--------------------------
  read_certificate
---------------------------*/
X509*
read_certificate(const char* filename)
{
    BIO  *bio_cert = NULL; /**< OpenSSL BIO ptr */
    X509 *cert = NULL;     /**< X.509 certificate data structure */
    FILE *fp = NULL;       /**< File pointer for DER encoded file */
    /** Points to expected location of ".pem" filename extension */
    const char *temp = filename + strlen(filename) -
                       PEM_FILE_EXTENSION_BYTES;

    bio_cert = BIO_new(BIO_s_file());
    if (bio_cert == NULL)
    {
        return NULL;
    }

    /* PEM encoded */
    if (!strncasecmp(temp, PEM_FILE_EXTENSION, PEM_FILE_EXTENSION_BYTES))
    {
        if (BIO_read_filename(bio_cert, filename) <= 0)
        {
            BIO_free(bio_cert);
            return NULL;
        }

        cert = PEM_read_bio_X509(bio_cert, NULL, 0, NULL);
    }
    /* DER encoded */
    else
    {
        /* Open the DER file and load it into a X509 object */
        fp = fopen(filename, "rb");
        cert = d2i_X509_fp(fp, NULL);
        fclose(fp);
    }

    BIO_free(bio_cert);
    return cert;
}

/*--------------------------------
  get_der_encoded_certificate_data
----------------------------------*/
int32_t get_der_encoded_certificate_data(const char* filename,
                                         uint8_t ** der)
{
    /** Used for returning either size of der data or 0 to indicate an error */
    int32_t ret_val = 0;

    /* Read X509 certificate data from cert file */
    X509 *cert = read_certificate(filename);

    if (cert != NULL)
    {
        /* i2d_X509() allocates memory for der data, converts the X509
         * cert structure to binary der formatted data.  It then
         * returns the address of the memory allocated for the der data
         */
        ret_val = i2d_X509(cert, der);

        /* On error return 0 */
        if (ret_val < 0)
        {
            ret_val = 0;
        }
        X509_free(cert);
    }
    return ret_val;
}

/*--------------------------
  read_private_key
---------------------------*/
EVP_PKEY*
read_private_key(const char *filename, const pem_password_cb *password_cb,
                 const char *password)
{
    BIO      *private_key = NULL; /**< OpenSSL BIO ptr */
    EVP_PKEY *pkey;               /**< Private Key data structure */
    /** Points to expected location of ".pem" filename extension */
    const char *temp = filename + strlen(filename) -
                       PEM_FILE_EXTENSION_BYTES;

    /* Read Private key */
    private_key = BIO_new(BIO_s_file( ));
	if (!private_key)
    {
        return NULL;
    }

    /* Set BIO to read from the given filename */
	if (BIO_read_filename(private_key, filename) <= 0)
    {
        BIO_free(private_key);
        return NULL;
    }

    if (!strncasecmp(temp, PEM_FILE_EXTENSION, PEM_FILE_EXTENSION_BYTES))
    {
        /* Read Private key - from PEM encoded file */
        pkey = PEM_read_bio_PrivateKey(private_key, NULL, password_cb,
                                       (char *)password);
        if (!pkey)
        {
            BIO_free(private_key);
            return NULL;
        }
    }
    else
    {
        pkey = d2i_PKCS8PrivateKey_bio (private_key, NULL, password_cb,
                                        (char *)password );
        if (!pkey)
        {
            BIO_free(private_key);
            return NULL;
        }
    }
    return pkey;
}

/*--------------------------
  print_version
---------------------------*/

void print_version(void)
{
    printf("Code Signing Tool release version %s\n",CST_VERSION);
}

/*--------------------------
  seed_prng
---------------------------*/
uint32_t seed_prng(uint32_t bytes)
{
    return RAND_load_file("/dev/random", bytes);
}


/*--------------------------
  gen_random_bytes
---------------------------*/
int32_t gen_random_bytes(uint8_t *buf, size_t bytes)
{
    if (!RAND_bytes(buf, bytes))
    {
        return CAL_RAND_API_ERROR;
    }

    return CAL_SUCCESS;
}

/*--------------------------
  print_license
---------------------------*/

void print_license(void)
{
    printf("\n\nFreescale License Information:\n");
    printf("----------------------------------\n");
    printf("Copyright (c) Freescale Semiconductor, Inc. 2011. All rights reserved.\n\n");
    printf("This software is under license from Freescale Semiconductor Inc.\n");
    printf("By using this software you agree to the license terms provided\n");
    printf("at the time this release was downloaded from www.freescale.com\n");
    printf("\nOpenssl/SSLeay License Information:\n");
    printf("---------------------------------------\n");
    printf("This product includes software developed by the OpenSSL Project\n");
    printf("for use in the OpenSSL Toolkit (http://www.openssl.org/)\n\n");
    printf("This product includes cryptographic software written by\n");
    printf("Eric Young (eay@cryptsoft.com)\n");
    printf("This product includes cryptographic software written by\n");
    printf("Brian Gladman, Worcester, UK\n");
    printf("\nThe following is the full license text for OpenSSL, SSLeay\n");
    printf("and Brian Gladman:\n\n");
    printf("OpenSSL License\n");
    printf("---------------\n\n");
    printf("/* ====================================================================\n");
    printf(" * Copyright (c) 1998-2011 The OpenSSL Project.  All rights reserved.\n");
    printf(" *\n");
    printf(" * Redistribution and use in source and binary forms, with or without\n");
    printf(" * modification, are permitted provided that the following conditions\n");
    printf(" * are met:\n");
    printf(" *\n");
    printf(" * 1. Redistributions of source code must retain the above copyright\n");
    printf(" *    notice, this list of conditions and the following disclaimer.\n");
    printf(" *\n");
    printf(" * 2. Redistributions in binary form must reproduce the above copyright\n");
    printf(" *    notice, this list of conditions and the following disclaimer in\n");
    printf(" *    the documentation and/or other materials provided with the\n");
    printf(" *    distribution.\n");
    printf(" *\n");
    printf(" * 3. All advertising materials mentioning features or use of this\n");
    printf(" *    software must display the following acknowledgment:\n");
    printf(" *    \"This product includes software developed by the OpenSSL Project\n");
    printf(" *    for use in the OpenSSL Toolkit. (http://www.openssl.org/)\"\n");
    printf(" *\n");
    printf(" * 4. The names \"OpenSSL Toolkit\" and \"OpenSSL Project\" must not be used to\n");
    printf(" *    endorse or promote products derived from this software without\n");
    printf(" *    prior written permission. For written permission, please contact\n");
    printf(" *    openssl-core@openssl.org.\n");
    printf(" *\n");
    printf(" * 5. Products derived from this software may not be called \"OpenSSL\"\n");
    printf(" *    nor may \"OpenSSL\" appear in their names without prior written\n");
    printf(" *    permission of the OpenSSL Project.\n");
    printf(" *\n");
    printf(" * 6. Redistributions of any form whatsoever must retain the following\n");
    printf(" *    acknowledgment:\n");
    printf(" *    \"This product includes software developed by the OpenSSL Project\n");
    printf(" *    for use in the OpenSSL Toolkit (http://www.openssl.org/)\"\n");
    printf(" *\n");
    printf(" * THIS SOFTWARE IS PROVIDED BY THE OpenSSL PROJECT ``AS IS'' AND ANY\n");
    printf(" * EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\n");
    printf(" * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR\n");
    printf(" * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE OpenSSL PROJECT OR\n");
    printf(" * ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,\n");
    printf(" * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT\n");
    printf(" * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n");
    printf(" * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)\n");
    printf(" * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,\n");
    printf(" * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)\n");
    printf(" * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED\n");
    printf(" * OF THE POSSIBILITY OF SUCH DAMAGE.\n");
    printf(" * ====================================================================\n");
    printf(" *\n");
    printf(" * This product includes cryptographic software written by Eric Young\n");
    printf(" * (eay@cryptsoft.com).  This product includes software written by Tim\n");
    printf(" * Hudson (tjh@cryptsoft.com).\n");
    printf(" *\n");
    printf(" */\n\n");
    printf("Original SSLeay License\n");
    printf("-----------------------\n\n");
    printf("/* Copyright (C) 1995-1998 Eric Young (eay@cryptsoft.com)\n");
    printf(" * All rights reserved.\n");
    printf(" *\n");
    printf(" * This package is an SSL implementation written\n");
    printf(" * by Eric Young (eay@cryptsoft.com).\n");
    printf(" * The implementation was written so as to conform with Netscapes SSL.\n");
    printf(" *\n");
    printf(" * This library is free for commercial and non-commercial use as long as\n");
    printf(" * the following conditions are aheared to.  The following conditions\n");
    printf(" * apply to all code found in this distribution, be it the RC4, RSA,\n");
    printf(" * lhash, DES, etc., code; not just the SSL code.  The SSL documentation\n");
    printf(" * included with this distribution is covered by the same copyright terms\n");
    printf(" * except that the holder is Tim Hudson (tjh@cryptsoft.com).\n");
    printf(" *\n");
    printf(" * Copyright remains Eric Young's, and as such any Copyright notices in\n");
    printf(" * the code are not to be removed.\n");
    printf(" * If this package is used in a product, Eric Young should be given attribution\n");
    printf(" * as the author of the parts of the library used.\n");
    printf(" * This can be in the form of a textual message at program startup or\n");
    printf(" * in documentation (online or textual) provided with the package.\n");
    printf(" *\n");
    printf(" * Redistribution and use in source and binary forms, with or without\n");
    printf(" * modification, are permitted provided that the following conditions\n");
    printf(" * are met:\n");
    printf(" * 1. Redistributions of source code must retain the copyright\n");
    printf(" *    notice, this list of conditions and the following disclaimer.\n");
    printf(" * 2. Redistributions in binary form must reproduce the above copyright\n");
    printf(" *    notice, this list of conditions and the following disclaimer in the\n");
    printf(" *    documentation and/or other materials provided with the distribution.\n");
    printf(" * 3. All advertising materials mentioning features or use of this software\n");
    printf(" *    must display the following acknowledgement:\n");
    printf(" *    \"This product includes cryptographic software written by\n");
    printf(" *     Eric Young (eay@cryptsoft.com)\"\n");
    printf(" *    The word 'cryptographic' can be left out if the rouines from the library\n");
    printf(" *    being used are not cryptographic related :-).\n");
    printf(" * 4. If you include any Windows specific code (or a derivative thereof) from\n");
    printf(" *    the apps directory (application code) you must include an acknowledgement:\n");
    printf(" *    \"This product includes software written by Tim Hudson (tjh@cryptsoft.com)\"\n");
    printf(" *\n");
    printf(" * THIS SOFTWARE IS PROVIDED BY ERIC YOUNG ``AS IS'' AND\n");
    printf(" * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\n");
    printf(" * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE\n");
    printf(" * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE\n");
    printf(" * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\n");
    printf(" * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS\n");
    printf(" * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)\n");
    printf(" * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT\n");
    printf(" * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY\n");
    printf(" * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF\n");
    printf(" * SUCH DAMAGE.\n");
    printf(" *\n");
    printf(" * The licence and distribution terms for any publically available version or\n");
    printf(" * derivative of this code cannot be changed.  i.e. this code cannot simply be\n");
    printf(" * copied and put under another distribution licence\n");
    printf(" * [including the GNU Public Licence.]\n");
    printf(" */\n\n");
    printf("Original Brian Gladman License\n");
    printf("------------------------------\n\n");
    printf("  /*\n");
    printf("  ---------------------------------------------------------------------------\n");
    printf("  Copyright (c) 1998-2008, Brian Gladman, Worcester, UK. All rights reserved.\n");
    printf(" \n");
    printf("  LICENSE TERMS\n");
    printf(" \n");
    printf("  The redistribution and use of this software (with or without changes)\n");
    printf("  is allowed without the payment of fees or royalties provided that:\n");
    printf(" \n");
    printf("   1. source code distributions include the above copyright notice, this\n");
    printf("      list of conditions and the following disclaimer;\n");
    printf(" \n");
    printf("   2. binary distributions include the above copyright notice, this list\n");
    printf("      of conditions and the following disclaimer in their documentation;\n");
    printf(" \n");
    printf("   3. the name of the copyright holder is not used to endorse products\n");
    printf("      built using this software without specific written permission.\n");
    printf(" \n");
    printf("  DISCLAIMER\n");
    printf(" \n");
    printf("  This software is provided 'as is' with no explicit or implied warranties\n");
    printf("  in respect of its properties, including, but not limited to, correctness\n");
    printf("  and/or fitness for purpose.\n");
    printf("  ---------------------------------------------------------------------------\n");
    printf("  Issue Date: 20/12/2007\n");
    printf(" */\n\n");
}
