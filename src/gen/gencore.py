#! /usr/bin/env python
import wx
import sys
import os
sys.path.append(os.path.abspath(".."))
from info import infomgr
from utils import elf
from ui import uidef

class secBootGen(infomgr.secBootInfo):

    def __init__(self, parent):
        infomgr.secBootInfo.__init__(self, parent)

        self.srcAppFilename = None
        self.elfObject = None
        self.destAppFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bootable_image', 'ivt_application.bin')
        self.bdFilepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bd_file')
        self.bdName = None
        self.bdfilename = None
        self.elftosbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'elftosb', 'win')

    def _updateBdfileContent( self, startAddress, ivtOffset, initialLoadSize, entryPointAddress)

    def createMatchedBdfile( self ):
        self.srcAppFilename = self.m_filePicker_appPath.GetPath()
        if os.path.isfile(self.srcAppFilename):
            appPath, appFilename = os.path.split(self.srcAppFilename)
            appName, appType = os.path.splitext(appFilename)
            if appType == '.elf':
                with open(self.srcAppFilename, 'rb') as f:
                    e = elf.ELFObject()
                    e.fromFile(f)
                    self.elfObject = e
                print hex(self.elfObject.getSymbol('Reset_Handler').st_value)
                print hex(self.elfObject.getSymbol('__VECTOR_TABLE').st_value)
            elif appType == '.s19' or appType == '.srec':
                pass
            else:
                pass
            if self.secureBootType == uidef.kSecureBootType_Development:
                self.bdName = 'imx-unsigned.bd'
                self.bafilename = os.path.join(self.bdFilepath, self.bdName)
            else:
                pass
        else:
            return False

    def genBootableImage( self ):
        pass

