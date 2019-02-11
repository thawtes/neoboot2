#!/bin/sh
#script - gutosie 

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
                   
if [ $TARGET = "Flash" ]; then                    
                if [ -e /.multinfo ]; then                    
                    if [ ! -e /proc/stb/info/boxtype ]; then 
                        if [ $VUMODEL = "ultimo4k" ] || [ $VUMODEL = "solo4k" ] || [ $VUMODEL = "uno4k" ] || [ $VUMODEL = "uno4kse" ] ; then                         
                            if [ -f /proc/stb/info/vumodel ]; then
                                cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    echo "Instalacja kernel do /dev/mmcblk0p1..."                                    
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin conv=noerror conv=sync of=/dev/mmcblk0p1
                                            fi
                                            true                                     
                                            echo "Przenoszenie pliku kernel do /tmp..."
                                            sleep 2
                                            cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk  
                                            echo "Instalacja kernel zImage.ipk do /dev/mmcblk0p1..."                                  
                                            opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                            cat /dev/mmcblk0p1 | grep "kernel"
                                fi                                                   
                            fi

                        elif [ $VUMODEL = "zero4k" ]; then 
                            if [ -f /proc/stb/info/vumodel ]; then
                                cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    echo "Instalacja kernel do /dev/mmcblk0p4..."                                    
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin conv=noerror conv=sync of=/dev/mmcblk0p4
                                            fi
                                            true                                                                                 
                                            echo "Przenoszenie pliku kernel do /tmp..."
                                            sleep 2
                                            cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk  
                                            echo "Instalacja kernel zImage.ipk do /dev/mmcblk0p4..."                                  
                                            opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                            cat /dev/mmcblk0p4 | grep "kernel"
                                fi                                                   
                            fi
                            
                        elif [ $VUMODEL = "duo4k" ]; then 
                            if [ -f /proc/stb/info/vumodel ]; then
                                cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    echo "Instalacja kernel do /dev/mmcblk0p6..."                                    
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin conv=noerror conv=sync of=/dev/mmcblk0p6
                                            fi
                                            true                                                                                 
                                            echo "Przenoszenie pliku kernel do /tmp..."
                                            sleep 2
                                            cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk  
                                            echo "Instalacja kernel zImage.ipk do /dev/mmcblk0p6..."                                  
                                            opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                            cat /dev/mmcblk0p6 | grep "kernel"
                                fi                                                   
                            fi                                                 
                            
                        elif [ $VUMODEL = "solo2" ] || [ $VUMODEL = "duo2" ] || [ $VUMODEL = "solose" ] || [ $VUMODEL = "zero" ]; then 
                            if [ -f /proc/stb/info/vumodel ]; then
                                if [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    echo "Kasowanie kernel z /dev/mtd2..."                                    
                                    flash_eraseall /dev/mtd2 
                                    sleep 2 
                                    echo "Instalacja kernel do /dev/mtd2..."                
		                    nandwrite -p /dev/mtd2 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                fi
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    echo "Przenoszenie pliku kernel do /tmp..."
                                    sleep 2
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk  
                                    echo "Instalacja kernel do /dev/mtd2..."                                 
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk

                                fi                            
                            fi                        

                        elif [ $VUMODEL = "bm750" ] || [ $VUMODEL = "duo" ] || [ $VUMODEL = "solo" ] || [ $VUMODEL = "uno" ] || [ $VUMODEL = "ultimo" ]; then
                            if [ -f /proc/stb/info/vumodel ]; then
                                if [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    echo "Kasowanie kernel z /dev/mtd1..."
                                    sleep 2                                
                                    flash_eraseall /dev/mtd1  
                                    echo "Instalacja kernel do /dev/mtd1..." 
                                    sleep 2                                                    
		                    nandwrite -p /dev/mtd1 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                fi
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    echo "Przenoszenie pliku kernel do /tmp..."
                                    sleep 2                                
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk 
                                    echo "Instalacja kernel do /dev/mtd1..."                                                                       
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                fi                            
                            fi 
                        fi
                        update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                        echo "NEOBOOT is booting image from " $TARGET
                        echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                        sleep 5; reboot -d -f -h -i
                    fi
#MiracleBox Ultra - test



                    if [ $BOXNAME = "mbultra" ] || [ $CHIPSET = "bcm7424" ]; then 
                            if [ -f /proc/stb/info/boxtype ]; then
                                #if [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    #echo "Kasowanie kernel z /dev/mtd2..."                                    
                                    #flash_erase /dev/mtd2 0 0
                                    #sleep 2 
                                    #echo "Instalacja kernel do /dev/mtd2..."                
		                    #nandwrite -p /dev/mtd2 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    #update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                #fi
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$BOXNAME.ipk ] ; then
                                    echo "Przenoszenie pliku kernel do /tmp..."
                                    sleep 2
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$BOXNAME.ipk /tmp/zImage.ipk  
                                    echo "Instalacja kernel do /dev/mtd2..."                                 
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk

                                fi                            
                            fi 
                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                            echo "NEOBOOT is booting image from " $TARGET
                            echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                            sleep 5; reboot -d -f -h -i                           
##################
#Edision OSmini - test

                    elif [ $BOXNAME = "osmini" ] || [ $CHIPSET = "BCM7362" ]  || [ $BOXNAME = "osmini" ]; then 
                            if [ -f /proc/stb/info/vumodel ]; then
                                if [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    echo "Kasowanie kernel z /dev/mtd0..."                                    
                                    flash_eraseall /dev/mtd0 
                                    sleep 2 
                                    echo "Instalacja kernel do /dev/mtd0..."                
		                    nandwrite -p /dev/mtd0 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                fi
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$BOXNAME.ipk ] ; then
                                    echo "Przenoszenie pliku kernel do /tmp..."
                                    sleep 2
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$BOXNAME.ipk /tmp/zImage.ipk  
                                    echo "Instalacja kernel do /dev/mtd0..."                                 
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk

                                fi                            
                            fi 
                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                            echo "NEOBOOT is booting image from " $TARGET
                            echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                            sleep 5; reboot -d -f -h -i                             
##################
                    fi

                else
                    if [ ! -e /.multinfo ]; then
                        if [ ! -e /media/neoboot/ImagesUpload/.kernel/used_flash_kernel ]; then
                            if [ ! -e /proc/stb/info/boxtype ]; then 
                                if [ $VUMODEL = "ultimo4k" ] || [ $VUMODEL = "solo4k" ] || [ $VUMODEL = "uno4k" ] || [ $VUMODEL = "uno4kse" ] ; then                         
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                        echo "Instalacja kernel do /dev/mmcblk0p1..."                                    
                                        if [ -d /proc/stb ] ; then
                                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin conv=noerror conv=sync of=/dev/mmcblk0p1
                                            fi
                                            true                                      
                                            echo "Przenoszenie pliku kernel do /tmp..."
                                            sleep 2                                    
                                            cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk
                                            echo "Instalacja kernel zImage.ipk do /dev/mmcblk0p1..."
                                            opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk                                
                                            cat /dev/mmcblk0p1 | grep "kernel"
                                    fi

                                elif [ $VUMODEL = "zero4k" ]; then                             
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                        echo "Instalacja kernel do /dev/mmcblk0p4..."                                    
                                        if [ -d /proc/stb ] ; then
                                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin conv=noerror conv=sync of=/dev/mmcblk0p4
                                            fi
                                            true                                     
                                            echo "Przenoszenie pliku kernel do /tmp..."
                                            sleep 2                                    
                                            cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk
                                            echo "Instalacja kernel zImage.ipk do /dev/mmcblk0p..."
                                            opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                            cat /dev/mmcblk0p4 | grep "kernel"                                
                                    fi
                                
                                elif [ $VUMODEL = "bm750" ] || [ $VUMODEL = "duo" ] || [ $VUMODEL = "solo" ] || [ $VUMODEL = "uno" ] || [ $VUMODEL = "ultimo" ]; then                     
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                        echo "Kasowanie kernel z /dev/mtd1..."
                                        sleep 2
                                        flash_eraseall /dev/mtd1   
                                        echo "Wgrywanie kernel do /dev/mtd1..."
                                        sleep 2                                                   
		                        nandwrite -p /dev/mtd1 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                        update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                    fi
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                        echo "Przenoszenie pliku kernel do /tmp..."
                                        sleep 2 
                                        cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk 
                                        echo "Instalacja kernel zImage.ipk..."                                   
                                        opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                    fi                            
                                
                                elif [ $VUMODEL = "solo2" ] || [ $VUMODEL = "duo2" ] || [ $VUMODEL = "solose" ] || [ $VUMODEL = "zero" ]; then 
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                        echo "Kasowanie kernel z /dev/mtd2..."
                                        sleep 2                                
                                        flash_eraseall /dev/mtd2   
                                        echo "Wgrywanie kernel do /dev/mtd2..."
                                        sleep 2                                                    
		                        nandwrite -p /dev/mtd2 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                        update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                    fi
                                    if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                        echo "Przenoszenie pliku kernel do /tmp..."
                                        sleep 2                                 
                                        cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk   
                                        echo "Instalacja kernel zImage.ipk..."                                                                      
                                        opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                    fi                            
                                fi
                            fi                            
                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                            echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                            echo " NEOBOOT - zainstalowano kernel-image - " $TARGET  "Za chwile nastapi restart systemu !!!"
                            sleep 5 ; reboot -d -f -h -i


                        fi 
#Ultra
                        if [ $BOXNAME = "mbultra" ] || [ $CHIPSET = "bcm7424" ]; then 
                                #if [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    #echo "Kasowanie kernel z /dev/mtd2..."
                                    #sleep 2                                
                                    #flash_eraseall /dev/mtd2 0 0   
                                    #echo "Wgrywanie kernel do /dev/mtd2..."
                                    #sleep 2                                                    
		                    #nandwrite -p /dev/mtd2 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    #update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                #fi
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$BOXNAME.ipk ] ; then
                                    echo "Przenoszenie pliku kernel do /tmp..."
                                    sleep 2                                 
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$BOXNAME.ipk /tmp/zImage.ipk   
                                    echo "Instalacja kernel zImage.ipk..."                                                                      
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                fi                            
                                echo " NEOBOOT Start sytem - " $TARGET  "Za chwile nastapi restart !!!"
                                sleep 5; reboot -d -f -h -i 
#OSmini
                        elif [ $BOXNAME = "osmini" ] || [ $CHIPSET = "BCM7362" ]; then
                                if [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    echo "Kasowanie kernel z /dev/mtd0..."
                                    sleep 2                                
                                    flash_eraseall /dev/mtd0   
                                    echo "Wgrywanie kernel do /dev/mtd0..."
                                    sleep 2                                                    
		                    nandwrite -p /dev/mtd0 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                fi
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$BOXNAME.ipk ] ; then
                                    echo "Przenoszenie pliku kernel do /tmp..."
                                    sleep 2                                 
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$BOXNAME.ipk /tmp/zImage.ipk   
                                    echo "Instalacja kernel zImage.ipk..."                                                                      
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                fi                            
                                echo " NEOBOOT Start sytem - " $TARGET  "Za chwile nastapi restart !!!"
                                sleep 5; reboot -d -f -h -i                            
                        else                            
                            echo " NEOBOOT Start sytem - " $TARGET  "Za chwile nastapi restart !!!"
                            sleep 5; reboot -d -f -h -i
                        fi
                    fi
                fi
else
              	    
    if [ -f /proc/stb/info/vumodel ]; then
        if [ ! -e /proc/stb/info/boxtype ]; then
            if [ $VUMODEL = "ultimo4k" ] || [ $VUMODEL = "solo4k" ] || [ $VUMODEL = "uno4k" ] || [ $VUMODEL = "uno4kse" ] ; then 
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET
                                else                                              
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    echo "Instalacja kernel do /dev/mmcblk0p1..."
                                    sleep 2                                     
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/tmp/zImage of=/dev/mmcblk0p1
                                            fi
                                            rm -f /tmp/zImage
                                            true 
                                            cat /dev/mmcblk0p1 | grep "kernel"1 
                                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                            echo "Kernel dla potrzeb startu systemu " $TARGET " VUPLUS z procesorem arm zostal zmieniony!!!"
                                            echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                            echo "Typ procesora: " $CHIPSET " STB"                                                                          
                                fi
                        else              
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -fR $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    echo "Instalacja kernel do /dev/mmcblk0p1..."
                                    sleep 2 
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/tmp/zImage of=/dev/mmcblk0p1
                                            fi
                                            rm -f /tmp/zImage
                                            true                                    
                                            cat /dev/mmcblk0p1 | grep "kernel"
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

            elif [ $VUMODEL = "zero4k" ]; then                         
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET
                                    sleep 5; reboot -d -f -h -i
                                else                                              
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    echo "Instalacja kernel do /dev/mmcblk0p4..."
                                    sleep 2                                     
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/tmp/zImage of=/dev/mmcblk0p4
                                            fi
                                            rm -f /tmp/zImage
                                            true 
                                            cat /dev/mmcblk0p4 | grep "kernel"
                                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                            echo "Kernel dla potrzeb startu systemu " $TARGET " VUPLUS z procesorem arm zostal zmieniony!!!"
                                            echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                            echo "Typ procesora: " $CHIPSET " STB"
                                            sleep 5; reboot -d -f -h -i                              
                                fi
                        else              
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -fR $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    echo "Instalacja kernel do /dev/mmcblk0p4..."
                                    sleep 2 
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/tmp/zImage of=/dev/mmcblk0p4
                                            fi
                                            rm -f /tmp/zImage
                                            true                                    
                                            cat /dev/mmcblk0p4 | grep "kernel"
                                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                            echo "Kernel dla potrzeb startu systemu " $TARGET " VU+ zmieniony."
                                            sleep 2
                                            echo "Za chwile nastapi restart systemu..."
                                            sleep 2
                                            echo "Used Kernel: " $TARGET  > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                            sleep 2
                                            echo "Typ procesora: " $CHIPSET " STB"
                                            sleep 5                                              
                        fi

                        reboot -d -f -h -i                                    

            elif [ $VUMODEL = "solo2" ] || [ $VUMODEL = "duo2" ] || [ $VUMODEL = "solose" ] || [ $VUMODEL = "zero" ] ; then	     
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET                                    
                                else                                  
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/$VUMODEL.vmlinux.gz /tmp/vmlinux.gz 
                                    echo "Kasowanie kernel z /dev/mtd2"
                                    sleep 2 
                                    flash_eraseall /dev/mtd2
                                    echo "Wgrywanie kernel do /dev/mtd2"                                    
                                    sleep 2
		                    nandwrite -p /dev/mtd2 //tmp/vmlinux.gz 
		                    rm -f //tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"t 
                                fi
                        else
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/$VUMODEL.vmlinux.gz /tmp/vmlinux.gz
                                    echo "Kasowanie kernel z /dev/mtd2"
                                    sleep 2                                    
                                    flash_eraseall /dev/mtd2 
                                    echo "Wgrywanie kernel do /dev/mtd2"                                    
                                    sleep 2                                                                       
		                    nandwrite -p /dev/mtd2 /tmp/vmlinux.gz 
		                    rm -f /tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"
                        fi
	                sleep 5; reboot -d -f -h -i                                    	     

            elif [ $VUMODEL = "bm750" ] || [ $VUMODEL = "duo" ] || [ $VUMODEL = "solo" ] || [ $VUMODEL = "uno" ] || [ $VUMODEL = "ultimo" ]; then
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET                                    
                                else                                    
                                    echo "Kasowanie kernel z /dev/mtd1"
                                    sleep 2
                                    flash_eraseall /dev/mtd1
                                    echo "Wgrywanie kernel do /dev/mtd1"                                    
                                    sleep 2
		                    nandwrite -p /dev/mtd1 //$IMAGE/$TARGET/boot/$VUMODEL.vmlinux.gz  
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                fi
                        else
                                    echo "Kasowanie kernel z /dev/mtd1"
                                    sleep 2
                                    flash_eraseall /dev/mtd1 
                                    echo "Wgrywanie kernel do /dev/mtd1"
                                    sleep 2                                                     
		                    nandwrite -p /dev/mtd1 //$IMAGE/$TARGET/boot/$VUMODEL.vmlinux.gz                                                                                                     
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel                                       
                        fi
                        sleep 5; reboot -d -f -h -i
            fi
        fi

    fi                       
        
#Ultra
    if [ $BOXNAME = "mbultra" ] || [ $CHIPSET = "bcm7424" ]; then	     
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET                                    
                                else                                  
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/$BOXNAME.vmlinux.gz /tmp/vmlinux.gz 
                                    echo "Kasowanie kernel z /dev/mtd2"
                                    sleep 2 
                                    flash_eraseall /dev/mtd2 0 0
                                    echo "Wgrywanie kernel do /dev/mtd2"                                    
                                    sleep 2
		                    nandwrite -p /dev/mtd2 //tmp/vmlinux.gz 
		                    rm -f //tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"t 
                                fi
                        else
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/$BOXNAME.vmlinux.gz /tmp/vmlinux.gz
                                    echo "Kasowanie kernel z /dev/mtd2"
                                    sleep 2                                    
                                    flash_eraseall /dev/mtd2 0 0 
                                    echo "Wgrywanie kernel do /dev/mtd2"                                    
                                    sleep 2                                                                       
		                    nandwrite -p /dev/mtd2 /tmp/vmlinux.gz 
		                    rm -f /tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"
                        fi
	                sleep 5; reboot -d -f -h -i

###############################
#OSmini
    elif [ $BOXNAME = "osmini" ] || [ $CHIPSET = "BCM7362" ] ; then
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET                                    
                                else                                  
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/$BOXNAME.vmlinux.gz /tmp/vmlinux.gz 
                                    echo "Kasowanie kernel z /dev/mtd0"
                                    sleep 2 
                                    flash_eraseall /dev/mtd0
                                    echo "Wgrywanie kernel do /dev/mtd0"                                    
                                    sleep 2
		                    nandwrite -p /dev/mtd0 //tmp/vmlinux.gz 
		                    rm -f //tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"t 
                                fi
                        else
                                    echo "Przenoszenie pliku kernel do /tmp"
                                    sleep 2
                                    cp -f $IMAGE/$TARGET/boot/$BOXNAME.vmlinux.gz /tmp/vmlinux.gz
                                    echo "Kasowanie kernel z /dev/mtd0"
                                    sleep 2                                    
                                    flash_eraseall /dev/mtd0 
                                    echo "Wgrywanie kernel do /dev/mtd0"                                    
                                    sleep 2                                                                       
		                    nandwrite -p /dev/mtd0 /tmp/vmlinux.gz 
		                    rm -f /tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"
                        fi
	                sleep 5; reboot -d -f -h -i 

            #else
                    #echo "$TARGET "  > /media/neoboot/ImageBoot/.neonextboot
                    #echo "Error - Nie wpierany model STB !!! "
                    #exit 0
            #fi
    else
        echo "$TARGET "  > /media/neoboot/ImageBoot/.neonextboot
        echo "Error - Nie wpierany model STB !!! "
        echo "Prawdopodobnie nie wspieramy tego modelu STB !!!"
        exit 0

    fi
fi
exit 0
