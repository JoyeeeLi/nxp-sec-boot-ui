#! /usr/bin/env python
import sys
import os
import uidef

g_semcNandOpt = None
g_semcNandFcbOpt = None
g_semcNandImageInfo = None

g_flexspiNorOpt0 = None
g_flexspiNorOpt1 = None

g_certSettingsDict = {'cstVersion':None,
                      'useExistingCaKey':None,
                      'pkiTreeKeyLen':None,
                      'pkiTreeDuration':None,
                      'SRKs':None,
                      'caFlagSet':None}

def initVar():
    global g_semcNandOpt
    global g_semcNandFcbOpt
    global g_semcNandImageInfo
    g_semcNandOpt = 0xD0010101
    g_semcNandFcbOpt = 0x00010101
    g_semcNandImageInfo = [None] * 8
    g_semcNandImageInfo[0] = 0x00020001

    global g_flexspiNorOpt0
    global g_flexspiNorOpt1
    g_flexspiNorOpt0 = 0xc0000006
    g_flexspiNorOpt1 = 0x00000000

    global g_certSettingsDict
    g_certSettingsDict['cstVersion'] = uidef.kCstVersion_v2_3_3
    g_certSettingsDict['useExistingCaKey'] = 'n'
    g_certSettingsDict['pkiTreeKeyLen'] = 2048
    g_certSettingsDict['pkiTreeDuration'] = 10
    g_certSettingsDict['SRKs'] = 4
    g_certSettingsDict['caFlagSet'] = 'y'

def getBootDeviceConfiguration( group ):
    if group == uidef.kBootDevice_SemcNand:
        global g_semcNandOpt
        global g_semcNandFcbOpt
        global g_semcNandImageInfo
        return g_semcNandOpt, g_semcNandFcbOpt, g_semcNandImageInfo
    elif group == uidef.kBootDevice_FlexspiNor:
        global g_flexspiNorOpt0
        global g_flexspiNorOpt1
        return g_flexspiNorOpt0, g_flexspiNorOpt1
    else:
        pass

def setBootDeviceConfiguration( group, *args ):
    if group == uidef.kBootDevice_SemcNand:
        global g_semcNandOpt
        global g_semcNandFcbOpt
        global g_semcNandImageInfo
        g_semcNandOpt = args[0]
        g_semcNandFcbOpt = args[1]
        g_semcNandImageInfo = args[2]
    elif group == uidef.kBootDevice_FlexspiNor:
        global g_flexspiNorOpt0
        global g_flexspiNorOpt1
        g_flexspiNorOpt0 = args[0]
        g_flexspiNorOpt1 = args[1]
    else:
        pass

def getAdvancedSettings( group ):
    if group == uidef.kAdvancedSettings_Cert:
        global g_certSettingsDict
        return g_certSettingsDict
    else:
        pass

def setAdvancedSettings( group, *args ):
    if group == uidef.kAdvancedSettings_Cert:
        global g_certSettingsDict
        g_certSettingsDict = args[0]
    else:
        pass

