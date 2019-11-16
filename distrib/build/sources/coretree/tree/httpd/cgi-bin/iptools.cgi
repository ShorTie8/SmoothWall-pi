#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) SmoothWall Ltd, 2002

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

use Socket;

my (%cgiparams, %selected);
my (@inaddrs, @addrs);
my ($addr, $address);
my $infomessage = '';
my $errormessage = '';

$cgiparams{'ACTION'} = '';

$cgiparams{"TOOL"} = '';
$cgiparams{'IP'} = '';

&getcgihash(\%cgiparams);

&showhttpheaders();

$selected{'TOOL'}{'PING'} = '';
$selected{'TOOL'}{'TRACEROUTE'} = '';
$selected{'TOOL'}{$cgiparams{'TOOL'}} = 'SELECTED';

if ($cgiparams{'ACTION'} eq $tr{'run'})
{
	@inaddrs = split(/,/, $cgiparams{'IP'});

	foreach $addr (@inaddrs)
	{
print STDERR "$addr\n";
		if (&validip($addr)) {
			push @addrs, $addr; }
		else
		{
			if ($address = gethostbyname($addr)) {
				push @addrs, inet_ntoa($address); }
			else {
				$errormessage .= "$tr{'could not resolve'} $addr<br />\n"; }
		}		
	}
}

&openpage($tr{'network utilities'}, 1, '', 'tools');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'select tool'});

print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:15%;' class='base'>$tr{'toolc'}</td>
	<td style='width:20%;'>
	<select name='TOOL'>
		<option value='PING' $selected{'TOOL'}{'PING'}>Ping
		<option value='TRACEROUTE' $selected{'TOOL'}{'TRACEROUTE'}>Traceroute
		</select> </td>
	<td style='width:20%;' class='base'>$tr{'ip addresses or hostnames'}</td>
	<td style='width:30%;'><input type='text' SIZE='40' name='IP' value='$cgiparams{'IP'}'></td>
	<td style='width:15%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'run'}'></td>
</tr>
</table>
END
;

&closebox();

foreach $addr (@addrs)
{
	my $iaddr = inet_aton($addr);
	my $hostname = gethostbyaddr($iaddr, AF_INET);
	if (!$hostname) { $hostname = $tr{'lookup failed'}; }

	&openbox("${addr} (${hostname})");
	print "<PRE>\n";
	if ($cgiparams{'TOOL'} eq 'PING') {
		system('/usr/bin/ping', '-n', '-c', '5', $addr); }
	elsif ($cgiparams{'TOOL'} eq 'TRACEROUTE') {
		system('/usr/bin/traceroute', '--resolve-hostnames', $addr); }
	print "</PRE>\n";
	&closebox();
}

print "</div></form>\n";

&closebigbox();

&closepage();
