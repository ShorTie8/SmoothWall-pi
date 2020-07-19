#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothtype qw( :standard );
use File::Basename;
use strict;
use warnings;

my (%cgiparams, %servicenames, %coreservices, %netsettings, %specialcases);
my $errormessage = '';
my $howlong;

# Maps a nice printable name to the changing part of the pid file, which
# is also the name of the program

my $iface = &readvalue("${swroot}/red/iface") || '';

# build the list of services.

# Adapted from Steve McNeill's SmoothInstall
# Find all services and prepare them.
my @files = <"/usr/lib/smoothwall/services/*" "/var/smoothwall/mods/*/usr/lib/smoothwall/services/*">;
chomp @files;

foreach my $file ( sort @files ){
	my $dirname  = dirname($file);
	my $basename = basename($file);

	open (SERVICE, "<$dirname/$basename" ) or next;
	my ( $name, $rel ) = split /,/, <SERVICE>;
	close SERVICE;

	chomp $name;
	my $servicename = $basename;
	$servicename =~s/\[RED\]/$iface/ig;
	$servicename =~s/-/\//g if ($servicename =~  "pluto-pluto");

	chomp $rel if ($rel);

	if ( defined $rel and $rel eq "core" ) {
		$coreservices{ $tr{ $name } } = $servicename;
	}
	elsif ( defined $rel and $rel eq "special" ) {
		# Another extension of ModInstall: allow mods with
		#   'special case' status checks
		$servicenames{ $tr{$name}} = $servicename;
		$specialcases{ $basename } = "$dirname/../../../bin/smoothwall/$basename-status.pl";
	}
	else {	
		$servicenames{ $tr{$name}} = $servicename;
	}
}

&showhttpheaders();

$cgiparams{'COLUMN_ONE'} = 1;
$cgiparams{'ORDER_ONE'} = $tr{'log ascending'};
$cgiparams{'COLUMN_TWO'} = 1;
$cgiparams{'ORDER_TWO'} = $tr{'log ascending'};

&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" )) {
        my @temp = split(',',$ENV{'QUERY_STRING'});
        $cgiparams{'ORDER_TWO'}  = $temp[3] if ( defined $temp[ 3 ] and $temp[ 3 ] ne "" );
        $cgiparams{'COLUMN_TWO'} = $temp[2] if ( defined $temp[ 2 ] and $temp[ 2 ] ne "" );
        $cgiparams{'ORDER_ONE'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
        $cgiparams{'COLUMN_ONE'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

&readhash("${swroot}/ethernet/settings", \%netsettings);

&openpage($tr{'status information'}, 1, '', 'about your smoothie');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

my %render_settings =
(
        'url'     => "",
        'columns' =>
        [
                {
                        column     => '1',
                        title      => "Service",
                        size       => '',
                        sort       => 'cmp',
                },
                {
                        column     => '2',
                        title      => "Status",
                        size       => 10,
                        sort       => 'cmp',
                },
                {
                        column     => '3',
                        title      => "Uptime",
                        size       => 25,
                        sort       => 'cmp',
                },
	]
);


# Display core services
&openbox($tr{'core services'});

my $lines = 0;
my @tabArray;

foreach my $key (sort keys %coreservices) {
	my $shortname = $coreservices{$key};
	my ( $status, $period ) = &isrunning($shortname);

	$tabArray[$lines++] = "$key|$status|$period";
}

$render_settings{'url'} = "/cgi-bin/status.cgi?$cgiparams{'COLUMN_ONE'},$cgiparams{'ORDER_ONE'},[%COL%],[%ORD%]";
print "<div style='margin:1em auto; width:70%'>\n";
&displaytable( \@tabArray, \%render_settings, $cgiparams{'ORDER_TWO'}, $cgiparams{'COLUMN_TWO'});
print "</div\n";

&closebox();


# Display other services
&openbox($tr{'services'});

$lines = 0;
undef @tabArray;

foreach my $key (sort keys %servicenames) {
	my $shortname = $servicenames{$key};
	my ( $status, $period ) = &isrunning($shortname);

	$tabArray[$lines++] = "$key|$status|$period";
}

$render_settings{'url'} = "/cgi-bin/status.cgi?[%COL%],[%ORD%],$cgiparams{'COLUMN_TWO'},$cgiparams{'ORDER_TWO'}";
print "<div style='margin:1em auto; width:70%'>\n";
&displaytable( \@tabArray, \%render_settings, $cgiparams{'ORDER_ONE'}, $cgiparams{'COLUMN_ONE'});
print "</div\n";

&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();

sub status_line
{	
	my $status = $_[0];
	return "<img src='/ui/img/service_$status.png' alt='$status'>";
}

sub running_since
{
	my ( $days, $hours, $minutes, $seconds );
	my $remain;

	my @pidStat = stat($_[0]);

	$remain = time - $pidStat[9];

	$days = int($remain/(3600*24));
	$remain -= $days*3600*24;
	$hours = int($remain/3600);
	$remain -= $hours*3600;
	$minutes = int($remain/60);
	$remain -= $minutes*60;
	$seconds = int($remain);

	my $howlong = "";

	# When the uptimes are negative, it's a strong clue that the clock was
	#   set backward. It should never happen under normal conditions. It
	#   could indicate a failing hardware clock, or one that keeps time
	#   badly. (So the abs() below is correct.)

	# Set day or days
	if ( abs($days) > 1 ) {
		$howlong = "$days days";
	}
	elsif ( $days != 0 ) {
		$howlong = "$days day";
	}

	# Append small values if needed
	if ($days < 7) {
		$howlong .= sprintf( ", %.2d:%.2d:%.2d", $hours, $minutes, $seconds);
	}

	# Trim if needed
	if ($howlong =~ /^,/) {
		$howlong = substr($howlong, 2);
	}
	return $howlong;
}

sub isrunning
{
	my $cmd = $_[0];
	my $procstatus = status_line( "stopped" );
	my $pid = '';
	my $testcmd = '';
	my $exename;
	my $qosPidFile = "/var/run/qos.pid";
	my $pidfile;

	$cmd =~ /(^[a-z]+)/;
	$exename = $1;

	($pidfile) = glob("/var/run/${cmd}/*.pid");
	$pidfile = "" unless defined $pidfile;
	if ($pidfile eq "") {
		$pidfile = "/var/run/${cmd}.pid";
	}

	my $howlong = "";
	# qos is a special case
	if ($cmd eq 'qos') {
		if (-f $qosPidFile) {
			$procstatus = &status_line( "running" );
			$howlong = &running_since($qosPidFile);
		}
	}
	elsif (defined $specialcases{$cmd}) {
		# Another extension of ModInstall: this is a
		#   'special case' status check
		require $specialcases{$cmd};
		my $speccase = \&{$cmd . "_isrunning"};
		($procstatus, $howlong) = &$speccase();
	}
	elsif (open(FILE, $pidfile)) {
		$pid = <FILE>; chomp $pid;
		close FILE;
		if (open(FILE, "/proc/${pid}/status")) {
			while (<FILE>) {
				$testcmd = $1 if (/^Name:\W+(.*)/);
			}
			close FILE;
			if ($testcmd =~ /$exename/) {
				$procstatus = &status_line( "running" );
				$howlong = &running_since($pidfile);

				if (open(FILE, "/proc/${pid}/cmdline")) {
					my $cmdline = <FILE>;
					$procstatus = status_line( "swapped" ) if (!$cmdline);
				}
			}
		}
	}
	return ( $procstatus, $howlong );
}
