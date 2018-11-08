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
        userKeyCtrlDict, userKeyCmdDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_UserKeys)
        self.userKeyCtrlDict = userKeyCtrlDict
        self.userKeyCmdDict = userKeyCmdDict
        #self._recoverLastSettings()

    def setNecessaryInfo( self, mcuDevice, otpmkData ):
        self.mcuDevice = mcuDevice
        self.otpmkData = otpmkData
        keySource = None
        if self.mcuDevice == uidef.kMcuDevice_iMXRT102x:
            keySource = uidef.kSupportedKeySource_iMXRT102x
        elif self.mcuDevice == uidef.kMcuDevice_iMXRT105x:
            keySource = uidef.kSupportedKeySource_iMXRT105x
        elif self.mcuDevice == uidef.kMcuDevice_iMXRT106x:
            keySource = uidef.kSupportedKeySource_iMXRT106x
        else:
            pass
        self.m_choice_region0keySource.Clear()
        self.m_choice_region1keySource.Clear()
        self.m_choice_region0keySource.SetItems(keySource)
        self.m_choice_region1keySource.SetItems(keySource)
        self.m_choice_region0keySource.SetSelection(1)
        self.m_choice_region1keySource.SetSelection(1)

    def _getRegionSelection( self ):
        self.userKeyCtrlDict['region_sel'] = self.m_choice_regionSel.GetString(self.m_choice_regionSel.GetSelection())

    def _getBeeEngKeySelection( self ):
        self.userKeyCmdDict['use_zero_key'] = str(self.m_choice_beeEngKeySel.GetSelection())

    def _getImageType( self ):
        self.userKeyCmdDict['is_boot_image'] = str(self.m_choice_imageType.GetSelection())

    def _getXipBaseAddr( self ):
        self.userKeyCmdDict['base_addr'] = self.m_choice_xipBaseAddr.GetString(self.m_choice_xipBaseAddr.GetSelection())

    def _getKeySource( self, regionIndex=0 ):
        if regionIndex == 0:
            self.userKeyCtrlDict['region0_key_src'] = self.m_choice_region0keySource.GetString(self.m_choice_region0keySource.GetSelection())
        elif regionIndex == 1:
            self.userKeyCtrlDict['region1_key_src'] = self.m_choice_region1keySource.GetString(self.m_choice_region1keySource.GetSelection())
        else:
            pass

    def _getUserKeyData( self, regionIndex=0 ):
        if regionIndex == 0:
            self.userKeyCmdDict['region0_key'] = self.m_textCtrl_region0UserKeyData.GetLineText(0)
        elif regionIndex == 1:
            self.userKeyCmdDict['region1_key'] = self.m_textCtrl_region1UserKeyData.GetLineText(0)
        else:
            pass

    def _getAesMode( self, regionIndex=0 ):
        if regionIndex == 0:
            self.userKeyCmdDict['region0_arg'] = str(self.m_choice_region0AesMode.GetSelection())
        elif regionIndex == 1:
            self.userKeyCmdDict['region1_arg'] = str(self.m_choice_region1AesMode.GetSelection())
        else:
            pass

    def _getFacCount( self, regionIndex=0 ):
        if regionIndex == 0:
            self.userKeyCtrlDict['region0_fac_cnt'] = self.m_choice_region0FacCnt.GetSelection() + 1
        elif regionIndex == 1:
            self.userKeyCtrlDict['region1_fac_cnt'] = self.m_choice_region1FacCnt.GetSelection() + 1
        else:
            pass

    def _getAccessPermision( self, regionIndex=0 ):
        if regionIndex == 0:
            self.userKeyCmdDict['region0_arg'] += str(self.m_choice_region0AccessPermision.GetSelection()) + ']'
        elif regionIndex == 1:
            self.userKeyCmdDict['region1_arg'] += str(self.m_choice_region1AccessPermision.GetSelection()) + ']'
        else:
            pass

    def _getRegionRange( self, regionIndex=0, facIndex=0 ):
        if regionIndex == 0:
            if facIndex == 0:
                self.userKeyCmdDict['region0_arg'] += ',[' + self.m_textCtrl_region0Fac0Start.GetLineText(0) + ',' + self.m_textCtrl_region0Fac0Length.GetLineText(0) + ','
            elif facIndex == 1:
                self.userKeyCmdDict['region0_arg'] += ',[' + self.m_textCtrl_region0Fac1Start.GetLineText(0) + ',' + self.m_textCtrl_region0Fac1Length.GetLineText(0) + ','
            elif facIndex == 2:
                self.userKeyCmdDict['region0_arg'] += ',[' + self.m_textCtrl_region0Fac2Start.GetLineText(0) + ',' + self.m_textCtrl_region0Fac2Length.GetLineText(0) + ','
            else:
                pass
        elif regionIndex == 1:
            if facIndex == 0:
                self.userKeyCmdDict['region1_arg'] += ',[' + self.m_textCtrl_region1Fac0Start.GetLineText(0) + ',' + self.m_textCtrl_region1Fac0Length.GetLineText(0) + ','
            elif facIndex == 1:
                self.userKeyCmdDict['region1_arg'] += ',[' + self.m_textCtrl_region1Fac1Start.GetLineText(0) + ',' + self.m_textCtrl_region1Fac1Length.GetLineText(0) + ','
            elif facIndex == 2:
                self.userKeyCmdDict['region1_arg'] += ',[' + self.m_textCtrl_region1Fac2Start.GetLineText(0) + ',' + self.m_textCtrl_region1Fac2Length.GetLineText(0) + ','
            else:
                pass
        else:
            pass

    def _getRegionLock( self, regionIndex=0 ):
        if regionIndex == 0:
            self.userKeyCmdDict['region0_lock'] = str(self.m_choice_region0Lock.GetSelection())
        elif regionIndex == 1:
            self.userKeyCmdDict['region1_lock'] = str(self.m_choice_region1Lock.GetSelection())
        else:
            pass

    def _getRegionArg( self, regionIndex=0 ):
        self._getFacCount(regionIndex)
        self._getAesMode(regionIndex)
        facCnt = 0
        if regionIndex == 0:
            facCnt = self.userKeyCtrlDict['region0_fac_cnt']
        elif regionIndex == 1:
            facCnt = self.userKeyCtrlDict['region1_fac_cnt']
        else:
            pass
        for i in range(facCnt):
            self._getRegionRange(regionIndex, i)
            self._getAccessPermision(regionIndex)

    def _getRegionInfo( self, regionIndex=0 ):
        self._getKeySource(regionIndex)
        self._getUserKeyData(regionIndex)
        self._getRegionArg(regionIndex)
        self._getRegionLock(regionIndex)

    def _updateKeySourceInfoField ( self, regionIndex=0 ):
        if regionIndex == 0:
            if self.userKeyCtrlDict['region0_key_src'] == uidef.kUserKeySource_OTPMK:
                self.m_textCtrl_region0UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0UserKeyData.Clear()
                if self.otpmkData != None:
                    self.m_textCtrl_region0UserKeyData.write(self.otpmkData)
            else:
                self.m_textCtrl_region0UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        elif regionIndex == 1:
            if self.userKeyCtrlDict['region1_key_src'] == uidef.kUserKeySource_OTPMK:
                self.m_textCtrl_region1UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1UserKeyData.Clear()
                if self.otpmkData != None:
                    self.m_textCtrl_region1UserKeyData.write(self.otpmkData)
            else:
                self.m_textCtrl_region1UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        else:
            pass
        self.Refresh()

    def _updateRegionRangeInfoField ( self, regionIndex=0 ):
        if regionIndex == 0:
            if self.userKeyCtrlDict['region0_fac_cnt'] < 1:
                self.m_staticText_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            if self.userKeyCtrlDict['region0_fac_cnt'] < 2:
                self.m_staticText_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            if self.userKeyCtrlDict['region0_fac_cnt'] < 3:
                self.m_staticText_region0Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region0Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        elif regionIndex == 1:
            if self.userKeyCtrlDict['region1_fac_cnt'] < 1:
                self.m_staticText_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            if self.userKeyCtrlDict['region1_fac_cnt'] < 2:
                self.m_staticText_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            if self.userKeyCtrlDict['region1_fac_cnt'] < 3:
                self.m_staticText_region1Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region1Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        else:
            pass
        self.Refresh()

    def _updateRegionInfoField ( self, regionIndex=0, isRegionEnabled=False ):
        if regionIndex == 0:
            if isRegionEnabled:
                self.m_staticText_region0keySource.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0FacCnt.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0AccessPermision.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Lock.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

                self.m_choice_region0keySource.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_choice_region0AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_choice_region0FacCnt.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_choice_region0AccessPermision.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_choice_region0Lock.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

                self._getKeySource(0)
                self._updateKeySourceInfoField(0)
                self._getFacCount(0)
                self._updateRegionRangeInfoField(0)
            else:
                self.m_staticText_region0keySource.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0FacCnt.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0AccessPermision.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Lock.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

                self.m_choice_region0keySource.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_choice_region0AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_choice_region0FacCnt.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_choice_region0AccessPermision.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_choice_region0Lock.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        elif regionIndex == 1:
            if isRegionEnabled:
                self.m_staticText_region1keySource.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1FacCnt.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1AccessPermision.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Lock.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

                self.m_choice_region1keySource.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_choice_region1AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_choice_region1FacCnt.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_choice_region1AccessPermision.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_choice_region1Lock.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

                self._getKeySource(1)
                self._updateKeySourceInfoField(1)
                self._getFacCount(1)
                self._updateRegionRangeInfoField(1)
            else:
                self.m_staticText_region1keySource.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1FacCnt.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1AccessPermision.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Lock.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

                self.m_choice_region1keySource.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1UserKeyData.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_choice_region1AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_choice_region1FacCnt.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac2Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac2Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_choice_region1AccessPermision.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_choice_region1Lock.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        else:
            pass
        self.Refresh()

    def callbackChangeRegionSelection( self, event ):
        self._getRegionSelection()
        if self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region0:
            self._updateRegionInfoField(0, True)
            self._updateRegionInfoField(1, False)
        elif self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region1:
            self._updateRegionInfoField(0, False)
            self._updateRegionInfoField(1, True)
        elif self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            self._updateRegionInfoField(0, True)
            self._updateRegionInfoField(1, True)
        else:
            pass

    def callbackChangeRegion0KeySource( self, event ):
        if self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region0 or \
           self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            self._getKeySource(0)
            self._updateKeySourceInfoField(0)

    def popupMsgBox( self, msgStr ):
        messageText = (msgStr)
        wx.MessageBox(messageText, "Error", wx.OK | wx.ICON_INFORMATION)

    def callbackChangeRegion0FacCnt( self, event ):
        if self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region0:
            self._getFacCount(0)
            self._updateRegionRangeInfoField(0)
        elif self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            region0FacCnt = self.m_choice_region0FacCnt.GetSelection() + 1
            if region0FacCnt + self.userKeyCtrlDict['region1_fac_cnt'] > uidef.kMaxFacRegionCount:
                self.m_choice_region0FacCnt.SetSelection(self.userKeyCtrlDict['region0_fac_cnt'] - 1)
                self.popupMsgBox('The sum of FAC Region count of Region0 and Region1 must be no more than ' + str(uidef.kMaxFacRegionCount))
            else:
                self._getFacCount(0)
                self._updateRegionRangeInfoField(0)
        else:
            pass

    def callbackChangeRegion1KeySource( self, event ):
        if self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region1:
            self._getKeySource(1)
            self._updateKeySourceInfoField(1)
        elif self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            region1FacCnt = self.m_choice_region1FacCnt.GetSelection() + 1
            if region1FacCnt + self.userKeyCtrlDict['region0_fac_cnt'] > uidef.kMaxFacRegionCount:
                self.m_choice_region1FacCnt.SetSelection(self.userKeyCtrlDict['region1_fac_cnt'] - 1)
                self.popupMsgBox('The sum of FAC Region count of Region0 and Region1 must be no more than ' + str(uidef.kMaxFacRegionCount))
            else:
                self._getFacCount(1)
                self._updateRegionRangeInfoField(1)
        else:
            pass

    def callbackChangeRegion1FacCnt( self, event ):
        if self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region1 or \
           self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            self._getFacCount(1)
            self._updateRegionRangeInfoField(1)

    def callbackOk( self, event ):
        self._getRegionSelection()
        if self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region0:
            self._getRegionInfo(0)
        elif self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region1:
            self._getRegionInfo(1)
        elif self.userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            self._getRegionInfo(0)
            self._getRegionInfo(1)
        else:
            pass
        self._getBeeEngKeySelection()
        self._getImageType()
        self._getXipBaseAddr()
        #print 'base_addr=' + self.userKeyCmdDict['base_addr']
        #print 'region0_key=' + self.userKeyCmdDict['region0_key'] + \
        #      ' region0_arg=' + self.userKeyCmdDict['region0_arg'] + \
        #      ' region0_lock=' + self.userKeyCmdDict['region0_lock']
        #print 'region1_key=' + self.userKeyCmdDict['region1_key'] + \
        #      ' region1_arg=' + self.userKeyCmdDict['region1_arg'] + \
        #      ' region1_lock=' + self.userKeyCmdDict['region1_lock']
        #print 'use_zero_key=' + self.userKeyCmdDict['use_zero_key']
        #print 'is_boot_image=' + self.userKeyCmdDict['is_boot_image']
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_UserKeys, self.userKeyCtrlDict, self.userKeyCmdDict)
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)
