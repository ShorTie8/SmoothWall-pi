#!/usr/bin/perl

use lib "/usr/lib/smoothwall";
use header qw( :standard );

use LWP;

# fetch the system id
my $sysid = &getsystemid();

my %proxy;
&readhash("${swroot}/main/proxy", \%proxy);

my $xhost = 'x3.smoothwall.org';

my $host; my $port;
unless ($proxy{'SERVER'})
{
	$host = $xhost;
	$port = 80;
} else {
	$host = $proxy{'SERVER'};
	$port = $proxy{'PORT'};
}

my %ownership;
&readhash("${swroot}/main/ownership", \%ownership);
my $sysid = $ownership{'ID'};

my $infoURL = "http://$xhost/cgi-bin/system_info.cgi?$sysid";
$req = HTTP::Request->new(GET => $infoURL);
$ua = LWP::UserAgent->new;
$ua->agent("Smoothwall/3.0");

if ($proxy{'SERVER'})
{
	$ua->proxy(http => "http://$host:$port");
}

$rsp = $ua->request($req);
$retsrt = $rsp->content();

@page = split(/\n/,$retsrt,-1);
$found = 0;

foreach(@page)
{
	if($_ =~ m/^status/)
	{
		@temp = split(/\=/,$_,2);
		$found = 1;
	}
	elsif($_ =~ m/^name/)
	{
		( $junk, $name ) = split(/\=/,$_,2);
	}
	elsif($_ =~ m/^added/)
	{
		( $junk, $added ) = split(/\=/,$_,2);
	}
	elsif($_ =~ m/^timestamp/)
	{
		( $junk, $timestamp ) = split(/\=/,$_,2);
	}
}

if($added)
{
	$ownership{'NAME'} = $name;
	$ownership{'ADDED_TO_X3'} = $added;
	$ownership{'ADDED_TO_X3_ON'} = $timestamp;
	&writehash("${swroot}/main/ownership", \%ownership);
}

if ($found == 1)
{
	if ($temp[1] =~ /^success/) {
		print STDERR "got my.Smoothwall system info with id [$sysid]\n";
		exit 0; 
	} else {
		exit 1; 
	}
} else {
	exit 2; 
}
