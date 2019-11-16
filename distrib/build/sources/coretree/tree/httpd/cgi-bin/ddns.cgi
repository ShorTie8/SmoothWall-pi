#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothtype qw(:standard);
use strict;
use warnings;

my (%cgiparams, %selected, %checked);
my $filename = "${swroot}/ddns/config";

&showhttpheaders();

$cgiparams{'ACTION'} = '';

$cgiparams{'SERVICE'} = '';
$cgiparams{'ENABLED'} = 'off';
$cgiparams{'PROXY'} = 'off';
$cgiparams{'WILDCARDS'} = 'off';
$cgiparams{'HOSTNAME'} = '';
$cgiparams{'DOMAIN'} = '';
$cgiparams{'LOGIN'} = '';
$cgiparams{'PASSWORD'} = '';
$cgiparams{'COMMENT'} = '';

$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'} = $tr{'log ascending'};

&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" )) {
	my @temp = split(',',$ENV{'QUERY_STRING'});
	$cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
	$cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

my $errormessage = '';
my $infomessage = '';
my @service = ();

if ($cgiparams{'ACTION'} eq $tr{'add'}) {
	my $domOnce = 0;
	$errormessage .= $tr{'invalid input'} ."<br />" unless ($cgiparams{'SERVICE'} =~ /^(dhs|dyndns-custom|dyndns|dyns|hn|no-ip|zoneedit|easydns|ods)$/);
	$errormessage .= $tr{'invalid username'} ."<br />" unless ($cgiparams{'LOGIN'} =~ /^[^\"\']*$/);
	$errormessage .= $tr{'username not set'} ."<br />" unless ($cgiparams{'LOGIN'} ne '');
	$errormessage .= $tr{'password not set'} ."<br />" unless ($cgiparams{'PASSWORD'} ne '');
	$errormessage .= $tr{'invalid username'} ."<br />" unless ($cgiparams{'PASSWORD'} =~ /^[^\s\"\']*$/);
	$errormessage .= $tr{'domain not set'} ."<br />" unless ($cgiparams{'DOMAIN'} ne '');
	unless ($cgiparams{'DOMAIN'} =~ /^[a-zA-Z_0-9.-]+$/) {
		$domOnce = 1;
		$errormessage .= $tr{'invalid domain name'} ."<br />";
	}
	unless ($cgiparams{'DOMAIN'} =~ /[.]/) {
		$errormessage .= $tr{'invalid domain name'} ."<br />" unless ($domOnce);
	}
	$errormessage .= $tr{'invalid comment'} ."<br />" unless ( &validcomment( $cgiparams{'COMMENT'} ) );

	if ( open(FILE, $filename)) {
		my @current = <FILE>;
		close(FILE);
		my $line;
		foreach $line (@current) {
			my @temp = split(/\,/,$line);
			if($cgiparams{'HOSTNAME'} eq $temp[1] && $cgiparams{'DOMAIN'} eq $temp[2]) {
			 	$errormessage .= $tr{'hostname and domain already in use'} ."<br />";
			}
		}
		unless ($errormessage) {
			if (open(FILE,">>$filename")) {
				flock FILE, 2;
				print FILE "$cgiparams{'SERVICE'},$cgiparams{'HOSTNAME'},$cgiparams{'DOMAIN'},$cgiparams{'PROXY'},$cgiparams{'WILDCARDS'},$cgiparams{'LOGIN'},$cgiparams{'PASSWORD'},$cgiparams{'ENABLED'},$cgiparams{'COMMENT'}\n";
				close(FILE);

				foreach my $key (keys %cgiparams) {
					$cgiparams{$key} = '';
				}
				$cgiparams{'COLUMN'} = 1;
				$cgiparams{'ORDER'} = $tr{'log ascending'};
				&log($tr{'ddns hostname added'});
			}
		}
		else {
			$errormessage .= "Could not open config file to save.<br />\n";
		}
	}
	else {
		$errormessage .= "Could not open config file for validation.<br />\n";
	}
}

if ($cgiparams{'ACTION'} eq $tr{'remove'} || $cgiparams{'ACTION'} eq $tr{'edit'}) {
	if ( open(FILE, $filename)) {
		my @current = <FILE>;
		close(FILE);

		my $count = 0;
		my $id = 0;
		my $line;
		foreach $line (@current) {
			$id++;
			$count++ if ($cgiparams{$id} eq "on");
		}
		$errormessage .= $tr{'nothing selected'} ."<br />" if ($count == 0);
		$errormessage .= $tr{'you can only select one item to edit'} ."<br />" if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'});
		unless ($errormessage) {
			if ( open(FILE, ">$filename")) {
				flock FILE, 2;
				my $id = 0;
				foreach $line (@current) {
					$id++;
					unless ($cgiparams{$id} eq "on") {
						print FILE "$line";
					}
					elsif ($cgiparams{'ACTION'} eq $tr{'edit'}) {
						chomp($line);
						my @temp = split(/\,/,$line);
						$cgiparams{'SERVICE'} = $temp[0];
						$cgiparams{'HOSTNAME'} = $temp[1];
						$cgiparams{'DOMAIN'} = $temp[2];
						$cgiparams{'PROXY'} = $temp[3];
						$cgiparams{'WILDCARDS'} = $temp[4];
						$cgiparams{'LOGIN'} = $temp[5];
						$cgiparams{'PASSWORD'} = $temp[6];
						$cgiparams{'ENABLED'} = $temp[7];
						$cgiparams{'COMMENT'} = $temp[8] || '';
					}
				}
				close(FILE);
				&log($tr{'ddns hostname removed'});
			}
			else {
				$errormessage .= "Could not open config file to remove entry.<br />\n";
			}
		}
	}
	else {
		$errormessage .= "Could not open config file to remove or edit.<br />\n";
	}
}

system('/usr/bin/smoothwall/setddns.pl', '-f') if ($cgiparams{'ACTION'} eq $tr{'force update'});

$cgiparams{'ENABLED'} = 'on' if ($cgiparams{'ACTION'} eq '');

$selected{'SERVICE'}{'dhs'} = '';
$selected{'SERVICE'}{'dyndns'} = '';
$selected{'SERVICE'}{'dyndns-custom'} = '';
$selected{'SERVICE'}{'dyns'} = '';
$selected{'SERVICE'}{'hn'} = '';
$selected{'SERVICE'}{'no-ip'} = '';
$selected{'SERVICE'}{'zoneedit'} = '';
$selected{'SERVICE'}{'easydns'} = '';
$selected{'SERVICE'}{'ods'} = '';
$selected{'SERVICE'}{$cgiparams{'SERVICE'}} = 'SELECTED';

$checked{'PROXY'}{'off'} = '';
$checked{'PROXY'}{'on'} = '';
$checked{'PROXY'}{$cgiparams{'PROXY'}} = 'CHECKED';

$checked{'WILDCARDS'}{'off'} = '';
$checked{'WILDCARDS'}{'on'} = '';
$checked{'WILDCARDS'}{$cgiparams{'WILDCARDS'}} = 'CHECKED';

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&openpage($tr{'dynamic dns'}, 1, '', 'services');

&openbigbox('100%', 'LEFT');

#$errormessage = "<br />". $errormessage if ($errormessage);
&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'add a host'});

print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:20%;' class='base'>$tr{'servicec'}</td>
	<td style='width:25%;'>
		<select name='SERVICE'>
		<option value='dhs' $selected{'SERVICE'}{'dhs'}>dhs.org
		<option value='dyndns' $selected{'SERVICE'}{'dyndns'}>dyndns.org
		<option value='dyndns-custom' $selected{'SERVICE'}{'dyndns-custom'}>dyndns.org (Custom)
		<option value='dyns' $selected{'SERVICE'}{'dyns'}>dyns.cx
		<option value='hn' $selected{'SERVICE'}{'hn'}>hn.org
		<option value='no-ip' $selected{'SERVICE'}{'no-ip'}>no-ip.com
		<option value='zoneedit' $selected{'SERVICE'}{'zoneedit'}>zonedit.com
		<option value='easydns' $selected{'SERVICE'}{'easydns'}>easydns.com
		<option value='ods' $selected{'SERVICE'}{'ods'}>ods.org
		</select></td>

	<td style='width:20%;' class='base'>$tr{'behind a proxy'}</td>
	<td style='width:5%'><input type='checkbox' name='PROXY' value='on' $checked{'PROXY'}{'on'}></td>
	<td style='width:20%;' class='base'>$tr{'enable wildcards'}</td>
	<td> <input type='checkbox' name='WILDCARDS' value='on' $checked{'WILDCARDS'}{'on'}></td>
</tr>
<tr>
	<td class='base'>$tr{'hostnamec'}</td>
	<td><input type='text' name='HOSTNAME' value='$cgiparams{'HOSTNAME'}' id='hostname' 
		@{[jsvalidregex('hostname','^[a-zA-Z_0-9-]+$','true')]}></td>
	<td class='base'>$tr{'domainc'}</td>
	<td><input type='text' name='DOMAIN' value='$cgiparams{'DOMAIN'}' id='domain' 
		@{[jsvalidregex('domain','^[a-zA-Z_0-9-\.]+$')]}></td>
</tr>
<tr>
	<td class='base'>$tr{'username'}</td>
	<td><input type='text' name='LOGIN' value='$cgiparams{'LOGIN'}' id='login' 
		@{[jsvalidregex('login','^[a-zA-Z0-9\@\s~#!\(\)\&^\%\$£\*]+$')]}></td>
	<td class='base'>$tr{'password'}</td>
	<td><input type='PASSWORD' name='PASSWORD' value='$cgiparams{'PASSWORD'}' id='password' 
		@{[jsvalidregex('password','^[a-zA-Z0-9\@\s~#!\(\)\&^\%\$£\*]+$')]}></td>
</tr>
<tr>
	<td class='base'>$tr{'commentc'}</td>
	<td colspan='3'><input type='text' style='width: 80%;' name='COMMENT' id='comment' 
		@{[jsvalidcomment('comment')]} value='$cgiparams{'COMMENT'}'></td>
</tr>
</table>

<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:40%;' class='base'>$tr{'enabledc'}</td>
	<td><input type='checkbox' name='ENABLED' value='on' $checked{'ENABLED'}{'on'}></td>
	<td style='width:50%; text-align:center'><input type='SUBMIT' name='ACTION' value='$tr{'add'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'current hosts'});

my %render_settings =
(
	'url'     => "/cgi-bin/ddns.cgi?[%COL%],[%ORD%]",
	'columns' => 
	[
		{ 
			column => '1',
			title  => "$tr{'service'}",
			size   => 15,
			maxrowspan => 2,
			sort   => 'cmp',
		},
		{
			column => '2',
			title  => "$tr{'hostname'}",
			size   => 20,
			sort   => 'cmp'
		},
		{
			column => '3',
			title  => "$tr{'domain'}",
			size   => 25,
			sort   => 'cmp'
		},
		{
			column => '4',
			title  => "$tr{'proxy'}",
			rotate => 60,
			tr     => 'onoff',
			align  => 'center',
		},
		{
			column => '5',
			title  => "$tr{'wildcards'}",
			rotate => 60,
			tr     => 'onoff',
			align  => 'center',
		},
		{
			column => '8',
			title  => "$tr{'enabledtitle'}",
			rotate => 60,
			tr     => 'onoff',
			align  => 'center',
		},
		{
			title  => "$tr{'mark'}", 
			rotate => 60,
			mark   => ' ',
		},
		{ 
			column => '9',
			title => "$tr{'comment'}",
			break => 'line',
			spanadj => -1,
			align  => 'left',
		},

	]
);

&displaytable($filename, \%render_settings, $cgiparams{'ORDER'}, $cgiparams{'COLUMN'} );

print <<END
<table class='blank'>
<tr>
	<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
	<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
<table class='blank'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'force update'}'></td>
</tr>
</table>
END
;
&closebox();

print "</div></form>\n";

&alertbox('add','add');
&closebigbox();
&closepage();
