#!/usr/bin/perl
# Smoothinfo CLI reporting script v. 2.2
# Pascal Touch (nanouk) on Smoothwall forums - 2009

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

my $SIdir="${swroot}/smoothinfo";

my (%smoothinfosettings, $response, @chains);
&readhash("${swroot}/smoothinfo/etc/settings", \%smoothinfosettings);
for (keys %smoothinfosettings) {
	$smoothinfosettings{$_} = '';
}

my $ColourRed = "\033[31;1m";
my $ColourGreen = "\033[32;1m";
my $ColourCyan = "\033[36;1m";
my $ColourPurp   = "\033[35;1m";
my $ColourYellow = "\033[33;1m";
my $ColourNorm = "\033[m";

# Set some defaults
$smoothinfosettings{'CONFIG'} = 'on';
$smoothinfosettings{'CONNTYPE'} = 'on';
$smoothinfosettings{'FWPOLICY'} = 'on';
$smoothinfosettings{'NETCONF1'} = 'on';
$smoothinfosettings{'NETCONF2'} = 'on';
$smoothinfosettings{'DISKSPACE'} = 'on';
$smoothinfosettings{'MEMORY'} = 'on';
$smoothinfosettings{'WRAP'} = 100;

system ("/usr/bin/smoothwall/getchains.pl");
open (FILE, "<${SIdir}/etc/chains");
@chains = (@chains,<FILE>);
chomp @chains;

open (OUT, ">",\$smoothinfosettings{'CHAINS'});
foreach (@chains) {
	print OUT "$_,";
}
close (OUT);

print $ColourNorm . "\nBy default, the script will provide info on the" . $ColourYellow 
	. " network configuration type" . $ColourNorm . ", the" .$ColourYellow 
	. " connection type" . $ColourNorm . ",\nthe" . $ColourYellow 
	. " network settings (as saved in /var/smoothwall/ethernet settings)" . $ColourNorm 
	. ", the" . $ColourYellow . " disk space" . $ColourNorm . ",\nthe" . $ColourYellow 
	. " firewall policy" .$ColourNorm . ", the" . $ColourYellow 
	. " state of all interfaces" . $ColourNorm . ", and the" . $ColourYellow 
	. " current state of memory usage" . $ColourNorm . ".\n
Now, before you can generate a basic report (with no logs), would you like to include additional info on:\n";

print $ColourPurp . "\nThe network cards detected by the system? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'ADAPTERS'} = 'on';
} 
else {
	$smoothinfosettings{'ADAPTERS'} = 'off';
}

print $ColourPurp . "\nThe CPU? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'CPU'} = 'on';
}
else {
	$smoothinfosettings{'CPU'} = 'off';
}

print $ColourPurp . "\nThe used IRQ's? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'IRQs'} = 'on';
}
else {
	$smoothinfosettings{'IRQs'} = 'off';
}

print "$ColourPurp \nThe status of stock services"
	." (DHCP, Web proxy, IM proxy, Pop3 proxy, Sip proxy, IDS etc.)? (Y,N) $ColourNorm";
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'SERVICES'} = 'on';
}
else {
	$smoothinfosettings{'SERVICES'} = 'off';
}

print $ColourPurp . "\nThe current DNS settings? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'DNS'} = 'on';
}
else {
	$smoothinfosettings{'DNS'} = 'off';
}

if (-e "${swroot}/dhcp/enable") {
	print $ColourPurp . "\nThe current DHCP settings? (Y,N) " . $ColourNorm;
	$response = "";
	$response = <STDIN>;
	if ($response =~ /y/i) {
		$smoothinfosettings{'DHCPINFO'} = 'on';
	}
	else {
		$smoothinfosettings{'DHCPINFO'} = 'off';
	}
}

print $ColourPurp . "\nThe current IP routing table? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'ROUTE'} = 'on';
}
else {
	$smoothinfosettings{'ROUTE'} = 'off';
}

print $ColourPurp . "\nThe current port forwarding rules? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'PORTFW'} = 'on';
}
else {
	$smoothinfosettings{'PORTFW'} = 'off';
}

print $ColourPurp . "\nThe current firewall rules? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
unless ($response =~ /y/i) {
	$smoothinfosettings{'CHAINS'} = '';
}

print $ColourPurp . "\nThe loaded modules? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'LOADEDMODULES'} = 'on';
}
else {
	$smoothinfosettings{'LOADEDMODULES'} = 'off';
}

print $ColourPurp . "\nThe resource usage snapshot? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'TOP'} = 'on';
}
else {
	$smoothinfosettings{'TOP'} = 'off';
}

print $ColourPurp . "\nThe installed mods? (Y,N) " . $ColourNorm;
$response = "";
$response = <STDIN>;
if ($response =~ /y/i) {
	$smoothinfosettings{'MODLIST'} = 'on';
}
else {
	$smoothinfosettings{'MODLIST'} = 'off';
}

print $ColourCyan . "\nGenerating report...\n\n";

&writehash("${SIdir}/etc/settings", \%smoothinfosettings);
wait();

# header.pm can throw a 'uninitialized value' warning (not error) when reading hash values
# from settings files that include a line break, so redirect to null and ignore.
system ('/usr/bin/smoothwall/smoothinfo.pl >/dev/null 2>&1');

print $ColourGreen . "Done!\n\n";

print $ColourNorm . "Now copy/paste the contents of " . $ColourYellow . "${SIdir}/etc/report.txt " 
	. $ColourNorm . "\"AS IS\"\ninto your post edit box.\n\n";

unlink ("${SIdir}/etc/chains");
