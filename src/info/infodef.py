import sys, os

kRegisterAddr_UUID1  = 0x401F4410
kRegisterAddr_UUID2  = 0x401F4420

kRegisterAddr_SRC_SBMR1  = 0x400F8004
kRegisterAddr_SRC_SBMR2  = 0x400F801C

kEfuseAddr_BOOT_CFG0  = 0x5
kEfuseAddr_BOOT_CFG1  = 0x6
kEfuseAddr_BOOT_CFG2  = 0x7

kEfuseAddr_OTPMK0 = 0x10
kEfuseAddr_OTPMK1 = 0x11
kEfuseAddr_OTPMK2 = 0x12
kEfuseAddr_OTPMK3 = 0x13
kEfuseAddr_OTPMK4 = 0x14
kEfuseAddr_OTPMK5 = 0x15
kEfuseAddr_OTPMK6 = 0x16
kEfuseAddr_OTPMK7 = 0x17

kEfuseAddr_SRK0 = 0x18
kEfuseAddr_SRK1 = 0x19
kEfuseAddr_SRK2 = 0x1A
kEfuseAddr_SRK3 = 0x1B
kEfuseAddr_SRK4 = 0x1C
kEfuseAddr_SRK5 = 0x1D
kEfuseAddr_SRK6 = 0x1E
kEfuseAddr_SRK7 = 0x1F

kEfuseAddr_SW_GP2_0 = 0x29
kEfuseAddr_SW_GP2_1 = 0x2A
kEfuseAddr_SW_GP2_2 = 0x2B
kEfuseAddr_SW_GP2_3 = 0x2C

kEfuseAddr_GP4_0 = 0x4C
kEfuseAddr_GP4_1 = 0x4D
kEfuseAddr_GP4_2 = 0x4E
kEfuseAddr_GP4_3 = 0x4F

#----------------SEMC NAND----------------------
kSemcNandFcbTag_Fingerprint = 0x4E464342  # 'NFCB'
kSemcNandFcbTag_Semc        = 0x434D4553  # 'SEMC'

kSemcNandFcbInfo_StartAddr = 0x0
kSemcNandFcbInfo_Length    = 0x400

kSemcNandFcbOffset_Fingerprint    = 0x004
kSemcNandFcbOffset_FirmwareCopies = 0x014
kSemcNandFcbOffset_NandCfgBlock   = 0x100
kSemcNandFcbOffset_SemcTag        = 0x100
kSemcNandFcbOffset_PageByteSize   = 0x1a0
kSemcNandFcbOffset_PagesInBlock   = 0x1a8
kSemcNandFcbOffset_BlocksInPlane  = 0x1ac
kSemcNandFcbOffset_PlanesInDevice = 0x1b0

#----------------FlexSPI NOR---------------------
kFlexspiNorCfgTag_Flexspi = 0x42464346  # 'FCFB'

kFlexspiNorCfgInfo_StartAddr = 0x0
kFlexspiNorCfgInfo_Length    = 0x1000
kFlexspiNorCfgInfo_Notify    = 0xF000000F

kFlexspiNorCfgOffset_FlexspiTag     = 0x000
kFlexspiNorCfgOffset_PageByteSize   = 0x1c0
kFlexspiNorCfgOffset_SectorByteSize = 0x1c4
kFlexspiNorCfgOffset_BlockByteSize  = 0x1d0

