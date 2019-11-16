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
use strict;
use warnings;

my (%cgiparams, %selected, %checked);

&showhttpheaders();

$cgiparams{'ACTION'} = '';

$cgiparams{'VALID'} = '';
$cgiparams{'ENABLE'} = '';
$cgiparams{'START_HOUR'} = '';
$cgiparams{'END_HOUR'} = '';
$cgiparams{'START_MIN'} = '';
$cgiparams{'END_MIN'} = '';
$cgiparams{'MACHINES'} = '';
$cgiparams{'MODE'} = '';

for (my $day = 0; $day < 7; $day++) {
	$cgiparams{"DAY_${day}"} = '';
}

&getcgihash(\%cgiparams);

my $infomessage = '';
my $errormessage = '';
my $refresh = '';

if ($cgiparams{'ACTION'} eq $tr{'save'}) {
	if (($cgiparams{'START_HOUR'} * 60) + $cgiparams{'START_MIN'} >
		($cgiparams{'END_HOUR'} * 60) + $cgiparams{'END_MIN'}) {
		$errormessage .= $tr{'from time must be before to time'} ."<br />\n";
	}

	my @machines = split(/\n/, $cgiparams{'MACHINES'});
	my $line = 1;
	foreach (@machines) {
		chomp;
		next if ($_ eq '');
		$errormessage .= $tr{'invalid address'}." '$_' ($line)<br />" unless (&validipormask($_));
		$line++;
	}
		
ERROR:
	if ($errormessage) {
		$cgiparams{'VALID'} = 'no';
	}
	else {
		$cgiparams{'VALID'} = 'yes';
	}
		
	delete $cgiparams{'MACHINES'};
	&writehash("${swroot}/timedaccess/settings", \%cgiparams);
	
	open(FILE, ">${swroot}/timedaccess/machines") or die 'Unable to open machines for writing';
	foreach (@machines) {
		chomp;
		next if ($_ eq '');
		print FILE "$_\n";
	}
	close(FILE);	

	if ($cgiparams{'VALID'} eq 'yes') {
		my $success = message('settimedaccess');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= "settimedaccess ".$tr{'smoothd failure'} ."<br />\n" unless ($success);
	}
}

&readhash("${swroot}/timedaccess/settings", \%cgiparams);

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$cgiparams{'ENABLE'}} = 'CHECKED';

for (my $day = 0; $day < 7; $day++) {
	$checked{"DAY_${day}"}{'on'} = '';
	$checked{"DAY_${day}"}{'off'} = '';
	$checked{"DAY_${day}"}{$cgiparams{"DAY_${day}"}} = 'CHECKED';
}

for (my $hour = 0; $hour < 24; $hour++) {
	$selected{'START_HOUR'}{$hour} = '';
	$selected{'END_HOUR'}{$hour} = '';
}
$selected{'START_HOUR'}{$cgiparams{'START_HOUR'}} = 'SELECTED';
$selected{'END_HOUR'}{$cgiparams{'END_HOUR'}} = 'SELECTED';

for (my $min = 0; $min < 60; $min++) {
	$selected{'START_MIN'}{$min} = '';
	$selected{'END_MIN'}{$min} = '';
}
$selected{'START_MIN'}{$cgiparams{'START_MIN'}} = 'SELECTED';
$selected{'END_MIN'}{$cgiparams{'END_MIN'}} = 'SELECTED';

$selected{'MODE'}{'ALLOW'} = '';
$selected{'MODE'}{'REJECT'} = '';
$selected{'MODE'}{$cgiparams{'MODE'}} = 'SELECTED';

&openpage($tr{'timed access'}, 1, $refresh, 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='post' action='?'><div>\n";

&openbox($tr{'global settingsc'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base' style='width:25%;'>$tr{'enabledc'}</td>
	<td style='width:5%;'><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td class='base' style='width:15%;'>$tr{'modec'}</td>
	<td style='width:55%;'>
	<select name='MODE'>
		<option value='ALLOW' $selected{'MODE'}{'ALLOW'}>$tr{'allow at specified times'}
		<option value='REJECT' $selected{'MODE'}{'REJECT'}>$tr{'reject at specified times'}
	</select></td>
</tr>
</table>
END
;

&closebox();

&openbox($tr{'timed accessc'});
print <<END
<table style='width: 50%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base' style='width:15%;'>$tr{'fromc'}</td>
	<td>
	<select name='START_HOUR'>
END
;

for (my $hour = 0; $hour < 24; $hour++) {
	my $printhour = $hour;
	$printhour = '0'.$hour if ($hour < 10);
	print "		<option value='$hour' $selected{'START_HOUR'}{$hour}>$printhour\n";
}

print <<END
	</select>
:
	<select name='START_MIN'>
END
;

for (my $min = 0; $min < 60; $min++) {
	my $printmin = $min;
	$printmin = '0'.$min if ($min < 10);
	print "		<option value='$min' $selected{'START_MIN'}{$min}>$printmin\n";
}

print <<END
	</select></td>
	<td class='base' style='width:15%;'>$tr{'toc'}</td>
	<td>
	<select name='END_HOUR'>
END
;

for (my $hour = 0; $hour < 24; $hour++) {
	my $printhour = $hour;
	$printhour = '0'.$hour if ($hour < 10);
	print "		<option value='$hour' $selected{'END_HOUR'}{$hour}>$printhour\n";
}

print <<END
	</select>
:
	<select name='END_MIN'>
END
;

for (my $min = 0; $min < 60; $min++) {
	my $printmin = $min;
	$printmin = '0'.$min if ($min < 10);
	print "		<option value='$min' $selected{'END_MIN'}{$min}>$printmin\n";
}

print <<END
	</select></td>
</tr>
</table>
<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
END
;

for (my $day = 0; $day < 7; $day++) {
	print <<END
	<td class='base' >$tr{"day $day"}:</td>
	<td><input type='checkbox' name='DAY_$day' $checked{"DAY_${day}"}{'on'}></td>
END
;
}

print <<END
</tr>
</table>
<br>
END
;

print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align:center;'>$tr{'machinesc'}<br>
	<textarea name='MACHINES' cols='35' rows='6'>
END
;

open(FILE, "${swroot}/timedaccess/machines") or die 'Unable to open machines list';
my @machines = <FILE>;
close(FILE);

foreach (@machines) {
	chomp;
	print "$_\n";
}

print <<END
</textarea><br>
$tr{'enter one ip address or network with netmask address per line'}</td>
</tr>
</table>
END
;

&closebox();

print <<END
<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
        <td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;

print "</div></form>\n";

&alertbox('add', 'add');
&closebigbox();
&closepage();
