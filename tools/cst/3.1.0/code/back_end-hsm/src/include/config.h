#ifndef ___CONFIG_H_INC___
#define ___CONFIG_H_INC___
/*===========================================================================*/
/**
 @file    config.h

 @brief   Header file for config.c

 @verbatim
 =============================================================================

    Copyright 2018 NXP

Presence of a copyright notice is not an acknowledgement of publication.
This software file listing contains information of NXP that is of a
confidential and proprietary nature and any viewing or use of this file is
prohibited without specific written permission from NXP

 =============================================================================
 @endverbatim */


#define LIBCONFIG_STATIC

#include <libconfig.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAX_PATH 260
#define MAX_PIN_LEN 255
#define MAX_AUTH_LEN 32
#define MAX_ID_LEN 128

/* This should definitively be removed in future version */
/* In this version we should have it since we can't modify the frontend to support providing HSM objects ID in CSF file */
typedef struct hsm_object {
	char id[MAX_ID_LEN]; /*HSM Object ID*/
	char file[MAX_PATH]; /*Object path on file system*/
	struct hsm_object *next;
} hsm_object_t;

typedef struct hsm_config {
	unsigned char module_path[MAX_PATH];
	unsigned char pin[MAX_PIN_LEN];
	unsigned long slot;
} hsm_config_t;

int read_hsm_config(const char* config_file, hsm_config_t * config,
		hsm_object_t** hsm_objects);

#endif /* ___CONFIG_H_INC___ */

