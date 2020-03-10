#! /bin/bash

cp -v /usr/sbin/setup setup.orig

tar -xf smoothwall-fullfirewall.tar.gz -C /

touch /var/smoothwall/mods/fullfirewall/installed

echo "Done untar, switching to install-ffc.pl"
./install-ffc.pl
