import wx
import sys, os

kConnectStage_Rom            = 1
kConnectStage_Flashloader    = 2
kConnectStage_ExternalMemory = 3
kConnectStage_Reset          = 4

kConnectStep_Fast   = 3
kConnectStep_Normal = 1

kBootSeqColor_Invalid  = wx.Colour( 160, 160, 160 )
kBootSeqColor_Inactive = wx.Colour( 166, 255, 255 )
kBootSeqColor_Active   = wx.Colour( 147, 255, 174 )

kMcuDevice_iMXRT102x = 'i.MXRT102x'
kMcuDevice_iMXRT105x = 'i.MXRT105x'
kMcuDevice_iMXRT106x = 'i.MXRT106x'

kBootDevice_FlexspiNor  = 'FLEXSPI NOR'
kBootDevice_FlexspiNand = 'FLEXSPI NAND'
kBootDevice_SemcNor     = 'SEMC NOR'
kBootDevice_SemcNand    = 'SEMC NAND'
kBootDevice_UsdhcSd     = 'uSDHC SD'
kBootDevice_UsdhcMmc    = 'uSDHC MMC/eMMC'
kBootDevice_LpspiNor    = 'LPSPI NOR,EEPROM'

kSecureBootType_Development = 'Unsigned (XIP) image Boot'
kSecureBootType_HabAuth     = 'Signed (XIP) Image Boot'
kSecureBootType_HabCrypto   = 'HAB Signed Encrypted Image Boot'
kSecureBootType_BeeCrypto   = 'BEE (Signed) Encrypted XIP Image Boot'

kKeyStorageRegion_Otpmk    = 'Fuse OTPMK'
kKeyStorageRegion_Gp4      = 'Fuse GP4'
kKeyStorageRegion_SwGp2    = 'Fuse SW_GP2 '
kKeyStorageRegion_Gp4SwGp2 = 'Fuse GP4&SW_GP2'

kAdvancedSettings_Cert      = 1
kAdvancedSettings_BD        = 2
kAdvancedSettings_OtpmkKey  = 3

kCstVersion_Invalid = 'x.x.x'
kCstVersion_v2_3_3  = '2.3.3'
kCstVersion_v3_0_1  = '3.0.1'

