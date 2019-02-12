Chcesz kupić tuner ? Polecam sklep : http://www.expert-tvsat.com/


Pierwsza instalacja neoboot-a

Uruchom poniższą komendę w terminalu wspieranego tunera:
#

opkg update 

opkg install curl 

curl -kLs https://raw.githubusercontent.com/gutosie/neoboot2/master/iNB.sh|sh
#

Inny sposób na zainstalkowanie, jeśli narzędzie curl nie zadziała poprawnie, to proszę spróbować polecenia :


opkg update

cd /tmp

wget https://raw.githubusercontent.com/gutosie/neoboot2/master/iNB.sh

chmod 0755 /tmp/iNB.sh

/tmp/iNB.sh
#

UWAGA!!! 
 Redystrybucja wersji programu i dokonywania modyfikacji JEST DOZWOLONE, pod warunkiem zachowania niniejszej informacji o prawach autorskich. 

Autor NIE ponosi JAKIEJKOLWIEK odpowiedzialności za skutki użytkowania tego programu oraz za wykorzystanie zawartych tu informacji.

Instalację i modyfikacje przeprowadzasz na wlasne ryzyko!!! Przed instalacją lub aktualizacją Neoboot przeczytaj uważnie wszystkie informacje zawarte tu i w wtyczce. !

Dziękuję wszystkim kolegom wpierającym projekt neoboot.

Dziękuję też kolegom wspierającym projekt.

pozdrawiam gutosie

Wspierane tunery satelitarne:

#cat /proc/stb/info/chipset:  

Ultimo4k            :    7444s 

Solo4k              :    7376  

Zero 4K             :    72604

Duo4k               :    7278  #BCM7278 

Uno 4K              :    7252s 

Uno4kSE             :    7252s  

Ultimo              :    7405(with 3D) 

Uno                 :    7405(with 3D) 

Duo                 :    7335 

Duo2                :    7424 

Zero                :    7362 

Solo                :    7325

Solose              :    7241 

Solose-v2           :    7241 

Solo2               :    7356  
              
Formuler F1         :    bcm7356  

Formuler F3         :    7362       
     
Miraclebox MBmini   :    bcm7358 

Miraclebox Micro    :    bcm7362  

Miraclebox Ultra    :    bcm7424  

  
Octagon Sf8008      :    3798mv200

Octagon SF4008      :    bcm7251

Zgemma h7S          :    bcm7251s 
Zgemma H9S          :

AX HD60 4K          :    hi3798mv200  root@ax60:~# cat /etc/hostname : ax60

OSmini              :    BCM7362

atemio6000          :    bcm7362 




