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

from collections import namedtuple

##
# @brief Supported bootloader peripherals.
kPeripheral_Sim  = 'sim'
kPeripheral_UART = 'uart'
kPeripheral_I2C  = 'i2c'
kPeripheral_SPI  = 'spi'
kPeripheral_USB  = 'usb'
kPeripheral_CAN  = 'can'

##
# @brief Supported SDP peripherals.
kPeripheral_SDP_UART = 'sdp_uart'
kPeripheral_SDP_USB = 'sdp_usb'

Peripherals = [kPeripheral_Sim, kPeripheral_UART, kPeripheral_I2C, kPeripheral_SPI, kPeripheral_USB, kPeripheral_CAN]
PeripheralsSDP = [kPeripheral_SDP_UART, kPeripheral_SDP_USB]

PeripheralMask = namedtuple('PeripheralMask', 'name, propertyMask')

PeripheralMasks = {
    kPeripheral_Sim         : PeripheralMask(kPeripheral_Sim,         0x00),
    kPeripheral_UART        : PeripheralMask(kPeripheral_UART,        0x01),
    kPeripheral_I2C         : PeripheralMask(kPeripheral_I2C,         0x02),
    kPeripheral_SPI         : PeripheralMask(kPeripheral_SPI,         0x04),
    kPeripheral_USB         : PeripheralMask(kPeripheral_USB,         0x10),
    kPeripheral_CAN         : PeripheralMask(kPeripheral_CAN,         0x20)
}

