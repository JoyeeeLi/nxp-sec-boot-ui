#! /usr/bin/env python
import wx
import sys
import os
from run import runcore
from ui import uidef

class secBootMain(runcore.secBootRun):

    def __init__(self, parent):
        runcore.secBootRun.__init__(self, parent)

        self.connectStage = uidef.kConnectStage_Rom

    def callbackBootDeviceConfiguration( self, event ):
        self.updateTargetSetupValue()
        self.runBootDeviceConfiguration()

    def callbackSetUartPort( self, event ):
        self.setPortSetupValue(self.connectStage)

    def callbackSetUsbhidPort( self, event ):
        self.updateTargetSetupValue()
        usbIdList = self.getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList)

    def callbackConnectToDevice( self, event ):
        self.printLog("'Connect to xxx' button is clicked")
        self.updateTargetSetupValue()
        self.updatePortSetupValue()
        if self.connectStage == uidef.kConnectStage_Rom:
            self.connectToDevice(self.connectStage)
            if self.pingRom():
                self.getDeviceStatusViaRom()
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
            if self.pingFlashloader():
                self.getDeviceStatusViaFlashloader()
                self.updateConnectStatus('green')
                self.connectStage = uidef.kConnectStage_ExternalMemory
            else:
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('red')
        elif self.connectStage == uidef.kConnectStage_ExternalMemory:
            # To-Do
            self.connectStage = uidef.kConnectStage_Reset
            self.updateConnectStatus('blue')
            pass
        elif self.connectStage == uidef.kConnectStage_Reset:
            self.resetMcuDevice()
            self.connectStage = uidef.kConnectStage_Rom
            self.updateConnectStatus('black')
            usbIdList = self.getUsbid()
            self.adjustPortSetupValue(self.connectStage, usbIdList)
            self.connectToDevice(self.connectStage)
        else:
            pass

    def callbackSetSecureBootType( self, event ):
        self.setSecureBootSeqColor()

    def callbackSetKeyStorageRegion( self, event ):
        self.setKeyStorageRegionColor()

    def callbackGenImage( self, event ):
        self.printLog("'Generate Bootable Image' button is clicked")
        self.updateTargetSetupValue()
        if self.createMatchedBdfile():
            self.genBootableImage()

    def callbackFlashImage( self, event ):
        self.printLog("'Load Bootable Image' button is clicked")
        self.flashBootableImage()

    def callbackClearLog( self, event ):
        self.clearLog()

if __name__ == '__main__':
    app = wx.App()

    main_win = secBootMain(None)
    main_win.SetTitle(u"nxpSecBoot v0.2.0")
    main_win.Show()

    app.MainLoop()
