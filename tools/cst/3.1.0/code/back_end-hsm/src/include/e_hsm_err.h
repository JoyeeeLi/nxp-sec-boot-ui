#ifndef _E_HSM_ERR_H_
#define _E_HSM_ERR_H_
/*===========================================================================*/
/**
 @file    e_hsm_err.h

 @brief   Header file for e_hsm_err.c

 @verbatim
 =============================================================================

    Copyright 2018 NXP

Presence of a copyright notice is not an acknowledgement of publication.
This software file listing contains information of NXP that is of a
confidential and proprietary nature and any viewing or use of this file is
prohibited without specific written permission from NXP

 =============================================================================
 @endverbatim */

void ERR_load_hsm_strings(void);
void ERR_unload_hsm_strings(void);
void ERR_hsm_error(int function, int reason, char *file, int line);
#define hsm_err(f,r) ERR_hsm_error((f),(r),__FILE__,__LINE__)

/* Error codes for the HSM functions. */

/* Function codes. */

#define HSM_F_INIT 100
#define HSM_F_FINISH 101
#define HSM_F_DESTROY 102
#define HSM_F_CTRL 103
#define HSM_F_RSA_INIT 104
#define HSM_F_RSA_FINISH 105
#define HSM_F_FINDKEY 106
#define HSM_F_RSA_GEN_KEY 107
#define HSM_F_RSA_PUB_ENC 108
#define HSM_F_RSA_PRIV_ENC 109
#define HSM_F_RSA_PUB_DEC 110
#define HSM_F_RSA_PRIV_DEC 111
#define HSM_F_RSA_SIGN 112
#define HSM_F_RSA_VERIFY 113
#define HSM_F_RAND_ADD 114
#define HSM_F_RAND_BYTES 115
#define HSM_F_GETSESSION 116
#define HSM_F_FREESESSION 117
#define HSM_F_LOAD_PUBKEY 118
#define HSM_F_LOAD_PRIVKEY 119
#define HSM_F_ADDTOKEN 120
#define HSM_F_INITKEY 121
#define HSM_F_DIGESTINIT 122
#define HSM_F_DIGESTUPDATE 123
#define HSM_F_DIGESTFINISH 124
#define HSM_F_CIPHER_UPDATE 125
#define HSM_F_PREINIT 126
#define HSM_F_DIGESTCOPY 127
#define HSM_F_ENGINE_DIGESTS 128
#define HSM_F_ENGINE_CIPHERS 129
#define HSM_F_GET_HSM_DIGESTS 130
#define HSM_F_GET_HSM_CIPHERS 131
#define HSM_F_FINDCERT 132

/* Reason codes. */
#define HSM_R_ALREADY_LOADED 100
#define HSM_R_DSO_FAILURE 101
#define HSM_R_NOT_LOADED 102
#define HSM_R_PASSED_NULL_PARAMETER 103
#define HSM_R_COMMAND_NOT_IMPLEMENTED 104
#define HSM_R_INITIALIZE 105
#define HSM_R_FINALIZE 106
#define HSM_R_GETINFO 107
#define HSM_R_GETSLOTLIST 108
#define HSM_R_NO_MODULUS_OR_NO_EXPONENT 109
#define HSM_R_ATTRIBUT_SENSITIVE_OR_INVALID 110
#define HSM_R_GETATTRIBUTVALUE 111
#define HSM_R_NO_MODULUS 112
#define HSM_R_NO_EXPONENT 113
#define HSM_R_FINDOBJECTSINIT 114
#define HSM_R_FINDOBJECTS 115
#define HSM_R_FINDOBJECTSFINAL 116
#define HSM_R_OBJECT_NOT_FOUND 117
#define HSM_R_CREATEOBJECT 118
#define HSM_R_DESTROYOBJECT 119
#define HSM_R_OPENSESSION 120
#define HSM_R_CLOSESESSION 121
#define HSM_R_ENCRYPTINIT 122
#define HSM_R_ENCRYPT 123
#define HSM_R_SIGNINIT 124
#define HSM_R_SIGN 125
#define HSM_R_DECRYPTINIT 126
#define HSM_R_DECRYPT 127
#define HSM_R_VERIFYINIT 128
#define HSM_R_VERIFY 129
#define HSM_R_VERIFYRECOVERINIT 130
#define HSM_R_VERIFYRECOVER 131
#define HSM_R_GEN_KEY 132
#define HSM_R_SEEDRANDOM 133
#define HSM_R_GENERATERANDOM 134
#define HSM_R_INVALID_MESSAGE_LENGTH 135
#define HSM_R_UNKNOWN_ALGORITHM_TYPE 136
#define HSM_R_UNKNOWN_ASN1_OBJECT_ID 137
#define HSM_R_UNKNOWN_PADDING_TYPE 138
#define HSM_R_DIGEST_TOO_BIG 139
#define HSM_R_MALLOC_FAILURE 140
#define HSM_R_CTRL_COMMAND_NOT_IMPLEMENTED 141
#define HSM_R_GETSLOTINFO 142
#define HSM_R_GETMECHANISMLIST 143
#define HSM_R_GETMECHANISMINFO 144
#define HSM_R_BADMECHANISM 145
#define HSM_R_DIGESTINIT 146
#define HSM_R_DIGESTUPDATE 147
#define HSM_R_DIGESTFINAL 148
#define HSM_R_NOTOKENS 149
#define HSM_R_NOTOKENFORALGORITHM 150
#define HSM_R_DIGEST 151
#define HSM_R_TOKEN_NOT_AVAILABLE 152
#define HSM_R_NO_SLOT_SELECTED 153
#define HSM_R_LOGIN 154
#define HSM_R_BIGNUM 155
#endif
