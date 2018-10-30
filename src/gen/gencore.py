#! /usr/bin/env python
import wx
import sys
import os
import bincopy
sys.path.append(os.path.abspath(".."))
from info import infomgr
from utils import elf
from ui import uidef
from gen import gendef

class secBootGen(infomgr.secBootInfo):

    def __init__(self, parent):
        infomgr.secBootInfo.__init__(self, parent)

        self.srcAppFilename = None
        self.destAppFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bootable_image', 'ivt_application.bin')
        self.bdFilepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bd_file')
        self.bdName = None
        self.bdfilename = None
        self.elftosbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'elftosb', 'win')

    def _updateBdfileContent( self, startAddress, ivtOffset, initialLoadSize, entryPointAddress):
        pass

    def createMatchedBdfile( self ):
        self.srcAppFilename = self.m_filePicker_appPath.GetPath()
        if os.path.isfile(self.srcAppFilename):
            startAddress = None
            entryPointAddress = None
            appPath, appFilename = os.path.split(self.srcAppFilename)
            appName, appType = os.path.splitext(appFilename)
            if appType == '.elf':
                elfObj = None
                with open(self.srcAppFilename, 'rb') as f:
                    e = elf.ELFObject()
                    e.fromFile(f)
                    elfObj = e
                for symbol in gendef.kToolchainSymbolList_VectorAddr:
                    try:
                        startAddress = elfObj.getSymbol(symbol).st_value
                        break
                    except:
                        pass
                #entryPointAddress = elfObj.e_entry
                for symbol in gendef.kToolchainSymbolList_EntryAddr:
                    try:
                        entryPointAddress = elfObj.getSymbol(symbol).st_value
                        break
                    except:
                        pass
            elif appType == '.s19' or appType == '.srec':
                srecObj = bincopy.BinFile(str(self.srcAppFilename))
                startAddress = srecObj.minimum_address
                #entryPointAddress = srecObj.execution_start_address
                entryPointAddress = self.getVal32FromByteArray(srecObj.as_binary(startAddress + 0x4, startAddress  + 0x8))
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

