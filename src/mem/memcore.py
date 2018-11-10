#! /usr/bin/env python
import wx
import sys
import os
import boot
sys.path.append(os.path.abspath(".."))
from fuse import fusecore
from run import rundef
from ui import uidef
from ui import uivar

class secBootMem(fusecore.secBootFuse):

    def __init__(self, parent):
        fusecore.secBootFuse.__init__(self, parent)

    def readProgrammedMemoryAndShow( self ):
        memLen = 0
        imageLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == uidef.kBootDevice_SemcNand:
            semcNandOpt, semcNandFcbOpt, imageInfo = uivar.getBootDeviceConfiguration(self.bootDevice)
            memLen += (imageInfo[self.semcNandImageCopies - 1] >> 16) * self.semcNandBlockSize
        elif self.bootDevice == uidef.kBootDevice_FlexspiNor:
            pass
        else:
            pass
        if self.habDekDataOffset != None and (self.habDekDataOffset + rundef.kKeyBlobMaxSize > imageLen):
            memLen += self.habDekDataOffset + rundef.kKeyBlobMaxSize
        else:
            memLen += imageLen

        memFilename = 'bootDeviceMem.dat'
        memFilepath = os.path.join(self.blhostVectorsDir, memFilename)
        status, results, cmdStr = self.blhost.readMemory(self.bootDeviceMemBase, memLen, memFilename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False

        self.clearMem()
        memLen = os.path.getsize(memFilepath)
        memLeft = memLen
        addr = self.bootDeviceMemBase
        with open(memFilepath, 'rb') as fileObj:
            while memLeft > 0:
                memContent = ''
                contentToShow = '0x' + self.getFormattedFuseValue(addr) + '    '
                if memLeft > 16:
                    memContent = fileObj.read(16)
                else:
                    memContent = fileObj.read(memLeft)
                memLeft -= len(memContent)
                addr += len(memContent)
                for i in range(16):
                    if i < len(memContent):
                        halfbyteStr = str(hex((ord(memContent[i]) & 0xF0)>> 4))
                        contentToShow += halfbyteStr[2]
                        halfbyteStr = str(hex((ord(memContent[i]) & 0x0F)>> 0))
                        contentToShow += halfbyteStr[2] + ' '
                    else:
                        contentToShow += '-- '
                #contentToShow += '        ' + memContent
                self.printMem(contentToShow)
            fileObj.close()

        #try:
        #    os.remove(memFilepath)
        #except:
        #    pass
        #return True


