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
use smoothtype qw(:standard);
use strict;
use warnings;

my (%cgiparams, %selected, %checked, @service);
my $filename = "${swroot}/hosts/config";

my $refresh = '';
my $errormessage = '';
my $infomessage = '';

&showhttpheaders();

$cgiparams{'ACTION'} = '';

$cgiparams{'ENABLED'} = 'off';
$cgiparams{'IP'} = '';
$cgiparams{'HOSTNAME'} = '';
$cgiparams{'COMMENT'} = '';

$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'} = $tr{'log ascending'};

&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && $cgiparams{'ACTION'} eq "" ) {
	my @temp = split(',',$ENV{'QUERY_STRING'});
	$cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
	$cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

if ($cgiparams{'ACTION'} eq $tr{'add'}) {
	$errormessage .= $tr{'ip address not valid'} ."<br />\n" unless(&validip($cgiparams{'IP'}));
	$errormessage .= $tr{'invalid hostname'} ."<br />\n" unless(&validhostname($cgiparams{'HOSTNAME'}));
	$errormessage .= $tr{'invalid comment'} ."<br />\n" unless ( &validcomment( $cgiparams{'COMMENT'} ) );

	unless ($errormessage) {
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'IP'},$cgiparams{'HOSTNAME'},$cgiparams{'ENABLED'},$cgiparams{'COMMENT'}\n";
		close(FILE);

		$cgiparams{'ENABLED'} = 'on';
		$cgiparams{'IP'} = '';
		$cgiparams{'HOSTNAME'} = '';
		$cgiparams{'COMMENT'} = '';

		$cgiparams{'COLUMN'} = 1;
		$cgiparams{'ORDER'} = $tr{'log ascending'};
		&log($tr{'host added to hosts list.'});
		
		system('/usr/bin/smoothwall/writehosts.pl');

		my $success = message('dnsproxyhup');
		$infomessage .= "$success<br />\n" if ($success);
		$errormessage .= "dnsproxyhup ".$tr{'smoothd failure'}."<br />" unless ($success);
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
				$cgiparams{'IP'} = $temp[0];
				$cgiparams{'HOSTNAME'} = $temp[1];
				$cgiparams{'ENABLED'} = $temp[2];
				$cgiparams{'COMMENT'} = $temp[3] || '';
			}
		}
		close(FILE);
		&log($tr{'host removed from host list'});

		system('/usr/bin/smoothwall/writehosts.pl');

		my $success = message('dnsproxyhup');
		$infomessage .= "$success<br />\n" if ($success);
		$errormessage .= "dnsproxyhup ".$tr{'smoothd failure'} ."<br />\n" unless ($success);
	}
}

$cgiparams{'ENABLED'} = 'on' if ($cgiparams{'ACTION'} eq '');

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&openpage($tr{'static dns configuration'}, 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'add a host'});

print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base'>$tr{'ip addressc'}</td>
	<td><input type='text' name='IP' value='$cgiparams{'IP'}' id='ip' @{[jsvalidip('ip')]}></td>
	<td class='base'>$tr{'hostnamec'}</td>
	<td><input type='text' name='HOSTNAME' value='$cgiparams{'HOSTNAME'}' id='hostname' 
		@{[jsvalidregex('hostname','^[a-zA-Z_0-9-\.]+$')]}></td>
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
	<td style='width:50%; text-align:center;'><input type='SUBMIT' name='ACTION' value='$tr{'add'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'current hosts'});

my %render_settings =
(
	'url'     => "/cgi-bin/hosts.cgi?[%COL%],[%ORD%]",
	'columns' => 
	[
		{ 
			column => '1',
			title  => "$tr{'ip address'}",
			size   => 5,
			sort   => \&ipcompare,
		},
		{
			column => '2',
			title  => "$tr{'hostname'}",
			size   => 10,
			sort   => 'cmp'
		},
		{ 
			column => '4',
			title => "$tr{'comment'}",
			align   => 'left',
		},
		{
			column => '3',
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
END
;
&closebox();

print "</div></form>\n";

&alertbox('add','add');
&closebigbox();
&closepage();
