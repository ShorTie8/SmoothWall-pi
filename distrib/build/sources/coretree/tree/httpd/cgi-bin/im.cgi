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

my %imsettings;
my %netsettings;
my %mainsettings;

&readhash("${swroot}/ethernet/settings", \%netsettings);
&readhash("${swroot}/main/settings", \%mainsettings);


$imsettings{'ACTION'} = '';
$imsettings{'VALID'} = '';

$imsettings{'ENABLE'} = 'off';
$imsettings{'FILTERING'} = 'off';
$imsettings{'MSN'} = 'off';
$imsettings{'ICQ'} = 'off';
$imsettings{'YAHOO'} = 'off';
$imsettings{'IRC'} = 'off';
$imsettings{'GG'} = 'off';
$imsettings{'XMPP'} = 'off';
$imsettings{'SSL'} = 'off';

&getcgihash(\%imsettings);

my $errormessage = '';
my $infomessage = '';
my $refresh = '';
my $success = '';

if ($imsettings{'ACTION'} eq $tr{'save'}) { 
ERROR:
	if ($errormessage) {
		$imsettings{'VALID'} = 'no';
	}
	else {
		$imsettings{'VALID'} = 'yes';
	}

	&writehash("${swroot}/im/settings", \%imsettings);

	if ($imsettings{'VALID'} eq 'yes') {
		system('/usr/bin/smoothwall/writeim.pl');

		if ($imsettings{'ENABLE'} eq 'on') {
			$success = message('imrestart');
		}
		else {
			$success = message('imstop');
		}
		$infomessage .= $success ."<br />\n" if ($success and $success !~ /fail/i);
		$errormessage .= "imspector ".$tr{'smoothd failure'} ."<br />\n" unless ($success and $success !~ /fail/i);
	}
}

if ($imsettings{'ACTION'} eq $tr{'download ca certificate'}) {
	&outputfile('/etc/httpd/server.crt', 'IM CA.pem');
}

if ($imsettings{'ACTION'} eq '') {
	$imsettings{'MSN'} = 'on';
	$imsettings{'ICQ'} = 'on';
	$imsettings{'YAHOO'} = 'on';
	$imsettings{'GG'} = 'on';
	$imsettings{'JABBER'} = 'on';
	$imsettings{'SSL'} = 'on';
}

&readhash("${swroot}/im/settings", \%imsettings);

my %checked;

$checked{'MSN'}{'off'} = '';
$checked{'MSN'}{'on'} = '';
$checked{'MSN'}{$imsettings{'MSN'}} = 'CHECKED';

$checked{'ICQ'}{'off'} = '';
$checked{'ICQ'}{'on'} = '';
$checked{'ICQ'}{$imsettings{'ICQ'}} = 'CHECKED';

$checked{'YAHOO'}{'off'} = '';
$checked{'YAHOO'}{'on'} = '';
$checked{'YAHOO'}{$imsettings{'YAHOO'}} = 'CHECKED';

$checked{'IRC'}{'off'} = '';
$checked{'IRC'}{'on'} = '';
$checked{'IRC'}{$imsettings{'IRC'}} = 'CHECKED';

$checked{'GG'}{'off'} = '';
$checked{'GG'}{'on'} = '';
$checked{'GG'}{$imsettings{'GG'}} = 'CHECKED';

$checked{'XMPP'}{'off'} = '';
$checked{'XMPP'}{'on'} = '';
$checked{'XMPP'}{$imsettings{'XMPP'}} = 'CHECKED';

$checked{'SSL'}{'off'} = '';
$checked{'SSL'}{'on'} = '';
$checked{'SSL'}{$imsettings{'SSL'}} = 'CHECKED';

$checked{'FILTERING'}{'off'} = '';
$checked{'FILTERING'}{'on'} = '';
$checked{'FILTERING'}{$imsettings{'FILTERING'}} = 'CHECKED';

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$imsettings{'ENABLE'}} = 'CHECKED';

&showhttpheaders();

&openpage('IM proxy configuration', 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox('IM proxy:');
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'enabledc'}</td>
	<td style='width:25%;'><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td style='width:25%;' class='base'>Swear-word filtering:</td>
	<td style='width:25%;'><input type='checkbox' name='FILTERING' $checked{'FILTERING'}{'on'}></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'im protocols'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>MSN:</td>
	<td style='width:25%;'><input type='checkbox' name='MSN' $checked{'MSN'}{'on'}></td>
	<td style='width:25%;' class='base'>ICQ and AIM:</td>
	<td style='width:25%;'><input type='checkbox' name='ICQ' $checked{'ICQ'}{'on'}></td>
</tr>
<tr>
	<td class='base'>Yahoo:</td>
	<td><input type='checkbox' name='YAHOO' $checked{'YAHOO'}{'on'}></td>
	<td class='base'>IRC:</td>
	<td><input type='checkbox' name='IRC' $checked{'IRC'}{'on'}></td>
</tr>
<tr>
	<td class='base'>Gadu-Gadu:</td>
	<td><input type='checkbox' name='GG' $checked{'GG'}{'on'}></td>
	<td class='base'>Jabber and Gtalk:</td>
	<td><input type='checkbox' name='XMPP' $checked{'XMPP'}{'on'}></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'im ssl'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'im ssl mitm'}</td>
	<td style='width:25%;'><input type='checkbox' name='SSL' $checked{'SSL'}{'on'}></td>
	<td style='width:50%;' align='center'>
	<input type='submit' name='ACTION' value='$tr{'download ca certificate'}'>
	</td>
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
