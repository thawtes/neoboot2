#!/bin/sh
#script - gutosie 

#getCPUSoC() == 'bcm7252s' or getBoxHostName() == 'gbquad4k'

if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi
KERNEL=`uname -r` 
IMAGE=/media/neoboot/ImageBoot
IMAGENEXTBOOT=/media/neoboot/ImageBoot/.neonextboot
BOXNAME=$( cat /etc/hostname)   

if [ -f /proc/stb/info/vumodel ];  then  
    VUMODEL=$( cat /proc/stb/info/vumodel )     
fi 

if [ -f /proc/stb/info/boxtype ];  then  
    BOXTYPE=$( cat /proc/stb/info/boxtype )    
fi

if [ -f /proc/stb/info/chipset ];  then  
    CHIPSET=$( cat /proc/stb/info/chipset )    
fi

if [ -f /tmp/zImage.ipk ];  then  
    rm -f /tmp/zImage.ipk    
fi

if [ -f /tmp/zImage ];  then  
    rm -f /tmp/zImage    
fi

if [ -f $IMAGENEXTBOOT ]; then
  TARGET=`cat $IMAGENEXTBOOT`
else
  TARGET=Flash              
fi

echo "NEOBOOT is booting image from " $TARGET

if [ $BOXNAME = "h7" ] || [ $CHIPSET = "bcm7251s" ]; then                    

    if [ $TARGET = "Flash" ]; then                       
                if [ -e /.multinfo ]; then                                             
                                cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init
                                if [ -e /media/neoboot/ImagesUpload/.kernel/flash-kernel-$BOXNAME.bin ] ; then
                                    [ $PL ] && echo "Instalacja pliku kernel bin " || echo "Instaling the kernel.bin file"                                                                                                                                              
                                    if [ -d /proc/stb ] ; then
                                            python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/gbfindkerneldevice.py
                                            dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$BOXNAME.bin conv=noerror conv=sync of=/dev/kernel                      	    	            
                                    fi                                     
                                    cat /dev/kernel | grep "kernel"                                   
                                fi                                                                          
                                update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                                echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel                          
                                echo "Boot - Flash z dysku usb lub hdd..."  
                elif [ ! -e /.multinfo ]; then                                                        
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/flash-kernel-$BOXNAME.bin ] ; then
                                        [ $PL ] && echo "Instalacja pliku kernel.bin w flash ..." || echo "Instaling the kernel.bin file to flash..."                                                                          
                                        if [ -d /proc/stb ] ; then
                                                    python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/gbfindkerneldevice.py
                                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$BOXNAME.bin conv=noerror conv=sync of=/dev/kernel                                                    
                                        fi                                                                                                       
                                        cat /dev/kernel | grep "kernel"
                                        sleep 2
                                        update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                        echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                        echo "Reboot - Flash. Instalacja kernel do /dev/mmcblk0p..."                                         
                                        [ $PL ] && " NEOBOOT - zainstalowano kernel-image - " $TARGET  "Za chwile nastapi restart systemu !!!"  || " NEOBOOT - installed kernel-image - " $TARGET  "The system will restart in a moment !!!" 
                                    fi                                                                                                     
                fi
                sleep 5; reboot -d -f -h -i 
    else              	    
        if [ $TARGET != "Flash" ]; then 
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image " $TARGET
                                else
                                    [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."                                          
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/zImage.$BOXNAME /tmp/zImage
                                    echo "Instalacja kernel do /dev/mmcblk0p..."
                                    sleep 2                                   
                                    if [ -d /proc/stb ] ; then
                                                    python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/gbfindkerneldevice.py
                                                    dd if=dd if=/tmp/zImage of=/dev/kernel                                    
                                    fi
                                    rm -f /tmp/zImage
                                    cat /dev/kernel | grep "kernel" 
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " VUPLUS z procesorem arm zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"                                                                          
                                fi
                        else        
                                    [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."
                                    sleep 2
                                    cp -fR $IMAGE/$TARGET/boot/zImage.$BOXNAME /tmp/zImage
                                    echo "Instalacja kernel bin do /dev/mmcblk0p..."
                                    sleep 2 
                                    if [ -d /proc/stb ] ; then
                                                    python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/gbfindkerneldevice.py
                                                    dd if=dd if=/tmp/zImage of=/dev/kernel                                                      
                                    fi
                                    rm -f /tmp/zImage                                   
                                    cat /dev/kernel | grep "kernel"
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " H7 zmieniony."
                                    echo "Za chwile nastapi restart systemu..."
                                    echo "Used Kernel: " $TARGET  > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"                                             
                        fi                        
                        sleep 5; reboot -d -f -h -i
        fi
    fi                               
else
                    echo "$TARGET "  > /media/neoboot/ImageBoot/.neonextboot
                    echo "Error - Nie wpierany model STB !!! "
                    exit 0
fi
exit 0
