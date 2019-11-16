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
use App::Control;
use strict;
use warnings;

my (%p3scansettings, %clamavsettings, %checked);

my $refresh = '';
my $errormessage = '';
my $infomessage = '';
my $success = '';

&showhttpheaders();

$p3scansettings{'ACTION'} = '';

$p3scansettings{"ENABLE"} = '';

&readhash("${swroot}/clamav/settings", \%clamavsettings);

&getcgihash(\%p3scansettings);

if ($p3scansettings{'ACTION'} eq $tr{'clam update'}) { 
	$success = message('clamavfreshclam');
	$success = $tr{'clam still updating'} if ($success =~ /TIMEOUT/i);
	$infomessage .= $success."<br />" if ($success);
	$errormessage .= "$tr{'clam update failed'}<br />" unless ($success);
}

if ($p3scansettings{'ACTION'} eq $tr{'save'}) { 

	$clamavsettings{'ENABLE_ZAP'} = $p3scansettings{'ENABLE'};

	&writehash("${swroot}/clamav/settings", \%clamavsettings);
	&writehash("${swroot}/p3scan/settings", \%p3scansettings);
	system('/usr/bin/smoothwall/writep3scan.pl');

	if ($p3scansettings{"ENABLE"} eq 'on') {
		$success = message('p3scanrestart');
		$infomessage .= $success."<br />" if ($success);
		$errormessage .= "p3scanrestart ".$tr{'smoothd failure'}."<br />" unless ($success);

		# Check if ClamAV is already running
		my $avstatus = isclamrunning("clamd");
		if ($avstatus eq 'running') {
			# ClamAV is running - Don't restart it - It takes ages.
			$infomessage .= "$tr{'clam already running'}<br />";
		}
		else {
			$success = message('clamavrestart');
			print STDERR "ClamAV Restart: '$success'\n";
			$success = $tr{'clam still restarting'} if ($success =~ /TIMEOUT/i);
			$infomessage .= $success."<br />" if ($success and $success !~ "[Ff]ailed" );
			$errormessage .= "clamavrestart ".$tr{'smoothd failure'}." <i>$success<i><br />" unless ($success and $success !~ "[Ff]ailed" );
		}
		#$refresh = "<meta http-equiv='refresh' content='2;'>" unless ($errormessage =~ /fail/i || $errormessage =~ /$tr{'smoothd failure'}/);
	}
	else {
		$success = message('p3scanstop');
		$infomessage .= $success."<br />" if ($success);
		$errormessage .= "p3scanstop ".$tr{'smoothd failure'}."<br />" unless ($success);

		# Check if anything else has ClamAV turned on, if not - turn it off.
		open (CLAM, "${swroot}/clamav/settings") || die "Unable to open $!"; 
		my @clamsettings = (<CLAM>); 
		close (CLAM);
		my $clamused = grep { /\=on$/ } @clamsettings;

		if ($clamused == 0) {
			$success = message('clamavstop');
			$infomessage .= $success."<br />" if ($success);
			$errormessage .= "clamavstop ".$tr{'smoothd failure'}."<br />" unless ($success);
		}
		else {
			$errormessage .= "$tr{'clam in use'}<br />";
		}
		#$refresh = "<meta http-equiv='refresh' content='2;'>" unless ($errormessage =~ /fail/i || $errormessage =~ /$tr{'smoothd failure'}/);
	}
}

&readhash("${swroot}/p3scan/settings", \%p3scansettings);

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$p3scansettings{'ENABLE'}} = 'CHECKED';

&openpage('POP3 proxy configuration', 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

print STDERR  "emsg=$errormessage; imsg=$infomessage\n";
&alertbox($errormessage, "", $infomessage);

print "<form method='post' action='?'><div>\n";

&openbox('POP3 proxy:');
print <<END;
<table style='width:100%;'>
<tr>
	<td style='width:25%;' class='base'>$tr{'enabledc'}</td>
	<td style='width:30%;'><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td style='width:45%;'>
		<p style="margin:0"><b>$tr{'clam db file dates'}</b></p>
		<div style='margin:0 0 0 2em;'>
			<code>
END

system("cd /var/clamav; /bin/ls -lstr *.c*d | sed -e 's/.*clam clam *[0-9]* //' -e 's=\$=<br />='");

print <<END;
			</code>
		</div>
        </td>
</tr>
</table>
END

&closebox();

print <<END
<table style='width: 80%; border: none; margin-left:auto; margin-right:auto'>
<tr>
        <td style='width:45%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
        <td style='width:55%; text-align:center;'><input type='submit' name='ACTION' value='$tr{'clam update'}'></td>
</tr>
</table>
END
;

print "</div></form>\n";

&alertbox('add', 'add');

&closebigbox();

&closepage();

sub isclamrunning {
	my $cmd = $_[0];
	my $pid = '';
	my $testcmd = '';
	my $exename;

	$cmd =~ /(^[a-z]+)/;
	$exename = $1;
	my $status = "stopped";

	if (open(FILE, "/var/run/${cmd}.pid")) {
		$pid = <FILE>;
		chomp ($pid) if ($pid);
		close FILE;

		if ($pid) {
			if (open(FILE, "/proc/${pid}/status")) {
				while (<FILE>) {
					$testcmd = $1 if (/^Name:\W+(.*)/);
				}
				close FILE;
				$status = "running" if ($testcmd =~ /$exename/);
			}
		}
	}
	else {
		$pid = `ps -C $cmd -o pid=`;
		chomp ($pid) if ($pid);
		$status = "running" if ($pid);
	}
	return ( $status );
}
