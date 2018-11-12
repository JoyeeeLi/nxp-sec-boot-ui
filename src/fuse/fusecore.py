#! /usr/bin/env python
import wx
import sys
import os
import fusedef
sys.path.append(os.path.abspath(".."))
from run import runcore
from ui import uidef

class secBootFuse(runcore.secBootRun):

    def __init__(self, parent):
        runcore.secBootRun.__init__(self, parent)

        self.scannedFuseList = [None] * fusedef.kMaxEfuseWords
        self.toBeBurnnedFuseList = [None] * fusedef.kMaxEfuseWords

    def _parseReadFuseValue( self, fuseValue ):
        if fuseValue != None:
            result = str(hex(fuseValue))
            if result[len(result) - 1] != 'L':
                return result
            else:
                return result[0:len(result) - 1]
        else:
            return '--------'

    def _setScannedFuse( self ):
        self.m_textCtrl_fuse400.Clear()
        self.m_textCtrl_fuse400.write(self._parseReadFuseValue(self.scannedFuseList[0]))
        self.m_textCtrl_fuse410.Clear()
        self.m_textCtrl_fuse410.write(self._parseReadFuseValue(self.scannedFuseList[1]))
        self.m_textCtrl_fuse420.Clear()
        self.m_textCtrl_fuse420.write(self._parseReadFuseValue(self.scannedFuseList[2]))
        self.m_textCtrl_fuse430.Clear()
        self.m_textCtrl_fuse430.write(self._parseReadFuseValue(self.scannedFuseList[3]))
        self.m_textCtrl_fuse440.Clear()
        self.m_textCtrl_fuse440.write(self._parseReadFuseValue(self.scannedFuseList[4]))
        self.m_textCtrl_fuse450.Clear()
        self.m_textCtrl_fuse450.write(self._parseReadFuseValue(self.scannedFuseList[5]))
        self.m_textCtrl_fuse460.Clear()
        self.m_textCtrl_fuse460.write(self._parseReadFuseValue(self.scannedFuseList[6]))
        self.m_textCtrl_fuse470.Clear()
        self.m_textCtrl_fuse470.write(self._parseReadFuseValue(self.scannedFuseList[7]))
        self.m_textCtrl_fuse480.Clear()
        self.m_textCtrl_fuse480.write(self._parseReadFuseValue(self.scannedFuseList[8]))
        self.m_textCtrl_fuse490.Clear()
        self.m_textCtrl_fuse490.write(self._parseReadFuseValue(self.scannedFuseList[9]))
        self.m_textCtrl_fuse4a0.Clear()
        self.m_textCtrl_fuse4a0.write(self._parseReadFuseValue(self.scannedFuseList[10]))
        self.m_textCtrl_fuse4b0.Clear()
        self.m_textCtrl_fuse4b0.write(self._parseReadFuseValue(self.scannedFuseList[11]))
        self.m_textCtrl_fuse4c0.Clear()
        self.m_textCtrl_fuse4c0.write(self._parseReadFuseValue(self.scannedFuseList[12]))
        self.m_textCtrl_fuse4d0.Clear()
        self.m_textCtrl_fuse4d0.write(self._parseReadFuseValue(self.scannedFuseList[13]))
        self.m_textCtrl_fuse4e0.Clear()
        self.m_textCtrl_fuse4e0.write(self._parseReadFuseValue(self.scannedFuseList[14]))
        self.m_textCtrl_fuse4f0.Clear()
        self.m_textCtrl_fuse4f0.write(self._parseReadFuseValue(self.scannedFuseList[15]))

        self.m_textCtrl_fuse500.Clear()
        self.m_textCtrl_fuse500.write(self._parseReadFuseValue(self.scannedFuseList[16]))
        self.m_textCtrl_fuse510.Clear()
        self.m_textCtrl_fuse510.write(self._parseReadFuseValue(self.scannedFuseList[17]))
        self.m_textCtrl_fuse520.Clear()
        self.m_textCtrl_fuse520.write(self._parseReadFuseValue(self.scannedFuseList[18]))
        self.m_textCtrl_fuse530.Clear()
        self.m_textCtrl_fuse530.write(self._parseReadFuseValue(self.scannedFuseList[19]))
        self.m_textCtrl_fuse540.Clear()
        self.m_textCtrl_fuse540.write(self._parseReadFuseValue(self.scannedFuseList[20]))
        self.m_textCtrl_fuse550.Clear()
        self.m_textCtrl_fuse550.write(self._parseReadFuseValue(self.scannedFuseList[21]))
        self.m_textCtrl_fuse560.Clear()
        self.m_textCtrl_fuse560.write(self._parseReadFuseValue(self.scannedFuseList[22]))
        self.m_textCtrl_fuse570.Clear()
        self.m_textCtrl_fuse570.write(self._parseReadFuseValue(self.scannedFuseList[23]))
        self.m_textCtrl_fuse580.Clear()
        self.m_textCtrl_fuse580.write(self._parseReadFuseValue(self.scannedFuseList[24]))
        self.m_textCtrl_fuse590.Clear()
        self.m_textCtrl_fuse590.write(self._parseReadFuseValue(self.scannedFuseList[25]))
        self.m_textCtrl_fuse5a0.Clear()
        self.m_textCtrl_fuse5a0.write(self._parseReadFuseValue(self.scannedFuseList[26]))
        self.m_textCtrl_fuse5b0.Clear()
        self.m_textCtrl_fuse5b0.write(self._parseReadFuseValue(self.scannedFuseList[27]))
        self.m_textCtrl_fuse5c0.Clear()
        self.m_textCtrl_fuse5c0.write(self._parseReadFuseValue(self.scannedFuseList[28]))
        self.m_textCtrl_fuse5d0.Clear()
        self.m_textCtrl_fuse5d0.write(self._parseReadFuseValue(self.scannedFuseList[29]))
        self.m_textCtrl_fuse5e0.Clear()
        self.m_textCtrl_fuse5e0.write(self._parseReadFuseValue(self.scannedFuseList[30]))
        self.m_textCtrl_fuse5f0.Clear()
        self.m_textCtrl_fuse5f0.write(self._parseReadFuseValue(self.scannedFuseList[31]))

        self.m_textCtrl_fuse600.Clear()
        self.m_textCtrl_fuse600.write(self._parseReadFuseValue(self.scannedFuseList[32]))
        self.m_textCtrl_fuse610.Clear()
        self.m_textCtrl_fuse610.write(self._parseReadFuseValue(self.scannedFuseList[33]))
        self.m_textCtrl_fuse620.Clear()
        self.m_textCtrl_fuse620.write(self._parseReadFuseValue(self.scannedFuseList[34]))
        self.m_textCtrl_fuse630.Clear()
        self.m_textCtrl_fuse630.write(self._parseReadFuseValue(self.scannedFuseList[35]))
        self.m_textCtrl_fuse640.Clear()
        self.m_textCtrl_fuse640.write(self._parseReadFuseValue(self.scannedFuseList[36]))
        self.m_textCtrl_fuse650.Clear()
        self.m_textCtrl_fuse650.write(self._parseReadFuseValue(self.scannedFuseList[37]))
        self.m_textCtrl_fuse660.Clear()
        self.m_textCtrl_fuse660.write(self._parseReadFuseValue(self.scannedFuseList[38]))
        self.m_textCtrl_fuse670.Clear()
        self.m_textCtrl_fuse670.write(self._parseReadFuseValue(self.scannedFuseList[39]))
        self.m_textCtrl_fuse680.Clear()
        self.m_textCtrl_fuse680.write(self._parseReadFuseValue(self.scannedFuseList[40]))
        self.m_textCtrl_fuse690.Clear()
        self.m_textCtrl_fuse690.write(self._parseReadFuseValue(self.scannedFuseList[41]))
        self.m_textCtrl_fuse6a0.Clear()
        self.m_textCtrl_fuse6a0.write(self._parseReadFuseValue(self.scannedFuseList[42]))
        self.m_textCtrl_fuse6b0.Clear()
        self.m_textCtrl_fuse6b0.write(self._parseReadFuseValue(self.scannedFuseList[43]))
        self.m_textCtrl_fuse6c0.Clear()
        self.m_textCtrl_fuse6c0.write(self._parseReadFuseValue(self.scannedFuseList[44]))
        self.m_textCtrl_fuse6d0.Clear()
        self.m_textCtrl_fuse6d0.write(self._parseReadFuseValue(self.scannedFuseList[45]))
        self.m_textCtrl_fuse6e0.Clear()
        self.m_textCtrl_fuse6e0.write(self._parseReadFuseValue(self.scannedFuseList[46]))
        self.m_textCtrl_fuse6f0.Clear()
        self.m_textCtrl_fuse6f0.write(self._parseReadFuseValue(self.scannedFuseList[47]))

        self.m_textCtrl_fuse700.Clear()
        self.m_textCtrl_fuse700.write(self._parseReadFuseValue(self.scannedFuseList[48]))
        self.m_textCtrl_fuse710.Clear()
        self.m_textCtrl_fuse710.write(self._parseReadFuseValue(self.scannedFuseList[49]))
        self.m_textCtrl_fuse720.Clear()
        self.m_textCtrl_fuse720.write(self._parseReadFuseValue(self.scannedFuseList[50]))
        self.m_textCtrl_fuse730.Clear()
        self.m_textCtrl_fuse730.write(self._parseReadFuseValue(self.scannedFuseList[51]))
        self.m_textCtrl_fuse740.Clear()
        self.m_textCtrl_fuse740.write(self._parseReadFuseValue(self.scannedFuseList[52]))
        self.m_textCtrl_fuse750.Clear()
        self.m_textCtrl_fuse750.write(self._parseReadFuseValue(self.scannedFuseList[53]))
        self.m_textCtrl_fuse760.Clear()
        self.m_textCtrl_fuse760.write(self._parseReadFuseValue(self.scannedFuseList[54]))
        self.m_textCtrl_fuse770.Clear()
        self.m_textCtrl_fuse770.write(self._parseReadFuseValue(self.scannedFuseList[55]))
        self.m_textCtrl_fuse780.Clear()
        self.m_textCtrl_fuse780.write(self._parseReadFuseValue(self.scannedFuseList[56]))
        self.m_textCtrl_fuse790.Clear()
        self.m_textCtrl_fuse790.write(self._parseReadFuseValue(self.scannedFuseList[57]))
        self.m_textCtrl_fuse7a0.Clear()
        self.m_textCtrl_fuse7a0.write(self._parseReadFuseValue(self.scannedFuseList[58]))
        self.m_textCtrl_fuse7b0.Clear()
        self.m_textCtrl_fuse7b0.write(self._parseReadFuseValue(self.scannedFuseList[59]))
        self.m_textCtrl_fuse7c0.Clear()
        self.m_textCtrl_fuse7c0.write(self._parseReadFuseValue(self.scannedFuseList[60]))
        self.m_textCtrl_fuse7d0.Clear()
        self.m_textCtrl_fuse7d0.write(self._parseReadFuseValue(self.scannedFuseList[61]))
        self.m_textCtrl_fuse7e0.Clear()
        self.m_textCtrl_fuse7e0.write(self._parseReadFuseValue(self.scannedFuseList[62]))
        self.m_textCtrl_fuse7f0.Clear()
        self.m_textCtrl_fuse7f0.write(self._parseReadFuseValue(self.scannedFuseList[63]))

        self.m_textCtrl_fuse800.Clear()
        self.m_textCtrl_fuse800.write(self._parseReadFuseValue(self.scannedFuseList[64]))
        self.m_textCtrl_fuse810.Clear()
        self.m_textCtrl_fuse810.write(self._parseReadFuseValue(self.scannedFuseList[65]))
        self.m_textCtrl_fuse820.Clear()
        self.m_textCtrl_fuse820.write(self._parseReadFuseValue(self.scannedFuseList[66]))
        self.m_textCtrl_fuse830.Clear()
        self.m_textCtrl_fuse830.write(self._parseReadFuseValue(self.scannedFuseList[67]))
        self.m_textCtrl_fuse840.Clear()
        self.m_textCtrl_fuse840.write(self._parseReadFuseValue(self.scannedFuseList[68]))
        self.m_textCtrl_fuse850.Clear()
        self.m_textCtrl_fuse850.write(self._parseReadFuseValue(self.scannedFuseList[69]))
        self.m_textCtrl_fuse860.Clear()
        self.m_textCtrl_fuse860.write(self._parseReadFuseValue(self.scannedFuseList[70]))
        self.m_textCtrl_fuse870.Clear()
        self.m_textCtrl_fuse870.write(self._parseReadFuseValue(self.scannedFuseList[71]))
        self.m_textCtrl_fuse880.Clear()
        self.m_textCtrl_fuse880.write(self._parseReadFuseValue(self.scannedFuseList[72]))
        self.m_textCtrl_fuse890.Clear()
        self.m_textCtrl_fuse890.write(self._parseReadFuseValue(self.scannedFuseList[73]))
        self.m_textCtrl_fuse8a0.Clear()
        self.m_textCtrl_fuse8a0.write(self._parseReadFuseValue(self.scannedFuseList[74]))
        self.m_textCtrl_fuse8b0.Clear()
        self.m_textCtrl_fuse8b0.write(self._parseReadFuseValue(self.scannedFuseList[75]))
        self.m_textCtrl_fuse8c0.Clear()
        self.m_textCtrl_fuse8c0.write(self._parseReadFuseValue(self.scannedFuseList[76]))
        self.m_textCtrl_fuse8d0.Clear()
        self.m_textCtrl_fuse8d0.write(self._parseReadFuseValue(self.scannedFuseList[77]))
        self.m_textCtrl_fuse8e0.Clear()
        self.m_textCtrl_fuse8e0.write(self._parseReadFuseValue(self.scannedFuseList[78]))
        self.m_textCtrl_fuse8f0.Clear()
        self.m_textCtrl_fuse8f0.write(self._parseReadFuseValue(self.scannedFuseList[79]))

    def _swapRemappedScannedFuseIfAppliable( self ):
        if self.mcuDevice == uidef.kMcuDevice_iMXRT106x:
            for i in range(fusedef.kEfuseRemapLen):
                self.scannedFuseList[fusedef.kEfuseRemapIndex_Src + i], self.scannedFuseList[fusedef.kEfuseRemapIndex_Dest + i] = \
                self.scannedFuseList[fusedef.kEfuseRemapIndex_Dest + i], self.scannedFuseList[fusedef.kEfuseRemapIndex_Src + i]
        elif self.mcuDevice == uidef.kMcuDevice_iMXRT105x and self.mcuDevice == uidef.kMcuDevice_iMXRT102x:
            pass
        else:
            pass

    def scanAllFuseRegions( self ):
        for i in range(fusedef.kMaxEfuseWords):
            self.scannedFuseList[i] = self.readMcuDeviceFuseByBlhost(fusedef.kEfuseIndex_START + i, '', False)
        self._swapRemappedScannedFuseIfAppliable()
        self._setScannedFuse()

    def _parseUserFuseValue( self, fuseText ):
        if len(fuseText) >= 3 and fuseText[0:2] == '0x':
            return int(fuseText[2:len(fuseText)], 16)
        else:
            return None

    def _getToBeBurnnedFuse( self ):
        self.toBeBurnnedFuseList[0] = self._parseUserFuseValue(self.m_textCtrl_fuse400.GetLineText(0))
        self.toBeBurnnedFuseList[1] = self._parseUserFuseValue(self.m_textCtrl_fuse410.GetLineText(0))
        self.toBeBurnnedFuseList[2] = self._parseUserFuseValue(self.m_textCtrl_fuse420.GetLineText(0))
        self.toBeBurnnedFuseList[3] = self._parseUserFuseValue(self.m_textCtrl_fuse430.GetLineText(0))
        self.toBeBurnnedFuseList[4] = self._parseUserFuseValue(self.m_textCtrl_fuse440.GetLineText(0))
        self.toBeBurnnedFuseList[5] = self._parseUserFuseValue(self.m_textCtrl_fuse450.GetLineText(0))
        self.toBeBurnnedFuseList[6] = self._parseUserFuseValue(self.m_textCtrl_fuse460.GetLineText(0))
        self.toBeBurnnedFuseList[7] = self._parseUserFuseValue(self.m_textCtrl_fuse470.GetLineText(0))
        self.toBeBurnnedFuseList[8] = self._parseUserFuseValue(self.m_textCtrl_fuse480.GetLineText(0))
        self.toBeBurnnedFuseList[9] = self._parseUserFuseValue(self.m_textCtrl_fuse490.GetLineText(0))
        self.toBeBurnnedFuseList[10] = self._parseUserFuseValue(self.m_textCtrl_fuse4a0.GetLineText(0))
        self.toBeBurnnedFuseList[11] = self._parseUserFuseValue(self.m_textCtrl_fuse4b0.GetLineText(0))
        self.toBeBurnnedFuseList[12] = self._parseUserFuseValue(self.m_textCtrl_fuse4c0.GetLineText(0))
        self.toBeBurnnedFuseList[13] = self._parseUserFuseValue(self.m_textCtrl_fuse4d0.GetLineText(0))
        self.toBeBurnnedFuseList[14] = self._parseUserFuseValue(self.m_textCtrl_fuse4e0.GetLineText(0))
        self.toBeBurnnedFuseList[15] = self._parseUserFuseValue(self.m_textCtrl_fuse4f0.GetLineText(0))

        self.toBeBurnnedFuseList[16] = self._parseUserFuseValue(self.m_textCtrl_fuse500.GetLineText(0))
        self.toBeBurnnedFuseList[17] = self._parseUserFuseValue(self.m_textCtrl_fuse510.GetLineText(0))
        self.toBeBurnnedFuseList[18] = self._parseUserFuseValue(self.m_textCtrl_fuse520.GetLineText(0))
        self.toBeBurnnedFuseList[19] = self._parseUserFuseValue(self.m_textCtrl_fuse530.GetLineText(0))
        self.toBeBurnnedFuseList[20] = self._parseUserFuseValue(self.m_textCtrl_fuse540.GetLineText(0))
        self.toBeBurnnedFuseList[21] = self._parseUserFuseValue(self.m_textCtrl_fuse550.GetLineText(0))
        self.toBeBurnnedFuseList[22] = self._parseUserFuseValue(self.m_textCtrl_fuse560.GetLineText(0))
        self.toBeBurnnedFuseList[23] = self._parseUserFuseValue(self.m_textCtrl_fuse570.GetLineText(0))
        self.toBeBurnnedFuseList[24] = self._parseUserFuseValue(self.m_textCtrl_fuse580.GetLineText(0))
        self.toBeBurnnedFuseList[25] = self._parseUserFuseValue(self.m_textCtrl_fuse590.GetLineText(0))
        self.toBeBurnnedFuseList[26] = self._parseUserFuseValue(self.m_textCtrl_fuse5a0.GetLineText(0))
        self.toBeBurnnedFuseList[27] = self._parseUserFuseValue(self.m_textCtrl_fuse5b0.GetLineText(0))
        self.toBeBurnnedFuseList[28] = self._parseUserFuseValue(self.m_textCtrl_fuse5c0.GetLineText(0))
        self.toBeBurnnedFuseList[29] = self._parseUserFuseValue(self.m_textCtrl_fuse5d0.GetLineText(0))
        self.toBeBurnnedFuseList[30] = self._parseUserFuseValue(self.m_textCtrl_fuse5e0.GetLineText(0))
        self.toBeBurnnedFuseList[31] = self._parseUserFuseValue(self.m_textCtrl_fuse5f0.GetLineText(0))

        self.toBeBurnnedFuseList[32] = self._parseUserFuseValue(self.m_textCtrl_fuse600.GetLineText(0))
        self.toBeBurnnedFuseList[33] = self._parseUserFuseValue(self.m_textCtrl_fuse610.GetLineText(0))
        self.toBeBurnnedFuseList[34] = self._parseUserFuseValue(self.m_textCtrl_fuse620.GetLineText(0))
        self.toBeBurnnedFuseList[35] = self._parseUserFuseValue(self.m_textCtrl_fuse630.GetLineText(0))
        self.toBeBurnnedFuseList[36] = self._parseUserFuseValue(self.m_textCtrl_fuse640.GetLineText(0))
        self.toBeBurnnedFuseList[37] = self._parseUserFuseValue(self.m_textCtrl_fuse650.GetLineText(0))
        self.toBeBurnnedFuseList[38] = self._parseUserFuseValue(self.m_textCtrl_fuse660.GetLineText(0))
        self.toBeBurnnedFuseList[39] = self._parseUserFuseValue(self.m_textCtrl_fuse670.GetLineText(0))
        self.toBeBurnnedFuseList[40] = self._parseUserFuseValue(self.m_textCtrl_fuse680.GetLineText(0))
        self.toBeBurnnedFuseList[41] = self._parseUserFuseValue(self.m_textCtrl_fuse690.GetLineText(0))
        self.toBeBurnnedFuseList[42] = self._parseUserFuseValue(self.m_textCtrl_fuse6a0.GetLineText(0))
        self.toBeBurnnedFuseList[43] = self._parseUserFuseValue(self.m_textCtrl_fuse6b0.GetLineText(0))
        self.toBeBurnnedFuseList[44] = self._parseUserFuseValue(self.m_textCtrl_fuse6c0.GetLineText(0))
        self.toBeBurnnedFuseList[45] = self._parseUserFuseValue(self.m_textCtrl_fuse6d0.GetLineText(0))
        self.toBeBurnnedFuseList[46] = self._parseUserFuseValue(self.m_textCtrl_fuse6e0.GetLineText(0))
        self.toBeBurnnedFuseList[47] = self._parseUserFuseValue(self.m_textCtrl_fuse6f0.GetLineText(0))

        self.toBeBurnnedFuseList[48] = self._parseUserFuseValue(self.m_textCtrl_fuse700.GetLineText(0))
        self.toBeBurnnedFuseList[49] = self._parseUserFuseValue(self.m_textCtrl_fuse710.GetLineText(0))
        self.toBeBurnnedFuseList[50] = self._parseUserFuseValue(self.m_textCtrl_fuse720.GetLineText(0))
        self.toBeBurnnedFuseList[51] = self._parseUserFuseValue(self.m_textCtrl_fuse730.GetLineText(0))
        self.toBeBurnnedFuseList[52] = self._parseUserFuseValue(self.m_textCtrl_fuse730.GetLineText(0))
        self.toBeBurnnedFuseList[53] = self._parseUserFuseValue(self.m_textCtrl_fuse750.GetLineText(0))
        self.toBeBurnnedFuseList[54] = self._parseUserFuseValue(self.m_textCtrl_fuse760.GetLineText(0))
        self.toBeBurnnedFuseList[55] = self._parseUserFuseValue(self.m_textCtrl_fuse770.GetLineText(0))
        self.toBeBurnnedFuseList[56] = self._parseUserFuseValue(self.m_textCtrl_fuse780.GetLineText(0))
        self.toBeBurnnedFuseList[57] = self._parseUserFuseValue(self.m_textCtrl_fuse790.GetLineText(0))
        self.toBeBurnnedFuseList[58] = self._parseUserFuseValue(self.m_textCtrl_fuse7a0.GetLineText(0))
        self.toBeBurnnedFuseList[59] = self._parseUserFuseValue(self.m_textCtrl_fuse7b0.GetLineText(0))
        self.toBeBurnnedFuseList[60] = self._parseUserFuseValue(self.m_textCtrl_fuse7c0.GetLineText(0))
        self.toBeBurnnedFuseList[61] = self._parseUserFuseValue(self.m_textCtrl_fuse7d0.GetLineText(0))
        self.toBeBurnnedFuseList[62] = self._parseUserFuseValue(self.m_textCtrl_fuse7e0.GetLineText(0))
        self.toBeBurnnedFuseList[63] = self._parseUserFuseValue(self.m_textCtrl_fuse7f0.GetLineText(0))

        self.toBeBurnnedFuseList[64] = self._parseUserFuseValue(self.m_textCtrl_fuse800.GetLineText(0))
        self.toBeBurnnedFuseList[65] = self._parseUserFuseValue(self.m_textCtrl_fuse810.GetLineText(0))
        self.toBeBurnnedFuseList[66] = self._parseUserFuseValue(self.m_textCtrl_fuse820.GetLineText(0))
        self.toBeBurnnedFuseList[67] = self._parseUserFuseValue(self.m_textCtrl_fuse830.GetLineText(0))
        self.toBeBurnnedFuseList[68] = self._parseUserFuseValue(self.m_textCtrl_fuse840.GetLineText(0))
        self.toBeBurnnedFuseList[69] = self._parseUserFuseValue(self.m_textCtrl_fuse850.GetLineText(0))
        self.toBeBurnnedFuseList[70] = self._parseUserFuseValue(self.m_textCtrl_fuse860.GetLineText(0))
        self.toBeBurnnedFuseList[71] = self._parseUserFuseValue(self.m_textCtrl_fuse870.GetLineText(0))
        self.toBeBurnnedFuseList[72] = self._parseUserFuseValue(self.m_textCtrl_fuse880.GetLineText(0))
        self.toBeBurnnedFuseList[73] = self._parseUserFuseValue(self.m_textCtrl_fuse890.GetLineText(0))
        self.toBeBurnnedFuseList[74] = self._parseUserFuseValue(self.m_textCtrl_fuse8a0.GetLineText(0))
        self.toBeBurnnedFuseList[75] = self._parseUserFuseValue(self.m_textCtrl_fuse8b0.GetLineText(0))
        self.toBeBurnnedFuseList[76] = self._parseUserFuseValue(self.m_textCtrl_fuse8c0.GetLineText(0))
        self.toBeBurnnedFuseList[77] = self._parseUserFuseValue(self.m_textCtrl_fuse8d0.GetLineText(0))
        self.toBeBurnnedFuseList[78] = self._parseUserFuseValue(self.m_textCtrl_fuse8e0.GetLineText(0))
        self.toBeBurnnedFuseList[79] = self._parseUserFuseValue(self.m_textCtrl_fuse8f0.GetLineText(0))

    def _swapRemappedToBeBurnFuseIfAppliable( self ):
        if self.mcuDevice == uidef.kMcuDevice_iMXRT106x:
            for i in range(fusedef.kEfuseRemapLen):
                self.toBeBurnnedFuseList[fusedef.kEfuseRemapIndex_Src + i], self.toBeBurnnedFuseList[fusedef.kEfuseRemapIndex_Dest + i] = \
                self.toBeBurnnedFuseList[fusedef.kEfuseRemapIndex_Dest + i], self.toBeBurnnedFuseList[fusedef.kEfuseRemapIndex_Src + i]
        elif self.mcuDevice == uidef.kMcuDevice_iMXRT105x and self.mcuDevice == uidef.kMcuDevice_iMXRT102x:
            pass
        else:
            pass

    def burnAllFuseRegions( self ):
        self._getToBeBurnnedFuse()
        self._swapRemappedToBeBurnFuseIfAppliable()
        for i in range(fusedef.kMaxEfuseWords):
            if self.toBeBurnnedFuseList[i] != self.scannedFuseList[i] and self.toBeBurnnedFuseList[i] != None:
                fuseValue = self.toBeBurnnedFuseList[i] | self.scannedFuseList[i]
                self.burnMcuDeviceFuseByBlhost(fusedef.kEfuseIndex_START + i, fuseValue)
        self.scanAllFuseRegions()
