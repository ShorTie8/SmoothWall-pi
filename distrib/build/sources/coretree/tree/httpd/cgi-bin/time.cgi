#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) SmoothWall Ltd 2002, 2003

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );
use strict;
use warnings;

my @shortmonths = ( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
	'Sep', 'Oct', 'Nov', 'Dec' );

my (%cgitimesettings, %timesettings, %netsettings, %timeservers, %checked, %selected);
my $found;
my @temp;
my $temp;
my $errormessage = '';
my $infomessage = '';
my $refresh = '';

my $tzroot = '/usr/share/zoneinfo/posix';
open(FILE, "${swroot}/time/timezones");
my @timezones = <FILE>;
close(FILE);

&showhttpheaders();

$cgitimesettings{'ACTION'} = '';
$cgitimesettings{'VALID'} = '';
$cgitimesettings{'ENABLED'} = '';

$timesettings{'TIMEZONE'} = '';
$timesettings{'ENABLED'} = 'off';
$timesettings{'NTP_RTC'} = 'off';
$timesettings{'NTPD'} = 'off';

# Get stored and submitted settings
&getcgihash(\%cgitimesettings);
$cgitimesettings{'ENABLED'} = 'off' if ($cgitimesettings{'ENABLED'} eq "");
&readhash("${swroot}/time/settings", \%timesettings);
&readhash("${swroot}/ethernet/settings", \%netsettings);

if ($cgitimesettings{'ACTION'} eq $tr{'save'}) {
	my ($method, $year, $month, $day, $hour, $minute, $second);
	$method = $cgitimesettings{'NTP_METHOD'};
	$year = $cgitimesettings{'YEAR'};
	$month = $cgitimesettings{'MONTH'};
	$day = $cgitimesettings{'DAY'};
	$hour = $cgitimesettings{'HOUR'};
	$minute = $cgitimesettings{'MINUTE'};
	$second = $cgitimesettings{'SECOND'};

	my ($manual, $periodic, $automatic);
	$manual = $tr{'time method manual'};
	$periodic = $tr{'time method periodic'};
	$automatic = $tr{'time method automatic'};

#print STDERR "method:$method year:$year month:$month day:$day hour:$hour minute:$minute second:$second\n";

	# Validate date/time values
	unless ( ($method eq $manual and ($year =~ /\d+/ and $year >= 1970 and $year <= 2037)) or
	         ($method ne $manual and (($year eq "") or 
		  ($year =~ /\d+/ and $year >= 1970 and $year <= 2037)))) {
		$errormessage .= $tr{'time invalid year'} ."<br />";
	}
	unless ( ($method eq $manual and ($month =~ /\d+/ and $month >= 1 and $month <= 12)) or
	         ($method ne $manual and (($month eq "") or 
		  ($month =~ /\d+/ and $month >= 1 and $month <= 12)))) {
		$errormessage .= $tr{'time invalid month'} ."<br />";
	}
	unless ( ($method eq $manual and ($day =~ /\d+/ and $day >= 1 and $day <= 32)) or
	         ($method ne $manual and (($day eq "") or ($day =~ /\d+/ and $day >= 1 and $day <= 32)))) {
		$errormessage .= $tr{'time invalid day'} ."<br />";
	}
	unless ( ($method eq $manual and ($hour =~ /\d+/ and $hour >= 0 and $hour <= 23)) or
	         ($method ne $manual and (($hour eq "") or ($hour =~ /\d+/ and $hour >= 0 and $hour <= 23)))) {
		$errormessage .= $tr{'time invalid hour'} ."<br />";
	}
	unless ( ($method eq $manual and ($minute =~ /\d+/ and $minute >= 0 and $minute <= 59)) or
	         ($method ne $manual and (($minute eq "") or 
		  ($minute =~ /\d+/ and $minute >= 0 and $minute <= 59)))) {
		$errormessage .= $tr{'time invalid minute'} ."<br />";
	}
	unless ( ($method eq $manual and ($second =~ /\d+/ and $second >= 0 and $second <= 59)) or
	         ($method ne $manual and (($second eq "") or 
		  ($second =~ /\d+/ and $second >= 0 and $second <= 59)))) {
		$errormessage .= $tr{'time invalid second'} ."<br />";
	}

	# Validate method, interval, and zone
	unless ($cgitimesettings{'NTP_METHOD'} =~ /^($manual|$periodic|$automatic)$/) {
		$errormessage .= $tr{'time invalid method'} ."<br />";
	}
	unless ($cgitimesettings{'NTP_INTERVAL'} =~ /^(1|2|3|6|12|24|48|72)$/) {
		$errormessage .= $tr{'time invalid interval'} ."<br />";
	}

	$found = 0;
	foreach (@timezones) {
		chomp;
		if ($_ eq $cgitimesettings{'TIMEZONE'}) {
			$found = 1;
			last;
		}
	}
	if ($found == 0) {
		$errormessage .= $tr{'time invalid zone'} ."<br />";
	}

	# Validate server
        if (($cgitimesettings{'NTP_SERVER'} ne "") and
           (!(validip($cgitimesettings{'NTP_SERVER'}) or validhostname($cgitimesettings{'NTP_SERVER'})))) {
		$errormessage .= $tr{'time invalid server'} ."<br />";
	}	
	# End of validations

	# If there are errors, mark the data invalid. Otherwise mark them valid, store them,
	#   write the new ntpd.conf, and restart ntpd.
	if ($errormessage) {
		$cgitimesettings{'VALID'} = 'no';
	}
	else {
		my %tempsettings;

		$cgitimesettings{'VALID'} = 'yes';

		# Manual set works, enabled or not.
		if ($cgitimesettings{'NTP_METHOD'} eq 'Manual') {
			my ($year, $month, $day, $hour, $minute, $second);
			$year = $cgitimesettings{'YEAR'};
			$month = $cgitimesettings{'MONTH'};
			$day = $cgitimesettings{'DAY'};
			$hour = $cgitimesettings{'HOUR'};
			$minute = $cgitimesettings{'MINUTE'};
			$second = $cgitimesettings{'SECOND'};

			system('/usr/bin/smoothcom', 'settime', "$hour:$minute:$second $year/$month/$day");
			&log($tr{'setting time'});
		}

		# Write the savable settings; the smoothd plugin needs them.
		foreach $temp ('TIMEZONE', 'ENABLED', 'NTP_INTERVAL', 'NTP_METHOD', 'NTP_SERVER') {
			$tempsettings{$temp} = $cgitimesettings{$temp};
		}
		&writehash("${swroot}/time/settings", \%tempsettings);
		system('/usr/bin/smoothwall/writentpd.pl');

		# Time zone can change, enabled or not
		# Update time zone if it changed
		if ($cgitimesettings{'TIMEZONE'} ne $timesettings{'TIMEZONE'}) {
			unlink("${swroot}/time/localtime");
			system('/bin/ln', '-s', "${tzroot}/$cgitimesettings{'TIMEZONE'}", "${swroot}/time/localtime");

			# Update the kernel's time zone, H/W Clock, and DST cron task
			my $success = message('ntpdchgtimezone');
			$infomessage .= $success."<br />" if ($success);
			$errormessage .= "ntpdchgtimezone ".$tr{'smoothd failure'}."<br />" unless ($success);
		}

		# The smoothd plugin always stops, then checks 'enabled' before restarting.
		my $success = message('ntpdrestart');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= " ntpdrestart ".$tr{'smoothd failure'}."<br />" unless ($success);
	}

	# Merge in the form values because Save was clicked. If Save was not clicked,
	#   only the saved settings are used.
	%timesettings = (
		%timesettings,
		%cgitimesettings,
	);
}
# End of 'SAVE'

# Set defaults as needed
$timesettings{'TIMEZONE'} = 'Europe/London' if ($timesettings{'TIMEZONE'} eq "");
$timesettings{'ENABLED'} = 'off' if ($timesettings{'ENABLED'} eq "");
$timesettings{'NTP_INTERVAL'} = 6 if ($timesettings{'NTP_INTERVAL'} eq "");
$timesettings{'NTP_METHOD'} = $tr{'time method automatic'} if ($timesettings{'NTP_METHOD'} eq "");
$timesettings{'YEAR'} = '';
$timesettings{'MONTH'} = '';
$timesettings{'DAY'} = '';
$timesettings{'HOUR'} = '';
$timesettings{'MINUTE'} = '';
$timesettings{'SECOND'} = '';

$checked{'ENABLED'}{'on'} = '';
$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{$timesettings{'ENABLED'}} = 'CHECKED';

foreach (@timezones) {
	chomp;
	$selected{'TIMEZONE'}{$_} = '';
}
$selected{'TIMEZONE'}{$timesettings{'TIMEZONE'}} = 'SELECTED';

$selected{'NTP_INTERVAL'}{'1'} = '';
$selected{'NTP_INTERVAL'}{'2'} = '';
$selected{'NTP_INTERVAL'}{'3'} = '';
$selected{'NTP_INTERVAL'}{'6'} = '';
$selected{'NTP_INTERVAL'}{'12'} = '';
$selected{'NTP_INTERVAL'}{'24'} = '';
$selected{'NTP_INTERVAL'}{'48'} = '';
$selected{'NTP_INTERVAL'}{'72'} = '';
$selected{'NTP_INTERVAL'}{$timesettings{'NTP_INTERVAL'}} = 'SELECTED';

$selected{'NTP_METHOD'}{$tr{'time method manual'}} = '';
$selected{'NTP_METHOD'}{$tr{'time method periodic'}} = '';
$selected{'NTP_METHOD'}{$tr{'time method automatic'}} = '';
$selected{'NTP_METHOD'}{$timesettings{'NTP_METHOD'}} = 'CHECKED';

my @now = localtime(time);


# Now render
&openpage($tr{'time regulation title'}, 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='post' action='?'><div>\n";

&openbox($tr{'time timeboxc'});

print <<END
<table width='100%' style='margin:0 0 0 2em'>
<tr>
	<td style='width:10%;' class='base'>$tr{'enabledc'}</td>
	<td><input type='checkbox' name='ENABLED' $checked{'ENABLED'}{'on'}></td>
</tr>
<tr>
	<td style='width:10%;' class='base'>$tr{'timezonec'}</td>
	<td><select name='TIMEZONE'>
END
;

foreach (@timezones) {
	chomp;
	my $displayValue = $_;
	$displayValue =~ s/_/ /g;
	print "		<option value='$_' $selected{'TIMEZONE'}{$_}>$displayValue</option>\n";
}

print <<END
		</select></td>
</tr>
</table>
END
;

&closebox();

&openbox($tr{'time methodc'});

print <<END
<table width='100%' style='margin:0 0 0 2em'>
<tr>
	<td style='width:100%;'>
		<input type='radio' name='NTP_METHOD' value='$tr{'time method manual'}' $selected{'NTP_METHOD'}{$tr{'time method manual'}}>
		$tr{'time method manual'}</td>
</tr>
<tr>
	<td>
		<table width="100%">
		<tr>
			<td style='width:10%;' class='base'>$tr{'time datec'}</td>
			<td><input type="text" name="YEAR" value="$timesettings{'YEAR'}" size="4"> /
			    <input type="text" name="MONTH" value="$timesettings{'MONTH'}" size="2"> /
			    <input type="text" name="DAY" value="$timesettings{'DAY'}" size="2">
			    $tr{'time date ymd'}</td>
		</tr>
		<tr>
			<td style='width:10%;' class='base'>$tr{'time timec'}</td>
			<td><input type="text" name="HOUR" value="$timesettings{'HOUR'}" size="2"> :
			    <input type="text" name="MINUTE" value="$timesettings{'MINUTE'}" size="2"> :
			    <input type="text" name="SECOND" value="$timesettings{'SECOND'}" size="2">
			    $tr{'time time hms'}</td>
		</tr>
		</table>
	</td>
</tr>
<tr>
	<td>&nbsp;</td>
</tr>
<tr>
	<td style='width:100%;' title='$tr{'time periodic title'}'>
	    <input type='radio' name='NTP_METHOD' value='$tr{'time method periodic'}' $selected{'NTP_METHOD'}{$tr{'time method periodic'}}>
	    $tr{'time method periodic'}</td>
</tr>
<tr>
	<td style='width:100%;'>
		<table width="100%">
		<tr>
			<td style='width:10%;' class='base'>$tr{'time intervalc'}</td>
			<td>
END
;

my $timecount;
my $nextupdate;

open(FILE, "${swroot}/time/timecount");
$timecount = <FILE>; chomp $timecount;
close(FILE);

if (($timesettings{'NTP_INTERVAL'} - $timecount) > 1) {
	$nextupdate = $timesettings{'NTP_INTERVAL'} - $timecount . " $tr{'hours'}";
}
else {
	$nextupdate = $tr{'less than one hour'};
}

print <<END
			<select name='NTP_INTERVAL'>
				<option value='1' $selected{'NTP_INTERVAL'}{'1'}>$tr{'time one hour'}
				<option value='2' $selected{'NTP_INTERVAL'}{'2'}>$tr{'time two hours'}
				<option value='3' $selected{'NTP_INTERVAL'}{'3'}>$tr{'time three hours'}
				<option value='6' $selected{'NTP_INTERVAL'}{'6'}>$tr{'time six hours'}
				<option value='12' $selected{'NTP_INTERVAL'}{'12'}>$tr{'time twelve hours'}
				<option value='24' $selected{'NTP_INTERVAL'}{'24'}>$tr{'time one day'}
				<option value='48' $selected{'NTP_INTERVAL'}{'48'}>$tr{'time two days'}
				<option value='72' $selected{'NTP_INTERVAL'}{'72'}>$tr{'time three days'}
			</select></td>
		</tr>
		</table>
	</td>
</tr>
<tr>
	<td>&nbsp;</td>
</tr>
<tr>
	<td style='width:100%;' title='$tr{'time automatic title'}'>
	    <input type='radio' name='NTP_METHOD' value='$tr{'time method automatic'}' $selected{'NTP_METHOD'}{$tr{'time method automatic'}}>
	    $tr{'time method automatic'}</td>
</tr>
</table>
END
;

&closebox;


# Time server name or address
&openbox($tr{'time network serverc'});

print <<END
<table>
<tr>
	<td class='base'>$tr{'time ip or domainc'}</td>
	<td><input type='text' name='NTP_SERVER' size=60 value='$timesettings{'NTP_SERVER'}'></td>
</tr>
</table>
END
;

&closebox();

# Action button

print <<END
<table width='100%'>
<tr>
	<td style='text-align:center'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;


print "</div></form>\n";

&alertbox('add', 'add');

&closebigbox();

&closepage();
