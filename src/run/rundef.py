import sys, os

kUartSpeed_Blhost = ['4800', '9600', '19200', '57600', '115200']
kUartSpeed_Sdphost = ['115200']

kBootDeviceMemId_SemcNor      = 0x8
kBootDeviceMemId_FlexspiNor   = 0x9
kBootDeviceMemId_SemcNand     = 0x100
kBootDeviceMemId_FlexspiNand  = 0x101
kBootDeviceMemId_LpspiNor     = 0x110
kBootDeviceMemId_UsdhcSd      = 0x120
kBootDeviceMemId_UsdhcMmc     = 0x121

kBootDeviceMemBase_SemcNor      = 0x90000000
kBootDeviceMemBase_FlexspiNor   = 0x60000000
kBootDeviceMemBase_SemcNand     = 0x0
kBootDeviceMemBase_FlexspiNand  = 0x0
kBootDeviceMemBase_LpspiNor     = 0x0
kBootDeviceMemBase_UsdhcSd      = 0x0
kBootDeviceMemBase_UsdhcMmc     = 0x0

kRamFreeSpaceStart_LoadCommOpt        = 0x00002000
kRamFreeSpaceStart_LoadDekData        = 0x00002100
kRamFreeSpaceStart_LoadKeyBlobContext = 0x00002200
kRamFreeSpaceStart_LoadKeyBlobData    = 0x00002300
kRamFreeSpaceStart_LoadCfgBlock       = 0x00003000
kRamFreeSpaceStart_LoadPrdbOpt        = 0x00004000

kRamFreeSpaceStep_LoadKeyBlobData    = 0x100

kRamFreeSpaceStart_Rom         = 0x20208000

kKeyBlobMaxSize = 512

kRegisterAddr_UUID1  = 0x401F4410
kRegisterAddr_UUID2  = 0x401F4420

kRegisterAddr_SRC_SBMR1  = 0x400F8004
kRegisterAddr_SRC_SBMR2  = 0x400F801C

kRegisterMask_Bmod = 0x03000000
kRegisterShift_Bmod = 24

kRegisterMask_BtFuseSel = 0x00000010
kRegisterShift_BtFuseSel = 4

kRegisterMask_SecConfig = 0x00000003
kRegisterShift_SecConfig = 0

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
kFlexspiNorCfgInfo_Length    = 0x400
kFlexspiNorCfgInfo_Notify    = 0xF000000F

kFlexspiNorCfgOffset_FlexspiTag     = 0x000
kFlexspiNorCfgOffset_PageByteSize   = 0x1c0
kFlexspiNorCfgOffset_SectorByteSize = 0x1c4
kFlexspiNorCfgOffset_BlockByteSize  = 0x1d0

