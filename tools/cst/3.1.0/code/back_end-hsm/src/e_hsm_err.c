/*===========================================================================*/
/**
 @file    e_hsm_err.c

 @brief   Error routines, messages and status codes for HSM engine.

 @verbatim
 =============================================================================

    Copyright 2018 NXP

Presence of a copyright notice is not an acknowledgement of publication.
This software file listing contains information of NXP that is of a
confidential and proprietary nature and any viewing or use of this file is
prohibited without specific written permission from NXP

 =============================================================================
 @endverbatim */
 
#include <stdio.h>
#include <openssl/err.h>
#include "e_hsm_err.h"

/* BEGIN ERROR CODES */
#ifndef OPENSSL_NO_ERR
static ERR_STRING_DATA hsm_str_functs[]=
{
    {ERR_PACK(0,HSM_F_INIT,0),	    "HSM_INIT"},
    {ERR_PACK(0,HSM_F_FINISH,0),	    "HSM_FINISH"},
    {ERR_PACK(0,HSM_F_DESTROY,0),	    "HSM_DESTROY"},
    {ERR_PACK(0,HSM_F_CTRL,0),	    "HSM_CTRL"},
    {ERR_PACK(0,HSM_F_RSA_INIT,0),	    "HSM_RSA_INIT"},
    {ERR_PACK(0,HSM_F_RSA_FINISH,0),	    "HSM_RSA_FINISH"},
    {ERR_PACK(0,HSM_F_FINDKEY,0),"HSM_FINDKEY"},
    {ERR_PACK(0,HSM_F_RSA_GEN_KEY,0),    "HSM_RSA_GEN_KEY"},
    {ERR_PACK(0,HSM_F_RSA_PUB_ENC,0),    "HSM_RSA_PUB_ENC"},
    {ERR_PACK(0,HSM_F_RSA_PRIV_ENC,0),   "HSM_RSA_PRIV_ENC"},
    {ERR_PACK(0,HSM_F_RSA_PUB_DEC,0),    "HSM_RSA_PUB_DEC"},
    {ERR_PACK(0,HSM_F_RSA_PRIV_DEC,0),   "HSM_RSA_PRIV_DEC"},
    {ERR_PACK(0,HSM_F_RSA_SIGN,0),	    "HSM_RSA_SIGN"},
    {ERR_PACK(0,HSM_F_RSA_VERIFY,0),	    "HSM_RSA_VERIFY"},
    {ERR_PACK(0,HSM_F_RAND_ADD,0),	    "HSM_RAND_ADD"},
    {ERR_PACK(0,HSM_F_RAND_BYTES,0),	    "HSM_RAND_BYTES"},
    {ERR_PACK(0,HSM_F_GETSESSION,0),	    "HSM_GETSESSION"},
    {ERR_PACK(0,HSM_F_FREESESSION,0),    "HSM_FREESESSION"},
    {ERR_PACK(0,HSM_F_INITKEY,0),        "HSM_INITKEY"},
    {ERR_PACK(0,HSM_F_DIGESTINIT,0),    "HSM_DIGESTINIT"},
    {ERR_PACK(0,HSM_F_DIGESTUPDATE,0),    "HSM_DIGESTUPDATE"},
    {ERR_PACK(0,HSM_F_DIGESTFINISH,0),    "HSM_DIGESTFINISH"},
    {ERR_PACK(0,HSM_F_CIPHER_UPDATE,0),    "HSM_CIPHER_UPDATE"},
    {ERR_PACK(0,HSM_F_PREINIT,0),    "HSM_PREINIT"},
    {ERR_PACK(0,HSM_F_ADDTOKEN,0),    "HSM_ADDTOKEN"},
    {ERR_PACK(0,HSM_F_LOAD_PRIVKEY,0),    "HSM_LOAD_PRIVKEY"},
    {ERR_PACK(0,HSM_F_LOAD_PUBKEY,0),    "HSM_LOAD_PUBKEY"},
    {ERR_PACK(0,HSM_F_DIGESTCOPY,0),    "HSM_DIGESTCOPY"},
    {ERR_PACK(0,HSM_F_GET_HSM_CIPHERS,0),	    "HSM_GET_HSM_CIPHERS"},
    {ERR_PACK(0,HSM_F_GET_HSM_DIGESTS,0),	    "HSM_GET_HSM_DIGESTS"},
    {ERR_PACK(0,HSM_F_ENGINE_CIPHERS,0),	    "HSM_ENGINE_CIPHERS"},
    {ERR_PACK(0,HSM_F_ENGINE_DIGESTS,0),	    "HSM_ENGINE_DIGESTS"},
	{ERR_PACK(0,HSM_F_FINDCERT,0),"HSM_FINDCERT"},
    {0,NULL}
};

static ERR_STRING_DATA hsm_str_reasons[]=
{
    {HSM_R_ALREADY_LOADED                 ,"PKCS#11 DSO already loaded"},
    {HSM_R_DSO_FAILURE                    ,"unable to load PKCS#11 DSO"},
    {HSM_R_NOT_LOADED                     ,"PKCS#11 DSO not loaded"},
    {HSM_R_PASSED_NULL_PARAMETER          ,"null parameter passed"},
    {HSM_R_COMMAND_NOT_IMPLEMENTED        ,"command not implemented"},
    {HSM_R_INITIALIZE                     ,"C_Initialize failed"},
    {HSM_R_FINALIZE                       ,"C_Finalize failed"},
    {HSM_R_GETINFO                        ,"C_GetInfo faile"},
    {HSM_R_GETSLOTLIST                    ,"C_GetSlotList failed"},
    {HSM_R_NO_MODULUS_OR_NO_EXPONENT      ,"no modulus or no exponent"},
    {HSM_R_ATTRIBUT_SENSITIVE_OR_INVALID  ,"attrribute sensitive or invalid	"},
    {HSM_R_GETATTRIBUTVALUE               ,"C_GetAttributeValue failed"},
    {HSM_R_NO_MODULUS                     ,"no modulus"},
    {HSM_R_NO_EXPONENT                    ,"no exponent"},
    {HSM_R_FINDOBJECTSINIT                ,"C_FindObjectsInit failed"},
    {HSM_R_FINDOBJECTS                    ,"C_FindObjects failed"},
    {HSM_R_FINDOBJECTSFINAL               ,"C_FindObjectsFinal failed"},
    {HSM_R_OBJECT_NOT_FOUND               ,"object not found"},
    {HSM_R_CREATEOBJECT                   ,"C_CreateObject failed"},
    {HSM_R_DESTROYOBJECT                  ,"C_DestroyObject failed"},
    {HSM_R_OPENSESSION                    ,"C_OpenSession failed"},
    {HSM_R_CLOSESESSION                   ,"C_CloseSession failed"},
    {HSM_R_ENCRYPTINIT                    ,"C_EncryptInit failed"},
    {HSM_R_ENCRYPT                        ,"C_Encrypt failed"},
    {HSM_R_SIGNINIT                       ,"C_SignInit failed"},
    {HSM_R_SIGN                           ,"C_Sign failed"},
    {HSM_R_DECRYPTINIT                    ,"C_DecryptInit failed"},
    {HSM_R_DECRYPT                        ,"C_Decrypt failed"},
    {HSM_R_VERIFYINIT                     ,"C_VerifyRecover failed"},
    {HSM_R_VERIFY                         ,"C_Verify failed	"},
    {HSM_R_VERIFYRECOVERINIT              ,"C_VerifyRecoverInit failed"},
    {HSM_R_VERIFYRECOVER                  ,"C_VerifyRecover failed"},
    {HSM_R_GEN_KEY                        ,"C_GenerateKeyPair failed"},
    {HSM_R_SEEDRANDOM                     ,"C_SeedRandom failed"},
    {HSM_R_GENERATERANDOM                 ,"C_GenerateRandom failed"},
    {HSM_R_INVALID_MESSAGE_LENGTH         ,"invalid message length"},
    {HSM_R_UNKNOWN_ALGORITHM_TYPE         ,"unknown algorithm type"},
    {HSM_R_UNKNOWN_ASN1_OBJECT_ID         ,"unknown asn1 onject id"},
    {HSM_R_UNKNOWN_PADDING_TYPE           ,"unknown padding type"},
    {HSM_R_DIGEST_TOO_BIG                 ,"digest too big"},
    {HSM_R_MALLOC_FAILURE                 ,"malloc failure"},
    {HSM_R_CTRL_COMMAND_NOT_IMPLEMENTED   ,"control command not implemented"},
    {HSM_R_GETSLOTINFO		     ,"C_GetSlotInfo failed"},
    {HSM_R_GETMECHANISMLIST		     ,"C_GetMechanismList failed"},
    {HSM_R_GETMECHANISMINFO		     ,"C_GetMechanismInfo failed"},
    {HSM_R_BADMECHANISM		     ,"bad mechanism"},
    {HSM_R_DIGESTINIT		     ,"C_DigestInit failed"},
    {HSM_R_DIGESTUPDATE		     ,"C_DigestUpdate failed"},
    {HSM_R_DIGESTFINAL		     ,"C_DigestFinal failed"},
    {HSM_R_NOTOKENS			     ,"no hardware tokens found"},
    {HSM_R_NOTOKENFORALGORITHM	     ,"no tokens available to accelerate algorithm"},
    {HSM_R_DIGEST			     ,"C_Digest failed"},
    {HSM_R_TOKEN_NOT_AVAILABLE            ,"Token in requested slot is not available"},
    {HSM_R_NO_SLOT_SELECTED		     ,"No slot selected, please add slot = <num> to your"
					      " hsm.cfg configuration file"},
	{HSM_R_LOGIN			     ,"C_Login failed"},
	{HSM_R_BIGNUM			     ,"BN_bin2bn failed"},
    {0,NULL}
};

#endif	

static int hsm_lib_error_code=0;
static int hsm_error_init=1;

void ERR_load_hsm_strings(void)
{
    if (hsm_lib_error_code == 0)
	hsm_lib_error_code = ERR_get_next_error_library();

    if (hsm_error_init)
    {
	hsm_error_init=0;
#ifndef OPENSSL_NO_ERR
	ERR_load_strings(hsm_lib_error_code,hsm_str_functs);
	ERR_load_strings(hsm_lib_error_code,hsm_str_reasons);
#endif
    }
}

void ERR_unload_hsm_strings(void)
{
    if (hsm_error_init == 0)
    {
#ifndef OPENSSL_NO_ERR
	ERR_unload_strings(hsm_lib_error_code,hsm_str_functs);
	ERR_unload_strings(hsm_lib_error_code,hsm_str_reasons);
#endif
	hsm_error_init = 1;
    }
}

void ERR_hsm_error(int function, int reason, char *file, int line)
{
    if (hsm_lib_error_code == 0)
	hsm_lib_error_code=ERR_get_next_error_library();
    ERR_PUT_error(hsm_lib_error_code,function,reason,file,line);
    //ERR_print_errors_fp(stderr);
}
