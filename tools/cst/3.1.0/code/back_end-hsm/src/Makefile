#==============================================================================
#
#    File Name:  Makefile
#
#    General Description: Makefile for HSM backend for CST
#
#==============================================================================
#
#    Copyright 2018 NXP
#
# Presence of a copyright notice is not an acknowledgement of publication.
# This software file listing contains information of NXP that is of a
# confidential and proprietary nature and any viewing or use of this file is
# prohibited without specific written permission from NXP
#
#==============================================================================

#==============================================================================
# Compiler/Linker/Archiver Commands
#==============================================================================


ifneq ($(ARCH),)
ARCH := $(shell getconf LONG_BIT)
endif

$(info $$ARCH is [${ARCH}])

C_FLAGS_32 := -m32
C_FLAGS_64 := -m64

LD_FLAGS_32 := 
LD_FLAGS_64 := 

DESTDIR=./
PREFIX=./

STATIC=libbackend.a

CC = gcc
#CFLAGS = -Wall -Winline -pipe -I./include -I$(OPENSSL_PATH)/include

CFLAGS = $(C_FLAGS_$(ARCH)) -Wall -Wl,--export-all-symbols -w -Winline -pipe -I./include -I$(OPENSSL_PATH)/include 

LDFLAGS = -L./lib 

LIBS = -lssl -lcrypto -ldl -lpthread -lconfig

ifeq ($(OS),Windows_NT)
LIBS += -lpsapi -lgdi32
endif

SRC = backend.c config.c e_hsm.c e_hsm_err.c openssl_helper.c

OBJ = $(SRC:.c=.o)

ifeq ($(OPENSSL_PATH),)
OPENSSL_PATH := $(ROOTPATH)/../openssl
endif

# Define -mno-ms-bitfields to get correct bit-field layout of packed structs
LDFLAGS  += -I$(OPENSSL_PATH)/include -mno-ms-bitfields
LDFLAGS += -L$(OPENSSL_PATH)/lib


$(STATIC): $(OBJ)
		@echo "[Link (Static) libbackend]"
		@ar rcs $@ $^

.c.o:
		@echo [Compile] $<
		@$(CC) -c $(CFLAGS) $< -o $@

clean:
		rm -f $(OBJ) *~ core tags *.bak Makefile.bak libbackend.*

.PHONY: install
#install: $(STATIC)
#		@install -m 0755 $< $(DESTDIR)$(PREFIX)/lib

all: install
		$(CC)  $(C_FLAGS_$(ARCH)) -std=c99  -D_POSIX_C_SOURCE=200809L -Wall -Werror -g -Wall -o cst  libfrontend.a libbackend.a $(LDFLAGS) $(LIBS) -fno-builtin -fno-strict-aliasing -fno-common -DREMOVE_ENCRYPTION -Wl,--allow-multiple-definition
