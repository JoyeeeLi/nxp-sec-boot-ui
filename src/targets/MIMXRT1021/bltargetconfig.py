#!/usr/bin/env python

# Copyright (c) 2014 Freescale Semiconductor, Inc.
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
from fsl.bootloader.memoryrange import MemoryRange
#from fsl.debugger_utils import kDebuggerType_JLink
from fsl.debugger_utils import kDebuggerType_Mbed
from fsl.bootloader import bootsources
from fsl.bootloader import encryptiontypes
import bltestconfig

# board = fpga, rom
# build = Debug, Release
# file  = bootloader.elf 

cpu = 'MIMXRT1021'
board = bltestconfig.target[1]
compiler = bltestconfig.target[2]
build = bltestconfig.target[3]

availablePeripherals = 0x11 #0x02
availableCommands = 0x5EFDF #0x07
maximumPacketSize = 512
supportedPeripheralSpeed_uart = [4800, 9600, 19200, 57600, 115200] # @todo Verify
supportedPeripheralSpeed_i2c = [5, 50, 100, 400]                           # @todo Verify
supportedPeripheralSpeed_spi = [5, 10, 20, 50, 100, 200, 500]  # @todo Verify
systemDeviceId = 0x04500008                   # !!!prepare to delete

deviceMemoryAccessable = True

# new
kAccessLengthFor8BitModule = 1
kAccessLengthFor16BitModule = 2
kAccessLengthFor32BitModule = 8

# read/write register
# width8BitsAddress = 0x400B4002     # EWM Compare Low Register (CMPL)
# width16BitsAddress = 0x403B4000    # AOI BFCRT010
# width32BitsAddress = 0x401B8000    # GPIO data registe (DR)

# read/write/fill memory
interalRAMidName = ['itcm', 'dtcm', 'ram']
interalFlashidName = []
# externalMemoryName = ['SerialNORorEEPROM']

## eeprom
# SerialNORorEEPROM = [0x110, 0xc0100530]   # SPI1, PCS0, NOR Flash, 256B Page, 64KB Sector, 16MB Device
# new

#bootFrom = bootsources.bootSourcesDict['Freedom_Bootloader'] #kBootLoader = 0x04 
bootloaderType = 0x02 # bootsources.kBootRAM_ExecuteRAM

isCrcCheckSupported = False
isSystemRestorationCheckSupported = False
isEncryptionSupported = True
isCore1Present = False
encryptionModuleType = encryptiontypes.kEncryptionType_mmCAU
mmcauBinFileAppPlatform = encryptiontypes.kMmcauBinFileAppPlatformType_cm0p


ledDemoFileName = 'led_demo_MIMXRT1021_evk_ram.bin'
ledDemoStartAddress = 0x0000a000
ledDemoApplicationBinary = 0x20208400   # not use
flashloaderFileName = 'ivt_flashloader_MIMXRT1021_ocram.bin'
flashloaderStartAddress = 0x20208000
flashloaderIvtOffset = 0x20208400   # RAM resident bootloader entry address
isWdogMustBeDisabledForExecuteCase = True

# elfFilename = os.path.join(os.path.dirname(__file__), compiler, board, 'output', build, 'rom_bootloader.elf')
# workingDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'test', 'working')
# targetResetApp = os.path.join(workingDir, 'reset' + '_' + cpu.lower() + '_' + board.lower() + '.out')
#debugger = kDebuggerType_JLink
debugger = kDebuggerType_Mbed

# memory map
memoryRange = {
    # ITCM, 256KByte(64KByte)
    'itcm' : MemoryRange(0x00000000, 0x10000, 0x00040000, 'state_mem0.dat'),
    # DTCM, 256KByte(64KByte)
    'dtcm' : MemoryRange(0x20000000, 0x10000, 0x20040000, 'state_mem1.dat'),
    # OCRAM, 256KByte(128KByte)
    'ram' : MemoryRange(0x20200000, 0x20000, 0x20240000, 'state_mem2.dat'),

    # SEMC Parallel NOR (Micron MT28EW128ABA1LPC-0SIT)
    # Micron MT28EW128ABA1LPC-0SIT    (x8/x16 bits, 32B Page/128KB Block/128Mb Device,   Non-ADM, Asynchronous)
    # Winbond W29GL128CH9T            (x8/x16 bits, 64B Page/128KB Sector/128Mb Device,  Non-ADM, Asynchronous)
    # Spansion S29GL128S90TFI020      (x16 bits,    512B Page/128KB Sector/128Mb Device, Non-ADM, Asynchronous)
    'SEMC_Parallel_NOR' : MemoryRange(0x90000000, 0x01000000, 0x91000000, 'state_ex_Paralle_NOR.dat', True, True, 0x20, 0x20000),
    
    # Serial NOR over FlexSPI module (IS25LP064A-JBLE) (8MB)
    'FlexSPI_Serial_NOR' : MemoryRange(0x60000000, 0x00800000, 0x60800000, 'state_ex_Paralle_NOR.dat', True, True, 0x100, 0x10000),
    
    # SEMC Raw NAND (Micron MT29F16G08ABACAWP:C) 0x0 - 0x80000000 2GB
    # Macronix MX30LF4GE8AB-TI        (x8 bits, 2KB Page/128KB Block/4Gb Device,  0bit ECC, 3.3V)
    # Micron MT29F4G08ABBDAWP         (x8 bits, 2KB Page/128KB Block/4Gb Device,  4bit ECC, 1.8V)
    # Micron MT29F4G08ABAFAWP:D       (x8 bits, 2KB Page/128KB Block/4Gb Device,  4bit ECC, 3.3V)
    # Micron MT29F16G08ABACAWP:C      (x8 bits, 4KB Page/512KB Block/16Gb Device, 4bit ECC, 3.3V)
    # Winbond W29N01GVSIAA            (x8 bits, 2KB Page/128KB Block/1Gb Device,  1bit ECC, 3.3V)
    'SEMC_Raw_NAND' : MemoryRange(0x100000, 0x0FF00000, 0x0FF00000, 'state_ex_raw_NAND.dat', True, False, 0x1000, 0x80000),
    
    # LPSPI Serial NOR/EEPROM, 128KB (Micron MT25QL128ABA1ESE-OSIT)
    # Onsemi CAT25512HU5I-GT3         (EEPROM,    1-bit SPI,    20MHz,      128B Page/512Kb Device)
    # Micron MT25QL128ABA1ESE-OSIT    (NOR Flash, Multiple I/O, 133MHz-STR, 64B Page/4-32-64KB Sector/128Mb Device)
    # Spansion S25FL129P              (NOR Flash, Multiple I/O, 80MHz,      256B Page/4-8-64-256KB Sector/128Mb Device)
    'LPSPI_Serial_NOR_EEPROM' : MemoryRange(0x0, 0x01000000, 0x01000000, 'state_ex_ser_nor_eeprom.dat', True, False, 0x40, 0x1000),

    # uSDHC Managed NAND SD
    'uSDHC_Managed_NAND_SD' : MemoryRange(0x00000000, 0x01000000, 0x01000000, 'state_ex_Paralle_NOR.dat', True, False, 0x200, 0x20000),

    # uSDHC Managed NAND eMMC (MTFC8GAKAJCN-1M WT)
    'uSDHC_Managed_NAND_eMMC' : MemoryRange(0x00000000, 0x08000000, 0x08000000, 'state_ex_Paralle_NOR.dat', True, False, 0x200, 0x20000)
}

reservedRegionDict = {   # new
    # DTCM, 256KB
    'dtcm' : [0x20000000, 0x2000DA77],
    # OCRAM, 256KB
    'ram' : [0x2020A000, 0x2021E6CC]
}

externalMemoryIdDict = {
    0x00 : None,
    0x01 : 'QuadSPI_Serial_NOR',
    0x08 : 'SEMC_Parallel_NOR',
    0x09 : 'FlexSPI_Serial_NOR',
    0x100 : 'SEMC_Raw_NAND',
    0x101 : 'FlexSPI_Serial_NAND',
    0x110 : 'LPSPI_Serial_NOR_EEPROM',
    0x120 : 'uSDHC_Managed_NAND_SD',
    0x121 : 'uSDHC_Managed_NAND_eMMC'
}
