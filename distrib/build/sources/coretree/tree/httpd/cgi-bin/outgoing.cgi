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

my (%cgiparams, %selected, %checked, %interfaces, %netsettings, %render_settings);

my $config = "${swroot}/outgoing/config";
my $machineconfig = "${swroot}/outgoing/machineconfig";

# Load inbound interfaces into %interfaces (excluding RED)
&readhash("${swroot}/ethernet/settings", \%netsettings);

$interfaces{'GREEN'} = $netsettings{'GREEN_DEV'};
$interfaces{'ORANGE'} = $netsettings{'ORANGE_DEV'} if ($netsettings{'ORANGE_DEV'});
$interfaces{'PURPLE'} = $netsettings{'PURPLE_DEV'} if ($netsettings{'PURPLE_DEV'});

my $errormessage = '';
my $infomessage = '';
#my $interface;

my %backgroundColor = (
	'GREEN'  => 'rgba(0,255,0,.2',
	'ORANGE' => 'rgba(255,160,0,.4',
	'PURPLE' => 'rgba(179,0,255,.2',
	'RED'    => '#ffaaaa',
);

&showhttpheaders();

$cgiparams{'ACTION'} = '';
$cgiparams{'MACHINEACTION'} = '';

$cgiparams{'GREEN'} = '';
$cgiparams{'ORANGE'} = '' if ($netsettings{'ORANGE_DEV'});
$cgiparams{'PURPLE'} = '' if ($netsettings{'PURPLE_DEV'});
$cgiparams{'RULECOMMENT'} = '';
$cgiparams{'RULEENABLED'} = 'off';
$cgiparams{'MACHINE'} = '';
$cgiparams{'MACHINECOMMENT'} = '';
$cgiparams{'MACHINEENABLED'} = 'off';

$cgiparams{'COLUMN_ONE'} = 1;
$cgiparams{'ORDER_ONE'} = $tr{'log ascending'};
$cgiparams{'COLUMN_TWO'} = 1;
$cgiparams{'ORDER_TWO'} = $tr{'log ascending'};

&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && ( ! $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" )) {
	my @temp = split(',',$ENV{'QUERY_STRING'});
	$cgiparams{'ORDER_ONE'}  = $temp[1] if ( ($temp[ 1 ]) and $temp[ 1 ] ne "" );
	$cgiparams{'COLUMN_ONE'} = $temp[0] if ( ($temp[ 0 ]) and $temp[ 0 ] ne "" );
	$cgiparams{'ORDER_TWO'}  = $temp[3] if ( ($temp[ 3 ]) and $temp[ 1 ] ne "" );
	$cgiparams{'COLUMN_TWO'} = $temp[2] if ( ($temp[ 2 ]) and $temp[ 0 ] ne "" );
}

if ( $cgiparams{'ACTION'} eq '' ) {
	$cgiparams{'INTERFACE'} = 'GREEN';
	$cgiparams{'SERVICE'} = '';
	$cgiparams{'PORT'} = '';
	$cgiparams{'RULECOMMENT'} = '';
	$cgiparams{'RULEENABLED'} = 'on';
}

# Save the settings as is required.
if ( $cgiparams{'ACTION'} eq $tr{'save'} ) {
	my %settings;
	
	$settings{'GREEN'} = $cgiparams{'GREEN'};
	$settings{'ORANGE'} = $cgiparams{'ORANGE'};
	$settings{'PURPLE'} = $cgiparams{'PURPLE'};
		
	&writehash("${swroot}/outgoing/settings", \%settings);
	
	my $success = message('setoutgoing');
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
}

&readhash("${swroot}/outgoing/settings", \%cgiparams);

if ( $cgiparams{'ACTION'} eq $tr{'add'} ) {
	if ( $cgiparams{'SERVICE'} eq "user" ) {
		unless ( &validportrange( $cgiparams{'PORT'} ) ) {
			$errormessage .= $tr{'invalid port or range'} ."<br />\n";
		}
		else {
			$cgiparams{'SERVICE'} = $cgiparams{'PORT'};
		}
	}

	unless ($errormessage) {	
		open(FILE,">>$config") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'INTERFACE'},$cgiparams{'RULEENABLED'},$cgiparams{'SERVICE'},$cgiparams{'RULECOMMENT'}\n";
		close(FILE);
		
		my $success = message('setoutgoing');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);

		$cgiparams{'INTERFACE'} = 'GREEN';
		$cgiparams{'SERVICE'} = '';
		$cgiparams{'PORT'} = '';
		$cgiparams{'RULECOMMENT'} = '';
		$cgiparams{'RULEENABLED'} = 'on';
	}
}

my $service = 'user';

if ( $cgiparams{'ACTION'} eq $tr{'edit'} or $cgiparams{'ACTION'} eq $tr{'remove'}) {
	open(FILE, "$config") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $id = 0;
	my $count = 0;
	foreach my $line (@current) {
		$id++;
		$count++ if (($cgiparams{$id}) && $cgiparams{$id} eq "on");
	}
	$errormessage .= $tr{'nothing selected'} ."<br />\n" if ($count == 0);
	$errormessage .= $tr{'you can only select one item to edit'} ."<br />\n" if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'});
	
	unless ($errormessage) {
		open(FILE, ">$config") or die 'Unable to open config file.';
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
				$cgiparams{'INTERFACE'} = $temp[0];
				$cgiparams{'RULEENABLED'} = $temp[1];
				$cgiparams{'RULECOMMENT'} = $temp[3] || '';
				$service = $temp[2];
			}
		}
		close(FILE);

		my $success = message('setoutgoing');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
	}
}

if ( $cgiparams{'MACHINEACTION'} eq '' ) {
	$cgiparams{'MACHINE'} = "";
	$cgiparams{'MACHINEENABLED'} = "on";
	$cgiparams{'MACHINECOMMENT'} = "";
}

if ( $cgiparams{'MACHINEACTION'} eq $tr{'add'} ) {
	$errormessage .= "invalid ip<br />\n" unless ( &validip( $cgiparams{'MACHINE'} ) );

	unless ($errormessage) {
		open(FILE,">>$machineconfig") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'MACHINE'},$cgiparams{'MACHINEENABLED'},$cgiparams{'MACHINECOMMENT'}\n";
		close(FILE);

		my $success = message('setoutgoing');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);

		$cgiparams{'MACHINE'} = "";
		$cgiparams{'MACHINEENABLED'} = "on";
		$cgiparams{'MACHINECOMMENT'} = "";
	}
}

if ( $cgiparams{'MACHINEACTION'} eq $tr{'edit'} or $cgiparams{'MACHINEACTION'} eq $tr{'remove'}) {
	open(FILE, "$machineconfig") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $id = 0;
	my $count = 0;
	foreach my $line (@current) {
		$id++;
		$count++ if (($cgiparams{$id}) && $cgiparams{$id} eq "on");
	}

	$errormessage .= $tr{'nothing selected'} ."<br />\n" if ($count == 0);
	$errormessage .= $tr{'you can only select one item to edit'} ."<br />\n" if ($count > 1 && $cgiparams{'MACHINEACTION'} eq $tr{'edit'});
	
	unless ($errormessage) {
		open(FILE, ">$machineconfig") or die 'Unable to open config file.';
		flock FILE, 2;
		$id = 0;
		foreach my $line (@current) {
			$id++;
			unless (($cgiparams{$id}) && $cgiparams{$id} eq "on") {
				print FILE "$line";
			}
			elsif ($cgiparams{'MACHINEACTION'} eq $tr{'edit'}) {
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'MACHINE'} = $temp[0];
				$cgiparams{'MACHINEENABLED'} = $temp[1];
				$cgiparams{'MACHINECOMMENT'} = $temp[2] || '';
			}
		}
		close(FILE);

		my $success = message('setoutgoing');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
	}
}

$selected{'GREEN'}{'REJECT'} = '';
$selected{'GREEN'}{'ACCEPT'} = '';
$selected{'GREEN'}{$cgiparams{'GREEN'}} = 'SELECTED';

if ($netsettings{'ORANGE_DEV'}) {
	$selected{'ORANGE'}{'REJECT'} = '';
	$selected{'ORANGE'}{'ACCEPT'} = '';
	$selected{'ORANGE'}{$cgiparams{'ORANGE'}} = 'SELECTED';
}

if ($netsettings{'PURPLE_DEV'}) {
	$selected{'PURPLE'}{'REJECT'} = '';
	$selected{'PURPLE'}{'ACCEPT'} = '';
	$selected{'PURPLE'}{$cgiparams{'PURPLE'}} = 'SELECTED';
}

$selected{'EDIT'}{'GREEN'} = '';
$selected{'EDIT'}{'ORANGE'} = '';
$selected{'EDIT'}{'PURPLE'} = '';
$selected{'EDIT'}{$cgiparams{'INTERFACE'}} = 'SELECTED';

$checked{'RULEENABLED'}{'off'} = '';
$checked{'RULEENABLED'}{'on'} = '';
$checked{'RULEENABLED'}{$cgiparams{'RULEENABLED'}} = 'CHECKED';

$checked{'MACHINEENABLED'}{'off'} = '';
$checked{'MACHINEENABLED'}{'on'} = '';
$checked{'MACHINEENABLED'}{$cgiparams{'MACHINEENABLED'}} = 'CHECKED';

&openpage($tr{'outgoing filtering'}, 1, '', 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'filtered interfaces'} . ':');

print <<END;
<table class='list' style='width:50%; margin:6pt auto;'>
<tr>
	<td class='list' style='width: 50%; border-bottom:1px solid #b0b0b0; 
		background-color:(0,0,0,.03)'>$tr{'traffic is 1'}</td>
	<td class='list' style='width: 50%; border-bottom:1px solid #b0b0b0; 
		background-color:rgba(0,0,0,.03)'>$tr{'traffic is 4'}</td>
</tr>
END

foreach my $interface (keys(%interfaces)) {
	next if ($interfaces{$interface} eq '');
	
	print <<END
<tr>
	<td class='list' style='width:50%; border-bottom:1px solid #b0b0b0; 
	   background-color:$backgroundColor{$interface}'>
		<p style="margin:.1em 0; text-align:right; display:inline-block; width:7em">
		<span style='font-weight:bold;'>$interface</span>$tr{'traffic is 2'}:</p>
		<select id="outPolicy${interface}" style="margin:.1em 0" name="$interface" onclick="
		if (document.getElementById('outPolicy${interface}').value == 'REJECT') {
			document.getElementById('outPolicyExceptions${interface}').innerHTML = 
			'<span style=\\'font-weight:bold;\\'>$tr{'block'}</span>';
		}
		else {
			document.getElementById('outPolicyExceptions${interface}').innerHTML = 
			'<span style=\\'font-weight:bold;\\'>$tr{'allow'}</span>';
		}">
			<option value='REJECT' $selected{"$interface"}{'REJECT'}>$tr{'allowed'}</option>
			<option value='ACCEPT' $selected{"$interface"}{'ACCEPT'}>$tr{'blocked'}</option>
	</select>
	</td>
	<td class='list' id='outPolicyExceptions${interface}' 
		style='width:50%; border-bottom:1px solid #b0b0b0; background-color:$backgroundColor{$interface}'>
END
;
	print "<b>$tr{'block'}</b>" if ($cgiparams{"$interface"} eq 'REJECT');
	print "<b>$tr{'allow'}</b>" if ($cgiparams{"$interface"} eq 'ACCEPT');

}

print <<END;
</table>
<p class='list' style='padding-top:1em; text-align: center'>
		<input type="submit" name="ACTION" value="$tr{'save'}">
</p>
END

&closebox();

&openbox($tr{'add exception'});

print qq{
<table style='width: 100%;'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'interface'}</td>
	<td style='width: 25%;'>
	<select name='INTERFACE'>
};

foreach my $interface (keys %interfaces) {
	next if ($interfaces{$interface} eq '');
	print "<option value='$interface' $selected{'EDIT'}{$interface}>$interface</option>\n"; 
}

print qq{
	</select>
	</td>
	<td style='width: 25%;'></td>
	<td style='width: 25%;'></td>
</tr>
<tr>
	@{[&portlist('SERVICE', $tr{'application servicec'}, 'PORT', $tr{'portc'}, $service)]}
</tr>
<tr>
	<td class='base'>$tr{'commentc'}</td>
	<td colspan='3'><input type='text' style='width: 80%;' name='RULECOMMENT' 
		value='$cgiparams{'RULECOMMENT'}' id='rulecomment' 
		@{[jsvalidcomment('rulecomment')]}  ></td>
</tr>
};
print qq{
<tr>
	<td class='base' style='width: 25%;'>$tr{'enabledc'}</td>
	<td style='width: 25%;'><input type='checkbox' name='RULEENABLED' $checked{'RULEENABLED'}{'on'}></td>
	<td colspan='2' style='text-align: center;'>
		<input type="submit" name="ACTION" value="$tr{'add'}"></td>
</tr>
</table>
};

&closebox();

&openbox($tr{'current exceptions'});

my $portmap = &portmap();

%render_settings =
(
	'url'     => "/cgi-bin/outgoing.cgi?[%COL%],[%ORD%],$cgiparams{'COLUMN_TWO'},$cgiparams{'ORDER_TWO'}",
	'columns' => 
	[
		{ 
			column => '1',
			title  => "$tr{'interfacenc'}",
			size   => 20,
			sort   => 'cmp',
			maxrowspan  => 2,
		},
		{
			column => '3',
			title  => "$tr{'application service'}",
			size   => 50,
			sort   => 'cmp',
			tr     => \%{$portmap}
		},
		{
			column => '2',
			title  => "$tr{'enabledtitle'}",
			size   => 6,
			rotate => 60,
			tr     => 'onoff',
			align  => 'center',
		},
		{
			title  => "$tr{'mark'}", 
			size   => 6,
			rotate => 60,
			mark   => ' ',
		},
		{ 
			column => '4',
			title => "$tr{'comment'}",
			align  => 'left',
			break => 'line',
		},
		{
			column => '1',
			colour => 'colour',
			tr     => { 'GREEN' => 'green', 'ORANGE' => 'orange', 'PURPLE' => 'purple' },
		},
	]
);

&displaytable($config, \%render_settings, $cgiparams{'ORDER_ONE'}, $cgiparams{'COLUMN_ONE'} );

print <<END
<table class='blank'>
<tr>
	<td style='width: 50%; text-align: center;'><input type='submit' 
		name='ACTION' value='$tr{'remove'}'></td>
	<td style='width: 50%; text-align: center;'><input type='submit' 
		name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'add allowed machine'});

print qq{
<table style='width: 100%;'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'ip addressc'}</td>
	<td style='width: 25%;'><input type='text' name='MACHINE' id='address' 
		@{[jsvalidip('address')]} value='$cgiparams{'MACHINE'}'/></td>
	<td style='width: 25%;'></td>
	<td style='width: 25%;'></td>	
</tr>
<tr>
	<td class='base'>$tr{'commentc'}</td>
	<td colspan='3'><input type='text' style='width: 80%;' name='MACHINECOMMENT' 
		value='$cgiparams{'MACHINECOMMENT'}' id='machinecomment' 
		@{[jsvalidcomment('machinecomment')]}  ></td>
</tr>
};
print qq{
<tr>
	<td class='base'>$tr{'enabledc'}</td>
	<td><input type='checkbox' name='MACHINEENABLED' $checked{'MACHINEENABLED'}{'on'}></td>
	<td colspan='2' style='text-align: center;'><input type='submit' name='MACHINEACTION' 
		value='$tr{'add'}'></td>
</tr>
</table>
};

&closebox();


&openbox($tr{'current allowed machines'});

%render_settings =
(
	'url'     => "/cgi-bin/outgoing.cgi?$cgiparams{'COLUMN_ONE'},$cgiparams{'ORDER_ONE'},[%COL%],[%ORD%]",
	'columns' => 
	[
		{ 
			column => '1',
			title  => "$tr{'ip address'}",
			size   => 30,
			sort   => 'cmp',
		},
		{ 
			column => '3',
			title  => "$tr{'comment'}",
		},
		{
			column => '2',
			title  => "$tr{'enabledtitle'}",
			size   => 8,
			rotate => 60,
			tr     => 'onoff',
			align  => 'center',
		},
		{
			title  => "$tr{'mark'}", 
			size   => 4,
			rotate => 60,
			align  => 'center',
			mark   => ' ',
		}
	]
);

&displaytable($machineconfig, \%render_settings, $cgiparams{'ORDER_TWO'}, $cgiparams{'COLUMN_TWO'} );

print <<END
<table class='blank'>
<tr>
	<td style='width: 50%; text-align: center;'><input type='submit' 
		name='MACHINEACTION' value='$tr{'remove'}'></td>
	<td style='width: 50%; text-align: center;'><input type='submit' 
		name='MACHINEACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;

&closebox();

print "</div></form>\n";

&alertbox('add','add');
&closebigbox();
&closepage();
