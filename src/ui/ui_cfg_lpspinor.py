#! /usr/bin/env python
import wx
import sys
import os
import uivar
import uidef
sys.path.append(os.path.abspath("../.."))
from gui import bootDeviceWin_LpspiNor

class secBootUiLpspiNor(bootDeviceWin_LpspiNor.bootDeviceWin_LpspiNor):
    def __init__(self, parent):
        bootDeviceWin_LpspiNor.bootDeviceWin_LpspiNor.__init__(self, parent)
        lpspiNorOpt0, lpspiNorOpt1 = uivar.getBootDeviceConfiguration(uidef.kBootDevice_SemcNor)
        self.lpspiNorOpt0 = lpspiNorOpt0
        self.lpspiNorOpt1 = lpspiNorOpt1

    def _getPageSize( self ):
        txt = self.m_choice_Page_Size.GetString(self.m_choice_Page_Size.GetSelection())
        if txt == '256 Bytes':
            val = 0x0
        elif txt == '512 Bytes':
            val = 0x1
        elif txt == '1024 Bytes':
            val = 0x2
        elif txt == '32 Bytes':
            val = 0x3
        elif txt == '64 Bytes':
            val = 0x4
        elif txt == '128 Bytes':
            val = 0x5
        else:
            pass
        self.lpspiNorOpt0 = (self.lpspiNorOpt0 & 0xFFFFFFF0) | (val << 0)

    def _getSectorSize( self ):
        txt = self.m_choice_Sector_Size.GetString(self.m_choice_Sector_Size.GetSelection())
        if txt == '4 KBytes':
            val = 0x0
        elif txt == '8 KBytes':
            val = 0x1
        elif txt == '32 KBytes':
            val = 0x2
        elif txt == '64 KBytes':
            val = 0x3
        elif txt == '128 KBytes':
            val = 0x4
        elif txt == '256 KBytes':
            val = 0x5
        else:
            pass
        self.lpspiNorOpt0 = (self.lpspiNorOpt0 & 0xFFFFFF0F) | (val << 4)


    def _getMemorySize( self ):
        txt = self.m_choice_Memory_Size.GetString(self.m_choice_Memory_Size.GetSelection())
        if txt == '512 KBytes':
            val = 0x0
        elif txt == '1024 KBytes':
            val = 0x1
        elif txt == '2 MBytes':
            val = 0x2
        elif txt == '4 MBytes':
            val = 0x3
        elif txt == '8 MBytes':
            val = 0x4
        elif txt == '16 MBytes':
            val = 0x5
        elif txt == '32 MBytes':
            val = 0x6
        elif txt == '64 MBytes':
            val = 0x7
        elif txt == '128 MBytes':
            val = 0x8
        elif txt == '256 MBytes':
            val = 0x9
        elif txt == '512 MBytes':
            val = 0xA
        elif txt == '1024 MBytes':
            val = 0xB
        elif txt == '32 KBytes':
            val = 0xC
        elif txt == '64 KBytes':
            val = 0xD
        elif txt == '128 KBytes':
            val = 0xE
        else:
            pass
        self.lpspiNorOpt0 = (self.lpspiNorOpt0 & 0xFFFFF0FF) | (val << 8)

    def _getMemoryType( self ):
        txt = self.m_choice_Memory_Type.GetString(self.m_choice_Memory_Type.GetSelection())
        if txt == 'NOR Flash':
            val = 0x0
        elif txt == 'EEPROM':
            val = 0x1
        else:
            pass
        self.lpspiNorOpt0 = (self.lpspiNorOpt0 & 0xFFFF0FFF) | (val << 12)

    def _getPCSIndex( self ):
        txt = self.m_choice_PCS_Index.GetString(self.m_choice_PCS_Index.GetSelection())
        if txt == 'PCS0':
            val = 0x0
        elif txt == 'PCS1':
            val = 0x1
        elif txt == 'PCS2':
            val = 0x2
        elif txt == 'PCS3':
            val = 0x3
        else:
            pass
        self.lpspiNorOpt0 = (self.lpspiNorOpt0 & 0xFFF0FFFF) | (val << 16)

    def _getSPIIndex( self ):
        txt = self.m_choice_SPI_Index.GetString(self.m_choice_SPI_Index.GetSelection())
        if txt == 'SPI1':
            val = 0x1
        elif txt == 'SPI2':
            val = 0x2
        elif txt == 'SPI3':
            val = 0x3
        elif txt == 'SPI4':
            val = 0x4
        else:
            pass
        self.lpspiNorOpt0 = (self.lpspiNorOpt0 & 0xFF0FFFFF) | (val << 20)

    def _getOption1Size( self ):
        val = int(self.m_textCtrl_Option1_Size.GetLineText(0))
        self.lpspiNorOpt0 = (self.lpspiNorOpt0 & 0xF0FFFFFF) | (val << 24)

    def _getSPISpeed( self ):
        txt = self.m_choice_SPI_Speed.GetString(self.m_choice_SPI_Speed.GetSelection())
        if txt == '20 MHZ':
            val = 0x0
        elif txt == '10 MHZ':
            val = 0x1
        elif txt == '5 MHZ':
            val = 0x2
        elif txt == '2 MHZ':
            val = 0x3
        else:
            pass
        self.lpspiNorOpt1 = (self.lpspiNorOpt1 & 0xFFFFFFF0) | (val << 0)

    def cancel_of_LPSPI_NOR(self, event):
        self.Show(False)

    def apply_of_LPSPI_NOR(self, event):
        self._getPageSize()
        self._getSectorSize()
        self._getMemorySize()
        self._getMemoryType()
        self._getPCSIndex()
        self._getSPIIndex()
        self._getOption1Size()
        self._getSPISpeed()
        uivar.setBootDeviceConfiguration(uidef.kBootDevice_LpspiNor, self.lpspiNorOpt0, self.lpspiNorOpt1)
        self.Show(False)

    def OnClose_LPSPI_NOR(self, event):
        ret = wx.MessageBox('Do you really want to leave?', 'Confirm', wx.OK | wx.CANCEL)
        if ret == wx.OK:
            self.Show(False)