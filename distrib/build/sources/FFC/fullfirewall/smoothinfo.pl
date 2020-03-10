#!/usr/bin/perl -w

# Script to return FFC config file data to SmoothInfo.

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

my (@FFC, %netsettings);
my $moddir = "${swroot}/mods/fullfirewall";
&readhash("${swroot}/ethernet/settings", \%netsettings);


push (@FFC, '[b]FFC Configuration files:[/b][code]');

push (@FFC, "$moddir/portfw/aliases file\n\n");
my $aliases = `/bin/cat $moddir/portfw/aliases` if (-s "$moddir/portfw/aliases");
push (@FFC, "$aliases\n");

my $reddev = `/usr/sbin/ip addr show dev $netsettings{'RED_DEV'}`;
push (@FFC, $reddev);
push (@FFC, "===============================================================\n");
push (@FFC, "$moddir/portfw/config file\n\n");

my $portfw = `/bin/cat $moddir/portfw/config` if (-s "$moddir/portfw/config");
chomp ($portfw);
push (@FFC, $portfw);
push (@FFC, "\[/code\]");

return "@FFC";
#print @FFC; print "\n";
