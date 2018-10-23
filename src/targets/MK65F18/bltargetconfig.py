#!/usr/bin/env python

# Copyright (c) 2013 Freescale Semiconductor, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# o Redistributions of source code must retain the above copyright notice, this list
#   of conditions and the following disclaimer.
#
# o Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# o Neither the name of Freescale Semiconductor, Inc. nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, os
from fsl.bootloader import memoryrange
from fsl.debugger_utils import kDebuggerType_JLink
from fsl.bootloader import bootsources
from fsl.bootloader import encryptiontypes
import bltestconfig

# @todo Verify cpu and memoryRanges

# board = tower
# build = Debug, Release
# file  = board + _bootloader.elf


cpu = 'MK65F18'
board = bltestconfig.target[1]
compiler = bltestconfig.target[2]
build = bltestconfig.target[3]

availableCommands = 0xefff
availablePeripherals = 0x17
supportedPeripheralSpeed_uart = [4800, 9600, 19200, 57600, 115200, 256000] # @todo Verify
supportedPeripheralSpeed_i2c = [5, 50, 100, 400]                           # @todo Verify
supportedPeripheralSpeed_spi = [5, 10, 20, 50, 100, 200, 500]  # @todo Verify
deviceMemoryAccessable = True             # @todo Verify
systemDeviceId = 0x650013AC               # @ Device ID
                                           
bootFrom = bootsources.kFlashLoader_Flash
isCrcCheckSupported = False
isSystemRestorationCheckSupported = True
isEncryptionSupported = False
encryptionModuleType = encryptiontypes.kEncryptionType_LTC

isHardwareSwapForReliableUpdate = True
defaultBackupAppAddrForReliableUpdate = 0x105000

# registers referenced in test cases for device memory access 
kSIM_AddressFor8BitModuleClockGate = 0x40048034  # SIM_SCGC4
kClockGatePosFor8BitModule = 10                  # UART0
kAccessAddressFor8BitModuleStart = 0x4006A002  # UART0_BDH
kAccessLengthFor8BitModule = 1

kSIM_AddressFor16BitModuleClockGate = 0x4004803c # SIM_SCGC6
kClockGatePosFor16BitModule = 1 # DMA
kAccessAddressFor16BitModuleStart = 0x40009014
kAccessLengthFor16BitModule = 2

kSIM_AddressFor32BitModuleClockGate = 0x4004803c # SIM_SCGC6
kClockGatePosFor32BitModule = 1    #DMA
kAccessAddressFor32BitModuleStart = 0x40009028 # DMA_TCD1_NBYTES_MLNO
kAccessLengthFor32BitModule = 8

elfFilename = os.path.join(os.path.dirname(__file__), compiler, board, 'output', build, board + '.elf')
binFilename = os.path.join(os.path.dirname(__file__), compiler, board, 'output', build, board + '.bin')
testWorkingDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'test', 'working')
#debugger = kDebuggerType_Mbed
debugger = kDebuggerType_JLink

# flashStartAddress = 0
# flashSize = 2MB
# sectorSize = 4KB
# block count = 4
# flashAlignmentSize = 4 
# eraseAlignmentSize = 16
memoryRange = {'flash':memoryrange.MemoryRange(0, 0x200000, 'state_mem0.dat', True, 4096, 4, 8, 16),

# ramStartAddress = 0x1fff0000
# ramSize = 256KB
               'ram':memoryrange.MemoryRange(0x1fff0000, 0x40000, 'state_mem1.dat'),
              }

