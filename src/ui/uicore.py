#! /usr/bin/env python
import wx
import sys
import os
import serial.tools.list_ports
import uidef
import uivar
sys.path.append(os.path.abspath("../.."))
from gui import secBootWin
sys.path.append(os.path.abspath(".."))
from run import rundef

g_semcNandOpt = 0xD0000000
g_semcNandFcbOpt = 0x00000000
g_semcNandImageInfo = [None] * 8

class secBootUi(secBootWin.secBootWin):

    def __init__(self, parent):
        secBootWin.secBootWin.__init__(self, parent)
        self.m_bitmap_nxp.SetBitmap(wx.Bitmap( u"../img/logo_nxp.png", wx.BITMAP_TYPE_ANY ))
        self.updateConnectStatus()

        self.mcuSeries = None
        self.mcuDevice = None
        self.bootDevice = None
        self.setTargetSetupValue()
        uivar.initVar()

        self.isUartPortSelected = None
        self.isUsbhidPortSelected = None
        self.uartComPort = None
        self.uartBaudrate = None
        self.usbhidVid = None
        self.usbhidPid = None
        self._initPortSetupValue()
        self.isOneStepConnectMode = None
        self.getOneStepConnectMode()

        self.secureBootType = None
        self.keyStorageRegion = None
        self.isCertEnabledForBee = None
        self._initSecureBootSeqColor()

    def setTargetSetupValue( self ):
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
        os.chdir(os.path.join(os.path.dirname(os.path.dirname(__file__))))
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

    def getOneStepConnectMode( self ):
        self.isOneStepConnectMode = self.m_checkBox_oneStepConnect.GetValue()

    def _initSecureBootSeqColor ( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.keyStorageRegion = self.m_choice_keyStorageRegion.GetString(self.m_choice_keyStorageRegion.GetSelection())
        self.setSecureBootSeqColor()

    def _resetSecureBootSeqColor( self ):
        self._resetCertificateColor()
        self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_genImage3_enableCertForBee.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self._resetKeyStorageRegionColor()
        self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_progDek1_showHabDek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.Refresh()

    def _resetKeyStorageRegionColor( self ):
        self.m_panel_prepBee1_beeKeyRegion.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_prepBee2_showOtpmkDek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_prepBee3_advKeySettings.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_operBee1_beeKeyInfo.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_operBee2_showGp4Dek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_operBee3_showSwgp2Dek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.Refresh()

    def _resetCertificateColor( self ):
        self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.Refresh()

    def setSecureBootSeqColor( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self._resetSecureBootSeqColor()
        if self.secureBootType == uidef.kSecureBootType_Development:
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_genImage.SetLabel('Generate Unsigned Bootable Image')
            self.m_button_flashImage.SetLabel('Load Unsigned Image')
        elif self.secureBootType == uidef.kSecureBootType_HabAuth:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_genImage.SetLabel('Generate Signed Bootable Image')
            self.m_button_flashImage.SetLabel('Load Signed Image')
        elif self.secureBootType == uidef.kSecureBootType_HabCrypto:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_progDek1_showHabDek.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_genImage.SetLabel('Generate Encrypted Bootable Image,DEK')
            self.m_button_flashImage.SetLabel('Load HAB Encrypted Image')
        elif self.secureBootType == uidef.kSecureBootType_BeeCrypto:
            if self.bootDevice == uidef.kBootDevice_FlexspiNor:
                self.setBeeCertColor()
                self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
                self.m_panel_genImage3_enableCertForBee.SetBackgroundColour( uidef.kBootSeqColor_Active )
                self.setKeyStorageRegionColor()
                self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
                if self.isCertEnabledForBee:
                    self.m_button_genImage.SetLabel('Generate Signed Bootable Image')
                else:
                    self.m_button_genImage.SetLabel('Generate Unsigned Bootable Image')
                self.m_button_flashImage.SetLabel('Load Image, Burn BEE_KEYx_SEL')
            else:
                self._resetSecureBootSeqColor()
        else:
            pass
        self.Refresh()

    def getSerialAndKeypassContent( self ):
        serialContent = self.m_textCtrl_serial.GetLineText(0)
        keypassContent = self.m_textCtrl_keyPass.GetLineText(0)
        return serialContent, keypassContent

    def setBeeCertColor( self ):
        txt = self.m_choice_enableCertForBee.GetString(self.m_choice_enableCertForBee.GetSelection())
        if txt == 'No':
            self.isCertEnabledForBee = False
        elif txt == 'Yes':
            self.isCertEnabledForBee = True
        else:
            pass
        self._resetCertificateColor()
        if self.isCertEnabledForBee:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Optional )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Optional )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Optional )
        self.Refresh()

    def setKeyStorageRegionColor( self ):
        self.keyStorageRegion = self.m_choice_keyStorageRegion.GetString(self.m_choice_keyStorageRegion.GetSelection())
        self._resetKeyStorageRegionColor()
        self.m_panel_prepBee1_beeKeyRegion.SetBackgroundColour( uidef.kBootSeqColor_Active )
        self.m_panel_prepBee3_advKeySettings.SetBackgroundColour( uidef.kBootSeqColor_Active )
        if self.keyStorageRegion == uidef.kKeyStorageRegion_FixedOtpmkKey:
            self.m_panel_prepBee2_showOtpmkDek.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_prepBee.SetLabel('Prepare For Encryption')
        elif self.keyStorageRegion == uidef.kKeyStorageRegion_FlexibleUserKeys:
            self.m_panel_prepBee2_showOtpmkDek.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_operBee1_beeKeyInfo.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_operBee2_showGp4Dek.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_panel_operBee3_showSwgp2Dek.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_prepBee.SetLabel('Encrypt Bootable Image')
        else:
            pass
        self.Refresh()
