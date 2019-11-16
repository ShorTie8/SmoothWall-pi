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

my (%remotesettings, %checked);
my $errormessage='';
my $infomessage='';

&showhttpheaders();

$remotesettings{'ENABLE_SSH'} = 'off';
$remotesettings{'ENABLE_SECURE_ADMIN'} = 'off';
$remotesettings{'ACTION'} = '';

my $refresh = '';
my $success = '';

&getcgihash(\%remotesettings);

if ($remotesettings{'ACTION'} eq $tr{'save'}) {
	&writehash("${swroot}/remote/settings", \%remotesettings);

	if ($remotesettings{'ENABLE_SSH'} eq 'on') {
		&log($tr{'ssh is enabled'});
		$success = message('sshdrestart');
	}
	else {
		&log($tr{'ssh is disabled'});
		$success = message('sshdstop');
	}
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= "sshd ".$tr{'smoothd failure'} ."<br />\n" unless ($success);
}

$remotesettings{'ENABLE_SECURE_ADMIN'} = 'off';
&readhash("${swroot}/remote/settings", \%remotesettings);

$checked{'ENABLE_SSH'}{'off'} = '';
$checked{'ENABLE_SSH'}{'on'} = '';
$checked{'ENABLE_SSH'}{$remotesettings{'ENABLE_SSH'}} = 'CHECKED';

$checked{'ENABLE_SECURE_ADMIN'}{'off'} = '';
$checked{'ENABLE_SECURE_ADMIN'}{'on'} = '';
$checked{'ENABLE_SECURE_ADMIN'}{$remotesettings{'ENABLE_SECURE_ADMIN'}} = 'CHECKED';

&openpage($tr{'remote access'}, 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'remote access2'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>SSH:</td>
	<td style='width:25%;'><input type='checkbox' name='ENABLE_SSH' $checked{'ENABLE_SSH'}{'on'}></td>
	<td style='width:25%;' class='base'><img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;$tr{'secure admin'}</td>
	<td style='width:25%;'><input type='checkbox' name='ENABLE_SECURE_ADMIN' $checked{'ENABLE_SECURE_ADMIN'}{'on'}></td>
</tr>
</table>
<br />
<img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;
<span class='base'>$tr{'secure admin long'}</span>
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
