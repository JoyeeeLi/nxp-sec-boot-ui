#! /usr/bin/env python

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

import os
import exceptions

from collections import namedtuple


# User config tag constants
kUserConfig_Tag = 0x01
kUserConfig_CrcStartAddress = 0x02
kUserConfig_CrcByteCount = 0x03
kUserConfig_CrcExpectedValue = 0x04
kUserConfig_EnabledPeripherals = 0x05
kUserConfig_I2cSlaveAddress = 0x06
kUserConfig_PeripheralDetectionTimeout = 0x07
kUserConfig_UsbVid = 0x08
kUserConfig_UsbPid = 0x09
kUserConfig_UsbStringsPointer = 0x0A
kUserConfig_ClockFlags = 0x0B
kUserConfig_ClockDivider = 0x0C

kUserConfig_BootFlags = 0x0D
kUserConfig_Pad0 = 0x0E
kUserConfig_MmcauConfigPointer = 0x0F
kUserConfig_KeyBlobPointer = 0x10

kUserConfig_Pad1 = 0x11
kUserConfig_CanConfig1 = 0x12
kUserConfig_CanConfig2 = 0x13
kUserConfig_CanTxId = 0x14
kUserConfig_CanRxId = 0x15

kUserConfig_QspiConfigBlockPointer = 0x16


UserConfigItem = namedtuple('UserConfigItem', 'tag, size')

UserConfigItems = {
                  
    kUserConfig_Tag                         : UserConfigItem(kUserConfig_Tag, 4),
    kUserConfig_CrcStartAddress             : UserConfigItem(kUserConfig_CrcStartAddress,4),
    kUserConfig_CrcByteCount                : UserConfigItem(kUserConfig_CrcByteCount, 4),
    kUserConfig_CrcExpectedValue            : UserConfigItem(kUserConfig_CrcExpectedValue, 4),
    kUserConfig_EnabledPeripherals          : UserConfigItem(kUserConfig_EnabledPeripherals, 1),
    kUserConfig_I2cSlaveAddress             : UserConfigItem(kUserConfig_I2cSlaveAddress, 1),
    kUserConfig_PeripheralDetectionTimeout  : UserConfigItem(kUserConfig_PeripheralDetectionTimeout, 2),
    kUserConfig_UsbVid                      : UserConfigItem(kUserConfig_UsbVid, 2),
    kUserConfig_UsbPid                      : UserConfigItem(kUserConfig_UsbPid, 2), 
    kUserConfig_UsbStringsPointer           : UserConfigItem(kUserConfig_UsbStringsPointer, 4),
    kUserConfig_ClockFlags                  : UserConfigItem(kUserConfig_ClockFlags, 1),
    kUserConfig_ClockDivider                : UserConfigItem(kUserConfig_ClockDivider, 1),
    kUserConfig_BootFlags                   : UserConfigItem(kUserConfig_BootFlags, 1),
    kUserConfig_Pad0                        : UserConfigItem(kUserConfig_Pad0, 1),
    kUserConfig_MmcauConfigPointer          : UserConfigItem(kUserConfig_MmcauConfigPointer, 4),
    kUserConfig_KeyBlobPointer              : UserConfigItem(kUserConfig_KeyBlobPointer, 4),
    kUserConfig_Pad1                        : UserConfigItem(kUserConfig_Pad1, 1),
    kUserConfig_CanConfig1                  : UserConfigItem(kUserConfig_CanConfig1, 1),
    kUserConfig_CanConfig2                  : UserConfigItem(kUserConfig_CanConfig2, 2),
    kUserConfig_CanTxId                     : UserConfigItem(kUserConfig_CanTxId, 2),
    kUserConfig_CanRxId                     : UserConfigItem(kUserConfig_CanRxId, 2),
    kUserConfig_QspiConfigBlockPointer      : UserConfigItem(kUserConfig_QspiConfigBlockPointer, 4),
                  }


def FOUR_CHAR_CODE(a,b,c,d):
    return ((ord(d) << 24) | (ord(c) << 16) | (ord(b) << 8) | (ord(a)))


# @brief Generate an invalid integer according to length
def INVALID_VALUE(length):
    value = 0
    for i in range(0, length):
        value = value << 8
        value = value | 0xFF
    return value


kUserConfigTag = FOUR_CHAR_CODE('k', 'c', 'f', 'g')
kInvalidValue8  = INVALID_VALUE(1)
kInvalidValue16 = INVALID_VALUE(2)
kInvalidValue32 = INVALID_VALUE(4) 




class UserConfig(object):
    def __init__(self, tag = kUserConfigTag, crcStartAddress = kInvalidValue32, 
                 crcByteCount=kInvalidValue32, crcExpectedValue=kInvalidValue32,
                 enabledPeripherals = kInvalidValue8, i2cSlaveAddress = kInvalidValue8,
                 peripheralDetectionTimeout = kInvalidValue16,
                 usbVid = kInvalidValue16, usbPid = kInvalidValue16, usbStringsPointer = kInvalidValue32,
                 clockFlags = kInvalidValue8, clockDivider = kInvalidValue8,
                 _reserved0 = kInvalidValue16, 
                 applicationEntryPoint = kInvalidValue32, applicationStackPointer = kInvalidValue32,
                 bootFlags = kInvalidValue8,
                 pad0 = kInvalidValue8,
                 mmcauConfigPointer = kInvalidValue32,
                 keyBlobPointer = kInvalidValue32,
                 pad1 = kInvalidValue8,
                 canConfig1 = kInvalidValue8,
                 canConfig2 = kInvalidValue16,
                 canTxId = kInvalidValue16,
                 canRxId = kInvalidValue16,
                 qspiConfigBlockPointer = kInvalidValue32
                 ):
        self.tag = tag
        self.crcStartAddress = crcStartAddress
        self.crcByteCount = crcByteCount
        self.crcExpectedValue = crcExpectedValue
        self.enabledPeripherals = enabledPeripherals
        self.i2cSlaveAddress = i2cSlaveAddress
        self.peripheralDetectionTimeout = peripheralDetectionTimeout
        self.usbVid = usbVid
        self.usbPid = usbPid
        self.usbStringsPointer = usbStringsPointer
        self.clockFlags = clockFlags
        self.clockDivider = clockDivider
        self.bootFlags = bootFlags
        self.pad0 = pad0
        self.mmcauConfigPointer = mmcauConfigPointer
        self.keyBlobPointer = keyBlobPointer
        self.pad1 = pad1
        self.canConfig1 = canConfig1
        self.canConfig2 = canConfig2
        self.canTxId = canTxId
        self.canRxId = canRxId
        self.qspiConfigBlockPointer = qspiConfigBlockPointer
        
    # @brief return the size of the Bootloader Configuration Area
    @staticmethod
    def size():
        size = 0
        for userConfigItem in UserConfigItems.values():
            size += userConfigItem.size 
            
        return size   
    
    # @brief Convert a number to a little-endian byte array,
    # Note: maximum value of size should be less than or equal to 4
    def _getByteArrayFromData(self, data, size):
        expectedByteArray = bytearray(size)
        offset = 0
        while data > 0:
            expectedByteArray[offset] = data & 0xff
            data = data>>8
            offset = offset+1
        
        return expectedByteArray
    
    def _fillContent(self, dstArray, data, size):
        dataArray = self._getByteArrayFromData(data, size)
        
        for number in dataArray:
            dstArray.append(number)

    
    # Generate expected user config data
    # Note: !please don't change sequence of below codes!
    def _getUserConfigByteArray(self):
        
       content = bytearray()
       
       # fill content with config data
       # fill tag
       itemSize = UserConfigItems[kUserConfig_Tag].size
       self._fillContent(content, self.tag, itemSize)
       
       # fill crcStartAddress
       itemSize = UserConfigItems[kUserConfig_CrcStartAddress].size
       self._fillContent(content, self.crcStartAddress, itemSize)
       
       # fill crcByteCount
       itemSize = UserConfigItems[kUserConfig_CrcByteCount].size
       self._fillContent(content, self.crcByteCount, itemSize)
       
       # fill crcExpectedValue
       itemSize = UserConfigItems[kUserConfig_CrcExpectedValue].size
       self._fillContent(content, self.crcExpectedValue, itemSize)
       
       # fill enabledPeripherals
       itemSize = UserConfigItems[kUserConfig_EnabledPeripherals].size
       self._fillContent(content, self.enabledPeripherals, itemSize)
       
       # fill i2cSlaveAddress
       itemSize = UserConfigItems[kUserConfig_I2cSlaveAddress].size
       self._fillContent(content, self.i2cSlaveAddress, itemSize)
       
       # fill peripheralDetectionTimeout
       itemSize = UserConfigItems[kUserConfig_PeripheralDetectionTimeout].size
       self._fillContent(content, self.peripheralDetectionTimeout, itemSize)

       # fill usbVid
       itemSize = UserConfigItems[kUserConfig_UsbVid].size
       self._fillContent(content, self.usbVid, itemSize)
       
       # fill usbPid
       itemSize = UserConfigItems[kUserConfig_UsbPid].size
       self._fillContent(content, self.usbPid, itemSize)
       
       # fill usbStringsPointer
       itemSize = UserConfigItems[kUserConfig_UsbStringsPointer].size
       self._fillContent(content, self.usbStringsPointer, itemSize)
       
       # fill clockFlags
       itemSize = UserConfigItems[kUserConfig_ClockFlags].size
       self._fillContent(content, self.clockFlags, itemSize)
       
       # fill clockDivider
       itemSize = UserConfigItems[kUserConfig_ClockDivider].size
       self._fillContent(content, self.clockDivider, itemSize)
       
       # fill bootFlags
       itemSize = UserConfigItems[kUserConfig_BootFlags].size
       self._fillContent(content, self.bootFlags, itemSize)
       
       # fill pad0
       itemSize = UserConfigItems[kUserConfig_Pad0].size
       self._fillContent(content, self.pad0, itemSize)
       
       # fill mmcauConfigPointer
       itemSize = UserConfigItems[kUserConfig_MmcauConfigPointer].size
       self._fillContent(content, self.mmcauConfigPointer, itemSize)
       
       # fill keyBlobPointer
       itemSize = UserConfigItems[kUserConfig_KeyBlobPointer].size
       self._fillContent(content, self.keyBlobPointer, itemSize)
       
       # fill pad1
       itemSize = UserConfigItems[kUserConfig_Pad1].size
       self._fillContent(content, self.pad1, itemSize)
       
       # fill canConfig1
       itemSize = UserConfigItems[kUserConfig_CanConfig1].size
       self._fillContent(content, self.canConfig1, itemSize)
       
       # fill canConfig2
       itemSize = UserConfigItems[kUserConfig_CanConfig2].size
       self._fillContent(content, self.canConfig2, itemSize)
       
       # fill canTxId
       itemSize = UserConfigItems[kUserConfig_CanTxId].size
       self._fillContent(content, self.canTxId, itemSize)
       
       # fill canRxId
       itemSize = UserConfigItems[kUserConfig_CanRxId].size
       self._fillContent(content, self.canRxId, itemSize)      
       
       # file qspiConfigBlockPointer
       itemSize = UserConfigItems[kUserConfig_QspiConfigBlockPointer].size
       self._fillContent(content, self.qspiConfigBlockPointer, itemSize) 
       
       return content
    
    
    # @brief Create expected user config file
    def createUserConfigDataFile(self, path):
        expectedByteArray = self._getUserConfigByteArray()
        
        if os.path.exists(path):
            try:
                # If a file is occupied by other process, we may not be able to remove it
                os.remove(path)
            except Exception, e:
                pass
        
        with open(path, 'w') as file:
            file.write(expectedByteArray)
            file.close()


# if __name__ == '__main__':
#      userConfig = UserConfig(i2cSlaveAddress = 0x40)
#      userConfig.createUserConfigDataFile('D:\\')         
            
        
            
        
