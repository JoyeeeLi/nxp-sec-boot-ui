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

    def _getRegionSelection():
        self.userKeyCtrlDict['region_sel'] = self.m_choice_regionSel.GetString(self.m_choice_regionSel.GetSelection())

    def _getBeeEngKeySelection():
        self.userKeyCmdDict['use_zero_key'] = str(self.m_choice_beeEngKeySel.GetSelection())

    def _getImageType():
        self.userKeyCmdDict['is_boot_image'] = str(self.m_choice_imageType.GetSelection())

    def _getXipBaseAddr():
        self.userKeyCtrlDict['base_addr'] = self.m_choice_xipBaseAddr.GetString(self.m_choice_xipBaseAddr.GetSelection())

    def _updateRegionRangeInfoField ( self, regionIndex=0, regionCnt=1 ):
        if regionIndex == 0:
            if regionCnt < 1:
                self.m_staticText_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            if regionCnt < 2:
                self.m_staticText_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region0Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            if regionCnt < 3:
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
            if regionCnt < 1:
                self.m_staticText_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac0Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac0Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            if regionCnt < 2:
                self.m_staticText_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_staticText_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
                self.m_textCtrl_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            else:
                self.m_staticText_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_staticText_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac1Start.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
                self.m_textCtrl_region1Fac1Length.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            if regionCnt < 3:
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

    def callbackChangeRegionSelection( self, event ):
        event.Skip()

    def callbackChangeRegion0KeySource( self, event ):
        event.Skip()

    def callbackChangeRegion0FacCnt( self, event ):
        facCnt = self.m_choice_region0FacCnt.GetSelection() + 1
        self._updateRegionRangeInfoField(0, facCnt)

    def callbackChangeRegion1KeySource( self, event ):
        event.Skip()

    def callbackChangeRegion1FacCnt( self, event ):
        facCnt = self.m_choice_region1FacCnt.GetSelection() + 1
        self._updateRegionRangeInfoField(1, facCnt)

    def callbackOk( self, event ):
        self._getRegionSelection()
        self._getBeeEngKeySelection()
        self._getImageType()
        self._getXipBaseAddr()
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_UserKeys, self.userKeyCtrlDict, self.userKeyCmdDict)
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)
