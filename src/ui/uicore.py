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
from fuse import fusedef

s_isGaugeWorking = False
s_curGauge = 0
s_maxGauge = 0

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

    def popupMsgBox( self, msgStr ):
        messageText = (msgStr)
        wx.MessageBox(messageText, "Error", wx.OK | wx.ICON_INFORMATION)

    def printLog( self, logStr ):
        self.m_textCtrl_log.write(logStr + "\n")

    def clearLog( self ):
        self.m_textCtrl_log.Clear()

    def increaseGauge( self, evt ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        if s_isGaugeWorking:
            if s_curGauge < (s_maxGauge - 10):
                self.m_gauge_action.SetValue(s_curGauge)
                s_curGauge += 1
                #wx.CallLater(100, self.increaseGauge)

    def initGauge( self ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        s_isGaugeWorking = True
        s_curGauge = 30
        s_maxGauge = self.m_gauge_action.GetRange()
        self.m_gauge_action.SetValue(s_curGauge)

    def deinitGauge( self ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        s_isGaugeWorking = False
        s_curGauge = s_maxGauge
        self.m_gauge_action.SetValue(s_maxGauge)

    def printDeviceStatus( self, statusStr ):
        self.m_textCtrl_deviceStatus.write(statusStr + "\n")

    def clearDeviceStatus( self ):
        self.m_textCtrl_deviceStatus.Clear()

    def showMatchBdFilePath( self, bdPath ):
        self.m_textCtrl_bdPath.Clear()
        self.m_textCtrl_bdPath.write(bdPath)

    def getUserAppFilePath( self ):
        return self.m_filePicker_appPath.GetPath()

    def printSrkData( self, srkStr ):
        self.m_textCtrl_srk256bit.write(srkStr + "\n")

    def clearSrkData( self ):
        self.m_textCtrl_srk256bit.Clear()

    def printHabDekData( self, dekStr ):
        self.m_textCtrl_habDek128bit.write(dekStr + "\n")

    def clearHabDekData( self ):
        self.m_textCtrl_habDek128bit.Clear()

    def printOtpmkDekData( self, dekStr ):
        self.m_textCtrl_otpmkDek128bit.write(dekStr + "\n")

    def clearOtpmkDekData( self ):
        self.m_textCtrl_otpmkDek128bit.Clear()

    def printGp4DekData( self, dekStr ):
        self.m_textCtrl_gp4Dek128bit.write(dekStr + "\n")

    def clearGp4DekData( self ):
        self.m_textCtrl_gp4Dek128bit.Clear()

    def printSwGp2DekData( self, dekStr ):
        self.m_textCtrl_swgp2Dek128bit.write(dekStr + "\n")

    def clearSwGp2DekData( self ):
        self.m_textCtrl_swgp2Dek128bit.Clear()

    def printMem( self , memStr ):
        self.m_textCtrl_bootDeviceMem.write(memStr + "\n")

    def clearMem( self ):
        self.m_textCtrl_bootDeviceMem.Clear()

    def _parseReadFuseValue( self, fuseValue ):
        if fuseValue != None:
            result = str(hex(fuseValue))
            if result[len(result) - 1] != 'L':
                return result
            else:
                return result[0:len(result) - 1]
        else:
            return '--------'

    def showScannedFuses( self , scannedFuseList ):
        self.m_textCtrl_fuse400.Clear()
        self.m_textCtrl_fuse400.write(self._parseReadFuseValue(scannedFuseList[0]))
        self.m_textCtrl_fuse410.Clear()
        self.m_textCtrl_fuse410.write(self._parseReadFuseValue(scannedFuseList[1]))
        self.m_textCtrl_fuse420.Clear()
        self.m_textCtrl_fuse420.write(self._parseReadFuseValue(scannedFuseList[2]))
        self.m_textCtrl_fuse430.Clear()
        self.m_textCtrl_fuse430.write(self._parseReadFuseValue(scannedFuseList[3]))
        self.m_textCtrl_fuse440.Clear()
        self.m_textCtrl_fuse440.write(self._parseReadFuseValue(scannedFuseList[4]))
        self.m_textCtrl_fuse450.Clear()
        self.m_textCtrl_fuse450.write(self._parseReadFuseValue(scannedFuseList[5]))
        self.m_textCtrl_fuse460.Clear()
        self.m_textCtrl_fuse460.write(self._parseReadFuseValue(scannedFuseList[6]))
        self.m_textCtrl_fuse470.Clear()
        self.m_textCtrl_fuse470.write(self._parseReadFuseValue(scannedFuseList[7]))
        self.m_textCtrl_fuse480.Clear()
        self.m_textCtrl_fuse480.write(self._parseReadFuseValue(scannedFuseList[8]))
        self.m_textCtrl_fuse490.Clear()
        self.m_textCtrl_fuse490.write(self._parseReadFuseValue(scannedFuseList[9]))
        self.m_textCtrl_fuse4a0.Clear()
        self.m_textCtrl_fuse4a0.write(self._parseReadFuseValue(scannedFuseList[10]))
        self.m_textCtrl_fuse4b0.Clear()
        self.m_textCtrl_fuse4b0.write(self._parseReadFuseValue(scannedFuseList[11]))
        self.m_textCtrl_fuse4c0.Clear()
        self.m_textCtrl_fuse4c0.write(self._parseReadFuseValue(scannedFuseList[12]))
        self.m_textCtrl_fuse4d0.Clear()
        self.m_textCtrl_fuse4d0.write(self._parseReadFuseValue(scannedFuseList[13]))
        self.m_textCtrl_fuse4e0.Clear()
        self.m_textCtrl_fuse4e0.write(self._parseReadFuseValue(scannedFuseList[14]))
        self.m_textCtrl_fuse4f0.Clear()
        self.m_textCtrl_fuse4f0.write(self._parseReadFuseValue(scannedFuseList[15]))

        self.m_textCtrl_fuse500.Clear()
        self.m_textCtrl_fuse500.write(self._parseReadFuseValue(scannedFuseList[16]))
        self.m_textCtrl_fuse510.Clear()
        self.m_textCtrl_fuse510.write(self._parseReadFuseValue(scannedFuseList[17]))
        self.m_textCtrl_fuse520.Clear()
        self.m_textCtrl_fuse520.write(self._parseReadFuseValue(scannedFuseList[18]))
        self.m_textCtrl_fuse530.Clear()
        self.m_textCtrl_fuse530.write(self._parseReadFuseValue(scannedFuseList[19]))
        self.m_textCtrl_fuse540.Clear()
        self.m_textCtrl_fuse540.write(self._parseReadFuseValue(scannedFuseList[20]))
        self.m_textCtrl_fuse550.Clear()
        self.m_textCtrl_fuse550.write(self._parseReadFuseValue(scannedFuseList[21]))
        self.m_textCtrl_fuse560.Clear()
        self.m_textCtrl_fuse560.write(self._parseReadFuseValue(scannedFuseList[22]))
        self.m_textCtrl_fuse570.Clear()
        self.m_textCtrl_fuse570.write(self._parseReadFuseValue(scannedFuseList[23]))
        self.m_textCtrl_fuse580.Clear()
        self.m_textCtrl_fuse580.write(self._parseReadFuseValue(scannedFuseList[24]))
        self.m_textCtrl_fuse590.Clear()
        self.m_textCtrl_fuse590.write(self._parseReadFuseValue(scannedFuseList[25]))
        self.m_textCtrl_fuse5a0.Clear()
        self.m_textCtrl_fuse5a0.write(self._parseReadFuseValue(scannedFuseList[26]))
        self.m_textCtrl_fuse5b0.Clear()
        self.m_textCtrl_fuse5b0.write(self._parseReadFuseValue(scannedFuseList[27]))
        self.m_textCtrl_fuse5c0.Clear()
        self.m_textCtrl_fuse5c0.write(self._parseReadFuseValue(scannedFuseList[28]))
        self.m_textCtrl_fuse5d0.Clear()
        self.m_textCtrl_fuse5d0.write(self._parseReadFuseValue(scannedFuseList[29]))
        self.m_textCtrl_fuse5e0.Clear()
        self.m_textCtrl_fuse5e0.write(self._parseReadFuseValue(scannedFuseList[30]))
        self.m_textCtrl_fuse5f0.Clear()
        self.m_textCtrl_fuse5f0.write(self._parseReadFuseValue(scannedFuseList[31]))

        self.m_textCtrl_fuse600.Clear()
        self.m_textCtrl_fuse600.write(self._parseReadFuseValue(scannedFuseList[32]))
        self.m_textCtrl_fuse610.Clear()
        self.m_textCtrl_fuse610.write(self._parseReadFuseValue(scannedFuseList[33]))
        self.m_textCtrl_fuse620.Clear()
        self.m_textCtrl_fuse620.write(self._parseReadFuseValue(scannedFuseList[34]))
        self.m_textCtrl_fuse630.Clear()
        self.m_textCtrl_fuse630.write(self._parseReadFuseValue(scannedFuseList[35]))
        self.m_textCtrl_fuse640.Clear()
        self.m_textCtrl_fuse640.write(self._parseReadFuseValue(scannedFuseList[36]))
        self.m_textCtrl_fuse650.Clear()
        self.m_textCtrl_fuse650.write(self._parseReadFuseValue(scannedFuseList[37]))
        self.m_textCtrl_fuse660.Clear()
        self.m_textCtrl_fuse660.write(self._parseReadFuseValue(scannedFuseList[38]))
        self.m_textCtrl_fuse670.Clear()
        self.m_textCtrl_fuse670.write(self._parseReadFuseValue(scannedFuseList[39]))
        self.m_textCtrl_fuse680.Clear()
        self.m_textCtrl_fuse680.write(self._parseReadFuseValue(scannedFuseList[40]))
        self.m_textCtrl_fuse690.Clear()
        self.m_textCtrl_fuse690.write(self._parseReadFuseValue(scannedFuseList[41]))
        self.m_textCtrl_fuse6a0.Clear()
        self.m_textCtrl_fuse6a0.write(self._parseReadFuseValue(scannedFuseList[42]))
        self.m_textCtrl_fuse6b0.Clear()
        self.m_textCtrl_fuse6b0.write(self._parseReadFuseValue(scannedFuseList[43]))
        self.m_textCtrl_fuse6c0.Clear()
        self.m_textCtrl_fuse6c0.write(self._parseReadFuseValue(scannedFuseList[44]))
        self.m_textCtrl_fuse6d0.Clear()
        self.m_textCtrl_fuse6d0.write(self._parseReadFuseValue(scannedFuseList[45]))
        self.m_textCtrl_fuse6e0.Clear()
        self.m_textCtrl_fuse6e0.write(self._parseReadFuseValue(scannedFuseList[46]))
        self.m_textCtrl_fuse6f0.Clear()
        self.m_textCtrl_fuse6f0.write(self._parseReadFuseValue(scannedFuseList[47]))

        self.m_textCtrl_fuse700.Clear()
        self.m_textCtrl_fuse700.write(self._parseReadFuseValue(scannedFuseList[48]))
        self.m_textCtrl_fuse710.Clear()
        self.m_textCtrl_fuse710.write(self._parseReadFuseValue(scannedFuseList[49]))
        self.m_textCtrl_fuse720.Clear()
        self.m_textCtrl_fuse720.write(self._parseReadFuseValue(scannedFuseList[50]))
        self.m_textCtrl_fuse730.Clear()
        self.m_textCtrl_fuse730.write(self._parseReadFuseValue(scannedFuseList[51]))
        self.m_textCtrl_fuse740.Clear()
        self.m_textCtrl_fuse740.write(self._parseReadFuseValue(scannedFuseList[52]))
        self.m_textCtrl_fuse750.Clear()
        self.m_textCtrl_fuse750.write(self._parseReadFuseValue(scannedFuseList[53]))
        self.m_textCtrl_fuse760.Clear()
        self.m_textCtrl_fuse760.write(self._parseReadFuseValue(scannedFuseList[54]))
        self.m_textCtrl_fuse770.Clear()
        self.m_textCtrl_fuse770.write(self._parseReadFuseValue(scannedFuseList[55]))
        self.m_textCtrl_fuse780.Clear()
        self.m_textCtrl_fuse780.write(self._parseReadFuseValue(scannedFuseList[56]))
        self.m_textCtrl_fuse790.Clear()
        self.m_textCtrl_fuse790.write(self._parseReadFuseValue(scannedFuseList[57]))
        self.m_textCtrl_fuse7a0.Clear()
        self.m_textCtrl_fuse7a0.write(self._parseReadFuseValue(scannedFuseList[58]))
        self.m_textCtrl_fuse7b0.Clear()
        self.m_textCtrl_fuse7b0.write(self._parseReadFuseValue(scannedFuseList[59]))
        self.m_textCtrl_fuse7c0.Clear()
        self.m_textCtrl_fuse7c0.write(self._parseReadFuseValue(scannedFuseList[60]))
        self.m_textCtrl_fuse7d0.Clear()
        self.m_textCtrl_fuse7d0.write(self._parseReadFuseValue(scannedFuseList[61]))
        self.m_textCtrl_fuse7e0.Clear()
        self.m_textCtrl_fuse7e0.write(self._parseReadFuseValue(scannedFuseList[62]))
        self.m_textCtrl_fuse7f0.Clear()
        self.m_textCtrl_fuse7f0.write(self._parseReadFuseValue(scannedFuseList[63]))

        self.m_textCtrl_fuse800.Clear()
        self.m_textCtrl_fuse800.write(self._parseReadFuseValue(scannedFuseList[64]))
        self.m_textCtrl_fuse810.Clear()
        self.m_textCtrl_fuse810.write(self._parseReadFuseValue(scannedFuseList[65]))
        self.m_textCtrl_fuse820.Clear()
        self.m_textCtrl_fuse820.write(self._parseReadFuseValue(scannedFuseList[66]))
        self.m_textCtrl_fuse830.Clear()
        self.m_textCtrl_fuse830.write(self._parseReadFuseValue(scannedFuseList[67]))
        self.m_textCtrl_fuse840.Clear()
        self.m_textCtrl_fuse840.write(self._parseReadFuseValue(scannedFuseList[68]))
        self.m_textCtrl_fuse850.Clear()
        self.m_textCtrl_fuse850.write(self._parseReadFuseValue(scannedFuseList[69]))
        self.m_textCtrl_fuse860.Clear()
        self.m_textCtrl_fuse860.write(self._parseReadFuseValue(scannedFuseList[70]))
        self.m_textCtrl_fuse870.Clear()
        self.m_textCtrl_fuse870.write(self._parseReadFuseValue(scannedFuseList[71]))
        self.m_textCtrl_fuse880.Clear()
        self.m_textCtrl_fuse880.write(self._parseReadFuseValue(scannedFuseList[72]))
        self.m_textCtrl_fuse890.Clear()
        self.m_textCtrl_fuse890.write(self._parseReadFuseValue(scannedFuseList[73]))
        self.m_textCtrl_fuse8a0.Clear()
        self.m_textCtrl_fuse8a0.write(self._parseReadFuseValue(scannedFuseList[74]))
        self.m_textCtrl_fuse8b0.Clear()
        self.m_textCtrl_fuse8b0.write(self._parseReadFuseValue(scannedFuseList[75]))
        self.m_textCtrl_fuse8c0.Clear()
        self.m_textCtrl_fuse8c0.write(self._parseReadFuseValue(scannedFuseList[76]))
        self.m_textCtrl_fuse8d0.Clear()
        self.m_textCtrl_fuse8d0.write(self._parseReadFuseValue(scannedFuseList[77]))
        self.m_textCtrl_fuse8e0.Clear()
        self.m_textCtrl_fuse8e0.write(self._parseReadFuseValue(scannedFuseList[78]))
        self.m_textCtrl_fuse8f0.Clear()
        self.m_textCtrl_fuse8f0.write(self._parseReadFuseValue(scannedFuseList[79]))

    def _parseUserFuseValue( self, fuseText ):
        if len(fuseText) >= 3 and fuseText[0:2] == '0x':
            return int(fuseText[2:len(fuseText)], 16)
        else:
            return None

    def getUserFuses( self ):
        userFuseList = [None] * fusedef.kMaxEfuseWords
        userFuseList[0] = self._parseUserFuseValue(self.m_textCtrl_fuse400.GetLineText(0))
        userFuseList[1] = self._parseUserFuseValue(self.m_textCtrl_fuse410.GetLineText(0))
        userFuseList[2] = self._parseUserFuseValue(self.m_textCtrl_fuse420.GetLineText(0))
        userFuseList[3] = self._parseUserFuseValue(self.m_textCtrl_fuse430.GetLineText(0))
        userFuseList[4] = self._parseUserFuseValue(self.m_textCtrl_fuse440.GetLineText(0))
        userFuseList[5] = self._parseUserFuseValue(self.m_textCtrl_fuse450.GetLineText(0))
        userFuseList[6] = self._parseUserFuseValue(self.m_textCtrl_fuse460.GetLineText(0))
        userFuseList[7] = self._parseUserFuseValue(self.m_textCtrl_fuse470.GetLineText(0))
        userFuseList[8] = self._parseUserFuseValue(self.m_textCtrl_fuse480.GetLineText(0))
        userFuseList[9] = self._parseUserFuseValue(self.m_textCtrl_fuse490.GetLineText(0))
        userFuseList[10] = self._parseUserFuseValue(self.m_textCtrl_fuse4a0.GetLineText(0))
        userFuseList[11] = self._parseUserFuseValue(self.m_textCtrl_fuse4b0.GetLineText(0))
        userFuseList[12] = self._parseUserFuseValue(self.m_textCtrl_fuse4c0.GetLineText(0))
        userFuseList[13] = self._parseUserFuseValue(self.m_textCtrl_fuse4d0.GetLineText(0))
        userFuseList[14] = self._parseUserFuseValue(self.m_textCtrl_fuse4e0.GetLineText(0))
        userFuseList[15] = self._parseUserFuseValue(self.m_textCtrl_fuse4f0.GetLineText(0))

        userFuseList[16] = self._parseUserFuseValue(self.m_textCtrl_fuse500.GetLineText(0))
        userFuseList[17] = self._parseUserFuseValue(self.m_textCtrl_fuse510.GetLineText(0))
        userFuseList[18] = self._parseUserFuseValue(self.m_textCtrl_fuse520.GetLineText(0))
        userFuseList[19] = self._parseUserFuseValue(self.m_textCtrl_fuse530.GetLineText(0))
        userFuseList[20] = self._parseUserFuseValue(self.m_textCtrl_fuse540.GetLineText(0))
        userFuseList[21] = self._parseUserFuseValue(self.m_textCtrl_fuse550.GetLineText(0))
        userFuseList[22] = self._parseUserFuseValue(self.m_textCtrl_fuse560.GetLineText(0))
        userFuseList[23] = self._parseUserFuseValue(self.m_textCtrl_fuse570.GetLineText(0))
        userFuseList[24] = self._parseUserFuseValue(self.m_textCtrl_fuse580.GetLineText(0))
        userFuseList[25] = self._parseUserFuseValue(self.m_textCtrl_fuse590.GetLineText(0))
        userFuseList[26] = self._parseUserFuseValue(self.m_textCtrl_fuse5a0.GetLineText(0))
        userFuseList[27] = self._parseUserFuseValue(self.m_textCtrl_fuse5b0.GetLineText(0))
        userFuseList[28] = self._parseUserFuseValue(self.m_textCtrl_fuse5c0.GetLineText(0))
        userFuseList[29] = self._parseUserFuseValue(self.m_textCtrl_fuse5d0.GetLineText(0))
        userFuseList[30] = self._parseUserFuseValue(self.m_textCtrl_fuse5e0.GetLineText(0))
        userFuseList[31] = self._parseUserFuseValue(self.m_textCtrl_fuse5f0.GetLineText(0))

        userFuseList[32] = self._parseUserFuseValue(self.m_textCtrl_fuse600.GetLineText(0))
        userFuseList[33] = self._parseUserFuseValue(self.m_textCtrl_fuse610.GetLineText(0))
        userFuseList[34] = self._parseUserFuseValue(self.m_textCtrl_fuse620.GetLineText(0))
        userFuseList[35] = self._parseUserFuseValue(self.m_textCtrl_fuse630.GetLineText(0))
        userFuseList[36] = self._parseUserFuseValue(self.m_textCtrl_fuse640.GetLineText(0))
        userFuseList[37] = self._parseUserFuseValue(self.m_textCtrl_fuse650.GetLineText(0))
        userFuseList[38] = self._parseUserFuseValue(self.m_textCtrl_fuse660.GetLineText(0))
        userFuseList[39] = self._parseUserFuseValue(self.m_textCtrl_fuse670.GetLineText(0))
        userFuseList[40] = self._parseUserFuseValue(self.m_textCtrl_fuse680.GetLineText(0))
        userFuseList[41] = self._parseUserFuseValue(self.m_textCtrl_fuse690.GetLineText(0))
        userFuseList[42] = self._parseUserFuseValue(self.m_textCtrl_fuse6a0.GetLineText(0))
        userFuseList[43] = self._parseUserFuseValue(self.m_textCtrl_fuse6b0.GetLineText(0))
        userFuseList[44] = self._parseUserFuseValue(self.m_textCtrl_fuse6c0.GetLineText(0))
        userFuseList[45] = self._parseUserFuseValue(self.m_textCtrl_fuse6d0.GetLineText(0))
        userFuseList[46] = self._parseUserFuseValue(self.m_textCtrl_fuse6e0.GetLineText(0))
        userFuseList[47] = self._parseUserFuseValue(self.m_textCtrl_fuse6f0.GetLineText(0))

        userFuseList[48] = self._parseUserFuseValue(self.m_textCtrl_fuse700.GetLineText(0))
        userFuseList[49] = self._parseUserFuseValue(self.m_textCtrl_fuse710.GetLineText(0))
        userFuseList[50] = self._parseUserFuseValue(self.m_textCtrl_fuse720.GetLineText(0))
        userFuseList[51] = self._parseUserFuseValue(self.m_textCtrl_fuse730.GetLineText(0))
        userFuseList[52] = self._parseUserFuseValue(self.m_textCtrl_fuse730.GetLineText(0))
        userFuseList[53] = self._parseUserFuseValue(self.m_textCtrl_fuse750.GetLineText(0))
        userFuseList[54] = self._parseUserFuseValue(self.m_textCtrl_fuse760.GetLineText(0))
        userFuseList[55] = self._parseUserFuseValue(self.m_textCtrl_fuse770.GetLineText(0))
        userFuseList[56] = self._parseUserFuseValue(self.m_textCtrl_fuse780.GetLineText(0))
        userFuseList[57] = self._parseUserFuseValue(self.m_textCtrl_fuse790.GetLineText(0))
        userFuseList[58] = self._parseUserFuseValue(self.m_textCtrl_fuse7a0.GetLineText(0))
        userFuseList[59] = self._parseUserFuseValue(self.m_textCtrl_fuse7b0.GetLineText(0))
        userFuseList[60] = self._parseUserFuseValue(self.m_textCtrl_fuse7c0.GetLineText(0))
        userFuseList[61] = self._parseUserFuseValue(self.m_textCtrl_fuse7d0.GetLineText(0))
        userFuseList[62] = self._parseUserFuseValue(self.m_textCtrl_fuse7e0.GetLineText(0))
        userFuseList[63] = self._parseUserFuseValue(self.m_textCtrl_fuse7f0.GetLineText(0))

        userFuseList[64] = self._parseUserFuseValue(self.m_textCtrl_fuse800.GetLineText(0))
        userFuseList[65] = self._parseUserFuseValue(self.m_textCtrl_fuse810.GetLineText(0))
        userFuseList[66] = self._parseUserFuseValue(self.m_textCtrl_fuse820.GetLineText(0))
        userFuseList[67] = self._parseUserFuseValue(self.m_textCtrl_fuse830.GetLineText(0))
        userFuseList[68] = self._parseUserFuseValue(self.m_textCtrl_fuse840.GetLineText(0))
        userFuseList[69] = self._parseUserFuseValue(self.m_textCtrl_fuse850.GetLineText(0))
        userFuseList[70] = self._parseUserFuseValue(self.m_textCtrl_fuse860.GetLineText(0))
        userFuseList[71] = self._parseUserFuseValue(self.m_textCtrl_fuse870.GetLineText(0))
        userFuseList[72] = self._parseUserFuseValue(self.m_textCtrl_fuse880.GetLineText(0))
        userFuseList[73] = self._parseUserFuseValue(self.m_textCtrl_fuse890.GetLineText(0))
        userFuseList[74] = self._parseUserFuseValue(self.m_textCtrl_fuse8a0.GetLineText(0))
        userFuseList[75] = self._parseUserFuseValue(self.m_textCtrl_fuse8b0.GetLineText(0))
        userFuseList[76] = self._parseUserFuseValue(self.m_textCtrl_fuse8c0.GetLineText(0))
        userFuseList[77] = self._parseUserFuseValue(self.m_textCtrl_fuse8d0.GetLineText(0))
        userFuseList[78] = self._parseUserFuseValue(self.m_textCtrl_fuse8e0.GetLineText(0))
        userFuseList[79] = self._parseUserFuseValue(self.m_textCtrl_fuse8f0.GetLineText(0))

        return userFuseList
