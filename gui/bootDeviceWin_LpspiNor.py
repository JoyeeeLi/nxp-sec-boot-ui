# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jul 11 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class MyFrame_LPSPI_NOR
###########################################################################

class bootDeviceWin_LpspiNor(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(454, 335), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.Bind(wx.EVT_CLOSE, self.OnClose_LPSPI_NOR)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        wSizer_LPSPI_NOR = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.m_notebook_LPSPI_NOR = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel_LPSPI_NOR = wx.Panel(self.m_notebook_LPSPI_NOR, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          wx.TAB_TRAVERSAL)
        gSizer_LPSPI_NOR = wx.GridSizer(0, 2, 0, 0)

        self.m_staticText_Page_Size = wx.StaticText(self.m_panel_LPSPI_NOR, wx.ID_ANY, u"Page Size:",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_Page_Size.Wrap(-1)

        gSizer_LPSPI_NOR.Add(self.m_staticText_Page_Size, 0, wx.ALL, 5)

        m_choice_Page_SizeChoices = [u"256 Bytes", u"512 Bytes", u"1024 Bytes", u"32 Bytes", u"64 Bytes", u"128 Bytes"]
        self.m_choice_Page_Size = wx.Choice(self.m_panel_LPSPI_NOR, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            m_choice_Page_SizeChoices, 0)
        self.m_choice_Page_Size.SetSelection(0)
        gSizer_LPSPI_NOR.Add(self.m_choice_Page_Size, 0, wx.ALL, 5)

        self.m_staticText_Sector_Size = wx.StaticText(self.m_panel_LPSPI_NOR, wx.ID_ANY, u"Sector Size:",
                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_Sector_Size.Wrap(-1)

        gSizer_LPSPI_NOR.Add(self.m_staticText_Sector_Size, 0, wx.ALL, 5)

        m_choice_Sector_SizeChoices = [u"4 KBytes", u"8 KBytes", u"32 KBytes", u"64 KBytes", u"128 KBytes",
                                       u"256 KBytes"]
        self.m_choice_Sector_Size = wx.Choice(self.m_panel_LPSPI_NOR, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              m_choice_Sector_SizeChoices, 0)
        self.m_choice_Sector_Size.SetSelection(0)
        gSizer_LPSPI_NOR.Add(self.m_choice_Sector_Size, 0, wx.ALL, 5)

        self.m_staticText_Memory_Size = wx.StaticText(self.m_panel_LPSPI_NOR, wx.ID_ANY, u"Memory Size:",
                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_Memory_Size.Wrap(-1)

        gSizer_LPSPI_NOR.Add(self.m_staticText_Memory_Size, 0, wx.ALL, 5)

        m_choice_Memory_SizeChoices = [u"512 KBytes", u"1024 KBytes", u"2 MBytes", u"4 MBytes", u"8 MBytes",
                                       u"16 MBytes", u"32 MBytes", u"64 MBytes", u"128 MBytes", u"256 MBytes",
                                       u"512 MBytes", u"1024 MBytes", u"32 KBytes", u"64 KBytes", u"128 KBytes",
                                       u"256 KBytes"]
        self.m_choice_Memory_Size = wx.Choice(self.m_panel_LPSPI_NOR, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              m_choice_Memory_SizeChoices, 0)
        self.m_choice_Memory_Size.SetSelection(0)
        gSizer_LPSPI_NOR.Add(self.m_choice_Memory_Size, 0, wx.ALL, 5)

        self.m_staticText_Memory_Type = wx.StaticText(self.m_panel_LPSPI_NOR, wx.ID_ANY, u"Memory Type:",
                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_Memory_Type.Wrap(-1)

        gSizer_LPSPI_NOR.Add(self.m_staticText_Memory_Type, 0, wx.ALL, 5)

        m_choice_Memory_TypeChoices = [u"NOR Flash", u"EEPROM"]
        self.m_choice_Memory_Type = wx.Choice(self.m_panel_LPSPI_NOR, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              m_choice_Memory_TypeChoices, 0)
        self.m_choice_Memory_Type.SetSelection(0)
        gSizer_LPSPI_NOR.Add(self.m_choice_Memory_Type, 0, wx.ALL, 5)

        self.m_staticText_PCS_Index = wx.StaticText(self.m_panel_LPSPI_NOR, wx.ID_ANY, u"PCS Index:",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_PCS_Index.Wrap(-1)

        gSizer_LPSPI_NOR.Add(self.m_staticText_PCS_Index, 0, wx.ALL, 5)

        m_choice_PCS_IndexChoices = [u"PCS0", u"PCS1", u"PCS2", u"PCS3"]
        self.m_choice_PCS_Index = wx.Choice(self.m_panel_LPSPI_NOR, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            m_choice_PCS_IndexChoices, 0)
        self.m_choice_PCS_Index.SetSelection(0)
        gSizer_LPSPI_NOR.Add(self.m_choice_PCS_Index, 0, wx.ALL, 5)

        self.m_staticText_SPI_Index = wx.StaticText(self.m_panel_LPSPI_NOR, wx.ID_ANY, u"SPI Index:",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_SPI_Index.Wrap(-1)

        gSizer_LPSPI_NOR.Add(self.m_staticText_SPI_Index, 0, wx.ALL, 5)

        m_choice_SPI_IndexChoices = [u"SPI1", u"SPI2", u"SPI3", u"SPI4"]
        self.m_choice_SPI_Index = wx.Choice(self.m_panel_LPSPI_NOR, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            m_choice_SPI_IndexChoices, 0)
        self.m_choice_SPI_Index.SetSelection(0)
        gSizer_LPSPI_NOR.Add(self.m_choice_SPI_Index, 0, wx.ALL, 5)

        self.m_staticText_Option1_Size = wx.StaticText(self.m_panel_LPSPI_NOR, wx.ID_ANY, u"Option1 Size:",
                                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_Option1_Size.Wrap(-1)

        gSizer_LPSPI_NOR.Add(self.m_staticText_Option1_Size, 0, wx.ALL, 5)

        self.m_textCtrl_Option1_Size = wx.TextCtrl(self.m_panel_LPSPI_NOR, wx.ID_ANY, u"1",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer_LPSPI_NOR.Add(self.m_textCtrl_Option1_Size, 0, wx.ALL, 5)

        self.m_panel_LPSPI_NOR.SetSizer(gSizer_LPSPI_NOR)
        self.m_panel_LPSPI_NOR.Layout()
        gSizer_LPSPI_NOR.Fit(self.m_panel_LPSPI_NOR)
        self.m_notebook_LPSPI_NOR.AddPage(self.m_panel_LPSPI_NOR, u"Option 0", False)

        wSizer_LPSPI_NOR.Add(self.m_notebook_LPSPI_NOR, 1, wx.EXPAND | wx.ALL, 5)

        self.m_notebook2 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel2 = wx.Panel(self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer2 = wx.GridSizer(0, 2, 0, 0)

        self.m_staticText_SPI_Speed = wx.StaticText(self.m_panel2, wx.ID_ANY, u"SPI Speed:", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
        self.m_staticText_SPI_Speed.Wrap(-1)

        gSizer2.Add(self.m_staticText_SPI_Speed, 0, wx.ALL, 5)

        m_choice_SPI_SpeedChoices = [u"20 MHZ", u"10 MHZ", u"5 MHZ", u"2 MHZ"]
        self.m_choice_SPI_Speed = wx.Choice(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            m_choice_SPI_SpeedChoices, 0)
        self.m_choice_SPI_Speed.SetSelection(0)
        gSizer2.Add(self.m_choice_SPI_Speed, 0, wx.ALL, 5)

        self.m_panel2.SetSizer(gSizer2)
        self.m_panel2.Layout()
        gSizer2.Fit(self.m_panel2)
        self.m_notebook2.AddPage(self.m_panel2, u"Option 1", False)

        wSizer_LPSPI_NOR.Add(self.m_notebook2, 1, wx.EXPAND | wx.ALL, 5)

        self.m_staticText_LPSPI_NOR = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                    wx.Size(235, -1), 0)
        self.m_staticText_LPSPI_NOR.Wrap(-1)

        wSizer_LPSPI_NOR.Add(self.m_staticText_LPSPI_NOR, 0, wx.ALL, 5)

        m_sdbSizer_LPSPI_NOR = wx.StdDialogButtonSizer()
        self.m_sdbSizer_LPSPI_NOROK = wx.Button(self, wx.ID_OK)
        m_sdbSizer_LPSPI_NOR.AddButton(self.m_sdbSizer_LPSPI_NOROK)
        self.m_sdbSizer_LPSPI_NORCancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer_LPSPI_NOR.AddButton(self.m_sdbSizer_LPSPI_NORCancel)
        m_sdbSizer_LPSPI_NOR.Realize();

        wSizer_LPSPI_NOR.Add(m_sdbSizer_LPSPI_NOR, 1, wx.EXPAND, 5)

        self.SetSizer(wSizer_LPSPI_NOR)
        self.Layout()

        self.Centre(wx.BOTH)
        self.m_sdbSizer_LPSPI_NORCancel.Bind(wx.EVT_BUTTON, self.cancel_of_LPSPI_NOR)
        self.m_sdbSizer_LPSPI_NOROK.Bind(wx.EVT_BUTTON, self.apply_of_LPSPI_NOR)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def cancel_of_LPSPI_NOR(self, event):
        event.Skip()

    def apply_of_LPSPI_NOR(self, event):
        event.Skip()

    def OnClose_LPSPI_NOR(self, event):
        event.Skip()





