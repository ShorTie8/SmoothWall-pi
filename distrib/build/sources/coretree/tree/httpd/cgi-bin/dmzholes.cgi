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
use smoothd qw( message );
use strict;
use warnings;

my (%cgiparams, %checked, %selected);
my $filename = "${swroot}/dmzholes/config";

&showhttpheaders();

$cgiparams{'ACTION'} = '';

$cgiparams{'COLUMN_ONE'} = 2;
$cgiparams{'ORDER_ONE'} = $tr{'log ascending'};

$cgiparams{'ENABLED'} = 'off';
$cgiparams{'SRC_IP'} = '';
$cgiparams{'SERVICE'} = '';
$cgiparams{'DEST_IP'} = '';
$cgiparams{'DEST_PORT'} = '';
$cgiparams{'COMMENT'} = '';
$cgiparams{'PROTOCOL'} = 'tcp';

&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" )) {
	my @temp = split(',',$ENV{'QUERY_STRING'});
	$cgiparams{'ORDER_ONE'}  = $temp[1] if ( ($temp[ 1 ]) and $temp[ 1 ] ne "" );
	$cgiparams{'COLUMN_ONE'} = $temp[0] if ( ($temp[ 0 ]) and $temp[ 0 ] ne "" );
}

my $refresh = '';
my $infomessage = '';
my $errormessage = '';
my $service = "user";

if ($cgiparams{'ACTION'} eq '') {
	$cgiparams{'ENABLED'} = 'on';
	$cgiparams{'SRC_IP'} = '';
	$cgiparams{'SERVICE'} = '';
	$cgiparams{'DEST_IP'} = '';
	$cgiparams{'DEST_PORT'} = '';
	$cgiparams{'COMMENT'} = '';
	$cgiparams{'PROTOCOL'} = 'tcp';
}


if ($cgiparams{'ACTION'} eq $tr{'add'}) {
	$errormessage .= $tr{'invalid input'} ."<br />\n" unless ($cgiparams{'PROTOCOL'} =~ /^(tcp|udp)$/);
	$errormessage .= $tr{'source ip bad'} ."<br />\n" unless (&validipormask($cgiparams{'SRC_IP'}));

	if ( defined $cgiparams{'SERVICE'} and $cgiparams{'SERVICE'} ne "user" ) {
		$cgiparams{'DEST_PORT'} = $cgiparams{'SERVICE'};
	}
	else {
		$errormessage .= $tr{'destination port numbers'} ."<br />\n" unless (&validportrange($cgiparams{'DEST_PORT'}));
	}
	$errormessage .= $tr{'destination ip bad'} ."<br />\n" unless (&validipormask($cgiparams{'DEST_IP'}));
	$errormessage .= $tr{'invalid comment'} ."<br />\n" unless (&validcomment($cgiparams{'COMMENT'}));

	unless ($errormessage) {
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'PROTOCOL'},$cgiparams{'SRC_IP'},$cgiparams{'DEST_IP'},$cgiparams{'DEST_PORT'},$cgiparams{'ENABLED'},$cgiparams{'COMMENT'}\n";
		close(FILE);
		
		&log($tr{'dmz pinhole rule added'});

		my $success = message('setinternal');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= "setinternal ".$tr{'smoothd failure'} ."<br />\n" unless ($success);

		$cgiparams{'ENABLED'} = 'on';
		$cgiparams{'SRC_IP'} = '';
		$cgiparams{'SERVICE'} = '';
		$cgiparams{'DEST_IP'} = '';
		$cgiparams{'DEST_PORT'} = '';
		$cgiparams{'COMMENT'} = '';
		$cgiparams{'PROTOCOL'} = 'tcp';
	}
}

if ($cgiparams{'ACTION'} eq $tr{'remove'} || $cgiparams{'ACTION'} eq $tr{'edit'}) {
	open(FILE, "$filename") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $count = 0;
	my $id = 0;
	foreach my $line (@current) {
		$id++;
		$count++ if (($cgiparams{$id}) && $cgiparams{$id} eq "on");
	}
	$errormessage .= $tr{'nothing selected'} ."<br />\n" if ($count == 0);
	$errormessage .= $tr{'you can only select one item to edit'} ."<br />\n" if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'});

	unless ($errormessage) {
		open(FILE, ">$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		$id = 0;
		foreach my $line (@current) {
			$id++;
			unless (($cgiparams{$id}) && $cgiparams{$id} eq "on") {
				print FILE "$line";
			}
			elsif ($cgiparams{'ACTION'} eq $tr{'edit'}) {
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'PROTOCOL'} = $temp[0];
				$cgiparams{'SRC_IP'} = $temp[1];
				$cgiparams{'DEST_IP'}= $temp[2];
				$cgiparams{'DEST_PORT'} = $temp[3];
				$cgiparams{'ENABLED'} = $temp[4];
				$cgiparams{'COMMENT'} = $temp[5] || '';
				$service = $temp[3];
			}
		}
		close(FILE);

		&log($tr{'dmz pinhole rule removed'});

		my $success = message('setinternal');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
	}
}


$selected{'PROTOCOL'}{'udp'} = '';
$selected{'PROTOCOL'}{'tcp'} = '';
$selected{'PROTOCOL'}{$cgiparams{'PROTOCOL'}} = 'SELECTED';

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&openpage($tr{'dmz pinhole configuration'}, 1, $refresh, 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'add a new rule'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base'>$tr{'source ip or networkc'}</td>
	<td><input type='text' name='SRC_IP' value='$cgiparams{'SRC_IP'}' id='iaddress' 
		@{[jsvalidipormask('iaddress')]}></td>
	<td class='base'>$tr{'protocolc'}</td>
	<td>
		<select name='PROTOCOL'>
		<option value='udp' $selected{'PROTOCOL'}{'udp'}>UDP
		<option value='tcp' $selected{'PROTOCOL'}{'tcp'}>TCP
		</select></td>
</tr>
<tr>
	<td class='base'>$tr{'destination ip or networkc'}</td>
	<td><input type='text' name='DEST_IP' value='$cgiparams{'DEST_IP'}' id='dstiaddress' 
		@{[jsvalidipormask('dstiaddress')]}></td>
</tr>
<tr>
	@{[&portlist('SERVICE', $tr{'application servicec'}, 'DEST_PORT', $tr{'destination portc'}, $service)]}
</tr>
<tr>
	<td class='base'>$tr{'commentc'}</td>
	<td colspan='3'><input type='text' style='width: 80%;' name='COMMENT' value='$cgiparams{'COMMENT'}' id='comment' 
		@{[jsvalidcomment('comment')]}  ></td>
</tr>
<tr>
	<td class='base'>$tr{'enabledc'}</td>
	<td><input type='checkbox' name='ENABLED' $checked{'ENABLED'}{'on'}></td>
	<td colspan=2 style='text-align: left;'><input type='submit' name='ACTION' value='$tr{'add'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'current rules'});

my $portmap = &portmap();

my %render_settings =
(
	'url'     => "/cgi-bin/dmzholes.cgi?[%COL%],[%ORD%]",
	'columns' =>
	[
		{ 
			column     => '1',
			title      => "$tr{'protocol'}",
			size       => 15,
			tr         => { 'udp' => 'UDP', 'tcp' => 'TCP' },
			maxrowspan => 2,
			sort       => 'cmp',
		},
		{
			column     => '2',
			title      => "$tr{'source ip'}",
			size       => 20,
			sort       => &ipcompare,
		},
		{
			column     => '3',
			title      => "$tr{'destination ip'}",
			size       => 20,
			sort       => &ipcompare,
		},
		{
			column     => '4',
			title      => "$tr{'destination port'}",
			size       => 15,
			sort       => 'cmp',
			tr         => \%{$portmap}
		},
		{
			column     => '5',
			title      => "$tr{'enabledtitle'}",
			size       => 10,
			rotate     => 60,
			tr         => 'onoff',
			align      => 'center',
		},
		{
			title      => "$tr{'mark'}", 
			size       => 10,
			rotate     => 60,
			mark       => ' ',
		},
		{ 
			column     => '6',
			title      => "$tr{'comment'}",
			break      => 'line',
			align      => 'left',
			spanadj    => '-1',
		}
	]
);

&displaytable( $filename, \%render_settings, $cgiparams{'ORDER_ONE'}, $cgiparams{'COLUMN_ONE'} );

print <<END
<table class='blank'>
<tr>
	<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
	<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();

print "</div></form>\n";

&alertbox('add','add');
&closebigbox();
&closepage();

