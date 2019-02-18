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

    def KeyOk(self): 
        if getImageNeoBoot() != 'Flash': 
            if not fileExists('/media/neoboot/ImageBoot/%s/.control_ok' % ( getImageNeoBoot())):
                cmd = _("echo -e '[NeoBoot] Uwaga!!! po poprawnym starcie wybranego oprogramowania w neoboot,\nnalezy uruchomic NEOBOOTA by potwierdzic prawidlowy start image.\n\nNacisnij OK lub exit na pilocie by kontynuowac...\n\n\n'") 
                self.session.openWithCallback(self.StartImageInNeoBoot, Console, _('NeoBoot: Start image...'), [cmd])
            else:
                self.StartImageInNeoBoot()
        else:
            self.StartImageInNeoBoot()

    def StartImageInNeoBoot(self):                              
        if fileExists('/media/neoboot/ImageBoot/%s/.control_ok' % ( getImageNeoBoot())):
            system('touch /tmp/.control_ok ') 
        else:
                system('touch /media/neoboot/ImageBoot/%s/.control_boot_new_image ' % ( getImageNeoBoot()))

        system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/*')               
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]     
        if self.sel == 0:          
            if fileExists('/media/mmc/etc/init.d/neobootmount.sh'):
                os.system('rm -f /media/mmc/etc/init.d/neobootmount.sh;')

            #DM900; AX HD60 4K                      
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
            elif getCPUtype() != 'ARMv7' and getCPUSoC() == 'bcm7358' or getCPUSoC() == 'bcm7362' or getCPUSoC() == 'bcm7356' or getCPUSoC() == 'bcm7241' or getCPUSoC() == 'bcm7362' or getBoxHostName() == 'mbmini' or getBoxHostName() == 'h3'  or getTunerModel() == 'ini-1000sv':  #or getCPUSoC() == 'bcm7424' or getTunerModel() == 'ini-8000sv' or getBoxHostName() == 'osmini'                                 
                        if getImageNeoBoot() == 'Flash':                                        
                            self.session.open(TryQuitMainloop, 2)
                        elif getImageNeoBoot() != 'Flash':                     
                                cmd='ln -sfn /sbin/neoinitmips /sbin/init; reboot -d -f -h -i' 
                                self.session.open(Console, _('NeoBoot ....'), [cmd])                                                         
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że multiboot nie wspiera tego modelu STB !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

            elif getCPUtype() == 'MIPS' and getCPUSoC() == 'BCM7362' or getBoxHostName() == 'osmini'  or getCPUSoC() == 'bcm7424' or getTunerModel() == 'ini-8000sv' or getCPUSoC() == '7356' or getCPUSoC() == '7429' or getCPUSoC() == '7424'  or getCPUSoC() == '7241' or getCPUSoC() == '7362' or getBoxHostName() == 'vusolo2' or getBoxHostName() == 'vusolose'  or getBoxHostName() == 'vuduo2' or getBoxHostName() == 'vuzero' or getCPUSoC() == '7335'  or getCPUSoC() == '7325' or getCPUSoC() == '7405' or getCPUSoC() == '7405(with 3D)' or getBoxHostName() == 'vuultimo' or getBoxHostName() == 'bm750' or getBoxHostName() == 'duo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuduo':                                
                restartbox = self.session.openWithCallback(self.selectboot, MessageBox, _('Wybierz Tak, start image z podmiana kernel lub Nie bez wczytywania kernel.'), MessageBox.TYPE_YESNO)
                restartbox.setTitle(_('Full restart GUI now ?'))

            elif getCPUtype() == 'ARMv7' and getCPUSoC() == 'bcm7251s' or getBoxHostName() == 'h7'or getCPUSoC() == 'bcm7251' or getBoxHostName() == 'sf4008' or getCPUSoC() == '7278' or getBoxHostName() == 'vuduo4k' or getCPUSoC() == '72604' or getBoxHostName() == 'vuzero4k' or getCPUSoC() == '7444s' or getBoxHostName() == 'vuultimo4k' or getCPUSoC() == '7376' or getBoxHostName() == 'vusolo4k' or getCPUSoC() == '7252s' or getBoxHostName() == 'vuuno4kse':
                restartbox = self.session.openWithCallback(self.selectboot, MessageBox, _('Wybierz Tak, start image z podmiana kernel lub Nie bez wczytywania kernel.'), MessageBox.TYPE_YESNO)
                restartbox.setTitle(_('Full restart GUI now ?'))

            else:
                os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez NEOBOOT !!! '), MessageBox.TYPE_INFO, 8)
                self.close()           
                
    def selectboot(self, answer):
        if answer is True:
            self.bootimage()
        else:
            self.selectboot2()

    def selectboot2(self):
                        if getImageNeoBoot() == 'Flash':                                        
                            self.session.open(TryQuitMainloop, 2)
                        elif getImageNeoBoot() != 'Flash':  
                                cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...\n')           
                                cmd1='ln -sfn /sbin/neoinitmips /sbin/init; reboot -d -f -h -i' 
                                self.session.open(Console, _('NeoBoot ....'), [cmd, cmd1])                                                         
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że multiboot nie wspiera tego modelu STB !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

    def bootimage(self):
        if getCPUtype() == 'ARMv7': #and        
            self.bootimageARM()
        elif getCPUtype() == 'MIPS': #and        
            self.bootimageARM()
        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że multiboot nie wspiera tego modelu STB !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()         

#################_____ARM____##########################                                                                                              
    def bootimageARM(self):
            #Zgemma h7S ARM  ARM - h7s_mmcblk0p2.sh 
            if getCPUSoC() == 'bcm7251s' or getBoxHostName() == 'h7':  
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxHostName()) ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxHostName()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin' % ( getBoxHostName()) ):
                            self.myclose2(_('\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela flash-kernel-%s.bin ' % ( getBoxHostName()) ))
                        else:
                            if getImageNeoBoot() == 'Flash':                                                
                                if fileExists('/.multinfo'):
                                    os.system('cd /media/mmc; ln -sf "init.sysvinit" "/media/mmc/sbin/init"')
                                    cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_mmcblk0p2.sh '                  

                                elif not fileExists('/.multinfo'):   
                                    cmd = 'ln -sf "init.sysvinit" "/sbin/init"; /etc/init.d/reboot'  
                                    #cmd = 'cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"; reboot -f' %  getBoxHostName()                                                     

                            elif  getImageNeoBoot() != 'Flash':                                                 
                                if not fileExists('/.multinfo'):  
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):   
                                        cmd = 'ln -sfn /sbin/neoinitarm /sbin/init; /etc/init.d/reboot'
                                    
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):     
                                        os.system('ln -sfn /sbin/neoinitarm /sbin/init')
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_mmcblk0p2.sh '                    

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):
                                        cmd = 'python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/findkerneldevice.py'
                                        cmd = 'dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin of=/dev/kernel; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"' %  getBoxHostName() 
                                        cmd = 'cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"; reboot -f' %  getBoxHostName() 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):
                                        os.system('cd /media/mmc; ln -sf "neoinitarm" "/media/mmc/sbin/init"')
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_mmcblk0p2.sh '                                                                                       

                            self.session.open(Console, _('NeoBoot ARM....'), [cmd])
                            self.close()                                                          

            #Octagon SF4008 ARM  ARM - sf4008_mmcblk0p3.sh                                                                                   
            elif getCPUSoC() == 'bcm7251' or getBoxHostName() == 'sf4008' :   
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxHostName()) ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxHostName()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin' % ( getBoxHostName()) ):
                            self.myclose2(_('\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela flash-kernel-%s.bin ' % ( getBoxHostName()) ))
                        else:
                            if getImageNeoBoot() == 'Flash':                                                
                                if fileExists('/.multinfo'):
                                    os.system('cd /media/mmc; ln -sf "init.sysvinit" "/media/mmc/sbin/init"')
                                    cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/sf4008_mmcblk0p3.sh '                  

                                elif not fileExists('/.multinfo'):   
                                    cmd = 'ln -sf "init.sysvinit" "/sbin/init"; /etc/init.d/reboot'  
                                    #cmd = 'cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; reboot -f' %  getBoxHostName()                                                     

                            elif  getImageNeoBoot() != 'Flash':                                                 
                                if not fileExists('/.multinfo'):  
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):   
                                        cmd = 'ln -sfn /sbin/neoinitarm /sbin/init; /etc/init.d/reboot'
                                    
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):     
                                        os.system('ln -sfn /sbin/neoinitarm /sbin/init')
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/sf4008_mmcblk0p3.sh '                    

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):
                                        cmd = 'dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin of=/dev/kernel; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"' %  getBoxHostName() 
                                        cmd = 'cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"; reboot -f' %  getBoxHostName() 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxHostName())):
                                        os.system('cd /media/mmc; ln -sf "neoinitarm" "/media/mmc/sbin/init"')
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/sf4008_mmcblk0p3.sh '                                                                                       

                            self.session.open(Console, _('NeoBoot ARM....'), [cmd])
                            self.close()  
                            
            #VUPLUS ARM - vu_mmcblk0p1.sh                                                                                    
            elif getCPUSoC() == '7444s' or getBoxHostName() == 'vuultimo4k' or getCPUSoC() == '7376' or getBoxHostName() == 'vusolo4k' or getCPUSoC() == '7252s' or getBoxHostName() == 'vuuno4kse': 
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxVuModel()) ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxVuModel()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin' % ( getBoxVuModel()) ):
                            self.myclose2(_('\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela flash-kernel-%s.bin ' % ( getBoxVuModel()) ))
                        else:
                            if getImageNeoBoot() == 'Flash':                                                
                                if fileExists('/.multinfo'):
                                    os.system('cd /media/mmc; ln -sf "init.sysvinit" "/media/mmc/sbin/init"')
                                    cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                    cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p1.sh '                  

                                elif not fileExists('/.multinfo'): 
                                    cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')                                  
                                    cmd1 = 'sleep 5; ln -sf "init.sysvinit" "/sbin/init"; reboot -dfhi'                                                   

                            elif  getImageNeoBoot() != 'Flash':                                                 
                                if not fileExists('/.multinfo'):  
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):  
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = 'ln -sfn /sbin/neoinitarm /sbin/init; /etc/init.d/reboot'
                                    
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):     
                                        os.system('ln -sfn /sbin/neoinitarmvu /sbin/init')
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p1.sh '                    

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        cmd = 'dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin of=/dev/mmcblk0p1; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"' %  getBoxVuModel() 
                                        cmd1 = 'cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"; /etc/init.d/reboot' %  getBoxVuModel() 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        os.system('cd /media/mmc; ln -sf "neoinitarmvu" "/media/mmc/sbin/init"')
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p1.sh '                                                                                       

                            self.session.open(Console, _('NeoBoot ARM VU+....'), [cmd, cmd1])
                            self.close()  

            #VUPLUS ARM - Zero4k vu_mmcblk0p4.sh                                                       
            elif getCPUSoC() == '72604' or getBoxHostName() == 'vuzero4k': 
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxVuModel()) ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxVuModel()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin' % ( getBoxVuModel()) ):
                            self.myclose2(_('\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela flash-kernel-%s.bin ' % ( getBoxVuModel()) ))
                        else:
                            if getImageNeoBoot() == 'Flash':                                                
                                if fileExists('/.multinfo'):
                                    os.system('cd /media/mmc; ln -sf "init.sysvinit" "/media/mmc/sbin/init"')
                                    cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                    cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p4.sh '                  

                                elif not fileExists('/.multinfo'): 
                                    cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')                                  
                                    cmd1 = 'sleep 5; ln -sf "init.sysvinit" "/sbin/init"; reboot -dfhi'                                                   

                            elif  getImageNeoBoot() != 'Flash':                                                 
                                if not fileExists('/.multinfo'):  
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):  
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = 'ln -sfn /sbin/neoinitarm /sbin/init; /etc/init.d/reboot'
                                    
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):     
                                        os.system('ln -sfn /sbin/neoinitarmvu /sbin/init')
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p4.sh '                    

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        cmd = 'dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin of=/dev/mmcblk0p1; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"' %  getBoxVuModel() 
                                        cmd1 = 'cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"; /etc/init.d/reboot' %  getBoxVuModel() 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        os.system('cd /media/mmc; ln -sf "neoinitarmvu" "/media/mmc/sbin/init"')
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p4.sh '                                                                                       
                                                                                                         
                            self.session.open(Console, _('NeoBoot ARM VU+....'), [cmd, cmd1])
                            self.close()

            #VUPLUS ARM - Duo4k vu_mmcblk0p6.sh                                                                  
            elif getCPUSoC() == '7278' or getBoxHostName() == 'vuduo4k' :
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxVuModel()) ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxVuModel()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin' % ( getBoxVuModel()) ):
                            self.myclose2(_('\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela flash-kernel-%s.bin ' % ( getBoxVuModel()) ))
                        else:
                            if getImageNeoBoot() == 'Flash':                                                
                                if fileExists('/.multinfo'):
                                    os.system('cd /media/mmc; ln -sf "init.sysvinit" "/media/mmc/sbin/init"')
                                    cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                    cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p6.sh '                  

                                elif not fileExists('/.multinfo'): 
                                    cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')                                  
                                    cmd1 = 'sleep 5; ln -sf "init.sysvinit" "/sbin/init"; reboot -dfhi'                                                   

                            elif  getImageNeoBoot() != 'Flash':                                                 
                                if not fileExists('/.multinfo'):  
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):  
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = 'ln -sfn /sbin/neoinitarm /sbin/init; /etc/init.d/reboot'
                                    
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):     
                                        os.system('ln -sfn /sbin/neoinitarmvu /sbin/init')
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p6.sh '                    

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        cmd = 'dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin of=/dev/mmcblk0p1; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"' %  getBoxVuModel() 
                                        cmd1 = 'cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"; /etc/init.d/reboot' %  getBoxVuModel() 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        os.system('cd /media/mmc; ln -sf "neoinitarmvu" "/media/mmc/sbin/init"')
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p6.sh '                                                                                       
                                                                                                         
                            self.session.open(Console, _('NeoBoot ARM VU+....'), [cmd, cmd1])
                            self.close() 

#################_____MIPS____################################## 
    def bootimageMIPS(self):
            #Miracle Box Ultra  - MIPS osmini_dev_mtd2.sh
            if getCPUtype() != 'ARMv7' and getCPUSoC() == 'bcm7424' or getTunerModel() == 'ini-8000sv':
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxHostName()) ):
                            self.myclose2(_('Error - w lokalizacji /media/neoboot/ImagesUpload/.kernel/ \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxHostName()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/vmlinux.gz'):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError 2 - w lokalizacji /media/neoboot/ImagesUpload/.kernel/ \nnie odnaleziono pliku kernela vmlinux.gz '))
                        elif not fileExists('/usr/sbin/nandwrite' ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError 3 - w lokalizacji /usr/sbin/ \nnie odnaleziono pliku nandwrite\nmusisz zainstalowac dodatkowe pakiety '))
                        else: 
                            if getImageNeoBoot() == 'Flash':                    
                                if fileExists('/.multinfo'):  
                                    cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/mbultra_dev_mtd2.sh'                  
                                elif not fileExists('/.multinfo'):   
                                    cmd = 'ln -sfn /sbin/init.sysvinit /sbin/init; reboot -d -f -h -i'

                            elif getImageNeoBoot() != 'Flash':                      
                                if not fileExists('/.multinfo'):                        
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                        os.system('ln -sfn /sbin/neoinitmips /sbin/init')
                                        cmd = 'reboot -d -f -h -i'                                                                 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                        os.system('ln -sfn /sbin/neoinitmips /sbin/init')
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/mbultra_dev_mtd2.sh'                  

                                elif fileExists('/.multinfo'):   
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                        cmd = 'flash_eraseall /dev/mtd2; sleep 2; nandwrite -p /dev/mtd2 /media/neoboot/ImagesUpload/.kernel/%s.vmlinux.gz; cp -Rf /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; reboot -f' % (getBoxHostName(),  getBoxHostName())
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/mbultra_dev_mtd2.sh'

                            self.session.open(Console, _('NeoBoot MIPS....'), [cmd])
                            self.close()

            #Edision OS MINI  - MIPS osmini_dev_mtd0.sh   
            elif getCPUtype() != 'ARMv7' and getCPUSoC() == 'BCM7362' or getBoxHostName() == 'osmini':                                      
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxHostName()) ):
                            self.myclose2(_('Error - w lokalizacji /media/neoboot/ImagesUpload/.kernel/ \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxHostName()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/vmlinux.gz'):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError 2 - w lokalizacji /media/neoboot/ImagesUpload/.kernel/ \nnie odnaleziono pliku kernela vmlinux.gz '))
                        elif not fileExists('/usr/sbin/nandwrite' ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError 3 - w lokalizacji /usr/sbin/ \nnie odnaleziono pliku nandwrite\nmusisz zainstalowac dodatkowe pakiety '))
                        else: 
                            if getImageNeoBoot() == 'Flash':                    
                                if fileExists('/.multinfo'):  
                                    cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/osmini_dev_mtd0.sh'                  
                                elif not fileExists('/.multinfo'):   
                                    cmd = 'ln -sfn /sbin/init.sysvinit /sbin/init; reboot -d -f -h -i'

                            elif getImageNeoBoot() != 'Flash':                      
                                if not fileExists('/.multinfo'):                        
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                        os.system('ln -sfn /sbin/neoinitmips /sbin/init')
                                        cmd = 'reboot -d -f -h -i'                                                                 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                        os.system('ln -sfn /sbin/neoinitmips /sbin/init')
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/osmini_dev_mtd0.sh'                  

                                elif fileExists('/.multinfo'):   
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                        cmd = 'flash_eraseall /dev/mtd2; sleep 2; nandwrite -p /dev/mtd2 /media/neoboot/ImagesUpload/.kernel/%s.vmlinux.gz; cp -Rf /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; reboot -f' % (getBoxHostName(),  getBoxHostName())
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxHostName())):
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/osmini_dev_mtd0.sh'

                            self.session.open(Console, _('NeoBoot MIPS....'), [cmd])
                            self.close()
            #VUPLUS MIPS vu_dev_mtd2.sh             
            elif getCPUSoC() == '7356' or getCPUSoC() == '7429' or getCPUSoC() == '7424'  or getCPUSoC() == '7241' or getCPUSoC() == '7362' or getBoxHostName() == 'vusolo2' or getBoxHostName() == 'vusolose'  or getBoxHostName() == 'vuduo2' or getBoxHostName() == 'vuzero':
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxVuModel()) ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxVuModel()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/vmlinux.gz' % ( getBoxVuModel()) ):
                            self.myclose2(_('\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela vmlinux.gz ' ))
                        else:
                        
                            if getImageNeoBoot() == 'Flash':                    
                                if fileExists('/.multinfo'):  
                                    cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd2.sh'                  
                                elif not fileExists('/.multinfo'):  
                                    cmd = 'ln -sfn /sbin/init.sysvinit /sbin/init; /etc/init.d/reboot -i'

                            elif getImageNeoBoot() != 'Flash':                       
                                if not fileExists('/.multinfo'):                        
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        os.system('ln -sfn /sbin/neoinitmipsvu /sbin/init')
                                        cmd = '/etc/init.d/reboot'                                                                 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        os.system('ln -sfn /sbin/neoinitmipsvu /sbin/init')
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd2.sh'                  

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        cmd = 'flash_eraseall /dev/mtd2; sleep 2; nandwrite -p /dev/mtd2 /media/neoboot/ImagesUpload/.kernel/%s.vmlinux.gz; cp -Rf /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; /etc/init.d/reboot' % (getBoxVuModel(), getBoxVuModel())
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd2.sh'

                            self.session.open(Console, _('NeoBoot MIPS....'), [cmd])
                            self.close()

            #VUPLUS MIPS vu_dev_mtd1.sh   
            elif getCPUSoC() == '7335'  or getCPUSoC() == '7325' or getCPUSoC() == '7405' or getCPUSoC() == '7405(with 3D)' or getBoxHostName() == 'vuultimo' or getBoxHostName() == 'bm750' or getBoxHostName() == 'duo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuduo':                              
                        if not fileExists('/media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % ( getBoxVuModel()) ):
                            self.myclose2(_('#############>>>>>>>>>\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela zImage.%s.ipk ' % ( getBoxVuModel()) ))
                        elif not fileExists('/media/neoboot/ImagesUpload/.kernel/vmlinux.gz' % ( getBoxVuModel()) ):
                            self.myclose2(_('\n\n\nError - w lokalizacji /media/neoboot/ImagesUpload/.kernel/  \nnie odnaleziono pliku kernela vmlinux.gz ' ))
                        else:
                        
                            if getImageNeoBoot() == 'Flash':                    
                                if fileExists('/.multinfo'):  
                                    cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd1.sh'                  
                                elif not fileExists('/.multinfo'):  
                                    cmd = 'ln -sfn /sbin/init.sysvinit /sbin/init; /etc/init.d/reboot -i'

                            elif getImageNeoBoot() != 'Flash':                       
                                if not fileExists('/.multinfo'):                        
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        os.system('ln -sfn /sbin/neoinitmipsvu /sbin/init')
                                        cmd = '/etc/init.d/reboot'                                                                 

                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        os.system('ln -sfn /sbin/neoinitmipsvu /sbin/init')
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd1.sh'                  

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        cmd = 'flash_eraseall /dev/mtd1; sleep 2; nandwrite -p /dev/mtd1 /media/neoboot/ImagesUpload/.kernel/%s.vmlinux.gz; cp -Rf /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk /tmp/zImage.ipk; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /tmp/zImage.ipk; /etc/init.d/reboot' % (getBoxVuModel(), getBoxVuModel())
                                    elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                        cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd1.sh'

                            self.session.open(Console, _('NeoBoot MIPS....'), [cmd])
                            self.close()

            else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że multiboot nie wspiera tego modelu STB !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()