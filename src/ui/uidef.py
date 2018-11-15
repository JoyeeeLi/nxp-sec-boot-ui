import wx
import sys, os

kConnectStage_Rom            = 1
kConnectStage_Flashloader    = 2
kConnectStage_ExternalMemory = 3
kConnectStage_Reset          = 4

kConnectStep_Fast   = 3
kConnectStep_Normal = 1

kBootSeqColor_Invalid  = wx.Colour( 160, 160, 160 )
kBootSeqColor_Optional = wx.Colour( 166, 255, 255 )
kBootSeqColor_Active   = wx.Colour( 147, 255, 174 )

kMcuDevice_iMXRT102x = 'i.MXRT102x'
kMcuDevice_iMXRT105x = 'i.MXRT105x'
kMcuDevice_iMXRT106x = 'i.MXRT106x'

kBootDevice_FlexspiNor     = 'FLEXSPI NOR'
kBootDevice_FlexspiNand    = 'FLEXSPI NAND'
kBootDevice_SemcNor        = 'SEMC NOR'
kBootDevice_SemcNand       = 'SEMC NAND'
kBootDevice_UsdhcSd        = 'uSDHC SD'
kBootDevice_UsdhcMmc       = 'uSDHC MMC/eMMC'
kBootDevice_LpspiNor       = 'LPSPI NOR,EEPROM'
kBootDevice_RamFlashloader = 'RAM FLASHLOADER'

kSecureBootType_Development = 'Unsigned (XIP) Image Boot'
kSecureBootType_HabAuth     = 'Signed (XIP) Image Boot'
kSecureBootType_HabCrypto   = 'HAB Signed Encrypted Image Boot'
kSecureBootType_BeeCrypto   = 'BEE (Signed) Encrypted XIP Image Boot'

kKeyStorageRegion_FixedOtpmkKey    = 'Fixed SNVS Key'
kKeyStorageRegion_FlexibleUserKeys = 'Flexible User Keys'

kAdvancedSettings_Cert      = 1
kAdvancedSettings_BD        = 2
kAdvancedSettings_OtpmkKey  = 3
kAdvancedSettings_UserKeys  = 4

kCstVersion_Invalid = 'x.x.x'
kCstVersion_v2_3_3  = '2.3.3'
kCstVersion_v3_0_1  = '3.0.1'
kCstVersion_v3_1_0  = '3.1.0'

kPkiTreeKeySel_IsEcc  = ['p256', 'p384', 'p521']
kPkiTreeKeySel_NotEcc = ['1024', '2048', '3072', '4096']

kUserRegionSel_Region0     = 'Region 0'
kUserRegionSel_Region1     = 'Region 1'
kUserRegionSel_BothRegions = 'Both Regions'

kUserKeySource_OTPMK  = 'Fuse OTPMK[255:128]'
kUserKeySource_SW_GP2 = 'Fuse SW-GP2'
kUserKeySource_GP4    = 'Fuse GP4[127:0]'

kSupportedKeySource_iMXRT102x = [kUserKeySource_SW_GP2]
kSupportedKeySource_iMXRT105x = [kUserKeySource_SW_GP2]
kSupportedKeySource_iMXRT106x = [kUserKeySource_SW_GP2, kUserKeySource_GP4]

kMaxFacRegionCount = 3
