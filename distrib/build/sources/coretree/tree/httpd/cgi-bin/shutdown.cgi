#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use Digest::SHA qw(sha1_hex);
use header qw( :standard );
use smoothd qw( message );
use strict;
use warnings;

my %cgiparams;
my $infomessage = '';
my $errormessage = '';
my $refresh = '';
my $death = 0;
my $rebirth = 0;
my ($lastToken, $newToken, $rtnToken);
my $tmp = "";

# Generate a new token and the previous token on each entry.
foreach my $token ("1","2","3") {
	if (open TKN,"</usr/etc/token${token}.sum") {
		$tmp .= <TKN>;
		close TKN;
	}
	else {
		$errormessage .= "Can't read token${token}.<br />";
	}
}

my $time = time;
my $life = 10;	# seconds
my $toSum = $tmp . int($time/$life) ."\n";
$newToken = sha1_hex $toSum;
$toSum = $tmp . int($time/$life - 1) ."\n";
$lastToken = sha1_hex $toSum;

# Clear these, just in case
undef $time;
undef $toSum;
undef $tmp;

$cgiparams{'ACTION'} = '';

&getcgihash(\%cgiparams);
$rtnToken = $cgiparams{'Token'};

&showhttpheaders();

if ($cgiparams{'ACTION'} eq $tr{'shutdown'} or $cgiparams{'ACTION'} eq $tr{'reboot'}) {
	# Validate $rtnToken, then compare it with $newToken and $lastToken
	if ($rtnToken !~ /[0-9a-f]/ or ($rtnToken ne $newToken and $rtnToken ne $lastToken)) {
		$errormessage = "$tr{'token error 1'}<br /><br />$tr{'token error 2'}<br />";
		$refresh = '<meta http-equiv="refresh" content="6; url=index.cgi">';
		goto ERROR;
	}
}

if ($cgiparams{'ACTION'} eq $tr{'shutdown'}) {
	$death = 1;
	
	&log($tr{'shutting down smoothwall'});
	
	my $success = message('systemshutdown');
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
}
elsif ($cgiparams{'ACTION'} eq $tr{'reboot'}) {
	$rebirth = 1;

	&log($tr{'rebooting smoothwall'});

	my $success = message('systemrestart');
	$infomessage .= $success ."<br />\n" if ($success);
	$errormessage .= $tr{'smoothd failure'} ."<br />\n" unless ($success);
}

ERROR:

if ($death == 0 && $rebirth == 0) {

	&openpage($tr{'shutdown control'}, 1, $refresh, 'maintenance');

	&openbigbox('100%', 'LEFT');

	&alertbox($errormessage, "", $infomessage);

	print "<form method='post' action='?'><div>\n";
	print "  <input type='hidden' name='Token' value='$newToken'>\n";

	&openbox($tr{'shutdown2'});
	my $myName = `hostname`;
	chomp $myName;
	$myName = " ($myName)";

	print <<END
<table width='100%'>
<tr>
	<td align='center'>
        <input type='submit' name='ACTION' value='$tr{'reboot'}'
               onClick="return confirm('Are you sure you want to reboot this Smoothwall$myName?');">
	</td>
	<td align='center'>
		<input type='submit' name='ACTION' value='$tr{'shutdown'}'
               onClick="return confirm('Are you sure you want to shutdown this Smoothwall$myName?');">
	</td>
</tr>
</table>
END
;
	&closebox();

	print "</div></form>\n";
}
else {
	my ($message,$title);
	if ($death) {
		$title = $tr{'shutting down'};
		$infomessage = $tr{'smoothwall is shutting down'};
	}
	else {
		$title = $tr{'rebooting'};
		$infomessage = $tr{'smoothwall is rebooting'};
	}

	&openpage($title, 1, '', 'shutdown');

	&openbigbox('100%', 'CENTER');
	print <<END
<div align='center'>
<table style="margin:2em; background-color:none;">

<tr>
	<td align='center'>
		<a href='/' border='0'><img src='/ui/img/smoothwall_big.png'></a><br /><br />
END
;
	&alertbox($errormessage, "", $infomessage);

	print <<END;
	</td>
</tr>
</table>
</div>
END
}

&closebigbox();
&closepage();
