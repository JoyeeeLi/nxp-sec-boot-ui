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
## Class bootDeviceWin_SemcNand
###########################################################################

class bootDeviceWin_SemcNand ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 785,370 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer9 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook6 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel27 = wx.Panel( self.m_notebook6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText27 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"ONFI Version:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		gSizer1.Add( self.m_staticText27, 0, wx.ALL, 5 )

		m_choice12Choices = [ u"ONFI 1.x" ]
		self.m_choice12 = wx.Choice( self.m_panel27, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice12Choices, 0 )
		self.m_choice12.SetSelection( 0 )
		gSizer1.Add( self.m_choice12, 0, wx.ALL, 5 )

		self.m_staticText30 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"ONFI Timing Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )

		gSizer1.Add( self.m_staticText30, 0, wx.ALL, 5 )

		m_choice15Choices = [ u"Mode0 - 10MHz" ]
		self.m_choice15 = wx.Choice( self.m_panel27, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice15Choices, 0 )
		self.m_choice15.SetSelection( 0 )
		gSizer1.Add( self.m_choice15, 0, wx.ALL, 5 )

		self.m_staticText31 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"EDO Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		gSizer1.Add( self.m_staticText31, 0, wx.ALL, 5 )

		m_choice16Choices = [ u"Enabled", u"Disabled" ]
		self.m_choice16 = wx.Choice( self.m_panel27, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice16Choices, 0 )
		self.m_choice16.SetSelection( 0 )
		gSizer1.Add( self.m_choice16, 0, wx.ALL, 5 )

		self.m_staticText32 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"I/O Port Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		gSizer1.Add( self.m_staticText32, 0, wx.ALL, 5 )

		m_choice17Choices = [ u"x8 bits", u"x16 bits" ]
		self.m_choice17 = wx.Choice( self.m_panel27, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice17Choices, 0 )
		self.m_choice17.SetSelection( 0 )
		gSizer1.Add( self.m_choice17, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"PCS Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		gSizer1.Add( self.m_staticText33, 0, wx.ALL, 5 )

		m_choice18Choices = [ u"CSX0" ]
		self.m_choice18 = wx.Choice( self.m_panel27, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice18Choices, 0 )
		self.m_choice18.SetSelection( 0 )
		gSizer1.Add( self.m_choice18, 0, wx.ALL, 5 )

		self.m_staticText34 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"ECC Type:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )

		gSizer1.Add( self.m_staticText34, 0, wx.ALL, 5 )

		m_choice19Choices = [ u"SW - 1bit ECC", u"HW" ]
		self.m_choice19 = wx.Choice( self.m_panel27, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice19Choices, 0 )
		self.m_choice19.SetSelection( 0 )
		gSizer1.Add( self.m_choice19, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"Initial ECC status:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		gSizer1.Add( self.m_staticText35, 0, wx.ALL, 5 )

		m_choice20Choices = [ u"Enabled", u"Disabled" ]
		self.m_choice20 = wx.Choice( self.m_panel27, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice20Choices, 0 )
		self.m_choice20.SetSelection( 0 )
		gSizer1.Add( self.m_choice20, 0, wx.ALL, 5 )


		self.m_panel27.SetSizer( gSizer1 )
		self.m_panel27.Layout()
		gSizer1.Fit( self.m_panel27 )
		self.m_notebook6.AddPage( self.m_panel27, u"Nand Option", False )

		wSizer9.Add( self.m_notebook6, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook7 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel28 = wx.Panel( self.m_notebook7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText28 = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Search Count:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )

		gSizer2.Add( self.m_staticText28, 0, wx.ALL, 5 )

		m_choice13Choices = [ u"1", u"2" ]
		self.m_choice13 = wx.Choice( self.m_panel28, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice13Choices, 0 )
		self.m_choice13.SetSelection( 0 )
		gSizer2.Add( self.m_choice13, 0, wx.ALL, 5 )

		self.m_staticText36 = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Search Stride:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText36.Wrap( -1 )

		gSizer2.Add( self.m_staticText36, 0, wx.ALL, 5 )

		m_choice21Choices = [ u"64", u"2", u"4", u"8", u"16", u"32", u"128", u"256", u"512", u"1024", u"2048", u"4096", u"8192", u"16384", u"32768" ]
		self.m_choice21 = wx.Choice( self.m_panel28, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice21Choices, 0 )
		self.m_choice21.SetSelection( 0 )
		gSizer2.Add( self.m_choice21, 0, wx.ALL, 5 )

		self.m_staticText37 = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Image Copies", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText37.Wrap( -1 )

		gSizer2.Add( self.m_staticText37, 0, wx.ALL, 5 )

		m_choice22Choices = [ u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8" ]
		self.m_choice22 = wx.Choice( self.m_panel28, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice22Choices, 0 )
		self.m_choice22.SetSelection( 0 )
		gSizer2.Add( self.m_choice22, 0, wx.ALL, 5 )

		self.m_staticText38 = wx.StaticText( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )

		gSizer2.Add( self.m_staticText38, 0, wx.ALL, 5 )

		self.m_staticText39 = wx.StaticText( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )

		gSizer2.Add( self.m_staticText39, 0, wx.ALL, 5 )

		self.m_staticText40 = wx.StaticText( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )

		gSizer2.Add( self.m_staticText40, 0, wx.ALL, 5 )

		self.m_staticText41 = wx.StaticText( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )

		gSizer2.Add( self.m_staticText41, 0, wx.ALL, 5 )

		self.m_staticText42 = wx.StaticText( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )

		gSizer2.Add( self.m_staticText42, 0, wx.ALL, 5 )

		self.m_staticText43 = wx.StaticText( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )

		gSizer2.Add( self.m_staticText43, 0, wx.ALL, 5 )

		self.m_staticText44 = wx.StaticText( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )

		gSizer2.Add( self.m_staticText44, 0, wx.ALL, 5 )

		self.m_staticText45 = wx.StaticText( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )

		gSizer2.Add( self.m_staticText45, 0, wx.ALL, 5 )


		self.m_panel28.SetSizer( gSizer2 )
		self.m_panel28.Layout()
		gSizer2.Fit( self.m_panel28 )
		self.m_notebook7.AddPage( self.m_panel28, u"FCB Option", False )

		wSizer9.Add( self.m_notebook7, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook8 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel29 = wx.Panel( self.m_notebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer3 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText29 = wx.StaticText( self.m_panel29, wx.ID_ANY, u"Block Index", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		gSizer3.Add( self.m_staticText29, 0, wx.ALL, 5 )

		self.m_staticText46 = wx.StaticText( self.m_panel29, wx.ID_ANY, u"Block Count", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )

		gSizer3.Add( self.m_staticText46, 0, wx.ALL, 5 )

		self.m_textCtrl11 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl11, 0, wx.ALL, 5 )

		self.m_textCtrl12 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl12, 0, wx.ALL, 5 )

		self.m_textCtrl13 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl13, 0, wx.ALL, 5 )

		self.m_textCtrl14 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl14, 0, wx.ALL, 5 )

		self.m_textCtrl15 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl15, 0, wx.ALL, 5 )

		self.m_textCtrl16 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl16, 0, wx.ALL, 5 )

		self.m_textCtrl17 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl17, 0, wx.ALL, 5 )

		self.m_textCtrl18 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl18, 0, wx.ALL, 5 )

		self.m_textCtrl19 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl19, 0, wx.ALL, 5 )

		self.m_textCtrl20 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl20, 0, wx.ALL, 5 )

		self.m_textCtrl21 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl21, 0, wx.ALL, 5 )

		self.m_textCtrl22 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl22, 0, wx.ALL, 5 )

		self.m_textCtrl23 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl23, 0, wx.ALL, 5 )

		self.m_textCtrl24 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl24, 0, wx.ALL, 5 )

		self.m_textCtrl25 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl25, 0, wx.ALL, 5 )

		self.m_textCtrl26 = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_textCtrl26, 0, wx.ALL, 5 )


		self.m_panel29.SetSizer( gSizer3 )
		self.m_panel29.Layout()
		gSizer3.Fit( self.m_panel29 )
		self.m_notebook8.AddPage( self.m_panel29, u"Image Info", False )

		wSizer9.Add( self.m_notebook8, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( wSizer9 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


