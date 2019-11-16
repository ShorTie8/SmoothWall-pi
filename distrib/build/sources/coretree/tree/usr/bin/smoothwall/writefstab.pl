#!/usr/bin/perl
#
# Copyright 2005-2010 SmoothWall Ltd

# Must run as root.

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %hwprofile;
my @fsatb;
my $fstabboot, $fstabswap, $fstablog;

my $basic = 'no';
if ( $ARGV[0] eq '--basic' ){
	$basic = 'yes';
}

&readhash("${swroot}/main/hwprofile", \%hwprofile);

my $fs = 'ext3';
if ($hwprofile{'FS'} ne ''){
	$fs = $hwprofile{'FS'};
}

my $file;

open ($file, "/usr/lib/smoothwall/fstab.in");
@fstab = <$file>;
close ($file);

open ($file, "/usr/lib/smoothwall/fstab.boot");
$fstabboot = <$file>;
$fstabboot =~ s/%%DEV%%/$hwprofile{'BOOT_DEV'}/;
$fstabboot =~ s/%%FS%%/$fs/;
close ($file);
open ($file, "/usr/lib/smoothwall/fstab.root");
$fstabroot = <$file>;
$fstabroot =~ s/%%DEV%%/$hwprofile{'ROOT_DEV'}/;
$fstabroot =~ s/%%FS%%/$fs/;
close ($file);
open ($file, "/usr/lib/smoothwall/fstab.swap");
$fstabswap = <$file>;
$fstabswap =~ s/%%DEV%%/$hwprofile{'SWAP_DEV'}/;
close ($file);
open ($file, "/usr/lib/smoothwall/fstab.log");
$fstablog = <$file>;
$fstablog =~ s/%%DEV%%/$hwprofile{'LOG_DEV'}/;
$fstablog =~ s/%%FS%%/$fs/;
close ($file);

open( $file, ">/etc/fstab" );
foreach $line ( @fstab ){
	print $file "$line";
}

if ( $basic eq 'no' ){
	if ( $hwprofile{'ROOT_DEV'} ne '' ) {
		print $file $fstabroot;
	}
	if ( $hwprofile{'BOOT_DEV'} ne '' ) {
		print $file $fstabboot;
	}
	if ( $hwprofile{'SWAP_DEV'} ne '' ) {
		print $file $fstabswap;
	}
	if ( $hwprofile{'LOG_DEV'} ne '' ) {
		print $file $fstablog;
	}
}

close ($file);
