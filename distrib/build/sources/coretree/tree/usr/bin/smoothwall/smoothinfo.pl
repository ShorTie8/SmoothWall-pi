#!/usr/bin/perl -w
# Perl script to gather the info requested  in the UI.
# smoothinfo.pl v. 2.2b (c) Pascal Touch (nanouk) on Smoothwall forums
# smoothinfo.pl v. 2.2c © Neal Murphy (fest3er) on Smoothwall forums;
#     Roadster & SWE3.1 integration and tweaks
# Improved mods sorting routine and the list is now numbered.
# New smoothd module to make SmoothInfo more "compliant".
# Packed using Steve McNeill's Mod Build System.
# Detects mods packed with the Mod Build System.
# Added detection of several additional "non-standard" mods.
# Added IRQ's and Conntracks sections.
# Corrected "double webproxy section" bug.
# Corrected "missing opening info tag square bracket" bug in the screenshot section.
# Added verbosity to the display of firewall rules.
# smoothinfo.pl v. 2.3 Various tweaks to be 'strict' compliant.
# Removed mod specific info. Generic searches and service data provided by mods replaces.
# /var/smoothwall/mods/*/smoothinfo.pl is used to return formatted data displayed in [info=][quote] tags
# Added hooks to override stock chains and proxy reports for mods to generate their own data instead.
# /var/smoothwall/mods/*/usr/bin/smoothwall/SIchains.pl will override chains
# /var/smoothwall/mods/*/usr/bin/smoothwall/SIproxy.pl will override proxy

use lib "/usr/lib/smoothwall";
use header qw( :standard );
#use File::Basename; # Not required as basename & dirname are (now) exported by header.pm.
use File::Find;
use Net::Netmask;
use strict;
use warnings;

# Data::Dumper is great for displaying arrays and hashes.
#use Data::Dumper;

my $SIdir= "${swroot}/smoothinfo";
my $MODDIR = "$SIdir/etc";
require "${SIdir}/about.ph";

my ($line, $block, $netmask, $bcast, $netmask_tag, $howlong, @newarray, @livered);
my ($dns1_tag, $dns2_tag, $redIP_tag, $bcast_tag, $remoteIP_tag, $swe_version) = ('', '', '', '', '', '');
my (%productdata, %pppsettings, %modemsettings, %netsettings, %smoothinfosettings, %defseclevelsettings, 
	%green_dhcpsettings, %purple_dhcpsettings, %orange_dhcpsettings, %imsettings, %p3scansettings, 
	%sipproxysettings, %proxysettings, %SSHsettings, %snortsettings, %apcupsdsettings, %ntpsettings, 
	%qossettings, %qoslocalsettings, %modinfo, %DETAILS, %servicenames, %adslsettings);

&readhash("${swroot}/smoothinfo/etc/settings", \%smoothinfosettings);
&readhash("${swroot}/main/productdata", \%productdata);
&readhash("${swroot}/ppp/settings", \%pppsettings) if (-s "${swroot}/ppp/settings");
&readhash("${swroot}/modem/settings", \%modemsettings) if (-s "${swroot}/modem/settings");
&readhash("${swroot}/ethernet/settings", \%netsettings);
&readhash("${swroot}/main/settings", \%defseclevelsettings);

# stock services
&readhash("${swroot}/im/settings", \%imsettings) if (-s "${swroot}/im/settings");
&readhash("${swroot}/p3scan/settings", \%p3scansettings) if (-s "${swroot}/p3scan/settings");
&readhash("${swroot}/sipproxy/settings", \%sipproxysettings) if (-s "${swroot}/sipproxy/settings");
&readhash("${swroot}/proxy/settings", \%proxysettings) if (-s "${swroot}/proxy/settings");
&readhash("${swroot}/snort/settings", \%snortsettings) if (-s "${swroot}/snort/settings");
&readhash("${swroot}/remote/settings", \%SSHsettings) if (-s "${swroot}/remote/settings");
&readhash("${swroot}/apcupsd/settings", \%apcupsdsettings) if (-s "${swroot}/apcupsd/settings");
&readhash("${swroot}/time/settings", \%ntpsettings) if (-s "${swroot}/time/settings");
&readhash("${swroot}/dhcp/settings-green", \%green_dhcpsettings) if (-s "${swroot}/dhcp/settings-green");
&readhash("${swroot}/dhcp/settings-purple", \%purple_dhcpsettings) if (-s "${swroot}/dhcp/settings-purple");
&readhash("${swroot}/dhcp/settings-orange", \%orange_dhcpsettings) if (-s "${swroot}/dhcp/settings-orange");
&readhash("${swroot}/traffic/settings", \%qossettings) if (-s "${swroot}/traffic/settings");
&readhash("${swroot}/traffic/localsettings", \%qoslocalsettings) if (-s "${swroot}/traffic/localsettings");
&readhash("${swroot}/adsl/settings", \%adslsettings) if (-s "${swroot}/adsl/settings");

my $outputfile = "${SIdir}/etc/report.txt";

# MEMORY
my $memory = `/usr/bin/free -ot`;
chomp ($memory);

# CPU
open (CPUDATA, "/proc/cpuinfo") || die "Unable to open $!"; 
my @cpudata = (<CPUDATA>); 
close (CPUDATA);

my ($cpu, $frequency, $cache, $physCores);
foreach (@cpudata) {
	chomp $_;
	$cpu = $' if (/^model name\s+:\s+/);
	$frequency = $' if (/^cpu MHz\s+:\s+/);
	$cache = $' if (/^cache size\s+:\s+/);
	$physCores = $' if (/^cpu cores\s+:\s+/);
}

$physCores = '1' unless ($physCores);

my $cpuCores = grep { /^processor\s+:/ } @cpudata;
chomp ($cpuCores);

#IRQ's
opendir (DIR, "/proc/irq") || die "Unable to open $!"; 
my @IRQs = '';
my $warning = '';
my @files = sort { $a <=> $b } (grep { /^\d+$/ } readdir DIR);
foreach (@files) {
	opendir (IRQS, "/proc/irq/$_");
	my $device = "";
	foreach (readdir IRQS) {
		next if /\./;
		next if /\.\./;
		next if /affinity_hint/;
		next if /node/;
		next if /smp_affinity/;
		next if /spurious/;
		#print "$_\n";
		$device .= "$_, ";
	}
	closedir (IRQS);
	chop ($device);
	chop ($device);
	if ($device) {
		if ($device =~ /,/) {
			push (@IRQs, "IRQ $_ used by $device\t<==\n");
			$warning = "There seems to be at least one shared IRQ in your system!\n";
		}
		else {
			push (@IRQs, "IRQ $_ used by $device\n");
		}
	}
}
closedir (DIR);

#CONNTRACKS
my $conntracks = `wc -l < /proc/net/ip_conntrack`;
$conntracks .= "\n";
$conntracks .= `/bin/cat /proc/net/ip_conntrack`;
chomp ($conntracks);

# DISKSPACE
my $diskspace = &pipeopen( '/bin/df', '-h' );
chomp ($diskspace);

# ETHERNET ADAPTERS
open (LSPCI, "/usr/sbin/lspci|");
my @ethernet_adapters = '';
foreach (<LSPCI>){
	if (/Ethernet/) {
		$_ =~ s/^(.*)Ethernet controller: //;
		push (@ethernet_adapters, $_);
	}
}
close (LSPCI);


# IF statuses, addrs, pegs, etc.

# Get the 'real' red iface when connected
$netsettings{'RED_DEV'} = &readvalue("${swroot}/red/iface") if (-e "${swroot}/red/active");

# Get the link, addrs and stats for each active IF. GREEN must always be done first
my @netconf;
push (@netconf, &getLinkData($netsettings{"GREEN_DEV"}, "green")) if ($netsettings{'GREEN_DEV'});
push (@netconf, &getLinkData($netsettings{"ORANGE_DEV"}, "orange")) if ($netsettings{'ORANGE_DEV'});
push (@netconf, &getLinkData($netsettings{"PURPLE_DEV"}, "purple")) if ($netsettings{'PURPLE_DEV'});
push (@netconf, &getLinkData($netsettings{"RED_DEV"}, "red")) if ($netsettings{'RED_DEV'});

## Get all IFs that have peg counts
open (DEV, "/proc/net/dev");
my @dev = <DEV>;
close DEV;

## Tidy up
chomp (@dev);
shift @dev;
shift @dev;

# Check 'em all
foreach (@dev) {
	# Split and trim
	my @tmp = split;
	$tmp[0] =~ s/://;

	# Skip the obvious; we don't want repeats
	next if ($netsettings{'GREEN_DEV'} && $tmp[0] =~ /$netsettings{'GREEN_DEV'}/);
	next if ($netsettings{'ORANGE_DEV'} && $tmp[0] =~ /$netsettings{'ORANGE_DEV'}/);
	next if ($netsettings{'PURPLE_DEV'} && $tmp[0] =~ /$netsettings{'PURPLE_DEV'}/);
	next if ($netsettings{'RED_DEV'} && $tmp[0] =~ /$netsettings{'RED_DEV'}/);

	# If an IF saw traffic, get its info
	if ($tmp[1] > 0 || $tmp[2] > 0 || $tmp[9] > 0 || $tmp[10] > 0 ) {
		push (@netconf, &getLinkData($tmp[0], "grey"));
	}
}

# 'LIVE' NET SETTINGS
# Define the 'not used' tags that show when values in net settings are no used.
my $not_used = " \[/b\]\[/color\]\[/size\]\[size=85\]\[color=grey\]\[i\]<not used>\[/i\]\[/color\]\[/size\]\[size=90\]";
my $orange_notused = $not_used."\[color=orange\]\[b\]";
my $purple_notused = $not_used."\[color=purple\]\[b\]";
my $red_notused    = $not_used."\[color=red\]\[b\]";

# Define the actual values on a pppoX connected system
my (@red, @green, @purple, @orange, @other, @live_red);
if (($netsettings{'RED_TYPE'} eq 'DHCP' || 
     $netsettings{'RED_TYPE'} eq 'PPPOE') && (-e "${swroot}/red/active")) {
	if (-s "${swroot}/red/dns1") {
		my $redDNS1 = &readvalue("${swroot}/red/dns1");
		$dns1_tag = "$red_notused" if (!$netsettings{'DNS1'} || $netsettings{'DNS1'} ne $redDNS1);
		$netsettings{'DNS1'} = $redDNS1;
	}
	else { 
		my $redDNS1 = "Not Configured";
		$dns1_tag = "$red_notused";
	}

	unless (-z "/var/smoothwall/red/dns2") {
		my $redDNS2 = &readvalue("${swroot}/red/dns2");
		$dns2_tag = "$red_notused" if (!$netsettings{'DNS2'} || $netsettings{'DNS2'} ne $redDNS2);
		$netsettings{'DNS2'} = $redDNS2;
	}
	else { 
		my $redDNS2 = "Not Configured";
		$dns2_tag = "$red_notused";
	}

	my $redIP = &readvalue("${swroot}/red/local-ipaddress");
	$redIP_tag = "$red_notused" if ($netsettings{'RED_ADDRESS'} ne $redIP);
	$netsettings{'RED_ADDRESS'} = $redIP;

	my $remoteIP = &readvalue("${swroot}/red/remote-ipaddress");
	$remoteIP_tag = "$red_notused" if (!$netsettings{'DEFAULT_GATEWAY'} || $netsettings{'DEFAULT_GATEWAY'} ne $remoteIP);
	$netsettings{'DEFAULT_GATEWAY'} = $remoteIP;

  	# Let's get the broadcast and netmask of the red iface when up
	# IP ADDR
	open (IPADDR_RED, "/usr/sbin/ip addr show $netsettings{'RED_DEV'}|");
	my @temp = <IPADDR_RED>;
	close (IPADDR_RED);

	foreach $line (@temp) {
		chomp $line;
		$line =~ s/^\s+//;
		if ($line =~ /inet /) {
			@newarray = split /\s+/, $line;
			$block = new Net::Netmask($newarray[1]);
			$netmask = $block->mask();
			$bcast = $newarray[3];
			$bcast = '' if ($netsettings{'RED_DEV'} =~ /ppp/);
			last;
		}
	}
	$bcast_tag = "$red_notused" if ($netsettings{'RED_BROADCAST'} ne $bcast);
	$netsettings{'RED_BROADCAST'} = $bcast;
	$netmask_tag = "$red_notused" if ($netsettings{'RED_NETMASK'} ne $netmask);
	$netsettings{'RED_NETMASK'} = $netmask;
	&writehash("$MODDIR/livesettings", \%netsettings);

	open (LIVESETTINGS,"<$MODDIR/livesettings");
	while (<LIVESETTINGS>) {
		push (@livered, $_) if (/RED|DNS|GATEWAY/);
	}
	@live_red = sort @livered;
	@live_red = ("\[color=red\]\[b\]@live_red\[/b\]\[/color\]");
	close (LIVESETTINGS);
}

# Opening /var/smoothwall/ethernet/settings regardless of the connection state.
# This file is not updated when on pppoe and/or dhcp and when you are disconnected/reconnected,
# and possibly when you subsequently run setup.

open (NETSETTINGS,"<${swroot}/ethernet/settings") || die "Unable to open $!";
while (<NETSETTINGS>) {
	chomp;
	if (/DNS1[^_]/) {
		push (@red, "$_" . $dns1_tag . "\n");
	}
	elsif (/DNS2[^_]/) {
		push (@red, "$_" . $dns2_tag . "\n");
	}
	elsif (/DNS[12]_/) {
		push (@red, "$_\n");
	}
	elsif (/GATEWAY/) {
		push (@red, "$_" . $remoteIP_tag . "\n");
	}
	elsif (/RED_ADDRESS/) {
		push (@red, "$_" . $redIP_tag . "\n");
	}
	elsif (/RED_BROADCAST/) {
		push (@red, "$_" . $bcast_tag . "\n");
	}
	elsif (/RED_NETMASK/) {
		push (@red, "$_" . $netmask_tag . "\n");
	}
	elsif (/RED_D.*/) {
		push (@red, "$_\n");
	}
	elsif (/RED_IGNORE.*/) {
		push (@red, "$_\n");
	}
	elsif (/RED_N.*/) {
		push (@red, "$_\n");
	}
	elsif (/RED_T.*/) {
		push (@red, "$_\n");
	}
	elsif (/RED_MAC/) {
		push (@red, "$_\n");
	}
	elsif (/GREEN/) {
		push (@green, "$_\n");
	}
	elsif ($netsettings{'PURPLE_DEV'} eq "" && /PURPLE/) {
		push (@purple, "$_" . $purple_notused . "\n");
	}
	elsif ($netsettings{'PURPLE_DEV'} ne "" && /PURPLE/) {
		push (@purple, "$_\n");
	}
	elsif ($netsettings{'ORANGE_DEV'} eq "" && /ORANGE/) {
		push (@orange, "$_" . $orange_notused . "\n");
	}
	elsif ($netsettings{'ORANGE_DEV'} ne "" && /ORANGE/) {
		push (@orange, "$_\n");
	}
	else { 
		push (@other, "$_\n\n");
	}
}

close (NETSETTINGS);
@green = sort @green;
@green = ("\[color=green\]\[b\]", @green, "\[/b\]\[/color\]\n");
@red = sort @red;
@red = ("\[color=red\]\[b\]", @red, "\[/b\]\[/color\]");
@purple = sort @purple;
@purple = ("\[color=purple\]\[b\]", @purple, "\[/b\]\[/color\]\n");
@orange = sort @orange;
@orange = ("\[color=orange\]\[b\]", @orange, "\[/b\]\[/color\]\n");
@other = sort @other;

my $note = '';
if ($netsettings{'RED_TYPE'} eq 'DHCP' || $netsettings{'RED_TYPE'} eq 'PPPOE') {
	$note = "$tr{'smoothinfo-note'}\n\n";
}
my @ethernet_settings = ("\[color=\#400000\]\[i\]$note\[/i\]\[/color\]", "\[size=90\]", @other,@green,@orange,@purple,@red, "\[/size\]");
my @live_settings = ("\[size=90\]", @other,@green,@orange,@purple,@live_red, "\[/size\]");

# ROUTING
my $route = &pipeopen( '/usr/sbin/ip', 'route' );

# IPTABLES CHAINS
my @chains = split (/,/,$smoothinfosettings{'CHAINS'});

# MODS
my %modlist;
our $modpath;

opendir(DIR, $modpath) or die "Cannot open directory: '$modpath': $!";

while ( my $entry = readdir DIR ) {
	next if $entry =~ /^\./;
	next unless (-d "$modpath/$entry");

	if (-s "$modpath/$entry/DETAILS") {
		($DETAILS{'MOD_NAME'}, $DETAILS{'MOD_LONG_NAME'}, $DETAILS{'MOD_VERSION'}, $DETAILS{'MOD_INFO'}) = ('', '', '', '');
		&readhash("$modpath/$entry/DETAILS", \%DETAILS);
		if ($DETAILS{'MOD_LONG_NAME'}) {
			$modlist{$entry} = "$DETAILS{'MOD_LONG_NAME'} $DETAILS{'MOD_VERSION'} $DETAILS{'MOD_INFO'}";
		}
		else {
			$modlist{$entry} = "$DETAILS{'MOD_NAME'} $DETAILS{'MOD_VERSION'} $DETAILS{'MOD_INFO'}";
		}
	}
	elsif (-s "$modpath/$entry/installed") {
		my $installed = &readvalue ("$modpath/$entry/installed");
		$installed =~ s/#//;
		$installed =~ s/^\s+//;
		$modlist{$entry} = "$installed";
	}
	else {
		$modlist{$entry} = "$entry for SWE 3.1";
	}
}
closedir (DIR);

# MODULES
my $modules = &pipeopen( '/bin/lsmod' );
open (TOP, "/usr/bin/top -b -n 1|");

my @top = (<TOP>);
close (TOP);
pop (@top);

# CONFIG
my ($RED, $reddev, $ORANGE, $orangedev, $PURPLE, $purpledev) = ('', '', '', '', '', '');

open (ETHERSETTINGS,"<${swroot}/ethernet/settings") || print "Unable to open $!";
my @ethersettings = <ETHERSETTINGS>;
close (ETHERSETTINGS);

$reddev = (grep /RED_DEV=eth/, @ethersettings)[0] if ($netsettings{'RED_DEV'});
$orangedev = (grep /ORANGE_DEV=eth/, @ethersettings)[0] if ($netsettings{'ORANGE_DEV'});
$purpledev = (grep /PURPLE_DEV=eth/, @ethersettings)[0] if ($netsettings{'PURPLE_DEV'});
chomp $reddev if ($reddev);
chomp $orangedev if ($orangedev);
chomp $purpledev if ($purpledev);


###################  Report Generation  ###################  

my $reportDate = `/bin/date +"%Y/%m/%d %H:%M:%S"`;
chomp $reportDate;
open (FILE,">$outputfile") || die 'Unable to open file';
print FILE "\[size=110\]\[color=purple\]\[u\]\[b\]$tr{'smoothinfo-generated'}${reportDate}\[/b\]\[/u\]\[/color\]\[/size\]\n\n";


### Smoothwall Section
print FILE "\n\[u\]\[b\]Smoothwall $displayVersion\[/b\]\[/u\]\n";

chomp %smoothinfosettings;

# Generate the ASCII schematic (ugly but works)
my ($orange, $purple) = ('', '');
$orange = '(orange)' if ($orangedev);
$purple = '(purple)' if ($purpledev);

if (-e "$MODDIR/schematic") {
	print FILE "\[info=\"$tr{'smoothinfo-ascii-schematic'}\"\]\[code\]";

	# RED
	print FILE "                                            Internet\n";
	print FILE "                                               |\n";
	if ($smoothinfosettings{'MODEM'} eq 'on') {
		print FILE "                                             Modem\n";
		print FILE "                                               |\n";
	}
	if ($smoothinfosettings{'ROUTER'} eq 'on') {
		print FILE "                                             Router\n";
		print FILE "                                               |\n";
	}
	print FILE "                                             (red)\n";

	# ORANGE
	if (($orangedev) && $smoothinfosettings{'SWITCH2'} eq 'on') {
		if ($smoothinfosettings{'WAP2'} eq 'on') {
			print FILE "  WLan <=== WAP <=== Switch <=== $orange ";
		}
		else {
			print FILE "                     Switch <=== $orange ";
		}
		print FILE "\[SMOOTHWALL\] (green)";
	}
	elsif (($orangedev) && $smoothinfosettings{'WAP3'} eq 'on') {
		print FILE "              WLan <=== WAP <=== $orange \[SMOOTHWALL\] (green)";
	}
	elsif ($orangedev) {
		print FILE "                                 $orange \[SMOOTHWALL\] (green)";
	}
	else {
		print FILE "                                          \[SMOOTHWALL\] (green)";
	}

	# GREEN
	if ($smoothinfosettings{'SWITCH1'} eq 'on') {
		if ($smoothinfosettings{'WAP1'} eq 'on') {
			print FILE " ===> Switch ===> WAP ===> WLan";
		}
		else {
			print FILE " ===> Switch";
		}
	}
	elsif ($smoothinfosettings{'WAP4'} eq 'on') {
		print FILE " ===> WAP ===> WLan";
	}

	# PURPLE
	if (($purpledev) && $smoothinfosettings{'WAP6'} eq 'on' && $smoothinfosettings{'SWITCH3'} eq 'on') {
		print FILE "\n                                            $purple\n";
		print FILE "                                               |\n";
		print FILE "                                             Switch\n";
		print FILE "                                               |\n";
		print FILE "                                              WAP\n";
		print FILE "                                               |\n";
		print FILE "                                             W/LAN";
	}
	elsif (($purpledev) && $smoothinfosettings{'WAP6'} ne 'on' && $smoothinfosettings{'SWITCH3'} eq 'on') {
		print FILE "\n                                            $purple\n";
		print FILE "                                               |\n";
		print FILE "                                             Switch";
	}
	elsif (($purpledev) && $smoothinfosettings{'WAP5'} eq 'on') {
		print FILE "\n                                            $purple\n";
		print FILE "                                               |\n";
		print FILE "                                              WAP\n";
		print FILE "                                               |\n";
		print FILE "                                             W/LAN";
	}
	elsif ($purpledev) {
		print FILE "\n                                            $purple\n";
	}
	else {
		print FILE "\n";
	}
	print FILE "\[/code\]\[/info\]";
}

# How to determine what's available and what isn't, because values aren't necessarily deleted
# from network/settings. (It's nice to have them reappear later.)
#   CT = netsettings{'CONFIG_TYPE'}
#   GREEN is always configurable
#   CT & 1: 0 - ORANGE is not included; 1 - ORANGE is configurable
#   CT & 2: 0 - RED is NOT LAN; 1 - RED is LAN
#   CT & 4: 0 - PURPLE is not included; 1 - PURPLE is configurable

# Configuration type
if ($smoothinfosettings{'CONFIG'} eq 'on') {
	if ($netsettings{'CONFIG_TYPE'} & 2) {
		# RED is NIC
		# Pre-match as the unknown catchall
		$RED = "RED (Unknown LAN)";
      
		if ($netsettings{'RED_TYPE'} eq "STATIC") {
			$RED = "RED (STATIC)";
		}
		elsif ($netsettings{'RED_TYPE'} eq "DHCP") {
			$RED = "RED (DHCP)";
		}
		elsif ($netsettings{'RED_TYPE'} eq "PPPOE") {
			if ($pppsettings{'COMPORT'} eq "PPPoE") {
				$RED = "RED (PPPoE)";
			}
			else {
				$RED = "RED (PPPoE/$pppsettings{'COMPORT'})";
			}
		}
	}
	else {
		# RED is PPP
		# Pre-match as the unknown catchall
		$RED = "RED (Unknown PPP)";
      
		if ($pppsettings{'COMPORT'}) {
			if ($pppsettings{'COMPORT'} =~ /^tty/) {
				$RED = 'RED (Dial-Up/Cellular)';
			}
			elsif ($pppsettings{'COMPORT'} =~ /^isdn/) {
				$RED = 'RED (ISDN)';
			}
			elsif ($adslsettings{'ENABLED'}  eq "on") {
				$RED = 'RED (ADSL)';
			}
		}
	}
	$ORANGE = '-ORANGE' if ($netsettings{'CONFIG_TYPE'} & 1);
	$PURPLE = '-PURPLE' if ($netsettings{'CONFIG_TYPE'} & 4);

	print FILE "\[info=\"$tr{'smoothinfo-firewall-config-type'}\"\]\[code\]$RED-GREEN$ORANGE$PURPLE\[/code\]\[/info\]";
}

# Firewall policy
# Check for replacement chain data (xtaccess, portfw, dmzholes, outgoing) from FFC and other mods
my @chainfiles = </var/smoothwall/mods/*/usr/bin/smoothwall/SIchains.pl>;
chomp @chainfiles;

if ($smoothinfosettings{'FWPOLICY'} eq 'on') {
	if ($defseclevelsettings{'OPENNESS'} eq 'halfopen') {
		$smoothinfosettings{'SECPOLICY'} = 'Half-open';
	}
	elsif ($defseclevelsettings{'OPENNESS'} eq 'open') {
		$smoothinfosettings{'SECPOLICY'} = 'Open';
	}
	elsif ($defseclevelsettings{'OPENNESS'} eq 'closed') {
		$smoothinfosettings{'SECPOLICY'} = 'Closed';
	}
	else {
		$smoothinfosettings{'SECPOLICY'} = '(Unknown)';
	}

	if (@chainfiles) {
		print FILE "\[info=\"$tr{'smoothinfo-default-secpol'}\"\]\[code\]$tr{'smoothinfo-policy'}: N/A - Mod policy exists\[/code\]\[/info\]";
	}
	else {
		print FILE "\[info=\"$tr{'smoothinfo-default-secpol'}\"\]\[code\]$tr{'smoothinfo-policy'}: $smoothinfosettings{'SECPOLICY'}\n";
		if (open (OUTGOING, "<${swroot}/outgoing/settings")) {
			foreach (<OUTGOING>) {
				if (grep /GREEN=REJECT/, $_) {
					my $rule_green = "$tr{'smoothinfo-traffic-originating'} GREEN is: $tr{'smoothinfo-allowed'}";
					print FILE "$rule_green\n";
				}
				if (grep /GREEN=ACCEPT/, $_) {
					my $rule_green = "$tr{'smoothinfo-traffic-originating'} GREEN is: $tr{'smoothinfo-blocked'}";
					print FILE "$rule_green\n";
				}
				if (($netsettings{"ORANGE_DEV"}) && grep /ORANGE=REJECT/, $_) {
					my $rule_orange = "$tr{'smoothinfo-traffic-originating'} ORANGE is: $tr{'smoothinfo-allowed'}";
					print FILE "$rule_orange\n";
				}
				if (($netsettings{"ORANGE_DEV"}) && grep /ORANGE=ACCEPT/, $_) {
					my $rule_orange = "$tr{'smoothinfo-traffic-originating'} ORANGE is: $tr{'smoothinfo-blocked'}";
					print FILE "$rule_orange\n";
				}
				if (($netsettings{"PURPLE_DEV"}) && grep /PURPLE=REJECT/, $_) {
					my $rule_purple = "$tr{'smoothinfo-traffic-originating'} PURPLE is: $tr{'smoothinfo-allowed'}";
					print FILE "$rule_purple\n";
				}
				if (($netsettings{"PURPLE_DEV"}) && grep /PURPLE=ACCEPT/, $_) {
					my $rule_purple = "$tr{'smoothinfo-traffic-originating'} PURPLE is: $tr{'smoothinfo-blocked'}";
					print FILE "$rule_purple\n";
				}
			}
			close OUTGOING;
		}
		print FILE "\[/code\]\[/info\]";
	}
}

# Installed Mods
if ($smoothinfosettings{'MODLIST'} eq 'on') {
	my ($number, $suffix) = ('', '');
	$number = scalar (keys(%modlist)) if (%modlist);
	$suffix = 's' if (($number) && $number gt 1);

	my $id = 0;
	if (%modlist) {
		print FILE "\[info=\"$tr{'smoothinfo-mods2'}$suffix - $number detected\"\]\[code\]";
		my @sorted = sort { lc($modlist{$a}) cmp lc($modlist{$b}) } keys %modlist;
		foreach(@sorted) {
			$id++;
			chomp ($modlist{$_});
			print FILE "$id - $modlist{$_}\n";
		}
		print FILE "\[/code\]\[/info\]";
	}
}

#Service status
my (%coreservices, %stockservices, %specialcases, @modservices);
if ($smoothinfosettings{'SERVICES'} eq 'on') {
	# Status of core services
	print FILE "\[info=\"$tr{'smoothinfo-services-status'} - Core\"\]\[code\]";

	# Find all core services and prepare them.
	my @svcfiles = </usr/lib/smoothwall/services/*>;
	chomp @svcfiles;

	foreach my $corefile ( sort @svcfiles ) {
		my $dirname  = dirname($corefile);
		my $basename = basename($corefile);

		open (SERVICE, "<$dirname/$basename" ) or next;
		my ( $name, $rel ) = split /,/, <SERVICE>;
		close (SERVICE);

		next if ( not defined $rel );

		chomp $name;
		chomp $rel;
		my $servicename = $basename;
		$servicename =~s/\[RED\]/$netsettings{'RED_DEV'}/ig;
		$servicename =~s/-/\//g;
		$coreservices{ $tr{ $name } } = $servicename if ( $rel eq "core" );
	}
	print FILE "Firewall Rules: Non-Standard\n" if (@chainfiles);
	foreach my $key (sort keys %coreservices) {
		print FILE "$key: " . ucfirst (&isrunning($coreservices{$key})) . "\n";
	}
	print FILE "\[/code\]\[/info\]";

	# Status of stock services
	print FILE "\[info=\"$tr{'smoothinfo-services-status'} - Stock\"\]\[code\]";

	# Find all stock services and prepare them.
	foreach my $stockfile ( sort @svcfiles ) {
		my $dirname  = dirname($stockfile);
		my $basename = basename($stockfile);

		open (SERVICE, "<$dirname/$basename" ) or next;
		my ( $name, $rel ) = split /,/, <SERVICE>;
		close (SERVICE);

		chomp $rel if ($rel);
		next if ( defined $rel and $rel eq "core" );

		chomp $name;
		my $servicename = $basename;
		$servicename =~s/\[RED\]/$netsettings{'RED_DEV'}/ig;
		$servicename =~s/-/\//g;
		$stockservices{ $tr{$name}} = $servicename;
	}
	foreach my $key (sort keys %stockservices) {
		print FILE "$key: " . ucfirst (&isrunning($stockservices{$key})) . "\n";
		if ($key =~ /DHCP/) {
			print FILE "DHCP server on green: $green_dhcpsettings{'ENABLE'}\n" if ($green_dhcpsettings{'ENABLE'});
			print FILE "DHCP server on purple: $purple_dhcpsettings{'ENABLE'}\n" if ($purple_dhcpsettings{'ENABLE'});
			print FILE "DHCP server on orange: $orange_dhcpsettings{'ENABLE'}\n" if ($orange_dhcpsettings{'ENABLE'});
		}
	}
	print FILE "\[/code\]\[/info\]";

	# Find all mod services and prepare them.
	my @modsvcfiles = </var/smoothwall/mods/*/usr/lib/smoothwall/services/*>;
	chomp @modsvcfiles;

	foreach my $modfile ( sort @modsvcfiles ) {
		my $dirname  = dirname($modfile);
		my $basename = basename($modfile);

		open (SERVICE, "<$dirname/$basename" ) or next;
		my ( $name, $rel ) = split /,/, <SERVICE>;
		close (SERVICE);

		chomp $name;
		chomp $rel if ($rel);
		my $servicename = $basename;
		$servicename =~s/\[RED\]/$netsettings{'RED_DEV'}/ig;
		$servicename =~s/-/\//g;

		if ( defined $rel and $rel eq "special" ) {
			# Another extension of ModInstall: allow mods with 'special case' status checks
			$servicenames{ $tr{$name}} = $servicename;
			$specialcases{ $basename } = "$dirname/../../../bin/smoothwall/$basename-status.pl";
		}
		else {	
			$servicenames{ $tr{$name}} = $servicename;
		}
	}

	foreach my $key (sort keys %servicenames) {
		push (@modservices, "$key: " . ucfirst (&isrunning($servicenames{$key})) . "\n");
	}
	unshift (@modservices, "\[info=\"$tr{'smoothinfo-mod-services-status'}\"\]\[code\]");
	push (@modservices, "\[/code\]\[/info\]");

	# If at least one mod is found create the section
	my $test = @modservices;
	print FILE @modservices if ($test > 2);
}

### Networking Section
if ($smoothinfosettings{'DNS'} eq 'on' or
    $smoothinfosettings{'NETCONF1'} eq 'on' or
    $smoothinfosettings{'NETCONF2'} eq 'on' or
    $smoothinfosettings{'DHCPINFO'} eq 'on' or
    $smoothinfosettings{'ROUTE'} eq 'on') {
	print FILE "\n\[u\]\[b\]$tr{'smoothinfo-sect-networking'}\[/b\]\[/u\]\n";

  	if ($smoothinfosettings{'NETCONF2'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-netsettings2'}\"\]\[quote\]@ethernet_settings\[/quote\]\[/info\]";
		if (($netsettings{'RED_TYPE'} eq 'DHCP' || $netsettings{'RED_TYPE'} eq 'PPPOE') && (-e "${swroot}/red/active")) {
			print FILE "\[info=\"$tr{'smoothinfo-livesettings'}\"\]\[quote\]@live_settings\[/quote\]\[/info\]";
		}
	}

	if ($smoothinfosettings{'DHCPINFO'} eq 'on' && -e "${swroot}/dhcp/enable") {
		if (-s "${swroot}/dhcp/green") {
			print FILE "\[info=\"$tr{'smoothinfo-dhcpsettings'} green\"\]\[code\]";
			print FILE "Range of addresses: $green_dhcpsettings{'START_ADDR'} - $green_dhcpsettings{'END_ADDR'}\n";
			print FILE "Default lease time (mins): $green_dhcpsettings{'DEFAULT_LEASE_TIME'}\n";
			print FILE "Max lease time (mins): $green_dhcpsettings{'MAX_LEASE_TIME'}\n";
			print FILE "Primary DNS: $green_dhcpsettings{'DNS1'}\n";
			print FILE "Secondary DNS: $green_dhcpsettings{'DNS2'}\n";
			print FILE "Primary NTP: $green_dhcpsettings{'NTP1'}\n";
			print FILE "Secondary NTP: $green_dhcpsettings{'NTP2'}\n";
			print FILE "Primary WINS: $green_dhcpsettings{'WINS1'}\n";
			print FILE "Secondary WINS: $green_dhcpsettings{'WINS2'}\n";
			print FILE "Domain name suffix: $green_dhcpsettings{'DOMAIN_NAME'}\n";
			print FILE "NIS domain: $green_dhcpsettings{'NIS_DOMAIN'}\n";
			print FILE "Primary NIS: $green_dhcpsettings{'NIS1'}\n";
			print FILE "Secondary NIS: $green_dhcpsettings{'NIS2'}\n";
			if ($green_dhcpsettings{'DENYUNKNOWN'}) {
				print FILE "Deny Unknown Clients: $green_dhcpsettings{'DENYUNKNOWN'}\n";
			}
			print FILE "\[/code\]";
    
			if (-s "${swroot}/dhcp/staticconfig-green") {
				open (STATIC, "${swroot}/dhcp/staticconfig-green");
				my @statics = <STATIC>;
				close (STATIC);
				for (@statics) {
					s/(<span.*'>|<\/span>)//g;
				}
				print FILE "\[b\]$tr{'smoothinfo-statics'}\[/b\]\[code\]";
				print FILE " @statics";
				print FILE "\[/code\]\[/info\]";
			}
			else {
				print FILE "\[/info\]";
			}
		}

		if (-s "${swroot}/dhcp/purple") {
			print FILE "\[info=\"$tr{'smoothinfo-dhcpsettings'} purple\"\]\[code\]";
			print FILE "Range of addresses: $purple_dhcpsettings{'START_ADDR'} - $purple_dhcpsettings{'END_ADDR'}\n";
			print FILE "Default lease time (mins): $purple_dhcpsettings{'DEFAULT_LEASE_TIME'}\n";
			print FILE "Max lease time (mins): $purple_dhcpsettings{'MAX_LEASE_TIME'}\n";
			print FILE "Primary DNS: $purple_dhcpsettings{'DNS1'}\n";
			print FILE "Secondary DNS: $purple_dhcpsettings{'DNS2'}\n";
			print FILE "Primary NTP: $purple_dhcpsettings{'NTP1'}\n";
			print FILE "Secondary NTP: $purple_dhcpsettings{'NTP2'}\n";
			print FILE "Primary WINS: $purple_dhcpsettings{'WINS1'}\n";
			print FILE "Secondary WINS: $purple_dhcpsettings{'WINS2'}\n";
			print FILE "Domain name suffix: $purple_dhcpsettings{'DOMAIN_NAME'}\n";
			print FILE "NIS domain: $purple_dhcpsettings{'NIS_DOMAIN'}\n";
			print FILE "Primary NIS: $purple_dhcpsettings{'NIS1'}\n";
			print FILE "Secondary NIS: $purple_dhcpsettings{'NIS2'}\n";
			if ($purple_dhcpsettings{'DENYUNKNOWN'}) {
				print FILE "Deny Unknown Clients: $purple_dhcpsettings{'DENYUNKNOWN'}\n";
			}
			print FILE "\[/code\]";
    
			if (-s "${swroot}/dhcp/staticconfig-purple") {
				open (STATIC, "${swroot}/dhcp/staticconfig-purple");
				my @statics = <STATIC>;
				close (STATIC);
				for (@statics) {
					s/(<span.*'>|<\/span>)//g;
				}
				print FILE "\[b\]$tr{'smoothinfo-statics'}\[/b\]\[code\]";
				print FILE " @statics";
				print FILE "\[/code\]\[/info\]";
			}
			else {
				print FILE "\[/info\]";
			}
		}

		if (-s "${swroot}/dhcp/orange") {
			print FILE "\[info=\"$tr{'smoothinfo-dhcpsettings'} orange\"\]\[code\]";
			print FILE "Range of addresses: $orange_dhcpsettings{'START_ADDR'} - $orange_dhcpsettings{'END_ADDR'}\n";
			print FILE "Default lease time (mins): $orange_dhcpsettings{'DEFAULT_LEASE_TIME'}\n";
			print FILE "Max lease time (mins): $orange_dhcpsettings{'MAX_LEASE_TIME'}\n";
			print FILE "Primary DNS: $orange_dhcpsettings{'DNS1'}\n";
			print FILE "Secondary DNS: $orange_dhcpsettings{'DNS2'}\n";
			print FILE "Primary NTP: $orange_dhcpsettings{'NTP1'}\n";
			print FILE "Secondary NTP: $orange_dhcpsettings{'NTP2'}\n";
			print FILE "Primary WINS: $orange_dhcpsettings{'WINS1'}\n";
			print FILE "Secondary WINS: $orange_dhcpsettings{'WINS2'}\n";
			print FILE "Domain name suffix: $orange_dhcpsettings{'DOMAIN_NAME'}\n";
			print FILE "NIS domain: $orange_dhcpsettings{'NIS_DOMAIN'}\n";
			print FILE "Primary NIS: $orange_dhcpsettings{'NIS1'}\n";
			print FILE "Secondary NIS: $orange_dhcpsettings{'NIS2'}\n";
			if ($orange_dhcpsettings{'DENYUNKNOWN'}) {
				print FILE "Deny Unknown Clients: $orange_dhcpsettings{'DENYUNKNOWN'}\n";
			}
			print FILE "\[/code\]";
    
			if (-s "${swroot}/dhcp/staticconfig-orange") {
				open (STATIC, "${swroot}/dhcp/staticconfig-orange");
				my @statics = <STATIC>;
				close (STATIC);
				for (@statics) {
					s/(<span.*'>|<\/span>)//g;
				}
				print FILE "\[b\]$tr{'smoothinfo-statics'}\[/b\]\[code\]";
				print FILE " @statics";
				print FILE "\[/code\]\[/info\]";
			}
			else {
				print FILE "\[/info\]";
			}
		}

		if (-e "/usr/etc/dhcpd.leases") {
			print FILE "\[info=\"$tr{'smoothinfo-dhcpleases'}\"\]\[code\]";
			# block of code borrowed from dhcp.cgi

			### Simple DHCP Lease Viewer (2007-0905) put together by catastrophe
			# - Borrowed "dhcpLeaseData" subroutine from dhcplease.pl v0.2.5 (DHCP Pack v1.3) for SWE2.0
			# by Dane Robert Jones and Tiago Freitas Leal
			# - Borrowed parts of "displaytable" subroutine from smoothtype.pm
			# (Smoothwall Express "Types" Module) from SWE3.0 by the Smoothwall Team
			# - Josh DeLong - 09/15/07 - Added unique filter
			# - Josh DeLong - 09/16/07 - Fixed sort bug and added ability to sort columns
			# - Josh DeLong - 10/1/07 - Rewrote complete dhcp.cgi to use this code
			###

			my $leaseCount = -1;
			my (@dhcptemparray, @dhcplHostName, @dhcplMACAddy, @dhcplEnd, @dhcplStart, @dhcplIPAddy);

			# Load the DHCP Lease File into array
			open (LEASES,"</usr/etc/dhcpd.leases") || die "Unable to open $!";
			my @catleasesFILENAME = (<LEASES>);
			close (LEASES);
			chomp (@catleasesFILENAME);

			foreach my $i (0..$#catleasesFILENAME) {
				my $datLine = $catleasesFILENAME[$i];

				next if ($datLine =~ /^\s*#/);	# Skip comment lines
				next if ($datLine eq '');		# Skip empty lines

				for ($datLine) {
					# Filter out open brace, double quotes, semi-colon, leading and trailing spaces
					s/\{|\"|\;//g;
					s/^\s+//;
					s/\s+$//;
				}
				if ($datLine =~ /^lease\s+((\d+\.){3}\d+)/) {		# Start of lease info
					$leaseCount++;					# Increment the counter
					$dhcplIPAddy[$leaseCount] = $1;			# Extract IP address
					next;
				}
				if ($datLine =~ /^starts\s+\d*\s*(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2})/) {
					$dhcplStart[$leaseCount] = UTC2LocalString($1) if ($leaseCount > -1);	# Extract Lease Start Date
					next;
				}
				if ($datLine =~ /^ends\s+\d*\s*(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2})/) {
					$dhcplEnd[$leaseCount] = UTC2LocalString($1) if ($leaseCount > -1);	# Extract Lease End Date
					next;
				}
				if ($datLine =~ /^hardware ethernet\s+(([0-9a-f]{2}:){5}[0-9a-f]{2})/i) {
					$dhcplMACAddy[$leaseCount] = uc($1) if ($leaseCount > -1);		# Make MAC Address Upper Case
					next;
				}
				if ($datLine =~ /^client-hostname\s+(.+)$/ || $datLine =~ /^hostname\s+(.+)$/) {
					$dhcplHostName[$leaseCount] = $1 if ($leaseCount > -1);			# Extract Host Name
					next;
				}
			}
			foreach my $i (0..$#dhcplIPAddy) {
				push (@dhcptemparray, $dhcplIPAddy[$i]);
				print FILE ($i+1) . " - IP: $dhcplIPAddy[$i] Lease started: $dhcplStart[$i] Ends: $dhcplEnd[$i] Mac: $dhcplMACAddy[$i] Host name: ";
				print FILE $dhcplHostName[$i] if ($dhcplHostName[$i]);
				print FILE "\n";

			}
			print FILE "No leases." unless (@dhcptemparray);
			print FILE "\[/code\]\[/info\]";
		}
		else {
			print FILE "\[info=\"$tr{'smoothinfo-dhcpleases'}\"\]\[code\]No leases file!\[/code\]\[/info\]";
		}

	}

	if ($smoothinfosettings{'DNS'} eq "on") {
		# Get the DNS info for Red, Green, Purple
		my ($redDNS1, $redDNS2) = ('', '');
		$redDNS1 = &readvalue("${swroot}/red/dns1") if (-s "${swroot}/red/dns1");
		$redDNS2 = &readvalue("${swroot}/red/dns2") if (-s "${swroot}/red/dns2");

		print FILE "\[info=\"$tr{'smoothinfo-dns'}\"\]\[code\]";
		print FILE "DNS servers for RED:\nDNS1: $redDNS1\nDNS2: $redDNS2\n";

		if (-s "${swroot}/dhcp/settings-green") {
			print FILE "DNS servers for GREEN:\nDNS1: $green_dhcpsettings{'DNS1'}\nDNS2: $green_dhcpsettings{'DNS2'}\n";
		}
		if (-s "${swroot}/dhcp/settings-purple") {
			print FILE "DNS servers for PURPLE:\nDNS1: $purple_dhcpsettings{'DNS1'}\nDNS2: $purple_dhcpsettings{'DNS2'}\n";
		}
		if (-s "${swroot}/dhcp/settings-orange") {
			print FILE "DNS servers for ORANGE:\nDNS1: $orange_dhcpsettings{'DNS1'}\nDNS2: $orange_dhcpsettings{'DNS2'}\n";
		}
		print FILE "\[/code\]\[/info\]";
	}

	if ($smoothinfosettings{'NETCONF1'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-netsettings1'}\"\]\[quote\]\[size=90\]@netconf\[/size\]\[/quote\]\[/info\]";
	}

	if ($smoothinfosettings{'ROUTE'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-routes'}\"\]\[code\]$route\[/code\]\[/info\]";
	}
}

# Firewall section
if ($smoothinfosettings{'CHAINS'} ne '' or
    $smoothinfosettings{'CONNTRACKS'} eq 'on' or
    $smoothinfosettings{'XTACCESS'} eq 'on' or
    $smoothinfosettings{'PORTFW'} eq 'on' or
    $smoothinfosettings{'PINHOLES'} eq 'on' or
    $smoothinfosettings{'OUTGOING'} eq 'on') {

	print FILE "\n\[u\]\[b\]$tr{'smoothinfo-sect-firewall'}\[/b\]\[/u\]\n";

	if ($smoothinfosettings{'CHAINS'} ne '') {
		my @filtering;
		foreach (@chains) {
			if (/All chains/) {
				open (FIREWALL,"-|", '/usr/sbin/iptables', '-L', '-n', '-v');  last;
			}
			else {
				open (FIREWALL,"-|", '/usr/sbin/iptables', '-L', $_, '-n', '-v')
			}
			my @firewall = <FIREWALL>;
			push (@filtering, "\n");
			@filtering = (@filtering,@firewall);
		}
		shift (@filtering);
		print FILE "\[info=\"$tr{'smoothinfo-firewall'}\"\]\[code\]@filtering\[/code\]\[/info\]";
	}

	if ($smoothinfosettings{'CONNTRACKS'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-conntracks'}\"\]\[code\]$conntracks\[/code\]\[/info\]";
	}

	# Check for replacement chain data (xtaccess, portfw, dmzholes, outgoing) from FFC and other mods.
	# We searched for SIchains.pl earlier (around line 522), so no need to search again.
	if (@chainfiles) {
		foreach my $SIchain ( sort @chainfiles ) {
			my $chaininfo = do $SIchain if (-s $SIchain && -x _);
			print FILE $chaininfo if ($chaininfo);
		}
	}
	else {
		if (($smoothinfosettings{'XTACCESS'} eq 'on') && (-s "${swroot}/xtaccess/config")) {
			my @xtaccess = `/bin/cat /var/smoothwall/xtaccess/config`;
			my @rules = `/usr/sbin/iptables -nvL xtaccess`;
			print FILE "\[info=\"External access\"\]\[code\]Config file:\n @xtaccess\n@rules\[/code\]\[/info\]";
		}

		if (($smoothinfosettings{'PORTFW'} eq 'on') && (-s "${swroot}/portfw/config")) {
			my @portfw = `/bin/cat /var/smoothwall/portfw/config`;
			my @rules = `/usr/sbin/iptables -nvL portfwf`;
			my @rules2 = `/usr/sbin/iptables -t nat -nvL portfw`;
			print FILE "\[info=\"$tr{'smoothinfo-portfw'}\"\]\[code\]Config File:\n @portfw\n@rules\n@rules2\[/code\]\[/info\]";
		}

		if (($smoothinfosettings{'PINHOLES'} eq 'on') && (-s "${swroot}/dmzholes/config")) {
			my @dmzholes = `/bin/cat /var/smoothwall/dmzholes/config`;
			my @rules = `/usr/sbin/iptables -nvL dmzholes`;
			print FILE "\[info=\"$tr{'smoothinfo-internal-pinholes'}\"\]\[code\]Config file:\n @dmzholes\n@rules\[/code\]\[/info\]";
		}

		if ($smoothinfosettings{'OUTGOING'} eq 'on') {
			unless (-z "${swroot}/outgoing/config") {
				my @config = `/bin/cat /var/smoothwall/outgoing/config`;
				my @chaingreen = `/usr/sbin/iptables -nvL outgreen`;
				my @chainpurple = `/usr/sbin/iptables -nvL outpurple`;
				my @chainorange = `/usr/sbin/iptables -nvL outorange`;
				my @chainallows = `/usr/sbin/iptables -nvL allows`;
				print FILE "\[info=\"$tr{'smoothinfo-outgoing-exceptions'}\"\]\[code\]Config file:\n @config\n@chaingreen\n@chainpurple\n@chainorange\n@chainallows\[/code\]\[/info\]";
			}
		}
	}
}

### Linux & Hardware Section
if ($smoothinfosettings{'CPU'} eq 'on' or
    $smoothinfosettings{'MEMORY'} eq 'on'or
    $smoothinfosettings{'IRQs'} eq 'on' or
    $smoothinfosettings{'DISKSPACE'} eq 'on' or
    $smoothinfosettings{'ADAPTERS'} eq 'on' or
    $smoothinfosettings{'LOADEDMODULES'} eq 'on' or
    $smoothinfosettings{'TOP'} eq 'on') {

	print FILE "\n\[u\]\[b\]$tr{'smoothinfo-sect-hardware'}\[/b\]\[/u\]\n";

	if ($smoothinfosettings{'ADAPTERS'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-ethernet-reported'}\"\]\[code\]@ethernet_adapters\[/code\]\[/info\]";
	}
	if ($smoothinfosettings{'CPU'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-cpu'}\"\]\[code\]$cpu \nFreq.: $frequency MHz \nCache: $cache \nCores: $physCores \nProcessors: $cpuCores\[/code\]\[/info\]";
	}
	if ($smoothinfosettings{'DISKSPACE'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-diskspace'}\"\]\[code\]$diskspace\[/code\]\[/info\]";
	}
	if ($smoothinfosettings{'IRQs'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-irq'}\"\]\[code\]$warning@IRQs\[/code\]\[/info\]";
	}
	if ($smoothinfosettings{'LOADEDMODULES'} eq 'on') {
		my $data = do {local $/; $modules};

		# Will wrap lines longer then n characters
		$data =~ s{(.{$smoothinfosettings{'WRAP'}})(?=.)}{$1\n}g;
		print FILE "\[info=\"$tr{'smoothinfo-modules'}\"\]\[code\]$data\[/code\]\[/info\]";
	}
	if ($smoothinfosettings{'MEMORY'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-memory-specs'}\"\]\[code\]$memory\[/code\]\[/info\]";
	}
	if ($smoothinfosettings{'TOP'} eq 'on') {
		print FILE "\[info=\"$tr{'smoothinfo-top'}\"\]\[code\]@top\[/code\]\[/info\]";
	}
}

### Logs Section
if ($smoothinfosettings{'DMESG'} eq 'on' or
    $smoothinfosettings{'APACHE'} eq 'on' or
    $smoothinfosettings{'MESSAGES'} eq 'on') {

	print FILE "\n\[u\]\[b\]Logs\[/b\]\[/u\]\n";
	if ($smoothinfosettings{'DMESG'} eq 'on') {
		my $file = "/var/log/dmesg";
		my $dmesg;
		if ($smoothinfosettings{'LINES'} ne '' && $smoothinfosettings{'STRING'} eq '') {
			if ($smoothinfosettings{'HEADORTAIL'} eq 'HEAD') {
				open (DMESG,"<$file") || die "Unable to open $!";
				my @dmesg = (<DMESG>);
				my @tmp = splice (@dmesg,0,$smoothinfosettings{'LINES'});
				open (TMP,">",\$dmesg);
				foreach (@tmp) {
					chomp;
					print TMP "$_\n";
				}
			}
			elsif ($smoothinfosettings{'HEADORTAIL'} eq 'TAIL') {
				open (DMESG,"<$file") || die "Unable to open $!";
				my @dmesg = (<DMESG>);
				my $end = @dmesg;
				my $start = $end - $smoothinfosettings{'LINES'};
				open (TMP,">",\$dmesg);
				my $count = 0;
				foreach (@dmesg) {
					$count++;
					chomp;
					if ($count > $start && $count <= $end) {
						print TMP "$_\n";
					}
				}
			}
		}
		elsif ($smoothinfosettings{'LINES'} eq '' && $smoothinfosettings{'STRING'} ne '') {
			if ($smoothinfosettings{'IGNORECASE'} eq 'on') {
				open (DMESG,"<$file") || die "Unable to open $!";
				my @dmesg = (grep /$smoothinfosettings{'STRING'}/i, <DMESG>);
				open (TMP,">",\$dmesg);
				foreach (@dmesg) {
					chomp; print TMP "$_\n";
				}
			}
			else {
				open (DMESG,"<$file") || die "Unable to open $!";
				my @dmesg = (grep /$smoothinfosettings{'STRING'}/, <DMESG>);
				open (TMP,">",\$dmesg);
				foreach (@dmesg) {
					chomp; print TMP "$_\n";
				}
			}
		}
		elsif ($smoothinfosettings{'LINES'} eq '' && $smoothinfosettings{'STRING'} eq '') {
			open (DMESG,"<$file") || die "Unable to open $!";
			open (TMP,">",\$dmesg);
			foreach (<DMESG>) {
				chomp; print TMP "$_\n";
			}
		}
    
		if (!$dmesg) {
			print FILE "\[info=\"$tr{'smoothinfo-dmesg2'}\"\]\[code\]No search results for string '$smoothinfosettings{'STRING'}'.\[/code\]\[/info\]";
		}
		else {
			my $data = do {local $/; $dmesg};
			# Will wrap lines longer then n characters
			$data =~ s{(.{$smoothinfosettings{'WRAP'}})(?=.)}{$1\n}g;
			print FILE "\[info=\"$tr{'smoothinfo-dmesg2'}\"\]\[code\]$data\[/code\]\[/info\]";
		}
	}

	if ($smoothinfosettings{'APACHE'} eq 'on') {
		my $file = "/var/log/httpd/error.log";
		my $apache_error_log;
		if ($smoothinfosettings{'LINES2'} ne '' && $smoothinfosettings{'STRING2'} eq '') {
			if ($smoothinfosettings{'HEADORTAIL2'} eq 'HEAD2') {
				open (ERRORLOG,"<$file") || die "Unable to open $!";
				my @errorlog = (<ERRORLOG>);
				my @tmp = splice (@errorlog,0,$smoothinfosettings{'LINES2'});
				open (TMP,">",\$apache_error_log);
				foreach (@tmp) {
					chomp;
					print TMP "$_\n";
				}
			}
			elsif ($smoothinfosettings{'HEADORTAIL2'} eq 'TAIL2') {
				open (ERRORLOG,"<$file") || die "Unable to open $!";
				my @errorlog = (<ERRORLOG>);
				my $end = @errorlog;
				my $start = $end - $smoothinfosettings{'LINES2'};
				open (TMP,">",\$apache_error_log);
				my $count = 0;
				foreach (@errorlog) {
					$count++;
					chomp;
					if ($count > $start && $count <= $end) {
						print TMP "$_\n";
					}
				}
			}
		}
		elsif ($smoothinfosettings{'LINES2'} eq '' && $smoothinfosettings{'STRING2'} ne '') {
			if ($smoothinfosettings{'IGNORECASE2'} eq 'on') {
				open (ERRORLOG,"<$file") || die "Unable to open $!";
				my @errorlog = (grep /$smoothinfosettings{'STRING2'}/i, <ERRORLOG>);
				open (TMP,">",\$apache_error_log);
				foreach (@errorlog) {
					chomp;
					print TMP "$_\n";
				}
			}
			else {
				open (ERRORLOG,"<$file") || die "Unable to open $!";
				my @errorlog = (grep /$smoothinfosettings{'STRING2'}/, <ERRORLOG>);
				open (TMP,">",\$apache_error_log);
				foreach (@errorlog) {
					chomp;
					print TMP "$_\n";
				}
			}
			close (ERRORLOG);
		}
		elsif ($smoothinfosettings{'LINES2'} ne '' && $smoothinfosettings{'STRING2'} ne '') {
			my $temporary;
			if ($smoothinfosettings{'IGNORECASE2'} eq 'on') {
				open (ERRORLOG,"<$file") || die "Unable to open /var/log/httpd/error_log";
				my @errorlog = (grep /$smoothinfosettings{'STRING2'}/i, <ERRORLOG>);
				open (TMP,">",\$temporary);
				foreach (@errorlog) {
					chomp;
					print TMP "$_\n";
				}
				close (TMP);
				if ($smoothinfosettings{'HEADORTAIL2'} eq 'HEAD2') {
					open (HEAD,"<",\$temporary) || die "Unable to open $temporary";
					my @head = <HEAD>;
					my @tmp = splice (@head,0,$smoothinfosettings{'LINES2'});
					open (TMP,">",\$apache_error_log);
					foreach (@tmp) {
						chomp;
						print TMP "$_\n";
					}
					close (TMP);
				}
				elsif ($smoothinfosettings{'HEADORTAIL2'} eq 'TAIL2') {
					open (TAIL,"<",\$temporary) || die "Unable to open $temporary";
					my @tail = <TAIL>;
					my $end = @tail;
					my $start = $end - $smoothinfosettings{'LINES2'};
					open (TMP,">",\$apache_error_log);
					my $count = 0;
					foreach (@tail) {
						$count++;
						chomp;
						if ($count > $start && $count <= $end) {
							print TMP "$_\n";
						}
					}
				}
			}
			else {
				open (ERRORLOG,"<$file") || die "Unable to open $file: $!";
				my @errorlog = (grep /$smoothinfosettings{'STRING2'}/, <ERRORLOG>);
				open (TMP,">",\$temporary);
				foreach (@errorlog) {
					chomp;
					print TMP "$_\n";
				}
				close (TMP);
				if ($smoothinfosettings{'HEADORTAIL2'} eq 'HEAD2') {
					open (HEAD,"<",\$temporary) || die "Unable to open $temporary";
					my @head = <HEAD>;
					my @tmp = splice (@head,0,$smoothinfosettings{'LINES2'});
					open (TMP,">",\$apache_error_log);
					foreach (@tmp) {
						chomp;
						print TMP "$_\n";
					}
					close (TMP);
				}
				elsif ($smoothinfosettings{'HEADORTAIL2'} eq 'TAIL2') {
					open (TAIL,"<",\$temporary) || die "Unable to open $temporary";
					my @tail = <TAIL>;
					my $end = @tail;
					my $start = $end - $smoothinfosettings{'LINES2'};
					open (TMP,">",\$apache_error_log);
					my $count = 0;
					foreach (@tail) {
						$count++;
						chomp;
						if ($count > $start && $count <= $end) {
							print TMP "$_\n";
						}
					}
				}
			}
		}
		if (!$apache_error_log) {
			print FILE "\[info=\"$tr{'smoothinfo-apache-error2'}\"\]\[code\]No search results for string '$smoothinfosettings{'STRING2'}'.\[/code\]\[/info\]";
		}
		else {
			my $data = do {local $/; $apache_error_log};
			# Will wrap lines longer than n characters
			$data =~ s{(.{$smoothinfosettings{'WRAP'}})(?=.)}{$1\n}g;
			print FILE "\[info=\"$tr{'smoothinfo-apache-error2'}\"\]\[code\]$data\[/code\]\[/info\]";
		}
	}

	if ($smoothinfosettings{'MESSAGES'} eq 'on') {
		my $file = "/var/log/messages";
		my $messages_log;
		if ($smoothinfosettings{'LINES3'} ne '' && $smoothinfosettings{'STRING3'} eq '') {
			if ($smoothinfosettings{'HEADORTAIL3'} eq 'HEAD3') {
				open (MESSAGES,"<$file") || die "Unable to open $!";
				my @messages = (<MESSAGES>);
				my @tmp = splice (@messages,0,$smoothinfosettings{'LINES3'});
				open (TMP,">",\$messages_log);
				foreach (@tmp) {
					chomp;
					print TMP "$_\n";
				}
			}
			elsif ($smoothinfosettings{'HEADORTAIL3'} eq 'TAIL3') {
				open (MESSAGES,"<$file") || die "Unable to open $!";
				my @messages = (<MESSAGES>);
				my $end = @messages;
				my $start = $end - $smoothinfosettings{'LINES3'};
				open (TMP,">",\$messages_log);
				my $count = 0;
				foreach (@messages) {
					$count++;
					chomp;
					if ($count > $start && $count <= $end) {
						print TMP "$_\n";
					}
				}
			}
		}
		elsif ($smoothinfosettings{'LINES3'} eq '' && $smoothinfosettings{'STRING3'} ne '') {
			if ($smoothinfosettings{'IGNORECASE3'} eq 'on') {
				open (MESSAGES,"<$file") || die "Unable to open $!";
				my @messages = (grep /$smoothinfosettings{'STRING3'}/i, <MESSAGES>);
				open (TMP,">",\$messages_log);
				foreach (@messages) {
					chomp;
					print TMP "$_\n";
				}
			}
			else {
				open (MESSAGES,"<$file") || die "Unable to open $!";
				my @messages = (grep /$smoothinfosettings{'STRING3'}/, <MESSAGES>);
				open (TMP,">",\$messages_log);
				foreach (@messages) {
					chomp;
					print TMP "$_\n";
				}
			}
			close (MESSAGES);
		}
		elsif ($smoothinfosettings{'LINES3'} ne '' && $smoothinfosettings{'STRING3'} ne '') {
			my $temporary2;
			if ($smoothinfosettings{'IGNORECASE3'} eq 'on') {
				open (MESSAGES,"<$file") || die "Unable to open $file: $!";
				my @messages = (grep /$smoothinfosettings{'STRING3'}/i, <MESSAGES>);
				open (TMP,">",\$temporary2);
				foreach (@messages) {
					chomp;
					print TMP "$_\n";
				}
				close (TMP);
				if ($smoothinfosettings{'HEADORTAIL3'} eq 'HEAD3') {
					open (HEAD,"<",\$temporary2) || die "Unable to open $temporary2";
					my @head = <HEAD>;
					my @tmp = splice (@head,0,$smoothinfosettings{'LINES3'});
					open (TMP,">",\$messages_log);
					foreach (@tmp) {
						chomp;
						print TMP "$_\n";
					}
					close (TMP);
				}
				elsif ($smoothinfosettings{'HEADORTAIL3'} eq 'TAIL3') {
					open (TAIL,"<",\$temporary2) || die "Unable to open $temporary2: $!";
					my @tail = <TAIL>;
					my $end = @tail;
					my $start = $end - $smoothinfosettings{'LINES3'};
					open (TMP,">",\$messages_log);
					my $count = 0;
					foreach (@tail) {
						$count++;
						chomp;
						if ($count > $start && $count <= $end) {
							print TMP "$_\n";
						}
					}
				}
			}
			else {
				open (MESSAGES,"<$file") || die "Unable to open $file: $!";
				my @messages = (grep /$smoothinfosettings{'STRING3'}/, <MESSAGES>);
				open (TMP,">",\$temporary2);
				foreach (@messages) {
					chomp;
					print TMP "$_\n";
				}
				close (TMP);
				if ($smoothinfosettings{'HEADORTAIL3'} eq 'HEAD3') {
					open (HEAD,"<",\$temporary2) || die "Unable to open $temporary2";
					my @head = <HEAD>;
					my @tmp = splice (@head,0,$smoothinfosettings{'LINES3'});
					open (TMP,">",\$messages_log);
					foreach (@tmp) {
						chomp;
						print TMP "$_\n";
					}
					close (TMP);
				}
				elsif ($smoothinfosettings{'HEADORTAIL3'} eq 'TAIL3') {
					open (TAIL,"<",\$temporary2) || die "Unable to open $temporary2";
					my @tail = <TAIL>;
					my $end = @tail;
					my $start = $end - $smoothinfosettings{'LINES3'};
					open (TMP,">",\$messages_log);
					my $count = 0;
					foreach (@tail) {
						$count++;
						chomp;
						if ($count > $start && $count <= $end) {
							print TMP "$_\n";
						}
					}
				}
			}
		}
		if (!$messages_log) {
			print FILE "\[info=\"$tr{'smoothinfo-system2'}\"\]\[code\]No search results for string '$smoothinfosettings{'STRING3'}'.\[/code\]\[/info\]";
		}
		else {
			my $data = do {local $/; $messages_log};
			# Will wrap lines longer then n characters
			$data =~ s{(.{$smoothinfosettings{'WRAP'}})(?=.)}{$1\n}g;
			print FILE "\[info=\"$tr{'smoothinfo-system2'}\"\]\[code\]$data\[/code\]\[/info\]";
		}
	}
}


### Service details Section
if ($smoothinfosettings{'SQUID'} eq 'on' or $smoothinfosettings{'MODEXTRA'} eq 'on' or $smoothinfosettings{'QOS'} eq 'on') {
	print FILE "\n\[u\]\[b\]$tr{'smoothinfo-sect-services'}\[/b\]\[/u\]\n";

	if ($smoothinfosettings{'SQUID'} eq 'on') {
		# Check for replacement proxy data from E2G or other mods
		my @proxyfiles = </var/smoothwall/mods/*/usr/bin/smoothwall/SIproxy.pl>;
		chomp @proxyfiles;
		if (@proxyfiles) {
			foreach my $SIproxy ( sort @proxyfiles ) {
				my $proxyinfo = do $SIproxy if (-s $SIproxy && -x _);
				print FILE $proxyinfo if ($proxyinfo);
			}
		}
		else {
			print FILE "\[info=\"$tr{'smoothinfo-proxy'}\"\]\[code\]";
			print FILE "Squid Web proxy\n===========================\n";
			print FILE "Enabled: $proxysettings{'ENABLE'}\n";  
			print FILE "Transparent: $proxysettings{'TRANSPARENT'}\n";  
			print FILE "Cache size (MB): $proxysettings{'CACHE_SIZE'}\n";
			print FILE "Remote proxy: $proxysettings{'UPSTREAM_PROXY'}\n";
			print FILE "Max object size (KB): $proxysettings{'MAX_SIZE'}\n";
			print FILE "Min object size (KB): $proxysettings{'MIN_SIZE'}\n";
			print FILE "Max outgoing size (KB): $proxysettings{'MAX_OUTGOING_SIZE'}\n";
			print FILE "Max incoming size (KB): $proxysettings{'MAX_INCOMING_SIZE'}";
			print FILE "\[/code\]\[/info\]";
		}
	}

	if ($smoothinfosettings{'QOS'} eq 'on') {
		print FILE "\[info=\"QoS\"\]\[code\]";
		if ($qossettings{'ENABLE'} eq 'on') {
			foreach (sort(keys %qossettings)) {
				# Remove the HTML TITLE text from rules
				if ($_ =~ /^R_\d+/) {
					my @qosarray = split(/,/, $qossettings{$_});
					delete $qosarray[6];
					$qossettings{$_} = join(',', @qosarray);
				}
				print FILE "$_=$qossettings{$_}\n"
			}
			if (%qoslocalsettings) {
				print FILE "\[/code\]";
				print FILE "\[color=red\]QoS local settings and overrides:\[/color\]\[code\]";
				foreach (sort(keys %qoslocalsettings)) {
				# Remove the HTML TITLE text from rules
					if ($_ =~ /^R_\d+/) {
						my @qosarray = split(/,/, $qoslocalsettings{$_});
						delete $qosarray[6];
						$qoslocalsettings{$_} = join(',', @qosarray);
					}
					print FILE "$_=$qoslocalsettings{$_}\n"
				}
			}
		}
		else {
			print FILE "QoS not enabled";
		}
		print FILE "\[/code\]\[/info\]";
	}

	if ($smoothinfosettings{'MODEXTRA'} eq 'on') {
		opendir(DIR, $modpath) or die "Cannot open directory: '$modpath': $!";

		while ( my $entry = readdir DIR ) {
			next if $entry =~ /^\./;
			next unless (-d "$modpath/$entry");

			if (-s "$modpath/$entry/smoothinfo.pl" && -x _) {
				print FILE "\[info=\"" . ucfirst ($entry) . "\"\]\[quote\]";
				my $modinfo = do "$modpath/$entry/smoothinfo.pl";
				print FILE $modinfo;
				print FILE "\[\/quote\]\[\/info\]";
			}
		}
		closedir (DIR);
	}
}

# Xtra info section
if (-e "$MODDIR/clientip" or -e "$MODDIR/otherinfo" or
     ($smoothinfosettings{'SCREENSHOTS'} ne '' && $smoothinfosettings{'SCREENSHOTS'} =~ /^(http|ftp)/)) {
	print FILE "\n\[u\]\[b\]Xtra info\[/b\]\[/u\]\n";

	if ( -e "$MODDIR/clientip") {
		open (CLIENTIP,"<$MODDIR/clientip") || die "Unable to open $!";
		my @clientIP = (<CLIENTIP>);
		close (CLIENTIP);
		print FILE "\[info=\"$tr{'smoothinfo-client-IP'}\"\]";
		print FILE "\[code\]@clientIP\[/code\]\[/info\]";
	}

	if ($smoothinfosettings{'SCREENSHOTS'} ne '' && $smoothinfosettings{'SCREENSHOTS'} =~ /^\s*(http|ftp)/) {
		$smoothinfosettings{'SCREENSHOTS'} =~ s/^\s+//;		# Delete any leading spaces
		if ($smoothinfosettings{'SCREENSHOTS'} =~ /[, \;]+/) {
			my @sstemp = split('[, \;]+',$smoothinfosettings{'SCREENSHOTS'});
			$smoothinfosettings{'SCREENSHOTS'} = '';
			foreach my $line (@sstemp) {
				chomp ($line);
				$smoothinfosettings{'SCREENSHOTS'} .= "\n\[img\]$line\[/img\]\n";
			}
		}
		else {
			$smoothinfosettings{'SCREENSHOTS'} = "\n\[img\]$smoothinfosettings{'SCREENSHOTS'}\[/img\]";
		}
		print FILE "\[info=\"$tr{'smoothinfo-screenshots'}\"\]$smoothinfosettings{'SCREENSHOTS'}\[/info\]";
	}
	if ( -e "$MODDIR/otherinfo") {
		open (EXTRA,"<$MODDIR/otherinfo") || die "Unable to open $!";
		my @extrainfo = (<EXTRA>);
		close (EXTRA);

		my $section_title = shift @extrainfo;
		chomp $section_title;
		$section_title =~ s/([:;\)\(!'"]*)//g;
		print FILE "\[info=\"" . ucfirst ($section_title) . "\"\]";
		print FILE "\[code\]@extrainfo\[/code\]\[/info\]";
	}
}

print FILE "\[color=purple\]\[i\]\[size=90\]Smoothinfo was adapted from Pascal Touche's Smoothinfo mod for SWE3.0.\[/size\]\[/i\]\[/color\]\n";

unlink ("$MODDIR/livesettings");

close (FILE);

# This function fetches the link and addr info for the specified IF. It is assumed that
# the caller has verified the IF's existence. It returns BBcode of the desired color.
#
sub getLinkData {
	my ($iface, $color) = @_;
	my @ifconf;
	# Get the link info and RX/TX counts; note that splitting loses the newlines
	my @ifconf1 = split(/\n/, &pipeopen( "/usr/sbin/ip", "-s", "link", "show", "$iface" ));

	# Get the ip address(es); note that splitting loses the newlines
	my @ifconf2 = split(/\n/, &pipeopen( "/usr/sbin/ip", "addr", "show", "$iface" ));

	my $getStats = 0;
	foreach (@ifconf1, @ifconf2) {
		# Make the IP & MAC addr/masks black 
		$_ =~ s/(\d+\.\d+\.\d+\.\d+(\/\d+)*)/\[\/b\]\[\/color\]\[color=#000000\]\[b\]$1\[\/b\]\[\/color\]\[color=$color\]\[b\]/g;	# IPv4
    		$_ =~ s/(([0-9a-f]{2}:){5}([0-9a-f]{2}))/\[\/b\]\[\/color\]\[color=#000000\]\[b\]$1\[\/b\]\[\/color\]\[color=$color\]\[b\]/g;	# MAC
    		$_ =~ s/(([0-9a-f:])+(\/\d+))/\[\/b\]\[\/color\]\[color=#000000\]\[b\]$1\[\/b\]\[\/color\]\[color=$color\]\[b\]/g;		# IPv6

		# Restore the newlines that were split out above
		$_ =~ s/$/\n/;

		# Add labels to the RX stats line
		if ($getStats == 1) {
			my @tmp = split(/ +/);
			$_ = "RX: bytes:$tmp[1] packets:$tmp[2] errors:$tmp[3] dropped:$tmp[4] overrun:$tmp[5] multicast:$tmp[6]\n";
			$getStats = 0;
		}

		# Add labels to the TX stats line
		if ($getStats == 2) {
			my @tmp = split(/ +/);
			$_ = "TX: bytes:$tmp[1] packets:$tmp[2] errors:$tmp[3] dropped:$tmp[4] carrier:$tmp[5] collisions:$tmp[6]\n";
			$getStats = 0;
		}

		# The RX: and TX: stats lines trigger the operation on the next line and 'delete' themselves
		if ($_ =~ /^ +RX:/) {
			$getStats = 1;
			$_ = undef;
		}
		elsif ($_ =~ /^ +TX:/) {
			$getStats = 2;
			$_ = undef;
		}
	}

	# Dump the interface 'number'
	$ifconf1[0] =~ s/^[0-9]+: +//;

	# Prepare the final text (build a new list)
	# Use the first two lines of 'ip link' output, lines 2... of 'ip addr', then lines 2... of 'ip link'
	@ifconf = ("\[color=$color\]\[b\]", @ifconf1[0..1], @ifconf2[2..$#ifconf2], @ifconf1[2..$#ifconf1], "\[/b\]\[/color\]");
	#print stderr "$iface IF Info\n". Dumper @ifconf;

	# oss in a newline if not the first (GREEN)
	$ifconf[0] = "\n".$ifconf[0] if ($color ne "green" );
	# Remove any elements not defined
	@ifconf = grep defined, @ifconf;

	# And return it
	return @ifconf;
}

sub status_line
{	
	my $status = $_[0];
	return $status;
}

sub running_since
{
	my $age = time - (stat( $_[0] ))[9];
	my ( $days, $hours, $minutes, $seconds ) = (gmtime($age))[7,2,1,0];

	if ( $days != 0 ) {
		$howlong = "$days days";
	}
	elsif ( $hours != 0 ) {
		$howlong = sprintf( "%d hours, %.2d minutes", $hours, $minutes );
	}
	else {
		$howlong = sprintf( "%.d:%.2d", $minutes, $seconds );
	}
	return $howlong;
}

sub isrunning
{
	my $cmd = $_[0];
	my $status = "stopped";
	my $pid = '';
	my $testcmd = '';
	my $exename;
	my $qosPidFile = "/var/run/qos.pid";

	$cmd =~ /(^[a-z]+)/;
	$exename = $1;

	my $howlong = "";
	# qos is a special case
	if ($cmd eq 'qos') {
		if (-f $qosPidFile) {
			$status = "running";
			$howlong = &running_since($qosPidFile);
		}
	}
	elsif (defined $specialcases{$cmd}) {
		# Another extension of ModInstall: this is a
		#   'special case' status check
		require $specialcases{$cmd};
		my $speccase = \&{$cmd . "_isrunning"};
		($status, $howlong) = &$speccase();
	}
	elsif (open(MODFILE, "/var/run/${cmd}.pid")) {
		$pid = <MODFILE>;
		chomp $pid;
		close MODFILE;
		if (open(MODFILE, "/proc/${pid}/status")) {
			while (<MODFILE>) {
				$testcmd = $1 if (/^Name:\W+(.*)/);
			}
			close MODFILE;
			if ($testcmd =~ /$exename/) {
				$status = "running";
				$howlong = &running_since("/var/run/${cmd}.pid");

				if (open(MODFILE, "/proc/${pid}/cmdline")) {
					my $cmdline = <MODFILE>;
					$status = "Swapped" if (!$cmdline);
				}
				close MODFILE;
			}
		}
	}
	return $status;
}


