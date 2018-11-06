#! /usr/bin/env python
import wx
import sys
import os
import time
from run import runcore
from ui import uidef

class secBootMain(runcore.secBootRun):

    def __init__(self, parent):
        runcore.secBootRun.__init__(self, parent)
        self.connectStage = uidef.kConnectStage_Rom

    def callbackSetMcuSeries( self, event ):
        self.setTargetSetupValue()

    def callbackSetMcuDevice( self, event ):
        self.setTargetSetupValue()
        usbIdList = self.getUsbid()
        self.adjustPortSetupValue(self.connectStage, usbIdList)

    def callbackSetBootDevice( self, event ):
        self.setTargetSetupValue()

    def callbackBootDeviceConfiguration( self, event ):
        self.runBootDeviceConfiguration()

    def callbackSetUartPort( self, event ):
        self.setPortSetupValue(self.connectStage)

    def callbackSetUsbhidPort( self, event ):
        usbIdList = self.getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList)

    def callbackConnectToDevice( self, event ):
        self.printLog("'Connect to xxx' button is clicked")
        connectSteps = uidef.kConnectStep_Normal
        self.getConnectSpeedMode()
        if self.isConnectSpeedMode and self.connectStage != uidef.kConnectStage_Reset:
            connectSteps = uidef.kConnectStep_Fast
        while connectSteps:
            self.updatePortSetupValue()
            if self.connectStage == uidef.kConnectStage_Rom:
                self.connectToDevice(self.connectStage)
                if self.pingRom():
                    self.getMcuDeviceInfoViaRom()
                    if self.jumpToFlashloader():
                        self.updateConnectStatus('yellow')
                        self.connectStage = uidef.kConnectStage_Flashloader
                        usbIdList = self.getUsbid()
                        self.adjustPortSetupValue(self.connectStage, usbIdList)
                    else:
                        self.updateConnectStatus('red')
                else:
                    self.updateConnectStatus('red')
            elif self.connectStage == uidef.kConnectStage_Flashloader:
                self.connectToDevice(self.connectStage)
                # A new USB device is being enumerated, we need to delay some time here
                if self.isUsbhidPortSelected and connectSteps > uidef.kConnectStep_Normal:
                    time.sleep(5)
                if self.pingFlashloader():
                    self.getMcuDeviceInfoViaFlashloader()
                    self.updateConnectStatus('green')
                    self.connectStage = uidef.kConnectStage_ExternalMemory
                else:
                    self.updateConnectStatus('red')
            elif self.connectStage == uidef.kConnectStage_ExternalMemory:
                if self.configureBootDevice():
                    self.getBootDeviceInfoViaFlashloader()
                    self.connectStage = uidef.kConnectStage_Reset
                    self.updateConnectStatus('blue')
                else:
                    self.updateConnectStatus('red')
            elif self.connectStage == uidef.kConnectStage_Reset:
                self.resetMcuDevice()
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('black')
                usbIdList = self.getUsbid()
                self.adjustPortSetupValue(self.connectStage, usbIdList)
                self.connectToDevice(self.connectStage)
            else:
                pass
            connectSteps -= 1

    def callbackSetSecureBootType( self, event ):
        self.setSecureBootSeqColor()

    def callbackAdvCertSettings( self, event ):
        self.runAdvancedCertSettings()
        self.updateAllCstPathToCorrectVersion()

    def callbackGenCert( self, event ):
        self.printLog("'Generate Certificate' button is clicked")
        self.updateAllCstPathToCorrectVersion()
        if self.createSerialAndKeypassfile():
            self.genCertificate()
            self.genSuperRootKeys()
            self.showSuperRootKeys()

    def callbackGenImage( self, event ):
        self.printLog("'Generate Bootable Image' button is clicked")
        if self.createMatchedBdfile():
            self.genBootableImage()
            self.showDekIfApplicable()

    def callbackSetKeyStorageRegion( self, event ):
        self.setKeyStorageRegionColor()

    def callbackAdvKeySettings( self, event ):
        self.runAdvancedKeySettings()

    def callbackProgramSrk( self, event ):
        self.printLog("'Load SRK data' button is clicked")
        self.burnSrkData()

    def callbackFlashImage( self, event ):
        self.printLog("'Load Bootable Image' button is clicked")
        self.flashBootableImage()

    def callbackFlashDek( self, event ):
        self.printLog("'Load KeyBlob Data' button is clicked")
        self.flashDekToGenerateKeyBlob()

    def callbackClearLog( self, event ):
        self.clearLog()

if __name__ == '__main__':
    app = wx.App()

    main_win = secBootMain(None)
    main_win.SetTitle(u"nxpSecBoot v0.3.0")
    main_win.Show()

    app.MainLoop()
