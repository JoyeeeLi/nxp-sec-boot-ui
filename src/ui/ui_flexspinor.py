#! /usr/bin/env python
import wx
import sys
import os
import math
import uidef
import uivar
sys.path.append(os.path.abspath("../.."))
from gui import bootDeviceWin_FlexspiNor

g_flexspiNorOpt0_ISSI_IS25LP064A   = 0xc0000006
g_flexspiNorOpt0_MXIC_MX25UM51245G = 0xc0403037
g_flexspiNorOpt0_MXIC_MX25UM51345G = 0xc0403007
g_flexspiNorOpt0_Micron_MT35X      = 0xc0600006
g_flexspiNorOpt0_Adesto_ATXP032    = 0xc0803007

class secBootUiFlexspiNor(bootDeviceWin_FlexspiNor.bootDeviceWin_FlexspiNor):

    def __init__(self, parent):
        bootDeviceWin_FlexspiNor.bootDeviceWin_FlexspiNor.__init__(self, parent)
        flexspiNorOpt0, flexspiNorOpt1 = uivar.getBootDeviceConfiguration(uidef.kBootDevice_FlexspiNor)
        self.flexspiNorOpt0 = flexspiNorOpt0
        self.flexspiNorOpt1 = flexspiNorOpt1
        self._recoverLastSettings()

    def _updateOpt1Field ( self, isEnabled ):
        if isEnabled:
            self.m_choice_flashConnection.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            self.m_textCtrl_driveStrength.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            self.m_choice_dqsPinmuxGroup.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            self.m_choice_enableSecondPinmux.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            self.m_choice_statusOverride.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            self.m_choice_dummyCycles.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        else:
            self.m_choice_flashConnection.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            self.m_textCtrl_driveStrength.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            self.m_choice_dqsPinmuxGroup.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            self.m_choice_enableSecondPinmux.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            self.m_choice_statusOverride.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
            self.m_choice_dummyCycles.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.Refresh()

    def _recoverLastSettings ( self ):
        deviceType = (self.flexspiNorOpt0 & 0x00F00000) >> 20
        self.m_choice_deviceType.SetSelection(deviceType)

        queryPads = (self.flexspiNorOpt0 & 0x000F0000) >> 16
        if queryPads == 0:
            self.m_choice_queryPads.SetSelection(queryPads)
        else:
            self.m_choice_queryPads.SetSelection(queryPads - 1)

        cmdPads = (self.flexspiNorOpt0 & 0x0000F000) >> 12
        if queryPads == 0:
            self.m_choice_cmdPads.SetSelection(cmdPads)
        else:
            self.m_choice_cmdPads.SetSelection(cmdPads - 1)

        quadModeSetting = (self.flexspiNorOpt0 & 0x00000F00) >> 8
        self.m_choice_quadModeSetting.SetSelection(quadModeSetting)

        miscMode = (self.flexspiNorOpt0 & 0x000000F0) >> 4
        self.m_choice_miscMode.SetSelection(miscMode)

        maxFrequency = (self.flexspiNorOpt0 & 0x0000000F) >> 0
        self.m_choice_maxFrequency.SetSelection(maxFrequency - 1)

        hasOption1 = (self.flexspiNorOpt0 & 0x0F000000) >> 24
        self.m_choice_hasOption1.SetSelection(hasOption1)
        if hasOption1 == 0:
            self._updateOpt1Field(False)
        else:
            self._updateOpt1Field(True)

    def _getDeviceType( self ):
        txt = self.m_choice_deviceType.GetString(self.m_choice_deviceType.GetSelection())
        if txt == 'QuadSPI SDR NOR':
            val = 0x0
        elif txt == 'QuadSPI DDR NOR':
            val = 0x1
        elif txt == 'Hyper Flash 1.8V':
            val = 0x2
        elif txt == 'Hyper Flash 3.0V':
            val = 0x3
        elif txt == 'Macronix Octal DDR':
            val = 0x4
        elif txt == 'Macronix Octal SDR':
            val = 0x5
        elif txt == 'Micron Octal DDR':
            val = 0x6
        elif txt == 'Micron Octal SDR':
            val = 0x7
        elif txt == 'Adesto EcoXIP DDR':
            val = 0x8
        elif txt == 'Adesto EcoXIP SDR':
            val = 0x9
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFF0FFFFF) | (val << 20)

    def _getQueryPads( self ):
        val = int(self.m_choice_queryPads.GetString(self.m_choice_queryPads.GetSelection()))
        val = int(math.log(val, 2))
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFF0FFFF) | (val << 16)

    def _getCmdPads( self ):
        val = int(self.m_choice_cmdPads.GetString(self.m_choice_cmdPads.GetSelection()))
        val = int(math.log(val, 2))
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFFF0FFF) | (val << 12)

    def _getQuadModeSetting( self ):
        txt = self.m_choice_quadModeSetting.GetString(self.m_choice_quadModeSetting.GetSelection())
        if txt == 'Not Configured':
            val = 0x0
        elif txt == 'Set StatusReg1[6]':
            val = 0x1
        elif txt == 'Set StatusReg2[1]':
            val = 0x2
        elif txt == 'Set StatusReg2[7]':
            val = 0x3
        elif txt == 'Set StatusReg2[1] by 0x31':
            val = 0x4
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFFFF0FF) | (val << 8)

    def _getMiscMode( self ):
        txt = self.m_choice_miscMode.GetString(self.m_choice_miscMode.GetSelection())
        if txt == 'Disabled':
            val = 0x0
        elif txt == '0_4_4 Mode':
            val = 0x1
        elif txt == '0_8_8 Mode':
            val = 0x2
        elif txt == 'Data Order Swapped':
            val = 0x3
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFFFFF0F) | (val << 4)

    def _getMaxFrequency( self ):
        txt = self.m_choice_maxFrequency.GetString(self.m_choice_maxFrequency.GetSelection())
        if txt == '30MHz':
            val = 0x1
        elif txt == '50MHz':
            val = 0x2
        elif txt == '60MHz':
            val = 0x3
        elif txt == '75MHz':
            val = 0x4
        elif txt == '80MHz':
            val = 0x5
        elif txt == '100MHz':
            val = 0x6
        elif txt == '133MHz':
            val = 0x7
        elif txt == '166MHz':
            val = 0x8
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFFFFFF0) | (val << 0)

    def _getHasOpt1( self ):
        txt = self.m_choice_hasOption1.GetString(self.m_choice_hasOption1.GetSelection())
        if txt == 'No':
            val = 0x0
        elif txt == 'Yes':
            val = 0x1
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xF0FFFFFF) | (val << 24)

    def callbackUseTypicalDeviceModel( self, event ):
        txt = self.m_choice_deviceMode.GetString(self.m_choice_deviceMode.GetSelection())
        if txt == 'ISSI - IS25LP064A':
            self.flexspiNorOpt0 = g_flexspiNorOpt0_ISSI_IS25LP064A
        elif txt == 'MXIC - MX25UM51245G/MX66UM51245G/MX25LM51245G':
            self.flexspiNorOpt0 = g_flexspiNorOpt0_MXIC_MX25UM51245G
        elif txt == 'MXIC - MX25UM51345G':
            self.flexspiNorOpt0 = g_flexspiNorOpt0_MXIC_MX25UM51345G
        elif txt == 'Micron - MT35X':
            self.flexspiNorOpt0 = g_flexspiNorOpt0_Micron_MT35X
        elif txt == 'Adesto - ATXP032':
            self.flexspiNorOpt0 = g_flexspiNorOpt0_Adesto_ATXP032
        else:
            pass
        if txt != 'No':
            self._recoverLastSettings()

    def callbackHasOption1( self, event ):
        txt = self.m_choice_hasOption1.GetString(self.m_choice_hasOption1.GetSelection())
        if txt == 'No':
            self._updateOpt1Field(False)
        elif txt == 'Yes':
            self._updateOpt1Field(True)
        else:
            pass

    def callbackOk( self, event ):
        self._getDeviceType()
        self._getQueryPads()
        self._getCmdPads()
        self._getQuadModeSetting()
        self._getMiscMode()
        self._getMaxFrequency()
        self._getHasOpt1()
        uivar.setBootDeviceConfiguration(uidef.kBootDevice_FlexspiNor, self.flexspiNorOpt0, self.flexspiNorOpt1)
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)

