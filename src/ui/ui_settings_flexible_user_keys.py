#! /usr/bin/env python
import wx
import sys
import os
import uidef
import uivar
sys.path.append(os.path.abspath("../.."))
from gui import advSettingsWin_FlexibleUserKeys

class secBootUiSettingsFlexibleUserKeys(advSettingsWin_FlexibleUserKeys.advSettingsWin_FlexibleUserKeys):

    def __init__(self, parent):
        advSettingsWin_FlexibleUserKeys.advSettingsWin_FlexibleUserKeys.__init__(self, parent)

    def callbackChangeRegionSelection( self, event ):
        event.Skip()

    def callbackChangeRegion0KeySource( self, event ):
        event.Skip()

    def callbackChangeRegion0FacCnt( self, event ):
        event.Skip()

    def callbackChangeRegion1KeySource( self, event ):
        event.Skip()

    def callbackChangeRegion1FacCnt( self, event ):
        event.Skip()

    def callbackOk( self, event ):
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)
