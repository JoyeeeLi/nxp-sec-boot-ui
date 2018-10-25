#! /usr/bin/env python
import sys
import os
import rundef
sys.path.append(os.path.abspath(".."))
from ui import uicore
from ui import uidef
from boot import bltest
from boot import target

def createTarget(device):
    # Build path to target directory and config file.
    if device == uidef.MCU_DEVICE_iMXRT102x:
        cpu = "MIMXRT1021"
    else:
        pass
    targetBaseDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'targets', cpu)
    targetConfigFile = os.path.join(targetBaseDir, 'bltargetconfig.py')

    # Check for existing target directory.
    if not os.path.isdir(targetBaseDir):
        raise ValueError("Missing target directory at path %s" % targetBaseDir)

    # Check for config file existence.
    if not os.path.isfile(targetConfigFile):
        raise RuntimeError("Missing target config file at path %s" % targetConfigFile)

    # Build locals dict by copying our locals and adjusting file path and name.
    targetConfig = locals().copy()
    targetConfig['__file__'] = targetConfigFile
    targetConfig['__name__'] = 'bltargetconfig'

    # Execute the target config script.
    execfile(targetConfigFile, globals(), targetConfig)

    # Create the target object.
    tgt = target.Target(**targetConfig)

    return tgt

##
# @brief
class secBootRun(uicore.secBootUi):

    def __init__(self, parent):
        uicore.secBootUi.__init__(self, parent)
        self.blhost = None
        self.sdphost = None

    def connectToDevice( self , connectStage):
        # Create the target object.
        tgt = createTarget(self.mcuDevice)

        vectorsDir = os.path.join(os.path.dirname(__file__), 'working', 'vectors')

        if connectStage == uidef.CONNECT_STAGE_ROM:
            if self.isUartPortSelected:
                sdpPeripheral = 'sdp_uart'
                uartComPort = self.uartComPort
                uartBaudrate = int(self.uartBaudrate)
            elif self.isUsbhidPortSelected:
                sdpPeripheral = 'sdp_usb'
                uartComPort = ''
                uartBaudrate = ''
            else:
                pass
            self.sdphost = bltest.createBootloader(tgt,
                                                   vectorsDir,
                                                   sdpPeripheral,
                                                   uartBaudrate, uartComPort,
                                                   rundef.SDPHOST_USBHID_VID[0],
                                                   rundef.SDPHOST_USBHID_PID[0])
        elif connectStage == uidef.CONNECT_STAGE_FLASHLOADER:
            if self.isUartPortSelected:
                blPeripheral = 'uart'
                uartComPort = self.uartComPort
                uartBaudrate = int(self.uartBaudrate)
            elif self.isUsbhidPortSelected:
                blPeripheral = 'usb'
                uartComPort = ''
                uartBaudrate = ''
            else:
                pass
            self.blhost = bltest.createBootloader(tgt,
                                                  vectorsDir,
                                                  blPeripheral,
                                                  uartBaudrate, uartComPort,
                                                  rundef.BLHOST_USBHID_VID[0],
                                                  rundef.BLHOST_USBHID_PID[0],
                                                  True)
        elif connectStage == uidef.CONNECT_STAGE_EXTERNAL_MEMORY:
            pass


