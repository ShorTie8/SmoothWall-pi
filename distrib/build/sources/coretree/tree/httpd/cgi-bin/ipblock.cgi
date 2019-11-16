#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL

#
# (c) SmoothWall Ltd 2003

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );
use strict;
use warnings;

my (%cgiparams, %checked, %selected, @vars);
my $filename = "${swroot}/ipblock/config";

my ($var, $addr);
my $needrestart = 0;
my $infomessage = '';
my $errormessage = '';

&showhttpheaders();

$cgiparams{"ACTION"} = '';
$cgiparams{'SRC_IP'} = '';
$cgiparams{'LOG'} = 'off';
$cgiparams{'TARGET'} = '';
$cgiparams{'ENABLED'} = 'off';
$cgiparams{'COMMENT'} = '';


$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'} = $tr{'log ascending'};

&getcgihash(\%cgiparams);


if ($ENV{'QUERY_STRING'} && $cgiparams{'ACTION'} eq '') {
	@vars = split(/\&/, $ENV{'QUERY_STRING'});
	foreach $_ (@vars) {
		($var, $addr) = split(/\=/);
		if ($var eq 'ip') {
			if (&validipormask($addr)) {
				open(FILE,">>$filename") or die 'Unable to open config file.';
				flock FILE, 2;
				print FILE "$addr,off,DROP,on\n";
				close(FILE);
				$needrestart = 1;
			}
		}
	}
	if ($needrestart) {
		my $success = message('setipblock');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
	}


}

if ($ENV{'QUERY_STRING'} && ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" )) {
        my @temp = split(',',$ENV{'QUERY_STRING'});
        $cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
        $cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

if ($cgiparams{'ACTION'} eq $tr{'add'}) {
	$errormessage .= $tr{'source ip bad'} ."<br />\n" unless(&validipormask($cgiparams{'SRC_IP'}));
	$errormessage .= $tr{'invalid comment'} ."<br />\n" unless ( &validcomment( $cgiparams{'COMMENT'} ) );

	open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	unless ($errormessage) {
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'SRC_IP'},$cgiparams{'LOG'},$cgiparams{'TARGET'},$cgiparams{'ENABLED'},$cgiparams{'COMMENT'}\n";
		close(FILE);

		my $column = $cgiparams{ 'COLUMN' };
		my $order  = $cgiparams{ 'ORDER' };

		foreach my $key (keys %cgiparams) {
			$cgiparams{$key} = '';
		}

		#undef %cgiparams;

		$cgiparams{ 'COLUMN' } = $column;
		$cgiparams{ 'ORDER' } = $order;

		&log($tr{'ip block rule added'});

		my $success = message('setipblock');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
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
		$id = 0;
		foreach $line (@current) {
			$id++;
			unless (($cgiparams{$id}) && $cgiparams{$id} eq "on") {
				print FILE "$line";
			}
			elsif ($cgiparams{'ACTION'} eq $tr{'edit'}) {
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'SRC_IP'} = $temp[0];
				$cgiparams{'LOG'} = $temp[1];
				$cgiparams{'TARGET'} = $temp[2];
				$cgiparams{'ENABLED'} = $temp[3];
				$cgiparams{'COMMENT'} = $temp[4] || '';
			}
		}
		close(FILE);
		&log($tr{'ip block rule removed'});

		my $success = message('setipblock');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
	}
}

if ($cgiparams{'ACTION'} eq '') {
	$cgiparams{'TARGET'} = 'DROP';
	$cgiparams{'ENABLED'} = 'on';
}

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

$checked{'LOG'}{'off'} = '';
$checked{'LOG'}{'on'} = '';  
$checked{'LOG'}{$cgiparams{'LOG'}} = 'CHECKED';

$checked{'TARGET'}{'DROP'} = '';
$checked{'TARGET'}{'REJECT'} = '';
$checked{'TARGET'}{$cgiparams{'TARGET'}} = 'CHECKED';

&openpage($tr{'ip block configuration'}, 1, '', 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'add a new rule'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:20%;' class='base'>$tr{'source ip or networkc'}</td>
	<td style='width:20%;'><input type='TEXT' name='SRC_IP' value='$cgiparams{'SRC_IP'}' SIZE='15' id='src_ip' 
		@{[jsvalidipormask('src_ip')]}></td>
	<td style='width:10%;' class='base'><input type='radio' name='TARGET' value='DROP' $checked{'TARGET'}{'DROP'}></td>
	<td>$tr{'drop packet'}</td>
	<td style='width:5%;' class='base'><input type='radio' name='TARGET' value='REJECT' $checked{'TARGET'}{'REJECT'}></td>
	<td>$tr{'reject packet'}</td>
	<td class='base'>$tr{'logc'}</td>
	<td style='width:15%;'><input type='checkbox' name='LOG' $checked{'LOG'}{'on'}></td>
</tr>
<tr>
	<td class='base'>$tr{'commentc'}</td>
	<td colspan='3'><input type='text' style='width: 80%;' name='COMMENT' value='$cgiparams{'COMMENT'}' id='comment' 
		@{[jsvalidcomment('comment')]}  ></td>
</tr>
</table>

<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:50%;' class='base'>$tr{'enabledc'}</td><td><input type='CHECKBOX' name='ENABLED' style='vertical-align:middle' $checked{'ENABLED'}{'on'}></td>
	<td style='width:50%; text-align:center;'><input type='SUBMIT' name='ACTION' value='$tr{'add'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'current rules'});

my %render_settings = (
			'url'     => "/cgi-bin/ipblock.cgi?[%COL%],[%ORD%]",
			'columns' => [ 
				{ 
					column => '1',
					title  => "$tr{'source ip'}",
					size   => 5,
					sort   => \&ipcompare,
					tr     => {
						'0.0.0.0/0' => 'N/A',
					},					
				},
				{ 
					column => '5',
					title => "$tr{'comment'}",
					align => 'left',
				},
				{
					column => '3',
					title  => "$tr{'action'}", 
					rotate => 60,
					tr     => {
						'REJECT' => 'REJECT',
						'DROP'   => 'DROP',
						'RETURN' => 'EXCEPTION',
					},
				},
				{
					column => '2',
					title => "$tr{'log'}",
					size   => 20,
					rotate => 60,
					tr     => 'onoff',
					align  => 'center',
				},
				{
					column => '4',
					title  => "$tr{'enabledtitle'}",
					size   => 15,
					rotate => 60,
					tr     => 'onoff',
					align  => 'center',
				},
				{
					title  => "$tr{'mark'}", 
					size   => 15,
					rotate => 60,
					mark   => ' ',
				},
			]
			);

&displaytable( $filename, \%render_settings, $cgiparams{'ORDER'}, $cgiparams{'COLUMN'} );

print <<END
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

&closebigbox();
&closepage();

