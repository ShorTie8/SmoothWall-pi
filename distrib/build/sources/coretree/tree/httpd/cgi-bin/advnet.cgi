#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) SmoothWall Ltd, 2002-2003

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use strict;
use warnings;

my (%advnetsettings,%checked, %selected);
my $refresh = '';
my $infomessage = '';
my $errormessage = '';
my $success = '';

&showhttpheaders();

# These defaults must be 'off'; the system defaults must be set in the advnet settings file.
$advnetsettings{'ENABLE_NOPING'} = 'off';
$advnetsettings{'ENABLE_COOKIES'} = 'off';
$advnetsettings{'ENABLE_NOIGMP'} = 'off';
$advnetsettings{'ENABLE_NOMULTICAST'} = 'off';
$advnetsettings{'ENABLE_UPNP'} = 'off';
$advnetsettings{'LOG_INVALID'} = 'off';
$advnetsettings{'BAD_TRAFFIC'} = 'REJECT';
$advnetsettings{'ACTION'} = '';
&getcgihash(\%advnetsettings);

if ($advnetsettings{'ACTION'} eq $tr{'save'}) {
	&writehash("${swroot}/advnet/settings", \%advnetsettings);
	
	$success = message('setadvnet');
	$infomessage .= $success."<br />" if ($success);
	$errormessage .= "setadvnet ".$tr{'smoothd failure'}."<br />" unless ($success);

	if ($advnetsettings{'ENABLE_UPNP'} eq 'on') {
		$success = message('upnpdrestart');
		$infomessage .= $success."<br />" if ($success);
		$errormessage .= "upnpdrestart ".$tr{'smoothd failure'}."<br />" unless ($success);
	}
	else {
		$success = message('upnpdstop');
		$infomessage .= $success."<br />" if ($success);
		$errormessage .= "upnpdstop ".$tr{'smoothd failure'}."<br />" unless ($success);
	}
}

&readhash("${swroot}/advnet/settings", \%advnetsettings);

$checked{'ENABLE_NOPING'}{'off'} = '';
$checked{'ENABLE_NOPING'}{'on'} = '';
$checked{'ENABLE_NOPING'}{$advnetsettings{'ENABLE_NOPING'}} = 'CHECKED';

$checked{'ENABLE_COOKIES'}{'off'} = '';
$checked{'ENABLE_COOKIES'}{'on'} = '';
$checked{'ENABLE_COOKIES'}{$advnetsettings{'ENABLE_COOKIES'}} = 'CHECKED';

$checked{'ENABLE_NOIGMP'}{'off'} = '';
$checked{'ENABLE_NOIGMP'}{'on'} = '';
$checked{'ENABLE_NOIGMP'}{$advnetsettings{'ENABLE_NOIGMP'}} = 'CHECKED';

$checked{'ENABLE_NOMULTICAST'}{'off'} = '';
$checked{'ENABLE_NOMULTICAST'}{'on'} = '';
$checked{'ENABLE_NOMULTICAST'}{$advnetsettings{'ENABLE_NOMULTICAST'}} = 'CHECKED';

$checked{'ENABLE_UPNP'}{'off'} = '';
$checked{'ENABLE_UPNP'}{'on'} = '';
$checked{'ENABLE_UPNP'}{$advnetsettings{'ENABLE_UPNP'}} = 'CHECKED';

$checked{'LOG_INVALID'}{'off'} = '';
$checked{'LOG_INVALID'}{'on'} = '';
$checked{'LOG_INVALID'}{$advnetsettings{'LOG_INVALID'}} = 'CHECKED';

$selected{'BAD_TRAFFIC'}{'REJECT'} = '';
$selected{'BAD_TRAFFIC'}{'DROP'} = '';
$selected{'BAD_TRAFFIC'}{$advnetsettings{'BAD_TRAFFIC'}} = 'SELECTED';

&openpage($tr{'advanced networking features'}, 1, $refresh, 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'advanced networking featuresc'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:38%;' class='base'>$tr{'block icmp ping'}</td>
	<td style='width:12%;'><input type='checkbox' style='vertical-align:middle' name='ENABLE_NOPING' $checked{'ENABLE_NOPING'}{'on'}></td>
	<td style='width:38%;' class='base'>$tr{'enable syn cookies'}</td>
	<td style='width:12%;'><input type='checkbox' style='vertical-align:middle' name='ENABLE_COOKIES' $checked{'ENABLE_COOKIES'}{'on'}></td>
</tr>
<tr>
	<td style='width:38%;' class='base'>$tr{'block and ignore igmp packets'}</td>
	<td style='width:12%;'><input type='checkbox' style='vertical-align:middle' name='ENABLE_NOIGMP' $checked{'ENABLE_NOIGMP'}{'on'}></td>
	<td style='width:38%;' class='base'>$tr{'block and ignore multicast traffic'}</td>
	<td style='width:12%;'><input type='checkbox' style='vertical-align:middle' name='ENABLE_NOMULTICAST' $checked{'ENABLE_NOMULTICAST'}{'on'}></td>
</tr>
<tr>
	<td style='width:38%;' class='base'>$tr{'upnp support'}</td>
	<td style='width:12%;'><input type='checkbox' style='vertical-align:middle' name='ENABLE_UPNP' $checked{'ENABLE_UPNP'}{'on'}></td>
	<td style='width:38%;' class='base'>$tr{'log invalid'}</td>
	<td style='width:12%;'><input type='checkbox' style='vertical-align:middle' name='LOG_INVALID' $checked{'LOG_INVALID'}{'on'}></td>
</tr>
<tr>
	<td></td>
	<td></td>
	<td style='width:38%;' class='base'>$tr{'action to perform on bad external traffic'}</td>
	<td style='width:12%;'>
	<select name='BAD_TRAFFIC'>
		<option value='REJECT' $selected{'BAD_TRAFFIC'}{'REJECT'}>$tr{'reject'}
		<option value='DROP' $selected{'BAD_TRAFFIC'}{'DROP'}>$tr{'drop'}
	</select></td>
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

&closebigbox();
&closepage();
