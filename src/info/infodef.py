import sys, os

kRegisterAddr_UUID1  = 0x401F4410
kRegisterAddr_UUID2  = 0x401F4420

kRegisterAddr_SRC_SBMR1  = 0x400F8004
kRegisterAddr_SRC_SBMR2  = 0x400F801C

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

