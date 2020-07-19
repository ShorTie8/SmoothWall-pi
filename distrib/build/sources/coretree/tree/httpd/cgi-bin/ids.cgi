#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

sub localdebug
{
	$label = $_[0];
	local (*settings) = @_[1];
	print "<br><b>$label</b><br>\n";
	print "&nbsp;&nbsp;&nbsp;&nbsp;<b><i>ENV</i></b><br>\n";
	foreach $key (sort keys %ENV) {
		print "$key=>$ENV{$key}<br>\n";
	}
	print "<br>\n";
	print "&nbsp;&nbsp;&nbsp;&nbsp;<b><i>snortsettings</i></b><br>\n";
	foreach $key (sort keys %settings) {
		print "$key=>$settings{$key}<br>\n";
	}
	print "<br>\n";
	print "&nbsp;&nbsp;&nbsp;&nbsp;<b><i>others</i></b><br>\n";
	print "formDOWNLOAD=>$formdownload<br>\n";
	print "formdebug=>$formdebug<br>\n";
	print "formoink=>$formoink<br>\n";
}

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );
use Cwd;
use strict;
use warnings;

my (%snortsettings, %snortoldsettings, $snortversion, %checked);
my $maxwidth = 20;	# em (EM - width of an M in the current font)

&showhttpheaders();

$snortsettings{'ENABLE_SNORT'} = 'off';
$snortsettings{'DOWNLOAD'} = 'off';
$snortsettings{'ACTION'} = '';
$snortsettings{'OINK'} = '';

my $errormessage = '';
my $infomessage = '';
my $refresh = '';
my $success = '';

&getcgihash(\%snortsettings);

my ($oink_display, $oink_display_not, $idslastdownload, $ids_status, $idslastDLdays);
my $formdownload = $snortsettings{'DOWNLOAD'} || '';
my $formdebug = $snortsettings{'DEBUG'} || '';
my $formoink = $snortsettings{'OINK'} || '';
my $days = 0;
my $enable_disabled = '';

delete $snortsettings{'DOWNLOAD'};
delete $snortsettings{'DEBUG'};
&readhash("${swroot}/snort/settings", \%snortoldsettings);

#&localdebug("initial", \%snortsettings);

############################
# Early actions
#
# Verify OINK code length and content
if ($snortsettings{'ACTION'} eq $tr{'save'} and 
    $formdownload eq 'on' and 
    $errormessage eq '') {
	if ($formoink !~ /^([\da-f]){40}$/i) {
		$errormessage .= $tr{'oink code must be 40 hex digits'} ."<br />";
	}
	else {
		$snortsettings{'OINK'} = $formoink;
		&writehash("${swroot}/snort/settings", \%snortsettings);
		# &localdebug("saveoink", \%snortsettings);
	}
}

# Turn on or off, but only if the option changed and not downloading.
if ($snortsettings{'ACTION'} eq $tr{'save'} and
    $formdownload ne "on" and
    $snortoldsettings{'ENABLE_SNORT'} ne $snortsettings{'ENABLE_SNORT'}) {

	&writehash("${swroot}/snort/settings", \%snortsettings);

	if ($snortsettings{'ENABLE_SNORT'} eq 'on') {
		&log($tr{'snort is enabled'});
		$success = &message('snortrestart');
		$success = "TIMEOUT: Snort Still Restarting" if ($success =~ /TIMEOUT/i);
	}
	else {
		&log($tr{'snort is disabled'});
		$success = &message('snortstop');
	}
	$infomessage .= $success."<br />" if ($success);
	$errormessage .= "snort ".$tr{'smoothd failure'} ."<br />" unless ($success);
}

# If download is checked, uncheck and make oink text
if ($formdownload eq 'on') {
	$checked{'DOWNLOAD'}{'off'} = '';
	$checked{'DOWNLOAD'}{'on'} = '';
	$oink_display = "none";
	$oink_display_not = "inline-block";
}
else {
	# Download is not checked, so pre-check it or not, but
	# display OINK properly
	$checked{'DOWNLOAD'}{'off'} = '';
	$checked{'DOWNLOAD'}{'on'} = '';
	if (($days==-1 || $days > 30) and ($idslastDLdays > 5)) {
		$checked{'DOWNLOAD'}{'on'} = 'checked';
		$oink_display = "inline-block";
		$oink_display_not = "none";
	}
	else {
		$oink_display = "none";
		$oink_display_not = "inline-block";
	}
}

############################
# Preparations
&readhash("${swroot}/snort/settings", \%snortsettings);

# Extract on or off
$checked{'ENABLE_SNORT'}{'off'} = '';
$checked{'ENABLE_SNORT'}{'on'} = '';
$checked{'ENABLE_SNORT'}{$snortsettings{'ENABLE_SNORT'}} = 'CHECKED';

# Extract days since last DL
my $mylastdownload = 'N/A';
if (-e "${swroot}/snort/DL-age") {
	$idslastDLdays = int(-M "${swroot}/snort/DL-age");
	if ($idslastDLdays == 1) {
		$idslastdownload = "$idslastDLdays $tr{'ids day ago'}";
	}
	else {
		$idslastdownload = "$idslastDLdays $tr{'ids days ago'}";
	}
	$enable_disabled = "";
}
else {
	$idslastdownload = "($tr{'ids never downloaded'})";
	$enable_disabled = " disabled='disabled'";
}

# status at page rendering
if ($snortsettings{'ENABLE_SNORT'} eq 'on') {
	$ids_status = $tr{'ids enabled'};
}
else {
	$ids_status = $tr{'ids disabled'};
}

############################
# Start page rendering
&openpage($tr{'intrusion detection system'}, 1, $refresh, 'services');

&openbigbox('100%', 'left');

&alertbox($errormessage, "", $infomessage);

print "<form method='post' action='?'><div>\n";

my $snortTitle = $tr{'intrusion detection system2'};
my $snortVersion = `snort --version 2>&1 | grep Version`;
chomp $snortVersion;
$snortVersion =~ s/^.*Version //;
$snortVersion =~ s/ .*$//;
$snortTitle =~ s/Snort/Snort v$snortVersion/;
&openbox($snortTitle.' <i>('.$ids_status.')</i>');

print "
<div style='margin:12pt 0 0 0'>
	<div class='base' style='text-align:right; margin-right:.2em; display:inline-block; width:20%; '>$tr{'ids enable'}</div>
	<div style='margin-right:.2em; display:inline-block; width:20%; '>
		<input id='ENABLE_SNORT' type='checkbox' name='ENABLE_SNORT' style='margin:0'
		${enable_disabled}$checked{'ENABLE_SNORT'}{'on'}></div>
	<div class='base' style='text-align:right; margin-right:.2em; display:inline-block; width:20%; '>&nbsp;</div>
	<div style='margin-right:.2em; display:inline-block; width:20%; '>&nbsp;</div>
	<br />
	<div class='base' style='text-align:right; margin-right:.2em; display:inline-block; width:20%;'>
		$tr{'ids download label'}</div>
	<div style='margin-right:.2em; display:inline-block; width:20%; '>
		<input id='dlCheckBox' type='checkbox' name='DOWNLOAD'
		onchange='if (getElementById(\"dlCheckBox\").checked) {
			getElementById(\"OINK-input\").style.display=\"inline-block\";
			getElementById(\"OINK-text\").style.display=\"none\";
		}
		else {
			getElementById(\"OINK-input\").style.display=\"none\";
			getElementById(\"OINK-text\").style.display=\"inline-block\";
		}
		return true;'
		style='margin:0' $checked{'DOWNLOAD'}{'on'}>
		<span style='margin-left:18pt; margin-right:.5em'>$tr{'ids debug'}</span>
		<span><input type='checkbox' name='DEBUG' style='margin:0'></span></div>
	<div class='base' style='text-align:right; margin-right:.2em; display:inline-block; width:20%; '>
		$tr{'last download'}</div>
	<div style='margin-right:.2em; display:inline-block; width:20%; '><b>$idslastdownload</b></div>
	<div style='height:3em'>
		<div class='base' style='text-align:right; margin-right:.2em; display:inline-block; width:20%'>
			$tr{'oink code'}</div>
		<div id='OINK-input' style='margin:0 .2em 0 0; display:$oink_display; width:50%'>
			<input type='text' name='OINK' size='45' maxlength='40' value='$snortsettings{'OINK'}'
			id='OINK' @{[jsvalidregex('OINK','^([0-9a-fA-F]){40}$')]}></div>
		<div id='OINK-text' style='margin:0 .2em 0 0; display:$oink_display_not; width:50%'>
			<span>$snortsettings{'OINK'}</span></div>
	</div>
</div>
";

&closebox();

print "
<div style='width:100%; text-align:center; vertical-align:middle'>
	<input type='submit' name='ACTION' value='$tr{'save'}'>
</div>
";


&openbox($tr{'rule retreval'});

print "
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base' style='width:20%;'>$tr{'ids download progress'}</td>
	<td>	<div style='width:${maxwidth}em; height:100%; border:lightgrey 1px solid'>
		<div id='progress' class='progressbar'
		style='width:0; height:100%; background-color:#000090'>&nbsp;</div>
		</div></td>
	<td class='progressend'>&nbsp;</td>
</tr>
<tr>
	<td class='base' style='width:20%;'>$tr{'ids download status'}</td>
	<td><span id='status'></span></td>
</tr>
<tr id='log-row' style='display:none;'>
	<td class='base' style='width:20%;'>$tr{'ids download log'}</td>
	<td><div id='log' style='height:250px; max-height:250px; min-height:250px; padding:2pt;
                          overflow:auto; border:lightgrey 1px solid;'></div></td>
</tr>
</table>
";

&closebox();

print "</div></form>\n";

&closebigbox();

# close except </body> and </html>
&closepage( "update" );

if (($snortsettings{'ACTION'} eq $tr{'save'}) &&
    ($formdownload eq 'on') && !$errormessage) {
	# start snort version query; borrowed from GAR's update-rules.pl
	open SNORT, "/usr/bin/snort -V 2>&1 |" or die "Couldn't open snort: $! \n";
	my ($display_version, $sub1, $sub2, $sub3, $sub4);
	while (my $line = <SNORT>) {
		chomp($line);
		if ($line =~ /Version\s+(.*)/) {
			($display_version, $sub1, $sub2, $sub3, $sub4) = split(/ /, $1);
			my @versionParts = split(/\./, $display_version);
			# If any parts are not defined, make them zero.
			# Start at the end to avoid unneeded work.
			for (my $i=3; $i>=0; $i--) {
				last if (defined($versionParts[$i]));
				$versionParts[$i] = "0";
			}
			$snortversion = join(".", @versionParts);
			last;
		}
	}
	close SNORT or die "Couldn't close snort command: $! \n";

	# Try to fetch the ruleset
	my $snortver_nodots = $snortversion;
	$snortver_nodots =~ s/\.//g;
	print "
<script language='javascript' type='text/javascript'>
  document.getElementById('log-row').style.display = 'table-row';
</script>
";
	&runoinkmaster($snortver_nodots);
	my $runmsg .= $errormessage if ($errormessage ne "");

	# Display DL errors encountered
	if (($runmsg) && ($runmsg ne "")) {
		$errormessage .= $runmsg;
		$errormessage .= "Could not fetch the $snortversion ruleset.<br />";
		print STDERR $errormessage;
	}

	if ($snortsettings{'ENABLE_SNORT'} eq 'on' and !$errormessage) {  
		my $success = &message('snortrestart');
		$errormessage .= $tr{'smoothd failure'} ."<br />" unless ($success);
	}

	if ($errormessage) {
		print "
<script language='javascript' type='text/javascript'>
document.getElementById('status').innerHTML = '$errormessage';
document.getElementById('log').innerHTML += '$errormessage';
</script>
";
	}
	else {
		print "
<script language='javascript' type='text/javascript'>
  document.getElementById('status').innerHTML = 'Installation complete (ruleset v$snortversion)';
  document.getElementById('progress').style.width = '${maxwidth}em';
  document.getElementById('ENABLE_SNORT').disabled = '';
  //document.location = '/cgi-bin/ids.cgi';
</script>
";
	}

}

print "
</body>
</html>
";

sub runoinkmaster
{
	my $v = $_[0];
	my $attempt = $_[1] if (defined $_[1]);
	my $url = "http://www.snort.org/reg-rules/snortrules-snapshot-$v.tar.gz/" . $snortsettings{'OINK'};
	#my $url = "http://downloads/snortrules-snapshot-$v.tar.gz/" . $snortsettings{'OINK'};

	my $curdir = getcwd;
	chdir "${swroot}/snort/";

	select STDOUT;
	$| = 1;

	my $pid = open(FD, '-|');
	if (!defined $pid) {
		$errormessage .= $tr{'unable to fetch rules'} ."<br />";
	}
	elsif ($pid) {
		$errormessage .= $tr{'rules not available'} ."<br />";

		print "
<script language='javascript' type='text/javascript'>
  document.getElementById('status').innerHTML = 'Starting';
  document.getElementById('progress').style.background = '#a0a0ff';
</script>
";
		my $percent = 0;
		while(<FD>) {
			my $line = $_;
			chomp ($line);
			$line =~ s/'/\\'/g;
			if ($formdebug ne "") {
				print "
<script language='javascript' type='text/javascript'>
  document.getElementById('log').innerHTML += '${line}<br />\\n';
</script>
";
			}
			$errormessage = '';
			if ($percent < 100 && $line =~ / (\d{1,3})%/) {
				$percent = $1;
				my $message;
				if ($percent == 100) {
					print "
<script language='javascript' type='text/javascript'>
  document.getElementById('status').innerHTML = 'Unpacking, please wait';
  document.getElementById('progress').style.width = '${maxwidth}em';
</script>
";
				}
				else {
					# $message = "Download $percent% complete";
					my $curwidth = $maxwidth * $percent/100;
					print "
<script language='javascript' type='text/javascript'>
  document.getElementById('progress').style.width = '${curwidth}em';
</script>
";
				}
			}
			elsif (/.*successfully downloaded.*/) {
				print "
<script language='javascript' type='text/javascript'>
  document.getElementById('status').innerHTML = 'Rules unpacked';
</script>
";
			}
			elsif (/.*successfully downloaded.*|.*Processing.*/) {
				print "
<script language='javascript' type='text/javascript'>
  document.getElementById('status').innerHTML = 'Processing rules';
</script>
";
			}
			elsif (/.*302 Found.*|.*200 OK.*/) {
print "
  <script language='javascript' type='text/javascript'>
    document.getElementById('status').innerHTML = 'Downloading';
  </script>
";
			}
			elsif (/.*403 Forbidden.*/) {
				$errormessage .= "You can't download now. Try again later.<br />";
				print "
  <script language='javascript' type='text/javascript'>
    document.getElementById('status').innerHTML = 'You can\\'t download now; try later.';
  </script>
";
			}
			elsif (/.*404 Not Found.*/) {
				$errormessage .= "Rules version $v not found. Try again another day.<br />";
				print "
  <script language='javascript' type='text/javascript'>
    document.getElementById('status').innerHTML = 'Rules $v not found; Try again another day.';
  </script>
";
			}
		}
		close(FD);

		if ($?) {
			$errormessage .= $tr{'unable to fetch rules'} ."<br />";
		}
		else {
			unlink (">${swroot}/snort/DL-age");
			open (FILE, ">${swroot}/snort/DL-age");
			close (FILE);
			#open (FILE, ">${swroot}/snort/ruleage");
			#close (FILE);
		}
	}
	else {
		# so we see wget's output
		close(STDERR);
		open(STDERR, ">&STDOUT");

		# exec("wget", "-O", "/tmp/a.tgz", "$url");
		exec('/usr/bin/oinkmaster.pl', '-v', '-C', '/usr/lib/smoothwall/oinkmaster.conf', '-o', 'rules', '-u', $url);
	}
	chdir $curdir;
}
