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

    def callbackSetSecureBootType( self, event ):
        self.setSecureBootSeqColor()

    def callbackSetKeyStorageRegion( self, event ):
        self.setKeyStorageRegionColor()

    def callbackSetUartPort( self, event ):
        self.updateTargetSetupValue()
        usbIdList = self.getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList)

    def callbackSetUsbhidPort( self, event ):
        self.updateTargetSetupValue()
        usbIdList = self.getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList)

    def callbackConnectToDevice( self, event ):
        self.m_textCtrl_log.write("'Connect' button is clicked\n")
        self.updateTargetSetupValue()
        self.updatePortSetupValue()
        self.connectToDevice(self.connectStage)
        if self.connectStage == uidef.kConnectStage_Rom:
            if self.pingRom() and self.jumpToFlashloader():
                self.updateConnectStatus('yellow')
                self.connectStage = uidef.kConnectStage_Flashloader
                usbIdList = self.getUsbid()
                self.adjustPortSetupValue(self.connectStage, usbIdList)
            else:
                self.updateConnectStatus('red')
        elif self.connectStage == uidef.kConnectStage_Flashloader:
            if self.pingFlashloader():
                self.updateConnectStatus('green')
                self.connectStage = uidef.kConnectStage_ExternalMemory
            else:
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('red')
        elif self.connectStage == uidef.kConnectStage_ExternalMemory:
            self.connectStage = uidef.kConnectStage_Reset
            self.updateConnectStatus('blue')
            pass
        elif self.connectStage == uidef.kConnectStage_Reset:
            self.resetMcuDevice()
            self.connectStage = uidef.kConnectStage_Rom
            self.updateConnectStatus('black')
            usbIdList = self.getUsbid()
            self.adjustPortSetupValue(self.connectStage, usbIdList)
        else:
            pass

if __name__ == '__main__':
    app = wx.App()

    main_win = secBootMain(None)
    main_win.SetTitle(u"nxpSecBoot v0.1.0")
    main_win.Show()

    app.MainLoop()
