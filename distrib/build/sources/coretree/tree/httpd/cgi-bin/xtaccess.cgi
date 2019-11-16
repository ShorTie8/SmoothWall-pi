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

my (%cgiparams, %checked, %selected);
my $filename = "${swroot}/xtaccess/config";
my $refresh = '';
my $infomessage = '';
my $errormessage = '';

&showhttpheaders();

$cgiparams{'ACTION'} = '';

$cgiparams{'EXT'} = '';
$cgiparams{'DEST_PORT'} = '';
$cgiparams{'COMMENT'} = '';
$cgiparams{'ENABLED'} = 'off';
$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'} = $tr{'log ascending'};

&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && $cgiparams{'ACTION'} eq "" ) {
	my @temp = split(',',$ENV{'QUERY_STRING'});
	$cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
	$cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

if ($cgiparams{'ACTION'} eq $tr{'add'}) {
	$errormessage .= $tr{'invalid input'} ."<br />\n" unless($cgiparams{'PROTOCOL'} =~ /^(tcp|udp)$/);
	unless(&validipormask($cgiparams{'EXT'})) {
		if ($cgiparams{'EXT'} ne '') {
			$errormessage .= $tr{'source ip bad'} ."<br />\n";
		}
		else {
			$cgiparams{'EXT'} = '0.0.0.0/0';
		}
	}
	$errormessage .= $tr{'invalid comment'} ."<br />\n" unless ( &validcomment( $cgiparams{'COMMENT'} ) );	
	$errormessage .= $tr{'destination port numbers'} ."<br />\n" unless(&validportrange($cgiparams{'DEST_PORT'}));

	open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	unless ($errormessage) {
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'PROTOCOL'},$cgiparams{'EXT'},$cgiparams{'DEST_PORT'},$cgiparams{'ENABLED'},$cgiparams{'COMMENT'}\n";
		close(FILE);

		$cgiparams{'EXT'} = '';
		$cgiparams{'DEST_PORT'} = '';
		$cgiparams{'COMMENT'} = '';
		$cgiparams{'ENABLED'} = 'off';
		$cgiparams{'COLUMN'} = 1;
		$cgiparams{'ORDER'} = $tr{'log ascending'};
		
		&log($tr{'external access rule added'});

		my $success = message('setxtaccess');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= "setxtaccess ".$tr{'smoothd failure'} ."<br />\n" unless ($success);
	}
}

if ($cgiparams{'ACTION'} eq $tr{'remove'} || $cgiparams{'ACTION'} eq $tr{'edit'}) {
	open(FILE, "$filename") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $count = 0;
	my $id = 0;
	my $line;
	foreach $line (@current) {
		$id++;
		$count++ if (($cgiparams{$id}) && $cgiparams{$id} eq "on");
	}
	$errormessage .= $tr{'nothing selected'} ."<br />\n" if ($count == 0);
	$errormessage .= $tr{'you can only select one item to edit'} ."<br />\n" if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'});

	unless ($errormessage) {
		open(FILE, ">$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		my $id = 0;
		foreach $line (@current) {
			$id++;
			unless (($cgiparams{$id}) && $cgiparams{$id} eq "on") {
				print FILE "$line";
			}
			elsif ($cgiparams{'ACTION'} eq $tr{'edit'}) {
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'PROTOCOL'} = $temp[0];
				$cgiparams{'EXT'} = $temp[1];
				$cgiparams{'DEST_PORT'} = $temp[2];
				$cgiparams{'ENABLED'} = $temp[3];
				$cgiparams{'COMMENT'} = $temp[4] || '';
			}
		}
		close(FILE);

		&log($tr{'external access rule removed'});

		my $success = message('setxtaccess');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
	}
}
if ($cgiparams{'ACTION'} eq '') {
	$cgiparams{'PROTOCOL'} = 'tcp';
	$cgiparams{'ENABLED'} = 'on';
}

$selected{'PROTOCOL'}{'udp'} = '';
$selected{'PROTOCOL'}{'tcp'} = '';
$selected{'PROTOCOL'}{$cgiparams{'PROTOCOL'}} = 'SELECTED';

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&openpage($tr{'external access configuration'}, 1, $refresh, 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'add a new rule'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td>
	<select name='PROTOCOL'>
	<option value='udp' $selected{'PROTOCOL'}{'udp'}>UDP
	<option value='tcp' $selected{'PROTOCOL'}{'tcp'}>TCP
	</select></td>
	<td class='base'>$tr{'sourcec'}</td>
	<td><input type='TEXT' name='EXT' value='$cgiparams{'EXT'}' SIZE='32' id='ext' 
		@{[jsvalidipormask('ext','true')]}></td>
	<td class='base'>$tr{'destination portc'}</td>
	<td><input type='TEXT' name='DEST_PORT' value='$cgiparams{'DEST_PORT'}' SIZE='5' id='dest_port' 
		@{[jsvalidport('dest_port')]}></td>
</tr>
<tr>
	<td>$tr{'commentc'}</td>
	<td colspan='3'><input type='text' style='width: 80%;' name='COMMENT' value='$cgiparams{'COMMENT'}' id='comment' @{[jsvalidcomment('comment')]}  ></td>
</tr>
</table>
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base' style='width:50%;'>$tr{'enabledc'}</td>
	<td><input type='CHECKBOX' name='ENABLED' $checked{'ENABLED'}{'on'}></td>
	<td style='width:50%; text-align:center;'><input type='SUBMIT' name='ACTION' value='$tr{'add'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'current rules'});

my %render_settings =
(
	'url'     => "/cgi-bin/xtaccess.cgi?[%COL%],[%ORD%]",
	'columns' => 
	[
		{ 
			column => '1',
			title  => "$tr{'protocol'}",
			size   => 5,
			#rotate => 60,
			tr     => { 'udp' => 'UDP', 'tcp' => 'TCP' },
			sort   => 'cmp',
		},
		{
			column => '2',
			title  => "$tr{'source'}",
			size   => 10,
			sort   => 'cmp',
			tr     => { '0.0.0.0/0' => 'ALL' },
		},
		{
			column => '3',
			title  => "$tr{'destination port'}",
			rotate => 60,
		},
		{
			title  => "$tr{'comment'}",
			align => 'left',
			column => '5',
		},
		{
			column => '4',
			title  => "$tr{'enabledtitle'}",
			size   => 10,
			rotate => 60,
			tr     => 'onoff',
			align  => 'center',
		},
		{
			title  => "$tr{'mark'}", 
			size   => 10,
			rotate => 60,
			mark   => ' ',
		},
	]
);

&displaytable($filename, \%render_settings, $cgiparams{'ORDER'}, $cgiparams{'COLUMN'} );

print <<END
<table class='blank'>
<tr>
	<td style='text-align: center; width: 50%;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
	<td style='text-align: center; width: 50%;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();

print "</div></form>\n";

&alertbox('add', 'add');
&closebigbox();
&closepage();

