#!/bin/sh
#script - gutosie 
if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi

if [ -f /proc/stb/info/boxtype ];  then  
    BOXTYPE=$( cat /proc/stb/info/boxtype )    
fi                                        

if [ -f /proc/stb/info/chipset ];  then  
    CHIPSET=$( cat /proc/stb/info/chipset )    
fi

if [ -f /tmp/zImage ];  then  
    rm -f /tmp/zImage    
fi

KERNEL=`uname -r` 
IMAGE=ImageBoot
IMAGENEXTBOOT=/ImageBoot/.neonextboot
NEOBOOTMOUNT=$( cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location) 
BOXNAME=$( cat /etc/hostname) 
# $NEOBOOTMOUNT$IMAGE 
# $NEOBOOTMOUNT

if [ -f $NEOBOOTMOUNT$IMAGENEXTBOOT ]; then
  TARGET=`cat $NEOBOOTMOUNT$IMAGENEXTBOOT`
else
  TARGET=Flash              
fi

echo "NEOBOOT is booting image from " $TARGET

#gbquad4k: bcm7252s    
# cat /proc/stb/info/model : gbquad4k 
# cat /etc/hostname : gbquad4k 
# cat /proc/cmdline root=/dev/mmcblk0p5 rootwait rw rootflags=data=journal libata.force=1:3.0G,2:3.0G,3:3.0G coherent_poll=2M vmalloc=525m bmem=529m@491m bmem=608m@2464m

if [ $BOXNAME = "gbquad4k" ] || [ $CHIPSET = "bcm7252s" ]; then
    if [ $TARGET = "Flash" ]; then                       
                [ $PL ] && echo "Instalacja pliku kernel bin /dev/mmcblk0p......" || echo "Instaling kernel bin file /dev/mmcblk0p... "                
                if [ -e /.multinfo ]; then                                                                                                                             
                                cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init
                                if [ -e $NEOBOOTMOUNT/ImagesUpload/.kernel/flash-kernel-$BOXNAME.bin ] ; then                                                                                                                                                                                                                       
                                    if [ -d /proc/stb ] ; then
                      	    	            python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/gbfindkerneldevice.py
                      	    	            dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$BOXNAME.bin conv=noerror conv=sync of=/dev/kernel                      	    	            
                                    fi
                                    echo "Boot - Flash. "                                                                                                                                                                                        
                                    echo "Start image Flash z dysku hdd lub usb za 5 sekund RESTART...; \n\n..................._REBOOT_..................." 
                                fi                                                                                                                              
                elif [ ! -e /.multinfo ]; then                                                        
                                    if [ -e $NEOBOOTMOUNT/ImagesUpload/.kernel/flash-kernel-$BOXNAME.bin ] ; then
                                        [ $PL ] && echo "Instalacja pliku kernel bin..." || echo "Instaling kernel bin file "                                                                                                                  
                                        if [ -d /proc/stb ] ; then
                      	    	                    python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/gbfindkerneldevice.py
                      	    	                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$BOXNAME.bin conv=noerror conv=sync of=/dev/kernel                      	    	            
                                        fi                                                                                                                                              
                                        echo "Start-restart Flash image..."                                                                                 
                                        echo "Reboot image Flash za 5 sekund RESTART...; \n\n...................=REBOOT=..................." 
                                    fi                                                                                                     
                fi                
                update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                [ $PL ] && echo " Zainstalowano kernel image  " $TARGET  " "  || echo " Installed kernel image - "$TARGET" "
                cat /dev/kernel | grep "kernel"
                echo "Used Kernel: " $TARGET > $NEOBOOTMOUNT/ImagesUpload/.kernel/used_flash_kernel
                echo "STB: " $CHIPSET " "$BOXNAME" "
                sleep 5; reboot -d -f -h -i 
    else              	    
        if [ $TARGET != "Flash" ]; then                    
                        [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image " $TARGET
                                else                                         
                                    sleep 2
                                    cp -f $NEOBOOTMOUNT$IMAGE/$TARGET/boot/zImage.$BOXNAME /tmp/zImage
                                    echo "Instalacja kernel do /dev/mmcblk0p..."
                                    sleep 2                                   
                                    if [ -d /proc/stb ] ; then
                      	    	                    python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/gbfindkerneldevice.py
                                                    dd if=/tmp/zImage of=/dev/kernel                     	    	                            
                                    fi                                                                                                                                               
                                    echo "Start image z Flash..."
                                    echo "Kernels for image " $TARGET " changed..."                                                                        
                                    echo "Start innego image z Flash za 5 sekund RESTART...... \n\n...................*REBOOT*..................."
                                fi
                        else                                            
                                    sleep 2
                                    cp -fR $NEOBOOTMOUNT$IMAGE/$TARGET/boot/zImage.$BOXNAME /tmp/zImage
                                    echo "Instalacja kernel bin do /dev/mmcblk0p..."
                                    sleep 2 
                                    if [ -d /proc/stb ] ; then
          	    	                    python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/gbfindkerneldevice.py
                                            dd if=/tmp/zImage of=/dev/kernel                     	    	                            
                                    fi                                                                         
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " zmieniony."                                                                                                                                                      
                                    echo "Start innego image z Flash za 5 sekund RESTART...... \n\n...................-REBOOT-..................."
                        fi                        
                        rm -f /tmp/zImage
                        cat /dev/kernel | grep "kernel"
                        update-alternatives --remove vmlinux vmlinux-`uname -r` || true                        
                        echo "Used Kernel: " $TARGET  > $NEOBOOTMOUNT/ImagesUpload/.kernel/used_flash_kernel 
                        echo "STB: " $CHIPSET " "$BOXNAME" "
                        sleep 5; reboot -d -f -h -i
        fi
    fi                               
else
                    ln -sfn /sbin/init.sysvinit /sbin/init
                    echo "CHIPSET: " $CHIPSET " BOXNAME: "$BOXNAME" "
                    echo "$TARGET "  > $NEOBOOTMOUNT/ImageBoot/.neonextboot
                    echo "Error - Nie wpierany model STB !!! "
                    exit 0
fi
exit 0