#! /usr/bin/env python
import wx
import sys
import os
import serial.tools.list_ports
import uidef
sys.path.append(os.path.abspath("../.."))
from gui import nxpSecBoot
sys.path.append(os.path.abspath(".."))
from run import rundef

class secBootUi(nxpSecBoot.secBootWin):

    def __init__(self, parent):
        nxpSecBoot.secBootWin.__init__(self, parent)
        self.m_bitmap_nxp.SetBitmap(wx.Bitmap( u"../img/logo_nxp.png", wx.BITMAP_TYPE_ANY ))
        self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_black.png", wx.BITMAP_TYPE_ANY ))

        self.mcuSeries = None
        self.mcuDevice = None
        self.bootDevice = None
        self.updateTargetSetupValue()

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

    def updateTargetSetupValue( self ):
        self.mcuSeries = self.m_choice_mcuSeries.GetString(self.m_choice_mcuSeries.GetSelection())
        self.mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())
        self.bootDevice = self.m_choice_bootDevice.GetString(self.m_choice_bootDevice.GetSelection())

    def _initPortSetupValue( self ):
        self.m_radioBtn_uart.SetValue(True)
        self.m_radioBtn_usbhid.SetValue(False)
        self.setPortSetupValue()

    def adjustPortSetupValue( self, connectStage=uidef.CONNECT_STAGE_ROM ):
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
            if connectStage == uidef.CONNECT_STAGE_ROM:
                self.m_choice_baudPid.SetItems(rundef.SDPHOST_UART_SPEED)
            elif connectStage == uidef.CONNECT_STAGE_FLASHLOADER:
                self.m_choice_baudPid.SetItems(rundef.BLHOST_UART_SPEED)
            else:
                pass
        elif self.isUsbhidPortSelected:
            self.m_staticText_portVid.SetLabel('VID:')
            self.m_staticText_baudPid.SetLabel('PID:')
            if connectStage == uidef.CONNECT_STAGE_ROM:
                self.m_choice_portVid.SetItems(rundef.SDPHOST_USBHID_VID)
                self.m_choice_baudPid.SetItems(rundef.SDPHOST_USBHID_PID)
            elif connectStage == uidef.CONNECT_STAGE_FLASHLOADER:
                self.m_choice_portVid.SetItems(rundef.BLHOST_USBHID_VID)
                self.m_choice_baudPid.SetItems(rundef.BLHOST_USBHID_PID)
            else:
                pass
        else:
            pass
        self.m_choice_portVid.SetSelection(0)
        self.m_choice_baudPid.SetSelection(0)

    def setPortSetupValue( self, connectStage=uidef.CONNECT_STAGE_ROM ):
        self.adjustPortSetupValue(connectStage)
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

    def _initSecureBootSeqColor ( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.keyStorageRegion = self.m_choice_keyStorageRegion.GetString(self.m_choice_keyStorageRegion.GetSelection())
        self.setSecureBootSeqColor()

    def _resetSecureBootSeqColor( self ):
        self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_progDek1_showDek.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self._resetKeyStorageRegionColor()
        self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.Refresh()

    def _resetKeyStorageRegionColor( self ):
        self.m_panel_prepBee1_beeKeyRegion.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_prepBee2_beeKeyInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_prepBee3_advKeySettings.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_prepBee4_beeCryptoAlgo.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_operBeeKey1_readOtpmk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.Refresh()

    def setSecureBootSeqColor( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self._resetSecureBootSeqColor()
        if self.secureBootType == uidef.SECURE_BOOT_TYPE_DEVELOPMENT:
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
        elif self.secureBootType == uidef.SECURE_BOOT_TYPE_HAB_AUTH:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
        elif self.secureBootType == uidef.SECURE_BOOT_TYPE_HAB_CRYPTO:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_progDek1_showDek.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
        elif self.secureBootType == uidef.SECURE_BOOT_TYPE_BEE_CRYPTO:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INACTIVE )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INACTIVE )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INACTIVE )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.setKeyStorageRegionColor()
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
        else:
            pass
        self.Refresh()

    def setKeyStorageRegionColor( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        if self.secureBootType == uidef.SECURE_BOOT_TYPE_BEE_CRYPTO:
            self._resetKeyStorageRegionColor()
            self.keyStorageRegion = self.m_choice_keyStorageRegion.GetString(self.m_choice_keyStorageRegion.GetSelection())
            self.m_panel_prepBee1_beeKeyRegion.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_prepBee4_beeCryptoAlgo.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            if self.keyStorageRegion == uidef.KEY_STORAGE_REGION_OPTMK:
                self.m_panel_operBeeKey1_readOtpmk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            elif self.keyStorageRegion == uidef.KEY_STORAGE_REGION_GP4 or keyStorageRegion == uidef.KEY_STORAGE_REGION_SW_GP2:
                self.m_panel_prepBee2_beeKeyInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
                self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            elif self.keyStorageRegion == uidef.KEY_STORAGE_REGION_GP4_SW_GP2:
                self.m_panel_prepBee3_advKeySettings.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
                self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            else:
                pass
        self.Refresh()

