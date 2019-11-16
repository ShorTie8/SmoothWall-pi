#!/usr/bin/perl
#
# (c) SmoothWall Ltd, 2002

use lib "/usr/lib/smoothwall/";
use header qw( :standard );

my %hwprofilesettings;

&readhash("${swroot}/main/hwprofile", \%hwprofilesettings);

my @partitionmapping = ( 'BOOT', 'SWAP', 'LOG', 'ROOT', );

open(PIPE, '-|') || exec('/sbin/blkid', '-c', '/dev/null', '-o', 'full');

my @allpartitions;

while ( <PIPE> ){
	chomp;
	
	push @blkid, $_;
}

foreach ( sort @blkid )
{
	my %thispartition;
	my ( $devnode ) = ( $_ =~ /^(.*?): / );
	my $rest = $';

	my @pairs = split( / +/, $rest );
	foreach my $pair ( @pairs ){
		my ( $key, $value ) = split( /=/, $pair);
		$value =~ s/[\"\']//g;
		$thispartition{ $key } = $value;
	}

	my $mount = shift @partitionmapping;

	$thispartition{ 'MOUNT' } = $mount;
	$thispartition{ 'DEVNODE' } = $devnode;
	
	push @allpartitions, \%thispartition;
}

foreach my $partition ( @allpartitions ){
	my $uuid = $partition->{ 'UUID' };
	my $label = $partition->{ 'LABEL' };
	my $mount = $partition->{ 'MOUNT' };
	my $devnode = $partition->{ 'DEVNODE' };

	if ( $uuid ){
		$hwprofilesettings{ "${mount}_DEV" } = "UUID=$uuid";
	} elsif ( $label ){
		$hwprofilesettings{ "${mount}_DEV" } = "LABEL=$label";
	} else {
		$hwprofilesettings{ "${mount}_DEV" } = $devnode;
	}
}

if ( $hwprofilesettings{'PROFILE_LOG_RAM' eq '1'} ){
	$hwprofilesettings{'LOG_DEV'} = '/dev/ram0';
}

&writehash("${swroot}/main/hwprofile", \%hwprofilesettings);
