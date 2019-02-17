#!/bin/sh
#script - gutosie 
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

if [ $VUMODEL = "duo4k" ]; then                    

    if [ $TARGET = "Flash" ]; then   
        if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then                     
                if [ -e /.multinfo ]; then                                            
                            if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then  
                                cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    echo "Boot - Flash. Instalacja kernel do /dev/mmcblk0p6..."                                                                                                           
                                    if [ -d /proc/stb ] ; then
                      	    	            dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin of=/dev/mmcblk0p6
                                    fi

                                    if [ ! -e "$D/lib/modules/`uname -r`" ]; then
                                            mkdir -p $D/lib/modules/`uname -r`
                                    fi
                                    if [ -n "$D" ]; then
                                            depmodwrapper -a -b $D `uname -r`
                                    else
                                        depmod -a `uname -r`
                                    fi

                                    rm -f /tmp/zImage
                                    true
                                    [ $PL ] && echo "Przenoszenie pliku kernel bin do /tmp" || echo "Moving the kernel file to /tmp"                                      
                                    sleep 2
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk  
                                    echo "Instalacja kernel zImage.ipk do /dev/mmcblk0p6..."                                  
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                    cat /dev/mmcblk0p6 | grep "kernel"                                   
                                fi                                                   
                            fi                        
                        update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                        echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel                          

                elif [ ! -e /.multinfo ]; then
                            if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then                                                         
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                        echo "Reboot - Flash. Instalacja kernel do /dev/mmcblk0p6..."                                                                           
                                        if [ -d /proc/stb ] ; then
                                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin conv=noerror conv=sync of=/dev/mmcblk0p6
                                        fi
                                        true
                                        [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."                                      
                                        sleep 2                                    
                                        cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk
                                        echo "Instalacja kernel zImage.ipk do /dev/mmcblk0p6..."
                                        opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk                                
                                        cat /dev/mmcblk0p6 | grep "kernel"
                                    fi
                               
                            fi                                                                       
                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                            echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                            [ $PL ] && " NEOBOOT - zainstalowano kernel-image - " $TARGET  "Za chwile nastapi restart systemu !!!"  || " NEOBOOT - installed kernel-image - " $TARGET  "The system will restart in a moment !!!" 
                fi
                sleep 5; reboot -d -f -h -i 
        fi
    else              	    
        if [ $TARGET != "Flash" ]; then 
            if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image " $TARGET
                                else
                                    [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."                                          
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    echo "Instalacja kernel do /dev/mmcblk0p6..."
                                    sleep 2                                   
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/tmp/zImage of=/dev/mmcblk0p6
                                    fi
                                    rm -f /tmp/zImage
                                    true 
                                    cat /dev/mmcblk0p6 | grep "kernel"1 
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " VUPLUS z procesorem arm zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"                                                                          
                                fi
                        else        
                                    [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."
                                    sleep 2
                                    cp -fR $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    echo "Instalacja kernel bin do /dev/mmcblk0p6..."
                                    sleep 2 
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/tmp/zImage of=/dev/mmcblk0p6
                                    fi
                                    rm -f /tmp/zImage
                                    true                                    
                                    cat /dev/mmcblk0p6 | grep "kernel"
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " VU+ zmieniony."
                                    sleep 2
                                    echo "Za chwile nastapi restart systemu..."
                                    sleep 2
                                    echo "Used Kernel: " $TARGET  > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    sleep 2
                                    echo "Typ procesora: " $CHIPSET " STB"                                             
                        fi                        
                        sleep 5; reboot -d -f -h -i
            fi
        fi
    fi                               
else
                    echo "$TARGET "  > /media/neoboot/ImageBoot/.neonextboot
                    echo "Error - Nie wpierany model STB !!! "
                    exit 0
fi
exit 0
