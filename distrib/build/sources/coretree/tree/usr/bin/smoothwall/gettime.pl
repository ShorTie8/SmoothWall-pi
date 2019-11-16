#!/usr/bin/perl

# (c) SmoothWall Ltd, 2002

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %timesettings;
my $count;

&readhash("${swroot}/time/settings", \%timesettings);

# If the service is off, or if the service is 'on' but the method is not 'Automatic', exit.
if ( $timesettings{'ENABLED'} ne 'on' or 
    ($timesettings{'ENABLED'} eq 'on' and $timesettings{'NTP_METHOD'} ne $tr{'time method periodic'}))
{
	exit 0;
}

if ($ARGV[0] eq 'FORCE')
{
	&ntpgettime();
	&resetcount();
} else {
	$count = &inccount();

	if ($count >= $timesettings{'NTP_INTERVAL'})
	{
		&ntpgettime();
		&resetcount();
	}
}

exit 0;


sub ntpgettime
{
	my @allservers; my $totalallservers;
	my @servers;
	my @command;
	my $count;

	unless (-e "${swroot}/red/active") {
		return; }

	push(@servers, $timesettings{'NTP_SERVER'});

	@command = ('/usr/sbin/ntpdate', '-su', @servers);

	if (system(@command) == 0)
	{
		&log("System clock successfully updated using server @servers.");
		system('/sbin/hwclock', '--systohc', '--localtime');
	} else {
		&log("Unable to update system clock using server @servers");
	}
}

sub inccount
{
	my $current;

	open(FILE, "+<${swroot}/time/timecount") or die "Couldn't load ntpcount.";
	flock FILE, 2;
	$current = <FILE>; chomp $current;
	seek FILE, 0, 0;
	$current++;
	truncate FILE, 0;
	print FILE "$current\n";
	close(FILE);

	return $current;
}

sub resetcount
{
	open(FILE, ">${swroot}/time/timecount") or die "Couldn't load ntpcount.";
	flock FILE, 2;
	print FILE "0\n";
	close(FILE);
}
