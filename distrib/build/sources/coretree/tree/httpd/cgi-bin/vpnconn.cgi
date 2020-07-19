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

my (%cgiparams, %checked);
my $filename = "${swroot}/vpn/config";

$cgiparams{'ACTION'} = '';

$cgiparams{'NAME'} = '';
$cgiparams{'LEFT'} = '';
$cgiparams{'LEFT_SUBNET'} = '';
$cgiparams{'RIGHT'} = '';
$cgiparams{'RIGHT_SUBNET'} = '';
$cgiparams{'SECRET1'} = '';
$cgiparams{'SECRET2'} = '';
$cgiparams{'COMMENT'} = '';
$cgiparams{'ENABLED'} = 'off';
$cgiparams{'COMPRESSION'} = 'off';

&getcgihash(\%cgiparams);

my $infomessage = '';
my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'add'}) {
	unless ($cgiparams{'NAME'} =~ /^[-._0-9a-zA-Z]+$/) {
		$errormessage .= $tr{'name must only contain characters'} ."<br />";
	}
	unless (&validip($cgiparams{'LEFT'}) or &validhostname($cgiparams{'LEFT'})) { 
		$errormessage .= $tr{'left ip is invalid'} ."<br />";
	}
	unless (&validipandmask($cgiparams{'LEFT_SUBNET'})) {
		$errormessage .= $tr{'left subnet is invalid'} ."<br />";
	}
	unless (&validip($cgiparams{'RIGHT'}) or &validhostname($cgiparams{'RIGHT'})) { 
		$errormessage .= $tr{'right ip is invalid'} ."<br />";
	}
	unless (&validipandmask($cgiparams{'RIGHT_SUBNET'})) {
		$errormessage .= $tr{'right subnet is invalid'} ."<br />";
	}

	unless ( &validcomment( $cgiparams{'COMMENT'} ) ){
		$errormessage .= $tr{'invalid comment'} ."<br />";
	}

	unless ($cgiparams{'SECRET1'} and ($cgiparams{'SECRET1'} =~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage .= "$tr{'invalid password'}: $tr{'secretc'}<br />";
	}

	unless ($cgiparams{'SECRET2'} and ($cgiparams{'SECRET2'} =~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage .= "$tr{'invalid password'}: $tr{'again'}<br />";
	}

	if ($cgiparams{'SECRET1'} ne $cgiparams{'SECRET2'}) {
		$errormessage .= $tr{'passwords do not match'} ."<br />";
	}
	unless ($cgiparams{'SECRET1'} and $cgiparams{'SECRET2'}) {
		$errormessage .= $tr{'password not set'} ."<br />";
	}

	if (open(FILE, "$filename")) {
		my @current = <FILE>;
		close(FILE);
		unless ($errormessage) {
			if (open(FILE, ">>$filename")) {
				flock FILE, 2;
				print FILE "$cgiparams{'NAME'},$cgiparams{'LEFT'},$cgiparams{'LEFT_SUBNET'},$cgiparams{'RIGHT'},$cgiparams{'RIGHT_SUBNET'},$cgiparams{'SECRET1'},$cgiparams{'ENABLED'},$cgiparams{'COMPRESSION'},$cgiparams{'COMMENT'}\n";
				close(FILE);

				$cgiparams{'NAME'} = '';
				$cgiparams{'LEFT'} = '';
				$cgiparams{'LEFT_SUBNET'} = '';
				$cgiparams{'RIGHT'} = '';
				$cgiparams{'RIGHT_SUBNET'} = '';
				$cgiparams{'SECRET1'} = '';
				$cgiparams{'SECRET2'} = '';
				$cgiparams{'COMMENT'} = '';
				$cgiparams{'ENABLED'} = 'off';
				$cgiparams{'COMPRESSION'} = 'off';

				system('/usr/bin/smoothwall/writeipsec.pl');
 				$infomessage .= 'IPsec connection added.' ."<br />\n";
			}
			else {
 				$errormessage .= 'Could not write config file; connection not added.' ."<br />\n";
			}
		}
	}
	else {
 		$errormessage .= 'Could not read config file; connection not addded.' ."<br />\n";
	}
}

if ($cgiparams{'ACTION'} eq $tr{'remove'} || $cgiparams{'ACTION'} eq $tr{'edit'}) {
	my ($action, $actionOK);
 	$actionOK = ' ready to edit' if ($cgiparams{'ACTION'} eq $tr{'edit'});
 	$action = 'editted' if ($cgiparams{'ACTION'} eq $tr{'edit'});
 	$actionOK = '(s) removed' if ($cgiparams{'ACTION'} eq $tr{'remove'});
 	$action = 'removed' if ($cgiparams{'ACTION'} eq $tr{'remove'});

	if (open(FILE, "$filename")) {
		my @current = <FILE>;
		close(FILE);

		my $count = 0;
		my $id = 0;
		my $line;
		foreach $line (@current) {
			$id++;
			$count++ if ($cgiparams{$id} eq "on");
		}
		if ($count == 0) {
			$errormessage .= $tr{'nothing selected'} ."<br />\n";
		}
		if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
			$errormessage .= $tr{'you can only select one item to edit'} ."<br />\n";
		}
		unless ($errormessage) {
			if (open(FILE, ">$filename")) {
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
						$cgiparams{'NAME'} = $temp[0];
						$cgiparams{'LEFT'} = $temp[1];
						$cgiparams{'LEFT_SUBNET'} = $temp[2];
						$cgiparams{'RIGHT'} = $temp[3];
						$cgiparams{'RIGHT_SUBNET'} = $temp[4];
						$cgiparams{'SECRET1'} = $temp[5];
						$cgiparams{'SECRET2'} = $temp[5];
						$cgiparams{'ENABLED'} = $temp[6];
						$cgiparams{'COMPRESSION'} = $temp[7];
						$cgiparams{'COMMENT'} = $temp[8] || '';
					}
				}
				close(FILE);

				system('/usr/bin/smoothwall/writeipsec.pl');
 				$infomessage .= "IPsec connection${actionOK}.<br />\n";
			}
			else {
 				$errormessage .= "Could not write config file; connection not $action." ."<br />\n";
			}
		}
	}
	else {
 		$errormessage .= 'Could not read config file; connection not $action.' ."<br />\n";
	}
}

if ($cgiparams{'ACTION'} eq $tr{'export'}) {
	# Get hostname
	my $hostName = '';
	open (FILE, "/var/smoothwall/main/hostname.conf");
	while (<FILE>) {
		next unless ($_ =~ /^ServerName/ );
		chomp;
		$hostName = $_;
		$hostName =~ s/.* //;
		last;
	}
	close (FILE);

	# Get VPNs
        undef $/;
	open (FILE, "$filename");
	$_ = <FILE>;
	close (FILE);
	my $configLength = length;

	# Send the file
	print "Content-type: text/plain\n";
	print "Content-length: \"$configLength\"\n";
	print "Content-disposition: attachment; filename=\"vpn-config-$hostName\"\n\n";
	print;

	exit;
}

if ($cgiparams{'ACTION'} eq $tr{'import'}) {
	if (length($cgiparams{'FH'}) > 1) {
		if (open(FILE, ">$filename")) {
			flock FILE, 2;
			binmode(FILE);
			print FILE $cgiparams{'FH'};
			close (FILE);
		
			system('/usr/bin/smoothwall/writeipsec.pl');
 			$infomessage .= 'IPsec connections imported.' ."<br />\n";
		}
		else {
 			$errormessage .= 'Could not write config file; connections not imported.' ."<br />\n";
		}
	}
}

if ($cgiparams{'ACTION'} eq '') {
	$cgiparams{'ENABLED'} = 'on';
	$cgiparams{'COMPRESSION'} = 'off';
	$cgiparams{'COMMENT'} = '';
}

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

$checked{'COMPRESSION'}{'off'} = '';
$checked{'COMPRESSION'}{'on'} = '';
$checked{'COMPRESSION'}{$cgiparams{'COMPRESSION'}} = 'CHECKED';

&showhttpheaders();

&openpage('VPN configuration - Connections', 1, '', 'vpn');

&openbigbox();

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'add a new connection'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'namec'}</td>
	<td style='width:25%;'><input type='TEXT' name='NAME' value='$cgiparams{'NAME'}' id='name' 
		@{[jsvalidregex('name','^[-._0-9a-zA-Z]+$')]}></td>
	<td style='width:25%;' class='base'>Compression:</tD>
	<td style='width:25%;'><input type='CHECKBOX' name='COMPRESSION' $checked{'COMPRESSION'}{'on'}></td>
<tr>
	<td class='base'>$tr{'leftc'}</td>
	<td><input type=TEXT name='LEFT' value='$cgiparams{'LEFT'}' id='left' @{[jsvalidip('left')]}></td>
	<td class='base'>$tr{'left subnetc'}</td>
	<td><input type=TEXT name='LEFT_SUBNET' value='$cgiparams{'LEFT_SUBNET'}' id='left_subnet' 
		@{[jsvalidipandmask('left_subnet')]}></td>
</tr>
<tr>
	<td class='base'>$tr{'rightc'}</td>
	<td><input type=TEXT name='RIGHT' value='$cgiparams{'RIGHT'}' id='right' @{[jsvalidip('right')]} ></td>
	<td class='base'>$tr{'right subnetc'}</td>
	<td><input type=TEXT name='RIGHT_SUBNET' value='$cgiparams{'RIGHT_SUBNET'}' id='right_subnet' 
		@{[jsvalidipandmask('right_subnet')]}></td>
</tr>
<tr>
	<td class='base'>$tr{'secretc'}</td>
	<td colspan='4'>
		<input type='PASSWORD' name='SECRET1' value='$cgiparams{'SECRET1'}' SIZE='40' id='secret1' 
		@{[jsvalidpassword('secret1','secret2',,'^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]}></td>
</tr>
<tr>
	<td class='base'>$tr{'again'}</td>
	<td colspan='4'>
		<input type='PASSWORD' name='SECRET2' value='$cgiparams{'SECRET2'}' SIZE='40' id='secret2' 
		@{[jsvalidpassword('secret2','secret1','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]} ></td>
</tr>
<tr>
	<td class='base'>$tr{'commentc'}</td>
	<td colspan='3'><input type='text' style='width: 80%;' name='COMMENT' value='$cgiparams{'COMMENT'}' id='comment' 
		@{[jsvalidcomment('comment')]}  ></td>
</tr>
</table>
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'enabledc'}</td>
	<td style='width:25%;'><input type='CHECKBOX' name='ENABLED' $checked{'ENABLED'}{'on'}></td>
	<td style='width:50%;' colspan='2' ALIGN='CENTER'><input type='SUBMIT' name='ACTION' value='$tr{'add'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'current connections'});

print <<END
<table class='centered'>
<tr>
	<td></td>
</tr>
END
;

my $id = 0;
open(RULES, "$filename") or die 'Unable to open config file.';
while (<RULES>) {
	my $egif;
	my $cgif;
	$id++;
	chomp($_);
	my @temp = split(/\,/,$_);
	my $class;

	if ($id % 2) {
		$class = 'light';
	}
	else {
		$class = 'dark';
	}

 	if ($temp[6] eq 'on') {
		$egif = 'on.gif';
	}
	else {
		$egif = 'off.gif';
	}

 	if ($temp[7] eq 'on') {
		$cgif = 'on.gif';
	}
	else {
		$cgif = 'off.gif';
	}
	$temp[8] = '' if (! $temp[8]);

	print <<END
<tr class='$class'>
	<td style='width: 25%;'><strong>$tr{'namec'}</strong> $temp[0]</td>
	<td style='width: 25%;'><strong>$tr{'enabled'}</strong> <img src='/ui/img/$egif' alt='$egif'></td>
	<td style='width: 25%;'><strong>Compression:</strong> <img src='/ui/img/$cgif' alt='$cgif'></td>
	<td style='width: 25%;'>&nbsp;</td>
</tr>
<tr class='$class'>
	<td><strong>$tr{'leftc'}</strong> $temp[1]</td>
	<td><strong>$tr{'left subnetc'}</strong> $temp[2]</td>
	<td><strong>$tr{'rightc'}</strong> $temp[3]</td>
	<td><strong>$tr{'right subnetc'}</strong> $temp[4]</td>
</tr>
<tr class='$class'>
	<td colspan='3'><strong>$tr{'commentc'}</strong> $temp[8]</td>
	<td><strong>$tr{'markc'}</strong> <input type='checkbox' name='$id'></td>
</tr>
END
;
}

close(RULES);

print <<END
</table>
<table class='blank'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();

print "</div></form>\n";

&openbox($tr{'import and export'});
print <<END
<table style='width: 80%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align:left;'><form method='POST' action='?'>
		<div><input type='SUBMIT' name='ACTION' value='$tr{'export'}'></div></form></td>
	<td style='text-align:right;'><form method='POST' action='?' ENCTYPE='multipart/form-data'>
		<div><input type='FILE' name='FH' SIZE='30'>
		<input type='SUBMIT' name='ACTION' value='$tr{'import'}'></div></form></td>
</tr>
</table>
END
;

&closebox();

&closebigbox();
&closepage();
