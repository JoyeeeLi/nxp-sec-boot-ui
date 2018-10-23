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
import conftest
sys.path.append(os.path.abspath("../boot"))
from fsl import bootloader
from fsl.bootloader import properties

##
# @brief Test the bootloader get property command.
class TestGetProperty(object):

    def test_version(self, bl):
        status, results = bl.getProperty(bootloader.properties.kPropertyTag_CurrentVersion)
        if status == bootloader.status.kStatus_Success:
            print 'CMD Status Success'
        # Test for version 1.0.0 or version 1.1.0 or version 1.2.0
        if (results[0] == properties.kBootloaderVersion_1_0_0) or \
            (results[0] == properties.kBootloaderVersion_1_1_0) or \
            (results[0] == properties.kBootloaderVersion_1_1_1) or \
            (results[0] == properties.kBootloaderVersion_1_2_0) or \
            (results[0] == properties.kBootloaderVersion_1_3_0) or \
            (results[0] == properties.kBootloaderVersion_1_4_0) or \
            (results[0] == properties.kBootloaderVersion_1_4_1) or \
            (results[0] == properties.kBootloaderVersion_1_5_0) or \
            (results[0] == properties.kBootloaderVersion_1_5_1) or \
            (results[0] == properties.kBootloaderVersion_2_0_0) or \
            (results[0] == properties.kBootloaderVersion_2_1_0):
            print 'CMD Result Success'

if __name__ == '__main__':
    myGetProperty = TestGetProperty()
    tgt = conftest.tgt()
    myGetProperty.test_version(tgt)

