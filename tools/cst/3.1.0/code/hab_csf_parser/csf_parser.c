/*
 * Copyright 2017-2018 NXP
 */

#include "csf_parser.h"
#include "extract_csf.h"

/* @Function    : parse_mac_sec
 * @Description : This function parses the MAC Section in CSF
 *                and prints the parsed content
 *
 * @Inputs      : csf_hdr - Pointer to the start of CSF
 *                csf_len - Length of CSF
 *                offset  - Offset from beginning of CSF
 *
 * @Outputs     : return length of MAC
 *
 */
int parse_mac_sec(const uint8_t *csf_hdr, int csf_len, int offset)
{
        assert(csf_hdr != NULL);

        validate(csf_len != 0, "csf length");

        csf_sec_mac_t *mac_sec_temp = (csf_sec_mac_t *)csf_hdr;

        int i, mac_sec_len;

        if (debug_log) {
                fprintf(fp_debug, "Parsing following values\n");
                for (i=0; i < HAB_HDR_LEN(mac_sec_temp) ; i++)
                        fprintf(fp_debug, "0x%02X ", csf_hdr[i]);
                fprintf(fp_debug, "\n");
        }

        validate(mac_sec_temp->tag == HAB_TAG_MAC, "tag");
        validate((mac_sec_temp->version == HAB_VER_40 || \
                  mac_sec_temp->version == HAB_VER_41 || \
                  mac_sec_temp->version == HAB_VER_42 ), "hab version");
        validate((offset + HAB_HDR_LEN(mac_sec_temp)) <= csf_len, "length OOB");
        validate((HAB_HDR_LEN(mac_sec_temp) == (mac_sec_temp->nonce_bytes + \
                                                mac_sec_temp->mac_bytes + \
                                                sizeof(hab_hdr_t) + sizeof(hab_hdr_t))), \
                                                "MAC Nonce length");

        csf_sec_mac_t *mac_sec = malloc(HAB_HDR_LEN(mac_sec_temp));
        if (memcpy(mac_sec, csf_hdr, HAB_HDR_LEN(mac_sec_temp)) == NULL) {
                puts("Error: Memcopy to copy mac section contents failed.\n");
                free(mac_sec);
                return FAIL;
        }

        fprintf(fp_output, "\n\n");
        w2f_hdr("TAG");
        fprintf(fp_output, "   \t0x%X\t\tHAB_TAG_MAC\t\tMAC and Nonce\n\n", mac_sec->tag);

        w2f_hdr("LEN");
        fprintf(fp_output, "   \t0x%X\t\t%d bytes\t\tLength of MAC and Nonce\n\n", HAB_HDR_LEN(mac_sec), HAB_HDR_LEN(mac_sec));

        w2f_hdr("VER");
        fprintf(fp_output, "   \t0x%X\t\tHAB_MAJOR.HAB_MINOR\tHAB VERSION\n\n", mac_sec->version);

        fprintf(fp_output, "NONCE\tNONCE_LEN\tVALUE\n");
        fprintf(fp_output, "----------------------------------------------------------------------\n");
        fprintf(fp_output, "   \t0x%X\t\t", mac_sec->nonce_bytes);
        for (i = 0; i < mac_sec->nonce_bytes; i++)
                fprintf(fp_output, "%02X", mac_sec->nonce_mac[i]);
        fprintf(fp_output, "\n\n");

        fprintf(fp_output, "MAC\tMAC_LEN\t\tVALUE\n");
        fprintf(fp_output, "----------------------------------------------------------------------\n");
        fprintf(fp_output, "   \t0x%X\t\t", mac_sec->mac_bytes);
        for (i=0; i < mac_sec->mac_bytes ; i++)
                fprintf(fp_output, "%02X", mac_sec->nonce_mac[mac_sec->nonce_bytes + i]);
        fprintf(fp_output, "\n\n");

        mac_sec_len = HAB_HDR_LEN(mac_sec);
        free(mac_sec);

        return mac_sec_len;
}

/* @Function    : parse_sig_sec
 * @Description : This function parses the Signature Section in CSF
 *                and prints the parsed content
 *
 * @Inputs      : csf_hdr - Pointer to the start of CSF
 *                csf_len - Length of CSF
 *                offset  - Offset from beginning of CSF
 *                sig_num - Signature number
 *
 * @Outputs     : return length of signature
 *
 */
int parse_sig_sec(const uint8_t *csf_hdr, int csf_len, int offset, int *sig_num)
{
        assert(csf_hdr != NULL);

        validate(csf_len != 0, "csf length");

        csf_sec_sig_t *sig_sec_temp = (csf_sec_sig_t *)csf_hdr;

        int sig_sec_len;

        if (debug_log) {
                int i = 0;
                fprintf(fp_debug, "Parsing following values\n");
                for (i=0; i < HAB_HDR_LEN(sig_sec_temp) ; i++)
                        fprintf(fp_debug, "0x%02X ", csf_hdr[i]);
                fprintf(fp_debug, "\n");
        }

        validate(sig_sec_temp->tag == HAB_TAG_SIG, "tag");
        validate((sig_sec_temp->version == HAB_VER_40 || \
                  sig_sec_temp->version == HAB_VER_41 || \
                  sig_sec_temp->version == HAB_VER_42 ), "hab version");
        validate((offset + HAB_HDR_LEN(sig_sec_temp)) <= csf_len, "length OOB");

        csf_sec_sig_t *sig_sec = malloc(HAB_HDR_LEN(sig_sec_temp));
        if (memcpy(sig_sec, csf_hdr, HAB_HDR_LEN(sig_sec_temp)) == NULL) {
                puts("Error: Memcopy to copy mac section contents failed.\n");
                free(sig_sec);
                return FAIL;
        }

        fprintf(fp_output, "\n\n");
        w2f_hdr("TAG");
        fprintf(fp_output, "   \t0x%X\t\tHAB_TAG_SIG\t\tSignature\n\n", sig_sec->tag);

        w2f_hdr("LEN");
        fprintf(fp_output, "   \t0x%X\t\t%d bytes\t\tLength of Signature\n\n", HAB_HDR_LEN(sig_sec), HAB_HDR_LEN(sig_sec));

        w2f_hdr("VER");
        fprintf(fp_output, "   \t0x%X\t\tHAB_MAJOR.HAB_MINOR\tHAB VERSION\n\n", sig_sec->version);

        w2f_hdr("SIG");
        fprintf(fp_output, "   \t0x%X\t\tSignature Offset\tRelative to start of CSF\n\n", offset + HAB_HDR_SIZE);

        if (getAbs(sig_sec))
                sig_sec_len = HAB_HDR_LEN(sig_sec) + (HAB_HDR_SIZE - getAbs(sig_sec));
        else
                sig_sec_len = HAB_HDR_LEN(sig_sec);

        /* Create Signature files */
        char sig_fn[16];
        snprintf(sig_fn, sizeof(sig_fn), "output/sig%d.bin", *sig_num);
        FILE *fp_sig = fopen(sig_fn, "w");
        if (fp_sig) {
                fwrite(sig_sec->sig, (HAB_HDR_LEN(sig_sec) - HAB_HDR_SIZE),  1, fp_sig);
                puts("Signature file created\n");
                (*sig_num)++;
        } else
                puts("Error: Unable to create Signature file\n");

        fclose(fp_sig);

        free(sig_sec);

        return sig_sec_len;
}

/* @Function    : parse_cert_sec
 * @Description : This function parses the Certificate Section in CSF
 *                and prints the parsed content
 *
 * @Inputs      : csf_hdr - Pointer to the start of CSF
 *                csf_len - Length of CSF
 *                offset  - Offset from beginning of CSF
 *
 * @Outputs     : return length of certificate
 *
 */
int parse_cert_sec(const uint8_t *csf_hdr, int csf_len, int offset)
{
        assert(csf_hdr != NULL);

        validate(csf_len != 0, "csf length");

        csf_sec_cert_t *cert_sec = (csf_sec_cert_t *)csf_hdr;

        if (debug_log) {
                int i = 0;
                fprintf(fp_debug, "Parsing following values\n");
                for (i=0; i < HAB_HDR_LEN(cert_sec) ; i++)
                        fprintf(fp_debug, "0x%02X ", csf_hdr[i]);
                fprintf(fp_debug, "\n");
        }

        validate(cert_sec->tag == HAB_TAG_CRT, "tag");
        validate((cert_sec->version == HAB_VER_40 || \
                  cert_sec->version == HAB_VER_41 || \
                  cert_sec->version == HAB_VER_42), "hab version");
        validate((offset + HAB_HDR_LEN(cert_sec)) <= csf_len, "length OOB");

        fprintf(fp_output, "\n\n");
        w2f_hdr("TAG");
        fprintf(fp_output, "   \t0x%X\t\tHAB_TAG_CSF\t\tCertificate\n\n", cert_sec->tag);

        w2f_hdr("LEN");
        fprintf(fp_output, "   \t0x%X\t\t%d bytes\t\tLength of Certificate\n\n", HAB_HDR_LEN(cert_sec), HAB_HDR_LEN(cert_sec));

        w2f_hdr("VER");
        fprintf(fp_output, "   \t0x%X\t\tHAB_MAJOR.HAB_MINOR\tHAB VERSION\n\n", cert_sec->version);

        w2f_hdr("CERT");
        fprintf(fp_output, "   \t0x%X\t\tCertificate Offset\tRelative to start of CSF\n\n", (offset + HAB_HDR_SIZE));

        if (getAbs(cert_sec))
                return HAB_HDR_LEN(cert_sec) + (HAB_HDR_SIZE - getAbs(cert_sec));
        else
                return HAB_HDR_LEN(cert_sec);
}

/* @Function    : parse_set_cmd
 * @Description : This function parses the Set command in CSF
 *                and prints the parsed content
 *
 * @Inputs      : csf_hdr - Pointer to the start of CSF
 *                csf_len - Length of CSF
 *                offset  - Offset from beginning of CSF
 *
 * @Outputs     : return length of Set command
 *
 */

int parse_set_cmd(const uint8_t *csf_hdr, int csf_len, int offset)
{
        assert(csf_hdr != NULL);

        validate(csf_len != 0, "csf length");

        char *def = NULL;
        char *des = NULL;
        csf_cmd_set_t *set_cmd = (csf_cmd_set_t *)csf_hdr;

        if (debug_log) {
                int i = 0;
                fprintf(fp_debug, "Parsing following values\n");
                for (i=0; i < HAB_HDR_LEN(set_cmd) ; i++)
                        fprintf(fp_debug, "0x%02X ", csf_hdr[i]);
                fprintf(fp_debug, "\n");
        }

        validate(set_cmd->cmd == HAB_CMD_SET, "tag");
        validate(set_cmd->cfg_itm == HAB_VAR_CFG_ITM_ENG, "config item");
        validate(set_cmd->alg == HAB_ALG_SHA1 || \
                 set_cmd->alg == HAB_ALG_SHA256 || \
                 set_cmd->alg == HAB_ALG_SHA512, "algorithm");
        validate(set_cmd->engine == HAB_ENG_ANY || \
                 set_cmd->engine == HAB_ENG_CAAM || \
                 set_cmd->engine == HAB_ENG_DCP || \
                 set_cmd->engine == HAB_ENG_SAHARA || \
                 set_cmd->engine == HAB_ENG_RTIC || \
                 set_cmd->engine == HAB_ENG_SW, "engine");
        validate((offset + HAB_HDR_LEN(set_cmd)) <= csf_len, "length OOB");
        validate(!(set_cmd->eng_cfg & (uint8_t)~HAB_ENG_CONF_MASK), "engine configuration");

        fprintf(fp_output, "\n\n");
        w2f_hdr("TAG");
        fprintf(fp_output, "   \t0x%X\t\tHAB_CMD_SET\t\tSet Command\n\n",  set_cmd->cmd);

        w2f_hdr("LEN");
        fprintf(fp_output, "   \t0x%X\t\t%d bytes\t\t\tLength of Set Command\n\n", HAB_HDR_LEN(set_cmd), HAB_HDR_LEN(set_cmd));

        w2f_hdr("CFG_ITM");
        if (set_cmd->cfg_itm == HAB_VAR_CFG_ITM_ENG)
                { def = "HAB_VAR_CFG_ITM_ENG"; des = "Set Engine command"; }
        else { puts("Error: Invalid configuration item.\n"); return FAIL; }

        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", set_cmd->cfg_itm, def, des);

        w2f_hdr("ALG");
        if (set_cmd->alg == HAB_ALG_SHA1)
                { def = "HAB_ALG_SHA1";
                  des = "SHA1 Algorithm"; }
        else if (set_cmd->alg == HAB_ALG_SHA256)
                { def = "HAB_ALG_SHA256";
                  des = "SHA256 Algorithm"; }
        else if (set_cmd->alg == HAB_ALG_SHA512)
                { def = "HAB_ALG_SHA512";
                  des = "SHA512 Algorithm"; }
        else { puts("Error: Invalid Algorithm.\n"); return FAIL; }
        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", set_cmd->alg, def, des);

        w2f_hdr("ENG");
        if (set_cmd->engine == HAB_ENG_ANY)
                { def = "HAB_ENG_ANY";
                  des = "Any – HAB will chose the most appropriate engine"; }
        else if (set_cmd->engine == HAB_ENG_CAAM)
                { def = "HAB_ENG_CAAM"; des = "CAAM"; }
        else if (set_cmd->engine == HAB_ENG_DCP)
                { def = "HAB_ENG_DCP"; des = "DCP"; }
        else if (set_cmd->engine == HAB_ENG_SAHARA)
                { def = "HAB_ENG_SAHARA"; des = "SAHARA"; }
        else if (set_cmd->engine == HAB_ENG_RTIC)
                { def = "HAB_ENG_RTIC"; des = "RTIC"; }
        else if (set_cmd->engine == HAB_ENG_SW)
                { def = "HAB_ENG_SW"; des = "Software Engine"; }
        else { puts("Error: Invalid Engine.\n"); return FAIL; }

        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", set_cmd->engine, def, des);

        w2f_hdr("ENG_CFG");
        fprintf(fp_output, "   \t0x%X\t\tBITWISE OR   \t\tBitwise OR of Engine confs as below\n\n", set_cmd->eng_cfg);

        if (set_cmd->engine == HAB_ENG_ANY && set_cmd->eng_cfg == HAB_ANY_CONF_DEFAULT) {
                def = "HAB_ANY_CONF_DEFAULT"; des = "Engine Configuration ANY Default";
                fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", HAB_ANY_CONF_DEFAULT, def, des);
        } else if (set_cmd->engine == HAB_ENG_CAAM) {
                if (set_cmd->eng_cfg == HAB_CAAM_DEFAULT) {
                        def = "HAB_CAAM_DEFAULT";
                        des = "Engine Configuration CAAM Default";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_DEFAULT, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_CAAM_IN_SWAP8)) {
                        def = "HAB_CAAM_IN_SWAP8";
                        des = "Engine Configuration CAAM IN SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_IN_SWAP8, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_CAAM_IN_SWAP16)) {
                        def = "HAB_CAAM_IN_SWAP16";
                        des = "Engine Configuration CAAM IN SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_IN_SWAP16, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_CAAM_OUT_SWAP8)) {
                        def = "HAB_CAAM_OUT_SWAP8";
                        des = "Engine Configuration CAAM OUT SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_OUT_SWAP8, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_CAAM_OUT_SWAP16)) {
                        def = "HAB_CAAM_OUT_SWAP16";
                        des = "Engine Configuration CAAM OUT SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_OUT_SWAP16,def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_CAAM_DSC_SWAP8)) {
                        def = "HAB_CAAM_DSC_SWAP8";
                        des = "Engine Configuration CAAM DSC SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_DSC_SWAP8, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_CAAM_DSC_SWAP16)) {
                        def = "HAB_CAAM_DSC_SWAP16";
                        des = "Engine Configuration CAAM DSC SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_DSC_SWAP16,def, des);
                }
        }
        else if (set_cmd->engine == HAB_ENG_DCP) {
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_DCP_DEFAULT)) {
                        def = "HAB_DCP_DEFAULT";
                        des = "Engine Configuration DCP default";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", HAB_DCP_DEFAULT, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_DCP_IN_SWAP8)) {
                        def = "HAB_DCP_IN_SWAP8";
                        des = "Engine Configuration DCP IN SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_IN_SWAP8, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_DCP_IN_SWAP32)) {
                        def = "HAB_DCP_IN_SWAP32";
                        des = "Engine Configuration DCP IN SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_IN_SWAP32, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_DCP_OUT_SWAP8)) {
                        def = "HAB_DCP_OUT_SWAP8";
                        des = "Engine Configuration DCP OUT SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_OUT_SWAP8, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_DCP_OUT_SWAP32)) {
                        def = "HAB_DCP_OUT_SWAP32";
                        des = "Engine Configuration DCP OUT SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_OUT_SWAP32, def, des);
                }
        }
        else if (set_cmd->engine == HAB_ENG_SAHARA) {
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_SAHARA_DEFAULT)) {
                        def = "HAB_SAHARA_DEFAULT";
                        des = "Engine Configuration SAHARA default";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_DEFAULT,def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_SAHARA_IN_SWAP8)) {
                        def = "HAB_SAHARA_IN_SWAP8";
                        des = "Engine Configuration SAHARA IN SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_IN_SWAP8,def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_SAHARA_IN_SWAP16)) {
                        def = "HAB_SAHARA_IN_SWAP16";
                        des = "Engine Configuration SAHARA IN SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_IN_SWAP16,def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_SAHARA_DSC_BE8_16)) {
                        def = "HAB_SAHARA_DSC_BE8_16";
                        des = "Engine Configuration SAHARA DSC BE8 16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_DSC_BE8_16,def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_SAHARA_DSC_BE8_32)) {
                        def = "HAB_SAHARA_DSC_BE8_32";
                        des = "Engine Configuration SAHARA DSC BE8 32";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_DSC_BE8_32, def, des);
                }
        }
        else if (set_cmd->engine == HAB_ENG_RTIC) {
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_RTIC_DEFAULT)) {
                        def = "HAB_RTIC_DEFAULT";
                        des = "Engine Configuration RTIC default";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_RTIC_DEFAULT, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_RTIC_IN_SWAP8)) {
                        def = "HAB_RTIC_IN_SWAP8";
                        des = "Engine Configuration RTIC IN SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_RTIC_IN_SWAP8, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_RTIC_IN_SWAP16)) {
                        def = "HAB_RTIC_IN_SWAP16";
                        des = "Engine Configuration RTIC IN SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_RTIC_IN_SWAP16,def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_RTIC_OUT_SWAP8)) {
                        def = "HAB_RTIC_OUT_SWAP8";
                        des = "Engine Configuration RTIC OUT SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_RTIC_OUT_SWAP8, def, des);
                }
                if (CHECK_BIT(set_cmd->eng_cfg, HAB_RTIC_KEEP)) {
                        def = "HAB_RTIC_KEEP";
                        des = "Engine Configuration RTIC KEEP";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_RTIC_KEEP, def, des);
                }
        }
        else if (set_cmd->engine == HAB_ENG_SW && \
                set_cmd->eng_cfg == HAB_SW_CONF_DEFAULT) {
                def = "HAB_SW_CONF_DEFAULT";
                des = "Engine Configuration SW Default";
                fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SW_CONF_DEFAULT, def, des);
        }
        else { puts("Error: Invalid Engine configuration found\n"); return FAIL; }

        return HAB_HDR_LEN(set_cmd);
}

/* @Function    : parse_unlock_cmd
 * @Description : This function parses the Unlock command in CSF
 *                and prints the parsed content
 *
 * @Inputs      : csf_hdr - Pointer to the start of CSF
 *                csf_len - Length of CSF
 *                offset  - Offset from beginning of CSF
 *
 * @Outputs     : return length of Unlock command
 *
 */

int parse_unlock_cmd(const uint8_t *csf_hdr, int csf_len, int offset)
{
        assert(csf_hdr != NULL);

        validate(csf_len != 0, "csf length");

        char *def = NULL;
        char *des = NULL;
        uint32_t ulck_features;
        csf_cmd_unlock_t *unlock_cmd = (csf_cmd_unlock_t *)csf_hdr;

        if (debug_log) {
                int i = 0;
                fprintf(fp_debug, "Parsing following values\n");
                for (i=0; i < HAB_HDR_LEN(unlock_cmd) ; i++)
                        fprintf(fp_debug, "0x%02X ", csf_hdr[i]);
                fprintf(fp_debug, "\n");
        }

        validate((unlock_cmd->cmd == HAB_CMD_UNLK ||\
                  unlock_cmd->cmd == HAB_CMD_INIT), "tag");
        validate(unlock_cmd->engine == HAB_ENG_CAAM || \
                 unlock_cmd->engine == HAB_ENG_SNVS || \
                 unlock_cmd->engine == HAB_ENG_OCOTP, "engine");
        validate((offset + HAB_HDR_LEN(unlock_cmd)) <= csf_len, "length OOB");
        ulck_features = from_be32(unlock_cmd->features);
        validate(!(ulck_features & (uint32_t)~HAB_UNLK_FEAT_MASK), "unlock features");

        fprintf(fp_output, "\n\n");
        w2f_hdr("TAG");
        if (unlock_cmd->cmd == HAB_CMD_UNLK)
                fprintf(fp_output, "   \t0x%X\t\tHAB_CMD_UNLK\t\tUnlock Command\n\n", unlock_cmd->cmd);
        else
                fprintf(fp_output, "   \t0x%X\t\tHAB_CMD_INIT\t\tInit Command\n\n", unlock_cmd->cmd);

        w2f_hdr("LEN");
        if (unlock_cmd->cmd == HAB_CMD_UNLK)
                fprintf(fp_output, "   \t0x%X\t\t%d bytes  \t\tLength of Unlock Command\n\n", HAB_HDR_LEN(unlock_cmd), HAB_HDR_LEN(unlock_cmd));
        else
                fprintf(fp_output, "   \t0x%X\t\t%d bytes  \t\tLength of Init Command\n\n", HAB_HDR_LEN(unlock_cmd), HAB_HDR_LEN(unlock_cmd));

        w2f_hdr("ENG");
        if (unlock_cmd->engine == HAB_ENG_CAAM)
                { def = "HAB_ENG_CAAM"; des = "CAAM"; }
        else if (unlock_cmd->engine == HAB_ENG_SNVS)
                { def = "HAB_ENG_SNVS"; des = "Secure Non-Volatile Storage"; }
        else if (unlock_cmd->engine == HAB_ENG_OCOTP)
                { def = "HAB_ENG_OCOTP"; des = "On Chip OTP memory"; }
        else { puts("Error: Invalid Engine.\n"); return FAIL; }

        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", unlock_cmd->engine, def, des);

        w2f_hdr("FEATURE");
        fprintf(fp_output, "   \t0x%X\t\tBITWISE OR \t\tBitwise OR of features below \n\n", (ulck_features));

        if (unlock_cmd->engine == HAB_ENG_CAAM) {
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_CAAM_MID)) {
                        def = "UNLOCK_CAAM_MID"; des = "Unlock CAAM MID feature enabled";
                        fprintf(fp_output, "   \t0x%X\t\t%s \t%s\n\n", HAB_CMD_UNLOCK_CAAM_MID, def, des);
                }
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_CAAM_RNG)) {
                        if (unlock_cmd->cmd == HAB_CMD_UNLK) {
                                def = "UNLOCK_CAAM_RNG"; des = "Unlock CAAM RNG feature enabled";
                        } else {
                                def = "INIT_CAAM_RNG"; des = "Init CAAM RNG feature enabled";
                        }
                        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", HAB_CMD_UNLOCK_CAAM_RNG, def, des);
                }
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_CAAM_MFG)) {
                        def = "UNLOCK_CAAM_MFG"; des = "Unlock CAAM MFG feature enabled";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", HAB_CMD_UNLOCK_CAAM_MFG, def, des);
                }
        } else if (unlock_cmd->engine == HAB_ENG_SNVS) {
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_SNVS_LP_SWR)) {
                        def = "UNLOCK_SNVS_LP_SWR";
                        des = "Unlock SNVS LP SWR feature enabled";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CMD_UNLOCK_SNVS_LP_SWR, def, des);
                }
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_SNVS_ZMK_WRITE)) {
                        def = "UNLOCK_SNVS_ZMK_WRITE";
                        des = "Unlock SNVS ZMK WRITE feature enabled";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CMD_UNLOCK_SNVS_ZMK_WRITE, def, des);
                }
        } else if (unlock_cmd->engine == HAB_ENG_OCOTP) {
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_OCOTP_FLD_RTN)) {
                        def = "UNLOCK_OCOTP_FLD_RTN";
                        des = "Unlock OCOTP Field Return feature enabled";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CMD_UNLOCK_OCOTP_FLD_RTN, def, des);
                }
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_OCOTP_SRK_RVK)) {
                        def = "UNLOCK_OCOTP_SRK_RVK";
                        des = "Unlock OCOTP SRK Revoke feature enabled";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CMD_UNLOCK_OCOTP_SRK_RVK, def, des);
                }
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_OCOTP_SCS)) {
                        def = "UNLOCK_OCOTP_SCS";
                        des = "Unlock OCOTP SCS feature enabled";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CMD_UNLOCK_OCOTP_SCS, def, des);
                }
                if (CHECK_BIT(ulck_features, HAB_CMD_UNLOCK_OCOTP_JTAG)) {
                        def = "UNLOCK_OCOTP_JTAG";
                        des = "Unlock OCOTP JTAG feature enabled";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CMD_UNLOCK_OCOTP_JTAG, def, des);
                }
        } else { puts("Error: Invalid Engine configuration found\n"); return FAIL; }

        if (unlock_cmd->cmd == HAB_CMD_UNLK && \
            unlock_cmd->engine == HAB_ENG_OCOTP && \
            HAB_HDR_LEN(unlock_cmd) > MIN_UNLK_CMD_LEN) {
                fprintf(fp_output, "UID\tVALUE\t\t\t\t\tDESCRIPTION\n");
                fprintf(fp_output, "----------------------------------------------------------------------\n");
                fprintf(fp_output, "   \t0x%08X%08X\t\t\tUnique Identifier\n\n", \
                                        (uint32_t)from_be32(unlock_cmd->uid), \
                                        (uint32_t)from_be32((unlock_cmd->uid >> 32)));
        }

        return HAB_HDR_LEN(unlock_cmd);
}

/* @Function    : parse_aut_dat_cmd
 * @Description : This function parses the Authenticate Data command in CSF 
 *                and prints the parsed content
 *
 * @Inputs      : csf_hdr - Pointer to the start of CSF
 *                csf_len - Length of CSF
 *                offset  - Offset from beginning of CSF
 *
 * @Outputs     : return Success or Fail
 *
 */

int parse_aut_dat_cmd(const uint8_t *csf_hdr, int csf_len, int offset)
{

        assert(csf_hdr != NULL);

        validate(csf_len != 0, "csf length");

        char *def = NULL;
        char *des = NULL;
        csf_cmd_aut_dat_t *aut_dat_cmd_temp = (csf_cmd_aut_dat_t *)csf_hdr;
        int nregions = 0;
        int aut_dat_len;

        if (HAB_HDR_LEN(aut_dat_cmd_temp) > MIN_AUT_DAT_CMD_LEN) {
                nregions = (HAB_HDR_LEN(aut_dat_cmd_temp) - sizeof(csf_cmd_aut_dat_t)) / sizeof(region_t);

                if (aut_dat_cmd_temp->engine == HAB_ENG_CAAM) {
                        validate(nregions < HAB_CAAM_BLOCK_MAX && nregions > 0, "blocks");
                } else if (aut_dat_cmd_temp->engine == HAB_ENG_DCP) {
                        validate(nregions < HAB_DCP_BLOCK_MAX && nregions > 0, "blocks");
                } else if (aut_dat_cmd_temp->engine == HAB_ENG_SAHARA) {
                        validate(nregions < HAB_SAHARA_BLOCK_MAX && nregions > 0, "blocks");
                }
        }

        csf_cmd_aut_dat_t *aut_dat_cmd = malloc(sizeof(csf_cmd_aut_dat_t) + (nregions * sizeof(region_t)));

        if (memcpy(aut_dat_cmd, csf_hdr, HAB_HDR_LEN(aut_dat_cmd_temp)) == NULL) {
                puts("Error: Memcopy to copy aut dat cmd contents failed.\n");
                free(aut_dat_cmd);
                return FAIL;
        }

        if (debug_log) {
                int i = 0;
                fprintf(fp_debug, "Parsing following values\n");
                for (i=0; i < HAB_HDR_LEN(aut_dat_cmd) ; i++)
                        fprintf(fp_debug, "0x%02X ", csf_hdr[i]);
                fprintf(fp_debug, "\n");
        }

        validate(aut_dat_cmd->cmd == HAB_CMD_AUT_DAT, "tag");
        validate(aut_dat_cmd->flags == HAB_CMD_AUT_DAT_NO_FLAG || aut_dat_cmd->flags == HAB_CMD_AUT_DAT_ABS, "flags");
        validate((offset + HAB_HDR_LEN(aut_dat_cmd)) <= csf_len, "length OOB");
        /* Normal Authentication Verification Index = 1 for CSF
         * Normal Authentication Verification Index = 2 - 4 for IMG
         * Fast Authentication Verification Index : 0
         */
        validate(aut_dat_cmd->key >= 0 && aut_dat_cmd->key < 5 , "key");
        validate(aut_dat_cmd->sig_fmt == HAB_CMD_AUT_DAT_PCL_CMS || \
                 aut_dat_cmd->sig_fmt == HAB_CMD_AUT_DAT_PCL_AEAD, "signature format");
        validate(aut_dat_cmd->engine == HAB_ENG_ANY || \
                 aut_dat_cmd->engine == HAB_ENG_CAAM || \
                 aut_dat_cmd->engine == HAB_ENG_DCP || \
                 aut_dat_cmd->engine == HAB_ENG_SAHARA || \
                 aut_dat_cmd->engine == HAB_ENG_SW, "engine");
/* aut_dat_cmd->engine == HAB_ENG_SNVS || \
   aut_dat_cmd->engine == HAB_ENG_OCOTP || \ */
        validate(!(aut_dat_cmd->eng_cfg & (uint8_t)~HAB_ENG_CONF_MASK), "engine configuration");

        fprintf(fp_output, "\n\n");
        w2f_hdr("TAG");
        fprintf(fp_output, "   \t0x%X\t\tHAB_CMD_AUT_DAT\t\tAuthenticate Data Command\n\n", aut_dat_cmd->cmd);

        w2f_hdr("LEN");
        fprintf(fp_output, "   \t0x%X\t\t%d bytes\t\tLength of Authenticate Data Command\n\n", HAB_HDR_LEN(aut_dat_cmd), HAB_HDR_LEN(aut_dat_cmd));

        w2f_hdr("FLG");

        if (aut_dat_cmd->flags == HAB_CMD_AUT_DAT_NO_FLAG)
                { def = "HAB_CMD_AUT_DAT_NO_FLAG"; des = "No Flags set"; }
        else if (aut_dat_cmd->flags == HAB_CMD_AUT_DAT_ABS)
                { def = "HAB_CMD_AUT_DAT_ABS";
                  des = "Use absolute address for the key"; }
        else { puts("Error: Invalid Authenticate data flag.\n"); free(aut_dat_cmd); return FAIL; }

        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", aut_dat_cmd->flags, def, des);
    
        w2f_hdr("KEY");
        fprintf(fp_output, "   \t0x%X\t\tVerification Key Idx %d\tPublic Key Store Index\n\n", aut_dat_cmd->key, aut_dat_cmd->key);

        w2f_hdr("PCL");
        fprintf(fp_output, "   \t0x%X\t\tHAB_PCL_CMS\t\tCMS/PKCS#7 Signature Format\n\n", aut_dat_cmd->sig_fmt);
    
        w2f_hdr("ENG");
        if (aut_dat_cmd->engine == HAB_ENG_ANY)
                { def = "HAB_ENG_ANY";
                  des = "Any – HAB will chose the most appropriate engine"; }
        else if (aut_dat_cmd->engine == HAB_ENG_CAAM)
                { def = "HAB_ENG_CAAM"; des = "CAAM"; }
        else if (aut_dat_cmd->engine == HAB_ENG_DCP)
                { def = "HAB_ENG_DCP"; des = "DCP"; }
        else if (aut_dat_cmd->engine == HAB_ENG_SAHARA)
                { def = "HAB_ENG_SAHARA"; des = "SAHARA"; }
/*    else if (aut_dat_cmd->engine == HAB_ENG_SNVS) { def = "HAB_ENG_SNVS"; des = "Secure Non-Volatile Storage"; }
    else if (aut_dat_cmd->engine == HAB_ENG_OCOTP) { def = "HAB_ENG_OCOTP"; des = "On Chip OTP memory"; } */
        else if (aut_dat_cmd->engine == HAB_ENG_SW)
                { def = "HAB_ENG_SW"; des = "Software Engine"; }
        else { puts("Error: Invalid Engine.\n"); free(aut_dat_cmd); return FAIL; }

        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", aut_dat_cmd->engine, def, des);

        w2f_hdr("ENG_CFG");
        fprintf(fp_output, "   \t0x%X\t\tBITWISE OR   \t\tBitwise OR of Engine confs as below\n\n", aut_dat_cmd->eng_cfg);

        if (aut_dat_cmd->engine == HAB_ENG_ANY && aut_dat_cmd->eng_cfg == HAB_ANY_CONF_DEFAULT) {
                def = "HAB_ANY_CONF_DEFAULT"; des = "Engine Configuration ANY Default";
                fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_ANY_CONF_DEFAULT, def, des);
        } else if (aut_dat_cmd->engine == HAB_ENG_CAAM) {
                if (aut_dat_cmd->eng_cfg == HAB_CAAM_DEFAULT) {
                        def = "HAB_CAAM_DEFAULT";
                        des = "Engine Configuration CAAM Default";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_DEFAULT, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_CAAM_IN_SWAP8)) {
                        def = "HAB_CAAM_IN_SWAP8";
                        des = "Engine Configuration CAAM IN SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_IN_SWAP8, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_CAAM_IN_SWAP16)) {
                        def = "HAB_CAAM_IN_SWAP16";
                        des = "Engine Configuration CAAM IN SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_IN_SWAP16, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_CAAM_OUT_SWAP8)) {
                        def = "HAB_CAAM_OUT_SWAP8";
                        des = "Engine Configuration CAAM OUT SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_OUT_SWAP8, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_CAAM_OUT_SWAP16)) {
                        def = "HAB_CAAM_OUT_SWAP16";
                        des = "Engine Configuration CAAM OUT SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_OUT_SWAP16, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_CAAM_DSC_SWAP8)) {
                        def = "HAB_CAAM_DSC_SWAP8";
                        des = "Engine Configuration CAAM DSC SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_DSC_SWAP8, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_CAAM_DSC_SWAP16)) {
                        def = "HAB_CAAM_DSC_SWAP16";
                        des = "Engine Configuration CAAM DSC SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_CAAM_DSC_SWAP16, def, des);
                }
        }
        else if (aut_dat_cmd->engine == HAB_ENG_DCP) {
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_DCP_DEFAULT)) {
                        def = "HAB_DCP_DEFAULT";
                        des = "Engine Configuration DCP default";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_DEFAULT, def,  des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_DCP_IN_SWAP8)) {
                        def = "HAB_DCP_IN_SWAP8";
                        des = "Engine Configuration DCP IN SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_IN_SWAP8, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_DCP_IN_SWAP32)) {
                        def = "HAB_DCP_IN_SWAP32";
                        des = "Engine Configuration DCP IN SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_IN_SWAP32, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_DCP_OUT_SWAP8)) {
                        def = "HAB_DCP_OUT_SWAP8";
                        des = "Engine Configuration DCP OUT SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_OUT_SWAP8, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_DCP_OUT_SWAP32)) {
                        def = "HAB_DCP_OUT_SWAP32";
                        des = "Engine Configuration DCP OUT SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_DCP_OUT_SWAP32, def, des);
                }
        }
        else if (aut_dat_cmd->engine == HAB_ENG_SAHARA) {
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_SAHARA_DEFAULT)) {
                        def = "HAB_SAHARA_DEFAULT";
                        des = "Engine Configuration SAHARA default";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_DEFAULT,    def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_SAHARA_IN_SWAP8)) {
                        def = "HAB_SAHARA_IN_SWAP8";
                        des = "Engine Configuration SAHARA IN SWAP8";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_IN_SWAP8, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_SAHARA_IN_SWAP16)) {
                        def = "HAB_SAHARA_IN_SWAP16";
                        des = "Engine Configuration SAHARA IN SWAP16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_IN_SWAP16, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_SAHARA_DSC_BE8_16)) {
                        def = "HAB_SAHARA_DSC_BE8_16";
                        des = "Engine Configuration SAHARA DSC BE8 16";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_DSC_BE8_16, def, des);
                }
                if (CHECK_BIT(aut_dat_cmd->eng_cfg, HAB_SAHARA_DSC_BE8_32)) {
                        def = "HAB_SAHARA_DSC_BE8_32";
                        des = "Engine Configuration SAHARA DSC BE8 32";
                        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SAHARA_DSC_BE8_32, def, des);
                }
        }
        else if (aut_dat_cmd->engine == HAB_ENG_SW && \
                aut_dat_cmd->eng_cfg == HAB_SW_CONF_DEFAULT) {
                def = "HAB_SW_CONF_DEFAULT";
                des = "Engine Configuration SW Default";
                fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", HAB_SW_CONF_DEFAULT, def, des);
        }
        else { puts("Error: Invalid Engine configuration found\n"); free(aut_dat_cmd); return FAIL; }

        w2f_hdr("SIG_LOC");
        fprintf(fp_output, "   \t0x%X\t\tAuthentication Data\tRelative to start of CSF\n\n", (uint32_t)from_be32(aut_dat_cmd->sig_loc));

        if (HAB_HDR_LEN(aut_dat_cmd) > MIN_AUT_DAT_CMD_LEN && nregions > 0 && nregions < HAB_CAAM_BLOCK_MAX) {
                int j;
                for (j = 0; j < nregions; j++) {
                        if (debug_log) {
                                fprintf(fp_debug, "Region %d: address: 0x%X, size: 0x%X\n", j,
                                from_be32(aut_dat_cmd->region[j].address), from_be32(aut_dat_cmd->region[j].size));
                        }
                        w2f_hdr("BLK_SRT");
                        fprintf(fp_output, "   \t0x%X\tAddress of Region %d\tAddress of Region %d \
to verify\n\n", (uint32_t)from_be32(aut_dat_cmd->region[j].address), j, j);
                        w2f_hdr("BLK_LEN");
                        fprintf(fp_output, "   \t0x%X\t\tSize of Region %d\tSize of Region %d \
to verify\n\n", (uint32_t)from_be32(aut_dat_cmd->region[j].size), j, j);
                }
        }

        aut_dat_len = HAB_HDR_LEN(aut_dat_cmd);
        free(aut_dat_cmd);
        return aut_dat_len;
}

/* @Function    : parse_ins_key_cmd
 * @Description : This function parses the Insert key command in CSF 
 *                and prints the parsed content
 *
 * @Inputs      : csf_hdr  - Pointer to the start of CSF
 *                csf_len  - Length of CSF
 *                offset   - Offset from beginning of CSF
 8                cert_num - Certificate Number
 *
 * @Outputs     : return Success or Fail
 *
 */
int parse_ins_key_cmd(const uint8_t *csf_hdr, int csf_len, int offset, int *cert_num)
{
        assert(csf_hdr != NULL);

        validate(csf_len != 0, "csf length");

        char *def = NULL;
        char *des = NULL;
        csf_cmd_ins_key_t *ins_key_cmd = (csf_cmd_ins_key_t *)csf_hdr;

        if (debug_log) {
                int i = 0;
                fprintf(fp_debug, "Parsing following values\n");
                for (i=0; i < HAB_HDR_LEN(ins_key_cmd) ; i++)
                        fprintf(fp_debug, "0x%02X ", csf_hdr[i]);
                fprintf(fp_debug, "\n");
        }

        validate(ins_key_cmd->cmd == HAB_CMD_INS_KEY, "tag");
        validate(ins_key_cmd->flags == HAB_CMD_INS_KEY_NO_FLAG || \
                 ins_key_cmd->flags == HAB_CMD_INS_KEY_ABS || \
                 ins_key_cmd->flags == HAB_CMD_INS_KEY_CSF, "flags");
        validate((offset + HAB_HDR_LEN(ins_key_cmd)) <= csf_len, "length OOB");
        validate(ins_key_cmd->cert_fmt == HAB_PCL_SRK || \
                 ins_key_cmd->cert_fmt == HAB_PCL_X509 || \
                 ins_key_cmd->cert_fmt == HAB_PCL_BLOB, "cert format");
        validate(ins_key_cmd->hash_alg == HAB_ALG_NO_ALG || \
                 ins_key_cmd->hash_alg == HAB_ALG_SHA256, "hash algorithm");

        if (ins_key_cmd->cert_fmt == HAB_PCL_SRK) {
                /* Key Index of SRK1 - 4 */
                validate(ins_key_cmd->src_index >= 0 && ins_key_cmd->src_index < 4, "source index");
        } else if (ins_key_cmd->cert_fmt == HAB_PCL_BLOB) {
                /* Master KEK index */
                validate(ins_key_cmd->src_index >= 0 && ins_key_cmd->src_index < 4, "Master KEK index");
        } else {
                /* Verification Index */
                validate(ins_key_cmd->src_index == 0 || \
                        (ins_key_cmd->src_index > 1 && \
                         ins_key_cmd->src_index < 6 ), "verification index");
        }

        if (ins_key_cmd->cert_fmt == HAB_PCL_SRK) {
                validate(ins_key_cmd->tgt_index == 0, "target index");
        } else if (ins_key_cmd->cert_fmt == HAB_PCL_BLOB) {
                validate(ins_key_cmd->tgt_index >= 0 && ins_key_cmd->tgt_index < 4, "target index");
        } else {
                validate(ins_key_cmd->tgt_index > 0 && \
                         ins_key_cmd->tgt_index < 6 , "target index");
        }

        fprintf(fp_output, "\n\n");
        w2f_hdr("TAG");
        fprintf(fp_output, "   \t0x%X\t\tHAB_CMD_INS_KEY\t\tInstall Key Command\n\n", ins_key_cmd->cmd);

        w2f_hdr("LEN");
        fprintf(fp_output, "   \t0x%X\t\t%d bytes\t\tLength of Insert Key Command\n\n", HAB_HDR_LEN(ins_key_cmd), HAB_HDR_LEN(ins_key_cmd));

        w2f_hdr("FLG");
        if (ins_key_cmd->flags == HAB_CMD_INS_KEY_NO_FLAG)
                { def = "HAB_CMD_INS_KEY_NO_FLAG";
                  des = "No Flags set"; }
        else if (ins_key_cmd->flags == HAB_CMD_INS_KEY_ABS)
                { def = "HAB_CMD_INS_KEY_ABS";
                  des = "Use absolute address for the key"; }
        else if (ins_key_cmd->flags == HAB_CMD_INS_KEY_CSF)
                { def = "HAB_CMD_INS_KEY_CSF";
                  des = "Install CSF Key"; }
        else { puts("Error: Invalid Insert Key Flag.\n"); return FAIL; }

        fprintf(fp_output, "   \t0x%X\t\t%s\t%s\n\n", ins_key_cmd->flags, def, des);

        w2f_hdr("PCL");

        if (ins_key_cmd->cert_fmt == HAB_PCL_SRK) {
                def = "HAB_PCL_SRK";
                des = "SRK Format";
        } else if (ins_key_cmd->cert_fmt == HAB_PCL_X509) {
                def = "HAB_PCL_X509";
                des = "X.509v3 Cert Format";
        } else if (ins_key_cmd->cert_fmt == HAB_PCL_BLOB) {
                def = "HAB_PCL_BLOB";
                des = "SHW-specific wrapped key format";
        } else { puts("Error: Invalid Certificate format.\n"); return FAIL; }

        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", ins_key_cmd->cert_fmt, def, des);
        w2f_hdr("ALG");

        if (ins_key_cmd->hash_alg == HAB_ALG_NO_ALG)
                { def = "HAB_ALG_NO_ALG";
                  des = "No Hash Alg."; }
        else if (ins_key_cmd->hash_alg == HAB_ALG_SHA256)
                { def = "HAB_ALG_SHA256";
                  des = "SHA-256 Alg."; }
        else { puts("Error: Invalid hash algorithm.\n"); return FAIL; }

        fprintf(fp_output, "   \t0x%X\t\t%s\t\t%s\n\n", ins_key_cmd->hash_alg, def, des);

        if (ins_key_cmd->cert_fmt == HAB_PCL_SRK) {
                w2f_hdr("SRC");
                fprintf(fp_output, "   \t0x%X\t\tSRK Index %d\t\tSource Key Index of SRK\n\n", ins_key_cmd->src_index, ins_key_cmd->src_index);
        } else if (ins_key_cmd->cert_fmt == HAB_PCL_X509) {
                w2f_hdr("VRF");
                fprintf(fp_output, "   \t0x%X\t\tVerification Index %d\tSRK Verification Key Index\n\n", ins_key_cmd->src_index, ins_key_cmd->src_index);
        } else if (ins_key_cmd->cert_fmt == HAB_PCL_BLOB) {
                w2f_hdr("VRF");
                switch (ins_key_cmd->src_index) {
                case 0:
                case 1:
                        fprintf(fp_output, "   \t0x%X\t\tMaster KEK Index %d\tOTPMK:Master Key\n\n", ins_key_cmd->src_index, ins_key_cmd->src_index);
                        break;
                case 2:
                        fprintf(fp_output, "   \t0x%X\t\tMaster KEK Index %d\tOTPMK:Master Key\n\n", ins_key_cmd->src_index, ins_key_cmd->src_index);
                        break;
                case 3:
                        fprintf(fp_output, "   \t0x%X\t\tMaster KEK Index %d\tOTPMK:Master Key\n\n", ins_key_cmd->src_index, ins_key_cmd->src_index);
                        break;
                default:
                        puts("Error: Invalid Master KEK Index.\n");
                        return FAIL;
                }
        } else { puts("Error: Invalid Certificate format.\n"); return FAIL; }


        w2f_hdr("TGT");
        if (ins_key_cmd->cert_fmt == HAB_PCL_BLOB)
                fprintf(fp_output, "   \t0x%X\t\tKey Index %d\t\tSecret Key Store Index\n\n", ins_key_cmd->tgt_index, ins_key_cmd->tgt_index);
        else
                fprintf(fp_output, "   \t0x%X\t\tKey Index %d\t\tPublic Key Store Index\n\n", ins_key_cmd->tgt_index, ins_key_cmd->tgt_index);

        if (ins_key_cmd->cert_fmt == HAB_PCL_SRK)
                def = "Start of SRK Table";
        else if (ins_key_cmd->cert_fmt == HAB_PCL_X509)
                def = "Certificate Data";
        else if (ins_key_cmd->cert_fmt == HAB_PCL_BLOB)
                def = "Blob Address";
        else {  puts("Error: Invalid Certificate format.\n"); return FAIL; }

        w2f_hdr("KEY_DAT");

        if (ins_key_cmd->cert_fmt == HAB_PCL_BLOB)
                fprintf(fp_output, "   \t0x%X\t%s\t\tAbsolute memory address of blob\n\n", (uint32_t)from_be32(ins_key_cmd->key_loc), def);
        else
                fprintf(fp_output, "   \t0x%X\t\t%s\tRelative to start of CSF\n\n", (uint32_t)from_be32(ins_key_cmd->key_loc), def);

        if (ins_key_cmd->cert_fmt == HAB_PCL_SRK) {
                /* Create SRK Table file out of Image file */
                FILE *fp_srkTable = fopen("output/SRKTable.bin", "w");
                if (fp_srkTable) {
                        int srktable_offset = from_be32(ins_key_cmd->key_loc) - offset;
                        csf_sec_cert_t *cert_sec = (csf_sec_cert_t *)&csf_hdr[srktable_offset];
                        fwrite(&csf_hdr[srktable_offset], HAB_HDR_LEN(cert_sec), 1, fp_srkTable);
                        puts("SRK Table file created\n");
                } else
                        puts("Error: Unable to create SRK Table file\n");

                fclose(fp_srkTable);
        } else if (ins_key_cmd->cert_fmt == HAB_PCL_X509) {
                char cert_fn[17];
                snprintf(cert_fn, sizeof(cert_fn), "output/cert%d.der", *cert_num);
                FILE *fp_cert = fopen(cert_fn, "w");
                if (fp_cert) {
                        int cert_offset = from_be32(ins_key_cmd->key_loc) - offset;
                        csf_sec_cert_t *cert_sec = (csf_sec_cert_t *)&csf_hdr[cert_offset];
                        fwrite(&csf_hdr[cert_offset + HAB_HDR_SIZE], (HAB_HDR_LEN(cert_sec) - HAB_HDR_SIZE), 1, fp_cert);
                        puts("Certificate file created\n");
                        (*cert_num)++;
                } else
                        puts("Error: Unable to create Certificate file\n");

                fclose(fp_cert);
        }

        return HAB_HDR_LEN(ins_key_cmd);
}

/* @Function    : parse_csf_hdr
 * @Description : This function parses the CSF header and prints
 *                the parsed content
 *
 * @Inputs      : csf_hdr - Pointer to the start of CSF
 *                csf_len - Length of CSF
 *                offset  - Offset from beginning of CSF
 *
 * @outputs     : return Success or Fail
 *
 */

int parse_csf_hdr(const uint8_t *csf_hdr, int csf_len, int offset)
{

        assert(csf_hdr != NULL);

        validate(csf_len != 0, "csf length");

        csf_hdr_t *csf_header = (csf_hdr_t *)csf_hdr;

        if (debug_log) {
                int i = 0;
                fprintf(fp_debug, "Parsing following values\n");
                for (i=0; i < sizeof(csf_hdr_t) ; i++)
                        fprintf(fp_debug, "0x%02X ", csf_hdr[i]);
                fprintf(fp_debug, "\n");
        }

        validate(csf_header->tag == HAB_TAG_CSF, "tag");
        validate((csf_header->version == HAB_VER_40 || \
                  csf_header->version == HAB_VER_41 || \
                  csf_header->version == HAB_VER_42 ), "hab version");
        validate((offset + HAB_HDR_LEN(csf_header)) <= csf_len, "length OOB");

        fprintf(fp_output, "\n\n");
        w2f_hdr("TAG");
        fprintf(fp_output, "   \t0x%X\t\tHAB_TAG_CSF\t\tCommand Sequence File header\n\n", csf_header->tag);

        w2f_hdr("LEN");
        fprintf(fp_output, "   \t0x%X\t\t%d bytes\t\tLength of Command Sequence File\n\n", HAB_HDR_LEN(csf_header), HAB_HDR_LEN(csf_header));

        w2f_hdr("VER");
        fprintf(fp_output, "   \t0x%X\t\tHAB_MAJOR.HAB_MINOR\tHAB VERSION\n\n", csf_header->version);

        return sizeof(csf_hdr_t);
}

/*
 * Description : This function initiates the call to different parsing
 *               functions from offset of start of CSF
 *
 * @Inputs  : csf     - Pointer to the start of CSF
 *           csf_len - Length of CSF
 *
 * @Outputs : return Success or Fail
 *
 */
int parse_csf(const uint8_t *csf, int csf_len)
{
        assert(csf != NULL);

        validate(csf_len != 0, "csf length");
        if (debug_log) {
                fprintf(fp_debug, "CSF TAG = 0x%X and Total size = 0x%X\n", (const uint8_t)csf[0], csf_len);
        }

        int offset = 0;
        int hdr_len = 0;
        int cert_count = 0;
        int sig_count = 0;

        do {
                if (debug_log) {
                        fprintf(fp_debug, "\nCSF TAG: 0x%X\n",csf[offset]);
                }

                switch (csf[offset]) {
                case (HAB_TAG_CSF):
                        hdr_len = parse_csf_hdr(&csf[offset], csf_len, offset);
                        if (!hdr_len) {
                                puts("Error: Couldn't parse CSF Header\n");
                                return FAIL;
                        }
                        break;
                case (HAB_CMD_INS_KEY):
                        hdr_len = parse_ins_key_cmd(&csf[offset], csf_len, offset, &cert_count);
                        if (!hdr_len) {
                                puts("Error: Couldn't parse Insert Key Command\n");
                                return FAIL;
                        }
                        break;
                case (HAB_CMD_AUT_DAT):
                        hdr_len = parse_aut_dat_cmd(&csf[offset], csf_len, offset);
                        if (!hdr_len) {
                                puts("Error: Couldn't parse Authenticate Data Command\n");
                                return FAIL;
                        }
                        break;
                case (HAB_CMD_INIT):
                case (HAB_CMD_UNLK):
                        hdr_len = parse_unlock_cmd(&csf[offset], csf_len, offset);
                        if (!hdr_len) {
                                puts("Error: Couldn't parse Unlock Command\n");
                                return FAIL;
                        }
                        break;
                case (HAB_CMD_SET):
                        hdr_len = parse_set_cmd(&csf[offset], csf_len, offset);
                        if (!hdr_len) {
                                puts("Error: Couldn't parse Set Command\n");
                                return FAIL;
                        }
                        break;
                case (HAB_TAG_CRT):
                        hdr_len = parse_cert_sec(&csf[offset], csf_len, offset);
                        if (!hdr_len) {
                                puts("Error: Couldn't parse Certificate Section\n");
                                return FAIL;
                        }
                        break;
                case (HAB_TAG_SIG):
                        hdr_len = parse_sig_sec(&csf[offset], csf_len, offset, &sig_count);
                        if (!hdr_len) {
                                puts("Error: Couldn't parse Signature Section\n");
                                return FAIL;
                        }
                        break;
                case (HAB_TAG_MAC):
                        hdr_len = parse_mac_sec(&csf[offset], csf_len, offset);
                        if (!hdr_len) {
                                puts("Error: Couldn't parse MAC Section\n");
                                return FAIL;
                        }
                        break;
                default :
                        puts("Error : Unrecognized tag\n");
                        return FAIL;
                }

                offset +=hdr_len;

        } while(offset < csf_len);

        if (debug_log) {
                fprintf(fp_debug, "\nfinal offset = 0x%X csf_len = 0x%X\n", offset, csf_len);
        }
        return PASS;
}

/*
 * Description : This function reads the inputs file and returns size
 *
 * @Inputs  : fp         - Input file pointer
 *            input_file - Input file name
 *
 * @Outputs : return File size
 *
 */
static int read_file(FILE **fp, char *input_file)
{
        int ret = 0;

        /* Open file */
        *fp = fopen(input_file, "r");
        if (*fp == NULL) {
                fprintf(stderr, "Couldn't open file %s; %s\n", input_file, strerror(errno));
                return -1;
        }

        /* Seek to the end of file to calculate size */
        if (fseek(*fp , 0 , SEEK_END)) {
                errno = ENOENT;
                fprintf(stderr, "Couldn't seek to end of file %s; %s\n", input_file, strerror(errno));
                return -1;
        }

        /* Get size and go back to start of the file */
        ret = ftell(*fp);
        rewind(*fp);

        return ret;
}

/*
 * Description : Prints the usage information for running csf_parser
 *
 * @Outputs : The usage info will be printed out on console window.
 */
static void print_usage(void) {
        puts("Usage: csf_parser [-d] [[-s <signed_image>] | [-c <csf_binary>]]\n"
		"options:\n"
                "        -d|--enable-debug     -->\tEnable Debug information\n"
                "        -s|--signed-image     -->\tInput signed image\n"
                "        -c|--csf-binary       -->\tInput CSF binary\n"
                "\nNote: Only one image can be parsed at once.\n");
}

int main(int argc , char *argv[])
{
        FILE *fp;
        uint8_t *buf = NULL;
        size_t result;
        int file_size = 0, csf_len = 0;
        const uint8_t *csf;
        const char *output_folder;
        struct stat sb;
        int next_opt = 0;
        int mandatory_opt = 0;

        /* Initialize debug info variable */
        debug_log = 0;

        /* Check for minimum arguments */
        if (argc < 2 || argc > 4) {
                puts("Error: Either -s or -c option required\n");
                print_usage();
                exit(EXIT_FAILURE);
        }

        /* Create output folder */
        output_folder = "output";
        if (stat(output_folder, &sb) == -1)
                mkdir("output", 0700);

        /* Create Parsed output file */
        fp_output = fopen("output/parsed_output.txt", "w");
        if (fp_output == NULL) {
                puts("Error: Couldn't create parsed_output file\n");
                exit(EXIT_FAILURE);
        }

        /* Perform actions according to command-line option */
        do
        {
                next_opt = getopt_long(argc, argv, short_opt, long_opt, NULL);
                switch (next_opt)
                {
                /* Enable Debug */
                case 'd':
                        mandatory_opt += 0;
                        debug_log = 1;
                        /* Create debug output file */
                        fp_debug = fopen("output/debug_log.txt", "w");
                        if (fp_debug == NULL) {
                                puts("Error: Couldn't create debug output file\n");
                                exit(EXIT_FAILURE);
                        }
                        break;
                /* Get file size of signed image */
                case 's':
                /* Get file size of CSF binary */
                case 'c':
                        mandatory_opt += 1;
                        file_size = read_file(&fp, optarg);
                        if (file_size < 0) {
                                fprintf(stderr, "File read error; %s\n", strerror(errno));
                                exit(EXIT_FAILURE);
                        }
                        break;
                /* Display usage */
                case 'h':
                        print_usage();
                        exit(EXIT_FAILURE);
                        break;
                /* Invalid option */
                default:
                        break;
                }
        } while (next_opt != -1);

        if (mandatory_opt != 1) {
                puts("Error: Either -s or -c option required\n");
                print_usage();
                exit(EXIT_FAILURE);
        }

        /* Allocate memory to the buffer */
        buf = malloc(file_size);
        if (buf == NULL || buf == 0) {
                fprintf(stderr, "Error allocating memory; %s\n", strerror(errno));
                goto err;
        }

        /* Copy the file into the buffer */
        result = fread(buf,1,file_size,fp);
        if (result != file_size) {
                fprintf(stderr, "File read error; %s\n", strerror(errno));
                goto err;
        }

        fclose(fp);

        /* Start from the first command-line option */
        optind = 0;
        /* Extract and/or Parse CSF based on command-line option */
        do
        {
                next_opt = getopt_long(argc, argv, short_opt, long_opt, NULL);
                switch (next_opt)
                {
                /* Extract CSF and parse CSF binary */
                case 's':
                        /* Extract the CSF */
                        csf = extract_csf(buf, file_size, &csf_len);
                        if (csf == NULL) {
                                /* An issue with extracting CSF occured */
                                puts("Error: CSF extraction failed.\n");
                                goto err;
                        }

                        /* Parse CSF binary */
                        result = parse_csf(csf, csf_len);
                        if (result == FAIL) {
                                puts("Error: CSF Parse failed.\n");
                                goto err;
                        }
                        break;
                /* Parse CSF binary */
                case 'c':
                        csf = (uint8_t *) buf;
                        /* Parse CSF binary */
                        result = parse_csf(csf, file_size);
                        if (result == FAIL) {
                                puts("Error: CSF Parse failed.\n");
                                goto err;
                        }
                        break;
                default:
                        break;
                }
        } while (next_opt != -1);

        return EXIT_SUCCESS;

err:
        if (debug_log) {
                fclose(fp_debug);
        }
        fclose(fp_output);
        free(buf);
        return EXIT_FAILURE;
}
