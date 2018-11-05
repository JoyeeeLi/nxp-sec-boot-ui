/*===========================================================================*/
/**
    @file    adapt_layer_openssl.c

    @brief   Implements Code Signing Tool's Adaptation Layer API for the
             Freescale reference Code Signing Tool.  This file may be
             replaced in implementations using a Hardware Security Module
             or a client/server based infrastructure.

@verbatim
=============================================================================

              Freescale Semiconductor Confidential Proprietary
        (c) Freescale Semiconductor, Inc. 2011-2015. All rights reserved.

Presence of a copyright notice is not an acknowledgement of
publication. This software file listing contains information of
Freescale Semiconductor, Inc. that is of a confidential and
proprietary nature and any viewing or use of this file is prohibited
without specific written permission from Freescale Semiconductor, Inc.

=============================================================================
Revision History:

                 Modification Date   Tracking
Author             (dd-mmm-yyyy)      Number    Description of Changes
---------------    -------------   ----------  -----------------------
Fareed Mohammed/    20-Jan-2010    ENGR140621  Initial version
Rod Ziolkowski
Florent Auger       28-Aug-2012    ENGR162295  Path to key file built from CSF
Fareed Mohammed     10-Sep-2012    ENGR169497  Add encryption support
Fareed Mohammed     08-Nov-2012    ENGR232857  Conditionally build for
                                               encryption support
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
#include <ssl_wrapper.h>
#include <string.h>
#include <openssl/bio.h>
#include <openssl/x509.h>
#include <openssl/x509v3.h>
#include <openssl/cms.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl/rand.h>
#include <openssl/crypto.h>
#include <adapt_layer.h>
#include <openssl_helper.h>
#include <pkey.h>
#ifdef WIN32
#include <openssl/applink.c>
#endif
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
/*===========================================================================
                  LOCAL TYPEDEFS (STRUCTURES, UNIONS, ENUMS)
=============================================================================*/

/*===========================================================================
                          LOCAL FUNCTION PROTOTYPES
=============================================================================*/

/** Converts given digest value to equivalent OpenSSL string
 *
 * @param[in] hash_alg one of #hash_alg_t
 *
 * @returns Openssl string corresponding the given hash algorithm in
 *          @a hash_alg, if @a hash_alg is not valid #INVALID_DIGEST_STRING
 *          is returned.
 */
static char*
get_digest_name(hash_alg_t hash_alg);

/** Computes hash digest from a given input file
 *
 * This function differs from the generate_hash() function in
 * openssl_helper.c in that this function will hash an arbitrary amount of
 * data contained in @in_file. The generate_hash expects the data in a
 * contigous memory array with the data length already known.
 *
 * @param[in] in_file Character string holding the input data filename.
 *
 * @param[in] hash_alg Hash digest algorithm from #hash_alg_t
 *
 * @param[in,out] buf on input, used to read input data when computing
 *                hash value, on output holds the resulting hash value.
 *
 * @param[in,out] pbuf_bytes on input, holds the size of @a buf ib bytes,
 *                on output pbuf_bytes is updated to hold the size of the
 *                resulting hash in bytes.
 *
 * @pre @a in_file, @a buf, and @a pbuf_bytes must not be NULL
 *
 * @post On success @a buf is updated to hold the hash digest result and
 *       @a pbuf_bytes is updated to hold the length of the hash in bytes
 *
 * @retval #CAL_SUCCESS API completed its task successfully
 *
 * @retval #CAL_INVALID_ARGUMENTif @a hash_alg contains an unsupported
 *         algorithm
 *
 * @retval #CAL_CRYPTO_API_ERROR otherwise
 */
static int32_t
calculate_hash(const char *in_file,
               hash_alg_t hash_alg,
               uint8_t *buf,
               int32_t *pbuf_bytes);

/** Converts hash_alg to an equivalent NID value for OpenSSL
 *
 * @param[in] hash_alg Hash digest algorithm from #hash_alg_t
 *
 * @pre hash_alg is a valid value from #hash_alg_t
 *
 * @returns Openssl NID value corresponding to a valid value for @a hash_alg,
 *          NID_undef otherwise.
 */
static int32_t
get_NID(hash_alg_t hash_alg);

/** Generate raw PKCS#1 Signature Data
 *
 * Generates a raw PKCS#1 v1.5 signature for the given data file, signer
 * certificate, and hash algorithm. The signature data is returned in
 * a buffer provided by caller.
 *
 * @param[in] in_file string containing path to file with data to sign
 *
 * @param[in] key_file string containing path to signing key
 *
 * @param[in] hash_alg hash algorithm from #hash_alg_t
 *
 * @param[out] sig_buf signature data buffer
 *
 * @param[in,out] sig_buf_bytes On input, contains size of @a sig_buf in bytes,
 *                              On output, contains size of signature in bytes.
 *
 * @pre @a in_file, @a cert_file, @a key_file, @a sig_buf and @a sig_buf_bytes
 *         must not be NULL.
 *
 * @post On success @a sig_buf is updated to hold the resulting signature and
 *       @a sig_buf_bytes is updates to hold the length of the signature in
 *       bytes
 *
 * @retval #CAL_SUCCESS API completed its task successfully
 *
 * @retval #CAL_CRYPTO_API_ERROR An Openssl related error has occured
 */
static int32_t
gen_sig_data_raw(const char *in_file,
                 const char *key_file,
                 hash_alg_t hash_alg,
                 uint8_t *sig_buf,
                 int32_t *sig_buf_bytes);

/** Generate CMS Signature Data
 *
 * Generates a CMS signature for the given data file, signer certificate, and
 * hash algorithm. The signature data is returned in a buffer provided by
 * caller.  Note that sign_data cannot be used here since that function
 * requires an input buffer as an argument.  For large files it becomes
 * unreasonable to allocate a contigous block of memory.
 *
 * @param[in] in_file string containing path to file with data to sign
 *
 * @param[in] cert_file string constaining path to signer certificate
 *
 * @param[in] hash_alg hash algorithm from #hash_alg_t
 *
 * @param[out] sig_buf signature data buffer
 *
 * @param[in,out] sig_buf_bytes On input, contains size of @a sig_buf in bytes,
 *                              On output, contains size of signature in bytes.
 *
 * @pre @a in_file, @a cert_file, @a key_file, @a sig_buf and @a sig_buf_bytes
 *         must not be NULL.
 *
 * @post On success @a sig_buf is updated to hold the resulting signature and
 *       @a sig_buf_bytes is updates to hold the length of the signature in
 *       bytes
 *
 * @retval #CAL_SUCCESS API completed its task successfully
 *
 * @retval #CAL_INVALID_ARGUMENT One of the input arguments is invalid
 *
 * @retval #CAL_CRYPTO_API_ERROR An Openssl related error has occured
 */
static int32_t
gen_sig_data_cms(const char *in_file,
                 const char *cert_file,
                 const char *key_file,
                 hash_alg_t hash_alg,
                 uint8_t *sig_buf,
                 size_t *sig_buf_bytes);

/** Copies CMS Content Info with encrypted or signature data to buffer
 *
 * @param[in] cms CMS Content Info
 *
 * @param[in] bio_in input bio
 *
 * @param[out] data_buffer address to data buffer
 *
 * @param[in] data_buffer_size max size, [out] return size
 *
 * @param[in] flags CMS Flags
 *
 * @returns CAL_SUCCESS upon success
 *
 * @returns CAL_CRYPTO_API_ERROR when openssl BIO API fail
 */
int32_t cms_to_buf(CMS_ContentInfo *cms, BIO * bio_in, uint8_t * data_buffer,
                            size_t * data_buffer_size, int32_t flags);

/** generate_dek_key
 *
 * Uses openssl API to generate a random 128 bit AES key
 *
 * @param[out] key buffer to store the key data
 *
 * @param[in] len length of the key to generate
 *
 * @post if successful the random bytes are placed into output buffer
 *
 * @pre  #openssl_initialize has been called previously
 *
 * @returns if successful function returns location CAL_SUCCESS.
 */
int32_t generate_dek_key(uint8_t * key, int32_t len);

/**  write_plaintext_dek_key
 *
 * Writes the provide DEK to the give path. It will be encrypted
 * under the certificate file if provided.
 *
 * @param[in] key input key data
 *
 * @param[in] key_bytes length of the input key
 *
 * @param[in] cert_file  certificate to encrypt the DEK
 *
 * @param[in] enc_file  destination file
 *
 * @post if successful the dek is written to the file
 *
 * @returns if successful function returns location CAL_SUCCESS.
 */
int32_t write_plaintext_dek_key(uint8_t * key, size_t key_bytes,
                        const char * cert_file, const char * enc_file);

/** encrypt_dek_key
 *
 * Uses openssl API to encrypt the key. Saves the encrypted structure to a file
 *
 * @param[in] key input key data
 *
 * @param[in] key_bytes length of the input key
 *
 * @param[in] cert filename of the RSA certificate, dek will be encrypted with
 *
 * @param[in] file encrypted data saved in the file
 *
 * @post if successful the file is created with the encrypted data
 *
 * @pre  #openssl_initialize has been called previously
 *
 * @returns if successful function returns location CAL_SUCCESS.
 */
int32_t encrypt_dek_key(uint8_t * key, size_t key_bytes,
                const char * cert_file, const char * enc_file);

/** Display error message
 *
 * Displays error message to STDERR
 *
 * @param[in] err Error string to display
 *
 * @pre  @a err is not NULL
 *
 * @post None
 */
static void
display_error(const char *err);

/*===========================================================================
                               GLOBAL VARIABLES
=============================================================================*/

/*===========================================================================
                               LOCAL FUNCTIONS
=============================================================================*/

/*--------------------------
  get_digest_name
---------------------------*/
char*
get_digest_name(hash_alg_t hash_alg)
{
    char *hash_name = NULL;    /**< Ptr to return address of string macro */
    switch(hash_alg) {
        case SHA_1:
            hash_name = SHA1_STRING;
            break;
        case SHA_256:
            hash_name = SHA256_STRING;
            break;
        case SHA_512:
            hash_name = SHA512_STRING;
            break;
        default:
            hash_name = INVALID_DIGEST_STRING;
            break;
    }
    return hash_name;
}


/*--------------------------
  calculate_hash
---------------------------*/
int32_t
calculate_hash(const char *in_file,
               hash_alg_t hash_alg,
               uint8_t *buf,
               int32_t *pbuf_bytes)
{
    const EVP_MD *sign_md; /**< Ptr to digest name */
    int32_t bio_bytes; /**< Length of bio data */
    BIO *in = NULL; /**< Ptr to BIO for reading data from in_file */
    BIO *bmd = NULL; /**< Ptr to BIO with hash bytes */
    BIO *inp; /**< Ptr to BIO for appending in with bmd */
    /** Status initialized to API error */
    int32_t err_value =  CAL_CRYPTO_API_ERROR;

    sign_md = EVP_get_digestbyname(get_digest_name(hash_alg));
    if (sign_md == NULL) {
        return CAL_INVALID_ARGUMENT;
    }

    /* Read data to generate hash */
    do {

        /* Create necessary bios */
        in = BIO_new(BIO_s_file());
        bmd = BIO_new(BIO_f_md());
        if (in == NULL || bmd == NULL) {
            break;
        }

        /* Set BIO to read filename in_file */
        if (BIO_read_filename(in, in_file) <= 0) {
            break;
        }

        /* Set BIO md to given hash */
        if (!BIO_set_md(bmd, sign_md)) {
            break;
        }

        /* Appends BIO in to bmd */
        inp = BIO_push(bmd, in);

        /* Read data from file BIO */
        do
        {
            bio_bytes = BIO_read(inp, (uint8_t *)buf, *pbuf_bytes);
        } while (bio_bytes > 0);

        /* Check for read error */
        if (bio_bytes < 0) {
            break;
        }

        /* Get the hash */
        bio_bytes = BIO_gets(inp, (char *)buf, *pbuf_bytes);
        if (bio_bytes <= 0) {
            break;
        }

        /* Send the output bytes in pbuf_bytes */
        *pbuf_bytes = bio_bytes;
        err_value =  CAL_SUCCESS;
    } while(0);

    if (in != NULL) BIO_free(in);
    if (bmd != NULL) BIO_free(bmd);

    return err_value;
}

/*--------------------------
  get_NID
---------------------------*/
int32_t
get_NID(hash_alg_t hash_alg)
{
    return OBJ_txt2nid(get_digest_name(hash_alg));
}

/*--------------------------
  gen_sig_data_raw
---------------------------*/
int32_t
gen_sig_data_raw(const char *in_file,
                 const char *key_file,
                 hash_alg_t hash_alg,
                 uint8_t *sig_buf,
                 int32_t *sig_buf_bytes)
{
    EVP_PKEY *key = NULL; /**< Ptr to read key data */
    RSA *rsa = NULL; /**< Ptr to rsa of key data */
    uint8_t *rsa_in = NULL; /**< Mem ptr for hash data of in_file */
    uint8_t *rsa_out = NULL; /**< Mem ptr for encrypted data */
    int32_t rsa_inbytes; /**< Holds the length of rsa_in buf */
    int32_t rsa_outbytes = 0; /**< Holds the length of rsa_out buf */
    int32_t key_bytes; /**< Size of key data */
    int32_t hash_nid; /**< hash id needed for RSA_sign() */
    /** Array to hold error string */
    char err_str[MAX_ERR_STR_BYTES];
    /**< Holds the return error value */
    int32_t err_value = CAL_CRYPTO_API_ERROR;

    do
    {
        /* Read key */
        key = read_private_key(key_file,
                           (const pem_password_cb *)get_passcode_to_key_file,
                           key_file);
        if (!key) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Cannot open key file %s", key_file);
            display_error(err_str);
            break;
        }

        rsa = EVP_PKEY_get1_RSA(key);
        EVP_PKEY_free(key);

        if (!rsa) {
            display_error("Unable to extract RSA key for RAW PKCS#1 signature");
            break;
        }

        rsa_inbytes = MAX_DIGEST_BYTES;
        rsa_in = OPENSSL_malloc(MAX_DIGEST_BYTES);
        key_bytes = RSA_size(rsa);
        rsa_out = OPENSSL_malloc(key_bytes);

        /* Generate hash data of data from in_file */
        err_value = calculate_hash(in_file, hash_alg, rsa_in, &rsa_inbytes);
        if (err_value != CAL_SUCCESS) {
            break;
        }

        /* Compute signature.  Note: RSA_sign() adds the appropriate DER
         * encoded prefix internally.
         */
        hash_nid = get_NID(hash_alg);
        if (!RSA_sign(hash_nid, rsa_in,
                      rsa_inbytes, rsa_out,
                      (unsigned int *)&rsa_outbytes, rsa)) {
            err_value = CAL_CRYPTO_API_ERROR;
            display_error("Unable to generate signature");
            break;
        }
        else {
            err_value = CAL_SUCCESS;
        }

        /* Copy signature to sig_buf and update sig_buf_bytes */
        *sig_buf_bytes = rsa_outbytes;
        memcpy(sig_buf, rsa_out, rsa_outbytes);
    } while(0);

    if (err_value != CAL_SUCCESS) {
        ERR_print_errors_fp(stderr);
    }

    if (rsa) RSA_free(rsa);
    if (rsa_in) OPENSSL_free(rsa_in);
    if (rsa_out) OPENSSL_free(rsa_out);
    return err_value;
}

/*--------------------------
  cms_to_buf
---------------------------*/
int32_t cms_to_buf(CMS_ContentInfo *cms, BIO * bio_in, uint8_t * data_buffer,
                            size_t * data_buffer_size, int32_t flags)
{
    int32_t err_value = CAL_SUCCESS;
    BIO * bio_out = NULL;
    BUF_MEM buffer_memory;            /**< Used with BIO functions */

    buffer_memory.length = 0;
    buffer_memory.data = (char*)data_buffer;
    buffer_memory.max = *data_buffer_size;

    do {
        if (!(bio_out = BIO_new(BIO_s_mem()))) {
            display_error("Unable to allocate CMS signature result memory");
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        BIO_set_mem_buf(bio_out, &buffer_memory, BIO_NOCLOSE);

        /* Convert cms to der format */
        if (!i2d_CMS_bio_stream(bio_out, cms, bio_in, flags)) {
            display_error("Unable to convert CMS signature to DER format");
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Get the size of bio out in data_buffer_size */
        *data_buffer_size = BIO_ctrl_pending(bio_out);
    }while(0);

    if (bio_out)
        BIO_free(bio_out);
    return err_value;
}

/*--------------------------
  gen_sig_data_cms
---------------------------*/
int32_t
gen_sig_data_cms(const char *in_file,
                 const char *cert_file,
                 const char *key_file,
                 hash_alg_t hash_alg,
                 uint8_t *sig_buf,
                 size_t *sig_buf_bytes)
{
    BIO             *bio_in = NULL;   /**< BIO for in_file data */
    X509            *cert = NULL;     /**< Ptr to X509 certificate read data */
    EVP_PKEY        *key = NULL;      /**< Ptr to key read data */
    CMS_ContentInfo *cms = NULL;      /**< Ptr used with openssl API */
    const EVP_MD    *sign_md = NULL;  /**< Ptr to digest name */
    int32_t err_value = CAL_SUCCESS;  /**< Used for return value */
    /** Array to hold error string */
    char err_str[MAX_ERR_STR_BYTES];
    /* flags set to match Openssl command line options for generating
     *  signatures
     */
    int32_t         flags = CMS_DETACHED | CMS_NOCERTS |
                            CMS_NOSMIMECAP | CMS_BINARY;

    /* Set signature message digest alg */
    sign_md = EVP_get_digestbyname(get_digest_name(hash_alg));
    if (sign_md == NULL) {
        display_error("Invalid hash digest algorithm");
        return CAL_INVALID_ARGUMENT;
    }

    do
    {
        cert = read_certificate(cert_file);
        if (!cert) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Cannot open certificate file %s", cert_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Read key */
        key = read_private_key(key_file,
                           (const pem_password_cb *)get_passcode_to_key_file,
                           key_file);
        if (!key) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Cannot open key file %s", key_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Read Data to be signed */
        if (!(bio_in = BIO_new_file(in_file, "rb"))) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Cannot open data file %s", in_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Generate CMS Signature - can only use CMS_sign if default
         * MD is used which is SHA1 */
        flags |= CMS_PARTIAL;

        cms = CMS_sign(NULL, NULL, NULL, bio_in, flags);
        if (!cms) {
            display_error("Failed to initialize CMS signature");
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        if (!CMS_add1_signer(cms, cert, key, sign_md, flags)) {
            display_error("Failed to generate CMS signature");
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Finalize the signature */
        if (!CMS_final(cms, bio_in, NULL, flags)) {
            display_error("Failed to finalize CMS signature");
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Write CMS signature to output buffer - DER format */
        err_value = cms_to_buf(cms, bio_in, sig_buf, sig_buf_bytes, flags);
    } while(0);

    /* Print any Openssl errors */
    if (err_value != CAL_SUCCESS) {
        ERR_print_errors_fp(stderr);
    }

    /* Close everything down */
    if (cms)      CMS_ContentInfo_free(cms);
    if (cert)     X509_free(cert);
    if (key)      EVP_PKEY_free(key);
    if (bio_in)   BIO_free(bio_in);

    return err_value;
}

/*--------------------------
  error
---------------------------*/
void
display_error(const char *err)
{
    fprintf(stderr, "Error: %s\n", err);
}


/*===========================================================================
                              GLOBAL FUNCTIONS
=============================================================================*/

/*--------------------------
  gen_sig_data
---------------------------*/
int32_t gen_sig_data(const char* in_file,
                     const char* cert_file,
                     hash_alg_t hash_alg,
                     sig_fmt_t sig_fmt,
                     sig_alg_t sig_alg,
                     uint8_t* sig_buf,
                     size_t *sig_buf_bytes)
{
    int32_t err = CAL_SUCCESS; /**< Used for return value */
    char *key_file;            /**< Mem ptr for key filename */

    /* Check for valid arguments */
    if ((!in_file) || (!cert_file) || (!sig_buf) || (!sig_buf_bytes)) {
        return CAL_INVALID_ARGUMENT;
    }

    /* Determine private key filename from given certificate filename */
    key_file = malloc(strlen(cert_file)+1);
#ifdef WIN32
    CRYPTO_malloc_init();
#endif

    err = get_key_file(cert_file, key_file);
    if ( err != CAL_SUCCESS) {
        free(key_file);
        return CAL_FILE_NOT_FOUND;
    }

    if ((sig_fmt == (sig_fmt_t)PKCS1_RSA) && (sig_alg == ECDSA)) {
        free(key_file);
        display_error("Invalid signature format");
        return CAL_INVALID_ARGUMENT;
    }

    if (sig_fmt == (sig_fmt_t)PKCS1_RSA) {
        err = gen_sig_data_raw(in_file, key_file,
                               hash_alg, sig_buf, (int32_t *)sig_buf_bytes);
    }
    else {
        err = gen_sig_data_cms(in_file, cert_file, key_file,
                               hash_alg, sig_buf, sig_buf_bytes);
    }
    free(key_file);
    return err;
}

/*--------------------------
  generate_dek_key
---------------------------*/
int32_t generate_dek_key(uint8_t * key, int32_t len)
{
    if (gen_random_bytes(key, len) != CAL_SUCCESS) {
        return CAL_CRYPTO_API_ERROR;
    }

    return CAL_SUCCESS;
}

/*--------------------------
  write_plaintext_dek_key
---------------------------*/
int32_t write_plaintext_dek_key(uint8_t * key, size_t key_bytes,
                const char * cert_file, const char * enc_file)
{
    int32_t err_value = CAL_SUCCESS;  /**< Return value */
    char err_str[MAX_ERR_STR_BYTES];  /**< Used in preparing error message */
    FILE *fh = NULL;                  /**< File handle used with file api */
#ifdef DEBUG
    int32_t i = 0;                    /**< Used in for loops */
#endif

    do {
        /* Save the buffer into enc_file */
        if ((fh = fopen(enc_file, "wb")) == NULL) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Unable to create binary file %s", enc_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }
        if (fwrite(key, 1, key_bytes, fh) !=
            key_bytes) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Unable to write to binary file %s", enc_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }
        fclose (fh);
   } while(0);

    return err_value;
}


/*--------------------------
  encrypt_dek_key
---------------------------*/
int32_t encrypt_dek_key(uint8_t * key, size_t key_bytes,
                const char * cert_file, const char * enc_file)
{
    X509            *cert = NULL;     /**< Ptr to X509 certificate read data */
	STACK_OF(X509) *recips = NULL;    /**< Ptr to X509 stack */
	CMS_ContentInfo *cms = NULL;      /**< Ptr to cms structure */
    const EVP_CIPHER *cipher = NULL;  /**< Ptr to EVP_CIPHER */
    int32_t err_value = CAL_SUCCESS;  /**< Return value */
    char err_str[MAX_ERR_STR_BYTES];  /**< Used in preparing error message */
    BIO *bio_key = NULL;              /**< Bio for the key data to encrypt */
    uint8_t * enc_buf = NULL;         /**< Ptr for encoded key data */
    FILE *fh = NULL;                  /**< File handle used with file api */
    size_t cms_info_size = MAX_CMS_DATA; /**< Size of cms content info*/
#ifdef DEBUG
    int32_t i = 0;                    /**< Used in for loops */
#endif

    do {
        /* Read the certificate from cert_file */
        cert = read_certificate(cert_file);
        if (!cert) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Cannot open certificate file %s", cert_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

	    /* Create recipient STACK and add recipient cert to it */
	    recips = sk_X509_new_null();

	    if (!recips || !sk_X509_push(recips, cert)) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Cannot instantiate object STACK_OF(%s)", cert_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /*
         * sk_X509_pop_free will free up recipient STACK and its contents
	     * so set cert to NULL so it isn't freed up twice.
	     */
	    cert = NULL;

        /* Instantiate correct cipher */
        if (key_bytes == (AES_KEY_LEN_128 / BYTE_SIZE_BITS))
            cipher = EVP_aes_128_cbc();
        else if (key_bytes == (AES_KEY_LEN_192 / BYTE_SIZE_BITS))
            cipher = EVP_aes_192_cbc();
        else if (key_bytes == (AES_KEY_LEN_256 / BYTE_SIZE_BITS))
            cipher = EVP_aes_256_cbc();
        if (cipher == NULL) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Invalid cipher used for encrypting key %s", enc_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Allocate memory buffer BIO for input key */
        bio_key = BIO_new_mem_buf(key, key_bytes);
        if (!bio_key) {
            display_error("Unable to allocate BIO memory");
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Encrypt content of the key with certificate */
	    cms = CMS_encrypt(recips, bio_key, cipher, CMS_BINARY|CMS_STREAM);
	    if (cms == NULL) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Failed to encrypt key data");
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Finalize the CMS content info structure */
        if (!CMS_final(cms, bio_key, NULL,  CMS_BINARY|CMS_STREAM)) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Failed to finalize cms data");
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Alloc mem to convert cms to binary and save it into enc_file */
        enc_buf = malloc(MAX_CMS_DATA);
        if (enc_buf == NULL) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Failed to allocate memory");
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }

        /* Copy cms info into enc_buf */
        err_value = cms_to_buf(cms, bio_key, enc_buf, &cms_info_size,
            CMS_BINARY);

        /* Save the buffer into enc_file */
        if ((fh = fopen(enc_file, "wb")) == NULL) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Unable to create binary file %s", enc_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }
        if (fwrite(enc_buf, 1, cms_info_size, fh) !=
            cms_info_size) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Unable to write to binary file %s", enc_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }
        fclose (fh);
#ifdef DEBUG
        printf("Encoded key ;");
        for(i=0; i<key_bytes; i++) {
            printf("%02x ", enc_buf[i]);
        }
        printf("\n");
#endif
    } while(0);

    if (cms)
		CMS_ContentInfo_free(cms);
	if (cert)
		X509_free(cert);
	if (recips)
		sk_X509_pop_free(recips, X509_free);
    if (bio_key)
        BIO_free(bio_key);
    return err_value;
}

/*--------------------------
  gen_auth_encrypted_data
---------------------------*/
int32_t gen_auth_encrypted_data(const char* in_file,
                     const char* out_file,
                     aead_alg_t aead_alg,
                     uint8_t *aad,
                     size_t aad_bytes,
                     uint8_t *nonce,
                     size_t nonce_bytes,
                     uint8_t *mac,
                     size_t mac_bytes,
                     size_t key_bytes,
                     const char* cert_file,
                     const char* key_file,
                     int reuse_dek)
{
    int32_t err_value = CAL_SUCCESS;         /**< status of function calls */
    char err_str[MAX_ERR_STR_BYTES];         /**< Array to hold error string */
    uint8_t key[MAX_AES_KEY_LENGTH];         /**< Buffer for random key */
    FILE *fh = NULL;                         /**< Used with files */
    size_t file_size;                        /**< Size of in_file */
    unsigned char *plaintext = NULL;                /**< Array to read file data */
    int32_t bytes_read;
#ifdef DEBUG
    int32_t i;                                        /**< used in for loops */
#endif
    do {
        /* Generate Nonce */
        err_value = gen_random_bytes((uint8_t*)nonce, nonce_bytes);
        if (err_value != CAL_SUCCESS) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                         "Failed to get nonce");
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }
#ifdef DEBUG
        printf("nonce bytes: ");
        for(i=0; i<nonce_bytes; i++) {
            printf("%02x ", nonce[i]);
        }
        printf("\n");
#endif
        if (reuse_dek) {
            fh = fopen(key_file, "rb");
            if (fh == NULL) {
                snprintf(err_str, MAX_ERR_STR_BYTES-1,
                    "Unable to open dek file %s", key_file);
                display_error(err_str);
                err_value = CAL_FILE_NOT_FOUND;
                break;
            }
            /* Read encrypted data into input_buffer */
            bytes_read = fread(key, 1, key_bytes, fh);
            if (bytes_read == 0) {
                snprintf(err_str, MAX_ERR_STR_BYTES-1,
                    "Cannot read file %s", key_file);
                display_error(err_str);
                err_value = CAL_FILE_NOT_FOUND;
                fclose(fh);
                break;
            }
            fclose(fh);
        }
        else {
            /* Generate random aes key to use it for encrypting data */
            err_value = generate_dek_key(key, key_bytes);
            if (err_value) {
                snprintf(err_str, MAX_ERR_STR_BYTES-1,
                             "Failed to generate random key");
                display_error(err_str);
                err_value = CAL_CRYPTO_API_ERROR;
                break;
            }
        }

#ifdef DEBUG
        printf("random key : ");
        for (i=0; i<key_bytes; i++) {
            printf("%02x ", key[i]);
        }
        printf("\n");
#endif
        if (cert_file!=NULL) {
            /* Encrypt key using cert file and save it in the key_file */
            err_value = encrypt_dek_key(key, key_bytes, cert_file, key_file);
            if (err_value) {
                snprintf(err_str, MAX_ERR_STR_BYTES-1,
                         "Failed to encrypt and save key");
                display_error(err_str);
                err_value = CAL_CRYPTO_API_ERROR;
                break;
            }
        } else {
            /* Save key in the key_file */
            err_value = write_plaintext_dek_key(key, key_bytes, cert_file, key_file);
            if (err_value) {
                snprintf(err_str, MAX_ERR_STR_BYTES-1,
                         "Failed to save key");
                display_error(err_str);
                err_value = CAL_CRYPTO_API_ERROR;
                break;
            }
        }
        /* Get the size of in_file */
        fh = fopen(in_file, "rb");
        if (fh == NULL) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                     "Unable to open binary file %s", in_file);
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }
        fseek(fh, 0, SEEK_END);
        file_size = ftell(fh);
        plaintext = (unsigned char*)malloc(file_size);;
        if (plaintext == NULL) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                         "Not enough allocated memory" );
            display_error(err_str);
            err_value = CAL_CRYPTO_API_ERROR;
            break;
        }
        fclose(fh);

        fh = fopen(in_file, "rb");
        if (fh == NULL) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                         "Cannot open file %s", in_file);
            display_error(err_str);
            err_value = CAL_FILE_NOT_FOUND;
            break;
        }

        /* Read encrypted data into input_buffer */
        bytes_read = fread(plaintext, 1, file_size, fh);
        /* Reached EOF? */
        if (bytes_read == 0) {
            snprintf(err_str, MAX_ERR_STR_BYTES-1,
                         "Cannot read file %s", out_file);
            display_error(err_str);
            err_value = CAL_FILE_NOT_FOUND;
           break;
        }

        err_value = encryptccm(plaintext, file_size, aad, aad_bytes,
                               key, key_bytes, nonce, nonce_bytes, out_file,
                               mac, mac_bytes, &err_value, err_str);
        if (err_value == CAL_NO_CRYPTO_API_ERROR) {
            printf("Encryption not enabled\n");
            break;
        }
    } while(0);

    free(plaintext);

    /* Clean up */
    return err_value;
}
