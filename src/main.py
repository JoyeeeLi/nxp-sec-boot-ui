#! /usr/bin/env python
import wx
import sys
import os
from run import runcore
from ui import uidef
import boot

class secBootMain(runcore.secBootRun):

    def __init__(self, parent):
        runcore.secBootRun.__init__(self, parent)

        self.connectStage = uidef.kConnectStage_Rom

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
        if self.connectStage == uidef.kConnectStage_Rom:
            self.jumpToFlashloader()
            self.updateConnectStatus('yellow')
            self.connectStage = uidef.kConnectStage_Flashloader
            self.adjustPortSetupValue(self.connectStage)
        elif self.connectStage == uidef.kConnectStage_Flashloader:
            status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
            self.m_textCtrl_log.write("[CMD Action]: " + cmdStr + "\n")
            self.updateConnectStatus('green')
        elif self.connectStage == uidef.kConnectStage_ExternalMemory:
            pass

    def jumpToFlashloader( self ):
        status, results, cmdStr = self.sdphost.errorStatus()
        self.m_textCtrl_log.write("[CMD Action]: " + cmdStr + "\n")
        if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
            return
        if self.mcuDevice == uidef.kMcuDevice_iMXRT102x:
            cpu = "MIMXRT1021"
        else:
            pass
        flashloaderBinFile = os.path.join(os.path.dirname(__file__), 'targets', cpu, 'ivt_flashloader.bin')
        status, results, cmdStr = self.sdphost.writeFile(0x20208000, flashloaderBinFile)
        self.m_textCtrl_log.write("[CMD Action]: " + cmdStr + "\n")
        if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
            return
        status, results, cmdStr = self.sdphost.jumpAddress(0x20208400)
        self.m_textCtrl_log.write("[CMD Action]: " + cmdStr + "\n")
        if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
            return

if __name__ == '__main__':
    app = wx.App()

    main_win = secBootMain(None)
    main_win.SetTitle(u"nxpSecBoot v0.1.0")
    main_win.Show()

    app.MainLoop()
