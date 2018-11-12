/*
 * Copyright 2017-2018 NXP
 */

#include "extract_csf.h"

/* @Function    : extract_csf
 * @Description : This function parses the input image and
 *                finds the location of csf
 *
 * @inputs      : buf      - Pointer to the start of image
 *                buf_size - Length of image
 *
 * @Outputs     : csf_len  - Length of the CSF binary
 *                Return location CSF or NULL if error
 *
 */
const uint8_t *extract_csf(const uint8_t *buf, int buf_size, int *csf_len)
{
        assert(buf != NULL);

        int pos = 0;
        const ivt_t *ivt = (const ivt_t *)buf;
        long csf_pos;
        hab_hdr_t *hdr;
        int csf_hdr_len;

        /* Find the header of the IVT - must be on a 32 bit alignment */
        while((ivt->header & IVT_HDR_MASK) != IVT_HDR_VAL) {
                pos += 4;
                if (pos > (buf_size - sizeof(ivt_t))) {
                        puts("Reached end of file. CSF not found.\n");
                        return NULL;
                }

                ivt = (const ivt_t *)&buf[pos];
        }

        if (debug_log) {
                fprintf(fp_debug, "\nIVT : HEADER    = 0x%08X\n",ivt->header);
                fprintf(fp_debug, "      START     = 0x%08X\n",ivt->start);
                fprintf(fp_debug, "      RES1      = 0x%08X\n",ivt->res1);
                fprintf(fp_debug, "      DCD       = 0x%08X\n",ivt->dcd);
                fprintf(fp_debug, "      BOOT DATA = 0x%08X\n",ivt->boot_data);
                fprintf(fp_debug, "      SELF      = 0x%08X\n",ivt->self);
                fprintf(fp_debug, "      CSF       = 0x%08X\n",ivt->csf);
                fprintf(fp_debug, "      RES2      = 0x%08X\n\n",ivt->res2);
                fprintf(fp_debug, "IVT found at offset = 0x%08X\n", pos);
                fprintf(fp_debug, "\n");
        }

        csf_pos = pos + (ivt->csf - ivt->self);
        if (ivt->csf != 0 && csf_pos > (buf_size - sizeof(hab_hdr_t))) {
                /* CSF is out of bounds */
                puts("CSF out of bounds or non existent.\n");
                return NULL;
        }

        if (debug_log) {
                fprintf(fp_debug, "CSF found at offset = 0x%08X\n", (int)csf_pos);
        }

        hdr = (hab_hdr_t *)&buf[csf_pos];

        if (hdr->tag != HAB_TAG_CSF) {
                /* Not a CSF */
                puts("Not a CSF.\n");
                return NULL;
        }

        csf_hdr_len = HAB_HDR_LEN(hdr);

        if ((csf_pos + csf_hdr_len) < buf_size) {
                *csf_len = buf_size - csf_pos;
                /* Create CSF file out of Image file */
                FILE *fp_csf = fopen("output/csf.bin", "w");
                if (fp_csf) {
                        fwrite(&buf[csf_pos], *csf_len, 1, fp_csf);
                        puts("CSF file created\n");
                }
                else
                        puts("Unable to create CSF file\n");

                fclose(fp_csf);
                return &buf[csf_pos];
        } else {
                return NULL;
        }
}
