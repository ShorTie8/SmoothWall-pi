#!/bin/bash
# So, So, Sorry : ShorTie

# load our functions && colors
. /etc/rc.d/inc.rc-functions

echo -e "${BOUL}    Stoping GAR ${NO}"
echolog "" "s" "" "  Stoping GAR "
smoothcom GARstop

echo -e "${BOUL}    Deleting GAR symlink ${NO}"
echolog "" "s" "" "Deleting GAR symlink "
cd /var/smoothwall/mods
rm  -v GAR

echo -e "${BOUL}    ...Restarting smoothd to unregister GAR ${NO}"
echolog "" "s" "" "  ...Restarting smoothd to unregister GAR "
killall -v smoothd
sleep 0.1
smoothd
