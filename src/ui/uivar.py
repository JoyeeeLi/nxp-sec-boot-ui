#! /usr/bin/env python
import sys
import os
import uidef

g_flexspiNorOpt0 = None
g_flexspiNorOpt1 = None

g_flexspiNandOpt = None
g_flexspiNandFcbOpt = None
g_flexspiNandImageInfo = None
g_flexspiNandKeyBlob = None

g_semcNorOpt = None
g_semcNorSetting = None

g_semcNandOpt = None
g_semcNandFcbOpt = None
g_semcNandImageInfo = None

g_usdhcSDOpt = None

g_UsdhcMmcOpt1 = None
usdhcMmcOpt2 = None

g_certSettingsDict = {'cstVersion':None,
                      'useExistingCaKey':None,
                      'pkiTreeKeyLen':None,
                      'pkiTreeDuration':None,
                      'SRKs':None,
                      'caFlagSet':None}

g_otpmkKeyOpt = None
g_otpmkEncryptedRegionStart = None
g_otpmkEncryptedRegionLength = None

g_UserKeyCtrlDict = {'region_sel':None,
                     'region0_key_src':None,
                     'region0_fac_cnt':None,
                     'region1_key_src':None,
                     'region1_fac_cnt':None}
g_UserKeyCmdDict = {'base_addr':None,
                    'region0_key':None,
                    'region0_arg':None,
                    'region0_lock':None,
                    'region1_key':None,
                    'region1_arg':None,
                    'region1_lock':None,
                    'use_zero_key':None,
                    'is_boot_image':None}

def initVar():
    global g_flexspiNorOpt0
    global g_flexspiNorOpt1
    g_flexspiNorOpt0 = 0xc0000006
    g_flexspiNorOpt1 = 0x00000000

    global g_flexspiNandOpt
    global g_flexspiNandFcbOpt
    global g_flexspiNandKeyBlob
    global g_flexspiNandImageInfo
    g_flexspiNandOpt = 0xD0010101
    g_flexspiNandFcbOpt = 0x00010601
    g_flexspiNandImageInfo = 0x0
    g_flexspiNandKeyBlob = 0x0

    global g_semcNorOpt
    global g_semcNorSetting
    g_semcNorOpt = 0xD0010101
    g_semcNorSetting = 0x00010601

    global g_semcNandOpt
    global g_semcNandFcbOpt
    global g_semcNandImageInfo
    g_semcNandOpt = 0xD0010101
    g_semcNandFcbOpt = 0x00010601
    g_semcNandImageInfo = [None] * 8
    g_semcNandImageInfo[0] = 0x00020001

    global g_usdhcSDOpt
    g_usdhcSDOpt = 0xD0010101

    global g_UsdhcMmcOpt1
    global g_UsdhcMmcOpt2
    g_UsdhcMmcOpt1 = 0xD0010101
    g_UsdhcMmcOpt2 = 0xD0010101

    global g_certSettingsDict
    g_certSettingsDict['cstVersion'] = uidef.kCstVersion_v3_0_1
    g_certSettingsDict['useExistingCaKey'] = 'n'
    g_certSettingsDict['pkiTreeKeyLen'] = 2048
    g_certSettingsDict['pkiTreeDuration'] = 10
    g_certSettingsDict['SRKs'] = 4
    g_certSettingsDict['caFlagSet'] = 'y'

    global g_otpmkKeyOpt
    global g_otpmkEncryptedRegionStart
    global g_otpmkEncryptedRegionLength
    g_otpmkKeyOpt = 0xe0100000
    g_otpmkEncryptedRegionStart = [None] * 2
    g_otpmkEncryptedRegionLength = [None] * 2

    global g_UserKeyCtrlDict
    global g_UserKeyCmdDict
    g_UserKeyCtrlDict['region_sel'] = uidef.kUserRegionSel_BothRegions
    g_UserKeyCtrlDict['region0_key_src'] = uidef.kUserKeySource_OTPMK
    g_UserKeyCtrlDict['region0_fac_cnt'] = 1
    g_UserKeyCtrlDict['region1_key_src'] = uidef.kUserKeySource_OTPMK
    g_UserKeyCtrlDict['region1_fac_cnt'] = 1
    g_UserKeyCmdDict['base_addr'] = '0x60000000'
    #g_UserKeyCmdDict['region0_key']
    g_UserKeyCmdDict['region0_arg'] = '1,[0x60001000,0x1000,0]'
    g_UserKeyCmdDict['region0_lock'] = '0'
    #g_UserKeyCmdDict['region1_key']
    g_UserKeyCmdDict['region1_arg'] = '1,[0x60002000,0x1000,0]'
    g_UserKeyCmdDict['region1_lock'] = '0'
    g_UserKeyCmdDict['use_zero_key'] = '1'
    g_UserKeyCmdDict['is_boot_image'] = '1'

def getBootDeviceConfiguration( group ):
    if group == uidef.kBootDevice_FlexspiNor:
        global g_flexspiNorOpt0
        global g_flexspiNorOpt1
        return g_flexspiNorOpt0, g_flexspiNorOpt1
    elif group == uidef.kBootDevice_FlexspiNand:
        global g_flexspiNandOpt
        global g_flexspiNandFcbOpt
        global g_flexspiNandKeyBlob
        global g_flexspiNandImageInfo
        return g_flexspiNandOpt, g_flexspiNandFcbOpt, g_flexspiNandImageInfo, g_flexspiNandKeyBlob
    elif group == uidef.kBootDevice_SemcNor:
        global g_semcNorOpt
        global g_semcNorSetting
        return g_semcNorOpt, g_semcNorSetting
    elif group == uidef.kBootDevice_SemcNand:
        global g_semcNandOpt
        global g_semcNandFcbOpt
        global g_semcNandImageInfo
        return g_semcNandOpt, g_semcNandFcbOpt, g_semcNandImageInfo
    elif group == uidef.kBootDevice_UsdhcSd:
        global g_usdhcSDOpt
        return g_usdhcSDOpt
    elif group == uidef.kBootDevice_UsdhcMmc:
        global g_UsdhcMmcOpt1
        global g_UsdhcMmcOpt2
        return g_UsdhcMmcOpt1, g_UsdhcMmcOpt2
    elif group == uidef.kBootDevice_LpspiNor:
        pass
    else:
        pass


def setBootDeviceConfiguration( group, *args ):
    if group == uidef.kBootDevice_FlexspiNor:
        global g_flexspiNorOpt0
        global g_flexspiNorOpt1
        g_flexspiNorOpt0 = args[0]
        g_flexspiNorOpt1 = args[1]
    elif group == uidef.kBootDevice_FlexspiNand:
        global g_flexspiNandOpt
        global g_flexspiNandFcbOpt
        global g_flexspiNandKeyBlob
        global g_flexspiNandImageInfo
        g_flexspiNandOpt = args[0]
        g_flexspiNandFcbOpt = args[1]
        g_flexspiNandImageInfo = args[2]
        g_flexspiNandKeyBlob = args[3]
    elif group == uidef.kBootDevice_SemcNor:
        global g_semcNorOpt
        global g_semcNorSetting
        g_semcNorOpt = args[0]
        g_semcNorSetting = args[1]
    elif group == uidef.kBootDevice_SemcNand:
        global g_semcNandOpt
        global g_semcNandFcbOpt
        global g_semcNandImageInfo
        g_semcNandOpt = args[0]
        g_semcNandFcbOpt = args[1]
        g_semcNandImageInfo = args[2]
    elif group == uidef.kBootDevice_UsdhcSd:
        global g_usdhcSDOpt
        g_usdhcSDOpt = args[0]
    elif group == uidef.kBootDevice_UsdhcMmc:
        global g_UsdhcMmcOpt1
        global g_UsdhcMmcOpt2
        g_UsdhcMmcOpt1 = args[0]
        g_UsdhcMmcOpt2 = args[1]
    elif group == uidef.kBootDevice_LpspiNor:
        pass
    else:
        pass

def getAdvancedSettings( group ):
    if group == uidef.kAdvancedSettings_Cert:
        global g_certSettingsDict
        return g_certSettingsDict
    elif group == uidef.kAdvancedSettings_OtpmkKey:
        global g_otpmkKeyOpt
        global g_otpmkEncryptedRegionStart
        global g_otpmkEncryptedRegionLength
        return g_otpmkKeyOpt, g_otpmkEncryptedRegionStart, g_otpmkEncryptedRegionLength
    elif group == uidef.kAdvancedSettings_UserKeys:
        global g_UserKeyCtrlDict
        global g_UserKeyCmdDict
        return g_UserKeyCtrlDict, g_UserKeyCmdDict
    else:
        pass

def setAdvancedSettings( group, *args ):
    if group == uidef.kAdvancedSettings_Cert:
        global g_certSettingsDict
        g_certSettingsDict = args[0]
    elif group == uidef.kAdvancedSettings_OtpmkKey:
        global g_otpmkKeyOpt
        global g_otpmkEncryptedRegionStart
        global g_otpmkEncryptedRegionLength
        g_otpmkKeyOpt = args[0]
        g_otpmkEncryptedRegionStart = args[1]
        g_otpmkEncryptedRegionLength = args[2]
    elif group == uidef.kAdvancedSettings_UserKeys:
        global g_UserKeyCtrlDict
        global g_UserKeyCmdDict
        g_UserKeyCtrlDict = args[0]
        g_UserKeyCmdDict = args[1]
    else:
        pass

global_count = {}
global_count[1] = 0
global_count[2] = 0
global_count[3] = 0
global_count[4] = 0
global_count[5] = 0
global_count[6] = 0
global_count[7] = 0