#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

use Socket;

my %cgiparams;
my (@addrs, my @vars);
my $addr;
my $var;
my $hostname;
use strict;
use warnings;

$cgiparams{'ACTION'} = '';
$cgiparams{'IP'} = '';
$cgiparams{'MODE'} = '';

&getcgihash(\%cgiparams);

&showhttpheaders();

my $infomessage = '';
my $errormessage = '';

if ($ENV{'QUERY_STRING'} && $cgiparams{'ACTION'} eq '') {
	@vars = split(/\&/, $ENV{'QUERY_STRING'});
	$cgiparams{'IP'} = '';
	foreach $_ (@vars) {
		($var, $addr) = split(/\=/);
		if ($var eq 'ip') {
			$cgiparams{'IP'} .= "$addr,";
			push(@addrs, $addr);
		}
		elsif ( $var eq "MODE" ) {
			$cgiparams{'MODE'} = $addr;
		}
	}
	$cgiparams{'ACTION'} = 'Run';
}
else {
	@addrs = split(/,/, $cgiparams{'IP'});
}

foreach $addr (@addrs) {
	if (!&validipormask($addr) and !&validhostname($addr)) {
		$errormessage .= $tr{'invalid addresses or names'} ."<br />";
		last;
	}
}

if ( $cgiparams{'MODE'} ne "quick" ) {
	&openpage($tr{'ip info'}, 1, '', 'tools');

	&openbigbox('100%', 'left');

	&alertbox($errormessage, "", $infomessage);

	print "<form method='post' action='?'><div>\n";

	&openbox($tr{'whois lookupc'});

	print <<END;
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:20%;' class='base'>$tr{'ip addresses or domain names'}</td>
	<td style='width:65%;'><input type='text' size='60' name='IP' value='$cgiparams{'IP'}'></td>
	<td style='width:15%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'run'}'></td>
</tr>
</table>
END

	&closebox();

	if ($cgiparams{'ACTION'} eq $tr{'run'}) {
		unless ($errormessage) {
			foreach $addr (@addrs) {
				$hostname = gethostbyaddr(inet_aton($addr), AF_INET);
				$hostname = $tr{'lookup failed'} if (!$hostname);
				&openbox("$addr ($hostname)");
				print "<div style='margin:1em;'><code>\n";
				open (WHOIS,"/usr/bin/whois --nocgi -s $addr |");
				while (<WHOIS>) {
					s/&/&amp;/g;
					s/</&lt;/g;
					s/>/&gt;/g;
					print "$_<br />";
				}
				close(WHOIS);
				print "</code></div>\n";
				&closebox();
			}
		}	
	}

	print "</div></form>\n";

	&closebigbox();
	&closepage();
}
else {
	unless ($errormessage) {
		foreach $addr (@addrs) {
			$hostname = gethostbyaddr(inet_aton($addr), AF_INET);
			$hostname = $tr{'lookup failed'} if (!$hostname);
			&openbox("$addr ($hostname)");
			print "<div style='height: 140px; width: 400px; overflow: auto;'><pre style='font-size: 9px;'>";
				open (WHOIS,"/usr/bin/whois --nocgi -s $addr |");
				while (<WHOIS>) {
					s/&/&amp;/g;
					s/</&lt;/g;
					s/>/&gt;/g;
					print "$_";
				}
				close(WHOIS);
			print "</pre></div>";
			&closebox();
		}
	}	
}
