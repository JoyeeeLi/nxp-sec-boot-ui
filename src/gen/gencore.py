#! /usr/bin/env python
import wx
import sys
import os
import shutil
import subprocess
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

        self.serialFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'hab_cert', 'serial')
        self.keypassFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'hab_cert', 'key_pass.txt')
        self.cstBinFolder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'cst', uidef.kCstVersion_Invalid, 'mingw32', 'bin')
        self.cstKeysFolder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'cst', uidef.kCstVersion_Invalid, 'keys')
        self.cstCrtsFolder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'cst', uidef.kCstVersion_Invalid, 'crts')
        self.hab4PkiTreePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'cst', uidef.kCstVersion_Invalid, 'keys')
        self.hab4PkiTreeName = 'hab4_pki_tree.bat'
        self.srktoolPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'cst', uidef.kCstVersion_Invalid, 'mingw32', 'bin', 'srktool.exe')
        self.srkFolder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'hab_cert')
        self.srkTableFilename = None
        self.srkFuseFilename = None
        self.crtSrkCaPemFileList = [None] * 4
        self.crtCsfUsrPemFileList = [None] * 4
        self.crtImgUsrPemFileList = [None] * 4
        self.srkBatFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'hab_cert', 'imx_srk_gen.bat')
        self.cstBinToElftosbPath = '../../cst/' + uidef.kCstVersion_Invalid + '/mingw32/bin'
        self.cstCrtsToElftosbPath = '../../cst/' + uidef.kCstVersion_Invalid + '/crts/'
        self.genCertToElftosbPath = '../../../gen/hab_cert/'
        self.genCryptoToElftosbPath = '../../../gen/hab_crypto/'
        self.lastCstVersion = uidef.kCstVersion_Invalid
        self.habDekFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'hab_crypto', 'hab_dek.bin')
        self.habDekDataOffset = None
        self.srcAppFilename = None
        self.destAppFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bootable_image', 'ivt_application.bin')
        self.destAppNoPaddingFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bootable_image', 'ivt_application_nopadding.bin')
        self.bdFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bd_file', 'imx_image_gen.bd')
        self.elftosbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'elftosb', 'win', 'elftosb.exe')
        self.bdBatFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bd_file', 'imx_image_gen.bat')
        self.updateAllCstPathToCorrectVersion()
        self.imageEncPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools', 'image_enc', 'win', 'image_enc.exe')
        self.beeDek0Filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bee_crypto', 'bee_dek0.bin')
        self.beeDek1Filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bee_crypto', 'bee_dek1.bin')
        self.encBatFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bee_crypto', 'imx_image_enc.bat')
        self.otpmkDekFilename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'gen', 'bee_crypto', 'otpmk_dek.bin')

    def _copyCstBinToElftosbFolder( self ):
        shutil.copy(self.cstBinFolder + '\\cst.exe', os.path.split(self.elftosbPath)[0])

    def updateAllCstPathToCorrectVersion( self ):
        certSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Cert)
        if self.lastCstVersion != certSettingsDict['cstVersion']:
            self.cstBinFolder = self.cstBinFolder.replace(self.lastCstVersion, certSettingsDict['cstVersion'])
            self.cstKeysFolder = self.cstKeysFolder.replace(self.lastCstVersion, certSettingsDict['cstVersion'])
            self.cstCrtsFolder = self.cstCrtsFolder.replace(self.lastCstVersion, certSettingsDict['cstVersion'])
            self.hab4PkiTreePath = self.hab4PkiTreePath.replace(self.lastCstVersion, certSettingsDict['cstVersion'])
            self.srktoolPath = self.srktoolPath.replace(self.lastCstVersion, certSettingsDict['cstVersion'])
            self.cstBinToElftosbPath = self.cstBinToElftosbPath.replace(self.lastCstVersion, certSettingsDict['cstVersion'])
            self.cstCrtsToElftosbPath = self.cstCrtsToElftosbPath.replace(self.lastCstVersion, certSettingsDict['cstVersion'])
            self.lastCstVersion = certSettingsDict['cstVersion']
            self._copyCstBinToElftosbFolder()

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
        if certSettingsDict['cstVersion'] == uidef.kCstVersion_v3_0_1:
            batArg += ' ' + certSettingsDict['caFlagSet']
        elif certSettingsDict['cstVersion'] == uidef.kCstVersion_v2_3_3:
            pass
        else:
            pass
        # We have to change system dir to the path of hab4_pki_tree.bat, or hab4_pki_tree.bat will not be ran successfully
        os.chdir(self.hab4PkiTreePath)
        os.system(self.hab4PkiTreeName + batArg)
        self.printLog('Certificates are generated into these folders: ' + self.cstKeysFolder + ' , ' + self.cstCrtsFolder)

    def _setSrkFilenames( self ):
        certSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Cert)
        srkTableName = 'SRK'
        srkFuseName = 'SRK'
        for i in range(certSettingsDict['SRKs']):
            srkTableName += '_' + str(i + 1)
            srkFuseName += '_' + str(i + 1)
        srkTableName += '_table.bin'
        srkFuseName += '_fuse.bin'
        self.srkTableFilename = os.path.join(self.srkFolder, srkTableName)
        self.srkFuseFilename = os.path.join(self.srkFolder, srkFuseName)

    def _getCrtSrkCaPemFilenames( self ):
        certSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Cert)
        for i in range(certSettingsDict['SRKs']):
            self.crtSrkCaPemFileList[i] = self.cstCrtsFolder + '\\'
            self.crtSrkCaPemFileList[i] += 'SRK' + str(i + 1) + '_sha256'
            self.crtSrkCaPemFileList[i] += '_' + str(certSettingsDict['pkiTreeKeyLen'])
            self.crtSrkCaPemFileList[i] += '_65537_v3_ca_crt.pem'

    def _getCrtCsfImgUsrPemFilenames( self ):
        certSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Cert)
        for i in range(certSettingsDict['SRKs']):
            self.crtCsfUsrPemFileList[i] = self.cstCrtsFolder + '\\'
            self.crtCsfUsrPemFileList[i] += 'CSF' + str(i + 1) + '_1_sha256'
            self.crtCsfUsrPemFileList[i] += '_' + str(certSettingsDict['pkiTreeKeyLen'])
            self.crtCsfUsrPemFileList[i] += '_65537_v3_usr_crt.pem'
            self.crtImgUsrPemFileList[i] = self.cstCrtsFolder + '\\'
            self.crtImgUsrPemFileList[i] += 'IMG' + str(i + 1) + '_1_sha256'
            self.crtImgUsrPemFileList[i] += '_' + str(certSettingsDict['pkiTreeKeyLen'])
            self.crtImgUsrPemFileList[i] += '_65537_v3_usr_crt.pem'

    def _updateSrkBatfileContent( self ):
        self._setSrkFilenames()
        self._getCrtSrkCaPemFilenames()
        self._getCrtCsfImgUsrPemFilenames()
        certSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Cert)
        batContent = self.srktoolPath
        batContent += " -h 4"
        batContent += " -t " + self.srkTableFilename
        batContent += " -e " + self.srkFuseFilename
        batContent += " -d sha256"
        batContent += " -c "
        for i in range(certSettingsDict['SRKs']):
            if i != 0:
                batContent += ','
            batContent += self.crtSrkCaPemFileList[i]
        batContent += " -f 1"
        with open(self.srkBatFilename, 'wb') as fileObj:
            fileObj.write(batContent)
            fileObj.close()

    def genSuperRootKeys( self ):
        self._updateSrkBatfileContent()
        os.system(self.srkBatFilename)
        self.printLog('Public SuperRootKey files are generated successfully')

    def showSuperRootKeys( self ):
        self.clearSrkData()
        keyWords = gendef.kSecKeyLengthInBits_SRK / 32
        for i in range(keyWords):
            val32 = self.getVal32FromBinFile(self.srkFuseFilename, (i * 4))
            self.printSrkData(str(hex(val32)))

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
        return startAddress, entryPointAddress

    def _updateBdfileContent( self, vectorAddress, entryPointAddress):
        bdContent = ""
        ############################################################################
        bdContent += "options {\n"
        if self.secureBootType == uidef.kSecureBootType_Development:
            flags = gendef.kBootImageTypeFlag_Unsigned
        elif self.secureBootType == uidef.kSecureBootType_HabAuth:
            flags = gendef.kBootImageTypeFlag_Signed
        elif self.secureBootType == uidef.kSecureBootType_HabCrypto:
            flags = gendef.kBootImageTypeFlag_Encrypted
        elif self.secureBootType == uidef.kSecureBootType_BeeCrypto:
            if self.isCertEnabledForBee:
                flags = gendef.kBootImageTypeFlag_Signed
            else:
                flags = gendef.kBootImageTypeFlag_Unsigned
        else:
            pass
        bdContent += "    flags = " + flags + ";\n"
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
        bdContent += "    startAddress = " + str(hex(startAddress)) + ";\n"
        bdContent += "    ivtOffset = " + str(hex(ivtOffset)) + ";\n"
        bdContent += "    initialLoadSize = " + str(hex(initialLoadSize)) + ";\n"
        if self.secureBootType == uidef.kSecureBootType_HabAuth:
            #bdContent += "    cstFolderPath = \"" + self.cstBinFolder + "\";\n"
            #bdContent += "    cstFolderPath = \"" + self.cstBinToElftosbPath + "\";\n"
            pass
        else:
            pass
        bdContent += "    entryPointAddress = " + str(hex(entryPointAddress)) + ";\n"
        bdContent += "}\n"
        ############################################################################
        bdContent += "\nsources {\n"
        bdContent += "    elfFile = extern(0);\n"
        bdContent += "}\n"
        ############################################################################
        if self.secureBootType == uidef.kSecureBootType_Development or \
           (self.secureBootType == uidef.kSecureBootType_BeeCrypto and (not self.isCertEnabledForBee)):
            bdContent += "\nsection (0) {\n"
            bdContent += "}\n"
        elif self.secureBootType == uidef.kSecureBootType_HabAuth or \
             self.secureBootType == uidef.kSecureBootType_HabCrypto or \
             (self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.isCertEnabledForBee):
            ########################################################################
            bdContent += "\nconstants {\n"
            bdContent += "    SEC_CSF_HEADER              = 20;\n"
            bdContent += "    SEC_CSF_INSTALL_SRK         = 21;\n"
            bdContent += "    SEC_CSF_INSTALL_CSFK        = 22;\n"
            bdContent += "    SEC_CSF_INSTALL_NOCAK       = 23;\n"
            bdContent += "    SEC_CSF_AUTHENTICATE_CSF    = 24;\n"
            bdContent += "    SEC_CSF_INSTALL_KEY         = 25;\n"
            bdContent += "    SEC_CSF_AUTHENTICATE_DATA   = 26;\n"
            bdContent += "    SEC_CSF_INSTALL_SECRET_KEY  = 27;\n"
            bdContent += "    SEC_CSF_DECRYPT_DATA        = 28;\n"
            bdContent += "    SEC_NOP                     = 29;\n"
            bdContent += "    SEC_SET_MID                 = 30;\n"
            bdContent += "    SEC_SET_ENGINE              = 31;\n"
            bdContent += "    SEC_INIT                    = 32;\n"
            bdContent += "    SEC_UNLOCK                  = 33;\n"
            bdContent += "}\n"
            ########################################################################
            bdContent += "\nsection (SEC_CSF_HEADER;\n"
            if self.secureBootType == uidef.kSecureBootType_HabAuth or \
               (self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.isCertEnabledForBee):
                headerVersion = gendef.kBootImageCsfHeaderVersion_Signed
            elif self.secureBootType == uidef.kSecureBootType_HabCrypto:
                headerVersion = gendef.kBootImageCsfHeaderVersion_Encrypted
            else:
                pass
            bdContent += "    Header_Version=\"" + headerVersion + "\",\n"
            bdContent += "    Header_HashAlgorithm=\"sha256\",\n"
            bdContent += "    Header_Engine=\"DCP\",\n"
            bdContent += "    Header_EngineConfiguration=0,\n"
            bdContent += "    Header_CertificateFormat=\"x509\",\n"
            bdContent += "    Header_SignatureFormat=\"CMS\"\n"
            bdContent += "    )\n"
            bdContent += "{\n"
            bdContent += "}\n"
            ########################################################################
            bdContent += "\nsection (SEC_CSF_INSTALL_SRK;\n"
            #bdContent += "    InstallSRK_Table=\"" + self.srkTableFilename + "\",\n"
            bdContent += "    InstallSRK_Table=\"" + self.genCertToElftosbPath + os.path.split(self.srkTableFilename)[1] + "\",\n"
            bdContent += "    InstallSRK_SourceIndex=0\n"
            bdContent += "    )\n"
            bdContent += "{\n"
            bdContent += "}\n"
            bdContent += "\nsection (SEC_CSF_INSTALL_CSFK;\n"
            #bdContent += "    InstallCSFK_File=\"" + self.crtCsfUsrPemFileList[0] + "\",\n"
            bdContent += "    InstallCSFK_File=\"" + self.cstCrtsToElftosbPath + os.path.split(self.crtCsfUsrPemFileList[0])[1] + "\",\n"
            bdContent += "    InstallCSFK_CertificateFormat=\"x509\"\n"
            bdContent += "    )\n"
            bdContent += "{\n"
            bdContent += "}\n"
            bdContent += "\nsection (SEC_CSF_AUTHENTICATE_CSF)\n"
            bdContent += "{\n"
            bdContent += "}\n"
            bdContent += "\nsection (SEC_CSF_INSTALL_KEY;\n"
            #bdContent += "    InstallKey_File=\"" + self.crtImgUsrPemFileList[0] + "\",\n"
            bdContent += "    InstallKey_File=\"" + self.cstCrtsToElftosbPath + os.path.split(self.crtImgUsrPemFileList[0])[1] + "\",\n"
            bdContent += "    InstallKey_VerificationIndex=0,\n"
            bdContent += "    InstallKey_TargetIndex=2)\n"
            bdContent += "{\n"
            bdContent += "}\n"
            bdContent += "\nsection (SEC_CSF_AUTHENTICATE_DATA;\n"
            bdContent += "    AuthenticateData_VerificationIndex=2,\n"
            bdContent += "    AuthenticateData_Engine=\"DCP\",\n"
            bdContent += "    AuthenticateData_EngineConfiguration=0)\n"
            bdContent += "{\n"
            bdContent += "}\n"
            ########################################################################
            if self.secureBootType == uidef.kSecureBootType_HabAuth or \
               (self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.isCertEnabledForBee):
                bdContent += "\nsection (SEC_SET_ENGINE;\n"
                bdContent += "    SetEngine_HashAlgorithm = \"sha256\",\n"
                bdContent += "    SetEngine_Engine = \"DCP\",\n"
                bdContent += "    SetEngine_EngineConfiguration = \"0\")\n"
                bdContent += "{\n"
                bdContent += "}\n"
                bdContent += "\nsection (SEC_UNLOCK;\n"
                bdContent += "    Unlock_Engine = \"SNVS\",\n"
                bdContent += "    Unlock_features = \"ZMK WRITE\"\n"
                bdContent += "    )\n"
                bdContent += "{\n"
                bdContent += "}\n"
            elif self.secureBootType == uidef.kSecureBootType_HabCrypto:
                bdContent += "section (SEC_CSF_INSTALL_SECRET_KEY;\n"
                bdContent += "    SecretKey_Name=\"" + self.genCryptoToElftosbPath + os.path.split(self.habDekFilename)[1] + "\",\n"
                bdContent += "    SecretKey_Length=128,\n"
                bdContent += "    SecretKey_VerifyIndex=0,\n"
                bdContent += "    SecretKey_TargetIndex=0)\n"
                bdContent += "{\n"
                bdContent += "}\n"
                bdContent += "section (SEC_CSF_DECRYPT_DATA;\n"
                bdContent += "    Decrypt_Engine=\"DCP\",\n"
                bdContent += "    Decrypt_EngineConfiguration=\"0\",\n"
                bdContent += "    Decrypt_VerifyIndex=0,\n"
                bdContent += "    Decrypt_MacBytes=16)\n"
                bdContent += "{\n"
                bdContent += "}\n"
            else:
                pass
            ########################################################################
        else:
            pass

        with open(self.bdFilename, 'wb') as fileObj:
            fileObj.write(bdContent)
            fileObj.close()
        self.m_textCtrl_bdPath.Clear()
        self.m_textCtrl_bdPath.write(self.bdFilename)

        return True

    def _isCertificateGenerated( self ):
        if self.secureBootType == uidef.kSecureBootType_HabAuth or \
           self.secureBootType == uidef.kSecureBootType_HabCrypto or \
           (self.secureBootType == uidef.kSecureBootType_BeeCrypto and self.isCertEnabledForBee):
            if ((self.srkTableFilename != None) and \
                (self.srkFuseFilename != None) and \
                (self.crtSrkCaPemFileList[0] != None) and \
                (self.crtCsfUsrPemFileList[0] != None) and \
                (self.crtImgUsrPemFileList[0] != None)):
                return  (os.path.isfile(self.srkTableFilename) and \
                         os.path.isfile(self.srkFuseFilename) and \
                         os.path.isfile(self.crtSrkCaPemFileList[0]) and \
                         os.path.isfile(self.crtCsfUsrPemFileList[0]) and \
                         os.path.isfile(self.crtImgUsrPemFileList[0]))
            else:
                return False
        elif self.secureBootType == uidef.kSecureBootType_Development or \
             (self.secureBootType == uidef.kSecureBootType_BeeCrypto and (not self.isCertEnabledForBee)):
            return True
        else:
            pass

    def createMatchedBdfile( self ):
        self.srcAppFilename = self.m_filePicker_appPath.GetPath()
        imageStartAddr, imageEntryAddr = self._getImageInfo()
        if imageStartAddr == None or imageEntryAddr == None:
            self.popupMsgBox('You should first specify a source image file (.elf/.srec)!')
            return False
        if not self._isCertificateGenerated():
            self.popupMsgBox('You should first generate certificates!')
            return False
        return self._updateBdfileContent(imageStartAddr, imageEntryAddr)

    def _adjustDestAppFilenameForBd( self ):
        srcAppName = os.path.splitext(os.path.split(self.srcAppFilename)[1])[0]
        destAppPath, destAppFile = os.path.split(self.destAppFilename)
        destAppName, destAppType = os.path.splitext(destAppFile)
        destAppName ='ivt_' + srcAppName
        if self.secureBootType == uidef.kSecureBootType_Development:
            destAppName += '_unsigned'
        elif self.secureBootType == uidef.kSecureBootType_HabAuth:
            destAppName += '_signed'
        elif self.secureBootType == uidef.kSecureBootType_HabCrypto:
            destAppName += '_signed_hab_encrypted'
        elif self.secureBootType == uidef.kSecureBootType_BeeCrypto:
            if self.isCertEnabledForBee:
                destAppName += '_signed'
            else:
                destAppName += '_unsigned'
        else:
            pass
        self.destAppFilename = os.path.join(destAppPath, destAppName + destAppType)
        self.destAppNoPaddingFilename = os.path.join(destAppPath, destAppName + '_nopadding' + destAppType)

    def _updateBdBatfileContent( self ):
        self._adjustDestAppFilenameForBd()
        batContent = self.elftosbPath
        batContent += " -f imx -V -c " + self.bdFilename + ' -o ' + self.destAppFilename + ' ' + self.srcAppFilename
        with open(self.bdBatFilename, 'wb') as fileObj:
            fileObj.write(batContent)
            fileObj.close()

    def _parseBootableImageGenerationResult( self, output ):
        # elftosb ouput template:
        # (Signed)     CSF Processed successfully and signed data available in csf.bin
        # (All)                Section: xxx
        # (All)                ...
        # (All)        iMX bootable image generated successfully
        # (Encrypted)  Key Blob Address is 0xe000.
        # (Encrypted)  Key Blob data should be placed at Offset :0x6000 in the image
        info = 'iMX bootable image generated successfully'
        if output.find(info) != -1:
            self.printLog('Bootable image is generated: ' + self.destAppFilename)
            info1 = 'Key Blob data should be placed at Offset :0x'
            info2 = ' in the image'
            loc1 = output.find(info1)
            loc2 = output.find(info2)
            if loc1 != -1 and loc1 < loc2:
                loc1 += len(info1)
                self.habDekDataOffset = int(output[loc1:loc2], 16)
            else:
                self.habDekDataOffset = None
        else:
            self.habDekDataOffset = None
            self.popupMsgBox('Bootable image is not generated successfully!')

    def genBootableImage( self ):
        self._updateBdBatfileContent()
        # We have to change system dir to the path of elftosb.exe, or elftosb.exe may not be ran successfully
        os.chdir(os.path.split(self.elftosbPath)[0])
        process = subprocess.Popen(self.bdBatFilename, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        commandOutput = process.communicate()[0]
        print commandOutput
        self._parseBootableImageGenerationResult(commandOutput)

    def showHabDekIfApplicable( self ):
        if self.secureBootType == uidef.kSecureBootType_HabCrypto and self.habDekDataOffset != None:
            if os.path.isfile(self.habDekFilename):
                self.clearHabDekData()
                keyWords = gendef.kSecKeyLengthInBits_DEK / 32
                for i in range(keyWords):
                    val32 = self.getVal32FromBinFile(self.habDekFilename, (i * 4))
                    self.printHabDekData(str(hex(val32)))

    def _changeDestAppNoPaddingFilenameForBee( self ):
        destAppNoPaddingPath, destAppNoPaddingFile = os.path.split(self.destAppNoPaddingFilename)
        destAppNoPaddingName, destAppNoPaddingType = os.path.splitext(destAppNoPaddingFile)
        destAppNoPaddingName += '_bee_encrypted'
        self.destAppNoPaddingFilename = os.path.join(destAppNoPaddingPath, destAppNoPaddingName + destAppNoPaddingType)

    def _genBeeDekFile( self, regionIndex, keyContent ):
        if regionIndex == 0:
            #print 'beeDek0Filename content: ' + keyContent
            self.fillDek128ContentIntoBinFile(self.beeDek0Filename, keyContent)
        elif regionIndex == 1:
            #print 'beeDek1Filename content: ' + keyContent
            self.fillDek128ContentIntoBinFile(self.beeDek1Filename, keyContent)
        else:
            pass

    def _showBeeDekForGp4( self, dekFilename ):
        if os.path.isfile(dekFilename):
            self.clearGp4DekData()
            keyWords = gendef.kSecKeyLengthInBits_DEK / 32
            for i in range(keyWords):
                val32 = self.getVal32FromBinFile(dekFilename, (i * 4))
                self.printGp4DekData(str(hex(val32)))

    def _showBeeDekForSwGp2( self, dekFilename ):
        if os.path.isfile(dekFilename):
            self.clearSwGp2DekData()
            keyWords = gendef.kSecKeyLengthInBits_DEK / 32
            for i in range(keyWords):
                val32 = self.getVal32FromBinFile(dekFilename, (i * 4))
                self.printSwGp2DekData(str(hex(val32)))

    def _genBeeDekFilesAndShow( self, userKeyCtrlDict, userKeyCmdDict ):
        if userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region0 or userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            self._genBeeDekFile(0, userKeyCmdDict['region0_key'])
            if userKeyCtrlDict['region0_key_src'] == uidef.kUserKeySource_SW_GP2:
                self._showBeeDekForSwGp2(self.beeDek0Filename)
            elif userKeyCtrlDict['region0_key_src'] == uidef.kUserKeySource_GP4:
                self._showBeeDekForGp4(self.beeDek0Filename)
            else:
                pass
        if userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region1 or userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            self._genBeeDekFile(1, userKeyCmdDict['region1_key'])
            if userKeyCtrlDict['region1_key_src'] == uidef.kUserKeySource_SW_GP2:
                self._showBeeDekForSwGp2(self.beeDek1Filename)
            elif userKeyCtrlDict['region1_key_src'] == uidef.kUserKeySource_GP4:
                self._showBeeDekForGp4(self.beeDek1Filename)
            else:
                pass

    def _updateEncBatfileContent( self, userKeyCtrlDict, userKeyCmdDict, originalAppFilename ):
        batContent = self.imageEncPath
        batContent += " ifile=" + originalAppFilename
        batContent += " ofile=" + self.destAppNoPaddingFilename
        batContent += " base_addr=" + userKeyCmdDict['base_addr']
        if userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region0 or userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            if userKeyCtrlDict['region0_key_src'] == uidef.kUserKeySource_OTPMK:
                userKeyCmdDict['region0_key'] = self.getDek128ContentFromBinFile(self.otpmkDekFilename)
            batContent += " region0_key=" + userKeyCmdDict['region0_key']
            batContent += " region0_arg=" + userKeyCmdDict['region0_arg']
            batContent += " region0_lock=" + userKeyCmdDict['region0_lock']
        if userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_Region1 or userKeyCtrlDict['region_sel'] == uidef.kUserRegionSel_BothRegions:
            if userKeyCtrlDict['region1_key_src'] == uidef.kUserKeySource_OTPMK:
                userKeyCmdDict['region1_key'] = self.getDek128ContentFromBinFile(self.otpmkDekFilename)
            batContent += " region1_key=" + userKeyCmdDict['region1_key']
            batContent += " region1_arg=" + userKeyCmdDict['region1_arg']
            batContent += " region1_lock=" + userKeyCmdDict['region1_lock']
        batContent += " use_zero_key=" + userKeyCmdDict['use_zero_key']
        batContent += " is_boot_image=" + userKeyCmdDict['is_boot_image']
        with open(self.encBatFilename, 'wb') as fileObj:
            fileObj.write(batContent)
            fileObj.close()

    def _encrypteBootableImage( self ):
        os.chdir(os.path.split(self.imageEncPath)[0])
        process = subprocess.Popen(self.encBatFilename, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        commandOutput = process.communicate()[0]
        print commandOutput

    def encrypteImageUsingFlexibleUserKeys( self ):
        userKeyCtrlDict, userKeyCmdDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_UserKeys)
        if userKeyCmdDict['is_boot_image'] == '1':
            originalAppFilename = self.destAppNoPaddingFilename
            self._changeDestAppNoPaddingFilenameForBee()
            self._updateEncBatfileContent(userKeyCtrlDict, userKeyCmdDict, originalAppFilename)
            self._encrypteBootableImage()
            self._genBeeDekFilesAndShow(userKeyCtrlDict, userKeyCmdDict)
        elif userKeyCmdDict['is_boot_image'] == '0':
            pass

            #userKeyCtrlDict['region_sel'] = uidef.kUserRegionSel_BothRegions
            #userKeyCtrlDict['region0_key_src'] = uidef.kUserKeySource_OTPMK
            #userKeyCtrlDict['region1_key_src'] = uidef.kUserKeySource_OTPMK
            #userKeyCmdDict['region0_key'] = '0123456789abcdef0123456789ABCDEF'
            #userKeyCmdDict['region1_key'] = '0123456789abcdef0123456789ABCDEF'

