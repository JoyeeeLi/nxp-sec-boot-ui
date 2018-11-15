#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
from mem import memcore
from ui import uidef
from fuse import fusedef
from ui import ui_cfg_flexspinor
from ui import ui_cfg_flexspinand
from ui import ui_cfg_semcnor
from ui import ui_cfg_semcnand
from ui import ui_cfg_usdhcsd
from ui import ui_cfg_usdhcmmc
from ui import ui_settings_cert
from ui import ui_settings_fixed_otpmk_key
from ui import ui_settings_flexible_user_keys

kRetryPingTimes = 5

kBootloaderType_Rom         = 0
kBootloaderType_Flashloader = 1

class secBootMain(memcore.secBootMem):

    def __init__(self, parent):
        memcore.secBootMem.__init__(self, parent)
        self.connectStage = uidef.kConnectStage_Rom
        self.gaugeTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.increaseGauge, self.gaugeTimer)

    def _startGaugeTimer( self ):
        self.initGauge()
        #self.gaugeTimer.Start(500) # ms

    def _stopGaugeTimer( self ):
        #self.gaugeTimer.Stop()
        self.deinitGauge()

    def callbackSetMcuSeries( self, event ):
        self.setTargetSetupValue()

    def callbackSetMcuDevice( self, event ):
        self.setTargetSetupValue()
        usbIdList = self.getUsbid()
        self.adjustPortSetupValue(self.connectStage, usbIdList)

    def callbackSetBootDevice( self, event ):
        self.setTargetSetupValue()
        self.setSecureBootSeqColor()

    def callbackBootDeviceConfiguration( self, event ):
        if self.bootDevice == uidef.kBootDevice_FlexspiNor:
            flexspiNorFrame = ui_cfg_flexspinor.secBootUiCfgFlexspiNor(None)
            flexspiNorFrame.SetTitle(u"FlexSPI NOR Device Configuration")
            flexspiNorFrame.Show(True)
        elif self.bootDevice == uidef.kBootDevice_FlexspiNand:
            flexspiNandFrame = ui_cfg_flexspinand.secBootUiFlexspiNand(None)
            flexspiNandFrame.SetTitle(u"FlexSPI NAND Device Configuration")
            flexspiNandFrame.Show(True)
        elif self.bootDevice == uidef.kBootDevice_SemcNor:
            semcNorFrame = ui_cfg_semcnor.secBootUiSemcNor(None)
            semcNorFrame.SetTitle(u"SEMC NOR Device Configuration")
            semcNorFrame.Show(True)
        elif self.bootDevice == uidef.kBootDevice_SemcNand:
            semcNandFrame = ui_cfg_semcnand.secBootUiCfgSemcNand(None)
            semcNandFrame.SetTitle(u"SEMC NAND Device Configuration")
            semcNandFrame.Show(True)
        elif self.bootDevice == uidef.kBootDevice_UsdhcSd:
            usdhcSdFrame = ui_cfg_usdhcsd.secBootUiUsdhcSd(None)
            usdhcSdFrame.SetTitle(u"uSDHC SD Device Configuration")
            usdhcSdFrame.Show(True)
        elif self.bootDevice == uidef.kBootDevice_UsdhcMmc:
            usdhcMmcFrame = ui_cfg_usdhcmmc.secBootUiUsdhcMmc(None)
            usdhcMmcFrame.SetTitle(u"uSDHC MMC Device Configuration")
            usdhcMmcFrame.Show(True)
        else:
            pass

    def callbackSetUartPort( self, event ):
        self.setPortSetupValue(self.connectStage)

    def callbackSetUsbhidPort( self, event ):
        usbIdList = self.getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList)

    def _retryToPingBootloader( self, bootType ):
        pingStatus = False
        pingCnt = kRetryPingTimes
        while (not pingStatus) and pingCnt > 0:
            if bootType == kBootloaderType_Rom:
                pingStatus = self.pingRom()
            elif bootType == kBootloaderType_Flashloader:
                pingStatus = self.pingFlashloader()
            else:
                pass
            pingCnt = pingCnt - 1
            if self.isUsbhidPortSelected:
                time.sleep(2)
        return pingStatus

    def _connectStateMachine( self ):
        connectSteps = uidef.kConnectStep_Normal
        self.getOneStepConnectMode()
        if self.isOneStepConnectMode and self.connectStage != uidef.kConnectStage_Reset:
            connectSteps = uidef.kConnectStep_Fast
        while connectSteps:
            self.updatePortSetupValue()
            if self.connectStage == uidef.kConnectStage_Rom:
                self.connectToDevice(self.connectStage)
                if self._retryToPingBootloader(kBootloaderType_Rom):
                    self.getMcuDeviceInfoViaRom()
                    self.getMcuDeviceHabStatus()
                    if self.jumpToFlashloader():
                        self.updateConnectStatus('yellow')
                        self.connectStage = uidef.kConnectStage_Flashloader
                        usbIdList = self.getUsbid()
                        self.adjustPortSetupValue(self.connectStage, usbIdList)
                    else:
                        self.updateConnectStatus('red')
                else:
                    self.updateConnectStatus('red')
                    self.popupMsgBox('Make sure that you have put MCU in Serial Downloader mode (BMOD[1:0] pins = 2\'b01)!')
            elif self.connectStage == uidef.kConnectStage_Flashloader:
                self.connectToDevice(self.connectStage)
                if self._retryToPingBootloader(kBootloaderType_Flashloader):
                    self.getMcuDeviceInfoViaFlashloader()
                    self.getMcuDeviceBtFuseSel()
                    self.updateConnectStatus('green')
                    self.connectStage = uidef.kConnectStage_ExternalMemory
                else:
                    self.updateConnectStatus('red')
            elif self.connectStage == uidef.kConnectStage_ExternalMemory:
                if self.configureBootDevice():
                    self.getBootDeviceInfoViaFlashloader()
                    self.connectStage = uidef.kConnectStage_Reset
                    self.updateConnectStatus('blue')
                else:
                    self.updateConnectStatus('red')
            elif self.connectStage == uidef.kConnectStage_Reset:
                self.resetMcuDevice()
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('black')
                usbIdList = self.getUsbid()
                self.adjustPortSetupValue(self.connectStage, usbIdList)
                self.connectToDevice(self.connectStage)
            else:
                pass
            connectSteps -= 1

    def callbackConnectToDevice( self, event ):
        self._startGaugeTimer()
        self.printLog("'Connect to xxx' button is clicked")
        self._connectStateMachine()
        self._stopGaugeTimer()

    def callbackSetSecureBootType( self, event ):
        self.setSecureBootSeqColor()

    def callbackAdvCertSettings( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice != uidef.kBootDevice_FlexspiNor:
            self.popupMsgBox('Action is not available because BEE encryption boot is only designed for FlexSPI NOR device!')
        elif self.secureBootType != uidef.kSecureBootType_Development:
            if self.secureBootType == uidef.kSecureBootType_BeeCrypto and (not self.isCertEnabledForBee):
                self.popupMsgBox('Certificate is not enabled for BEE, You can enable it then try again!')
            else:
                certSettingsFrame = ui_settings_cert.secBootUiSettingsCert(None)
                certSettingsFrame.SetTitle(u"Advanced Certificate Settings")
                certSettingsFrame.Show(True)
                self.updateAllCstPathToCorrectVersion()
        else:
            self.popupMsgBox('No need to set certificate option when booting unsigned image!')

    def callbackGenCert( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice != uidef.kBootDevice_FlexspiNor:
            self.popupMsgBox('Action is not available because BEE encryption boot is only designed for FlexSPI NOR device!')
        elif self.secureBootType != uidef.kSecureBootType_Development:
            if self.secureBootType == uidef.kSecureBootType_BeeCrypto and (not self.isCertEnabledForBee):
                self.popupMsgBox('Certificate is not enabled for BEE, You can enable it then try again!')
            else:
                self._startGaugeTimer()
                self.printLog("'Generate Certificate' button is clicked")
                self.updateAllCstPathToCorrectVersion()
                if self.createSerialAndKeypassfile():
                    self.genCertificate()
                    self.genSuperRootKeys()
                    self.showSuperRootKeys()
                self._stopGaugeTimer()
        else:
            self.popupMsgBox('No need to generate certificate when booting unsigned image!')

    def callbackGenImage( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice != uidef.kBootDevice_FlexspiNor:
            self.popupMsgBox('Action is not available because BEE encryption boot is only designed for FlexSPI NOR device!')
        else:
            self._startGaugeTimer()
            self.printLog("'Generate Bootable Image' button is clicked")
            if self.createMatchedAppBdfile():
                self.genBootableImage()
                self.showHabDekIfApplicable()
            self._stopGaugeTimer()

    def callbackSetCertForBee( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto:
            self.setBeeCertColor()

    def callbackSetKeyStorageRegion( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto:
            self.setKeyStorageRegionColor()

    def callbackAdvKeySettings( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice == uidef.kBootDevice_FlexspiNor:
            if self.keyStorageRegion == uidef.kKeyStorageRegion_FixedOtpmkKey:
                otpmkKeySettingsFrame = ui_settings_fixed_otpmk_key.secBootUiSettingsFixedOtpmkKey(None)
                otpmkKeySettingsFrame.SetTitle(u"Advanced Key Settings - Fixed OTPMK")
                otpmkKeySettingsFrame.Show(True)
            elif self.keyStorageRegion == uidef.kKeyStorageRegion_FlexibleUserKeys:
                userKeySettingsFrame = ui_settings_flexible_user_keys.secBootUiSettingsFlexibleUserKeys(None)
                userKeySettingsFrame.SetTitle(u"Advanced Key Settings - Flexible User")
                userKeySettingsFrame.setNecessaryInfo(self.mcuDevice, self.otpmkDekFilename)
                userKeySettingsFrame.Show(True)
            else:
                pass
        else:
            self.popupMsgBox('Key setting is only available when booting BEE encrypted image in FlexSPI NOR device!')

    def callbackDoBeeEncryption( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice == uidef.kBootDevice_FlexspiNor:
            self._startGaugeTimer()
            if self.keyStorageRegion == uidef.kKeyStorageRegion_FixedOtpmkKey:
                if self.connectStage == uidef.kConnectStage_Reset:
                    self.prepareForFixedOtpmkEncryption()
                else:
                    self.popupMsgBox('Please configure boot device via Flashloader first!')
            elif self.keyStorageRegion == uidef.kKeyStorageRegion_FlexibleUserKeys:
                self.encrypteImageUsingFlexibleUserKeys()
            else:
                pass
            self._stopGaugeTimer()
        else:
            self.popupMsgBox('BEE encryption is only available when booting BEE encrypted image in FlexSPI NOR device!')

    def callbackProgramSrk( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice != uidef.kBootDevice_FlexspiNor:
            self.popupMsgBox('Action is not available because BEE encryption boot is only designed for FlexSPI NOR device!')
        elif self.secureBootType != uidef.kSecureBootType_Development:
            if self.secureBootType == uidef.kSecureBootType_BeeCrypto and (not self.isCertEnabledForBee):
                self.popupMsgBox('Certificate is not enabled for BEE, You can enable it then try again!')
            else:
                if self.connectStage == uidef.kConnectStage_ExternalMemory or \
                   self.connectStage == uidef.kConnectStage_Reset:
                    self._startGaugeTimer()
                    self.printLog("'Load SRK data' button is clicked")
                    self.burnSrkData()
                    self._stopGaugeTimer()
                else:
                    self.popupMsgBox('Please connect to Flashloader first!')
        else:
            self.popupMsgBox('No need to burn SRK data when booting unsigned image!')

    def callbackProgramBeeDek( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice == uidef.kBootDevice_FlexspiNor:
            if self.keyStorageRegion == uidef.kKeyStorageRegion_FlexibleUserKeys:
                if self.connectStage == uidef.kConnectStage_ExternalMemory or \
                   self.connectStage == uidef.kConnectStage_Reset:
                    self._startGaugeTimer()
                    self.burnBeeDekData()
                    self._stopGaugeTimer()
                else:
                    self.popupMsgBox('Please connect to Flashloader first!')
            else:
                self.popupMsgBox('No need to burn BEE DEK data as OTPMK key is selected!')
        else:
            self.popupMsgBox('BEE DEK Burning is only available when booting BEE encrypted image in FlexSPI NOR device!')

    def callbackFlashImage( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice != uidef.kBootDevice_FlexspiNor:
            self.popupMsgBox('Action is not available because BEE encryption boot is only designed for FlexSPI NOR device!')
        else:
            if self.connectStage == uidef.kConnectStage_Reset:
                self._startGaugeTimer()
                self.printLog("'Load Bootable Image' button is clicked")
                self.flashBootableImage()
                self.burnBeeKeySelIfApplicable()
                self._stopGaugeTimer()
            else:
                self.popupMsgBox('Please configure boot device via Flashloader first!')

    def callbackFlashHabDek( self, event ):
        if self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.bootDevice != uidef.kBootDevice_FlexspiNor:
            self.popupMsgBox('Action is not available because BEE encryption boot is only designed for FlexSPI NOR device!')
        elif self.secureBootType == uidef.kSecureBootType_HabCrypto:
            if self.connectStage == uidef.kConnectStage_Reset:
                self._startGaugeTimer()
                self.printLog("'Load KeyBlob Data' button is clicked")
                if self.mcuDeviceHabStatus != fusedef.kHabStatus_Closed0 and \
                   self.mcuDeviceHabStatus != fusedef.kHabStatus_Closed1:
                    self.enableHab()
                    self._connectStateMachine()
                    while self.connectStage != uidef.kConnectStage_Reset:
                        self._connectStateMachine()
                self.flashHabDekToGenerateKeyBlob()
                self._stopGaugeTimer()
            else:
                self.popupMsgBox('Please configure boot device via Flashloader first!')
        else:
            self.popupMsgBox('KeyBlob loading is only available when booting HAB encrypted image!')

    def callbackScanFuse( self, event ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.scanAllFuseRegions()
            self._stopGaugeTimer()
        else:
            self.popupMsgBox('Please connect to Flashloader first!')

    def callbackBurnFuse( self, event ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.burnAllFuseRegions()
            self._stopGaugeTimer()
        else:
            self.popupMsgBox('Please connect to Flashloader first!')

    def callbackViewMem( self, event ):
        if self.connectStage == uidef.kConnectStage_Reset:
            self.readProgrammedMemoryAndShow()
        else:
            self.popupMsgBox('Please configure boot device via Flashloader first!')

    def callbackClearMem( self, event ):
        self.clearMem()

    def callbackClearLog( self, event ):
        self.clearLog()

    def callbackShowHomePage( self, event ):
        msgText = (('https://github.com/JayHeng/nxp-sec-boot-ui.git \n'))
        wx.MessageBox(msgText, "Home Page", wx.OK | wx.ICON_INFORMATION)

    def callbackShowAboutAuthor( self, event ):
        author = "Author:  衡杰Jay, 李嘉奕Joyee \n"
        blog = "Blog:      痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n"
        msgText = ((author.encode('utf-8')) +
                   ('Email:     jie.heng@nxp.com \n') +
                   ('Email:     hengjie1989@foxmail.com \n') +
                   (blog.encode('utf-8')))
        wx.MessageBox(msgText, "About Author", wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()

    main_win = secBootMain(None)
    main_win.SetTitle(u"nxpSecBoot v0.6.0")
    main_win.Show()

    app.MainLoop()
