#! /usr/bin/env python

# Copyright (c) 2016 Freescale Semiconductor, Inc.
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

TEMP_FILE_INDEX = 0
kReadFileName   = 'sdp_read-register_rfile'

##
# @brief Test the SDP read-register command.
class TestReadRegister:
    @pytest.fixture(autouse=True)
    def setup(self, bl, request):
        bl.target.reset()
        shared_utils.timeSleepManager(bl, 'customized')

    @pytest.mark.parametrize(("format", "requestedBytes"), [
            ## Test Cases for RAM:    
                ## 1. Read 8-bit RAM location for various number of bytes
                (8,    1),
                (8,    2),
                (8,    3),
                (8,    4),
                (8,    5),
                (8,    64),
                (8,    65),
                ## 1. Read 16-bit RAM location for various number of bytes
                (16,    1),
                (16,    2),
                (16,    3),
                (16,    4),
                (16,    5),
                (16,    64),
                (16,    65),
                ## 1. Read 32-bit RAM location for various number of bytes
                (32,    1),
                (32,    2),
                (32,    3),
                (32,    4),
                (32,    5),
                (32,    64),
                (32,    65),
                ])  
    def test_read_ram_xFormat_xNumbytes(self, bl, format, requestedBytes):
        global TEMP_FILE_INDEX                       
        readFilePath = os.path.abspath(os.path.join(bl.vectorsDir, kReadFileName+str(TEMP_FILE_INDEX)+'.dat'))
        # Create independent temp file for every test to reduce file-handling issue.
        TEMP_FILE_INDEX += 1
        
        memoryRange = bl.target.memoryRange['ram']
        address = memoryRange.start     
        status, results = bl.readRegister(address, format, requestedBytes, readFilePath)
        assert status == bootloader.status.kSDP_Status_HabEnabled or status == bootloader.status.kSDP_Status_HabDisabled
        # Just check the number of bytes returned, not the values.
        assert os.path.getsize(readFilePath) == requestedBytes

