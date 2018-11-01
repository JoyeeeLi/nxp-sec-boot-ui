#! /usr/bin/env python
import wx
import sys
import os
import math
import serial.tools.list_ports
import uidef
sys.path.append(os.path.abspath("../.."))
from gui import nxpSecBoot
from gui import semcNand
sys.path.append(os.path.abspath(".."))
from run import rundef

g_semcNandOpt = 0xD0000000
g_semcNandFcbOpt = 0x00000000
g_semcNandImageInfo = [None] * 8

class secBootUiSemcNand(semcNand.bootDeviceWin_SemcNand):

    def __init__(self, parent):
        semcNand.bootDeviceWin_SemcNand.__init__(self, parent)

    def _getOnfiVersion( self ):
        global g_semcNandOpt
        txt = self.m_choice_onfiVersion.GetString(self.m_choice_onfiVersion.GetSelection())
        if txt == 'ONFI 1.x':
            val = 0x1
        else:
            pass
        g_semcNandOpt = (g_semcNandOpt & 0xFFFFFFF8) | (val << 0)

    def _getEdoMode( self ):
        global g_semcNandOpt
        txt = self.m_choice_edoMode.GetString(self.m_choice_edoMode.GetSelection())
        if txt == 'Disabled':
            val = 0x0
        elif txt == 'Enabled':
            val = 0x1
        else:
            pass
        g_semcNandOpt = (g_semcNandOpt & 0xFFFFFFF7) | (val << 3)

    def _getOnfiTimingMode( self ):
        global g_semcNandOpt
        txt = self.m_choice_onfiTimingMode.GetString(self.m_choice_onfiTimingMode.GetSelection())
        if txt == 'Mode0 - 10MHz':
            val = 0x0
        elif txt == 'Mode1 - 20MHz':
            val = 0x1
        elif txt == 'Mode2 - 28MHz':
            val = 0x2
        elif txt == 'Mode3 - 33MHz':
            val = 0x3
        elif txt == 'Mode4 - 40MHz':
            val = 0x4
        elif txt == 'Mode5 - 50MHz':
            val = 0x5
        else:
            pass
        g_semcNandOpt = (g_semcNandOpt & 0xFFFFFF8F) | (val << 4)

    def _getIoPortSize( self ):
        global g_semcNandOpt
        txt = self.m_choice_ioPortSize.GetString(self.m_choice_ioPortSize.GetSelection())
        if txt == 'x8 bits':
            val = 0x1
        elif txt == 'x16 bits':
            val = 0x2
        else:
            pass
        g_semcNandOpt = (g_semcNandOpt & 0xFFFFFCFF) | (val << 8)

    def _getPcsPort( self ):
        global g_semcNandOpt
        txt = self.m_choice_pcsPort.GetString(self.m_choice_pcsPort.GetSelection())
        if txt == 'CSX0':
            val = 0x0
        else:
            pass
        g_semcNandOpt = (g_semcNandOpt & 0xFFFF8FFF) | (val << 12)

    def _getEccType( self ):
        global g_semcNandOpt
        txt = self.m_choice_eccType.GetString(self.m_choice_eccType.GetSelection())
        if txt == 'SW - 1bit ECC':
            val = 0x0
        elif txt == 'HW':
            val = 0x1
        else:
            pass
        g_semcNandOpt = (g_semcNandOpt & 0xFFFEFFFF) | (val << 16)

    def _getEccStatus( self ):
        global g_semcNandOpt
        txt = self.m_choice_eccStatus.GetString(self.m_choice_eccStatus.GetSelection())
        if txt == 'Enabled':
            val = 0x0
        elif txt == 'Disabled':
            val = 0x1
        else:
            pass
        g_semcNandOpt = (g_semcNandOpt & 0xFFFDFFFF) | (val << 17)

    def _getSearchCount( self ):
        global g_semcNandFcbOpt
        val = int(self.m_choice_searchCount.GetString(self.m_choice_searchCount.GetSelection()))
        g_semcNandFcbOpt = (g_semcNandFcbOpt & 0xFFFFFFF0) | (val << 0)

    def _getSearchStride( self ):
        global g_semcNandFcbOpt
        val = int(self.m_choice_searchStride.GetString(self.m_choice_searchStride.GetSelection()))
        val = int(math.log(val, 2))
        g_semcNandFcbOpt = (g_semcNandFcbOpt & 0xFFFFF0FF) | (val << 8)

    def _getImageCopies( self ):
        global g_semcNandFcbOpt
        val = int(self.m_choice_imageCopies.GetString(self.m_choice_imageCopies.GetSelection()))
        g_semcNandFcbOpt = (g_semcNandFcbOpt & 0xFFF0FFFF) | (val << 16)

    def _getImageInfo( self ):
        global g_semcNandImageInfo
        imageCopies = int(self.m_choice_imageCopies.GetString(self.m_choice_imageCopies.GetSelection()))
        if imageCopies > 0:
            g_semcNandImageInfo[0] = (int(self.m_textCtrl_image0Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image0Cnt.GetLineText(0))
        if imageCopies > 1:
            g_semcNandImageInfo[1] = (int(self.m_textCtrl_image1Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image1Cnt.GetLineText(0))
        if imageCopies > 2:
            g_semcNandImageInfo[2] = (int(self.m_textCtrl_image2Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image2Cnt.GetLineText(0))
        if imageCopies > 3:
            g_semcNandImageInfo[3] = (int(self.m_textCtrl_image3Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image3Cnt.GetLineText(0))
        if imageCopies > 4:
            g_semcNandImageInfo[4] = (int(self.m_textCtrl_image4Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image4Cnt.GetLineText(0))
        if imageCopies > 5:
            g_semcNandImageInfo[5] = (int(self.m_textCtrl_image5Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image5Cnt.GetLineText(0))
        if imageCopies > 6:
            g_semcNandImageInfo[6] = (int(self.m_textCtrl_image6Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image6Cnt.GetLineText(0))
        if imageCopies > 7:
            g_semcNandImageInfo[7] = (int(self.m_textCtrl_image7Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image7Cnt.GetLineText(0))

    def callbackOk( self, event ):
        self._getOnfiVersion()
        self._getEdoMode()
        self._getOnfiTimingMode()
        self._getIoPortSize()
        self._getPcsPort()
        self._getEccType()
        self._getEccStatus()
        self._getSearchCount()
        self._getSearchStride()
        self._getImageCopies()
        self._getImageInfo()
        self.Show(False)

    def callbackCancel( self, event ):
        self.Show(False)

class secBootUi(nxpSecBoot.secBootWin):

    def __init__(self, parent):
        nxpSecBoot.secBootWin.__init__(self, parent)
        self.m_bitmap_nxp.SetBitmap(wx.Bitmap( u"../img/logo_nxp.png", wx.BITMAP_TYPE_ANY ))
        self.updateConnectStatus()

        self.mcuSeries = None
        self.mcuDevice = None
        self.bootDevice = None
        self.updateTargetSetupValue()
        self.semcNandOpt = None
        self.semcNandFcbOpt = None
        self.semcNandImageInfo = None

        self.isUartPortSelected = None
        self.isUsbhidPortSelected = None
        self.uartComPort = None
        self.uartBaudrate = None
        self.usbhidVid = None
        self.usbhidPid = None
        self._initPortSetupValue()

        self.secureBootType = None
        self.keyStorageRegion = None
        self._initSecureBootSeqColor()

    def getBootDeviceConfiguration( self ):
        if self.bootDevice == uidef.kBootDevice_SemcNand:
            global g_semcNandOpt
            global g_semcNandFcbOpt
            global g_semcNandImageInfo
            self.semcNandOpt = g_semcNandOpt
            self.semcNandFcbOpt = g_semcNandFcbOpt
            self.semcNandImageInfo = g_semcNandImageInfo
        else:
            pass

    def runBootDeviceConfiguration( self ):
        if self.bootDevice == uidef.kBootDevice_SemcNand:
            semcNandFrame = secBootUiSemcNand(None)
            semcNandFrame.SetTitle(u"SEMC NAND Device Configuration")
            semcNandFrame.Show(True)
        else:
            pass

    def updateTargetSetupValue( self ):
        self.mcuSeries = self.m_choice_mcuSeries.GetString(self.m_choice_mcuSeries.GetSelection())
        self.mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())
        self.bootDevice = self.m_choice_bootDevice.GetString(self.m_choice_bootDevice.GetSelection())

    def _initPortSetupValue( self ):
        self.m_radioBtn_uart.SetValue(True)
        self.m_radioBtn_usbhid.SetValue(False)
        self.setPortSetupValue()

    def adjustPortSetupValue( self, connectStage=uidef.kConnectStage_Rom, usbIdList=[] ):
        self.isUartPortSelected = self.m_radioBtn_uart.GetValue()
        self.isUsbhidPortSelected = self.m_radioBtn_usbhid.GetValue()
        self.m_choice_portVid.Clear()
        self.m_choice_baudPid.Clear()
        if self.isUartPortSelected:
            self.m_staticText_portVid.SetLabel('COM Port:')
            self.m_staticText_baudPid.SetLabel('Baudrate:')
            # Auto detect available ports
            comports = list(serial.tools.list_ports.comports())
            ports = [None] * len(comports)
            for i in range(len(comports)):
                comport = list(comports[i])
                ports[i] = comport[0]
            self.m_choice_portVid.SetItems(ports)
            if connectStage == uidef.kConnectStage_Rom:
                self.m_choice_baudPid.SetItems(rundef.kUartSpeed_Sdphost)
            elif connectStage == uidef.kConnectStage_Flashloader:
                self.m_choice_baudPid.SetItems(rundef.kUartSpeed_Blhost)
            else:
                pass
        elif self.isUsbhidPortSelected:
            self.m_staticText_portVid.SetLabel('VID:')
            self.m_staticText_baudPid.SetLabel('PID:')
            usbVid = [None]
            usbPid = [None]
            if connectStage == uidef.kConnectStage_Rom:
                usbVid[0] = usbIdList[0]
                usbPid[0] = usbIdList[1]
                self.m_choice_portVid.SetItems(usbVid)
                self.m_choice_baudPid.SetItems(usbPid)
            elif connectStage == uidef.kConnectStage_Flashloader:
                usbVid[0] = usbIdList[2]
                usbPid[0] = usbIdList[3]
                self.m_choice_portVid.SetItems(usbVid)
                self.m_choice_baudPid.SetItems(usbPid)
            else:
                pass
        else:
            pass
        self.m_choice_portVid.SetSelection(0)
        self.m_choice_baudPid.SetSelection(0)

    def setPortSetupValue( self, connectStage=uidef.kConnectStage_Rom, usbIdList=[] ):
        self.adjustPortSetupValue(connectStage, usbIdList)
        self.updatePortSetupValue()

    def updatePortSetupValue( self ):
        self.isUartPortSelected = self.m_radioBtn_uart.GetValue()
        self.isUsbhidPortSelected = self.m_radioBtn_usbhid.GetValue()
        if self.isUartPortSelected:
            self.uartComPort = self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection())
            self.uartBaudrate = self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection())
        elif self.isUsbhidPortSelected:
            self.usbhidVid = self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection())
            self.usbhidPid = self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection())
        else:
            pass

    def updateConnectStatus( self, color='black' ):
        if color == 'black':
            self.m_button_connect.SetLabel('Connect to ROM')
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_black.png", wx.BITMAP_TYPE_ANY ))
        elif color == 'yellow':
            self.m_button_connect.SetLabel('Connect to Flashloader')
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_yellow.png", wx.BITMAP_TYPE_ANY ))
        elif color == 'green':
            self.m_button_connect.SetLabel('Configure boot device')
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_green.png", wx.BITMAP_TYPE_ANY ))
        elif color == 'blue':
            self.m_button_connect.SetLabel('Reset device')
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_blue.png", wx.BITMAP_TYPE_ANY ))
        elif color == 'red':
            self.m_button_connect.SetLabel('Reconnect')
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_red.png", wx.BITMAP_TYPE_ANY ))
        else:
            pass

    def _initSecureBootSeqColor ( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.keyStorageRegion = self.m_choice_keyStorageRegion.GetString(self.m_choice_keyStorageRegion.GetSelection())
        self.setSecureBootSeqColor()

    def _resetSecureBootSeqColor( self ):
        self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_progDek1_showDek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self._resetKeyStorageRegionColor()
        self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.Refresh()

    def _resetKeyStorageRegionColor( self ):
        self.m_panel_prepBee1_beeKeyRegion.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_prepBee2_beeKeyInput.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_prepBee3_advKeySettings.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_prepBee4_beeCryptoAlgo.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_operBeeKey1_readOtpmk.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.Refresh()

    def setSecureBootSeqColor( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self._resetSecureBootSeqColor()
        if self.secureBootType == uidef.kSecureBootType_Development:
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
        elif self.secureBootType == uidef.kSecureBootType_HabAuth:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
        elif self.secureBootType == uidef.kSecureBootType_HabCrypto:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_progDek1_showDek.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
        elif self.secureBootType == uidef.kSecureBootType_BeeCrypto:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Inactive )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Inactive )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Inactive )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.setKeyStorageRegionColor()
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
        else:
            pass
        self.Refresh()

    def setKeyStorageRegionColor( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto:
            self._resetKeyStorageRegionColor()
            self.keyStorageRegion = self.m_choice_keyStorageRegion.GetString(self.m_choice_keyStorageRegion.GetSelection())
            self.m_panel_prepBee1_beeKeyRegion.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_prepBee4_beeCryptoAlgo.SetBackgroundColour( uidef.kBootSeqColor_Active )
            if self.keyStorageRegion == uidef.kKeyStorageRegion_Optmk:
                self.m_panel_operBeeKey1_readOtpmk.SetBackgroundColour( uidef.kBootSeqColor_Active )
            elif self.keyStorageRegion == uidef.kKeyStorageRegion_Gp4 or keyStorageRegion == uidef.kKeyStorageRegion_SwGp2:
                self.m_panel_prepBee2_beeKeyInput.SetBackgroundColour( uidef.kBootSeqColor_Active )
                self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.kBootSeqColor_Active )
            elif self.keyStorageRegion == uidef.kKeyStorageRegion_Gp4SwGp2:
                self.m_panel_prepBee3_advKeySettings.SetBackgroundColour( uidef.kBootSeqColor_Active )
                self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.kBootSeqColor_Active )
            else:
                pass
        self.Refresh()

