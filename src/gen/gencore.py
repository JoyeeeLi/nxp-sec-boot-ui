#! /usr/bin/env python
import wx
import sys
import os
import shutil
import bincopy
import gendef
sys.path.append(os.path.abspath(".."))
from info import infomgr
from utils import elf
from ui import uidef
from ui import uivar

class secBootGen(infomgr.secBootInfo):

    def __init__(self, parent):
        infomgr.secBootInfo.__init__(self, parent)

        self.serialFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'cert', 'serial')
        self.keypassFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'cert', 'key_pass.txt')
        self.cstKeysFolder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'cst', 'release', 'keys')
        self.cstCrtsFolder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'cst', 'release', 'crts')
        self.hab4PkiTreePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'cst', 'release', 'keys')
        self.hab4PkiTreeName = 'hab4_pki_tree.bat'
        self.srcAppFilename = None
        self.destAppFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bootable_image', 'ivt_application.bin')
        self.destAppNoPaddingFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bootable_image', 'ivt_application_nopadding.bin')
        self.bdFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bd_file', 'imx_secure_boot.bd')
        self.elftosbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'elftosb', 'win', 'elftosb.exe')
        self.batFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bd_file', 'imx_secure_boot.bat')

    def _copySerialAndKeypassfileToCstFolder( self ):
        shutil.copy(self.serialFilename, self.cstKeysFolder)
        shutil.copy(self.keypassFilename, self.cstKeysFolder)
        self.printLog('serial and key_pass.txt are copied to: ' + self.cstKeysFolder)

    def createSerialAndKeypassfile( self ):
        serialContent, keypassContent = self.getSerialAndKeypassContent()
        # The 8 digits in serial are the source that Openssl use to generate certificate serial number.
        if (not serialContent.isdigit()) or len(serialContent) != 8:
            self.popupMsgBox('Serial must be 8 digits!')
            return False
        if len(keypassContent) == 0:
            self.popupMsgBox('You forget to set key_pass!')
            return False
        with open(self.serialFilename, 'wb') as fileObj:
            fileObj.write(serialContent)
            fileObj.close()
        with open(self.keypassFilename, 'wb') as fileObj:
            # The 2 lines string need to be the same in key_pass.txt, which is the pass phase that used for protecting private key during code signing.
            fileObj.write(keypassContent + '\n' + keypassContent)
            fileObj.close()
        self.printLog('serial is generated: ' + self.serialFilename)
        self.printLog('key_pass.txt is generated: ' + self.keypassFilename)
        self._copySerialAndKeypassfileToCstFolder()
        return True

    def genCertificate( self ):
        certSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Cert)
        batArg = ''
        batArg += ' ' + certSettingsDict['useExistingCaKey']
        batArg += ' ' + str(certSettingsDict['pkiTreeKeyLen'])
        batArg += ' ' + str(certSettingsDict['pkiTreeDuration'])
        batArg += ' ' + str(certSettingsDict['SRKs'])
        batArg += ' ' + certSettingsDict['caFlagSet']
        # We have to change system dir to the path of hab4_pki_tree.bat, or hab4_pki_tree.bat will not be ran successfully
        os.chdir(self.hab4PkiTreePath)
        os.system(self.hab4PkiTreeName + batArg)
        self.printLog('Certificates are generated into these folders: ' + self.cstKeysFolder + ' , ' + self.cstCrtsFolder)

    def _getImageInfo( self ):
        startAddress = None
        entryPointAddress = None
        if os.path.isfile(self.srcAppFilename):
            appPath, appFilename = os.path.split(self.srcAppFilename)
            appName, appType = os.path.splitext(appFilename)
            if appType == '.elf' or appType == '.out':
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
                        startAddress = None
                if startAddress == None:
                    self.printLog('Cannot get vectorAddr symbol from image file: ' + self.srcAppFilename)
                #entryPointAddress = elfObj.e_entry
                for symbol in gendef.kToolchainSymbolList_EntryAddr:
                    try:
                        entryPointAddress = elfObj.getSymbol(symbol).st_value
                        break
                    except:
                        entryPointAddress = None
                if entryPointAddress == None:
                    self.printLog('Cannot get entryAddr symbol from image file: ' + self.srcAppFilename)
            elif appType == '.s19' or appType == '.srec':
                srecObj = bincopy.BinFile(str(self.srcAppFilename))
                startAddress = srecObj.minimum_address
                #entryPointAddress = srecObj.execution_start_address
                entryPointAddress = self.getVal32FromByteArray(srecObj.as_binary(startAddress + 0x4, startAddress  + 0x8))
            else:
                self.printLog('Cannot recognise the format of image file: ' + self.srcAppFilename)
        else:
            self.printLog('Cannnot find image file: ' + self.srcAppFilename)
        return startAddress, entryPointAddress

    def _updateBdfileContent( self, vectorAddress, entryPointAddress):
        startAddress = 0x0
        if self.bootDevice == uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == uidef.kBootDevice_SemcNor:
            ivtOffset = gendef.kIvtOffset_NOR
            initialLoadSize = gendef.kInitialLoadSize_NOR
        elif self.bootDevice == uidef.kBootDevice_FlexspiNand or \
             self.bootDevice == uidef.kBootDevice_SemcNand or \
             self.bootDevice == uidef.kBootDevice_UsdhcSdEmmc or \
             self.bootDevice == kBootDevice_LpspiNor:
            ivtOffset = gendef.kIvtOffset_NAND_SD_EEPROM
            initialLoadSize = gendef.kInitialLoadSize_NAND_SD_EEPROM
        else:
            pass
        if vectorAddress < initialLoadSize:
            self.printLog('Invalid vector address found in image file: ' + self.srcAppFilename)
            return False
        else:
            startAddress = vectorAddress - initialLoadSize
        if self.secureBootType == uidef.kSecureBootType_Development:
            bdContent = ""
            bdContent += "options {\n"
            bdContent += "    flags = 0x00;\n"
            bdContent += "    startAddress = " + str(hex(startAddress)) + ";\n"
            bdContent += "    ivtOffset = " + str(hex(ivtOffset)) + ";\n"
            bdContent += "    initialLoadSize = " + str(hex(initialLoadSize)) + ";\n"
            bdContent += "    entryPointAddress = " + str(hex(entryPointAddress)) + ";\n"
            bdContent += "}\n"
            bdContent += "sources {\n"
            bdContent += "    elfFile = extern(0);\n"
            bdContent += "}\n"
            bdContent += "section (0) {\n"
            bdContent += "}\n"
            with open(self.bdFilename, 'wb') as fileObj:
                fileObj.write(bdContent)
                fileObj.close()
            self.m_textCtrl_bdPath.Clear()
            self.m_textCtrl_bdPath.write(self.bdFilename)
            return True

    def createMatchedBdfile( self ):
        self.srcAppFilename = self.m_filePicker_appPath.GetPath()
        imageStartAddr, imageEntryAddr = self._getImageInfo()
        if imageStartAddr == None or imageEntryAddr == None:
            return False
        return self._updateBdfileContent(imageStartAddr, imageEntryAddr)

    def _updateBatfileContent( self ):
        batContent = self.elftosbPath
        batContent += " -f imx -V -c " + self.bdFilename + ' -o ' + self.destAppFilename + ' ' + self.srcAppFilename
        with open(self.batFilename, 'wb') as fileObj:
            fileObj.write(batContent)
            fileObj.close()

    def genBootableImage( self ):
        self._updateBatfileContent()
        os.system(self.batFilename)
        self.printLog('Bootable image is generated: ' + self.destAppFilename)

