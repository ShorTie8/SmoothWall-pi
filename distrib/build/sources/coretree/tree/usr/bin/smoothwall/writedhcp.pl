#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;

my (%dhcpsettings, %netsettings);

&readhash("${swroot}/dhcp/global", \%dhcpsettings);
&readhash("${swroot}/ethernet/settings", \%netsettings);

unlink ("${swroot}/dhcp/enable");

open(FILE, ">/${swroot}/dhcp/dhcpd.conf") or die "Unable to write dhcpd.conf file";
flock(FILE, 2);

print FILE "authoritative;\n";

if ($dhcpsettings{'BOOT_ENABLE'} eq 'on' && $dhcpsettings{'BOOT_SERVER'}
    && $dhcpsettings{'BOOT_FILE'}  && $dhcpsettings{'BOOT_ROOT'}) {
	print FILE "allow booting;\n"					if ($dhcpsettings{'BOOT_SERVER'});
	print FILE "allow bootp;\n"					if ($dhcpsettings{'BOOT_SERVER'});
	print FILE "next-server $dhcpsettings{'BOOT_SERVER'};\n"	if ($dhcpsettings{'BOOT_SERVER'} ne '');
	print FILE "filename \"$dhcpsettings{'BOOT_FILE'}\";\n"		if ($dhcpsettings{'BOOT_FILE'} ne '');
	print FILE "option root-path \"$dhcpsettings{'BOOT_ROOT'}\";\n" if ($dhcpsettings{'BOOT_ROOT'} ne '');
}
print FILE "ddns-update-style interim;\n\n";

my $id = 0;
my @ifs = ('green');

push (@ifs, 'purple') if (-e "${swroot}/dhcp/settings-purple");
push (@ifs, 'orange') if (-e "${swroot}/dhcp/settings-orange");

foreach my $subnet (@ifs) {
	%dhcpsettings = ();
	&readhash("${swroot}/dhcp/settings-$subnet", \%dhcpsettings);
	open(DEV, ">${swroot}/dhcp/${subnet}") or die "Unable to write to device file";	
	if ($dhcpsettings{'ENABLE'} eq 'on') {
		system ('/bin/touch', "${swroot}/dhcp/enable");
		my $zoneCAPdev = uc($subnet) ."_DEV";
		print DEV $netsettings{$zoneCAPdev};
	}
	close(DEV);
	
	# Do not write config for a zone if that zone's DHCP is NOT enabled
	next if ($dhcpsettings{'ENABLE'} ne 'on');
	
	# The zone *is* enabled, so write its config
	if ($subnet eq 'green') {
		print FILE "subnet $netsettings{'GREEN_NETADDRESS'} netmask $netsettings{'GREEN_NETMASK'}\n";
		print FILE "{\n";
		print FILE "\tdeny unknown-clients;\n" if ($dhcpsettings{'DENYUNKNOWN'} eq 'on');
		print FILE "\toption subnet-mask $netsettings{'GREEN_NETMASK'};\n";
		print FILE "\toption domain-name \"$dhcpsettings{'DOMAIN_NAME'}\";\n";
		print FILE "\toption routers $netsettings{'GREEN_ADDRESS'};\n";
	}
	elsif ($subnet eq 'purple') {
		print FILE "subnet $netsettings{'PURPLE_NETADDRESS'} netmask $netsettings{'PURPLE_NETMASK'}\n";
		print FILE "{\n";
		print FILE "\tdeny unknown-clients;\n" if ($dhcpsettings{'DENYUNKNOWN'} eq 'on');
		print FILE "\toption subnet-mask $netsettings{'PURPLE_NETMASK'};\n";
		print FILE "\toption domain-name \"$dhcpsettings{'DOMAIN_NAME'}\";\n";
		print FILE "\toption routers $netsettings{'PURPLE_ADDRESS'};\n";
	}
	else {
		print FILE "subnet $netsettings{'ORANGE_NETADDRESS'} netmask $netsettings{'ORANGE_NETMASK'}\n";
		print FILE "{\n";
		print FILE "\tdeny unknown-clients;\n" if ($dhcpsettings{'DENYUNKNOWN'} eq 'on');
		print FILE "\toption subnet-mask $netsettings{'ORANGE_NETMASK'};\n";
		print FILE "\toption domain-name \"$dhcpsettings{'DOMAIN_NAME'}\";\n";
		print FILE "\toption routers $netsettings{'ORANGE_ADDRESS'};\n";
	}
			
	if ($dhcpsettings{'DNS1'}) {
		print FILE "\toption domain-name-servers ";
		print FILE "$dhcpsettings{'DNS1'}";
		print FILE ", $dhcpsettings{'DNS2'}" if ($dhcpsettings{'DNS2'});
		print FILE ";\n";
	}
	if ($dhcpsettings{'NTP1'}) {
		print FILE "\toption ntp-servers ";
		print FILE "$dhcpsettings{'NTP1'}";
		print FILE ", $dhcpsettings{'NTP2'}" if ($dhcpsettings{'NTP2'});
		print FILE ";\n";
	}
	if ($dhcpsettings{'WINS1'}) {
		print FILE "\toption netbios-name-servers ";
		print FILE "$dhcpsettings{'WINS1'}";
		print FILE ", $dhcpsettings{'WINS2'}" if ($dhcpsettings{'WINS2'});
		print FILE ";\n";
	}
	if ($dhcpsettings{'NIS1'} && $dhcpsettings{'NIS_DOMAIN'}) {
		print FILE "\toption nis-servers ";
		print FILE "$dhcpsettings{'NIS1'}";
		print FILE ", $dhcpsettings{'NIS2'}" if ($dhcpsettings{'NIS2'});
		print FILE ";\n";
		print FILE "\toption nis-domain \"$dhcpsettings{'NIS_DOMAIN'}\";\n" if ($dhcpsettings{'NIS_DOMAIN'});
	}

	my $defaultleasetime = $dhcpsettings{'DEFAULT_LEASE_TIME'} * 60;
	my $maxleasetime = $dhcpsettings{'MAX_LEASE_TIME'} * 60;
	print FILE "\trange dynamic-bootp $dhcpsettings{'START_ADDR'} $dhcpsettings{'END_ADDR'};\n";
	print FILE "\tdefault-lease-time $defaultleasetime;\n";
	print FILE "\tmax-lease-time $maxleasetime;\n";

	open(RULES, "${swroot}/dhcp/staticconfig-$subnet") or die 'Unable to open config file.';
	while (<RULES>) {
		$id++;
		chomp($_);
		my @temp = split(/\,/,$_);
		( $temp[1] ) = $temp[1] =~ /(([0-9A-F]{2}:){5}[0-9A-F]{2})/;
		print FILE "\thost $id { hardware ethernet $temp[1]; fixed-address $temp[2]; option host-name \"$temp[0]\"; }\n" if ($temp[4] eq 'on');
	}
	close(RULES);

	print FILE "}\n\n";
}
close FILE;

unlink ("${swroot}/dhcp/uptodate");
