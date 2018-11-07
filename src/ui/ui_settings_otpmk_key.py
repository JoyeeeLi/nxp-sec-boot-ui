#! /usr/bin/env python
import wx
import sys
import os
import uidef
import uivar
sys.path.append(os.path.abspath("../.."))
from gui import advSettingsWin_OtpmkKey

class secBootUiSettingsOtpmkKey(advSettingsWin_OtpmkKey.advSettingsWin_OtpmkKey):

    def __init__(self, parent):
        advSettingsWin_OtpmkKey.advSettingsWin_OtpmkKey.__init__(self, parent)
        otpmkKeyOpt, otpmkEncryptedRegionStart, otpmkEncryptedRegionLength = uivar.getAdvancedSettings(uidef.kAdvancedSettings_OtpmkKey)
        self.otpmkKeyOpt = otpmkKeyOpt
        self.otpmkEncryptedRegionStart = otpmkEncryptedRegionStart
        self.otpmkEncryptedRegionLength = otpmkEncryptedRegionLength
        self._recoverLastSettings()

    def _updateRegionInfoField ( self, regionCnt ):
        if regionCnt < 1:
            self.m_textCtrl_region0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            self.m_textCtrl_region0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        else:
            self.m_textCtrl_region0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            self.m_textCtrl_region0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        if regionCnt < 2:
            self.m_textCtrl_region1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            self.m_textCtrl_region1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        else:
            self.m_textCtrl_region1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            self.m_textCtrl_region1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.Refresh()

    def _recoverLastSettings ( self ):
        keySource = (self.otpmkKeyOpt & 0x0F000000) >> 24
        self.m_choice_keySource.SetSelection(keySource)

        aesMode = (self.otpmkKeyOpt & 0x00F00000) >> 20
        self.m_choice_aesMode.SetSelection(aesMode)

        encryptedRegionCnt = (self.otpmkKeyOpt & 0x000F0000) >> 16
        self.m_choice_encryptedRegionCnt.SetSelection(encryptedRegionCnt)

        self._updateRegionInfoField(encryptedRegionCnt)

        if encryptedRegionCnt > 0:
            self.m_textCtrl_region0Start.Clear()
            self.m_textCtrl_region0Length.Clear()
            self.m_textCtrl_region0Start.write(str(hex(self.otpmkEncryptedRegionStart[0])))
            self.m_textCtrl_region0Length.write(str(hex(self.otpmkEncryptedRegionLength[0])))
        if encryptedRegionCnt > 1:
            self.m_textCtrl_region1Start.Clear()
            self.m_textCtrl_region1Length.Clear()
            self.m_textCtrl_region1Start.write(str(hex(self.otpmkEncryptedRegionStart[1])))
            self.m_textCtrl_region1Length.write(str(hex(self.otpmkEncryptedRegionLength[1])))

    def _getKeySource( self ):
        txt = self.m_choice_keySource.GetString(self.m_choice_keySource.GetSelection())
        if txt == 'Fuse OTPMK[255:128]':
            val = 0x0
        else:
            pass
        self.otpmkKeyOpt = (self.otpmkKeyOpt & 0xF0FFFFFF) | (val << 24)

    def _getAesMode( self ):
        txt = self.m_choice_aesMode.GetString(self.m_choice_aesMode.GetSelection())
        if txt == 'ECB':
            val = 0x0
        elif txt == 'CTR':
            val = 0x1
        else:
            pass
        self.otpmkKeyOpt = (self.otpmkKeyOpt & 0xFF0FFFFF) | (val << 20)

    def _getEncryptedRegionCount( self ):
        txt = self.m_choice_encryptedRegionCnt.GetString(self.m_choice_encryptedRegionCnt.GetSelection())
        val = int(txt[0])
        self.otpmkKeyOpt = (self.otpmkKeyOpt & 0xFFF0FFFF) | (val << 16)

    def _convertRegionInfoToVal32( self, regionInfoStr ):
        if len(regionInfoStr) > 2 and regionInfoStr[0:2] == '0x':
            return int(regionInfoStr[2:len(regionInfoStr)], 16)
        else:
            return None

    def _getEncryptedRegionInfo( self ):
        txt = self.m_choice_encryptedRegionCnt.GetString(self.m_choice_encryptedRegionCnt.GetSelection())
        regionCnt = int(txt[0])
        if regionCnt > 0:
            self.otpmkEncryptedRegionStart[0] = self._convertRegionInfoToVal32(self.m_textCtrl_region0Start.GetLineText(0))
            self.otpmkEncryptedRegionLength[0] = self._convertRegionInfoToVal32(self.m_textCtrl_region0Length.GetLineText(0))
        else:
            self.otpmkEncryptedRegionStart[0] = None
            self.otpmkEncryptedRegionLength[0] = None
        if regionCnt > 1:
            self.otpmkEncryptedRegionStart[1] = self._convertRegionInfoToVal32(self.m_textCtrl_region1Start.GetLineText(0))
            self.otpmkEncryptedRegionLength[1] = self._convertRegionInfoToVal32(self.m_textCtrl_region1Length.GetLineText(0))
        else:
            self.otpmkEncryptedRegionStart[1] = None
            self.otpmkEncryptedRegionLength[1] = None

    def callbackChangeRegionCount( self, event ):
        txt = self.m_choice_encryptedRegionCnt.GetString(self.m_choice_encryptedRegionCnt.GetSelection())
        regionCnt = int(txt[0])
        self._updateRegionInfoField(regionCnt)

    def callbackOk( self, event ):
        self._getKeySource()
        self._getAesMode()
        self._getEncryptedRegionCount()
        self._getEncryptedRegionInfo()
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_OtpmkKey, self.otpmkKeyOpt, self.otpmkEncryptedRegionStart, self.otpmkEncryptedRegionLength)
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)

