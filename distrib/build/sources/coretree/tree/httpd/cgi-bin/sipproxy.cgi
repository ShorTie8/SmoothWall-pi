#!/usr/bin/perl
#
# SmoothWall CGIs
#
# (c) SmoothWall Ltd, 2005

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use strict;
use warnings;

my (%sipsettings, %checked, %selected);

&showhttpheaders();

$sipsettings{'ACTION'} = '';
$sipsettings{'ENABLE'} = 'off';
$sipsettings{'LOG_CALLS'} = 'off';
$sipsettings{'TRANSPARENT'} = 'off';

&getcgihash(\%sipsettings);

my $errormessage = '';
my $infomessage = '';
my $refresh = '';
my $success = '';

if ($sipsettings{'ACTION'} eq $tr{'save'}) {
	&writehash("${swroot}/sipproxy/settings", \%sipsettings);
	system("/usr/bin/smoothwall/writesiproxdconf.pl");

	if ($sipsettings{'ENABLE'} eq 'on') {
		&log("SIP service restarted.");
		$success = message("siprestart");
	}
	else {
		&log("SIP service stopped.");
		$success = message("sipstop");
	}
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= "sip ".$tr{'smoothd failure'} ."<br />\n" unless ($success);
}

if ($sipsettings{'ACTION'} eq '') {
	$sipsettings{'LOGGING'} = '0';
	$sipsettings{'LOG_CALLS'} = 'on';
	$sipsettings{'CLIENTS'} = '50';
	
	&readhash("${swroot}/sipproxy/settings", \%sipsettings);
}

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$sipsettings{'ENABLE'}} = 'CHECKED';

$checked{'TRANSPARENT'}{'off'} = '';
$checked{'TRANSPARENT'}{'on'} = '';
$checked{'TRANSPARENT'}{$sipsettings{'TRANSPARENT'}} = 'CHECKED';

$checked{'LOG_CALLS'}{'off'} = '';
$checked{'LOG_CALLS'}{'on'} = '';
$checked{'LOG_CALLS'}{$sipsettings{'LOG_CALLS'}} = 'CHECKED';

$selected{'LOGGING'}{'0'} = '';
$selected{'LOGGING'}{'1'} = '';
$selected{'LOGGING'}{'2'} = '';
$selected{'LOGGING'}{$sipsettings{'LOGGING'}} = 'SELECTED';

$selected{'CLIENTS'}{'5'} = '';
$selected{'CLIENTS'}{'10'} = '';
$selected{'CLIENTS'}{'50'} = '';
$selected{'CLIENTS'}{'100'} = '';
$selected{'CLIENTS'}{'200'} = '';
$selected{'CLIENTS'}{$sipsettings{'CLIENTS'}} = 'SELECTED';

&openpage($tr{'sip'}, 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'session initiation protocol'});

print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'enabledc'}</td>
	<td style='width:25%;'><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td class='base'>$tr{'sip logging level'}</td>
	<td><select name='LOGGING'>
		<option value='0' $selected{'LOGGING'}{'0'}>$tr{'sip normal'}
		<option value='1' $selected{'LOGGING'}{'1'}>$tr{'sip detailed'}
		<option value='2' $selected{'LOGGING'}{'2'}>$tr{'sip very detailed'}
	</select></td>
</tr>
<tr>
	<td class='base'>$tr{'log calls'}</td>
	<td><input type='checkbox' name='LOG_CALLS' $checked{'LOG_CALLS'}{'on'}></td>
	<td class='base'>$tr{'maximum number of clients'}</td>
	<td><select name='CLIENTS'>
		<option value='5' $selected{'CLIENTS'}{'5'}>5
		<option value='10' $selected{'CLIENTS'}{'10'}>10
		<option value='50' $selected{'CLIENTS'}{'50'}>50
		<option value='100' $selected{'CLIENTS'}{'100'}>100
		<option value='200' $selected{'CLIENTS'}{'200'}>200
	</select></td>
</tr>
<tr>
	<td class='base'>$tr{'sip transparent'}</td>
	<td><input type='checkbox' name='TRANSPARENT' $checked{'TRANSPARENT'}{'on'}></td>
	<td>&nbsp;</td>
	<td>&nbsp;</td>
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
