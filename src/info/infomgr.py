#! /usr/bin/env python
import wx
import sys
import os
sys.path.append(os.path.abspath(".."))
from ui import uicore

class secBootInfo(uicore.secBootUi):

    def __init__(self, parent):
        uicore.secBootUi.__init__(self, parent)

    def printLog( self ,logoStr ):
        self.m_textCtrl_log.write(logoStr + "\n")

    def clearLog( self ):
        self.m_textCtrl_log.Clear()

    def printDeviceStatus( self ,statusStr ):
        self.m_textCtrl_deviceStatus.write(statusStr + "\n")

    def clearDeviceStatus( self ):
        self.m_textCtrl_deviceStatus.Clear()

