# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Aug  8 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class secBootWin
###########################################################################

class secBootWin ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"nxpSecBoot", pos = wx.DefaultPosition, size = wx.Size( 1078,760 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.m_menubar = wx.MenuBar( 0 )
		self.m_menu_help = wx.Menu()
		self.m_menuItem_homePage = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"Home Page", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.Append( self.m_menuItem_homePage )

		self.m_menuIte_aboutAuthor = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"About Author", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.Append( self.m_menuIte_aboutAuthor )

		self.m_menubar.Append( self.m_menu_help, u"Help" )

		self.SetMenuBar( self.m_menubar )

		bSizer_win = wx.BoxSizer( wx.VERTICAL )

		wSizer_logo = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_null1Logo = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 950,-1 ), 0 )
		self.m_staticText_null1Logo.Wrap( -1 )

		wSizer_logo.Add( self.m_staticText_null1Logo, 0, wx.ALL, 5 )

		self.m_bitmap_nxp = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 80,30 ), 0 )
		wSizer_logo.Add( self.m_bitmap_nxp, 0, wx.ALL, 5 )


		bSizer_win.Add( wSizer_logo, 1, wx.EXPAND, 5 )

		wSizer_func = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		bSizer_setup = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook_targetSetup = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_panel_targetSetup = wx.Panel( self.m_notebook_targetSetup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_targetSetup.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_targetSetup = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_mcuSeries = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, u"MCU Series:", wx.DefaultPosition, wx.Size( 95,-1 ), 0 )
		self.m_staticText_mcuSeries.Wrap( -1 )

		wSizer_targetSetup.Add( self.m_staticText_mcuSeries, 0, wx.ALL, 5 )

		m_choice_mcuSeriesChoices = [ u"i.MXRT", u"LPC", u"Kinetis" ]
		self.m_choice_mcuSeries = wx.Choice( self.m_panel_targetSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choice_mcuSeriesChoices, 0 )
		self.m_choice_mcuSeries.SetSelection( 0 )
		wSizer_targetSetup.Add( self.m_choice_mcuSeries, 0, wx.ALL, 5 )

		self.m_staticText_mcuDevice = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, u"MCU Device:", wx.DefaultPosition, wx.Size( 95,-1 ), 0 )
		self.m_staticText_mcuDevice.Wrap( -1 )

		wSizer_targetSetup.Add( self.m_staticText_mcuDevice, 0, wx.ALL, 5 )

		m_choice_mcuDeviceChoices = [ u"i.MXRT105x", u"i.MXRT106x", u"i.MXRT102x" ]
		self.m_choice_mcuDevice = wx.Choice( self.m_panel_targetSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choice_mcuDeviceChoices, 0 )
		self.m_choice_mcuDevice.SetSelection( 1 )
		wSizer_targetSetup.Add( self.m_choice_mcuDevice, 0, wx.ALL, 5 )

		self.m_staticText_bootDevice = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, u"Boot Device:", wx.DefaultPosition, wx.Size( 95,-1 ), 0 )
		self.m_staticText_bootDevice.Wrap( -1 )

		wSizer_targetSetup.Add( self.m_staticText_bootDevice, 0, wx.ALL, 5 )

		m_choice_bootDeviceChoices = [ u"FLEXSPI NOR", u"FLEXSPI NAND", u"SEMC NOR", u"SEMC NAND", u"uSDHC SD", u"uSDHC MMC/eMMC", u"LPSPI NOR,EEPROM" ]
		self.m_choice_bootDevice = wx.Choice( self.m_panel_targetSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choice_bootDeviceChoices, 0 )
		self.m_choice_bootDevice.SetSelection( 0 )
		wSizer_targetSetup.Add( self.m_choice_bootDevice, 0, wx.ALL, 5 )

		self.m_staticText_null1TargetSetup = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 256,5 ), 0 )
		self.m_staticText_null1TargetSetup.Wrap( -1 )

		wSizer_targetSetup.Add( self.m_staticText_null1TargetSetup, 0, wx.ALL, 5 )

		self.m_staticText_null2TargetSetup = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		self.m_staticText_null2TargetSetup.Wrap( -1 )

		wSizer_targetSetup.Add( self.m_staticText_null2TargetSetup, 0, wx.ALL, 5 )

		self.m_button_BootDeviceConfiguration = wx.Button( self.m_panel_targetSetup, wx.ID_ANY, u"Boot Device Configuration", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		wSizer_targetSetup.Add( self.m_button_BootDeviceConfiguration, 0, wx.ALL, 5 )


		self.m_panel_targetSetup.SetSizer( wSizer_targetSetup )
		self.m_panel_targetSetup.Layout()
		wSizer_targetSetup.Fit( self.m_panel_targetSetup )
		self.m_notebook_targetSetup.AddPage( self.m_panel_targetSetup, u"Target Setup", False )

		bSizer_setup.Add( self.m_notebook_targetSetup, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_portSetup = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_portSetup = wx.Panel( self.m_notebook_portSetup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		wSizer_portSetup = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_null1PortSetup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText_null1PortSetup.Wrap( -1 )

		wSizer_portSetup.Add( self.m_staticText_null1PortSetup, 0, wx.ALL, 5 )

		self.m_radioBtn_uart = wx.RadioButton( self.m_panel_portSetup, wx.ID_ANY, u"UART", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		wSizer_portSetup.Add( self.m_radioBtn_uart, 0, wx.ALL, 5 )

		self.m_radioBtn_usbhid = wx.RadioButton( self.m_panel_portSetup, wx.ID_ANY, u"USB-HID", wx.DefaultPosition, wx.Size( 70,-1 ), 0 )
		wSizer_portSetup.Add( self.m_radioBtn_usbhid, 0, wx.ALL, 5 )

		self.m_staticText_portVid = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, u"COM Port:", wx.DefaultPosition, wx.Size( 95,-1 ), 0 )
		self.m_staticText_portVid.Wrap( -1 )

		wSizer_portSetup.Add( self.m_staticText_portVid, 0, wx.ALL, 5 )

		m_choice_portVidChoices = []
		self.m_choice_portVid = wx.Choice( self.m_panel_portSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choice_portVidChoices, 0 )
		self.m_choice_portVid.SetSelection( 0 )
		wSizer_portSetup.Add( self.m_choice_portVid, 0, wx.ALL, 5 )

		self.m_staticText_baudPid = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, u"Baudrate:", wx.DefaultPosition, wx.Size( 95,-1 ), 0 )
		self.m_staticText_baudPid.Wrap( -1 )

		wSizer_portSetup.Add( self.m_staticText_baudPid, 0, wx.ALL, 5 )

		m_choice_baudPidChoices = []
		self.m_choice_baudPid = wx.Choice( self.m_panel_portSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choice_baudPidChoices, 0 )
		self.m_choice_baudPid.SetSelection( 0 )
		wSizer_portSetup.Add( self.m_choice_baudPid, 0, wx.ALL, 5 )

		self.m_staticText_null2PortSetup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 256,5 ), 0 )
		self.m_staticText_null2PortSetup.Wrap( -1 )

		wSizer_portSetup.Add( self.m_staticText_null2PortSetup, 0, wx.ALL, 5 )

		self.m_staticText_null3PortSetup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 45,-1 ), 0 )
		self.m_staticText_null3PortSetup.Wrap( -1 )

		wSizer_portSetup.Add( self.m_staticText_null3PortSetup, 0, wx.ALL, 5 )

		self.m_bitmap_connectLed = wx.StaticBitmap( self.m_panel_portSetup, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 30,30 ), 0 )
		wSizer_portSetup.Add( self.m_bitmap_connectLed, 0, wx.ALL, 5 )

		self.m_staticText_null4PortSetup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		self.m_staticText_null4PortSetup.Wrap( -1 )

		wSizer_portSetup.Add( self.m_staticText_null4PortSetup, 0, wx.ALL, 5 )

		self.m_checkBox_oneStepConnect = wx.CheckBox( self.m_panel_portSetup, wx.ID_ANY, u"One Step", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		wSizer_portSetup.Add( self.m_checkBox_oneStepConnect, 0, wx.ALL, 5 )

		self.m_staticText_null5PortSetup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 45,-1 ), 0 )
		self.m_staticText_null5PortSetup.Wrap( -1 )

		wSizer_portSetup.Add( self.m_staticText_null5PortSetup, 0, wx.ALL, 5 )

		self.m_button_connect = wx.Button( self.m_panel_portSetup, wx.ID_ANY, u"Connect to ROM", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		wSizer_portSetup.Add( self.m_button_connect, 0, wx.ALL, 5 )


		self.m_panel_portSetup.SetSizer( wSizer_portSetup )
		self.m_panel_portSetup.Layout()
		wSizer_portSetup.Fit( self.m_panel_portSetup )
		self.m_notebook_portSetup.AddPage( self.m_panel_portSetup, u"Port Setup", False )

		bSizer_setup.Add( self.m_notebook_portSetup, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_deviceStatus = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_deviceStatus = wx.Panel( self.m_notebook_deviceStatus, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_deviceStatus = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl_deviceStatus = wx.TextCtrl( self.m_panel_deviceStatus, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 250,200 ), wx.TE_MULTILINE|wx.TE_RICH2 )
		bSizer_deviceStatus.Add( self.m_textCtrl_deviceStatus, 0, wx.ALL, 5 )


		self.m_panel_deviceStatus.SetSizer( bSizer_deviceStatus )
		self.m_panel_deviceStatus.Layout()
		bSizer_deviceStatus.Fit( self.m_panel_deviceStatus )
		self.m_notebook_deviceStatus.AddPage( self.m_panel_deviceStatus, u"Device Status", False )

		bSizer_setup.Add( self.m_notebook_deviceStatus, 1, wx.EXPAND |wx.ALL, 5 )


		wSizer_func.Add( bSizer_setup, 1, wx.EXPAND, 5 )

		bSizer_boot = wx.BoxSizer( wx.VERTICAL )

		wSizer_bootType = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_null1BootType = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 415,-1 ), 0 )
		self.m_staticText_null1BootType.Wrap( -1 )

		wSizer_bootType.Add( self.m_staticText_null1BootType, 0, wx.ALL, 5 )

		self.m_staticText_secureBootType = wx.StaticText( self, wx.ID_ANY, u"Secure Boot Type:", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText_secureBootType.Wrap( -1 )

		wSizer_bootType.Add( self.m_staticText_secureBootType, 0, wx.ALL, 5 )

		m_choice_secureBootTypeChoices = [ u"Unsigned (XIP) Image Boot", u"Signed (XIP) Image Boot", u"HAB Signed Encrypted Image Boot", u"BEE (Signed) Encrypted XIP Image Boot" ]
		self.m_choice_secureBootType = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_secureBootTypeChoices, 0 )
		self.m_choice_secureBootType.SetSelection( 0 )
		wSizer_bootType.Add( self.m_choice_secureBootType, 0, wx.ALL, 5 )


		bSizer_boot.Add( wSizer_bootType, 1, wx.EXPAND, 5 )

		self.m_notebook_imageSeq = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,450 ), 0 )
		self.m_notebook_imageSeq.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.m_panel_genSeq = wx.Panel( self.m_notebook_imageSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_genSeq.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_panel_genSeq.SetBackgroundColour( wx.Colour( 160, 160, 160 ) )

		wSizer_genSeq = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_panel_doAuth = wx.Panel( self.m_panel_genSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_doAuth.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		bSizer_doAuth = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_doAuth1_certInput = wx.Panel( self.m_panel_doAuth, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_certInput = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_doAuth1_certInput, wx.ID_ANY, u"Step 1:" ), wx.VERTICAL )

		self.m_staticText_serial = wx.StaticText( sbSizer_certInput.GetStaticBox(), wx.ID_ANY, u"serial (8 digits):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_serial.Wrap( -1 )

		sbSizer_certInput.Add( self.m_staticText_serial, 0, wx.ALL, 5 )

		self.m_textCtrl_serial = wx.TextCtrl( sbSizer_certInput.GetStaticBox(), wx.ID_ANY, u"12345678", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		sbSizer_certInput.Add( self.m_textCtrl_serial, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_keyPass = wx.StaticText( sbSizer_certInput.GetStaticBox(), wx.ID_ANY, u"key_pass (text):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_keyPass.Wrap( -1 )

		sbSizer_certInput.Add( self.m_staticText_keyPass, 0, wx.ALL, 5 )

		self.m_textCtrl_keyPass = wx.TextCtrl( sbSizer_certInput.GetStaticBox(), wx.ID_ANY, u"test", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		sbSizer_certInput.Add( self.m_textCtrl_keyPass, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_button_advCertSettings = wx.Button( sbSizer_certInput.GetStaticBox(), wx.ID_ANY, u"Advanced Cert Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer_certInput.Add( self.m_button_advCertSettings, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_doAuth1_certInput.SetSizer( sbSizer_certInput )
		self.m_panel_doAuth1_certInput.Layout()
		sbSizer_certInput.Fit( self.m_panel_doAuth1_certInput )
		bSizer_doAuth.Add( self.m_panel_doAuth1_certInput, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_doAuth2_certFmt = wx.Panel( self.m_panel_doAuth, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_certFmt = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_doAuth2_certFmt, wx.ID_ANY, u"Certificate Format:" ), wx.VERTICAL )

		m_choice_certFmtChoices = [ u"X.509v3" ]
		self.m_choice_certFmt = wx.Choice( sbSizer_certFmt.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), m_choice_certFmtChoices, 0 )
		self.m_choice_certFmt.SetSelection( 0 )
		sbSizer_certFmt.Add( self.m_choice_certFmt, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_hashAlgo = wx.StaticText( sbSizer_certFmt.GetStaticBox(), wx.ID_ANY, u"Hash Algorithm:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_hashAlgo.Wrap( -1 )

		sbSizer_certFmt.Add( self.m_staticText_hashAlgo, 0, wx.ALL, 5 )

		m_choice_hashAlgoChoices = [ u"SHA-256" ]
		self.m_choice_hashAlgo = wx.Choice( sbSizer_certFmt.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), m_choice_hashAlgoChoices, 0 )
		self.m_choice_hashAlgo.SetSelection( 0 )
		sbSizer_certFmt.Add( self.m_choice_hashAlgo, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_doAuth2_certFmt.SetSizer( sbSizer_certFmt )
		self.m_panel_doAuth2_certFmt.Layout()
		sbSizer_certFmt.Fit( self.m_panel_doAuth2_certFmt )
		bSizer_doAuth.Add( self.m_panel_doAuth2_certFmt, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_genCert = wx.Button( self.m_panel_doAuth, wx.ID_ANY, u"Generate Certificate,SRK", wx.DefaultPosition, wx.Size( 195,-1 ), 0 )
		bSizer_doAuth.Add( self.m_button_genCert, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_doAuth.SetSizer( bSizer_doAuth )
		self.m_panel_doAuth.Layout()
		bSizer_doAuth.Fit( self.m_panel_doAuth )
		wSizer_genSeq.Add( self.m_panel_doAuth, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_genImage = wx.Panel( self.m_panel_genSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_genImage.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		bSizer_genImage = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_genImage1_browseApp = wx.Panel( self.m_panel_genImage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_browseApp = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_genImage1_browseApp, wx.ID_ANY, u"Step 3:" ), wx.VERTICAL )

		self.m_staticText_appPath = wx.StaticText( sbSizer_browseApp.GetStaticBox(), wx.ID_ANY, u"App Image File (.elf/.srec):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_appPath.Wrap( -1 )

		sbSizer_browseApp.Add( self.m_staticText_appPath, 0, wx.ALL, 5 )

		self.m_filePicker_appPath = wx.FilePickerCtrl( sbSizer_browseApp.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 280,-1 ), wx.FLP_DEFAULT_STYLE )
		sbSizer_browseApp.Add( self.m_filePicker_appPath, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_bdPath = wx.StaticText( sbSizer_browseApp.GetStaticBox(), wx.ID_ANY, u"Matched BD File:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_bdPath.Wrap( -1 )

		sbSizer_browseApp.Add( self.m_staticText_bdPath, 0, wx.ALL, 5 )

		self.m_textCtrl_bdPath = wx.TextCtrl( sbSizer_browseApp.GetStaticBox(), wx.ID_ANY, u"example.bd", wx.DefaultPosition, wx.Size( 280,-1 ), 0 )
		self.m_textCtrl_bdPath.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

		sbSizer_browseApp.Add( self.m_textCtrl_bdPath, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_button_advBdSettings = wx.Button( sbSizer_browseApp.GetStaticBox(), wx.ID_ANY, u"Advanced BD Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer_browseApp.Add( self.m_button_advBdSettings, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_genImage1_browseApp.SetSizer( sbSizer_browseApp )
		self.m_panel_genImage1_browseApp.Layout()
		sbSizer_browseApp.Fit( self.m_panel_genImage1_browseApp )
		bSizer_genImage.Add( self.m_panel_genImage1_browseApp, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_genImage2_habCryptoAlgo = wx.Panel( self.m_panel_genImage, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		sbSizer_habCryptoAlgo = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_genImage2_habCryptoAlgo, wx.ID_ANY, u"HAB Encryption Algorithm:" ), wx.VERTICAL )

		m_choice_habCryptoAlgoChoices = [ u"AES-128" ]
		self.m_choice_habCryptoAlgo = wx.Choice( sbSizer_habCryptoAlgo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), m_choice_habCryptoAlgoChoices, 0 )
		self.m_choice_habCryptoAlgo.SetSelection( 0 )
		sbSizer_habCryptoAlgo.Add( self.m_choice_habCryptoAlgo, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_genImage2_habCryptoAlgo.SetSizer( sbSizer_habCryptoAlgo )
		self.m_panel_genImage2_habCryptoAlgo.Layout()
		sbSizer_habCryptoAlgo.Fit( self.m_panel_genImage2_habCryptoAlgo )
		bSizer_genImage.Add( self.m_panel_genImage2_habCryptoAlgo, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_genImage3_enableCertForBee = wx.Panel( self.m_panel_genImage, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		sbSizer_enableCertForBee = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_genImage3_enableCertForBee, wx.ID_ANY, u"Enable Certificate for BEE Encryption" ), wx.VERTICAL )

		m_choice_enableCertForBeeChoices = [ u"No", u"Yes" ]
		self.m_choice_enableCertForBee = wx.Choice( sbSizer_enableCertForBee.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), m_choice_enableCertForBeeChoices, 0 )
		self.m_choice_enableCertForBee.SetSelection( 0 )
		sbSizer_enableCertForBee.Add( self.m_choice_enableCertForBee, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_genImage3_enableCertForBee.SetSizer( sbSizer_enableCertForBee )
		self.m_panel_genImage3_enableCertForBee.Layout()
		sbSizer_enableCertForBee.Fit( self.m_panel_genImage3_enableCertForBee )
		bSizer_genImage.Add( self.m_panel_genImage3_enableCertForBee, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_genImage = wx.Button( self.m_panel_genImage, wx.ID_ANY, u"Generate Unsigned Bootable Image", wx.DefaultPosition, wx.Size( 225,-1 ), 0 )
		bSizer_genImage.Add( self.m_button_genImage, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_genImage.SetSizer( bSizer_genImage )
		self.m_panel_genImage.Layout()
		bSizer_genImage.Fit( self.m_panel_genImage )
		wSizer_genSeq.Add( self.m_panel_genImage, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_prepBee = wx.Panel( self.m_panel_genSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_prepBee = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_prepBee1_beeKeyRegion = wx.Panel( self.m_panel_prepBee, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_keyStorageRegion = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_prepBee1_beeKeyRegion, wx.ID_ANY, u"Step 4:" ), wx.VERTICAL )

		self.m_staticText_keyStorageRegion = wx.StaticText( sbSizer_keyStorageRegion.GetStaticBox(), wx.ID_ANY, u"Key Storage Region:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_keyStorageRegion.Wrap( -1 )

		sbSizer_keyStorageRegion.Add( self.m_staticText_keyStorageRegion, 0, wx.ALL, 5 )

		m_choice_keyStorageRegionChoices = [ u"Fixed SNVS Key", u"Flexible User Keys" ]
		self.m_choice_keyStorageRegion = wx.Choice( sbSizer_keyStorageRegion.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_keyStorageRegionChoices, 0 )
		self.m_choice_keyStorageRegion.SetSelection( 0 )
		sbSizer_keyStorageRegion.Add( self.m_choice_keyStorageRegion, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_prepBee1_beeKeyRegion.SetSizer( sbSizer_keyStorageRegion )
		self.m_panel_prepBee1_beeKeyRegion.Layout()
		sbSizer_keyStorageRegion.Fit( self.m_panel_prepBee1_beeKeyRegion )
		bSizer_prepBee.Add( self.m_panel_prepBee1_beeKeyRegion, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_prepBee2_showOtpmkDek = wx.Panel( self.m_panel_prepBee, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_showOtpmkDek = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_prepBee2_showOtpmkDek, wx.ID_ANY, u"Pre-burned DEK in OTPMK" ), wx.VERTICAL )

		self.m_textCtrl_otpmkDek128bit = wx.TextCtrl( sbSizer_showOtpmkDek.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,85 ), wx.TE_MULTILINE|wx.TE_RICH2 )
		self.m_textCtrl_otpmkDek128bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

		sbSizer_showOtpmkDek.Add( self.m_textCtrl_otpmkDek128bit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_prepBee2_showOtpmkDek.SetSizer( sbSizer_showOtpmkDek )
		self.m_panel_prepBee2_showOtpmkDek.Layout()
		sbSizer_showOtpmkDek.Fit( self.m_panel_prepBee2_showOtpmkDek )
		bSizer_prepBee.Add( self.m_panel_prepBee2_showOtpmkDek, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_prepBee3_advKeySettings = wx.Panel( self.m_panel_prepBee, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_advKeySettings = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_prepBee3_advKeySettings, wx.ID_ANY, u"BEE Encryption Settings:" ), wx.VERTICAL )

		m_choice_beeCryptoAlgoChoices = [ u"AES-128" ]
		self.m_choice_beeCryptoAlgo = wx.Choice( sbSizer_advKeySettings.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), m_choice_beeCryptoAlgoChoices, 0 )
		self.m_choice_beeCryptoAlgo.SetSelection( 0 )
		sbSizer_advKeySettings.Add( self.m_choice_beeCryptoAlgo, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_button_advKeySettings = wx.Button( sbSizer_advKeySettings.GetStaticBox(), wx.ID_ANY, u"Advanced Key Settings", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		sbSizer_advKeySettings.Add( self.m_button_advKeySettings, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_prepBee3_advKeySettings.SetSizer( sbSizer_advKeySettings )
		self.m_panel_prepBee3_advKeySettings.Layout()
		sbSizer_advKeySettings.Fit( self.m_panel_prepBee3_advKeySettings )
		bSizer_prepBee.Add( self.m_panel_prepBee3_advKeySettings, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_prepBee = wx.Button( self.m_panel_prepBee, wx.ID_ANY, u"Prepare For Encryption", wx.DefaultPosition, wx.Size( 195,-1 ), 0 )
		bSizer_prepBee.Add( self.m_button_prepBee, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_prepBee.SetSizer( bSizer_prepBee )
		self.m_panel_prepBee.Layout()
		bSizer_prepBee.Fit( self.m_panel_prepBee )
		wSizer_genSeq.Add( self.m_panel_prepBee, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel_genSeq.SetSizer( wSizer_genSeq )
		self.m_panel_genSeq.Layout()
		wSizer_genSeq.Fit( self.m_panel_genSeq )
		self.m_notebook_imageSeq.AddPage( self.m_panel_genSeq, u"Image Generation Sequence", True )
		self.m_panel_loadSeq = wx.Panel( self.m_notebook_imageSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_loadSeq.SetBackgroundColour( wx.Colour( 160, 160, 160 ) )

		wSizer_loadSeq = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_panel_progSrk = wx.Panel( self.m_panel_loadSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_progSrk = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_progSrk1_showSrk = wx.Panel( self.m_panel_progSrk, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_showSrk = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_progSrk1_showSrk, wx.ID_ANY, u"Step 2:" ), wx.VERTICAL )

		self.m_staticText_srk256bit = wx.StaticText( sbSizer_showSrk.GetStaticBox(), wx.ID_ANY, u"Burn below SRK data (256bits) into Fuse SRK0-7 Region:", wx.DefaultPosition, wx.Size( 120,60 ), 0 )
		self.m_staticText_srk256bit.Wrap( -1 )

		sbSizer_showSrk.Add( self.m_staticText_srk256bit, 0, wx.ALL, 5 )

		self.m_textCtrl_srk256bit = wx.TextCtrl( sbSizer_showSrk.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,160 ), wx.TE_MULTILINE|wx.TE_RICH2 )
		self.m_textCtrl_srk256bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

		sbSizer_showSrk.Add( self.m_textCtrl_srk256bit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_progSrk1_showSrk.SetSizer( sbSizer_showSrk )
		self.m_panel_progSrk1_showSrk.Layout()
		sbSizer_showSrk.Fit( self.m_panel_progSrk1_showSrk )
		bSizer_progSrk.Add( self.m_panel_progSrk1_showSrk, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_progSrk = wx.Button( self.m_panel_progSrk, wx.ID_ANY, u"Burn SRK data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_progSrk.Add( self.m_button_progSrk, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_progSrk.SetSizer( bSizer_progSrk )
		self.m_panel_progSrk.Layout()
		bSizer_progSrk.Fit( self.m_panel_progSrk )
		wSizer_loadSeq.Add( self.m_panel_progSrk, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_operBee = wx.Panel( self.m_panel_loadSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_operBee = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_operBee1_beeKeyInfo = wx.Panel( self.m_panel_operBee, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_beeKeyInfo = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_operBee1_beeKeyInfo, wx.ID_ANY, u"Step 5:" ), wx.VERTICAL )

		self.m_staticText_beeKeyInfo = wx.StaticText( sbSizer_beeKeyInfo.GetStaticBox(), wx.ID_ANY, u"Burn below user DEK data (128bits * n) into below Region for BEE:", wx.DefaultPosition, wx.Size( 130,45 ), 0 )
		self.m_staticText_beeKeyInfo.Wrap( -1 )

		sbSizer_beeKeyInfo.Add( self.m_staticText_beeKeyInfo, 0, wx.ALL, 5 )


		self.m_panel_operBee1_beeKeyInfo.SetSizer( sbSizer_beeKeyInfo )
		self.m_panel_operBee1_beeKeyInfo.Layout()
		sbSizer_beeKeyInfo.Fit( self.m_panel_operBee1_beeKeyInfo )
		bSizer_operBee.Add( self.m_panel_operBee1_beeKeyInfo, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_operBee2_showGp4Dek = wx.Panel( self.m_panel_operBee, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_showGp4Dek = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_operBee2_showGp4Dek, wx.ID_ANY, u"Fuse GP4 Region:" ), wx.VERTICAL )

		self.m_textCtrl_gp4Dek128bit = wx.TextCtrl( sbSizer_showGp4Dek.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,85 ), wx.TE_MULTILINE|wx.TE_RICH2 )
		self.m_textCtrl_gp4Dek128bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

		sbSizer_showGp4Dek.Add( self.m_textCtrl_gp4Dek128bit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_operBee2_showGp4Dek.SetSizer( sbSizer_showGp4Dek )
		self.m_panel_operBee2_showGp4Dek.Layout()
		sbSizer_showGp4Dek.Fit( self.m_panel_operBee2_showGp4Dek )
		bSizer_operBee.Add( self.m_panel_operBee2_showGp4Dek, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_operBee3_showSwgp2Dek = wx.Panel( self.m_panel_operBee, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_showSwgp2Dek = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_operBee3_showSwgp2Dek, wx.ID_ANY, u"Fuse SW_GP2 Region:" ), wx.VERTICAL )

		self.m_textCtrl_swgp2Dek128bit = wx.TextCtrl( sbSizer_showSwgp2Dek.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,85 ), wx.TE_MULTILINE|wx.TE_RICH2 )
		self.m_textCtrl_swgp2Dek128bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

		sbSizer_showSwgp2Dek.Add( self.m_textCtrl_swgp2Dek128bit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_operBee3_showSwgp2Dek.SetSizer( sbSizer_showSwgp2Dek )
		self.m_panel_operBee3_showSwgp2Dek.Layout()
		sbSizer_showSwgp2Dek.Fit( self.m_panel_operBee3_showSwgp2Dek )
		bSizer_operBee.Add( self.m_panel_operBee3_showSwgp2Dek, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_operBee = wx.Button( self.m_panel_operBee, wx.ID_ANY, u"Burn DEK data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_operBee.Add( self.m_button_operBee, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_operBee.SetSizer( bSizer_operBee )
		self.m_panel_operBee.Layout()
		bSizer_operBee.Fit( self.m_panel_operBee )
		wSizer_loadSeq.Add( self.m_panel_operBee, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_flashImage = wx.Panel( self.m_panel_loadSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_flashImage.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		bSizer_flashImage = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_flashImage1_showImage = wx.Panel( self.m_panel_flashImage, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel_flashImage1_showImage.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		sbSizer_showImage = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_flashImage1_showImage, wx.ID_ANY, u"Step 6:" ), wx.VERTICAL )

		self.m_staticText_showImage = wx.StaticText( sbSizer_showImage.GetStaticBox(), wx.ID_ANY, u"Program final bootable image to flash:", wx.DefaultPosition, wx.Size( 180,50 ), 0 )
		self.m_staticText_showImage.Wrap( -1 )

		sbSizer_showImage.Add( self.m_staticText_showImage, 0, wx.ALL, 5 )

		self.m_bitmap_bootableImage = wx.StaticBitmap( sbSizer_showImage.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer_showImage.Add( self.m_bitmap_bootableImage, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_flashImage1_showImage.SetSizer( sbSizer_showImage )
		self.m_panel_flashImage1_showImage.Layout()
		sbSizer_showImage.Fit( self.m_panel_flashImage1_showImage )
		bSizer_flashImage.Add( self.m_panel_flashImage1_showImage, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_flashImage = wx.Button( self.m_panel_flashImage, wx.ID_ANY, u"Load Image", wx.DefaultPosition, wx.Size( 185,-1 ), 0 )
		bSizer_flashImage.Add( self.m_button_flashImage, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_flashImage.SetSizer( bSizer_flashImage )
		self.m_panel_flashImage.Layout()
		bSizer_flashImage.Fit( self.m_panel_flashImage )
		wSizer_loadSeq.Add( self.m_panel_flashImage, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel_progDek = wx.Panel( self.m_panel_loadSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_progDek = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_progDek1_showHabDek = wx.Panel( self.m_panel_progDek, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer_showHabDek = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_progDek1_showHabDek, wx.ID_ANY, u"Step 7:" ), wx.VERTICAL )

		self.m_staticText_habDek128bit = wx.StaticText( sbSizer_showHabDek.GetStaticBox(), wx.ID_ANY, u"Use below DEK data (128bits) to generate keyblob and program it to flash for HAB:", wx.DefaultPosition, wx.Size( 120,80 ), 0 )
		self.m_staticText_habDek128bit.Wrap( -1 )

		sbSizer_showHabDek.Add( self.m_staticText_habDek128bit, 0, wx.ALL, 5 )

		self.m_textCtrl_habDek128bit = wx.TextCtrl( sbSizer_showHabDek.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,85 ), wx.TE_MULTILINE|wx.TE_RICH2 )
		self.m_textCtrl_habDek128bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

		sbSizer_showHabDek.Add( self.m_textCtrl_habDek128bit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_progDek1_showHabDek.SetSizer( sbSizer_showHabDek )
		self.m_panel_progDek1_showHabDek.Layout()
		sbSizer_showHabDek.Fit( self.m_panel_progDek1_showHabDek )
		bSizer_progDek.Add( self.m_panel_progDek1_showHabDek, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_progDek = wx.Button( self.m_panel_progDek, wx.ID_ANY, u"Enable HAB, Load KeyBlob Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_progDek.Add( self.m_button_progDek, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel_progDek.SetSizer( bSizer_progDek )
		self.m_panel_progDek.Layout()
		bSizer_progDek.Fit( self.m_panel_progDek )
		wSizer_loadSeq.Add( self.m_panel_progDek, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel_loadSeq.SetSizer( wSizer_loadSeq )
		self.m_panel_loadSeq.Layout()
		wSizer_loadSeq.Fit( self.m_panel_loadSeq )
		self.m_notebook_imageSeq.AddPage( self.m_panel_loadSeq, u"Image Loading Sequence", False )
		self.m_panel_fuseUtil = wx.Panel( self.m_notebook_imageSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_fuseUtil.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_fuseUtil = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		bSizer_fuseGroupTxt0 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText_fuse400 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x400:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse400.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse400, 0, wx.ALL, 5 )

		self.m_staticText_fuse410 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x410:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse410.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse410, 0, wx.ALL, 5 )

		self.m_staticText_fuse420 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x420:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse420.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse420, 0, wx.ALL, 5 )

		self.m_staticText_fuse430 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x430:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse430.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse430, 0, wx.ALL, 5 )

		self.m_staticText_fuse440 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x440:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse440.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse440, 0, wx.ALL, 5 )

		self.m_staticText_fuse450 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x450:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse450.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse450, 0, wx.ALL, 5 )

		self.m_staticText_fuse460 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x460:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse460.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse460, 0, wx.ALL, 5 )

		self.m_staticText_fuse470 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x470:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse470.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse470, 0, wx.ALL, 5 )

		self.m_staticText_fuse480 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x480:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse480.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse480, 0, wx.ALL, 5 )

		self.m_staticText_fuse490 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x490:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse490.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse490, 0, wx.ALL, 5 )

		self.m_staticText_fuse4a0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x4a0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse4a0.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse4a0, 0, wx.ALL, 5 )

		self.m_staticText_fuse4b0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x4b0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse4b0.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse4b0, 0, wx.ALL, 5 )

		self.m_staticText_fuse4c0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x4c0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse4c0.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse4c0, 0, wx.ALL, 5 )

		self.m_staticText_fuse4d0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x4d0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse4d0.Wrap( -1 )

		bSizer_fuseGroupTxt0.Add( self.m_staticText_fuse4d0, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupTxt0, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupCtrl0 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl_fuse400 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse400, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse410 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse410, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse420 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse420, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse430 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse430, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse440 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse440, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse450 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse450, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse460 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse460, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse470 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse470, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse480 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse480, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse490 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse490, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse4a0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse4a0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse4b0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse4b0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse4c0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse4c0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse4d0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl0.Add( self.m_textCtrl_fuse4d0, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupCtrl0, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupTxt1 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText_fuse4e0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x4e0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse4e0.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse4e0, 0, wx.ALL, 5 )

		self.m_staticText_fuse4f0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x4f0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse4f0.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse4f0, 0, wx.ALL, 5 )

		self.m_staticText_fuse500 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x500:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse500.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse500, 0, wx.ALL, 5 )

		self.m_staticText_fuse510 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x510:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse510.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse510, 0, wx.ALL, 5 )

		self.m_staticText_fuse520 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x520:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse520.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse520, 0, wx.ALL, 5 )

		self.m_staticText_fuse530 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x530:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse530.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse530, 0, wx.ALL, 5 )

		self.m_staticText_fuse540 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x540:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse540.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse540, 0, wx.ALL, 5 )

		self.m_staticText_fuse550 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x550:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse550.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse550, 0, wx.ALL, 5 )

		self.m_staticText_fuse560 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x560:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse560.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse560, 0, wx.ALL, 5 )

		self.m_staticText_fuse570 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x570:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse570.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse570, 0, wx.ALL, 5 )

		self.m_staticText_fuse580 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x580:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse580.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse580, 0, wx.ALL, 5 )

		self.m_staticText_fuse590 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x590:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse590.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse590, 0, wx.ALL, 5 )

		self.m_staticText_fuse5a0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x5a0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse5a0.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse5a0, 0, wx.ALL, 5 )

		self.m_staticText_fuse5b0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x5b0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse5b0.Wrap( -1 )

		bSizer_fuseGroupTxt1.Add( self.m_staticText_fuse5b0, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupTxt1, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupCtrl1 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl_fuse4e0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse4e0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse4f0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse4f0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse500 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse500, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse510 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse510, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse520 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse520, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse530 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse530, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse540 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse540, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse550 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse550, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse560 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse560, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse570 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse570, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse580 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse580, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse590 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse590, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse5a0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse5a0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse5b0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl1.Add( self.m_textCtrl_fuse5b0, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupCtrl1, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupTxt2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText_fuse5c0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x5c0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse5c0.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse5c0, 0, wx.ALL, 5 )

		self.m_staticText_fuse5d0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x5d0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse5d0.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse5d0, 0, wx.ALL, 5 )

		self.m_staticText_fuse5e0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x5e0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse5e0.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse5e0, 0, wx.ALL, 5 )

		self.m_staticText_fuse5f0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x5f0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse5f0.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse5f0, 0, wx.ALL, 5 )

		self.m_staticText_fuse600 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x600:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse600.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse600, 0, wx.ALL, 5 )

		self.m_staticText_fuse610 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x610:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse610.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse610, 0, wx.ALL, 5 )

		self.m_staticText_fuse620 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x620:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse620.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse620, 0, wx.ALL, 5 )

		self.m_staticText_fuse630 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x630:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse630.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse630, 0, wx.ALL, 5 )

		self.m_staticText_fuse640 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x640:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse640.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse640, 0, wx.ALL, 5 )

		self.m_staticText_fuse650 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x650:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse650.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse650, 0, wx.ALL, 5 )

		self.m_staticText_fuse660 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x660:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse660.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse660, 0, wx.ALL, 5 )

		self.m_staticText_fuse670 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x670:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse670.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse670, 0, wx.ALL, 5 )

		self.m_staticText_fuse680 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x680:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse680.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse680, 0, wx.ALL, 5 )

		self.m_staticText_fuse690 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x690:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse690.Wrap( -1 )

		bSizer_fuseGroupTxt2.Add( self.m_staticText_fuse690, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupTxt2, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupCtrl2 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl_fuse5c0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse5c0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse5d0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse5d0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse5e0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse5e0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse5f0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse5f0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse600 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse600, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse610 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse610, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse620 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse620, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse630 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse630, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse640 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse640, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse650 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse650, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse660 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse660, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse670 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse670, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse680 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse680, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse690 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl2.Add( self.m_textCtrl_fuse690, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupCtrl2, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupTxt3 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText_fuse6a0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x6a0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse6a0.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse6a0, 0, wx.ALL, 5 )

		self.m_staticText_fuse6b0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x6b0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse6b0.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse6b0, 0, wx.ALL, 5 )

		self.m_staticText_fuse6c0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x6c0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse6c0.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse6c0, 0, wx.ALL, 5 )

		self.m_staticText_fuse6d0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x6d0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse6d0.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse6d0, 0, wx.ALL, 5 )

		self.m_staticText_fuse6e0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x6e0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse6e0.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse6e0, 0, wx.ALL, 5 )

		self.m_staticText_fuse6f0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x6f0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse6f0.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse6f0, 0, wx.ALL, 5 )

		self.m_staticText_fuse700 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x700:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse700.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse700, 0, wx.ALL, 5 )

		self.m_staticText_fuse710 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x710:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse710.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse710, 0, wx.ALL, 5 )

		self.m_staticText_fuse720 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x720:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse720.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse720, 0, wx.ALL, 5 )

		self.m_staticText_fuse730 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x730:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse730.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse730, 0, wx.ALL, 5 )

		self.m_staticText_fuse740 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x740:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse740.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse740, 0, wx.ALL, 5 )

		self.m_staticText_fuse750 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x750:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse750.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse750, 0, wx.ALL, 5 )

		self.m_staticText_fuse760 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x760:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse760.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse760, 0, wx.ALL, 5 )

		self.m_staticText_fuse770 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x770:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse770.Wrap( -1 )

		bSizer_fuseGroupTxt3.Add( self.m_staticText_fuse770, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupTxt3, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupCtrl3 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl_fuse6a0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse6a0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse6b0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse6b0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse6c0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse6c0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse6d0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse6d0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse6e0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse6e0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse6f0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse6f0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse700 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse700, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse710 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse710, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse720 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse720, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse730 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse730, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse740 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse740, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse750 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse750, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse760 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse760, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse770 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl3.Add( self.m_textCtrl_fuse770, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupCtrl3, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupTxt4 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText_fuse780 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x780:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse780.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse780, 0, wx.ALL, 5 )

		self.m_staticText_fuse790 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x790:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse790.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse790, 0, wx.ALL, 5 )

		self.m_staticText_fuse7a0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x7a0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse7a0.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse7a0, 0, wx.ALL, 5 )

		self.m_staticText_fuse7b0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x7b0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse7b0.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse7b0, 0, wx.ALL, 5 )

		self.m_staticText_fuse7c0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x7c0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse7c0.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse7c0, 0, wx.ALL, 5 )

		self.m_staticText_fuse7d0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x7d0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse7d0.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse7d0, 0, wx.ALL, 5 )

		self.m_staticText_fuse7e0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x7e0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse7e0.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse7e0, 0, wx.ALL, 5 )

		self.m_staticText_fuse7f0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x7f0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse7f0.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse7f0, 0, wx.ALL, 5 )

		self.m_staticText_fuse800 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x800:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse800.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse800, 0, wx.ALL, 5 )

		self.m_staticText_fuse810 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x810:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse810.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse810, 0, wx.ALL, 5 )

		self.m_staticText_fuse820 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x820:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse820.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse820, 0, wx.ALL, 5 )

		self.m_staticText_fuse830 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x830:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse830.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse830, 0, wx.ALL, 5 )

		self.m_staticText_fuse840 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x840:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse840.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse840, 0, wx.ALL, 5 )

		self.m_staticText_fuse850 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x850:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse850.Wrap( -1 )

		bSizer_fuseGroupTxt4.Add( self.m_staticText_fuse850, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupTxt4, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupCtrl4 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl_fuse780 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse780, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse790 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse790, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse7a0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse7a0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse7b0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse7b0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse7c0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse7c0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse7d0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse7d0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse7e0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse7e0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse7f0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse7f0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse800 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse800, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse810 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse810, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse820 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse820, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse830 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse830, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse840 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse840, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse850 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl4.Add( self.m_textCtrl_fuse850, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupCtrl4, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupTxt5 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText_fuse860 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x860:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse860.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse860, 0, wx.ALL, 5 )

		self.m_staticText_fuse870 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x870:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse870.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse870, 0, wx.ALL, 5 )

		self.m_staticText_fuse880 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x880:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse880.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse880, 0, wx.ALL, 5 )

		self.m_staticText_fuse890 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x890:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse890.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse890, 0, wx.ALL, 5 )

		self.m_staticText_fuse8a0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x8a0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse8a0.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse8a0, 0, wx.ALL, 5 )

		self.m_staticText_fuse8b0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x8b0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse8b0.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse8b0, 0, wx.ALL, 5 )

		self.m_staticText_fuse8c0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x8c0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse8c0.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse8c0, 0, wx.ALL, 5 )

		self.m_staticText_fuse8d0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x8d0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse8d0.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse8d0, 0, wx.ALL, 5 )

		self.m_staticText_fuse8e0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x8e0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse8e0.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse8e0, 0, wx.ALL, 5 )

		self.m_staticText_fuse8f0 = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, u"0x8f0:", wx.DefaultPosition, wx.Size( 31,20 ), 0 )
		self.m_staticText_fuse8f0.Wrap( -1 )

		bSizer_fuseGroupTxt5.Add( self.m_staticText_fuse8f0, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupTxt5, 1, wx.EXPAND, 5 )

		bSizer_fuseGroupCtrl5 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl_fuse860 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse860, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse870 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse870, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse880 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse880, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse890 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse890, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse8a0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse8a0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse8b0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse8b0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse8c0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse8c0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse8d0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse8d0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse8e0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse8e0, 0, wx.ALL, 5 )

		self.m_textCtrl_fuse8f0 = wx.TextCtrl( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,20 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_textCtrl_fuse8f0, 0, wx.ALL, 5 )

		self.m_staticText_null0Fuse = wx.StaticText( self.m_panel_fuseUtil, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 31,15 ), 0 )
		self.m_staticText_null0Fuse.Wrap( -1 )

		bSizer_fuseGroupCtrl5.Add( self.m_staticText_null0Fuse, 0, wx.ALL, 5 )

		self.m_button_scan = wx.Button( self.m_panel_fuseUtil, wx.ID_ANY, u"Scan", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_button_scan, 0, wx.ALL, 5 )

		self.m_button_burn = wx.Button( self.m_panel_fuseUtil, wx.ID_ANY, u"Burn", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		bSizer_fuseGroupCtrl5.Add( self.m_button_burn, 0, wx.ALL, 5 )


		wSizer_fuseUtil.Add( bSizer_fuseGroupCtrl5, 1, wx.EXPAND, 5 )


		self.m_panel_fuseUtil.SetSizer( wSizer_fuseUtil )
		self.m_panel_fuseUtil.Layout()
		wSizer_fuseUtil.Fit( self.m_panel_fuseUtil )
		self.m_notebook_imageSeq.AddPage( self.m_panel_fuseUtil, u"eFuse Operation Utility", False )
		self.m_panel_memView = wx.Panel( self.m_notebook_imageSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_memView.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_memView = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_textCtrl_bootDeviceMem = wx.TextCtrl( self.m_panel_memView, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 740,370 ), wx.TE_MULTILINE|wx.TE_RICH2 )
		self.m_textCtrl_bootDeviceMem.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_textCtrl_bootDeviceMem.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )

		wSizer_memView.Add( self.m_textCtrl_bootDeviceMem, 0, wx.ALL, 5 )

		self.m_staticText_null0MemView = wx.StaticText( self.m_panel_memView, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText_null0MemView.Wrap( -1 )

		wSizer_memView.Add( self.m_staticText_null0MemView, 0, wx.ALL, 5 )

		self.m_button_viewMem = wx.Button( self.m_panel_memView, wx.ID_ANY, u"View", wx.DefaultPosition, wx.DefaultSize, 0 )
		wSizer_memView.Add( self.m_button_viewMem, 0, wx.ALL, 5 )

		self.m_staticText_null1MemView = wx.StaticText( self.m_panel_memView, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText_null1MemView.Wrap( -1 )

		wSizer_memView.Add( self.m_staticText_null1MemView, 0, wx.ALL, 5 )

		self.m_button_clearMem = wx.Button( self.m_panel_memView, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		wSizer_memView.Add( self.m_button_clearMem, 0, wx.ALL, 5 )


		self.m_panel_memView.SetSizer( wSizer_memView )
		self.m_panel_memView.Layout()
		wSizer_memView.Fit( self.m_panel_memView )
		self.m_notebook_imageSeq.AddPage( self.m_panel_memView, u"Boot Device Memory", False )

		bSizer_boot.Add( self.m_notebook_imageSeq, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_bootLog = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_panel_log = wx.Panel( self.m_notebook_bootLog, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_log.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_log = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		bSizer_showLog = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl_log = wx.TextCtrl( self.m_panel_log, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 650,68 ), wx.TE_MULTILINE )
		bSizer_showLog.Add( self.m_textCtrl_log, 0, wx.ALL, 5 )


		wSizer_log.Add( bSizer_showLog, 1, wx.EXPAND, 5 )

		bSizer_logAction = wx.BoxSizer( wx.VERTICAL )

		self.m_button_clearLog = wx.Button( self.m_panel_log, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_clearLog.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer_logAction.Add( self.m_button_clearLog, 0, wx.ALL, 5 )

		self.m_button_saveLog = wx.Button( self.m_panel_log, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_saveLog.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer_logAction.Add( self.m_button_saveLog, 0, wx.ALL, 5 )


		wSizer_log.Add( bSizer_logAction, 1, wx.EXPAND, 5 )

		bSizer_actionGauge = wx.BoxSizer( wx.VERTICAL )

		self.m_gauge_action = wx.Gauge( self.m_panel_log, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 750,-1 ), wx.GA_HORIZONTAL )
		self.m_gauge_action.SetValue( 100 )
		bSizer_actionGauge.Add( self.m_gauge_action, 0, wx.ALL, 5 )


		wSizer_log.Add( bSizer_actionGauge, 1, wx.EXPAND, 5 )


		self.m_panel_log.SetSizer( wSizer_log )
		self.m_panel_log.Layout()
		wSizer_log.Fit( self.m_panel_log )
		self.m_notebook_bootLog.AddPage( self.m_panel_log, u"Log", False )

		bSizer_boot.Add( self.m_notebook_bootLog, 1, wx.EXPAND |wx.ALL, 5 )


		wSizer_func.Add( bSizer_boot, 1, wx.EXPAND, 5 )


		bSizer_win.Add( wSizer_func, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer_win )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.callbackShowHomePage, id = self.m_menuItem_homePage.GetId() )
		self.Bind( wx.EVT_MENU, self.callbackShowAboutAuthor, id = self.m_menuIte_aboutAuthor.GetId() )
		self.m_choice_mcuSeries.Bind( wx.EVT_CHOICE, self.callbackSetMcuSeries )
		self.m_choice_mcuDevice.Bind( wx.EVT_CHOICE, self.callbackSetMcuDevice )
		self.m_choice_bootDevice.Bind( wx.EVT_CHOICE, self.callbackSetBootDevice )
		self.m_button_BootDeviceConfiguration.Bind( wx.EVT_BUTTON, self.callbackBootDeviceConfiguration )
		self.m_radioBtn_uart.Bind( wx.EVT_RADIOBUTTON, self.callbackSetUartPort )
		self.m_radioBtn_usbhid.Bind( wx.EVT_RADIOBUTTON, self.callbackSetUsbhidPort )
		self.m_button_connect.Bind( wx.EVT_BUTTON, self.callbackConnectToDevice )
		self.m_choice_secureBootType.Bind( wx.EVT_CHOICE, self.callbackSetSecureBootType )
		self.m_button_advCertSettings.Bind( wx.EVT_BUTTON, self.callbackAdvCertSettings )
		self.m_button_genCert.Bind( wx.EVT_BUTTON, self.callbackGenCert )
		self.m_choice_enableCertForBee.Bind( wx.EVT_CHOICE, self.callbackSetCertForBee )
		self.m_button_genImage.Bind( wx.EVT_BUTTON, self.callbackGenImage )
		self.m_choice_keyStorageRegion.Bind( wx.EVT_CHOICE, self.callbackSetKeyStorageRegion )
		self.m_button_advKeySettings.Bind( wx.EVT_BUTTON, self.callbackAdvKeySettings )
		self.m_button_prepBee.Bind( wx.EVT_BUTTON, self.callbackDoBeeEncryption )
		self.m_button_progSrk.Bind( wx.EVT_BUTTON, self.callbackProgramSrk )
		self.m_button_operBee.Bind( wx.EVT_BUTTON, self.callbackProgramBeeDek )
		self.m_button_flashImage.Bind( wx.EVT_BUTTON, self.callbackFlashImage )
		self.m_button_progDek.Bind( wx.EVT_BUTTON, self.callbackFlashHabDek )
		self.m_button_scan.Bind( wx.EVT_BUTTON, self.callbackScanFuse )
		self.m_button_burn.Bind( wx.EVT_BUTTON, self.callbackBurnFuse )
		self.m_button_viewMem.Bind( wx.EVT_BUTTON, self.callbackViewMem )
		self.m_button_clearMem.Bind( wx.EVT_BUTTON, self.callbackClearMem )
		self.m_button_clearLog.Bind( wx.EVT_BUTTON, self.callbackClearLog )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackShowHomePage( self, event ):
		event.Skip()

	def callbackShowAboutAuthor( self, event ):
		event.Skip()

	def callbackSetMcuSeries( self, event ):
		event.Skip()

	def callbackSetMcuDevice( self, event ):
		event.Skip()

	def callbackSetBootDevice( self, event ):
		event.Skip()

	def callbackBootDeviceConfiguration( self, event ):
		event.Skip()

	def callbackSetUartPort( self, event ):
		event.Skip()

	def callbackSetUsbhidPort( self, event ):
		event.Skip()

	def callbackConnectToDevice( self, event ):
		event.Skip()

	def callbackSetSecureBootType( self, event ):
		event.Skip()

	def callbackAdvCertSettings( self, event ):
		event.Skip()

	def callbackGenCert( self, event ):
		event.Skip()

	def callbackSetCertForBee( self, event ):
		event.Skip()

	def callbackGenImage( self, event ):
		event.Skip()

	def callbackSetKeyStorageRegion( self, event ):
		event.Skip()

	def callbackAdvKeySettings( self, event ):
		event.Skip()

	def callbackDoBeeEncryption( self, event ):
		event.Skip()

	def callbackProgramSrk( self, event ):
		event.Skip()

	def callbackProgramBeeDek( self, event ):
		event.Skip()

	def callbackFlashImage( self, event ):
		event.Skip()

	def callbackFlashHabDek( self, event ):
		event.Skip()

	def callbackScanFuse( self, event ):
		event.Skip()

	def callbackBurnFuse( self, event ):
		event.Skip()

	def callbackViewMem( self, event ):
		event.Skip()

	def callbackClearMem( self, event ):
		event.Skip()

	def callbackClearLog( self, event ):
		event.Skip()


