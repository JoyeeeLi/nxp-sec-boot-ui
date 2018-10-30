#! /usr/bin/env python
import sys
import os
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import gencore
from info import infodef
from ui import uidef
from boot import bltest
from boot import target

def createTarget(device):
    # Build path to target directory and config file.
    if device == uidef.kMcuDevice_iMXRT102x:
        cpu = "MIMXRT1021"
    elif device == uidef.kMcuDevice_iMXRT105x:
        cpu = "MIMXRT1052"
    elif device == uidef.kMcuDevice_iMXRT106x:
        cpu = "MIMXRT1062"
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
class secBootRun(gencore.secBootGen):

    def __init__(self, parent):
        gencore.secBootGen.__init__(self, parent)
        self.blhost = None
        self.sdphost = None
        self.tgt = None
        self.sdphostVectorsDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'sdphost', 'win', 'vectors')
        self.blhostVectorsDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'blhost', 'win', 'vectors')

    def getUsbid( self ):
        # Create the target object.
        tgt = createTarget(self.mcuDevice)
        return [tgt.romUsbVid, tgt.romUsbPid, tgt.flashloaderUsbVid, tgt.flashloaderUsbPid]

    def connectToDevice( self , connectStage):
        # Create the target object.
        if self.tgt == None:
            self.tgt = createTarget(self.mcuDevice)

        if connectStage == uidef.kConnectStage_Rom:
            if self.isUartPortSelected:
                sdpPeripheral = 'sdp_uart'
                uartComPort = self.uartComPort
                uartBaudrate = int(self.uartBaudrate)
                usbVid = ''
                usbPid = ''
            elif self.isUsbhidPortSelected:
                sdpPeripheral = 'sdp_usb'
                uartComPort = ''
                uartBaudrate = ''
                usbVid = self.tgt.romUsbVid
                usbPid = self.tgt.romUsbPid
            else:
                pass
            self.sdphost = bltest.createBootloader(self.tgt,
                                                   self.sdphostVectorsDir,
                                                   sdpPeripheral,
                                                   uartBaudrate, uartComPort,
                                                   usbVid, usbPid)
        elif connectStage == uidef.kConnectStage_Flashloader:
            if self.isUartPortSelected:
                blPeripheral = 'uart'
                uartComPort = self.uartComPort
                uartBaudrate = int(self.uartBaudrate)
                usbVid = ''
                usbPid = ''
            elif self.isUsbhidPortSelected:
                blPeripheral = 'usb'
                uartComPort = ''
                uartBaudrate = ''
                usbVid = self.tgt.flashloaderUsbVid
                usbPid = self.tgt.flashloaderUsbPid
            else:
                pass
            self.blhost = bltest.createBootloader(self.tgt,
                                                  self.blhostVectorsDir,
                                                  blPeripheral,
                                                  uartBaudrate, uartComPort,
                                                  usbVid, usbPid,
                                                  True)
        elif connectStage == uidef.kConnectStage_Reset:
            self.tgt = None
        else:
            pass

    def pingRom( self ):
        status, results, cmdStr = self.sdphost.errorStatus()
        self.printLog(cmdStr)
        return (status == boot.status.kSDP_Status_HabEnabled or status == boot.status.kSDP_Status_HabDisabled)

    def _getDeviceRegisterBySdphost( self, regAddr, regName):
        filename = 'readReg.dat'
        filepath = os.path.join(self.sdphostVectorsDir, filename)
        status, results, cmdStr = self.sdphost.readRegister(regAddr, 32, 4, filename)
        self.printLog(cmdStr)
        if (status == boot.status.kSDP_Status_HabEnabled or status == boot.status.kSDP_Status_HabDisabled):
            regVal = self.getReg32FromBinFile(filepath)
            self.printDeviceStatus(regName + " = " + str(regVal))
        else:
            self.printDeviceStatus(regName + " = --------")
        try:
            os.remove(filepath)
        except:
            pass

    def getDeviceStatusViaRom( self ):
        self._getDeviceRegisterBySdphost( infodef.kRegisterAddr_SRC_SBMR1, 'SRC->SMBR1')
        self._getDeviceRegisterBySdphost( infodef.kRegisterAddr_SRC_SBMR2, 'SRC->SMBR2')

    def jumpToFlashloader( self ):
        if self.mcuDevice == uidef.kMcuDevice_iMXRT102x:
            cpu = "MIMXRT1021"
            loadAddr = 0x20208000
            jumpAddr = 0x20208400
        elif self.mcuDevice == uidef.kMcuDevice_iMXRT105x:
            cpu = "MIMXRT1052"
            loadAddr = 0x20000000
            jumpAddr = 0x20000400
        elif self.mcuDevice == uidef.kMcuDevice_iMXRT106x:
            cpu = "MIMXRT1062"
            loadAddr = 0x20000000
            jumpAddr = 0x20000400
        else:
            pass
        flashloaderBinFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'targets', cpu, 'ivt_flashloader.bin')
        status, results, cmdStr = self.sdphost.writeFile(loadAddr, flashloaderBinFile)
        self.printLog(cmdStr)
        if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
            return False
        status, results, cmdStr = self.sdphost.jumpAddress(jumpAddr)
        self.printLog(cmdStr)
        if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
            return False
        return True

    def pingFlashloader( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def _getDeviceFuseByBlhost( self, fuseIndex, fuseName):
        status, results, cmdStr = self.blhost.efuseReadOnce(fuseIndex)
        self.printLog(cmdStr)
        if (status == boot.status.kStatus_Success):
            self.printDeviceStatus(fuseName + " = " + str(hex(results[1])))
        else:
            self.printDeviceStatus(fuseName + " = --------")

    def getDeviceStatusViaFlashloader( self ):
        self._getDeviceFuseByBlhost(infodef.kEfuseAddr_BOOT_CFG0, 'Fuse->BOOT_CFG (0x450)')
        self._getDeviceFuseByBlhost(infodef.kEfuseAddr_BOOT_CFG1, 'Fuse->BOOT_CFG (0x460)')
        self._getDeviceFuseByBlhost(infodef.kEfuseAddr_BOOT_CFG2, 'Fuse->BOOT_CFG (0x470)')


    def resetMcuDevice( self ):
        status, results, cmdStr = self.blhost.reset()
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)
