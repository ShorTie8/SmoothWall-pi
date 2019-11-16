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
use strict;
use warnings;

my %modemsettings;
my $infomessage = '';
my $errormessage = '';

&showhttpheaders();

$modemsettings{'ACTION'} = '';
$modemsettings{'VALID'} = '';

&getcgihash(\%modemsettings);

if ($modemsettings{'ACTION'} eq $tr{'save'}) {
	if (!($modemsettings{'TIMEOUT'} =~ /^\d+$/)) {
		$errormessage .= $tr{'timeout must be a number'}."<br />";
	}

	unless ($modemsettings{'INIT'} 
	   and ($modemsettings{'INIT'} =~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage .= $tr{'modem invalid init'}."<br />";
	}

	unless ($modemsettings{'HANGUP'} 
	   and ($modemsettings{'HANGUP'} =~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage .= $tr{'modem invalid hangup'}."<br />";
	}

	unless ($modemsettings{'SPEAKER_ON'} 
	   and ($modemsettings{'SPEAKER_ON'} =~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage .= $tr{'modem invalid speaker'}."<br />"; 
	}

	unless ($modemsettings{'SPEAKER_OFF'} 
	   and ($modemsettings{'SPEAKER_OFF'} =~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage .= $tr{'modem invalid speaker'}."<br />"; 
	}

	unless ($modemsettings{'TONE_DIAL'} 
	   and ($modemsettings{'TONE_DIAL'} =~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage .= $tr{'modem invalid tone dial'}."<br />"; 
	}

	unless ($modemsettings{'PULSE_DIAL'} 
	   and ($modemsettings{'PULSE_DIAL'} =~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage .= $tr{'modem invalid pulse dial'}."<br />";
	}
  
	if ($errormessage) {
		$modemsettings{'VALID'} = 'no'; }
	else {
		$modemsettings{'VALID'} = 'yes'; }

	&writehash("${swroot}/modem/settings", \%modemsettings);
	$infomessage .= "Modem settings saved.<br />\n";
}

if ($modemsettings{'ACTION'} eq $tr{'restore defaults'}) {
	system('/bin/cp', "${swroot}/modem/defaults", "${swroot}/modem/settings", '-f');
}

&readhash("${swroot}/modem/settings", \%modemsettings);

&openpage($tr{'modem configuration'}, 1, '', 'maintenance');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'modem configurationc'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'><IMG SRC='/ui/img/blob.gif' alt='*' 
		style='vertical-align: text-top;'>&nbsp;$tr{'init string'}</td>
	<td style='width:25%;'><input type='text' name='INIT' value='$modemsettings{'INIT'}' id='init' 
		@{[jsvalidregex('init','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]}></td>
	<td style='width:25%;' class='base'><IMG SRC='/ui/img/blob.gif' alt='*' 
		style='vertical-align: text-top;'>&nbsp;$tr{'hangup string'}</td>
	<td style='width:25%;'><input type='text' name='HANGUP' value='$modemsettings{'HANGUP'}' id='hangup' 
		@{[jsvalidregex('hangup','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]} ></td>
</tr>
<tr>
	<td class='base'><IMG SRC='/ui/img/blob.gif' alt='*' 
		style='vertical-align: text-top;'>&nbsp;$tr{'speaker on'}</td>
	<td><input type='text' name='SPEAKER_ON' value='$modemsettings{'SPEAKER_ON'}' id='speakeron' 
		@{[jsvalidregex('speakeron','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]} ></td>
	<td class='base'><IMG SRC='/ui/img/blob.gif' alt='*' 
		style='vertical-align: text-top;'>&nbsp;$tr{'speaker off'}</td>
	<td><input type='text' name='SPEAKER_OFF' value='$modemsettings{'SPEAKER_OFF'}' id='speakeroff' 
		@{[jsvalidregex('speakeroff','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]} ></td>
</tr>
<tr>
	<td class='base'><IMG SRC='/ui/img/blob.gif' alt='*' 
		style='vertical-align: text-top;'>&nbsp;$tr{'tone dial'}</td>
	<td><input type='text' name='TONE_DIAL' value='$modemsettings{'TONE_DIAL'}' id='tone' 
		@{[jsvalidregex('tone','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]} ></td>
	<td class='base'><IMG SRC='/ui/img/blob.gif' alt='*' 
		style='vertical-align: text-top;'>&nbsp;$tr{'pulse dial'}</td>
	<td><input type='text' name='PULSE_DIAL' value='$modemsettings{'PULSE_DIAL'}' id='pulse' 
		@{[jsvalidregex('pulse','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]} ></td>
</tr>
<tr>
	<td class='base'>$tr{'connect timeout'}</td>
	<td><input type='text' name='TIMEOUT' value='$modemsettings{'TIMEOUT'}' id='timeout' 
		@{[jsvalidnumber('timeout','0','10000000')]}></td>
	<td class='base'>&nbsp;</td>
	<td>&nbsp;</td>
</tr>

</table>
<br />
<div class='base'><IMG SRC='/ui/img/blob.gif' alt='*' 
	style='vertical-align: text-top;'>&nbsp;$tr{'these fields may be blank'}</div>
END
;
&closebox();

print <<END
<table style='width: 80%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'restore defaults'}'></td>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;

print "</div></form>\n";

&alertbox('add','add');

&closebigbox();

&closepage();
