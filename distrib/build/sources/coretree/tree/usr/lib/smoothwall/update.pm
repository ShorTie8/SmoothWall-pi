# SmoothWall Express 3.0 Update Mechanism 
#
# Common functions and procedures for updating a SmoothWall system
#
# (c) 2004-2006 SmoothWall Ltd
# 
# Original Author: Darren Taylor
# Based upon updateslists.pl by Lawrence Manning and others
# 
# This Code is distributed under the terms of the GPL V2.0

package update;
require Exporter;

use lib "/usr/lib/smoothwall/";
use header qw(:standard);

@ISA = qw(Exporter);

# Define the export lists .

@EXPORT		= qw();
@EXPORT_OK	= qw(downloadlist);
%EXPORT_TAGS	= ( 
			standard => [@EXPORT_OK]
		  );

# Download function, retrieves the Updates list from SmoothWall's website and stores 
# it locally.

sub downloadlist
{
	use LWP;

	my %proxy;
	&readhash("${swroot}/main/proxy", \%proxy);
	my $infoURL;

	# From header.pm:
	#$version = "$productdata{'VERSION'}-$productdata{'REVISION'}-$productdata{'ARCH'}";

	if (! -e "/var/smoothwall/patches/TEST-NEW-UPDATE") {
		$infoURL = "http://sourceforge.net/projects/smoothwall/files/updateInfo/$version/info";
	}
	else {
		my %productdata;
		&readhash( "/var/smoothwall/main/productdata", \%productdata );
		$infoURL = "http://agcl.us/misc/info-$productdata{'ARCH'}";
		print STDERR "TEST: $infoURL\n";
	}
	$req = HTTP::Request->new(GET => $infoURL);
	$ua = LWP::UserAgent->new;
	$ua->agent("Smoothwall/3.0");

	if ($proxy{'SERVER'})
	{
		$ua->proxy(http => "http://$proxy{'SERVER'}:$proxy{'PORT'}");
	}

	$rsp = $ua->request($req);
	return $rsp->status_line()."\n".$rsp->content();
}

1;
