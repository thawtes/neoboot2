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

if [ $VUMODEL = "ultimo4k" ] || [ $VUMODEL = "solo4k" ] || [ $VUMODEL = "uno4kse" ] || [ $VUMODEL = "uno4k" ]; then                    

    if [ $TARGET = "Flash" ]; then   
        if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then                     
                if [ -e /.multinfo ]; then                                            
                            if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then  
                                cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init
                                if [ -e /media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin ] ; then
                                    echo "Boot - Flash. Instalacja kernel do /dev/mmcblk0p1..."  
                                    [ $PL ] && echo "Instalacja pliku kernel bin..." || echo "Instaling kernel bin file "                                                                                                                                              
                                    if [ -d /proc/stb ] ; then
                      	    	            dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin of=/dev/mmcblk0p1
                                    fi
                                    rm -f /tmp/zImage                                     
                                    cat /dev/mmcblk0p1 | grep "kernel"                                   
                                    echo "Start image Flash z dysku hdd lub usb..."
                                    sleep 5
                                fi                                                   
                            fi                        
                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                            echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel                          


                elif [ ! -e /.multinfo ]; then
                            if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then                                                         
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin ] ; then
                                        [ $PL ] && echo "Instalacja pliku kernel bin..." || echo "Instaling kernel bin file "                                                                                                                  
                                        if [ -d /proc/stb ] ; then
                                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin conv=noerror conv=sync of=/dev/mmcblk0p1
                                        fi
                                        echo "Reboot - Flash. Instalacja kernel /dev/mmcblk0p1..."                                                                                                       
                                        cat /dev/mmcblk0p1 | grep "kernel"
                                        echo "Start-restart Flash image..."
                                        sleep 5
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
                                    echo "Instalacja kernel do /dev/mmcblk0p1..."
                                    sleep 2                                   
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/tmp/zImage of=/dev/mmcblk0p1
                                    fi                                    
                                    rm -f /tmp/zImage
                                    cat /dev/mmcblk0p1 | grep "kernel" 
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Start image z Flash..."
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " VUPLUS z procesorem arm zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"                                                                          
                                    echo "Start image z dysku hdd lub usb..."
                                    sleep 5
                                fi
                        else        
                                    [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."
                                    sleep 2
                                    cp -fR $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    echo "Instalacja kernel bin do /dev/mmcblk0p1..."
                                    sleep 2 
                                    if [ -d /proc/stb ] ; then
                                            dd if=/tmp/zImage of=/dev/mmcblk0p1
                                    fi                                     
                                    rm -f /tmp/zImage                                                                      
                                    cat /dev/mmcblk0p1 | grep "kernel"
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " VU+ zmieniony."
                                    echo "Za chwile nastapi restart systemu..."
                                    echo "Used Kernel: " $TARGET  > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"                                             
                                    echo "Start innego image z Flash..."
                                    sleep 5
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
