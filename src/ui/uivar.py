#! /usr/bin/env python
import sys
import os
import uidef

g_semcNandOpt = None
g_semcNandFcbOpt = None
g_semcNandImageInfo = None

def initVar():
    global g_semcNandOpt
    global g_semcNandFcbOpt
    global g_semcNandImageInfo
    g_semcNandOpt = 0xD0000000
    g_semcNandFcbOpt = 0x00000000
    g_semcNandImageInfo = [None] * 8

def getVar( group ):
    if group == uidef.kBootDevice_SemcNand:
        global g_semcNandOpt
        global g_semcNandFcbOpt
        global g_semcNandImageInfo
        return g_semcNandOpt, g_semcNandFcbOpt, g_semcNandImageInfo
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
    else:
        pass

