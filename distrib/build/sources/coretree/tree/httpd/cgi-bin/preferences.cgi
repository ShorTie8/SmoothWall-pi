#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

my (%cgiparams, %settingsParams, %uiSettingsParams, %checked, %selected, %settings, %uisettings);
my $method;
my $infomessage = '';
my $errormessage = '';

$cgiparams{'ACTION'} = '';
$cgiparams{'MENU'} = 'off';
$cgiparams{'ALWAYS_ENGLISH'} = 'off';
$cgiparams{'LANGUAGE'} = 'en';
$cgiparams{'HOSTNAME'} = '';
$cgiparams{'KEYMAP'} = '';
$cgiparams{'OPENNESS'} = '';

&getcgihash(\%cgiparams);

if ($cgiparams{'ACTION'} eq $tr{'save'}) {
	$settingsParams{'LANGUAGE'} = $cgiparams{'LANGUAGE'};
	$settingsParams{'HOSTNAME'} = $cgiparams{'HOSTNAME'};
	$settingsParams{'KEYMAP'} = $cgiparams{'KEYMAP'};
	$settingsParams{'OPENNESS'} = $cgiparams{'OPENNESS'};

	$uiSettingsParams{'MENU'} = $cgiparams{'MENU'};
	$uiSettingsParams{'ALWAYS_ENGLISH'} = $cgiparams{'ALWAYS_ENGLISH'};
	
	&writehash("${swroot}/main/settings", \%settingsParams);
	&writehash("${swroot}/main/uisettings", \%uiSettingsParams);
	&readhash("${swroot}/main/settings", \%settings);
	&readhash("${swroot}/main/uisettings", \%uisettings);
	$language = $settings{'LANGUAGE'};
	if (($ENV{'HTTPS'}) && $ENV{'HTTPS'} eq "on") {
		$method = "https:";
	}
	else {
		$method = "http:";
	}
	print "Location: ${method}//$ENV{'HTTP_HOST'}$ENV{'REQUEST_URI'}\n\n";
}

&showhttpheaders();

if ($cgiparams{'ACTION'} eq '') {
	$cgiparams{'MENU'} = 'on';
	$cgiparams{'ALWAYS_ENGLISH'} = 'on';
}

&readhash("${swroot}/main/uisettings", \%cgiparams);
&readhash("${swroot}/main/settings", \%cgiparams);

$checked{'MENU'}{'off'} = '';
$checked{'MENU'}{'on'} = '';
$checked{'MENU'}{$cgiparams{'MENU'}} = "CHECKED";

$checked{'ALWAYS_ENGLISH'}{'off'} = '';
$checked{'ALWAYS_ENGLISH'}{'on'} = '';
$checked{'ALWAYS_ENGLISH'}{$cgiparams{'ALWAYS_ENGLISH'}} = "CHECKED";

&openpage( $tr{'preferences'}, 1, '', 'maintenance');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='post' action = '?'><div>\n";
print "	<input type='hidden' name='HOSTNAME' value='$cgiparams{'HOSTNAME'}'>\n";
print "	<input type='hidden' name='KEYMAP' value='$cgiparams{'KEYMAP'}'>\n";
print "	<input type='hidden' name='OPENNESS' value='$cgiparams{'OPENNESS'}'>\n";

&openbox($tr{'user interface'});

print "
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'drop down menus'}</td>
	<td style='width: 25%;'><input type='checkbox' name='MENU' $checked{'MENU'}{'on'}></td>
	<td class='base' style='width: 25%;'>$tr{'always use english'}</td>
	<td style='width: 25%;'><input type='checkbox' name='ALWAYS_ENGLISH' $checked{'ALWAYS_ENGLISH'}{'on'}></td>
</tr>
</table>
";

&closebox();

print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width: 100%; text-align: center;'>
		<input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;

print "</div></form>\n";

&closebigbox();

&closepage();
