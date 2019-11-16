#!/usr/bin/perl
#
# SmoothWall CGIs
#
# (c) 2005 SmoothWall Ltd

use lib ('/usr/lib/smoothwall');
use SmoothInstall qw( :standard );
use header qw ( :standard );

system("chmod 0666 /etc/apcupsd/apcupsd.conf");

my %settings;

readhash("/var/smoothwall/apcupsd/settings", \%settings);

if ($settings{KILLPOWER} eq 'on') {
@lines = (
 '# See if this is a powerfail situation.                               # ***apcupsd***',
 'if [ -f /etc/apcupsd/powerfail ]; then                                # ***apcupsd***',
 '   echo                                                               # ***apcupsd***',
 '   echo "APCUPSD will now power off the UPS"                          # ***apcupsd***',
 '   echo                                                               # ***apcupsd***',
 '   /var/smoothwall/mods/apcupsd/scripts/apccontrol killpower          # ***apcupsd***',
 '   echo                                                               # ***apcupsd***',
 '   echo "Please ensure that the UPS has powered off before rebooting" # ***apcupsd***',
 '   echo "Otherwise, the UPS may cut the power during the reboot!!!"   # ***apcupsd***',
 '   echo                                                               # ***apcupsd***',
 'fi                                                                    # ***apcupsd***');
$key = "apcupsd";
$pattern = "mount -n -o remount,ro /";
$filename = "/etc/rc.d/rc.halt";
InsertAfter($filename, $key, $pattern, @lines);
} else {
$key = "apcupsd";
$filename = "/etc/rc.d/rc.halt";
Remove($filename, $key);
}