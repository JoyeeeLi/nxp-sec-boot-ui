import wx
import sys, os
from ui import uicore

class secBootMain(uicore.secBootUi):

    def __init__(self, parent):
        uicore.secBootUi.__init__(self, parent)

    def callbackSwitchSecureBootType( self, event ):
        self.setSecureBootSeqColor()

    def callbackSwitchKeyStorageRegion( self, event ):
        self.setKeyStorageRegionColor()

if __name__ == '__main__':
    app = wx.App()

    main_win = secBootMain(None)
    main_win.SetTitle(u"nxpSecBoot v0.1.0")
    main_win.Show()

    app.MainLoop()
