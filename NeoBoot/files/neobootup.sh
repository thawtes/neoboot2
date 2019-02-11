#!/bin/sh
#DESCRIPTION=This script by gutosie

touch /tmp/.init_reboot

if [ -f /etc/init.d/neobootmount.sh ] ; then
    sync; rm -f /etc/init.d/neobootmount.sh;  
fi 
