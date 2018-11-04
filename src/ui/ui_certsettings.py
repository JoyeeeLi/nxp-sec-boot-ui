#! /usr/bin/env python
import wx
import sys
import os
import uidef
import uivar
sys.path.append(os.path.abspath("../.."))
from gui import advSettingsWin_Cert

class secBootUiCertSettings(advSettingsWin_Cert.advSettingsWin_Cert):

    def __init__(self, parent):
        advSettingsWin_Cert.advSettingsWin_Cert.__init__(self, parent)

    def callbackOk( self, event ):
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)

