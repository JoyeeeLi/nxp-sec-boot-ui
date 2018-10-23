#! /usr/bin/env python

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

import sys
import os
import stat
import time
import shared_utils
import common_util

sys.path.append(os.path.abspath("../bin"))
from fsl import bootloader
from fsl.bootloader.memoryrange import MemoryRange
from fsl.bootloader import bootsources
from fsl.bootloader import properties
import pytest

##
# @brief Reset the target before we start any of these tests in case the active peripheral
#        is different than the current bltestconfig.peripheral. Just have to do it once 
#        for all the test cases in this file.
#
@pytest.fixture(scope='module', autouse=True)
def setup(tgt, request):
    tgt.reset()
    time.sleep(5)

##
# @brief Test the bootloader get property command.
class TestGetProperty:
    clockConfigFlag = False
    
    @pytest.fixture(autouse=True)
    def setup(self, bl, request):
        # make sure bootloader run with specific clock if needed
        if not TestGetProperty.clockConfigFlag:
            common_util.updateUserConfigAreaAsRequested(bl) 
        TestGetProperty.clockConfigFlag = True

    def test_version(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_CurrentVersion)
        assert status == bootloader.status.kStatus_Success
        # Test for version 1.0.0 or version 1.1.0 or version 1.2.0
        assert (results[0] == properties.kBootloaderVersion_1_0_0) or \
               (results[0] == properties.kBootloaderVersion_1_1_0) or \
               (results[0] == properties.kBootloaderVersion_1_1_1) or \
               (results[0] == properties.kBootloaderVersion_1_2_0) or \
               (results[0] == properties.kBootloaderVersion_1_3_0) or \
               (results[0] == properties.kBootloaderVersion_1_4_0) or \
               (results[0] == properties.kBootloaderVersion_1_4_1) or \
               (results[0] == properties.kBootloaderVersion_1_5_0) or \
               (results[0] == properties.kBootloaderVersion_1_5_1) or \
               (results[0] == properties.kBootloaderVersion_2_0_0) or \
               (results[0] == properties.kBootloaderVersion_2_1_0)
 
    def test_target_version(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_TargetVersion)
        assert status == bootloader.status.kStatus_Success or status == bootloader.status.kStatus_UnknownProperty
        if status == bootloader.status.kStatus_Success:
            # Test for version 1.0.0 or version 1.1.0 or version 1.2.0
            assert (results[0] == properties.kTargetVersion_1_0_0) or \
                   (results[0] == properties.kTargetVersion_1_1_0) 
 
    def test_peripherals(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_AvailablePeripherals)
        assert status == bootloader.status.kStatus_Success
        assert results[0] == bl.target.availablePeripherals
 
 
    def test_flash_start_address(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_FlashStartAddress)
        assert status == bootloader.status.kStatus_Success
        assert results[0] == bl.target.memoryRange['flash'].start
 
 
    def test_flash_size(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_FlashSizeInBytes)
        assert status == bootloader.status.kStatus_Success
        assert results[0] == bl.target.memoryRange['flash'].length
 
 
    def test_flash_sector_size(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_FlashSectorSize)
        assert status == bootloader.status.kStatus_Success
        assert results[0] == bl.target.memoryRange['flash'].flashSectorSize
 
 
    def test_flash_block_count(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_FlashBlockCount)
        assert status == bootloader.status.kStatus_Success or \
               status == bootloader.status.kStatus_UnknownProperty
        if status == bootloader.status.kStatus_Success:
            assert results[0] == bl.target.memoryRange['flash'].flashBlockCount
 
 
    def test_available_commands(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_AvailableCommands)
        assert status == bootloader.status.kStatus_Success
        assert results[0] == bl.target.availableCommands
 
 
    def test_crc_check_status(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_CrcCheckStatus)
        if bl.target.isCrcCheckSupported:
            assert status == bootloader.status.kStatus_Success
        else:
            assert status == bootloader.status.kStatus_UnknownProperty
 
    def test_verify_write_flag(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_VerifyWrites)
        assert status == bootloader.status.kStatus_Success
        # defaults to 1
        assert results[0] == 1
 
 
    def test_max_supported_packet_size(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_MaxPacketSize)
        assert status == bootloader.status.kStatus_Success
        assert results[0] == 0x20
 
 
    def test_reserved_regions(self, bl):
        if bl.target.bootFrom == bootsources.kFlashLoader_Flash:
            pytest.skip("This case is not supported")
            
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_ReservedRegions)
        assert status == bootloader.status.kStatus_Success or \
               status == bootloader.status.kStatus_UnknownProperty
 
        if status == bootloader.status.kStatus_Success:
            resultRegionCount = len(results) / 2
            targetReservedRegions = []
     
            # Build the reported reserved regions list that the target reports
            for i in range(resultRegionCount):
                start = results[i * 2]
                length = results[i * 2 + 1] - start + 1
                thisRange = MemoryRange(start, length)
                targetReservedRegions.append(thisRange)
     
            for i in range(len(bl.target.reservedRanges)):
                # Check that at least the ELF reserved ranges are reported
                assert bl.target.reservedRanges[i] in targetReservedRegions
 
 
    def test_validate_region_flag(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_ValidateRegions)
        # Note: status == bootloader.status.kStatus_UnknownProperty is for L3KS, which doesn't support this property  
        assert status == bootloader.status.kStatus_Success or status == bootloader.status.kStatus_UnknownProperty
        if (status == bootloader.status.kStatus_Success):
            # defaults to 1
            assert results[0] == 1
 
 
    def test_ram_start_address(self, bl):
        ram_range = bl.target.memoryRange["ram"]
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_RAMStartAddress)
        assert status == bootloader.status.kStatus_Success or \
               status == bootloader.status.kStatus_UnknownProperty
  
        if status == bootloader.status.kStatus_Success: 
            assert results[0] == ram_range.start
 
 
    def test_ram_size_in_bytes(self, bl):
        ram_range = bl.target.memoryRange["ram"]
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_RAMSizeInBytes)
        assert status == bootloader.status.kStatus_Success or \
               status == bootloader.status.kStatus_UnknownProperty
        
        if status == bootloader.status.kStatus_Success:  
            assert results[0] == ram_range.length
 
 
    def test_system_device_id(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_SystemDeviceIdent)
        assert status == bootloader.status.kStatus_Success
        assert common_util.isSystemIdValid(results[0], bl.target.systemDeviceId)
 
 
    def test_flash_security_state(self, bl):
 
        # below codes only applies for chips with boot rom.
        if bl.target.bootFrom == bootsources.kBootROM:
            status, results = bl.flashEraseAllUnsecure()
            assert status == bootloader.status.kStatus_Success
            
            status, results = bl.reset()
            assert status == bootloader.status.kStatus_Success

            shared_utils.timeSleepManager(bl, 'command')
            shared_utils.timeSleepManager(bl, 'command')

 
            status, results = bl.getProperty(bootloader.properties.kPropertyTag_FlashSecurityState)
            assert status == bootloader.status.kStatus_Success
            # security bit is disabled
            assert results[0] == 0
 
            status, results = bl.flashEraseAll()
            assert status == bootloader.status.kStatus_Success
            
            
            status, results = bl.reset()
            assert status == bootloader.status.kStatus_Success

            shared_utils.timeSleepManager(bl, 'command')
            shared_utils.timeSleepManager(bl, 'command')

 
            status, results = bl.getProperty(bootloader.properties.kPropertyTag_FlashSecurityState)
            assert status == bootloader.status.kStatus_Success
            # security bit is enabled
            assert results[0] == 1
             
            # Recover unsecure state for flash to avoid the dialog box pop-up, which will be caused by next setup()
            status, results = bl.flashEraseAllUnsecure()
            assert status == bootloader.status.kStatus_Success
            
            # Overlap user config area if needed.
            if common_util.needTestClockConfig():
                if bl.target.bootFrom == bootsources.kBootROM:
                    common_util.configCoreClock(bl) 
 
        else:
            status, results = bl.getProperty(bootloader.properties.kPropertyTag_FlashSecurityState)
            assert status == bootloader.status.kStatus_Success
            assert results[0] == 0 or results[0] == 1

    def test_unique_device_id(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_UniqueDeviceIdent)
        # Note: Not all targets support this property
        assert status == bootloader.status.kStatus_Success or status == bootloader.status.kStatus_UnknownProperty
        if status == bootloader.status.kStatus_Success:
            # As unique ID property is special for each chip, so we cannot verify UID value.  
            pass
        else:
            pytest.skip("This property is not supported by current target.")  

    def test_program_flash_read_margin_level(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_FlashReadMargin)
        # Note: Not all targets support this property
        assert status == bootloader.status.kStatus_Success or status == bootloader.status.kStatus_UnknownProperty
        if status == bootloader.status.kStatus_Success:
            # Default margin level is set to 1 (user)
            assert results[0] == 1
        else:
            pytest.skip("This property is not supported by current target.")

    def test_invalid_property(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_Invalid)
        assert status == bootloader.status.kStatus_UnknownProperty


