#!/bin/bash
# Beerware by: ShorTie

# load our functions, colors, productdata && RED_DEV
. /etc/rc.d/inc.rc-functions
. /var/smoothwall/main/productdata
. /var/smoothwall/ethernet/settings

if [ "$ARCH" == "pi4-64" ]; then
  echo -e "${BOUL}    Switching GAR to pi4-64 ${NO}"
  echolog "" "s" "" "Switching GAR to pi4-64 "
  mv -v usr/lib/smoothd/sysGAR.so usr/lib/smoothd/sysGAR.so.back
  cp -v usr/lib/smoothd/sysGAR.so.pi4-64 usr/lib/smoothd/sysGAR.so
fi

if [ "$ARCH" == "x86_64" ]; then
  echo -e "${BOUL}    Switching GAR to x86_64 ${NO}"
  echolog "" "s" "" "Switching GAR to x86_64 "
  mv -v usr/lib/smoothd/sysGAR.so usr/lib/smoothd/sysGAR.so.back
  cp -v usr/lib/smoothd/sysGAR.so.x86_64 usr/lib/smoothd/sysGAR.so
fi

echo -e "${BOUL}    Creating GAR symlink ${NO}"
echolog "" "s" "" "Creating GAR symlink "
cd /var/smoothwall/mods
ln -sv ../mods-available/GAR GAR

echo -e "${BOUL}    ...Restarting smoothd to register GAR ${NO}"
echolog "" "s" "" "  ...Restarting smoothd to register GAR "
killall -v smoothd
sleep 0.1
smoothd

echo -e "${BOUL}    Configure GAR to ${DONE} ${RED_DEV} ${NO}"
echolog "" "s" "" "  Configure GAR to ${RED_DEV} "
cd /var/smoothwall/mods-available/GAR/etc
sed -i 's/Interface.*/Interface    ${RED_DEV}/' GAR.conf

echo -e "${BOUL}    Starting GAR ${NO}"
echolog "" "s" "" "  Starting GAR "
smoothcom GARstart
