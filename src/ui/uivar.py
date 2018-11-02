#! /usr/bin/env python
import sys
import os
import uidef

g_semcNandOpt = None
g_semcNandFcbOpt = None
g_semcNandImageInfo = None

g_flexspiNorOpt0 = None
g_flexspiNorOpt1 = None

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
    g_flexspiNorOpt0 = 0xC0000000
    g_flexspiNorOpt1 = 0x00000000

def getVar( group ):
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

def setVar( group, *args ):
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

