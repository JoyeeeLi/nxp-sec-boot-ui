/*
 * Copyright 2017-2018 NXP
 */

#ifndef CSF_PARSER_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>

#define IVT_HDR_VAL         0x402000d1
#define IVT_HDR_MASK        0xf0ffffff

#define assert(x)       if ((x) == 0) { \
                                printf("ASSERT failed at %s:%d\n", __FUNCTION__, __LINE__);    \
                                exit(2); \
                        }

#define HAB_HDR_LEN(h) ((((uint8_t *)&((h)->len))[0] << 8)    \
                        | (((uint8_t *)&((h)->len))[1]))

#define HAB_TAG_CSF      0xD4 /* Command Sequence File HAB_TAG_CSF */

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

typedef struct __attribute__((packed)) {
        uint8_t tag;
        uint16_t len;
        uint8_t flags;
} hab_hdr_t;

int debug_log;
FILE *fp_debug;

#endif /* CSF_PARSER_H */

const uint8_t *extract_csf(const uint8_t *buf, int buf_size, int *csf_len);
