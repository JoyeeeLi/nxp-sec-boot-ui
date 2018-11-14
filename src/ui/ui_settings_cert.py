#! /usr/bin/env python
import wx
import sys
import os
import uidef
import uivar
sys.path.append(os.path.abspath("../.."))
from gui import advSettingsWin_Cert

class secBootUiSettingsCert(advSettingsWin_Cert.advSettingsWin_Cert):

    def __init__(self, parent):
        advSettingsWin_Cert.advSettingsWin_Cert.__init__(self, parent)
        self.certSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Cert)
        self._recoverLastSettings()

    def _setPkiTreeKeyLenItems( self ):
        keySel = None
        if self.certSettingsDict['cstVersion'] == uidef.kCstVersion_v3_1_0 and self.certSettingsDict['useEllipticCurveCrypto'] == 'y':
            keySel = uidef.kPkiTreeKeySel_IsEcc
        else:
            keySel = uidef.kPkiTreeKeySel_NotEcc
        self.m_choice_pkiTreeKeyLen.Clear()
        self.m_choice_pkiTreeKeyLen.SetItems(keySel)
        self.m_choice_pkiTreeKeyLen.SetSelection(0)

    def _recoverLastSettings ( self ):
        cstVersion = self.certSettingsDict['cstVersion']
        if cstVersion == uidef.kCstVersion_v2_3_3:
            self.m_choice_cstVersion.SetSelection(0)
        elif cstVersion == uidef.kCstVersion_v3_0_1:
            self.m_choice_cstVersion.SetSelection(1)
        elif cstVersion == uidef.kCstVersion_v3_1_0:
            self.m_choice_cstVersion.SetSelection(2)
        else:
            pass

        useExistingCaKey = self.certSettingsDict['useExistingCaKey']
        if useExistingCaKey == 'n':
            self.m_choice_useExistingCaKey.SetSelection(0)
        else:
            pass

        useEllipticCurveCrypto = self.certSettingsDict['useEllipticCurveCrypto']
        if useEllipticCurveCrypto == 'n':
            self.m_choice_useEcc.SetSelection(0)
        elif useEllipticCurveCrypto == 'y':
            self.m_choice_useEcc.SetSelection(1)
        else:
            pass

        self._setPkiTreeKeyLenItems()

        pkiTreeKeyLen = self.certSettingsDict['pkiTreeKeyLen']
        if cstVersion == uidef.kCstVersion_v3_1_0 and useEllipticCurveCrypto == 'y':
            if pkiTreeKeyLen == 'p256':
                self.m_choice_pkiTreeKeyLen.SetSelection(0)
            elif pkiTreeKeyLen == 'p384':
                self.m_choice_pkiTreeKeyLen.SetSelection(1)
            elif pkiTreeKeyLen == 'p521':
                self.m_choice_pkiTreeKeyLen.SetSelection(2)
            else:
                pass
        else:
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

    def _getCstVersion( self ):
        self.certSettingsDict['cstVersion'] = self.m_choice_cstVersion.GetString(self.m_choice_cstVersion.GetSelection())

    def _getUseExistingCaKey( self ):
        txt = self.m_choice_useExistingCaKey.GetString(self.m_choice_useExistingCaKey.GetSelection())
        self.certSettingsDict['useExistingCaKey'] = txt[0].lower()

    def _getUseEllipticCurveCrypto( self ):
        txt = self.m_choice_useEcc.GetString(self.m_choice_useEcc.GetSelection())
        self.certSettingsDict['useEllipticCurveCrypto'] = txt[0].lower()

    def _getPkiTreeKeyLen( self ):
        if self.certSettingsDict['cstVersion'] == uidef.kCstVersion_v3_1_0 and self.certSettingsDict['useEllipticCurveCrypto'] == 'y':
            self.certSettingsDict['pkiTreeKeyLen'] = self.m_choice_pkiTreeKeyLen.GetString(self.m_choice_pkiTreeKeyLen.GetSelection())
            if self.certSettingsDict['pkiTreeKeyLen'] == 'p256':
                self.certSettingsDict['pkiTreeKeyCn'] = 'prime256v1'
            elif self.certSettingsDict['pkiTreeKeyLen'] == 'p384':
                self.certSettingsDict['pkiTreeKeyCn'] = 'secp384r1'
            elif self.certSettingsDict['pkiTreeKeyLen'] == 'p521':
                self.certSettingsDict['pkiTreeKeyCn'] = 'secp521r1'
            else:
                pass
        else:
            self.certSettingsDict['pkiTreeKeyLen'] = int(self.m_choice_pkiTreeKeyLen.GetString(self.m_choice_pkiTreeKeyLen.GetSelection()))

    def _getPkiTreeDuration( self ):
        self.certSettingsDict['pkiTreeDuration'] = int(self.m_textCtrl_pkiTreeDuration.GetLineText(0))

    def _getSRKs( self ):
        self.certSettingsDict['SRKs'] = int(self.m_choice_SRKs.GetString(self.m_choice_SRKs.GetSelection()))

    def _getCaFlagSet( self ):
        txt = self.m_choice_caFlagSet.GetString(self.m_choice_caFlagSet.GetSelection())
        self.certSettingsDict['caFlagSet'] = txt[0].lower()

    def callbackSwitchCstVersion( self, event ):
        self._getCstVersion()
        if self.certSettingsDict['cstVersion'] == uidef.kCstVersion_v3_1_0:
            self.m_staticText_useEcc.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        elif self.certSettingsDict['cstVersion'] == uidef.kCstVersion_v2_3_3 or self.certSettingsDict['cstVersion'] == uidef.kCstVersion_v3_0_1:
            self.m_staticText_useEcc.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        else:
            pass
        self._setPkiTreeKeyLenItems()

    def callbackUseEcc( self, event ):
        self._getUseEllipticCurveCrypto()
        if self.certSettingsDict['cstVersion'] == uidef.kCstVersion_v3_1_0:
            self._setPkiTreeKeyLenItems()

    def callbackOk( self, event ):
        self._getCstVersion()
        self._getUseExistingCaKey()
        self._getUseEllipticCurveCrypto()
        self._getPkiTreeKeyLen()
        self._getPkiTreeDuration()
        self._getSRKs()
        self._getCaFlagSet()
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_Cert, self.certSettingsDict)
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)

