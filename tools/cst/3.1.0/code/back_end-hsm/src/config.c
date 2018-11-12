/*===========================================================================*/
/**
 @file    config.c

 @brief   Implements an interface to load HSM related configuration and HSM objects
 binding table.

 @verbatim
 =============================================================================

    Copyright 2018 NXP

Presence of a copyright notice is not an acknowledgement of publication.
This software file listing contains information of NXP that is of a
confidential and proprietary nature and any viewing or use of this file is
prohibited without specific written permission from NXP

 =============================================================================
 @endverbatim */
 
#include <config.h>

int read_hsm_config(const char* config_file, hsm_config_t * config,
		hsm_object_t** hsm_objects) {
	/* When you are calling config_destroy() library will free all the memory allocated by it. */
	/* So before calling config_destroy() you need to save your result some where else. */

	config_t cfg, *cf;
	const char *hsm_module = NULL;
	const char *hsm_user = NULL;
	const char *hsm_pin = NULL;
	long long hsm_slot = 0;
	config_setting_t *setting = NULL;
	hsm_object_t * chsm_objects = NULL;

	cf = &cfg;
	config_init(cf);

	if (!config_read_file(cf, config_file)) {
		fprintf(stderr, "Error reading configuration file %s:%d - %s\n",
				config_error_file(cf), config_error_line(cf),
				config_error_text(cf));
		config_destroy(cf);
		return 1;
	}

	if (config_lookup_string(cf, "hsm.module", &hsm_module)) {
		strcpy(config->module_path, hsm_module);
	} else {
		printf("=> PKCS#11 MODULE PATH: ");
		scanf("%256s", config->module_path);
	}

	if (config_lookup_string(cf, "hsm.pin", &hsm_pin)) {
		strcpy(config->pin, hsm_pin);
	} else {
		printf("=> PIN: ");
		scanf("%32s", config->pin);
	}
	if (config_lookup_int64(cf, "hsm.slot", &hsm_slot)) {
		config->slot = hsm_slot;
	} else {
		printf("=> SLOT: ");
		scanf("%ld", &config->slot);
	}

	/* Output a list of file-id mapping . */
	setting = config_lookup(&cfg, "hsm.objects");
	if (setting != NULL) {
		unsigned int count = config_setting_length(setting);
		unsigned int i;

		for (i = 0; i < count; ++i) {
			config_setting_t *hsm_object = config_setting_get_elem(setting, i);

			const char *file, *id;

			if (!(config_setting_lookup_string(hsm_object, "id", &id)
					&& config_setting_lookup_string(hsm_object, "file", &file)))
				continue;

			hsm_object_t *hobject;
			hobject = (hsm_object_t *) malloc(sizeof(hsm_object_t));

			strcpy(hobject->id, id);
			strcpy(hobject->file, file);

			hobject->next = chsm_objects;
			chsm_objects = hobject;

		}

		*hsm_objects = chsm_objects;

	}

	config_destroy(&cfg);

	return 0;

}
