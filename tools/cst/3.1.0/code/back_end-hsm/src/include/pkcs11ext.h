/*===========================================================================*/
/**

@verbatim
=============================================================================

    Copyright 2018 NXP

Presence of a copyright notice is not an acknowledgement of publication.
This software file listing contains information of NXP that is of a
confidential and proprietary nature and any viewing or use of this file is
prohibited without specific written permission from NXP

=============================================================================
@endverbatim */

#ifndef PKCS11EXT_H
#define PKCS11EXT_H

#define CKM_TLS1_PRE_MASTER_KEY_GEN 	 CKM_VENDOR_DEFINED+CKM_SSL3_PRE_MASTER_KEY_GEN
#define CKM_TLS1_MASTER_KEY_DERIVE  	 CKM_VENDOR_DEFINED+CKM_SSL3_MASTER_KEY_DERIVE 
#define CKM_TLS1_KEY_AND_MAC_DERIVE 	 CKM_VENDOR_DEFINED+CKM_SSL3_KEY_AND_MAC_DERIVE
#define CKM_TLS1_MD5_MAC            	 CKM_VENDOR_DEFINED+CKM_SSL3_MD5_MAC           
#define CKM_TLS1_SHA1_MAC           	 CKM_VENDOR_DEFINED+CKM_SSL3_SHA1_MAC          
#define CKM_RSA_PKCS_KEY_PAIR_GEN_POOL   CKM_VENDOR_DEFINED+CKM_RSA_PKCS_KEY_PAIR_GEN

#endif
