#!/usr/bin/perl
#
# Copyright 2005-2010 SmoothWall Ltd

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %hwprofilesettingss;

&readhash("${swroot}/main/hwprofile", \%hwprofilesettings);

my $pipe;

open($pipe, '|-') || exec('/usr/sbin/grub', '--batch') or die "Unable to run grub";

if ($hwprofilesettings{'STORAGE_DEVNODE'})
{
	print $pipe <<END
device (hd0) $hwprofilesettings{'FIRST_STORAGE_DEVNODE'}
root (hd0,0)
setup (hd0)
END
	;
}

close($pipe);

system('/usr/sbin/grub-set-default', '0');
