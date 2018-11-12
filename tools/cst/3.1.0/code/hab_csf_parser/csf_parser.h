/*
 * Copyright 2017-2018 NXP
 */

#ifndef CSF_PARSER_H
#define CSF_PARSER_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>
#include <getopt.h>

#define PASS 1
#define FAIL 0

/* For little endian systems */
#define from_be32(x) \
        ((((x) & 0x000000ff) << 24) | \
        (((x) & 0x0000ff00) << 8 ) | \
        (((x) & 0x00ff0000) >> 8 ) | \
        (((x) & 0xff000000) >> 24))

#define assert(x)       if ((x) == 0) { \
                                printf("ASSERT failed at %s:%d\n", __FUNCTION__, __LINE__);    \
                                exit(2); \
                        }

#define validate(x,y)   if ((x) == 0) { \
                                printf("Invalid "y" in function %s\n", __FUNCTION__); \
                                return FAIL; \
                        }

/* Write to file */
#define w2f_hdr(x)      do { if(fp_output) { \
                                fprintf(fp_output, x"\tVALUE\t\tDEFINITION\t\tDESCRIPTION\n"); \
                                fprintf(fp_output, "----------------------------------------------------------------------\n"); \
                           } \
                        } while(0);


/*******************************************************************************
                        MACROS
*******************************************************************************/

#define IVT_HDR_VAL         0x402000d1
#define IVT_HDR_MASK        0xf0ffffff

#define HAB_HDR_LEN(h) ((((uint8_t *)&((h)->len))[0] << 8)    \
                        | (((uint8_t *)&((h)->len))[1]))

#define CHECK_BIT(x,y)  (x & y) == y

#define getAbs(x) (HAB_HDR_LEN(x) & 3)

#define MAX_STRING_LENGTH       30
#define MIN_AUT_DAT_CMD_LEN     12
#define MIN_UNLK_CMD_LEN        8
#define HAB_ENG_CONF_MASK       0xDB
#define HAB_HDR_SIZE            4
#define HAB_UNLK_FEAT_MASK      0xF

/************************
        HAB tags
************************/
#define HAB_TAG_IVT      0xD1 /* Image Vector Table HAB_TAG_IVT */
#define HAB_TAG_DCD      0xD2 /* Device Configuration Data HAB_TAG_DCD */
#define HAB_TAG_CSF      0xD4 /* Command Sequence File HAB_TAG_CSF */
#define HAB_TAG_CRT      0xD7 /* Certificate HAB_TAG_CRT */
#define HAB_TAG_SIG      0xD8 /* Signature HAB_TAG_SIG */
#define HAB_TAG_MAC      0xAC /* Message Authentication Code */

#define HAB_CMD_INS_KEY  0xBE /* Insert key command HAB_CMD_INS_KEY */
#define HAB_CMD_AUT_DAT  0xCA /* Authenticate Data command HAB_CMD_AUT_DAT */
#define HAB_CMD_SET      0xB1 /* Set command HAB_CMD_SET */
#define HAB_CMD_WRT_DAT  0xCC /* Write Data command HAB_CMD_WRT_DAT */
//#define HAB_CMD_CHK_DAT  0xCF /* Check Data HAB_CMD_CHK_DAT */
//#define HAB_CMD_NOP      0xC0 /* No Operation command HAB_CMD_NOP */
#define HAB_CMD_INIT     0xB4 /* Initialize command HAB_CMD_INIT */
#define HAB_CMD_UNLK     0xB2 /* Unlock command HAB_CMD_UNLK */

#define HAB_KEY_PUBLIC   0xE1 /* Public Key HAB_KEY_PUBLIC */
#define HAB_KEY_SECRET   0xE2 /* Secret Key HAB_KEY_SECRET */
#define HAB_KEY_MASTER   0xED /* Master Key Encryption Key HAB_KEY_MASTER */
#define HAB_KEY_HASH     0xEE /* Hash HAB_KEY_HASH */

/************************
        HAB version flags
************************/

#define HAB_VER_40      0x40 /* HAB 4.0: 0x40 */
#define HAB_VER_41      0x41 /* HAB 4.1: 0x41 */
#define HAB_VER_42      0x42 /* HAB 4.2: 0x42 */

/************************
        HAB engines
************************/

#define HAB_ENG_ANY      0x00 /* Any HAB will chose the most appropriate engine */
#define HAB_ENG_CAAM     0x1D /* CAAM HAB_ENG_CAAM */
#define HAB_ENG_SNVS     0x1E /* Secure Non-Volatile Storage HAB_ENG_SNVS */
#define HAB_ENG_OCOTP    0x21 /* On Chip OTP memory HAB_ENG_OCOTP */
#define HAB_ENG_SW       0xFF /* Software Engine HAB_ENG_SW */
#define HAB_ENG_SAHARA   0x06 /* Crypto accelerator */
#define HAB_ENG_SCC      0x03 /* Security controller */
#define HAB_ENG_DCP      0x1b /* Data Co-Processor */
#define HAB_ENG_RTIC     0x05 /* Run-time integrity checker */

/************************
        HAB engine configurations
************************/

#define HAB_ANY_CONF_DEFAULT  0x00 /* ANY 0x00 */
#define HAB_CAAM_DEFAULT      0x00 /* Default: 0x00 */
#define HAB_CAAM_IN_SWAP8     0x01 /* IN SWAP8: 0x01 */
#define HAB_CAAM_IN_SWAP16    0x02 /* IN SWAP16: 0x02 */
#define HAB_CAAM_OUT_SWAP8    0x08 /* OUT SWAP8: 0x08 */
#define HAB_CAAM_OUT_SWAP16   0x10 /* OUT SWAP16: 0x10 */
#define HAB_CAAM_DSC_SWAP8    0x40 /* DSC SWAP8: 0x40 */
#define HAB_CAAM_DSC_SWAP16   0x80 /* DSC SWAP16: 0x80 */
#define HAB_SW_CONF_DEFAULT   0x00 /* SW 0x00 */
#define HAB_SAHARA_DEFAULT    0x00 /* Default: 0x00 */
#define HAB_SAHARA_IN_SWAP8   0x01 /* Set MESS BYTE SWAP bit (reverse message
                                        bytes within word on input to
                                        SAHARA) */
#define HAB_SAHARA_IN_SWAP16  0x02 /* Set MESS HALF WORD SWAP bit (reverse
                                        message half-words within word on
                                        input to SAHARA)  */
#define HAB_SAHARA_DSC_BE8_16 0x10/**< Interpret descriptors and links as for
                                        BE-8 16-bit memory. */
#define HAB_SAHARA_DSC_BE8_32 0x20 /**< Interpret descriptors and links as for
                                        BE-8 32-bit memory. */
#define HAB_DCP_DEFAULT       0x00 /* Default: 0x00 */
#define HAB_DCP_IN_SWAP8      0x01 /* Set INPUT BYTE SWAP bit (reverse bytes
                                         within words on input to DCP) */
#define HAB_DCP_IN_SWAP32     0x04 /* Set INPUT WORD SWAP bit (ignored for
                                        hashing)  */
#define HAB_DCP_OUT_SWAP8     0x08 /* Set OUPUT BYTE SWAP bit (reverse bytes
                                        within words on output from DCP) */
#define HAB_DCP_OUT_SWAP32    0x20 /* Set OUTPUT WORD SWAP bit (ignored for
                                        hashing)  */
#define HAB_RTIC_DEFAULT      0x00 /* Default: 0x0 */
#define HAB_RTIC_IN_SWAP8     0x01 /* Set BYTE SWAP bit (reverse bytes within
                                        word on input to RTIC) */
#define HAB_RTIC_IN_SWAP16    0x02 /* Set HALF WORD SWAP bit (reverse
                                        half-words within word on input to
                                        RTIC)  */
#define HAB_RTIC_OUT_SWAP8    0x08 /* Set HASH RESULT BYTE SWAP bit (reverse
                                        bytes within word on output from RTIC) */
#define HAB_RTIC_KEEP         0x80 /* Retain reference hash value for later
                                        monitoring */

/************************
        HAB Insert key flags
************************/

#define HAB_CMD_INS_KEY_NO_FLAG 0x00 /* No flags */
#define HAB_CMD_INS_KEY_ABS     0x01 /* Use absolute address for the key */
#define HAB_CMD_INS_KEY_CSF     0x02 /* Install CSF Key */

/************************
        HAB Insert key certificate format
************************/

#define HAB_PCL_SRK     0x03 /* SRK format HAB_PCL_SRK */
#define HAB_PCL_X509    0x09 /* X509 format HAB_PCL_X509 */
// #define HAB_PCL_CMS     0xc5 /* CMS/PKCS#7 signature format */
#define HAB_PCL_BLOB    0xbb /* SHW-specific wrapped key format */
// #define HAB_PCL_AEAD    0xa3 /* Proprietary AEAD MAC format */

/************************
        HAB Insert key hash algorithm
************************/

#define HAB_ALG_NO_ALG  0x00 /* No hash algorithm */
#define HAB_ALG_SHA1    0x11 /* SHA-1 algorithm ID */
#define HAB_ALG_SHA256  0x17 /* SHA-256 algorithm ID */
#define HAB_ALG_SHA512  0x1b /* SHA-512 algorithm ID */

/************************
        HAB Authenticate data flags
************************/

#define HAB_CMD_AUT_DAT_NO_FLAG         0x00 /* No flags */
#define HAB_CMD_AUT_DAT_ABS             0x01 /* Use absolute address for the key */

/************************
        HAB Authenticate data Signature format
************************/

#define HAB_CMD_AUT_DAT_PCL_CMS         0xC5
#define HAB_CMD_AUT_DAT_PCL_AEAD        0xA3 /* Proprietary AEAD MAC format */

/************************
        HAB Unlock command flags
************************/

#define HAB_CMD_UNLOCK_CAAM_MID       0x01 /* CAAM MID No Leave Job Ring and
                                              DECO master ID registers unlocked. */
#define HAB_CMD_UNLOCK_CAAM_RNG       0x02 /* RNG No Leave RNG uninstantiated */
#define HAB_CMD_UNLOCK_CAAM_MFG       0x04 /* MFG Manufacturing Protection unlocked */

#define HAB_CMD_UNLOCK_SNVS_LP_SWR    0x01 /* SNVS LP SWR Leave LP SW reset
                                              unlocked. 0x01 */
#define HAB_CMD_UNLOCK_SNVS_ZMK_WRITE 0x02 /* ZMK WRITE Leave Zeroisable Master
                                              Key write unlocked. 0x02 */
#define HAB_CMD_UNLOCK_OCOTP_FLD_RTN  0x01 /* OCOTP Field Return Leave Field
                                              Return activation unlocked. 0x01 */
#define HAB_CMD_UNLOCK_OCOTP_SRK_RVK  0x02 /* SRK Revoke Leave SRK revocation
                                              unlocked. 0x02 */
#define HAB_CMD_UNLOCK_OCOTP_SCS      0x04 /* SCS No Leave SCS register unlocked */
#define HAB_CMD_UNLOCK_OCOTP_JTAG     0x08 /* JTAG No Unlock JTAG using SCS
                                              HAB_JDE bit. 0x08 */

#define HAB_DCP_BLOCK_MAX    6  /* Maximum on non-contiguous memory blocks
                                   supported for DCP operations */
#define HAB_SAHARA_BLOCK_MAX 12 /* Maximum on non-contiguous memory blocks
                                   supported for SAHARA operations */
#define HAB_CAAM_BLOCK_MAX   8  /* Maximum on non-contiguous memory blocks
                                   supported for CAAM operations */

/* HAB Engine variable configuration */
#define HAB_VAR_CFG_ITM_ENG 0x03 /**< Preferred engine for a given algorithm */

/************************
        Command line arguments
************************/
/* Valid short command line option letters. */
const char* const short_opt = "hds:c:";

/* Valid long command line options. */
const struct option long_opt[] =
{
        {"enable-debug", no_argument, 0, 'd'},
        {"signed-image", required_argument,  0, 's'},
        {"csf-binary", required_argument,  0, 'c'},
        {"help", no_argument, 0, 'h'},
        {NULL, 0, NULL, 0}
};

typedef struct __attribute__((packed)) {
        uint32_t header;
        uint32_t start;
        uint32_t res1;
        uint32_t dcd;
        uint32_t boot_data;
        uint32_t self;
        uint32_t csf;
        uint32_t res2;
} ivt_t;

/************************
        HAB STRUCTURES
************************/
typedef struct __attribute__((packed)) {
        uint8_t  tag;
        uint16_t len;
        uint8_t  version;
} csf_hdr_t;

typedef struct __attribute__((packed)) {
        uint8_t tag;
        uint16_t len;
        uint8_t flags;
} hab_hdr_t;

typedef struct __attribute__((packed)) {
        uint8_t cmd;
        uint16_t len;
        uint8_t flags;

        uint8_t cert_fmt;
        uint8_t hash_alg;
        uint8_t src_index;
        uint8_t tgt_index;

        uint32_t key_loc;
} csf_cmd_ins_key_t;

typedef struct __attribute__((packed)) {
        uint32_t address;
        uint32_t size;
} region_t;

typedef struct __attribute__((packed)) {
        uint8_t cmd;
        uint16_t len;
        uint8_t flags;

        uint8_t key;
        uint8_t sig_fmt;
        uint8_t engine;
        uint8_t eng_cfg;

        uint32_t sig_loc;

        region_t region[0];
} csf_cmd_aut_dat_t;

typedef struct __attribute__((packed)) {
        uint8_t cmd;
        uint16_t len;
        uint8_t engine;
        uint32_t features;
        uint64_t uid;
} csf_cmd_unlock_t;

typedef struct __attribute__((packed)) {
        uint8_t cmd;
        uint16_t len;
        uint8_t cfg_itm;
        uint8_t res;
        uint8_t alg;
        uint8_t engine;
        uint8_t eng_cfg;
} csf_cmd_set_t;

typedef struct __attribute__((packed)) {
        uint8_t tag;
        uint16_t len;
        uint8_t version;

        uint8_t cert[];
} csf_sec_cert_t;

typedef struct __attribute__((packed)) {
        uint8_t tag;
        uint16_t len;
        uint8_t version;

        uint8_t sig[];
} csf_sec_sig_t;

typedef struct __attribute__((packed)) {
        uint8_t tag;
        uint16_t len;
        uint8_t version;

        uint8_t res1;
        uint8_t nonce_bytes;
        uint8_t res2;
        uint8_t mac_bytes;

        uint8_t nonce_mac[];
} csf_sec_mac_t;

FILE *fp_output;
extern FILE *fp_debug;
extern int debug_log;

#endif /* CSF_PARSER_H */
