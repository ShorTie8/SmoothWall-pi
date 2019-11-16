#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );
use strict;
use warnings;

my (%cgiparams, %checked, %netsettings, @current, @active);
my $filename = "${swroot}/vpn/config";
my $infomessage = '';
my $errormessage = '';
my $refresh = '';

$cgiparams{'ACTION'} = '';
$cgiparams{'ENABLED'} = 'off';
$cgiparams{'VALID'} = '';
$cgiparams{'VPN_IP'} = '';

&getcgihash(\%cgiparams);

&readhash("${swroot}/ethernet/settings", \%netsettings);

if ($cgiparams{'ACTION'} eq $tr{'save'}) {
	if ($cgiparams{'VPN_IP'}) {
		$errormessage .= $tr{'invalid input'} ."<br />\n" unless (&validip($cgiparams{'VPN_IP'}));
	}
	if ($errormessage) {
		$cgiparams{'VALID'} = 'no';
	}
	else {
		$cgiparams{'VALID'} = 'yes';
	}

	&writehash("${swroot}/vpn/settings", \%cgiparams);
}
&readhash("${swroot}/vpn/settings", \%cgiparams);

if ($cgiparams{'ACTION'} eq $tr{'restart'}) {
	system('/usr/bin/smoothwall/writeipsec.pl');

	my $success = message('ipsecrestart');
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= "ipsecrestart ".$tr{'smoothd failure'} ."<br />\n" unless ($success);
}

if ($cgiparams{'ACTION'} eq $tr{'stop'}) {
	my $success = message('ipsecstop');
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= "ipsecstop ".$tr{'smoothd failure'} ."<br />\n" unless ($success);
}

$cgiparams{'ENABLE'} = 'off' if ($cgiparams{'VALID'} eq '');

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&showhttpheaders();

&openpage($tr{'vpn configuration main'}, 1, $refresh, 'vpn');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'manual control and status'});

if (-f "$filename") {
	open (FILE, "$filename");
	@current = <FILE>;
	close (FILE);
}

if (-f "/proc/net/ipsec_eroute") {
	open (ACTIVE, "/proc/net/ipsec_eroute");
	@active = <ACTIVE>;
	close (ACTIVE);
}

print <<END
<br/>
<table class='centered' style='width: 60%;'>
<tr>
	<td></td>
</tr>
END
;

my $id = 0;
my $line;

# 0          192.168.0.0/24     -> 192.168.0.0/16     => tun0x1002@82.69.176.133

foreach $line (@current) {
	$id++;
	chomp($line);

	my @temp = split(/\,/,$line);
	my $name = $temp[0];

	my $left = $temp[1];
	my $left_subnet = $temp[2];
	$left_subnet =~ /\//;
	$left_subnet = $`;

	my $right = $temp[3];
	my $right_subnet = $temp[4];
	$right_subnet =~ /\//;
	$right_subnet = $`;

	my $status = $temp[6];
	my $active = "<img src='/ui/img/closed.jpg' alt='$tr{'capsclosed'}'>";
	$active = "<img src='/ui/img/disabled.jpg' alt='$tr{'capsdisabled'}'>" if ($status eq 'off');

	my $left_private = $temp[9] || '';
	$left_private =~ /\//;
	$left_private = $` unless $left_private eq '';

	my $right_private = $temp[10] || '';
	$right_private =~ /\//;
	$right_private = $` unless $right_private eq '';

	foreach $line (@active) {
		chomp($line);
		@temp = split(/[\t ]+/,$line);
		my $d = 0;

		my $left_vpnnet = $temp[1];
		$left_vpnnet =~ /\//;
		$left_vpnnet = $`;

		my $right_vpnnet = $temp[3];
		$right_vpnnet =~ /\//;
		$right_vpnnet = $`;

		my $remote = $temp[5];
		$remote =~ /\@/;
		$remote = $';

		if ($status eq 'on' &&
			(($left_vpnnet eq $left_subnet &&
			$right_vpnnet eq $right_subnet &&
			(($right_private eq '' && $right eq $remote) ||
			($right_private ne '' && $right eq '%any')))
			or
			($left_vpnnet eq $right_subnet &&
			$right_vpnnet eq $left_subnet &&
			(($left_private eq '' && $left eq $remote) ||
			($left_private ne '' && $left eq '%any'))))) {
			$active = "<img src='/ui/img/open.jpg' alt='$tr{'capsopen'}'>";
		}
	}
	print "<tr class='dark' style='border: 1px solid #c0c0c0;background-color:rgba(0,0,0,.035)'>\n"; 
	print "<td style='width: 65%; text-align: center;'><strong>$name</strong></td><td style='text-align: left;'>$active</td>\n";
	print "</tr><tr><td>&nbsp;</td></tr>\n";
}

print "</table>\n";
print <<END
<table class='blank'>
<tr>
	<td style='width:50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'restart'}'></td>
	<td style='width:50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'stop'}'></td>
</tr>
</table>
<br/>
END
;

&closebox();

&openbox($tr{'global settingsc'});
print <<END
<table width='100%'>
<tr>
	<td style='width:25%;' class='base'><img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;$tr{'local vpn ip'}</td>
	<td style='width:25%;'><input type='TEXT' name='VPN_IP' value='$cgiparams{'VPN_IP'}' SIZE='15' id='vpn_ip' @{[jsvalidip('vpn_ip')]}></td>
	<td style='width:15%;' class='base'>$tr{'enabledc'}</td>
	<td><input type='CHECKBOX' name='ENABLED' $checked{'ENABLED'}{'on'}></td>
	<td style='width:25%; text-align:center;'><input type='SUBMIT' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
<BR>
<img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;
<span class='base'>$tr{'if blank the currently configured ethernet red address will be used'}</span>
END
;
&closebox();

print "</div></form>\n";

&alertbox('add','add');
&closebigbox();
&closepage();
