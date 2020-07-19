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

$remotesettings{'ENABLE_SSH_GREEN'} = 'off';
$remotesettings{'ENABLE_HTTP_GREEN'} = 'off';
$remotesettings{'ENABLE_HTTPS_GREEN'} = 'off';
$remotesettings{'ENABLE_SSH_PURPLE'} = 'off';
$remotesettings{'ENABLE_HTTP_PURPLE'} = 'off';
$remotesettings{'ENABLE_HTTPS_PURPLE'} = 'off';
$remotesettings{'ENABLE_SECURE_ADMIN'} = 'off';
$remotesettings{'ACTION'} = '';

my $refresh = '';
my $success = '';

&getcgihash(\%remotesettings);

if ($remotesettings{'ACTION'} eq $tr{'save'}) {
	&writehash("${swroot}/remote/settings", \%remotesettings);

	if ($remotesettings{'ENABLE_SSH_GREEN'} eq 'on'
	 || $remotesettings{'ENABLE_SSH_PURPLE'} eq 'on') {
		&log($tr{'ssh is enabled'});
	}
	else {
		&log($tr{'ssh is disabled'});
	}
	if ($remotesettings{'ENABLE_HTTP_GREEN'} eq 'on'
	 || $remotesettings{'ENABLE_HTTP_PURPLE'} eq 'on') {
		&log($tr{'http access is allowed'});
	}
	else {
		&log($tr{'http access is disabled'});
	}
	if ($remotesettings{'ENABLE_HTTPS_GREEN'} eq 'on'
	 || $remotesettings{'ENABLE_HTTPS_PURPLE'} eq 'on') {
		&log($tr{'https access is enabled'});
	}
	else {
		&log($tr{'https access is disabled'});
	}
	$success = message('sshdrestart');
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= "Remote Access restart failed." unless ($success);
}

$remotesettings{'ENABLE_SECURE_ADMIN'} = 'off';
&readhash("${swroot}/remote/settings", \%remotesettings);

$checked{'ENABLE_SSH_GREEN'}{'off'} = '';
$checked{'ENABLE_SSH_GREEN'}{'on'} = '';
$checked{'ENABLE_SSH_GREEN'}{$remotesettings{'ENABLE_SSH_GREEN'}} = 'CHECKED';
$checked{'ENABLE_HTTP_GREEN'}{'off'} = '';
$checked{'ENABLE_HTTP_GREEN'}{'on'} = '';
$checked{'ENABLE_HTTP_GREEN'}{$remotesettings{'ENABLE_HTTP_GREEN'}} = 'CHECKED';
$checked{'ENABLE_HTTPS_GREEN'}{'off'} = '';
$checked{'ENABLE_HTTPS_GREEN'}{'on'} = '';
$checked{'ENABLE_HTTPS_GREEN'}{$remotesettings{'ENABLE_HTTPS_GREEN'}} = 'CHECKED';
$checked{'ENABLE_SSH_PURPLE'}{'off'} = '';
$checked{'ENABLE_SSH_PURPLE'}{'on'} = '';
$checked{'ENABLE_SSH_PURPLE'}{$remotesettings{'ENABLE_SSH_PURPLE'}} = 'CHECKED';
$checked{'ENABLE_HTTP_PURPLE'}{'off'} = '';
$checked{'ENABLE_HTTP_PURPLE'}{'on'} = '';
$checked{'ENABLE_HTTP_PURPLE'}{$remotesettings{'ENABLE_HTTP_PURPLE'}} = 'CHECKED';
$checked{'ENABLE_HTTPS_PURPLE'}{'off'} = '';
$checked{'ENABLE_HTTPS_PURPLE'}{'on'} = '';
$checked{'ENABLE_HTTPS_PURPLE'}{$remotesettings{'ENABLE_HTTPS_PURPLE'}} = 'CHECKED';

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
	<td style='width:25%;' class='base'>$tr{'ssh enable green'}:</td>
	<td style='width:35%;'>
          SSH: <input type='checkbox' name='ENABLE_SSH_GREEN' $checked{'ENABLE_SSH_GREEN'}{'on'}>
          HTTP: <input type='checkbox' name='ENABLE_HTTP_GREEN' $checked{'ENABLE_HTTP_GREEN'}{'on'}>
          HTTPS: <input type='checkbox' name='ENABLE_HTTPS_GREEN' $checked{'ENABLE_HTTPS_GREEN'}{'on'}>
        </td>
	<td rowspan=2 style='width:25%;' class='base'><img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;$tr{'secure admin'}</td>
	<td rowspan=2 style='width:15%;'><input type='checkbox' name='ENABLE_SECURE_ADMIN' $checked{'ENABLE_SECURE_ADMIN'}{'on'}></td>
</tr>
<tr>
	<td style='width:25%;' class='base'>$tr{'ssh enable purple'}:</td>
	<td style='width:35%;'>
          SSH: <input type='checkbox' name='ENABLE_SSH_PURPLE' $checked{'ENABLE_SSH_PURPLE'}{'on'}>
          HTTP: <input type='checkbox' name='ENABLE_HTTP_PURPLE' $checked{'ENABLE_HTTP_PURPLE'}{'on'}>
          HTTPS: <input type='checkbox' name='ENABLE_HTTPS_PURPLE' $checked{'ENABLE_HTTPS_PURPLE'}{'on'}>
        </td>
	
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
