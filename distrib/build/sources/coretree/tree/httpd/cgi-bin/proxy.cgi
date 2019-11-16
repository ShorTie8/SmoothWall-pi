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

my (%proxysettings, %netsettings, %mainsettings, %filtersettings);

&readhash("${swroot}/ethernet/settings", \%netsettings);
&readhash("${swroot}/main/settings", \%mainsettings);

# Start of modification by URLfilter
$filtersettings{'CHILDREN'} = '5';

if (-e "${swroot}/urlfilter/settings") {
        &readhash("${swroot}/urlfilter/settings", \%filtersettings);
}
# End of modification by URLfilter

&showhttpheaders();

$proxysettings{'ACTION'} = '';
$proxysettings{'VALID'} = '';

$proxysettings{'UPSTREAM_PROXY'} = '';
$proxysettings{'ENABLE'} = 'off';
$proxysettings{'CACHE_SIZE'} = '500';
$proxysettings{'TRANSPARENT'} = 'off';
$proxysettings{'MAX_SIZE'} = '4096';
$proxysettings{'MIN_SIZE'} = '0';
$proxysettings{'MAX_OUTGOING_SIZE'} = '0';
$proxysettings{'MAX_INCOMING_SIZE'} = '0';

# Start of modification by URLfilter
$proxysettings{'ENABLE_FILTER'} = 'off';
# End of modification by URLfilter

&getcgihash(\%proxysettings);

my $needhup = 0;
my $errormessage = '';
my $infomessage = '';
my $refresh = '';

if ($proxysettings{'ACTION'} eq $tr{'save'} ||
	$proxysettings{'ACTION'} eq $tr{'save and restart with cleared cache'}) { 
	if (!($proxysettings{'CACHE_SIZE'} =~ /^\d+/) || ($proxysettings{'CACHE_SIZE'} < 10)) {
		$errormessage .= $tr{'invalid cache size'}."<br />";
	}
		
	if (!($proxysettings{'MAX_SIZE'} =~ /^\d+/)) {
		$errormessage .= $tr{'invalid maximum object size'}."<br />";
	}

	if (!($proxysettings{'MIN_SIZE'} =~ /^\d+/)) {
		$errormessage .= $tr{'invalid minimum object size'}."<br />";
	}

	if (!($proxysettings{'MAX_OUTGOING_SIZE'} =~ /^\d+/)) {
		$errormessage .= $tr{'invalid maximum outgoing size'}."<br />";
	}

	if (!($proxysettings{'MAX_INCOMING_SIZE'} =~ /^\d+/)) {
		$errormessage .= $tr{'invalid maximum incoming size'}."<br />";
	}

	if ($proxysettings{'PEER_USERNAME'}) {
		unless ($proxysettings{'PEER_PASSWORD'}) {
			$errormessage .= $tr{'password cant be blank'}."<br />";
		}
	}

	if ($errormessage) {
		$proxysettings{'VALID'} = 'no';
	}
	else {
              $proxysettings{'VALID'} = 'yes';
	}
	&writehash("${swroot}/proxy/settings", \%proxysettings);

	if ($proxysettings{'VALID'} eq 'yes') {
		system('/usr/bin/smoothwall/writeproxy.pl');
		my @args;

		if ($proxysettings{'ENABLE'} eq 'on') {
        		@args = ('squidrestart');
        		if ($proxysettings{'ACTION'} eq $tr{'save and restart with cleared cache'}) {
				push(@args, '--clearcache');
			}
		}
		else {
        		@args = ('squidstop');
        		if ($proxysettings{'ACTION'} eq $tr{'save and restart with cleared cache'}) {
				push(@args, '--clearcache');
			}
		}
		my $success = message(@args);
		$infomessage .= $success ."<br />\n" if ($success and $success !~ /fail/i);
		$errormessage .= "@args ".$tr{'smoothd failure'} ."<br />\n" unless ($success and $success !~ /fail/i);
	}
}

&readhash("${swroot}/proxy/settings", \%proxysettings);

my %checked;

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$proxysettings{'ENABLE'}} = 'CHECKED';

$checked{'TRANSPARENT'}{'off'} = '';
$checked{'TRANSPARENT'}{'on'} = '';
$checked{'TRANSPARENT'}{$proxysettings{'TRANSPARENT'}} = 'CHECKED';

# Start of modification by URLfilter
$checked{'ENABLE_FILTER'}{'off'} = '';
$checked{'ENABLE_FILTER'}{'on'} = '';
$checked{'ENABLE_FILTER'}{$proxysettings{'ENABLE_FILTER'}} = 'CHECKED';
# End of modification by URLfilter

&openpage($tr{'web proxy configuration'}, 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'web proxyc'});
print <<END
<table width='100%'>
<tr>
	<td class='base'>$tr{'enabledc'}</td>
	<td><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td class='base'>$tr{'urlfilter enabled'}</td>
	<td><input type='checkbox' name='ENABLE_FILTER' $checked{'ENABLE_FILTER'}{'on'} /></td>
</tr>
<tr>
	<td class='base'>$tr{'transparent'}</td>
	<td><input type='checkbox' name='TRANSPARENT' $checked{'TRANSPARENT'}{'on'}></td>
	<td></td>
	<td></td>
</tr>
<tr>
	<td colspan='4'>&nbsp;</td>
</tr>
<tr>
	<td style='width:25%;' class='base'>$tr{'cache size'}</td>
	<td style='width:25%;'><input type='text' name='CACHE_SIZE' value='$proxysettings{'CACHE_SIZE'}' SIZE='5'></td>
	<td style='width:25%;' class='base'><img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;$tr{'remote proxy'}</td>
	<td style='width:25%;'><input type='text' name='UPSTREAM_PROXY' value='$proxysettings{'UPSTREAM_PROXY'}'></td>
</tr>
<tr>
	<td class='base'><img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;$tr{'remote proxy username'}</td>
	<td><input type='text' name='PEER_USERNAME' value='$proxysettings{'PEER_USERNAME'}'></td>
	<td class='base'>$tr{'remote proxy password'}</td>
	<td><input type='password' name='PEER_PASSWORD' value='$proxysettings{'PEER_PASSWORD'}'></td>
</tr>
<tr>
	<td class='base'>$tr{'max size'}</td>
	<td><input type='text' name='MAX_SIZE' value='$proxysettings{'MAX_SIZE'}' SIZE='5'></td>
	<td class='base'>$tr{'min size'}</td>
	<td><input type='text' name='MIN_SIZE' value='$proxysettings{'MIN_SIZE'}' SIZE='5'></td>
</tr>
<tr>
	<td class='base'>$tr{'max outgoing size'}</td>
	<td><input type='text' name='MAX_OUTGOING_SIZE' value='$proxysettings{'MAX_OUTGOING_SIZE'}' SIZE='5'></td>
	<td class='base'>$tr{'max incoming size'}</td>
	<td><input type='text' name='MAX_INCOMING_SIZE' value='$proxysettings{'MAX_INCOMING_SIZE'}' SIZE='5'></td>
</tr>
</table>
<BR>
<img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;
<span class='base'>$tr{'these fields may be blank'}</span>
END
;
&closebox();


print <<END
<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
        <td style='width:50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
        <td style='width:50%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'save and restart with cleared cache'}'></td>
</tr>
</table>
END
;

print "</div></form>\n";

&alertbox('add', 'add');

&closebigbox();

&closepage();
