#!/bin/sh

if [ -f /media/neoboot/NeoBoot_Backup.tar.gz  ] ; then
        rm -R /media/neoboot/NeoBoot_Backupt.tar.gz         
        /bin/tar -czf /media/neoboot/NeoBoot_Backup.tar.gz /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot*/
        echo " "
        echo "Kopia o nazwie NeoBoot_Backup.tar.gz zostala utworzona w lokalizacji:    /media/neoboot . " 
        echo " "
else
        /bin/tar -czf /media/neoboot/NeoBoot_Backup.tar.gz /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot*/
        echo " "
        echo "Kopia o nazwie NeoBoot_Backup.tar.gz zostala utworzona w lokalizacji:    /media/neoboot/ . " 
        echo " "
fi

exit 0
  
