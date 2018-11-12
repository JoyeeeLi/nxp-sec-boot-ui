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
## Class advSettingsWin_FlexibleUserKeys
###########################################################################

class advSettingsWin_FlexibleUserKeys ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 934,636 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer_win = wx.BoxSizer( wx.VERTICAL )

		wSizer_Opt = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook_encryptionOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_encryptionOpt = wx.Panel( self.m_notebook_encryptionOpt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		wSizer_encryptionOpt = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_regionSel = wx.StaticText( self.m_panel_encryptionOpt, wx.ID_ANY, u"Region Selection:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_regionSel.Wrap( -1 )

		wSizer_encryptionOpt.Add( self.m_staticText_regionSel, 0, wx.ALL, 5 )

		m_choice_regionSelChoices = [ u"Region 0", u"Region 1", u"Both Regions" ]
		self.m_choice_regionSel = wx.Choice( self.m_panel_encryptionOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_regionSelChoices, 0 )
		self.m_choice_regionSel.SetSelection( 0 )
		wSizer_encryptionOpt.Add( self.m_choice_regionSel, 0, wx.ALL, 5 )

		self.m_staticText_null0EncryptionOpt = wx.StaticText( self.m_panel_encryptionOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 9,-1 ), 0 )
		self.m_staticText_null0EncryptionOpt.Wrap( -1 )

		wSizer_encryptionOpt.Add( self.m_staticText_null0EncryptionOpt, 0, wx.ALL, 5 )

		self.m_staticText_beeEngKeySel = wx.StaticText( self.m_panel_encryptionOpt, wx.ID_ANY, u"BEE Engine Key Selection:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_beeEngKeySel.Wrap( -1 )

		wSizer_encryptionOpt.Add( self.m_staticText_beeEngKeySel, 0, wx.ALL, 5 )

		m_choice_beeEngKeySelChoices = [ u"Random Key", u"Zero Key" ]
		self.m_choice_beeEngKeySel = wx.Choice( self.m_panel_encryptionOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_beeEngKeySelChoices, 0 )
		self.m_choice_beeEngKeySel.SetSelection( 1 )
		wSizer_encryptionOpt.Add( self.m_choice_beeEngKeySel, 0, wx.ALL, 5 )

		self.m_staticText_imageType = wx.StaticText( self.m_panel_encryptionOpt, wx.ID_ANY, u"Image Type:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_imageType.Wrap( -1 )

		wSizer_encryptionOpt.Add( self.m_staticText_imageType, 0, wx.ALL, 5 )

		m_choice_imageTypeChoices = [ u"Non-Bootable", u"Bootable" ]
		self.m_choice_imageType = wx.Choice( self.m_panel_encryptionOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_imageTypeChoices, 0 )
		self.m_choice_imageType.SetSelection( 1 )
		wSizer_encryptionOpt.Add( self.m_choice_imageType, 0, wx.ALL, 5 )

		self.m_staticText_null1EncryptionOpt = wx.StaticText( self.m_panel_encryptionOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 9,-1 ), 0 )
		self.m_staticText_null1EncryptionOpt.Wrap( -1 )

		wSizer_encryptionOpt.Add( self.m_staticText_null1EncryptionOpt, 0, wx.ALL, 5 )

		self.m_staticText_xipBaseAddr = wx.StaticText( self.m_panel_encryptionOpt, wx.ID_ANY, u"XIP Base Address:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_xipBaseAddr.Wrap( -1 )

		wSizer_encryptionOpt.Add( self.m_staticText_xipBaseAddr, 0, wx.ALL, 5 )

		m_choice_xipBaseAddrChoices = [ u"0x60000000" ]
		self.m_choice_xipBaseAddr = wx.Choice( self.m_panel_encryptionOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_xipBaseAddrChoices, 0 )
		self.m_choice_xipBaseAddr.SetSelection( 0 )
		wSizer_encryptionOpt.Add( self.m_choice_xipBaseAddr, 0, wx.ALL, 5 )

		self.m_staticText_null2EncryptionOpt = wx.StaticText( self.m_panel_encryptionOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 890,2 ), 0 )
		self.m_staticText_null2EncryptionOpt.Wrap( -1 )

		wSizer_encryptionOpt.Add( self.m_staticText_null2EncryptionOpt, 0, wx.ALL, 5 )


		self.m_panel_encryptionOpt.SetSizer( wSizer_encryptionOpt )
		self.m_panel_encryptionOpt.Layout()
		wSizer_encryptionOpt.Fit( self.m_panel_encryptionOpt )
		self.m_notebook_encryptionOpt.AddPage( self.m_panel_encryptionOpt, u"Encryption Option", False )

		wSizer_Opt.Add( self.m_notebook_encryptionOpt, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer_win.Add( wSizer_Opt, 1, wx.EXPAND, 5 )

		wSizer_Info = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook_region0Info = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_region0Info = wx.Panel( self.m_notebook_region0Info, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_region0Info = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_region0keySource = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"Key Source:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0keySource.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0keySource, 0, wx.ALL, 5 )

		m_choice_region0keySourceChoices = [ u"Fuse SW-GP2", u"Fuse GP4[127:0]" ]
		self.m_choice_region0keySource = wx.Choice( self.m_panel_region0Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region0keySourceChoices, 0 )
		self.m_choice_region0keySource.SetSelection( 1 )
		gSizer_region0Info.Add( self.m_choice_region0keySource, 0, wx.ALL, 5 )

		self.m_staticText_region0UserKeyData = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"User Key Data:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0UserKeyData.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0UserKeyData, 0, wx.ALL, 5 )

		self.m_textCtrl_region0UserKeyData = wx.TextCtrl( self.m_panel_region0Info, wx.ID_ANY, u"0123456789abcdeffedcba9876543210", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region0Info.Add( self.m_textCtrl_region0UserKeyData, 0, wx.ALL, 5 )

		self.m_staticText_region0AesMode = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"AES Mode:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0AesMode.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0AesMode, 0, wx.ALL, 5 )

		m_choice_region0AesModeChoices = [ u"ECB", u"CTR" ]
		self.m_choice_region0AesMode = wx.Choice( self.m_panel_region0Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region0AesModeChoices, 0 )
		self.m_choice_region0AesMode.SetSelection( 1 )
		self.m_choice_region0AesMode.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_choice_region0AesMode.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		gSizer_region0Info.Add( self.m_choice_region0AesMode, 0, wx.ALL, 5 )

		self.m_staticText_region0FacCnt = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"FAC Region Count:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0FacCnt.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0FacCnt, 0, wx.ALL, 5 )

		m_choice_region0FacCntChoices = [ u"1", u"2", u"3" ]
		self.m_choice_region0FacCnt = wx.Choice( self.m_panel_region0Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region0FacCntChoices, 0 )
		self.m_choice_region0FacCnt.SetSelection( 0 )
		gSizer_region0Info.Add( self.m_choice_region0FacCnt, 0, wx.ALL, 5 )

		self.m_staticText_region0Fac0Start = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"FAC0 Region Start (eg. 0x60001000):", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0Fac0Start.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0Fac0Start, 0, wx.ALL, 5 )

		self.m_textCtrl_region0Fac0Start = wx.TextCtrl( self.m_panel_region0Info, wx.ID_ANY, u"0x60001000", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region0Info.Add( self.m_textCtrl_region0Fac0Start, 0, wx.ALL, 5 )

		self.m_staticText_region0Fac0Length = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"FAC0 Region Length (eg. 0x1000):", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0Fac0Length.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0Fac0Length, 0, wx.ALL, 5 )

		self.m_textCtrl_region0Fac0Length = wx.TextCtrl( self.m_panel_region0Info, wx.ID_ANY, u"0x2000", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region0Info.Add( self.m_textCtrl_region0Fac0Length, 0, wx.ALL, 5 )

		self.m_staticText_region0Fac1Start = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"FAC1 Region Start:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0Fac1Start.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0Fac1Start, 0, wx.ALL, 5 )

		self.m_textCtrl_region0Fac1Start = wx.TextCtrl( self.m_panel_region0Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region0Info.Add( self.m_textCtrl_region0Fac1Start, 0, wx.ALL, 5 )

		self.m_staticText_region0Fac1Length = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"FAC1 Region Length:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0Fac1Length.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0Fac1Length, 0, wx.ALL, 5 )

		self.m_textCtrl_region0Fac1Length = wx.TextCtrl( self.m_panel_region0Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region0Info.Add( self.m_textCtrl_region0Fac1Length, 0, wx.ALL, 5 )

		self.m_staticText_region0Fac2Start = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"FAC2 Region Start:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0Fac2Start.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0Fac2Start, 0, wx.ALL, 5 )

		self.m_textCtrl_region0Fac2Start = wx.TextCtrl( self.m_panel_region0Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region0Info.Add( self.m_textCtrl_region0Fac2Start, 0, wx.ALL, 5 )

		self.m_staticText_region0Fac2Length = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"FAC2 Region Length:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0Fac2Length.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0Fac2Length, 0, wx.ALL, 5 )

		self.m_textCtrl_region0Fac2Length = wx.TextCtrl( self.m_panel_region0Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region0Info.Add( self.m_textCtrl_region0Fac2Length, 0, wx.ALL, 5 )

		self.m_staticText_region0AccessPermision = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"Access Permision:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0AccessPermision.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0AccessPermision, 0, wx.ALL, 5 )

		m_choice_region0AccessPermisionChoices = [ u"No Limitation", u"Debug Disabled", u"Execute Only, Debug Allowed", u"Execute Only, Debug Disabled" ]
		self.m_choice_region0AccessPermision = wx.Choice( self.m_panel_region0Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region0AccessPermisionChoices, 0 )
		self.m_choice_region0AccessPermision.SetSelection( 0 )
		gSizer_region0Info.Add( self.m_choice_region0AccessPermision, 0, wx.ALL, 5 )

		self.m_staticText_region0Lock = wx.StaticText( self.m_panel_region0Info, wx.ID_ANY, u"Region Lock:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region0Lock.Wrap( -1 )

		gSizer_region0Info.Add( self.m_staticText_region0Lock, 0, wx.ALL, 5 )

		m_choice_region0LockChoices = [ u"No Lock" ]
		self.m_choice_region0Lock = wx.Choice( self.m_panel_region0Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region0LockChoices, 0 )
		self.m_choice_region0Lock.SetSelection( 0 )
		gSizer_region0Info.Add( self.m_choice_region0Lock, 0, wx.ALL, 5 )


		self.m_panel_region0Info.SetSizer( gSizer_region0Info )
		self.m_panel_region0Info.Layout()
		gSizer_region0Info.Fit( self.m_panel_region0Info )
		self.m_notebook_region0Info.AddPage( self.m_panel_region0Info, u"Encrypted Region 0 Info", False )

		wSizer_Info.Add( self.m_notebook_region0Info, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_region1Info = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_region1Info = wx.Panel( self.m_notebook_region1Info, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_region1Info = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_region1keySource = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"Key Source:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1keySource.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1keySource, 0, wx.ALL, 5 )

		m_choice_region1keySourceChoices = [ u"Fuse SW-GP2", u"Fuse GP4[127:0]" ]
		self.m_choice_region1keySource = wx.Choice( self.m_panel_region1Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region1keySourceChoices, 0 )
		self.m_choice_region1keySource.SetSelection( 1 )
		gSizer_region1Info.Add( self.m_choice_region1keySource, 0, wx.ALL, 5 )

		self.m_staticText_region1UserKeyData = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"User Key Data:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1UserKeyData.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1UserKeyData, 0, wx.ALL, 5 )

		self.m_textCtrl_region1UserKeyData = wx.TextCtrl( self.m_panel_region1Info, wx.ID_ANY, u"0123456789abcdeffedcba9876543210", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region1Info.Add( self.m_textCtrl_region1UserKeyData, 0, wx.ALL, 5 )

		self.m_staticText_region1AesMode = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"AES Mode:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1AesMode.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1AesMode, 0, wx.ALL, 5 )

		m_choice_region1AesModeChoices = [ u"ECB", u"CTR" ]
		self.m_choice_region1AesMode = wx.Choice( self.m_panel_region1Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region1AesModeChoices, 0 )
		self.m_choice_region1AesMode.SetSelection( 1 )
		gSizer_region1Info.Add( self.m_choice_region1AesMode, 0, wx.ALL, 5 )

		self.m_staticText_region1FacCnt = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"FAC Region Count:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1FacCnt.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1FacCnt, 0, wx.ALL, 5 )

		m_choice_region1FacCntChoices = [ u"1", u"2", u"3" ]
		self.m_choice_region1FacCnt = wx.Choice( self.m_panel_region1Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region1FacCntChoices, 0 )
		self.m_choice_region1FacCnt.SetSelection( 0 )
		gSizer_region1Info.Add( self.m_choice_region1FacCnt, 0, wx.ALL, 5 )

		self.m_staticText_region1Fac0Start = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"FAC0 Region Start (eg. 0x60001000):", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1Fac0Start.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1Fac0Start, 0, wx.ALL, 5 )

		self.m_textCtrl_region1Fac0Start = wx.TextCtrl( self.m_panel_region1Info, wx.ID_ANY, u"0x60003000", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region1Info.Add( self.m_textCtrl_region1Fac0Start, 0, wx.ALL, 5 )

		self.m_staticText_region1Fac0Length = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"FAC0 Region Length (eg. 0x1000):", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1Fac0Length.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1Fac0Length, 0, wx.ALL, 5 )

		self.m_textCtrl_region1Fac0Length = wx.TextCtrl( self.m_panel_region1Info, wx.ID_ANY, u"0xc000", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region1Info.Add( self.m_textCtrl_region1Fac0Length, 0, wx.ALL, 5 )

		self.m_staticText_region1Fac1Start = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"FAC1 Region Start:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1Fac1Start.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1Fac1Start, 0, wx.ALL, 5 )

		self.m_textCtrl_region1Fac1Start = wx.TextCtrl( self.m_panel_region1Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region1Info.Add( self.m_textCtrl_region1Fac1Start, 0, wx.ALL, 5 )

		self.m_staticText_region1Fac1Length = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"FAC1 Region Length:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1Fac1Length.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1Fac1Length, 0, wx.ALL, 5 )

		self.m_textCtrl_region1Fac1Length = wx.TextCtrl( self.m_panel_region1Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region1Info.Add( self.m_textCtrl_region1Fac1Length, 0, wx.ALL, 5 )

		self.m_staticText_region1Fac2Start = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"FAC2 Region Start:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1Fac2Start.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1Fac2Start, 0, wx.ALL, 5 )

		self.m_textCtrl_region1Fac2Start = wx.TextCtrl( self.m_panel_region1Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region1Info.Add( self.m_textCtrl_region1Fac2Start, 0, wx.ALL, 5 )

		self.m_staticText_region1Fac2Length = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"FAC2 Region Length:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1Fac2Length.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1Fac2Length, 0, wx.ALL, 5 )

		self.m_textCtrl_region1Fac2Length = wx.TextCtrl( self.m_panel_region1Info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		gSizer_region1Info.Add( self.m_textCtrl_region1Fac2Length, 0, wx.ALL, 5 )

		self.m_staticText_region1AccessPermision = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"Access Permision:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1AccessPermision.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1AccessPermision, 0, wx.ALL, 5 )

		m_choice_region1AccessPermisionChoices = [ u"No Limitation", u"Debug Disabled", u"Execute Only, Debug Allowed", u"Execute Only, Debug Disabled" ]
		self.m_choice_region1AccessPermision = wx.Choice( self.m_panel_region1Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region1AccessPermisionChoices, 0 )
		self.m_choice_region1AccessPermision.SetSelection( 0 )
		gSizer_region1Info.Add( self.m_choice_region1AccessPermision, 0, wx.ALL, 5 )

		self.m_staticText_region1Lock = wx.StaticText( self.m_panel_region1Info, wx.ID_ANY, u"Region Lock:", wx.DefaultPosition, wx.Size( 210,-1 ), 0 )
		self.m_staticText_region1Lock.Wrap( -1 )

		gSizer_region1Info.Add( self.m_staticText_region1Lock, 0, wx.ALL, 5 )

		m_choice_region1LockChoices = [ u"No Lock" ]
		self.m_choice_region1Lock = wx.Choice( self.m_panel_region1Info, wx.ID_ANY, wx.DefaultPosition, wx.Size( 210,-1 ), m_choice_region1LockChoices, 0 )
		self.m_choice_region1Lock.SetSelection( 0 )
		gSizer_region1Info.Add( self.m_choice_region1Lock, 0, wx.ALL, 5 )


		self.m_panel_region1Info.SetSizer( gSizer_region1Info )
		self.m_panel_region1Info.Layout()
		gSizer_region1Info.Fit( self.m_panel_region1Info )
		self.m_notebook_region1Info.AddPage( self.m_panel_region1Info, u"Encrypted Region 1 Info", True )

		wSizer_Info.Add( self.m_notebook_region1Info, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer_win.Add( wSizer_Info, 1, wx.EXPAND, 5 )

		wSizer_action = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_null0Action = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 677,-1 ), 0 )
		self.m_staticText_null0Action.Wrap( -1 )

		wSizer_action.Add( self.m_staticText_null0Action, 0, wx.ALL, 5 )

		self.m_button_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		wSizer_action.Add( self.m_button_ok, 0, wx.ALL, 5 )

		self.m_button_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		wSizer_action.Add( self.m_button_cancel, 0, wx.ALL, 5 )


		bSizer_win.Add( wSizer_action, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer_win )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_choice_regionSel.Bind( wx.EVT_CHOICE, self.callbackChangeRegionSelection )
		self.m_choice_region0keySource.Bind( wx.EVT_CHOICE, self.callbackChangeRegion0KeySource )
		self.m_choice_region0FacCnt.Bind( wx.EVT_CHOICE, self.callbackChangeRegion0FacCnt )
		self.m_choice_region1keySource.Bind( wx.EVT_CHOICE, self.callbackChangeRegion1KeySource )
		self.m_choice_region1FacCnt.Bind( wx.EVT_CHOICE, self.callbackChangeRegion1FacCnt )
		self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackChangeRegionSelection( self, event ):
		event.Skip()

	def callbackChangeRegion0KeySource( self, event ):
		event.Skip()

	def callbackChangeRegion0FacCnt( self, event ):
		event.Skip()

	def callbackChangeRegion1KeySource( self, event ):
		event.Skip()

	def callbackChangeRegion1FacCnt( self, event ):
		event.Skip()

	def callbackOk( self, event ):
		event.Skip()

	def callbackCancel( self, event ):
		event.Skip()


