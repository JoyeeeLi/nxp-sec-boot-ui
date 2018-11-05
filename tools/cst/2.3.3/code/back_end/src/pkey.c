/*===========================================================================*/
/**
    @file    pkey.c

    @brief   Implements private key access API. This is part of libpkey.a
    library. The functionality of these API can be customized by linking to
    customer version of libpkey.a owned by customer.

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

                 Modification Date  Tracking
Author             (dd-mmm-yyyy)    Number      Description of Changes
---------------    -------------   ----------  -----------------------
Fareed Mohammed     12-Sep-2011                Initial version
Florent Auger       28-Aug-2012    ENGR162295  Path to key file built from CSF

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
#include <openssl/bio.h>
#include <openssl/x509.h>
#include <openssl/x509v3.h>
#include <openssl/cms.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl_helper.h>
#include <adapt_layer.h>
//#ifdef WIN32
//#include <openssl/applink.c>
//#endif

/*===========================================================================
                          LOCAL FUNCTION PROTOTYPES
=============================================================================*/
/** Chomp - removes newline from character string
 *
 * @param[in] s    input string
 *
 * @pre None
 *
 * @post s is modified removing new line characters
 */
static void
chomp(char *s);

/*===========================================================================
                               LOCAL FUNCTIONS
=============================================================================*/
/*--------------------------
  chomp
---------------------------*/
void
chomp(char *s)
{
    while(*s && *s != '\n' && *s != '\r') s++;
    *s = 0;
}

/*--------------------------
  get_passcode_to_key_file
---------------------------*/
int get_passcode_to_key_file(char *buf, int size, int rwflag, void *userdata)
{
    FILE * password_fp;
    char * ptr_to_last_slash;
    char key_file_path[255];
    char *key_file = (char *)userdata;

    /* Initialize the temporary path */
    memset(key_file_path,0,255);

    /*
     * Get the folder where the password file is present.
     * The file is located in the same folder than the keys used for signature.
     * Start by searching for the last occurance of '/' in the path of
     * a key installed by a CSF command and passed through *userdata.
     */
    ptr_to_last_slash = strrchr(key_file, '/');

    /* Copy from beginning to ptr_to_last_slash into key_file_path */
    if(ptr_to_last_slash != NULL)
    {
        strncpy(key_file_path, key_file, (ptr_to_last_slash -
                               key_file + 1));
    }

    /* Concatenate with key_pass.txt to form the complete path */
    strcat(key_file_path, "key_pass.txt");

    /*
     * This particular implementation assumes file key_file.txt to be present
     * in keys folder with password string.
     */
    password_fp = fopen(key_file_path, "r");
    if (password_fp == NULL)
    {
        /* Cannot open password file, it could be that keys are not encrypted
         * return 0 for password size */
        return 0;
    }

    fgets(buf, size, password_fp);
    chomp(buf);

    return strlen(buf);
}

/*--------------------------
  get_key_file
---------------------------*/
int32_t get_key_file(const char* cert_file, char* key_file)
{
    /* Algorithm to locate key file from given cert file  */
    /* for now just assume the key to present in the      */
    /* same folder as cert file. The crt in the name will */
    /* will be replaced with key */
    char * folder;
    int32_t i = strlen(cert_file);  /**< Index into key filename, initialized
                                         to filename length */

    strcpy(key_file, cert_file);
    key_file[i] = 0;

    key_file[i-5] = 'y';
    key_file[i-6] = 'e';
    key_file[i-7] = 'k';

    /* Search for folder name "certs" in the file and replace it with "keys" */
    /* Keys are found in "keys" folder and certs are in "certs" folder       */

    folder = strstr(key_file, "crts");
    if(folder)
    {
        folder[0] = 'k';
        folder[1] = 'e';
        folder[2] = 'y';
        folder[3] = 's';
    }
    return CAL_SUCCESS;
}
