import sys, os

kToolchainSymbolList_EntryAddr = ['Reset_Handler', '__iar_program_start']
kToolchainSymbolList_VectorAddr = ['__VECTOR_TABLE', '__vector_table', '__Vectors']

#define NOR_EEPROM_IROM_DATA_HEADER_OFFSET      (0x400)
#define FLEXSPI_NOR_IROM_DATA_HEADER_OFFSET     (0x1000)
#define FLEXSPI_NAND_IROM_DATA_HEADER_OFFSET    (0x400)
#define SEMC_NOR_IROM_DATA_HEADER_OFFSET        (0x1000)
#define SEMC_NAND_IROM_DATA_HEADER_OFFSET       (0x400)
#define CARD_IROM_DATA_HEADER_OFFSET            (0x400)

kIvtOffset_NAND_SD_EEPROM = 0x400
kIvtOffset_NOR            = 0x1000

#define SPI_NOR_EEPROM_4K_SIZE                  (4096U)
#define FLEXSPI_NOR_INIT_IMG_SIZE               (12u * 1024u)
#define FLEXSPI_NAND_4K_SIZE                    (4096U)
#define SEMC_NOR_INIT_IMG_SIZE                  (12u * 1024u)
#define SEMC_NAND_4K_SIZE                       (4096U)
#define CARD_IROM_INIT_IMAGE_SIZE               (4096U)

kInitialLoadSize_NAND_SD_EEPROM = 0x1000
kInitialLoadSize_NOR            = 0x2000
