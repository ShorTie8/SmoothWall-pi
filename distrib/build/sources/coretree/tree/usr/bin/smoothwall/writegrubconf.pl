#!/usr/bin/perl
#
# Copyright 2005-2010 SmoothWall Ltd

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %hwprofilesettings;
my %kernelsettings;

&readhash("${swroot}/main/hwprofile", \%hwprofilesettings);
&readhash("${swroot}/main/kernel", \%kernelsettings);

my $append; my $serial;

$append = $hwprofilesettings{'EXTRA_KERNEL_CMDLINE'};

my $file;

open ( $file, "/usr/lib/smoothwall/menu.lst.in" );
my @grub = <$file>;
close ($file);

if ( scalar @ARGV ){
	@specialgrub = <STDIN>;
}

open ( $file, ">/boot/grub/menu.lst" ) or die "Unable to write menu.lst $!";

print $file $serial;

foreach my $line ( @grub ){
	print $file "$line";
}

foreach my $line ( @specialgrub ){
	print $file "$line";
}

my $rootdev = $hwprofilesettings{'ROOT_DEV'};

my $kernelpath = '';
if ( not defined $hwprofilesettings{'BOOT_DEV'} ){
	$kernelpath = '/boot';
}

my $kernels = 0;
foreach my $kerneltype ('runtime', 'runtimebig')
{
	unless (-e "/boot/vmlinuz-$kernelsettings{'CURRENT'}-${kerneltype}") {
		next;
	}
	
	$kernels++;
	
	print $file "title Smoothwall-$kerneltype\n";

	print $file "kernel ${kernelpath}/vmlinuz-$kernelsettings{'CURRENT'}-${kerneltype} root=$rootdev $append\n";
	print $file "initrd ${kernelpath}/initrd-$kernelsettings{'CURRENT'}-${kerneltype}.bz2\n";
	print $file "savedefault\n";

	if ($kernelsettings{'OLD'})
	{
		print $file "title Smoothwall-${kerneltype}-OLD\n";
		if ( defined $grubroot and $grubroot ne '' ){
			print $file "root ($grubroot)\n";
		}
		print $file "kernel ${kernelpath}/vmlinuz-$kernelsettings{'OLD'}-${kerneltype} root=$rootdev $append\n";
		print $file "initrd ${kernelpath}/initrd-$kernelsettings{'OLD'}-${kerneltype}.bz2\n";
	}
}

close($file);

unless ( $kernels ){
	print STDERR "Found no kernels!\n";
	exit -1;
}

exit 0;
