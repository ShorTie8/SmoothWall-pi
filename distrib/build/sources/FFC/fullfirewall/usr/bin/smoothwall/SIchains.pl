#!/usr/bin/perl -w

# Script to return FFC chain data (External access, Incoming, Internal, Outgoing) to SmoothInfo.

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

my (%smoothinfosettings, %netsettings, @FFC);
my $moddir = "${swroot}/mods/fullfirewall";

&readhash("${swroot}/smoothinfo/etc/settings", \%smoothinfosettings);
&readhash("${swroot}/ethernet/settings", \%netsettings);

if (($smoothinfosettings{'PORTFW'} eq 'on') && (-s "$moddir/portfw/config")) {
	open (CHAINS, "$moddir/report/incoming") or die 'Unable to open incoming chains file.';
	my @chains = (<CHAINS>);
	close (CHAINS);

	push (@FFC, "\[info=\"FFC Incoming rules\"\]\[code\]");
	foreach my $chain (@chains) {
		chomp ($chain);
		if ($chain eq 'portfwb') {
			my $info = `/usr/sbin/iptables -t mangle -nvL $chain`;
			chomp ($info);
			push (@FFC, $info);
		}
		elsif ($chain eq 'portfw' or $chain eq 'portfw_post') {
			my $info = `/usr/sbin/iptables -t nat -nvL $chain`;
			chomp ($info);
			push (@FFC, $info);
		}
		elsif ($chain eq 'subnetchk' or $chain eq 'portfwf' or $chain eq 'portfwi') {
			my $info = `/usr/sbin/iptables -nvL $chain`;
			chomp ($info);
			push (@FFC, $info);
		}
	}
	push (@FFC, "\[/code\]\[/info\]");
}

if (($smoothinfosettings{'OUTGOING'} eq 'on') && (-s "$moddir/portfw/config")) {
	open (CHAINS, "$moddir/report/outgoing") or die 'Unable to open outgoing chains file.';
	my @chains = (<CHAINS>);
	close (CHAINS);

	push (@FFC, "\[info=\"FFC Outgoing rules\"\]\[code\]");
	foreach my $chain (@chains) {
		chomp ($chain);
		my $info = `/usr/sbin/iptables -t filter -nvL $chain`;
		chomp ($info);
		push (@FFC, $info);
	}
	push (@FFC, "\[/code\]\[/info\]");
}

if (($smoothinfosettings{'XTACCESS'} eq 'on') && (-s "$moddir/xtaccess/config")) {
	open (CHAINS, "$moddir/report/xtaccess") or die 'Unable to open external access chains file.';
	my $chain = (<CHAINS>);
	close (CHAINS);

	push (@FFC, "\[info=\"FFC External access\"\]\[code\]");
	chomp ($chain);
	my $info = `/usr/sbin/iptables -t filter -nvL $chain`;
	chomp ($info);
	push (@FFC, $info);
	push (@FFC, "\[/code\]\[/info\]");
}

if (($smoothinfosettings{'PINHOLES'} eq 'on') && (-s "$moddir/portfw/config")) {
	open (CHAINS, "$moddir/report/internal") or die 'Unable to open internal pinholes chains file.';
	my $chain = (<CHAINS>);
	close (CHAINS);

	push (@FFC, "\[info=\"FFC Internal rules\"\]\[code\]");
	my $info = `/usr/sbin/iptables -t filter -nvL $chain`;
	chomp ($info);
	push (@FFC, $info);
	push (@FFC, "\[/code\]\[/info\]");
}

push (@FFC, "\[info=\"FFC configuration files\"\]\[code\]");

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
push (@FFC, "\[/code\]\[/info\]");

return "@FFC";
#print "@FFC";
