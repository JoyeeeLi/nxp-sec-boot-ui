import wx
import sys, os
from run import runcore

class secBootMain(runcore.secBootRun):

    def __init__(self, parent):
        runcore.secBootRun.__init__(self, parent)

    def callbackSwitchSecureBootType( self, event ):
        self.setSecureBootSeqColor()

    def callbackSwitchKeyStorageRegion( self, event ):
        self.setKeyStorageRegionColor()

    def callbackConnectToDevice( self, event ):
        self.refreshTargetSetupObject()
        self.connectToDevice()
        status, results = self.sdphost.readRegister(0x401F46F0)

if __name__ == '__main__':
    app = wx.App()

    main_win = secBootMain(None)
    main_win.SetTitle(u"nxpSecBoot v0.1.0")
    main_win.Show()

    app.MainLoop()
