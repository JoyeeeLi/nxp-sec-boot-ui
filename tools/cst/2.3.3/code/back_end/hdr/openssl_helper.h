#ifndef __OPENSSL_HELPER_H
#define __OPENSSL_HELPER_H
/*===========================================================================*/
/**
    @file    openssl_helper.h

    @brief   Provide helper functions to ease openssl tasks and also defines
             common macros that can used across different tools

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
Fareed Mohammed       06-Apr-2011      ENGR140621  Initial Version
Auger Florent         18-Jul-2012      ENGR169493  Added prototype for the
                                                   new function print_version()
Fareed Mohammed       10-Sep-2012      ENGR169497  Add encryption support
=============================================================================
Portability:

These definitions are customised for 32 bit cores of either endianness.

=============================================================================
@endverbatim */

/*===========================================================================
                                INCLUDE FILES
=============================================================================*/
#include "adapt_layer.h"

/*===========================================================================
                                 CONSTANTS
=============================================================================*/

#define TRUE                      1 /**< Success val returned by functions */
#define FALSE                     0 /**< Failure val returned by functions */

#define X509_UTCTIME_STRING_BYTES 13 /**< Expected length of validity period
                                       *   strings in X.509 certificates using
                                       *   UTCTime format
                                       */
#define X509_GENTIME_STRING_BYTES 15 /**< Expected length of validity period
                                       *   strings in X.509 certificates using
                                       *   Generalized Time format
                                       */
#define PEM_FILE_EXTENSION        ".pem"   /* PEM file extention */
#define PEM_FILE_EXTENSION_BYTES  4        /* Length of pem extention */

/* Message digest string definitions */
#define HASH_ALG_SHA1             "sha1"   /**< String macro for sha1 */
#define HASH_ALG_SHA256           "sha256" /**< String macro for sha256 */

/* Message digest length definitions */
#define HASH_BYTES_SHA1           20   /**< Size of SHA1 output bytes */
#define HASH_BYTES_SHA256         32   /**< Size of SHA256 output bytes */
#define HASH_BYTES_SHA512         64   /**< Size of SHA512 output bytes */

/*===========================================================================
                                 CONSTANTS
=============================================================================*/

/** Extracts a byte from a given 32 bit word value
 *
 * @param [in] val value to extract byte from
 *
 * @param [in] bit_shift Number of bits to shift @a val left before
 *                       extracting the least significant byte
 *
 * @returns the least significant byte after shifting @a val to the left
 *          by @a bit_shift bits
 */
#define EXTRACT_BYTE(val, bit_shift) \
    (((val) >> (bit_shift)) & 0xFF)

/*============================================================================
                                      ENUMS
=============================================================================*/

typedef enum cst_status
{
    CST_FAILURE = FALSE,
    CST_SUCCESS = TRUE
} cst_status_t;

/*============================================================================
                           STRUCTURES AND OTHER TYPEDEFS
=============================================================================*/

/*============================================================================
                           GLOBAL VARIABLE DECLARATIONS
=============================================================================*/

/*============================================================================
                                FUNCTION PROTOTYPES
=============================================================================*/

/** openssl_initialize
 *
 * Initializes the openssl library.  This function must be called once
 * by the program using any of the openssl helper functions
 *
 */
extern void
openssl_initialize();

/** Unix time
 *
 * Converts the validity time provided in X.509 certificates to Unix time
 * required for WTLS certificates.
 *
 * @param[in] x509_time String with format: YYMMDDHHMMSSZ or YYYYMMDDHHMMSSZ
 *
 * @pre  Input X.509 certificate has validity period.
 *
 * @returns 32 bit time in UNIX format if successful, 0 otherwise
 */
extern uint32_t
unix_time(const char *x509_time);

/** Computes hash digest
 *
 * Calls openssl API to generate hash for the given data in buf.
 *
 * @param[in] buf, binary data for hashing
 *
 * @param[in] msg_bytes, size in bytes for binary data
 *
 * @param[in] hash_alg, character string containing hash algorithm,
 *                      "sha1" or "sha256"
 *
 * @param[out] hash_bytes, size of digest result in bytes
 *
 * @pre  #openssl_initialize has been called previously
 *
 * @pre  @a buf and @a hash_alg are not NULL.
 *
 * @post It is the responsibilty of the caller to free the memory allocated by
 *       this function holding the computed hash result.
 *
 * @returns The location of the digest result if successful, NULL otherwise
 */
extern uint8_t *
generate_hash(const uint8_t *buf, size_t msg_bytes, const char *hash_alg,
              size_t *hash_bytes);

/** get_bn
 *
 * Extracts data from an openssl BIGNUM type to a byte array.  Used
 * for extracting certificate data such as an RSA public key modulus.
 *
 * @param[in] a      BIG_NUM structure
 *
 * @param[out] bytes size of resulting byte array
 *
 * @pre @a a and @a bytes are not NULL
 *
 * @post It is the responsibilty of the caller to free the memory allocated by
 *       this function holding the big number result.
 *
 * @returns location of resulting byte array or NULL if failed to alloc mem.
 */
extern uint8_t*
get_bn(const BIGNUM *a, size_t *bytes);


/** sign_data
 *
 * Signs a data buffer with a given private key
 *
 * @param[in] skey       signer private key
 *
 * @param[in] bptr       location of data buffer to digitally sign
 *
 * @param[in] hash_alg   hash digest algorithm
 *
 * @param[out] sig_bytes size of resulting signature buffer
 *
 * @pre  #openssl_initialize has been called previously
 *
 * @post It is the responsibilty of the caller to free the memory allocated by
 *       this function holding the signature  result.
 *
 * @returns if successful returns location of resulting byte array otherwise
 * NULL.
 */
extern uint8_t*
sign_data(const EVP_PKEY *skey, const BUF_MEM *bptr, hash_alg_t hash_alg,
          size_t *sig_bytes);

/** write_cert_file
 *
 * Writes WTLS certificate data to a binary file
 *
 * @param[in] filename    filename of WTLS certificate file
 *
 * @param[in] data        WTLS certificate data
 *
 * @post if successful the contents of the WTLS certificate are written to
 *       the output file.
 *
 * @returns if successful function returns #CST_SUCCESS otherwise #CST_FAILURE
 */
extern cst_status_t
write_cert_file(const char *filename, const BIO *wtls_cert);

/** read_certificate
 *
 * Read X.509 certificate data from given certificate file
 *
 * @param[in] filename    filename of certificate file
 *
 * @post if successful the contents of the certificate are extracted to X509
 * object.
 *
 * @pre  #openssl_initialize has been called previously
 *
 * @post caller is responsible for releasing X.509 certificate memory.
 *
 * @returns if successful function returns location of X509 object
 *   otherwise NULL.
 */
extern X509*
read_certificate(const char* filename);

/** get_der_encoded_certificate_data
 *
 * Read X.509 certificate data from given certificate file and calls openssl
 * to encode X509 to DER format and returns DER formatted data located at
 * @derder.
 *
 * @param[in] filename    filename, function will work with both PEM and DER
 *                        input certificate files.
 *
 * @param[out] der        address to write der data
 *
 * @post if successful the contents of the certificate are written at address
 * @a der.
 *
 * @pre  #openssl_initialize has been called previously
 *
 * @post caller is responsible for releasing memory location returned in @a der
 *
 * @returns if successful function returns number of bytes written at address
 * @a der, 0 otherwise.
 */
extern int32_t get_der_encoded_certificate_data(const char* filename,
                                           uint8_t ** der);

/** read_private_key
 *
 * Uses openssl API to read private key from given certificate file
 *
 * @param[in] filename    filename of key file
 *
 * @param[in] password_cb callback fn to provide password for keyfile
 *            see openssl's pem.h for callback'e prototype
 *
 * @param[in] password    password for keyfile
 *
 * @post if successful the contents of the private key are extracted to
 * EVP_PKEY object.
 *
 * @pre  #openssl_initialize has been called previously
 *
 * @post caller is responsible for releasing the private key memory.
 *
 * @returns if successful function returns location of EVP_PKEY object
 *   otherwise NULL.
 */
extern EVP_PKEY*
read_private_key(const char *filename, const pem_password_cb *password_cb,
                 const char *password);

/** seed_prng
 *
 * Calls openssl API to seed prng to given bytes randomness
 *
 * @param[in] bytes   bytes to randomize the seed
 *
 * @pre  None
 *
 * @post None
 */
uint32_t seed_prng(uint32_t bytes);

/** gen_random_bytes
 *
 * Generates random bytes using openssl RAND_bytes
 *
 * @param[out] buf    buf to return the random bytes
 *
 * @param[in] bytes   size of the buf in bytes and number of random bytes
 *                    to generate
 *
 * @pre  None
 *
 * @post None
 */
int32_t gen_random_bytes(uint8_t *buf, size_t bytes);

/** Diplays program license information to stdout
 *
 * @pre  None
 *
 * @post None
 */
extern void
print_license(void);

/** Diplays program version information to stdout
 *
 * @pre  None
 *
 * @post None
 */
extern void
print_version(void);

#endif /* __OPENSSL_HELPER_H */
