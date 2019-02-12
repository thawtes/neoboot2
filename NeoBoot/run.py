#!/usr/bin/python
# -*- coding: utf-8 -*-  
                               
from __init__ import _
from Plugins.Extensions.NeoBoot.files import Harddisk                                                                                                                                                     
from Plugins.Extensions.NeoBoot.files.stbbranding import getKernelVersionString, getKernelImageVersion, getCPUtype, getCPUSoC,  getImageNeoBoot, getBoxVuModel, getBoxHostName, getTunerModel
from enigma import getDesktop
from enigma import eTimer
from Screens.Screen import Screen                                                                                                                                               
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
from Components.About import about
from Components.Sources.List import List
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.GUIComponent import *
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen
from os.path import dirname, isdir, isdir as os_isdir
import os
import time


class StartImage(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="center, center" size="1241, 850" title="NeoBoot">
        \n\t\t\t<ePixmap position="491, 673" zPosition="-2" size="365, 160" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" />
        <widget source="list" render="Listbox" position="20, 171" size="1194, 290" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
        \n                    \t\t\t],
        \n                    \t\t\t"fonts": [gFont("Regular", 40)],\n                    \t\t\t"itemHeight": 66\n                \t\t}
        \n            \t\t</convert>\n\t\t</widget>
        \n         <widget name="label1" position="21, 29" zPosition="1" size="1184, 116" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        <widget name="label2" position="22, 480" zPosition="-2" size="1205, 168" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        </screen>"""
    else:
        skin = """<screen position="center, center" size="835, 500" title="NeoBoot">
        \n\t\t\t           <ePixmap position="0,0" zPosition="-1" size="835,500" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame835x500.png"  />
        <widget source="list" render="Listbox" position="16, 150" size="800, 40"    selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/listselection800x35.png" scrollbarMode="showOnDemand">
        \n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (180, 0), size = (520, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),
        \n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 22)],
        \n                    \t\t\t"itemHeight": 35\n               \t\t}\n            \t\t</convert>
        \n\t\t</widget>\n<widget name="label1" font="Regular; 26" position="15, 70" size="803, 58" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />
        <widget name="label2" position="40, 232" zPosition="2" size="806, 294" font="Regular;25" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />
        \n\t\t        </screen>"""

    __module__ = __name__
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.select()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})
        self['label1'] = Label(_('Start the chosen system now ?'))
        self['label2'] = Label(_('Select OK to run the image.'))
        
    def select(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('OK Start image...'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

#################################
    def KeyOk(self): 
        if getImageNeoBoot() != 'Flash': 
            cmd = _("echo -e '[NeoBoot] Uwaga!!! po poprawnym starcie wybranego oprogramowania w neoboot,\nnalezy uruchomic NEOBOOTA by potwierdzic prawidlowy start image.\n\nNacisnij OK lub exit na pilocie by kontynuowac...\n\n\n'") 
            self.session.openWithCallback(self.StartImageInNeoBoot, Console, _('NeoBoot: Start image...'), [cmd])
        else:
            self.StartImageInNeoBoot()

    def StartImageInNeoBoot(self):                              
        if fileExists('/media/neoboot/ImageBoot/%s/.control_ok' % ( getImageNeoBoot())):
            system('touch /tmp/.control_ok ') 
        else:
                system('touch /media/neoboot/ImageBoot/%s/.control_boot_new_image ' % ( getImageNeoBoot()))

####################################
        system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/*')               
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]     
        if self.sel == 0:          
            if fileExists('/media/mmc/etc/init.d/neobootmount.sh'):
                os.system('rm -f /media/mmc/etc/init.d/neobootmount.sh;')

            #DM900; Zgemma h7S; AX HD60 4K                      
            if getCPUSoC() == 'hi3798mv200' or getBoxHostName == 'ax60' or getCPUSoC() == '3798mv200' or getBoxHostName() == 'sf8008' or getCPUSoC() == 'bcm7251s' or getBoxHostName() == 'h7' or getCPUSoC() == 'BCM97252SSFF' or getBoxHostName() == 'dm900':                  
                        if getImageNeoBoot() == 'Flash':                    
                            if fileExists('/.multinfo'):   
                                os.system('cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init; reboot -d -f -h -i')                 
                            elif not fileExists('/.multinfo'):                                  
                                os.system('ln -sfn /sbin/init.sysvinit /sbin/init; reboot -d -f -h -i')
                        elif getImageNeoBoot() != 'Flash':                     
                                os.system('ln -sfn /sbin/neoinitarm /sbin/init; reboot -d -f -h -i')                                                          
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że multiboot nie wspiera tego modelu STB !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

            #MiracleBox, ET8500, Formuler F1, Formuler F3, Atemio6000 - MIPS                                                                                                                                                                       # test -  ultra, osmini 
            elif getCPUtype() != 'ARMv7' and getCPUSoC() == 'bcm7358' or getCPUSoC() == 'bcm7362' or getCPUSoC() == 'bcm7356' or getCPUSoC() == 'bcm7241' or getCPUSoC() == 'bcm7362' or getBoxHostName() == 'mbmini' or getBoxHostName() == 'h3'  or getTunerModel() == 'ini-1000sv':  #or getBoxHostName == 'mbultra'  or getCPUSoC() == 'BCM7362' or getBoxHostName() == 'osmini'                                 
                        if getImageNeoBoot() == 'Flash':                                        
                            self.session.open(TryQuitMainloop, 2)
                        elif getImageNeoBoot() != 'Flash':                     
                                cmd='ln -sfn /sbin/neoinitmips /sbin/init; reboot -d -f -h -i' 
                                self.session.open(Console, _('NeoBoot ....'), [cmd])                                                         
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że multiboot nie wspiera tego modelu STB !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()



            #MiracleBox Ultra - MIPS  #Test 
            elif getCPUtype() != 'ARMv7' and getCPUSoC() == 'bcm7424' or getTunerModel() == 'ini-8000sv':                                                                                 

                        if getImageNeoBoot() == 'Flash':                    
                            if fileExists('/.multinfo'):  
                                cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/mbultra_dev_mtd2.sh' 
                                self.session.open(Console, _('NeoBoot MiracleBox Ultra...'), [cmd2])                 
                            elif not fileExists('/.multinfo'):  
                                self.session.open(TryQuitMainloop, 2)                                                                    

                        elif getImageNeoBoot() != 'Flash':                    
                            if not fileExists('/.multinfo'):                        
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz ' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd2='ln -sfn /sbin/neoinitmips /sbin/init; reboot -d -f -h -i' 
                                    self.session.open(Console, _('NeoBoot MiracleBox Ultra Rebooting....'), [cmd2])                                                                                                    
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):                                              
                                    cmd2='ln -sfn /sbin/neoinitmips /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/mbultra_dev_mtd2.sh' 
                                    self.session.open(Console, _('NeoBoot MiracleBox Ultra....'), [cmd2])              

                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd2='ln -sfn /sbin/init.sysvinit /sbin/init; opkg install --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' % getBoxHostName() 
                                    self.session.open(Console, _('NeoBoot MiracleBox Ultra Rebooting....'), [cmd2])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd2='ln -sfn /sbin/init.sysvinit /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/mbultra_dev_mtd2.sh'
                                    self.session.open(Console, _('NeoBoot MiracleBox Ultra....'), [cmd2])

                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez multiboota!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()
                            
                            
            #Edision OS MINI  - MIPS #Test   
            elif getCPUtype() != 'ARMv7' and getCPUSoC() == 'BCM7362' or getBoxHostName() == 'osmini':                                      
                        if getImageNeoBoot() == 'Flash':                    
                            if fileExists('/.multinfo'):  
                                cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/osmini_dev_mtd0.sh' 
                                self.session.open(Console, _('NeoBoot Arm....'), [cmd2])                 
                            elif not fileExists('/.multinfo'):  
                                self.session.open(TryQuitMainloop, 2)                                      
                        elif getImageNeoBoot() != 'Flash':                    
                            if not fileExists('/.multinfo'):                        
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd2='ln -sfn /sbin/neoinitmips /sbin/init; reboot -d -f -h -i' 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])                                                                                                    
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):                                              
                                    cmd2='ln -sfn /sbin/neoinitmips /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/osmini_dev_mtd0.sh' 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])              
                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd2='opkg install --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' % getBoxHostName() 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/osmini_dev_mtd0.sh'
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez multiboota!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()
                                                        
            #Octagon SF4008 ARM                                                        
            elif getCPUSoC() == 'bcm7251' or getBoxHostName() == 'sf4008' :
                        if getImageNeoBoot() == 'Flash':                                               
                            if fileExists('/.multinfo'):                                                                
                                cmd1='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/sf4008_mmcblk0p3.sh'                  
                                self.session.open(Console, _('NeoBoot Octagon SF4008 ARM ...'), [cmd1])
                            elif not fileExists('/.multinfo'):                                                                                             
                                self.session.open(TryQuitMainloop, 2)                                             
                        elif getImageNeoBoot() != 'Flash':                                                 
                            if not fileExists('/.multinfo'):  
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):   
                                    cmd1='ln -sfn /sbin/neoinitarm /sbin/init; reboot -d -f -h -i'  
                                    self.session.open(Console, _('NeoBoot Octagon SF4008 ARM ....'), [cmd1])   
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):     
                                    cmd1='ln -sfn /sbin/neoinitarm /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/sf4008_mmcblk0p3.sh'                   
                                    self.session.open(Console, _('NeoBoot Octagon SF4008 ARM ....'), [cmd1])
                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd1='cd /media/mmc; ln -sf /sbin/init.sysvinit /media/mmc/sbin/init; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' %  getBoxHostName()
                                    self.session.open(Console, _('NeoBoot Octagon SF4008 ARM ....'), [cmd1])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd1='cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/sf4008_mmcblk0p3.sh'                                                                                      
                                    self.session.open(Console, _('NeoBoot Octagon SF4008 ARM ....'), [cmd1])
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że Twój model STB nie jest wpierany!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()
                            
            #Zgemma h7S ARM                                                        
            elif getCPUSoC() == 'bcm7251s' or getBoxHostName() == 'h7' :
                        if getImageNeoBoot() == 'Flash':                                               
                            if fileExists('/.multinfo'):                                                                
                                cmd1='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_mmcblk0p2.sh'                  
                                self.session.open(Console, _('NeoBoot Zgemma h7S ARM ...'), [cmd1])
                            elif not fileExists('/.multinfo'):                                                                                             
                                self.session.open(TryQuitMainloop, 2)                                             
                        elif getImageNeoBoot() != 'Flash':                                                 
                            if not fileExists('/.multinfo'):  
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):   
                                    cmd1='ln -sfn /sbin/neoinitarm /sbin/init; reboot -d -f -h -i'  
                                    self.session.open(Console, _('NeoBoot Zgemma h7S ARM ....'), [cmd1])   
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):     
                                    cmd1='ln -sfn /sbin/neoinitarm /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_mmcblk0p2.sh'                   
                                    self.session.open(Console, _('NeoBoot Zgemma h7S ARM ....'), [cmd1])
                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd1='cd /media/mmc; ln -sf /sbin/neoinitarm /media/mmc/sbin/init; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' %  getBoxHostName()
                                    self.session.open(Console, _('NeoBoot Zgemma h7S ARM ....'), [cmd1])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):
                                    cmd1='cd /media/mmc; ln -sfn /sbin/neoinitarm /media/mmc/sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_mmcblk0p2.sh'                                                                                      
                                    self.session.open(Console, _('NeoBoot Zgemma h7S ARM ....'), [cmd1])
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że Twój model STB nie jest wpierany!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

            #VUPLUS ARM - vu_mmcblk0p1.sh                                                        
            elif getCPUSoC() == '7444s' or getBoxHostName() == 'vuultimo4k' or getCPUSoC() == '7376' or getBoxHostName() == 'vusolo4k' or getCPUSoC() == '7252s' or getBoxHostName() == 'vuuno4kse': 
                        if getImageNeoBoot() == 'Flash':                                               
                            if fileExists('/.multinfo'):                                                                
                                cmd1='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p1.sh'                  
                                self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                            elif not fileExists('/.multinfo'):                                                                                             
                                self.session.open(TryQuitMainloop, 2)                                             
                        elif getImageNeoBoot() != 'Flash':                                                 
                            if not fileExists('/.multinfo'):  
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):   
                                    cmd1='ln -sfn /sbin/neoinitarm /sbin/init; reboot -d -f -h -i'  
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])   
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):     
                                    cmd1='ln -sfn /sbin/neoinitarmvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p1.sh'                   
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='cd /media/mmc; ln -sf /sbin/neoinitarm /media/mmc/sbin/init; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' %  getBoxVuModel()
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='cd /media/mmc; ln -sfn /sbin/neoinitarmvu /media/mmc/sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p1.sh'                                                                                      
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że Twój model STB nie jest wpierany!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()
                         
            #VUPLUS ARM - vu_mmcblk0p4.sh                                                       
            elif getCPUSoC() == '72604' or getBoxHostName() == 'vuzero4k': 
                        if getImageNeoBoot() == 'Flash':                                               
                            if fileExists('/.multinfo'):                                                                
                                cmd1='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p4.sh'                  
                                self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                            elif not fileExists('/.multinfo'):                                                                                             
                                self.session.open(TryQuitMainloop, 2)                                             
                        elif getImageNeoBoot() != 'Flash':                                                 
                            if not fileExists('/.multinfo'):  
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):   
                                    cmd1='ln -sfn /sbin/neoinitarm /sbin/init; reboot -d -f -h -i'  
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])   
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):     
                                    cmd1='ln -sfn /sbin/neoinitarmvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p4.sh'                   
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='cd /media/mmc; ln -sf /sbin/neoinitarm /media/mmc/sbin/init; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' %  getBoxVuModel()
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='cd /media/mmc; ln -sfn /sbin/neoinitarmvu /media/mmc/sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p4.sh'                                                                                      
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że Twój model STB nie jest wpierany!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

            #VUPLUS ARM - Duo4k.sh                                                      
            elif getCPUSoC() == '7278' or getBoxHostName() == 'vuduo4k': 
                        if getImageNeoBoot() == 'Flash':                                               
                            if fileExists('/.multinfo'):                                                                
                                cmd1='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p6.sh'                  
                                self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                            elif not fileExists('/.multinfo'):                                                                                             
                                self.session.open(TryQuitMainloop, 2)                                             
                        elif getImageNeoBoot() != 'Flash':                                                 
                            if not fileExists('/.multinfo'):  
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):   
                                    cmd1='ln -sfn /sbin/neoinitarm /sbin/init; reboot -d -f -h -i'  
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])   
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):     
                                    cmd1='ln -sfn /sbin/neoinitarmvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p6.sh'                   
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='cd /media/mmc; ln -sf /sbin/neoinitarm /media/mmc/sbin/init; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' %  getBoxVuModel()
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='cd /media/mmc; ln -sfn /sbin/neoinitarmvu /media/mmc/sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p6.sh'                                                                                      
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że Twój model STB nie jest wpierany!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

            #VUPLUS MIPS  mtd2            
            elif getCPUSoC() == '7356' or getCPUSoC() == '7429' or getCPUSoC() == '7424'  or getCPUSoC() == '7241' or getCPUSoC() == '7362' or getBoxHostName() == 'vusolo2' or getBoxHostName() == 'vusolose'  or getBoxHostName() == 'vuduo2' or getBoxHostName() == 'vuzero':
                        if getImageNeoBoot() == 'Flash':                    
                            if fileExists('/.multinfo'):  
                                cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd2.sh' 
                                self.session.open(Console, _('NeoBoot MIPS...'), [cmd2])                 
                            elif not fileExists('/.multinfo'):  
                                self.session.open(TryQuitMainloop, 2)                                      
                        elif getImageNeoBoot() != 'Flash':                    
                            if not fileExists('/.multinfo'):                        
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='ln -sfn /sbin/neoinitmips /sbin/init; reboot -d -f -h -i' 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])                                                                                                    
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):                                              
                                    cmd2='ln -sfn /sbin/neoinitmipsvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd2.sh' 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])              
                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='opkg install --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' % getBoxVuModel() 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd2.sh'
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez multiboota!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()


            #VUPLUS MIPS mtd1              
            elif getCPUSoC() == '7335'  or getCPUSoC() == '7325' or getCPUSoC() == '7405' or getCPUSoC() == '7405(with 3D)' or getBoxHostName() == 'vuultimo' or getBoxHostName() == 'bm750' or getBoxHostName() == 'duo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuduo':                                                  
                        if getImageNeoBoot() == 'Flash':                    
                            if fileExists('/.multinfo'):  
                                cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd1.sh' 
                                self.session.open(Console, _('NeoBoot MIPS...'), [cmd2])                 
                            elif not fileExists('/.multinfo'):  
                                self.session.open(TryQuitMainloop, 2)                                      
                        elif getImageNeoBoot() != 'Flash':                    
                            if not fileExists('/.multinfo'):                        
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='ln -sfn /sbin/neoinitmips /sbin/init; reboot -d -f -h -i' 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])                                                                                                    
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):                                              
                                    cmd2='ln -sfn /sbin/neoinitmipsvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd1.sh' 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])              
                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='opkg install --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; reboot -d -f -h -i' % getBoxVuModel() 
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd1.sh'
                                    self.session.open(Console, _('NeoBoot Arm....'), [cmd2])
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez multiboota!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

            else:
                os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez NEOBOOT !!! '), MessageBox.TYPE_INFO, 8)
                self.close()           
                
