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
        self.certSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Cert)
        self._recoverLastSettings()

    def _recoverLastSettings ( self ):
        useExistingCaKey = self.certSettingsDict['useExistingCaKey']
        if useExistingCaKey == 'n':
            self.m_choice_useExistingCaKey.SetSelection(0)
        else:
            pass

        pkiTreeKeyLen = self.certSettingsDict['pkiTreeKeyLen']
        self.m_choice_pkiTreeKeyLen.SetSelection((pkiTreeKeyLen / 1024) - 1)

        pkiTreeDuration = self.certSettingsDict['pkiTreeDuration']
        self.m_textCtrl_pkiTreeDuration.Clear()
        self.m_textCtrl_pkiTreeDuration.write(str(pkiTreeDuration))

        SRKs = self.certSettingsDict['SRKs']
        self.m_choice_SRKs.SetSelection(SRKs - 1)

        caFlagSet = self.certSettingsDict['caFlagSet']
        if caFlagSet == 'y':
            self.m_choice_caFlagSet.SetSelection(0)
        elif caFlagSet == 'n':
            self.m_choice_caFlagSet.SetSelection(1)
        else:
            pass

    def _getUseExistingCaKey( self ):
        txt = self.m_choice_useExistingCaKey.GetString(self.m_choice_useExistingCaKey.GetSelection())
        if txt == 'No':
            self.certSettingsDict['useExistingCaKey'] = 'n'
        else:
            pass

    def _getPkiTreeKeyLen( self ):
        self.certSettingsDict['pkiTreeKeyLen'] = int(self.m_choice_pkiTreeKeyLen.GetString(self.m_choice_pkiTreeKeyLen.GetSelection()))

    def _getPkiTreeDuration( self ):
        self.certSettingsDict['pkiTreeDuration'] = int(self.m_textCtrl_pkiTreeDuration.GetLineText(0))

    def _getSRKs( self ):
        self.certSettingsDict['SRKs'] = int(self.m_choice_SRKs.GetString(self.m_choice_SRKs.GetSelection()))

    def _getCaFlagSet( self ):
        txt = self.m_choice_caFlagSet.GetString(self.m_choice_caFlagSet.GetSelection())
        if txt == 'No - Fast Auth Tree':
            self.certSettingsDict['caFlagSet'] = 'n'
        elif txt == 'Yes - Standard PKI Tree':
            self.certSettingsDict['caFlagSet'] = 'y'
        else:
            pass

    def callbackOk( self, event ):
        self._getUseExistingCaKey()
        self._getPkiTreeKeyLen()
        self._getPkiTreeDuration()
        self._getSRKs()
        self._getCaFlagSet()
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_Cert, self.certSettingsDict)
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)

