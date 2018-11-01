#! /usr/bin/env python
import sys
import os
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import gencore
from info import infodef
from ui import uidef
from ui import uivar
from boot import bltest
from boot import target
from utils import misc

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

        self.bootDeviceMemId = None
        self.bootDeviceMemBase = None
        self.semcNandImageCopies = None
        self.semcNandBlockSize = None

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

    def getMcuDeviceInfoViaRom( self ):
        self._getDeviceRegisterBySdphost( infodef.kRegisterAddr_UUID1, 'UUID[31:00]')
        self._getDeviceRegisterBySdphost( infodef.kRegisterAddr_UUID2, 'UUID[63:32]')
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

    def getMcuDeviceInfoViaFlashloader( self ):
        self._getDeviceFuseByBlhost(infodef.kEfuseAddr_BOOT_CFG0, 'Fuse->BOOT_CFG (0x450)')
        self._getDeviceFuseByBlhost(infodef.kEfuseAddr_BOOT_CFG1, 'Fuse->BOOT_CFG (0x460)')
        self._getDeviceFuseByBlhost(infodef.kEfuseAddr_BOOT_CFG2, 'Fuse->BOOT_CFG (0x470)')

    def _getBootDeviceMemoryInfo ( self ):
        if self.bootDevice == uidef.kBootDevice_FlexspiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_FlexspiNor
            self.bootDeviceMemBase = rundef.kBootDeviceMemBase_FlexspiNor
        elif self.bootDevice == uidef.kBootDevice_FlexspiNand:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_FlexspiNand
            self.bootDeviceMemBase = rundef.kBootDeviceMemBase_FlexspiNand
        elif self.bootDevice == uidef.kBootDevice_SemcNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_SemcNor
            self.bootDeviceMemBase = rundef.kBootDeviceMemBase_SemcNor
        elif self.bootDevice == uidef.kBootDevice_SemcNand:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_SemcNand
            self.bootDeviceMemBase = rundef.kBootDeviceMemBase_SemcNand
        elif self.bootDevice == uidef.kBootDevice_UsdhcSd:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_UsdhcSd
            self.bootDeviceMemBase = rundef.kBootDeviceMemBase_UsdhcSd
        elif self.bootDevice == uidef.kBootDevice_UsdhcMmc:
            self.bootDeviceMemId = rundef.kBootDevice_UsdhcMmc
            self.bootDeviceMemBase = rundef.kBootDeviceMemBase_UsdhcMmc
        elif self.bootDevice == uidef.kBootDevice_LpspiNor:
            self.bootDeviceMemId = rundef.kBootDevice_LpspiNor
            self.bootDeviceMemBase = rundef.kBootDeviceMemBase_LpspiNor
        else:
            pass

    def _getSemcNandDeviceInfo ( self ):
        filename = 'semcNandFcb.dat'
        filepath = os.path.join(self.blhostVectorsDir, filename)
        status, results, cmdStr = self.blhost.readMemory(self.bootDeviceMemBase + infodef.kSemcNandFcbInfo_StartAddr, infodef.kSemcNandFcbInfo_Length, filename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        fingerprint = self.getVal32FromBinFile(filepath, infodef.kSemcNandFcbOffset_Fingerprint)
        semcTag = self.getVal32FromBinFile(filepath, infodef.kSemcNandFcbOffset_SemcTag)
        if fingerprint == infodef.kSemcNandFcbTag_Fingerprint and semcTag == infodef.kSemcNandFcbTag_Semc:
            firmwareCopies = self.getVal32FromBinFile(filepath, infodef.kSemcNandFcbOffset_FirmwareCopies)
            pageByteSize = self.getVal32FromBinFile(filepath, infodef.kSemcNandFcbOffset_PageByteSize)
            pagesInBlock = self.getVal32FromBinFile(filepath, infodef.kSemcNandFcbOffset_PagesInBlock)
            blocksInPlane = self.getVal32FromBinFile(filepath, infodef.kSemcNandFcbOffset_BlocksInPlane)
            planesInDevice = self.getVal32FromBinFile(filepath, infodef.kSemcNandFcbOffset_PlanesInDevice)
            self.printDeviceStatus("pageByteSize = " + str(hex(pageByteSize)))
            self.printDeviceStatus("pagesInBlock = " + str(hex(pagesInBlock)))
            self.printDeviceStatus("blocksInPlane = " + str(hex(blocksInPlane)))
            self.printDeviceStatus("planesInDevice = " + str(hex(planesInDevice)))
            self.semcNandImageCopies = firmwareCopies
            self.semcNandBlockSize = pageByteSize * pagesInBlock
        else:
            self.printDeviceStatus("pageByteSize = --------")
            self.printDeviceStatus("pagesInBlock = --------")
            self.printDeviceStatus("blocksInPlane = --------")
            self.printDeviceStatus("planesInDevice = --------")
            return False
        try:
            os.remove(filepath)
        except:
            pass
        return True

    def geBootDeviceInfoViaFlashloader ( self ):
        if self.bootDevice == uidef.kBootDevice_SemcNand:
            self._getSemcNandDeviceInfo()
        else:
            pass

    def configureBootDevice ( self ):
        self._getBootDeviceMemoryInfo()
        if self.bootDevice == uidef.kBootDevice_SemcNand:
            semcNandOpt, semcNandFcbOpt, semcNandImageInfo = uivar.getVar(self.bootDevice)
            status, results, cmdStr = self.blhost.fillMemory(rundef.kRamFreeSpaceStart_Flashloader, 0x4, semcNandOpt)
            self.printLog(cmdStr)
            if status != boot.status.kStatus_Success:
                return False
            status, results, cmdStr = self.blhost.fillMemory(rundef.kRamFreeSpaceStart_Flashloader + 4, 0x4, semcNandFcbOpt)
            self.printLog(cmdStr)
            if status != boot.status.kStatus_Success:
                return False
            for i in range(len(semcNandImageInfo)):
                if semcNandImageInfo[i] != None:
                    status, results, cmdStr = self.blhost.fillMemory(rundef.kRamFreeSpaceStart_Flashloader + 8 + i * 4, 0x4, semcNandImageInfo[i])
                    self.printLog(cmdStr)
                    if status != boot.status.kStatus_Success:
                        return False
                else:
                    break
            status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, rundef.kRamFreeSpaceStart_Flashloader)
            self.printLog(cmdStr)
            if status != boot.status.kStatus_Success:
                return False
        else:
            pass
        return True

    def flashBootableImage ( self ):
        self._getBootDeviceMemoryInfo()
        imageLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == uidef.kBootDevice_SemcNand:
            semcNandOpt, semcNandFcbOpt, imageInfo = uivar.getVar(self.bootDevice)
            memEraseLen = misc.align_up(imageLen, self.semcNandBlockSize)
            for i in range(self.semcNandImageCopies):
                imageLoadAddr = self.bootDeviceMemBase + (imageInfo[i] >> 16) * self.semcNandBlockSize
                status, results, cmdStr = self.blhost.flashEraseRegion(imageLoadAddr, memEraseLen, self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, self.destAppFilename, self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
        else:
            pass

    def resetMcuDevice( self ):
        status, results, cmdStr = self.blhost.reset()
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)
