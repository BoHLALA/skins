import socket
import os
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Button import Button
from enigma import eConsoleAppContainer, eTimer
from Screens.MessageBox import MessageBox

PLUGIN_ICON = "icon.png"
PLUGIN_VERSION = "2.0.0"

class InstallProgressScreen(Screen):
    skin = """
 <screen name="InstallProgressScreen" position="center,center" size="1088,348" title="Installing..." backgroundColor="#40000000"> 

<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/SmartAddonspanel/Skin/BO-hlala.png" scale="1" position="0,0" size="1088,348" zPosition="-1" alphatest="blend" />
 <!-- ***** BoHLALA  ***** -->
  <ePixmap pixmap="BoHLALA_FHD/BO-hlala/wi2.png" position="1000,182" size="70,142" scale="1" alphatest="blend" zPosition="12" />
  <widget name="icon" position="75,16" size="37,37" pixmaps="BoHLALA_FHD/icons/message/question-53.png,icons/message/info-53.png,icons/message/info-53.png,icons/message/attention-53.png,icons/message/info-53.png" alphatest="blend" conditional="icon" scale="1" transparent="1" />
  <widget name="status" position="8,66" size="1061,273" font="Regular; 37" halign="center" transparent="1" backgroundColor="#e61616" borderWidth="4" borderColor="black" zPosition="4" valign="top" />
  <widget name="ErrorPixmap" pixmap="BoHLALA_FHD/icons/input_error.png" scale="1" position="75,16" size="37,37" alphatest="blend" />
  <widget name="QuestionPixmap" pixmap="BoHLALA_FHD/icons/input_question.png" scale="1" position="75,16" size="37,37" alphatest="blend" />
  <widget name="InfoPixmap" pixmap="BoHLALA_FHD/icons/input_info.png" scale="1" position="10,5" size="50,48" alphatest="blend" />
  <widget name="WarningPixmap" pixmap="BoHLALA_FHD/icons/input_warning.png" position="75,16" size="37,37" scale="1" alphatest="blend" />
  <widget name="list" position="9,227" size="1068,100" valign="center" halign="left" padding="10,0" itemHeight="50" font="Regular;30" transparent="1" scrollbarMode="showOnDemand" scrollbarForegroundColor="mcolor5" scrollbarBorderColor="mcolor2" scrollbarWidth="10" scrollbarBorderWidth="0" scrollbarRadius="5" itemCornerRadius="14" selectionPixmap="BoHLALA_FHD/menu/button1180x44.png" render="Listbox" foregroundColor="une5b243" backgroundColor="black" />
  <eLabel text="PluginsDownload Box" position="124,15" size="945,36" font="Regular; 26" backgroundColor="#fa0909" shadowColor="#000000" halign="left" transparent="1" zPosition="9" borderWidth="2" borderColor="black" />
  <applet type="onLayoutFinish">
    from enigma import eSize, ePoint
    orgwidth = self.instance.size().width()
    orgpos = self.instance.position()
    textsize = self["text"].getSize()
    textsize = (textsize[0] + 50, textsize[1] + 20)
    wsizex = textsize[0] + 50
    wsizey = textsize[1]
    if (64 &gt; wsizey):
	wsizey = 64
    if self.type == self.TYPE_YESNO:
	wsizey += 60
    if (280 &gt; wsizex):
	wsizex = 280
    wsize = (wsizex, wsizey)
    self.instance.resize(eSize(*wsize))
    self["text"].instance.resize(eSize(*textsize))
    listsize = (wsizex, 50)
    self["list"].instance.move(ePoint(0, textsize[1]))
    self["list"].instance.resize(eSize(*listsize))
    newwidth = wsize[0]
    self.instance.move(ePoint(orgpos.x() + (orgwidth - newwidth)/2, orgpos.y()))
    self.autoResize()
  </applet>
</screen>
    """

    def __init__(self, session, selected_plugins):
        self.session = session
        Screen.__init__(self, session)
        self.selected_plugins = selected_plugins
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.command_finished)
        self.container.dataAvail.append(self.command_output)
        self.current_plugin_index = 0
        self["status"] = Label("")
        self.run_next_command()

    def run_next_command(self):
        if self.current_plugin_index < len(self.selected_plugins):
            plugin_name, command = self.selected_plugins[self.current_plugin_index]
            self["status"].setText(f"Installing: {plugin_name} ({self.current_plugin_index + 1}/{len(self.selected_plugins)})...")
            if self.container.execute(command):
                self["status"].setText(f"Failed to execute: {command}")
        else:
            self.session.openWithCallback(
                self.on_close_messagebox,
                MessageBox,
                f"All plugins installed ({len(self.selected_plugins)}). Restarting Enigma2...",
                MessageBox.TYPE_INFO,
                timeout=5,
            )
            os.system("killall -9 enigma2")

    def command_output(self, data):
        pass

    def command_finished(self, retval):
        self.current_plugin_index += 1
        self.run_next_command()
                                                                           
    def on_close_messagebox(self, result):
        self.close()

class PluginsDownload(Screen):
    skin = """
<screen name="PluginsDownload" position="left,center" size="1920,1080" title="PluginsDownload">
   <!-- ***** BoHLALA  ***** -->
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="0,0" size="547,950" zPosition="-1" alphatest="blend" transparent="0" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="565,0" size="675,950" zPosition="-1" alphatest="blend" transparent="0" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,550" size="608,60" zPosition="-1" alphatest="blend" />
  <eLabel text="skin designer:by BO-HLALA" position="1224,1260" size="668,39" scale="1" font="Bold; 30" backgroundColor="#ff0000" borderColor="black" borderWidth="4" transparent="1" valign="top" halign="center" foregroundColor="fallback" zPosition="30" />
  <!-- ***** BoHLALA ClockToText ***** -->
  <widget source="global.CurrentTime" render="Label" position="1275,1015" size="598,50" backgroundColor="red" noWrap="1" transparent="1" zPosition="4" font="Bold;30" valign="center" halign="right" cornerRadius="10">
    <convert type="ClockToText">Date</convert>
  </widget>
  <widget name="main_menu" position="27,30" size="507,900" scrollbarMode="showOnDemand" itemHeight="70" scrollbarWidth="0" backgroundColor="#40000000" font="Bold;40" halign="left" render="Listbox" cornerRadius="15" zPosition="6" foregroundColorSelected="#ffbb00" transparent="0" itemCornerRadius="1" itemGradientSelected="#8b898c, un515050, horizontal" itemGradient="transpBlack,#1c1816,horizontal" borderWidth="2" borderColor="black" />
  <widget name="sub_menu" position="576,25" size="653,900" scrollbarMode="showOnDemand" itemHeight="70" scrollbarWidth="fallback" backgroundColor="transpBlack" font="Regular;40" halign="center" zPosition="6" render="Listbox" enableWrapAround="1" foregroundColorSelected="#ff00" transparent="0" cornerRadius="10" itemCornerRadius="1" itemGradientSelected="#8b898c, un515050, horizontal" itemGradient="transpBlack,#1c1816,horizontal" borderWidth="2" borderColor="black" />
  <widget name="status" position="30,960" size="1190,40" font="Regular;30" halign="center" backgroundColor="#303030" valign="bottom" cornerRadius="10" />
  <widget name="key_green" position="27,1021" size="380,48" font="Bold;28" halign="center" backgroundColor="black" foregroundColor="#8000" transparent="1" />
  <widget name="key_yellow" position="437,1021" size="380,48" font="Bold;28" halign="center" backgroundColor="black" foregroundColor="#ffbb00" transparent="1" />
  <widget name="key_blue" position="849,1020" size="378,49" font="Bold;28" halign="center" backgroundColor="black" foregroundColor="#8cff" transparent="1" />
  <widget name="key_exit" position="870,1023" size="260,46" font="Regular;26" halign="center" backgroundColor="#9f1313" />
  <!-- ***** BoHLALA ClockToText ***** -->
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/button_red.png" scale="1" position="414,1283" size="40,40" alphatest="blend" zPosition="100" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/button_green.png" scale="1" position="34,1025" size="40,40" alphatest="blend" zPosition="100" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/button_yellow.png" scale="1" position="442,1025" size="40,40" alphatest="blend" zPosition="100" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/button_blue.png" scale="1" position="855,1025" size="40,40" alphatest="blend" zPosition="100" />
  <!-- ***** BoHLALA  ***** -->
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,616" size="608,60" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,681" size="608,59" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,746" size="608,60" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,811" size="608,60" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,876" size="608,60" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,479" size="608,60" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,942" size="608,60" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1276,1010" size="608,60" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="845,1016" size="389,58" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="23,1016" size="389,58" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="434,1016" size="389,58" zPosition="-1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/BO-hlala.png" scale="1" position="1438,421" size="292,49" zPosition="-1" alphatest="blend" />
  <!-- ***** BoHLALA backgroundColor ***** -->
  <ePixmap position="1505,212" zPosition="0" size="154,202" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BoHLALA_FHD/mySkin/avatar_150.png" alphatest="blend" transparent="1" />
  <widget name="ip_address" position="1264,946" size="598,50" font="Bold;28" halign="right" foregroundColor="selectedFG" zPosition="2" backgroundColor="black" cornerRadius="10" valign="center" transparent="1" />
  <widget name="python_version" position="1454,433" size="260,30" font="Bold;28" halign="center" foregroundColor="white" zPosition="1" cornerRadius="10" backgroundColor="#90000000" transparent="1" />
  <widget name="receiver_model" position="1280,488" size="598,50" font="Bold;40" halign="center" backgroundColor="black" foregroundColor="#e5e5e5" cornerRadius="10" transparent="1" />
  <widget name="image_type" position="1280,560" size="598,50" font="Bold;30" halign="center" backgroundColor="red" foregroundColor="white" cornerRadius="10" transparent="1" />
  <widget name="image_version" position="1280,630" size="598,48" font="Bold;35" halign="center" backgroundColor="red" foregroundColor="white" cornerRadius="10" transparent="1" />
  <widget name="cpu_info" position="1280,691" size="598,50" font="Bold;30" halign="center" backgroundColor="red" foregroundColor="white" cornerRadius="10" transparent="1" />
  <widget name="memory_info" position="1280,755" size="598,50" font="Bold;30" halign="center" backgroundColor="red" foregroundColor="white" cornerRadius="10" transparent="1" />
  <widget name="storage_info" position="1280,820" size="598,50" font="Bold;30" halign="center" backgroundColor="red" foregroundColor="white" cornerRadius="10" transparent="1" />
  <widget name="mount_info" position="1280,886" size="598,50" font="Bold;30" halign="center" backgroundColor="red" foregroundColor="white" cornerRadius="10" transparent="1" />
  <widget name="current_time" position="1355,1017" size="329,50" backgroundColor="red" font="Bold;40" halign="left" transparent="1" zPosition="5" />
  <widget name="internet_status" position="1303,946" size="572,50" backgroundColor="red" font="Bold;30" cornerRadius="10" valign="center" transparent="1" zPosition="9" />
  <!-- ***** BoHLALA  ***** -->
</screen>
    """
# "by-BoHLALA Panels ","Channels",

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.main_menu = ["Skins BoHLALA FHD", "Skins TeamNitro", "Panels", "kiddac", "xtraevent", "Emu",  "Bootlogo", "Key Plugins", "Multiboot Plugins", "Skins Other"]
        self.sub_menus = {
    "Skins BoHLALA FHD": [
    ("BoHLALA Control Panel", """wget -q "--no-check-certificate" https://raw.githubusercontent.com/BoHLALA/Script/K.S.A/installerP.sh -O - | sed 's/\r//' | /bin/sh"""),
    ("BoHLALA_FHD", """wget -q "--no-check-certificate" https://raw.githubusercontent.com/BoHLALA/Script/K.S.A/installerB.sh -O - | sed 's/\r//' | /bin/sh"""),
    ],

#        "by-BoHLALA Panels": [
#        ("byBO-HLALA KiddaC-SkinE2sentials", """wget -q "--no-check-certificate" https://raw.githubusercontent.com/BoHLALA/Script/K.S.A/KiddaC_Skin_E2sentials.sh -O - | sed 's/\r//' | /bin/sh"""),

#        ("byBO-HLALA KiddaC-SkinE2sentials", "wget https://raw.githubusercontent.com/BoHLALA/main/K.S.A/KiddaC_Skin_E2sentials.sh -O - | /bin/sh"),  

#        ("byBO-HLALA KiddaC-SkinE2sentials", "wget https://raw.githubusercontent.com/BoHLALA/Plugins/script/K.S.A/KiddaC_Skin_E2sentials.sh -O - | /bin/sh"),
 
                              
#        ("byBO-HLALA KiddaC-SkinE2sentials", "wget --no-check-certificate -O '/tmp/byBO-HLALA_KiddaC-Skin-E2sentials.tar.gz' 'https://raw.githubusercontent.com/BoHLALA/Plugins/main/byBO-HLALA_KiddaC-Skin-E2sentials.tar.gz"),
                                
#        ("byBO-HLALA KiddaC-SkinE2sentials", "wget https://raw.githubusercontent.com/BoHLALA/Script/K.S.A/KiddaC_Skin_E2sentials.sh -O - | /bin/sh"),        
#        ("kiddac-skin-e2sentials", "wget https://raw.githubusercontent.com/biko-73/kiddac-skin-e2sentials/main/installer.sh -O - | /bin/sh"),  
#        ("byBoHLALA_xtraevent_v3.3", "wget https://raw.githubusercontent.com/BoHLALA/Plugins/main/byBoHLALA_enigma2-plugin-extensions-xtraevent_v3.3.tar.gz -O - | /bin/sh"),
#        ("BouquetMakerXtream", "wget https://raw.githubusercontent.com/biko-73/BouquetMakerXtream/main/installer.sh -O - | /bin/sh"),  
        
#    ],


            "Panels": [
        ("Ajpanel", "wget http://dreambox4u.com/emilnabil237/plugins/ajpanel/installer1.sh -O - | /bin/sh"),
        ("AjPanel Custom Menu All Panels", "wget https://dreambox4u.com/emilnabil237/plugins/ajpanel/emil-panel-all.sh -O - | /bin/sh"),
        ("Panel Lite By Emil Nabil", "wget https://dreambox4u.com/emilnabil237/plugins/ajpanel/new/emil-panel-lite.sh -O - | /bin/sh"),
        ("eliesatpanel", "wget https://raw.githubusercontent.com/eliesat/eliesatpanel/main/installer.sh -qO - | /bin/sh"),
        ("Ciefp-Panel", "wget https://github.com/ciefp/CiefpsettingsPanel/raw/main/installer.sh -O - | /bin/sh"),
        ("Ciefp-Panel mod Emil Nabil", "wget https://github.com/emilnabil/download-plugins/raw/refs/heads/main/Ciefp-Panel/Ciefp-Panel.sh -O - | /bin/sh"),
        ("dreamosat-downloader", "wget https://dreambox4u.com/emilnabil237/plugins/dreamosat-downloader/installer.sh -O - | /bin/sh"),
        ("EliesatPanel", "wget https://raw.githubusercontent.com/eliesat/eliesatpanel/main/installer.sh -O - | /bin/sh"),
        ("Epanel", "wget https://dreambox4u.com/emilnabil237/plugins/epanel/installer.sh -O - | /bin/sh"),
        ("linuxsat-panel", "wget https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/installer.sh -O - | /bin/sh"),
        ("levi45-AddonsManager", "wget https://dreambox4u.com/emilnabil237/plugins/levi45-addonsmanager/installer.sh -O - | /bin/sh"),
        ("Levi45MulticamManager", "wget https://dreambox4u.com/emilnabil237/plugins/levi45multicammanager/installer.sh -O - | /bin/sh"),
        ("MagicPanel-HAMDY_AHMED", "wget https://gitlab.com/h-ahmed/Panel/-/raw/main/MagicPanel-install.sh -O - | /bin/sh"),
        ("SatVenusPanel", "wget https://dreambox4u.com/emilnabil237/plugins/satvenuspanel/installer.sh -O - | /bin/sh"),
        ("Tspanel", "wget https://dreambox4u.com/emilnabil237/plugins/tspanel/installer.sh -O - | /bin/sh"),
        ("TvAddon-Panel", "wget https://dreambox4u.com/emilnabil237/plugins/tvaddon/installer.sh -O - | /bin/sh"),

    ],
        "kiddac": [
#        ("kiddac-skin-e2sentials", "wget https://raw.githubusercontent.com/biko-73/kiddac-skin-e2sentials/main/installer.sh -O - | /bin/sh"),  
        ("xklass", "wget https://dreambox4u.com/emilnabil237/plugins/xklass/installer.sh -qO - | /bin/sh"),
        ("BouquetMakerXtream", "wget https://raw.githubusercontent.com/biko-73/BouquetMakerXtream/main/installer.sh -O - | /bin/sh"),  
        ("xstreamity", "wget https://raw.githubusercontent.com/biko-73/xstreamity/main/installer.sh -O - | /bin/sh"),  
       
  
    ],

        "xtraevent": [
        ("xtraevent_3.3", "wget https://raw.githubusercontent.com/emil237/download-plugins/main/xtraevent_3.3.sh -O - | /bin/sh"), 
        ("xtraevent_4.2", "wget https://raw.githubusercontent.com/emil237/download-plugins/main/xtraEvent_4.2.sh -O - | /bin/sh"),
        ("xtraevent_4.5", "wget https://raw.githubusercontent.com/emil237/download-plugins/main/xtraEvent_4.5.sh -O - | /bin/sh"),
        ("Xtraevent_4.6", "wget https://github.com/emil237/download-plugins/raw/main/Xtraevent-v4.6.sh -O - | /bin/sh"),
        ("xtraevent_6.798", "wget https://dreambox4u.com/emilnabil237/plugins/xtraevent/xtraevent_6.798.sh -O - | /bin/sh"), 
        ("xtraevent_6.805", "wget https://dreambox4u.com/emilnabil237/plugins/xtraevent/xtraevent-6.805.sh -O - | /bin/sh"), 
 
    ],

        "Emu": [
#        ("oscamicam", "wget https://dreambox4u.com/emilnabil237/emu/installer-oscamicam.sh  -O - | /bin/sh"),
        ("Ncam", "wget https://raw.githubusercontent.com/biko-73/Ncam_EMU/main/installer.sh  -O - | /bin/sh"),
        ("OsCam", "wget https://raw.githubusercontent.com/biko-73/OsCam_EMU/main/installer.sh  -O - | /bin/sh"),
        ("Oscamicam", "wget https://raw.githubusercontent.com/biko-73/OsCam_EMU/main/installericam.sh  -O - | /bin/sh"),
        ("Oscam-11.726", "wget https://dreambox4u.com/emilnabil237/emu/oscam-by-lenuxsat/installer.sh  -O - | /bin/sh"),
        ("Oscam", "wget https://dreambox4u.com/emilnabil237/emu/installer-oscam.sh  -O - | /bin/sh"),
#        ("Ncam", "wget https://dreambox4u.com/emilnabil237/emu/installer-ncam.sh -O - | /bin/sh"),        
        ("Cccam", "wget https://dreambox4u.com/emilnabil237/emu/installer-cccam.sh  -O - | /bin/sh"),
        ("gosatplus-ncam", "wget https://dreambox4u.com/emilnabil237/emu/installer-gosatplus-ncam.sh  -O - | /bin/sh"),
        ("gosatplus-oscam", "wget https://dreambox4u.com/emilnabil237/emu/installer-gosatplus-oscam.sh  -O - | /bin/sh"),
        ("gosatplus_v3_arm", "wget http://e2.gosatplus.com/Plugin/V3/arm-openpli-installer_py3_v3.sh  -O - | /bin/sh"),
        ("gosatplus_v3_mips", "wget http://e2.gosatplus.com/Plugin/V3/mips-openpli-installer_py3_v3.sh  -O - | /bin/sh"),
        ("gosatplus_v3_Fix", "wget http://e2.gosatplus.com/Plugin/V3/GosatPlusPluginFixPy.sh  -O - | /bin/sh"),
        ("Hold-flag-ncam", "opkg flag hold enigma2-plugin-softcams-ncam"),
        ("Hold-flag-Oscam", "opkg flag hold enigma2-plugin-softcams-oscam"),
        ("powercam_v2-icam-arm", "wget https://dreambox4u.com/emilnabil237/emu/powercam/installer.sh  -O - | /bin/sh"),
        ("powercam-Ncam", "wget https://dreambox4u.com/emilnabil237/emu/installer-powercam-ncam.sh  -O - | /bin/sh"),
        ("powercam-Oscam", "wget https://dreambox4u.com/emilnabil237/emu/installer-powercam-oscam.sh  -O - | /bin/sh"),
        ("Restore-flag-ncam", "opkg flag user enigma2-plugin-softcams-ncam"),
        ("Restore-flag-oscam", "opkg flag user enigma2-plugin-softcams-oscam"),
        ("Revcam-Ncam", "wget https://dreambox4u.com/emilnabil237/emu/installer-revcam-ncam.sh  -O - | /bin/sh"),
        ("Revcam-Oscam", "wget https://dreambox4u.com/emilnabil237/emu/installer-revcam-oscam.sh  -O - | /bin/sh"),
        ("Revcam", "wget https://dreambox4u.com/emilnabil237/emu/installer-revcam.sh  -O - | /bin/sh"),
        ("Supcam-Ncam", "wget https://dreambox4u.com/emilnabil237/emu/installer-supcam-ncam.sh  -O - | /bin/sh"),
        ("Supcam-Oscam", "wget https://dreambox4u.com/emilnabil237/emu/installer-supcam-oscam.sh  -O - | /bin/sh"),
        ("Ultracam-Ncam", "wget https://dreambox4u.com/emilnabil237/emu/installer-ultracam-ncam.sh  -O - | /bin/sh"),
        ("Ultracam-Oscam", "wget https://dreambox4u.com/emilnabil237/emu/installer-ultracam-oscam.sh  -O - | /bin/sh"),
        ("Ultracam", "wget https://dreambox4u.com/emilnabil237/emu/installer-ultracam.sh  -O - | /bin/sh"),
    ],
    "Bootlogo": [
        ("BootlogoSwapper Atv", "wget http://dreambox4u.com/emilnabil237/script/bootlogoswapper-Atv.sh  -O - | /bin/sh"),
        ("Bootlogo-PURE2", "wget http://dreambox4u.com/emilnabil237/script/bootLogoswapper-Pure2.sh  -O - | /bin/sh"),
        ("BootlogoSwapper Christmas", "wget http://dreambox4u.com/emilnabil237/script/bootlogoswapper-christmas.sh -O - | /bin/sh"),
        ("BootlogoSwapper Pli", "wget http://dreambox4u.com/emilnabil237/script/bootlogoswapper-pli.sh -O - | /bin/sh"),
        ("BootlogoSwapper OpenBH", "wget http://dreambox4u.com/emilnabil237/script/bootlogoswapper-OpenBH.sh  -O - | /bin/sh"),
        ("BootlogoSwapper Egami", "wget http://dreambox4u.com/emilnabil237/script/bootLogoswapper-Egami.sh -O - | /bin/sh"),
        ("BootlogoSwapper OpenVix", "wget http://dreambox4u.com/emilnabil237/script/bootlogoswapper-OpenVix.sh  -O - | /bin/sh"),
        ("BootlogoSwapper Kids", "wget http://dreambox4u.com/emilnabil237/script/bootlogoswapper-kids.sh -O - | /bin/sh"),
        ("BootlogoSwapper Ramadan", "wget http://dreambox4u.com/emilnabil237/script/bootlogo-swapper-ramadan.sh  -O - | /bin/sh"),
        ("BootlogoSwapper Eid-Aldha", "wget http://dreambox4u.com/emilnabil237/script/bootlogoswaper-Eid-Aldha.sh -O - | /bin/sh"),
        ("BootlogoSwapper V2.1", "wget http://dreambox4u.com/emilnabil237/script/BootlogoSwapper_v2.1.sh  -O - | /bin/sh"),
        ("BootlogoSwapper V2.3", "wget http://dreambox4u.com/emilnabil237/script/BootlogoSwapper_v2.3.sh  -O - | /bin/sh"),

    ],
#    "Channels": [
#        ("Elsafty-Tv-Radio-Steaming", "wget https://dreambox4u.com/emilnabil237/settings/elsafty/installer.sh -O - | /bin/sh"),
#        ("Khaled Ali", "wget https://raw.githubusercontent.com/emilnabil/channel-khaled/main/installer.sh -qO - | /bin/sh"),
#        ("Mohamed Goda", "wget https://raw.githubusercontent.com/emilnabil/channel-mohamed-goda/main/installer.sh  -O - | /bin/sh"),
#        ("Emil Nabil", "wget https://raw.githubusercontent.com/emilnabil/channel-emil-nabil/main/installer.sh -O - | /bin/sh"),
#        ("Mohamed Os", "wget https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Settings_Enigma2/online-setup | bash"),
#        ("Tarek Ashry", "wget https://raw.githubusercontent.com/emilnabil/channel-tarek-ashry/main/installer.sh -qO - | /bin/sh"),
#    ],

    "Key Plugins": [
        ("BissFeedAutoKey", "wget https://raw.githubusercontent.com/emilnabil/bissfeed-autokey/main/installer.sh  -O - | /bin/sh"),
        ("feeds-finder", "wget https://dreambox4u.com/emilnabil237/plugins/feeds-finder/installer.sh  -O - | /bin/sh"),
        ("KeyAdder", "wget https://dreambox4u.com/emilnabil237/plugins/KeyAdder/installer.sh -O - | /bin/sh"),
    ],
    "Multiboot Plugins": [
        ("EgamiBoot_10.5", "wget https://raw.githubusercontent.com/emil237/egamiboot/refs/heads/main/installer.sh  -O - | /bin/sh"),
        ("EgamiBoot_10.6", "wget https://raw.githubusercontent.com/emil237/egamiboot/refs/heads/main/egamiboot-10.6.sh -O - | /bin/sh"),
        ("Neoboot_9.65", "wget https://dreambox4u.com/emilnabil237/plugins/neoboot-v9.65/iNB.sh  -O - | /bin/sh"),
        ("Neoboot_9.65_Mod-By-ElSafty", "wget https://raw.githubusercontent.com/emil237/neoboot_v9.65/main/iNB_9.65_mod-elsafty.sh  -O - | /bin/sh"),
        ("Neoboot_9.60", "wget https://dreambox4u.com/emilnabil237/plugins/neoboot-v9.60/iNB.sh  -O - | /bin/sh"),
        ("Neoboot_9.58", "wget https://dreambox4u.com/emilnabil237/plugins/neoboot-v9.58/iNB.sh -O - | /bin/sh"),
        ("Neoboot_9.54", "wget https://raw.githubusercontent.com/emil237/neoboot_9.54/main/installer.sh  -O - | /bin/sh"),
        ("OpenMultiboot_1.3", "wget https://raw.githubusercontent.com/emil237/openmultiboot/main/installer.sh  -O - | /bin/sh"),
        ("OpenMultiboot-E2turk", "wget https://raw.githubusercontent.com/e2TURK/omb-enhanced/main/install.sh  -O - | /bin/sh"),
        ("Multiboot-FlashOnline", "wget https://raw.githubusercontent.com/emil237/download-plugins/main/multiboot-flashonline.sh -O - | /bin/sh"),
    ],
    "Skins Other": [
        ("Aglare-FHD for Atv-Spa-Egami", "wget https://raw.githubusercontent.com/popking159/skins/refs/heads/main/aglareatv/installer.sh -O - | /bin/sh"),
        ("Aglare-FHD for Pli-OBH-Vix", "wget https://raw.githubusercontent.com/popking159/skins/refs/heads/main/aglarepli/installer.sh -O - | /bin/sh"),
        ("XDreamy-FHD", "wget https://raw.githubusercontent.com/Insprion80/Skins/main/xDreamy/installer.sh -O - | /bin/sh"),
    ],
    "Skins TeamNitro": [
        ("TeamNitro Control", "wget https://gitlab.com/emilnabil1/teamnitro/-/raw/main/SKIN-teamnitro.sh -O - | /bin/sh"),
        ("Al Ayam FHD", "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerAL.sh -O - | /bin/sh"),
        ("Desert-FHD", "wget https://gitlab.com/emilnabil1/teamnitro/-/raw/main/installer-skin-desert.sh -O - | /bin/sh"),
        ("Dragon FHD", "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerD.sh -O - | /bin/sh"),
        ("NitroAdvance-FHD", "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerN.sh -O - | /bin/sh"),
        ("Klll-Pro-FHD", "wget https://raw.githubusercontent.com/biko-73/zelda77/main/installer.sh -O - | /bin/sh"),
    ],

 }
        self.current_sub_menu = []
        self.selected_plugins = []
        self.focus = "main_menu"
        self["main_menu"] = MenuList(self.main_menu)
        self["sub_menu"] = MenuList(self.current_sub_menu)
        self["status"] = Label("Select a category to view items")
        self["key_green"] = Button("Install")
        self["key_yellow"] = Button("Update Plugin")
        self["key_blue"] = Button("Restart Enigma2")
        self["key_cancel"] = Button("Exit")
        self["ip_address"] = Label(self.get_router_ip())
        self["python_version"] = Label(self.get_python_version())
        self["receiver_model"] = Label(self.get_receiver_model())
        self["image_type"] = Label(self.get_image_type())
        self["image_version"] = Label(self.get_image_version())
        self["cpu_info"] = Label(self.get_cpu_info())
        self["memory_info"] = Label(self.get_memory_info())
        self["storage_info"] = Label(self.get_storage_info())
        self["mount_info"] = Label(self.get_mount_info())
        self["internet_status"] = Label(self.get_internet_status())
        self["current_time"] = Label("")
        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions", "ColorActions"],
            {
                "ok": self.handle_ok,
                "left": self.focus_main_menu,
                "right": self.focus_sub_menu,
                "cancel": self.exit,
                "green": self.execute_all_selected_plugins,
                # "yellow": self.update_plugin,
                "blue": self.restart_enigma2,
                "up": self.navigate_up,
                "down": self.navigate_down,
            },
            -1,
        )
        self["main_menu"].onSelectionChanged.append(self.load_sub_menu)

        self.timer = eTimer()
        self.timer.timeout.get().append(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        import time
        current_time = time.strftime("%H:%M:%S")
        self["current_time"].setText(current_time)

    def get_router_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except socket.error:
            return "IP not available"

    def get_python_version(self):
        return f"Python {os.sys.version.split()[0]}"

    def get_receiver_model(self):
        try:
            with os.popen("cat /etc/hostname") as f:
                return f.read().strip()
        except Exception:
            return "Unknown Model"

    def get_image_type(self):
        try:
            with os.popen("grep -iF 'creator' /etc/image-version") as f:
                return f.read().strip().replace("creator", "Image")
        except Exception:
            return "Unknown Image"

    def get_image_version(self):
        try:
            with os.popen("grep -iF 'version' /etc/image-version") as f:
                return f.read().strip()
        except Exception:
            return "Unknown Version"

    def get_cpu_info(self):
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except:
            return "Unknown CPU"

    def get_memory_info(self):
        try:
            with open("/proc/meminfo") as f:
                mem_total = mem_free = 0
                for line in f:
                    if "MemTotal" in line:
                        mem_total = int(line.split()[1]) // 1024
                    elif "MemFree" in line:
                        mem_free = int(line.split()[1]) // 1024
                return f"Ram: {mem_total} MB, Free: {mem_free} MB"
        except:
            return "Unknown Memory Info"

    def get_storage_info(self):
        try:
            statvfs = os.statvfs("/")
            total_storage = (statvfs.f_blocks * statvfs.f_frsize) // (1024 * 1024)
            free_storage = (statvfs.f_bfree * statvfs.f_frsize) // (1024 * 1024)
            return f"HDD: {total_storage} MB, Free: {free_storage} MB"
        except:
            return "Unknown Storage Info"

    def get_mount_info(self):
        try:
            mount_point = "/media/hdd"
            if os.path.exists(mount_point):
                return f"Mount = {mount_point}"
            else:
                return "Mount = Not Found"
        except:
            return "Mount = Unknown"

    def get_internet_status(self):
        return "INTERNET : Connected" if os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1") == 0 else "INTERNET : No Connection"

    def focus_main_menu(self):
        self.focus = "main_menu"
        self["main_menu"].selectionEnabled(1)
        self["sub_menu"].selectionEnabled(0)

    def focus_sub_menu(self):
        if self.current_sub_menu:
            self.focus = "sub_menu"
            self["main_menu"].selectionEnabled(0)
            self["sub_menu"].selectionEnabled(1)

    def handle_ok(self):
        if self.focus == "main_menu":
            self.load_sub_menu()
        elif self.focus == "sub_menu":
            self.execute_item()

    def load_sub_menu(self):
        selected = self["main_menu"].getCurrent()
        if selected and selected in self.sub_menus:
            self.current_sub_menu = [item[0] for item in self.sub_menus[selected]]
            self["sub_menu"].setList(self.current_sub_menu)
            self["status"].setText(f"Selected category: {selected}")
            self["main_menu"].selectionEnabled(1)
            self["sub_menu"].selectionEnabled(0)

    def navigate_up(self):
        if self.focus == "main_menu":
            self["main_menu"].up()
        elif self.focus == "sub_menu":
            self["sub_menu"].up()

    def navigate_down(self):
        if self.focus == "main_menu":
            self["main_menu"].down()
        elif self.focus == "sub_menu":
            self["sub_menu"].down()

    def execute_item(self):
        if self.focus == "sub_menu":
            selected = self["sub_menu"].getCurrent()
            if selected:
                for item in self.sub_menus.get(self["main_menu"].getCurrent(), []):
                    if item[0] == selected:
                        if not any(plugin[0] == selected for plugin in self.selected_plugins):
                            self.selected_plugins.append((selected, item[1]))
                            self["status"].setText(f"Selected plugins: {len(self.selected_plugins)}")
                        else:
                            self["status"].setText(f"Plugin '{selected}' is already selected.")
                        break

    def execute_all_selected_plugins(self):
        if self.selected_plugins:
            self.session.open(InstallProgressScreen, self.selected_plugins)
            self.selected_plugins = []
            self["status"].setText("Plugins installation started...")
        else:
            self["status"].setText("No plugins selected for installation.")

    def restart_enigma2(self):
        os.system("killall -9 enigma2")

    def exit(self):
        self.close()
