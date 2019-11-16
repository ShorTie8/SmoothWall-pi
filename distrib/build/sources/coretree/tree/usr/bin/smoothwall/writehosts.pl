#!/usr/bin/perl
#
# (c) SmoothWall Ltd, 2002
#
# This script rewrites the hosts file

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothtype qw( :standard );
use NetAddr::IP;

my (%netsettings, %dhcpsettings, %mainsettings);
my ($greenLAN, $purpleLAN, $orangeLAN);

my @temp;

my %hostEntries;

my $filename = "${swroot}/hosts/config";

&readhash("${swroot}/ethernet/settings", \%netsettings);
&readhash("${swroot}/dhcp/settings-green", \%dhcpsettingsGreen);
&readhash("${swroot}/dhcp/settings-purple", \%dhcpsettingsPurple);
if (-e "${swroot}/dhcp/settings-orange")
{
	&readhash("${swroot}/dhcp/settings-orange", \%dhcpsettingsOrange);
}
&readhash("${swroot}/main/settings", \%mainsettings);

# prepare the zone addresses for comparisons
$loopBACK = new NetAddr::IP "127.0.0.1/8";
$greenLAN = new NetAddr::IP "$netsettings{'GREEN_NETADDRESS'}/$netsettings{'GREEN_NETMASK'}";
if ($netsettings{'PURPLE_NETADDRESS'} ne "")
{
	$purpleLAN = new NetAddr::IP "$netsettings{'PURPLE_NETADDRESS'}/$netsettings{'PURPLE_NETMASK'}";
} else {
	$purpleLAN = "";
}
if ($netsettings{'ORANGE_NETADDRESS'} ne "")
{
	$orangeLAN = new NetAddr::IP "$netsettings{'ORANGE_NETADDRESS'}/$netsettings{'ORANGE_NETMASK'}";
} else {
	$orangeLAN = "";
}

# Set the local entries
&setentry("127.0.0.1", "localhost");
&setentry($netsettings{'GREEN_ADDRESS'}, $mainsettings{'HOSTNAME'});

# set the static DHCP entries
foreach $zone ("green","purple","orange")
{
	if (open(RULES, "$swroot/dhcp/staticconfig-$zone"))
	{
		while (<RULES>)
		{
			chomp($_);
			@temp = split(/\,/,$_);
			if ($temp[4] eq 'on')
			{
				&setentry($temp[2], $temp[0]);
			}
		}
		close RULES;
	}
}

# set the static DNS entries
open(RULES, "$filename") or die 'Unable to open config file.';
while (<RULES>)
{
	chomp($_);
	@temp = split(/\,/,$_);
	if ($temp[2] eq 'on')
	{
		&setentry($temp[0], $temp[1]);
	}
}
close RULES;

# write the entries to /etc/hosts
open(FILE, ">${swroot}/hosts/hosts") or die 'Unable to write hosts.';

print FILE "127.0.0.1\t$hostEntries{'127.0.0.1'}\n";
print FILE "$netsettings{'GREEN_ADDRESS'}\t$hostEntries{$netsettings{'GREEN_ADDRESS'}}\n";
delete $hostEntries{'127.0.0.1'};
delete $hostEntries{$netsettings{'GREEN_ADDRESS'}};

print FILE "\n";

foreach $ip (map $_->[0],
	     sort { $a->[1] cmp $b->[1] }
	     map [ $_, join '', map chr, split /\./, $_ ],
	     keys %hostEntries)
{
	print FILE "$ip\t$hostEntries{$ip}\n";
}

close FILE;



sub setentry
{
	my $ip = $_[0];
	my $name = $_[1];

	# Can't have an entry without an IP address.
	if ($ip eq "") { return; }

	my $thisIP = new NetAddr::IP $ip;
	my $names;

	if ($thisIP->within($loopBACK))
	{
		# loopback: no domain
		$domain = "";
	}
	elsif ($thisIP->within($greenLAN))
	{
		# Use GREEN domain
		$domain = $dhcpsettingsGreen{'DOMAIN_NAME'};
	}
	elsif ($purpleLAN and $thisIP->within($purpleLAN))
	{
		# Use PURPLE domain
		$domain = $dhcpsettingsPurple{'DOMAIN_NAME'};
	}
	elsif (-e "${swroot}/dhcp/settings-orange" and ($orangeLAN and $thisIP->within($orangeLAN)) )
	{
		# Use ORANGE domain IFF DHCP is configured for ORANGE
		$domain = $dhcpsettingsOrange{'DOMAIN_NAME'};
	}
	else
	{
		$domain = "";
	}

	if (!defined $hostEntries{$ip})
	{
		 $hostEntries{$ip} = "";
	}
	if (!($name =~ /\./) && $domain ne "")
	{
		$hostEntries{$ip} .= " ${name}.$domain";
	}
	$hostEntries{$ip} .= " $name";
	$hostEntries{$ip} =~ s/^ +//;
}
