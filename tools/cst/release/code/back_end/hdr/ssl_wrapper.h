#ifndef SSL_WRAPPER_H
#define SSL_WRAPPER_H
/*===========================================================================

    @file    ssl_wrapper.h

=============================================================================

              Freescale Semiconductor Confidential Proprietary
        (c) Freescale Semiconductor, Inc. 2011-2015. All rights reserved.

Presence of a copyright notice is not an acknowledgement of
publication. This software file listing contains information of
Freescale Semiconductor, Inc. that is of a confidential and
proprietary nature and any viewing or use of this file is prohibited
without specific written permission from Freescale Semiconductor, Inc.

===========================================================================*/

/*===========================================================================
                            INCLUDE FILES
=============================================================================*/
#ifndef REMOVE_ENCRYPTION
#include <openssl/evp.h>
#endif
#include <adapt_layer.h>
/*===========================================================================
                              CONSTANTS
=============================================================================*/

/*===========================================================================
                                MACROS
=============================================================================*/

/*===========================================================================
                                ENUMS
=============================================================================*/

/*===========================================================================
                    STRUCTURES AND OTHER TYPEDEFS
=============================================================================*/

/*===========================================================================
                     GLOBAL VARIABLE DECLARATIONS
=============================================================================*/

/*===========================================================================
                         FUNCTION PROTOTYPES
=============================================================================*/
#ifdef __cplusplus
extern "C" {
#endif
void handle_errors(char * str,  int32_t *err_value, char *err_str);

int32_t encryptccm(unsigned char *plaintext, int plaintext_len, unsigned char *aad,
                   int aad_len, unsigned char *key, int key_len, unsigned char *iv,
                   int iv_len, const char * out_file, unsigned char *tag, int tag_len,
                   int32_t *err_value, char *err_str);

#ifdef __cplusplus
}
#endif

#endif /* SSL_WRAPPER_H  */



