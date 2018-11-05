/*===========================================================================*/
/**
    @file    ssl_wrapper.c

    @brief   Implements Code Signing Tool's SSL Wrapper API for the
             Freescale reference Code Signing Tool.  .

@verbatim
=============================================================================

              Freescale Semiconductor Confidential Proprietary
        (c) Freescale Semiconductor, Inc. 2011-2015. All rights reserved.

Presence of a copyright notice is not an acknowledgement of
publication. This software file listing contains information of
Freescale Semiconductor, Inc. that is of a confidential and
proprietary nature and any viewing or use of this file is prohibited
without specific written permission from Freescale Semiconductor, Inc.

=============================================================================*/
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ssl_wrapper.h>
/*===========================================================================
                                 LOCAL MACROS
=============================================================================*/
#define SHA1_STRING                 ("SHA1")   /**< Openssl string: SHA-1 */
#define SHA256_STRING               ("SHA256") /**< Openssl string: SHA-256 */
#define SHA512_STRING               ("SHA512") /**< Openssl string: SHA-512 */
#define INVALID_DIGEST_STRING       ("null")

#define MAX_CMS_DATA                4096   /**< Max bytes in CMS_ContentInfo */
#define MAX_DIGEST_BYTES            64           /**< Max. digest is SHA-512 */
#define MAX_ERR_STR_BYTES           120         /**< Max. error string bytes */

void handle_errors(char * str,  int32_t *err_value, char *err_str) {
    snprintf(err_str, MAX_ERR_STR_BYTES-1, "%s", str);
    *err_value = CAL_CRYPTO_API_ERROR;
}

int32_t encryptccm(unsigned char *plaintext, int plaintext_len, unsigned char *aad,
    int aad_len, unsigned char *key, int key_len, unsigned char *iv, int iv_len,
    const char * out_file, unsigned char *tag, int tag_len, int32_t *err_value,
    char *err_str) {

#ifdef REMOVE_ENCRYPTION
    return CAL_NO_CRYPTO_API_ERROR;
#else
    EVP_CIPHER_CTX *ctx;

    int len;
    int ciphertext_len;

    unsigned char ciphertext[plaintext_len + EVP_MAX_BLOCK_LENGTH] ;

    FILE *fho = NULL;
    int err = 0;
    do{
        /* Create and initialise the context */
        if (!(ctx = EVP_CIPHER_CTX_new())) {
            handle_errors("Failed to allocate ccm context structure",
                          err_value, err_str);
            break;
        }

        /* Initialise the encryption operation. */
        switch(key_len) {
            case 16:
                err = EVP_EncryptInit_ex(ctx, EVP_aes_128_ccm(), NULL, NULL, NULL);
                break;
            case 24:
                err = EVP_EncryptInit_ex(ctx, EVP_aes_192_ccm(), NULL, NULL, NULL);
                break;
            case 32:
                err = EVP_EncryptInit_ex(ctx, EVP_aes_256_ccm(), NULL, NULL, NULL);
                break;
            default:
                handle_errors("Failed to allocate ccm context structure",
                              err_value, err_str);
                return *err_value;
        }

        if (err != 1) {
            handle_errors("Failed to initialize ccm context structure",
                          err_value, err_str);
            break;
        }

        /*
         * Setting IV len to 7. Not strictly necessary as this is the default
         * but shown here for the purposes of this example
         */
        if (1 != EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_CCM_SET_IVLEN, iv_len, NULL)) {
            handle_errors("Failed to initialize IV", err_value, err_str);
            break;
        }

        /* Set tag length */
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_CCM_SET_TAG, tag_len, NULL);

        /* Initialise key and IV */
        if (1 != EVP_EncryptInit_ex(ctx, NULL, NULL, key, iv)) {
            handle_errors("Failed to intialize key", err_value, err_str);
            break;
        }

        /* Provide the total plaintext length */
        if (1 != EVP_EncryptUpdate(ctx, NULL, &len, NULL, plaintext_len)) {
            handle_errors("Failed to initialize length parameter", err_value, err_str);
            break;
        }

        /*
         * Provide the message to be encrypted, and obtain the encrypted output.
         * EVP_EncryptUpdate can only be called once for this
         */
        if (1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len)) {
            handle_errors("Failed to encrypt", err_value, err_str);
            break;
        }
        ciphertext_len = len;

        /* Open out_file for writing */
        fho = fopen(out_file, "wb");
        if (fho == NULL) {
            handle_errors("Cannot open file", err_value, err_str);
            break;
        }

        /* Write encrypted data to out file */
        if (fwrite(ciphertext, 1, ciphertext_len, fho) != ciphertext_len) {
            handle_errors("Cannot write file", err_value, err_str);
            break;
        }

        /*
         * Finalise the encryption. Normally ciphertext bytes may be written at
         * this stage, but this does not occur in CCM mode
         */
        if (1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) {
            handle_errors("Failed to finalize", err_value, err_str);
            break;
        }
        ciphertext_len += len;

        /* Get the tag */
        if (1 != EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_CCM_GET_TAG, 16, tag)) {
            handle_errors("Failed to get tag", err_value, err_str);
            break;
        }

    } while(0);

    /* Clean up */
    EVP_CIPHER_CTX_free(ctx);

    if (fho) {
        fclose(fho);
    }

    return *err_value;
#endif
}

