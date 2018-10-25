#! /usr/bin/env python
import wx
import sys
import os
from run import runcore
from ui import uidef

class secBootMain(runcore.secBootRun):

    def __init__(self, parent):
        runcore.secBootRun.__init__(self, parent)

        self.connectStage = uidef.CONNECT_STAGE_ROM

    def callbackSetSecureBootType( self, event ):
        self.setSecureBootSeqColor()

    def callbackSetKeyStorageRegion( self, event ):
        self.setKeyStorageRegionColor()

    def callbackSetUartPort( self, event ):
        self.setPortSetupValue(self.connectStage)

    def callbackSetUsbhidPort( self, event ):
        self.setPortSetupValue(self.connectStage)

    def callbackConnectToDevice( self, event ):
        self.m_textCtrl_log.write("[GUI Action]: 'Connect' button is clicked\n")
        self.updateTargetSetupValue()
        self.updatePortSetupValue()
        self.connectToDevice(self.connectStage)
        if self.connectStage == uidef.CONNECT_STAGE_ROM:
            status, results, cmdStr = self.sdphost.readRegister(0x401F46F0)
            self.m_textCtrl_log.write("[CMD Action]: " + cmdStr + "\n")

            self.connectStage = uidef.CONNECT_STAGE_FLASHLOADER
            self.adjustPortSetupValue(self.connectStage)
        elif self.connectStage == uidef.CONNECT_STAGE_FLASHLOADER:
            pass
        elif self.connectStage == uidef.CONNECT_STAGE_EXTERNAL_MEMORY:
            pass

if __name__ == '__main__':
    app = wx.App()

    main_win = secBootMain(None)
    main_win.SetTitle(u"nxpSecBoot v0.1.0")
    main_win.Show()

    app.MainLoop()
