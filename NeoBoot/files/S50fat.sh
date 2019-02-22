#!/bin/sh
# script gutosie

if [ ! -e /usr/bin/ipkg ]; then 
   ln -sfn /usr/bin/opkg /usr/bin/ipkg
fi
if [ ! -e /usr/bin/ipkg-cl ]; then 
   ln -sfn /usr/bin/opkg-cl /usr/bin/ipkg-cl
fi

if [ -f /etc/vtiversion.info ] || [ -f /etc/bhversion ] || [ ! -e /boot/zImage.* ]; then
        /etc/init.d/networking stop; sync; /etc/init.d/networking start
fi
                   
if [ -f /etc/init.d/inadyn-mt ] ; then
    /etc/init.d/inadyn-mt start
fi
                                                
if [ -f /home/root/*.tar.gz ] ; then
    /bin/tar -xzvf /home/root/*.tar.gz -C /; rm /home/root/*.tar.gz
fi

if [ ! -e /media/usb ] ; then
        mkdir -p /media/usb
fi

if [ ! -e /media/hdd ] ; then
        mkdir -p /media/hdd 
fi
                                                
if [ ! -e /media//media/neoboot ] ; then
        mkdir -p /media/media/neoboot
fi
                                                
mount -a -t auto  
rdate -s ntp.task.gda.pl

if [ ! -e /media/neoboot/ImageBoot/.neonextboot ] ; then
    /usr/bin/enigma2_pre_start.sh   
fi
                      
if [ -f /etc/rcS.d/S50fat.sh ] ; then
                            ln -s /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/S50fat.sh /etc/rcS.d/S50neo.sh                                                        
                            telnetd on
                            echo ok  
                            rm -f /etc/rcS.d/S50fat.sh
                            echo "file S50fat.sh delete"  
fi 
echo ok                                                
