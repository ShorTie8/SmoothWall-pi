#!/usr/bin/perl
#
# SmoothWall CGIs
#
# (c) 2005-2015 SmoothWall Ltd

use lib ('/usr/lib/smoothwall');
use header qw ( :standard );
use strict;

my (%settings, %netsettings, %hostsettings);

readhash("/var/smoothwall/apcupsd/settings", \%settings);
readhash("${swroot}/ethernet/settings", \%netsettings);
readhash("${swroot}/main/settings", \%hostsettings);

open (FILE, ">/etc/apcupsd/apcupsd.conf");

print FILE <<END;
## apcupsd.conf v1.1 ##
##
##  for apcupsd release 3.14.13 (02 February 2015)
##
## "apcupsd" POSIX config file
#
##
## ========= General configuration parameters ============
##
#
#
LOCKFILE /var/lock
SCRIPTDIR /etc/apcupsd/scripts
NETSERVER on
EVENTSFILE /var/smoothwall/apcupsd/events
EVENTSFILEMAX 25

END

print FILE "NISIP $netsettings{'GREEN_ADDRESS'}\n";
print FILE "TIMEOUT $settings{'TO'}\n";

if ($settings{UPSMODE} eq '0') {
	print FILE "UPSCABLE smart\n";
	print FILE "UPSTYPE apcsmart\n";
	print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '1') {
        print FILE "UPSCABLE usb\n";
        print FILE "UPSTYPE usb\n";
        print FILE "DEVICE\n";
}

if ($settings{UPSMODE} eq '2') {
	print FILE "UPSCABLE smart\n";
	print FILE "UPSTYPE modbus\n";
	print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '3') {
	print FILE "UPSCABLE usb\n";
	print FILE "UPSTYPE modbus\n";
	print FILE "DEVICE\n";
}

if ($settings{UPSMODE} eq '4') {
        print FILE "UPSCABLE ether\n";
        print FILE "UPSTYPE net\n";
        print FILE "DEVICE $settings{'UPSIP'}\n";
}

if ($settings{UPSMODE} eq '5') {
        print FILE "UPSCABLE ether\n";
        print FILE "UPSTYPE pcnet\n";
        print FILE "DEVICE $settings{'UPSIP'}:$settings{'UPSUSER'}:$settings{'UPSAUTH'}\n";
}

if ($settings{UPSMODE} eq '6') {
        print FILE "UPSCABLE 940-0020B\n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '7') {
        print FILE "UPSCABLE 940-0020C\n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '8') {
        print FILE "UPSCABLE 940-0023A \n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '9') {
        print FILE "UPSCABLE 940-0024B \n";
        print FILE "UPSTYPE apcsmart\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '10') {
        print FILE "UPSCABLE 940-0024C \n";
        print FILE "UPSTYPE apcsmart\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '11') {
        print FILE "UPSCABLE 940-0024G \n";
        print FILE "UPSTYPE apcsmart\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '12') {
        print FILE "UPSCABLE 940-0095A \n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '13') {
        print FILE "UPSCABLE 940-0095B \n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '14') {
        print FILE "UPSCABLE 940-0095C \n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '15') {
        print FILE "UPSCABLE 940-0119A \n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '16') {
        print FILE "UPSCABLE 940-0127A \n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '17') {
        print FILE "UPSCABLE 940-0128A \n";
        print FILE "UPSTYPE dumb\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{UPSMODE} eq '18') {
        print FILE "UPSCABLE 940-1524C \n";
        print FILE "UPSTYPE apcsmart\n";
        print FILE "DEVICE $settings{'UPSPORT'}\n";
}

if ($settings{STANDALONE} eq 'on') {
        print FILE "UPSCLASS standalone\n";
        print FILE "UPSMODE disable\n";
}
if ($settings{STANDALONE} eq 'off') {
        print FILE "USPCLASS sharemaster\n";
        print FILE "UPSMODE share\n";
}

        print FILE "POLLTIME $settings{'POLLTIME'}\n";
        print FILE "ONBATTERYDELAY $settings{'BATTDELAY'}\n";
        print FILE "BATTERYLEVEL $settings{'BATTLEVEL'}\n";
        print FILE "MINUTES $settings{'RTMIN'}\n";
        print FILE "ANNOY $settings{'ANNOY'}\n";

if ($settings{UPSNAME} ne '') {
        print FILE "UPSNAME $settings{'UPSNAME'}\n";
}

if ($settings{NISPORT} ne '') {
        print FILE "NISPORT $settings{'NISPORT'}\n";
}

if ($settings{NOLOGINTYPE} eq '0') {
        print FILE "NOLOGON disable\n";
}
if ($settings{NOLOGINTYPE} eq '1') {
        print FILE "NOLOGON percent\n";
}
if ($settings{NOLOGINTYPE} eq '2') {
        print FILE "NOLOGON minutes\n";
}
if ($settings{NOLOGINTYPE} eq '3') {
        print FILE "NOLOGON always\n";
}

close FILE;


if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGONBATTERY} eq 'on') {
  open (FILE, ">/etc/apcupsd/scripts/onbattery");
  print FILE <<END;
#!/bin/sh
#
# UPS on battery alert script
#

export NOTIFYTYPE="ONBATTERY"
export SUBJECT="Utility Power Failure! UPS running on batteries."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
  close FILE;
}
elsif (-f "/etc/apcupsd/scripts/onbattery") {
	unlink("/etc/apcupsd/scripts/onbattery");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGOFFBATTERY} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/offbattery");
	print FILE <<END;
#!/bin/sh
#
# Utility power returned alert script
#

export NOTIFYTYPE="OFFBATTERY"
export SUBJECT="Utility Power Failure! UPS no longer running on batteries."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/offbattery") {
	unlink("/etc/apcupsd/scripts/offbattery");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGCOMMFAILURE} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/commfailure");
	print FILE <<END;
#!/bin/sh
#
# Communication with UPS lost alert script
#

export NOTIFYTYPE="COMMFAILURE"
export SUBJECT="Communication with UPS lost."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/commfailure") {
	unlink("/etc/apcupsd/scripts/commfailure");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGCOMMOK} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/commok");
	print FILE <<END;
#!/bin/sh
#
# Communication with UPS restored alert script
#

export NOTIFYTYPE="COMMOK  "
export SUBJECT="Communication with UPS restored."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/commok") {
	unlink("/etc/apcupsd/scripts/commok");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGCHANGEME} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/changeme");
	print FILE <<END;
#!/bin/sh
#
# UPS battery replacement required alert script
#

export NOTIFYTYPE="CHANGEME"
export SUBJECT="UPS batteries require replacement."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/changeme") {
	unlink("/etc/apcupsd/scripts/changeme");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGANNOY} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/annoyme");
	print FILE <<END;
#!/bin/sh
#
# Annoyme alert script
#

export NOTIFYTYPE="ANNOY   "
export SUBJECT="Power problems with UPS"
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
} 
elsif (-f "/etc/apcupsd/scripts/annoyme") {
	unlink("/etc/apcupsd/scripts/annoyme");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGBATTATTACH} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/battattach");
	print FILE <<END;
#!/bin/sh
#
# Battattach alert script
#

export NOTIFYTYPE="BATTATTACH"
export SUBJECT="UPS Battery has been reconnected."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/battattach") {
	unlink("/etc/apcupsd/scripts/battattach");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGBATTDETACH} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/battdetach");
	print FILE <<END;
#!/bin/sh
#
# Battdetach alert script
#

export NOTIFYTYPE="BATTDETACH"
export SUBJECT="UPS Battery has been disconnected."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/battdetach") {
	unlink("/etc/apcupsd/scripts/battdetach");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGDOSHUTDOWN} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/doshutdown");
	print FILE <<END;
#!/bin/sh
#
# Doshutdown alert script
#

export NOTIFYTYPE="DOSHUTDOWN"
export SUBJECT="UPS initiating Shutdown Sequence."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/doshutdown") {
	unlink("/etc/apcupsd/scripts/doshutdown");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGEMERGENCY} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/emergency");
	print FILE <<END;
#!/bin/sh
#
# Emergency alert script
#

export NOTIFYTYPE="EMERGENCY"
export SUBJECT="Emergency Shutdown. Possible battery failure on UPS."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/emergency") {
	unlink("/etc/apcupsd/scripts/emergency");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGENDSELFTEST} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/endselftest");
	print FILE <<END;
#!/bin/sh
#
# Endselftest alert script
#

export NOTIFYTYPE="ENDSELFTEST"
export SUBJECT="UPS Self Test ended."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/endselftest") {
	unlink("/etc/apcupsd/scripts/endselftest");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGFAILING} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/failing");
	print FILE <<END;
#!/bin/sh
#
# Battery failing alert script
#

export NOTIFYTYPE="FAILING "
export SUBJECT="Battery power exhausted on UPS. Doing shutdown."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/failing") {
	unlink("/etc/apcupsd/scripts/failing");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGKILLPOWER} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/killpower");
	print FILE <<END;
#!/bin/sh
#
# UPS killpower alert script
#

export NOTIFYTYPE="KILLPOWER"
export SUBJECT="Apccontrol doing: /sbin/apcupsd --killpower on UPS!"
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/killpower") {
	unlink("/etc/apcupsd/scripts/killpower");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGLOADLIMIT} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/loadlimit");
	print FILE <<END;
#!/bin/sh
#
# Loadlimit alert script
#

export NOTIFYTYPE="LOADLIMIT"
export SUBJECT="Remaining battery charge below limit on UPS. Doing shutdown."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/loadlimit") {
	unlink("/etc/apcupsd/scripts/loadlimit");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGPOWERBACK} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/mainsback");
	print FILE <<END;
#!/bin/sh
#
# Mainsback alert script
#

export NOTIFYTYPE="MAINSBACK"
export SUBJECT="Utility Power Restored!"
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/mainsback") {
	unlink("/etc/apcupsd/scripts/mainsback");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGPOWEROUT} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/powerout");
	print FILE <<END;
#!/bin/sh
#
# Powerout alert script
#

export NOTIFYTYPE="POWEROUT"
export SUBJECT="Utility Power Failure!"
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/powerout") {
	unlink("/etc/apcupsd/scripts/powerout");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGREMOTEDOWN} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/remotedown");
	print FILE <<END;
#!/bin/sh
#
# Remotedown alert script
#

export NOTIFYTYPE="REMOTEDOWN"
export SUBJECT="Remote Shutdown. Beginning Shutdown Sequence."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/remotedown") {
	unlink("/etc/apcupsd/scripts/remotedown");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGRUNLIMIT} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/runlimit");
	print FILE <<END;
#!/bin/sh
#
# Runlimit alert script
#

export NOTIFYTYPE="RUNLIMIT"
export SUBJECT="Remaining battery runtime below limit on UPS. Doing shutdown."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/runlimit") {
	unlink("/etc/apcupsd/scripts/runlimit");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGSTARTSELFTEST} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/startselftest");
	print FILE <<END;
#!/bin/sh
#
# Startselftest alert script
#

export NOTIFYTYPE="STARTSELFTEST"
export SUBJECT="UPS Self Test started."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/startselftest") {
	unlink("/etc/apcupsd/scripts/startselftest");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{MSGTIMEOUT} eq 'on') {
	open (FILE, ">/etc/apcupsd/scripts/timeout");
	print FILE <<END;
#!/bin/sh
#
# Timeout alert script
#

export NOTIFYTYPE="TIMEOUT "
export SUBJECT="Battery time limit exceeded on UPS. Doing shutdown."
export UPSNAME=\$(hostname)
/usr/bin/smoothwall/upsd-notify.pl

exit 0
END
close FILE;
}
elsif (-f "/etc/apcupsd/scripts/timeout") {
	unlink("/etc/apcupsd/scripts/timeout");
}

if ($settings{'ENABLEALERTS'} eq 'on' and $settings{OPMODE} eq 'testing') {
	open (FILE, ">/etc/apcupsd/scripts/apccontrol");
	print FILE <<END;
#!/bin/sh
#
# Copyright (C) 1999-2002 Riccardo Facchetti <riccardo\@master.oasi.gpa.it>
#
#  for apcupsd release 3.14.10 (13 September 2011)
#
# platforms/apccontrol.  Generated from apccontrol.in by configure.
#
prefix=/etc/apcupsd
exec_prefix=\${prefix}

APCPID=/var/run/apcupsd.pid
APCUPSD=/sbin/apcupsd
SHUTDOWN=/sbin/shutdown
SCRIPTSHELL=/
SCRIPTDIR=/etc/apcupsd/scripts
WALL=wall
#
#
if [ -f \${SCRIPTDIR}/\${1} -a -x \${SCRIPTDIR}/\${1} ]
then
    \${SCRIPTDIR}/\${1} \${2} \${3} \${4}
    # exit code 99 means he does not want us to do default action
    if [ \$? = 99 ] ; then
        exit 0
    fi
fi
#
#
case "\$1" in
#    killpower)
#        echo "Apccontrol doing: \${APCUPSD} --killpower on UPS \${2}"
#        sleep 10
#        \${APCUPSD} --killpower
#    echo "Apccontrol has done: \${APCUPSD} --killpower on UPS \${2}" | \${WALL}
#    ;;
    commfailure)
        echo "Warning communications lost with UPS \${2}" | \${WALL}
    ;;
    commok)
        echo "Communications restored with UPS \${2}" | \${WALL}
    ;;
#
# powerout, onbattery, offbattery, mainsback events occur
#   in that order.
#
    powerout)
    ;;
    onbattery)
        echo "Power failure on UPS \${2}. Running on batteries." | \${WALL}
    ;;
    offbattery)
        echo "Power has returned on UPS \${2}..." | \${WALL}
    ;;
    mainsback)
        if [ -f /etc/apcupsd/powerfail ] ; then
           printf "Continuing with shutdown."  | \${WALL}
        fi
    ;;
    failing)
        echo "Battery power exhaused on UPS \${2}. Doing shutdown." | \${WALL}
   ;;
    timeout)
        echo "Battery time limit exceeded on UPS \${2}. Doing shutdown." | \${WALL}
    ;;
    loadlimit)
        echo "Remaining battery charge below limit on UPS \${2}. Doing shutdown." | \${WALL}
    ;;
    runlimit)
        echo "Remaining battery runtime below limit on UPS \${2}. Doing shutdown." | \${WALL}
    ;;
#    doreboot)
#        echo "UPS \${2} initiating Reboot Sequence" | \${WALL}
#        \${SHUTDOWN} -r now "apcupsd UPS \${2} initiated reboot"
#    ;;
#    doshutdown)
#        echo "UPS \${2} initiated Shutdown Sequence" | \${WALL}
#        \${SHUTDOWN} -h now "apcupsd UPS \${2} initiated shutdown"
#    ;;
    annoyme)
        echo "Power problems with UPS \${2}. Please logoff." | \${WALL}
    ;;
    emergency)
        echo "Emergency Shutdown. Possible battery failure on UPS \${2}." | \${WALL}
    ;;
    changeme)
        echo "Emergency! Batteries have failed on UPS \${2}. Change them NOW" | \${WALL}
    ;;
    remotedown)
        echo "Remote Shutdown. Beginning Shutdown Sequence." | \${WALL}
    ;;
    startselftest)
    ;;
    endselftest)
    ;;
    battdetach)
    ;;
    battattach)
    ;;
    *)  echo "Usage: \${0##*/} command"
        echo "       warning: this script is intended to be launched by"
        echo "       apcupsd and should never be launched by users."
        exit 1
    ;;
esac
END
close FILE;
}

if ($settings{OPMODE} eq 'full') {
	open (FILE, ">/etc/apcupsd/scripts/apccontrol");
	print FILE <<END;
#!/bin/sh
#
# Copyright (C) 1999-2002 Riccardo Facchetti <riccardo\@master.oasi.gpa.it>
#
#  for apcupsd release 3.14.10 (13 September 2011)
#
# platforms/apccontrol.  Generated from apccontrol.in by configure.
#
prefix=/etc/apcupsd
exec_prefix=\${prefix}

APCPID=/var/run/apcupsd.pid
APCUPSD=/sbin/apcupsd
SHUTDOWN=/sbin/shutdown
SCRIPTSHELL=/bin/sh
SCRIPTDIR=/etc/apcupsd/scripts
WALL=wall
#
#
if [ -f \${SCRIPTDIR}/\${1} -a -x \${SCRIPTDIR}/\${1} ]
then
    \${SCRIPTDIR}/\${1} \${2} \${3} \${4}
    # exit code 99 means he does not want us to do default action
    if [ \$? = 99 ] ; then
        exit 0
    fi
fi
#
#
case "\$1" in
    killpower)
        echo "Apccontrol doing: \${APCUPSD} --killpower on UPS \${2}"
        sleep 10
        \${APCUPSD} --killpower
    echo "Apccontrol has done: \${APCUPSD} --killpower on UPS \${2}" | \${WALL}
    ;;
    commfailure)
        echo "Warning communications lost with UPS \${2}" | \${WALL}
    ;;
    commok)
        echo "Communications restored with UPS \${2}" | \${WALL}
    ;;
#
# powerout, onbattery, offbattery, mainsback events occur
#   in that order.
#
    powerout)
    ;;
    onbattery)
        echo "Power failure on UPS \${2}. Running on batteries." | \${WALL}
    ;;
    offbattery)
        echo "Power has returned on UPS \${2}..." | \${WALL}
    ;;
    mainsback)
        if [ -f /etc/apcupsd/powerfail ] ; then
           printf "Continuing with shutdown."  | \${WALL}
        fi
    ;;
    failing)
        echo "Battery power exhaused on UPS \${2}. Doing shutdown." | \${WALL}
   ;;
    timeout)
        echo "Battery time limit exceeded on UPS \${2}. Doing shutdown." | \${WALL}
    ;;
    loadlimit)
        echo "Remaining battery charge below limit on UPS \${2}. Doing shutdown." | \${WALL}
    ;;
    runlimit)
        echo "Remaining battery runtime below limit on UPS \${2}. Doing shutdown." | \${WALL}
    ;;
    doreboot)
        echo "UPS \${2} initiating Reboot Sequence" | \${WALL}
        \${SHUTDOWN} -r now "apcupsd UPS \${2} initiated reboot"
    ;;
    doshutdown)
        echo "UPS \${2} initiated Shutdown Sequence" | \${WALL}
        \${SHUTDOWN} -h now "apcupsd UPS \${2} initiated shutdown"
    ;;
    annoyme)
        echo "Power problems with UPS \${2}. Please logoff." | \${WALL}
    ;;
    emergency)
        echo "Emergency Shutdown. Possible battery failure on UPS \${2}." | \${WALL}
    ;;
    changeme)
        echo "Emergency! Batteries have failed on UPS \${2}. Change them NOW" | \${WALL}
    ;;
    remotedown)
        echo "Remote Shutdown. Beginning Shutdown Sequence." | \${WALL}
    ;;
    startselftest)
    ;;
    endselftest)
    ;;
    battdetach)
    ;;
    battattach)
    ;;
    *)  echo "Usage: \${0##*/} command"
        echo "       warning: this script is intended to be launched by"
        echo "       apcupsd and should never be launched by users."
        exit 1
    ;;
esac
END
close FILE;
}

system("chmod -R 0755 /etc/apcupsd/scripts/");
