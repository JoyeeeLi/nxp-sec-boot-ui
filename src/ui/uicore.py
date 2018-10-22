import wx
import sys, os
import uidef
sys.path.append(os.path.abspath("../.."))
from gui import nxpSecBoot
sys.path.append(os.path.abspath(".."))
from boot import bootdef

class secBootUi(nxpSecBoot.secBootWin):

    def __init__(self, parent):
        nxpSecBoot.secBootWin.__init__(self, parent)
        self.setSecureBootSeqColor()

    def resetSecureBootSeqColor( self ):
        self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_progDek1_showDek.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.resetKeyStorageRegionColor()
        self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )

    def resetKeyStorageRegionColor( self ):
        self.m_panel_prepBee1_beeKeyRegion.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_prepBee2_beeKeyInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_prepBee3_advKeySettings.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_prepBee4_beeCryptoAlgo.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_operBeeKey1_readOtpmk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )
        self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INVALID )

    def setSecureBootSeqColor( self ):
        secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.resetSecureBootSeqColor()
        if secureBootType == bootdef.SECURE_BOOT_TYPE_DEVELOPMENT:
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
        elif secureBootType == bootdef.SECURE_BOOT_TYPE_HAB_AUTH:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
        elif secureBootType == bootdef.SECURE_BOOT_TYPE_HAB_CRYPTO:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_progDek1_showDek.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
        elif secureBootType == bootdef.SECURE_BOOT_TYPE_BEE_CRYPTO:
            self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INACTIVE )
            self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INACTIVE )
            self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_INACTIVE )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.setKeyStorageRegionColor()
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
        else:
            pass

    def setKeyStorageRegionColor( self ):
        secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        if secureBootType == bootdef.SECURE_BOOT_TYPE_BEE_CRYPTO:
            self.resetKeyStorageRegionColor()
            keyStorageRegion = self.m_choice_keyStorageRegion.GetString(self.m_choice_keyStorageRegion.GetSelection())
            self.m_panel_prepBee1_beeKeyRegion.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            self.m_panel_prepBee4_beeCryptoAlgo.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            if keyStorageRegion == bootdef.KEY_STORAGE_REGION_OPTMK:
                self.m_panel_operBeeKey1_readOtpmk.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            elif keyStorageRegion == bootdef.KEY_STORAGE_REGION_GP4 or keyStorageRegion == bootdef.KEY_STORAGE_REGION_SW_GP2:
                self.m_panel_prepBee2_beeKeyInput.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
                self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            elif keyStorageRegion == bootdef.KEY_STORAGE_REGION_GP4_SW_GP2:
                self.m_panel_prepBee3_advKeySettings.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
                self.m_panel_operBeeKey2_progBeeKey.SetBackgroundColour( uidef.BOOT_SEQ_COLOR_ACTIVE )
            else:
                pass



