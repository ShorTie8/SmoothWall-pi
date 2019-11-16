#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use IO::Socket;

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use update qw( :standard );
use smoothnet qw( :standard );
use smoothd qw(message);
use Time::HiRes "usleep";
use Data::Dumper;
use strict;
use warnings;

&showhttpheaders();

my (%uploadsettings, %updates);

$uploadsettings{'ACTION'} = '';
our $infomessage = '';
our $errormessage = '';

&getcgihash(\%uploadsettings);

my $extrahead = qq {
<script type="text/javascript">
function toggle( what )
{
	var tog = document.getElementById( what );
	if ( tog.style.display && tog.style.display != 'inline' ) {
		tog.style.display = 'inline';
	}
	else {
		tog.style.display = 'none';
	}
}
</script>
};

&openpage($tr{'updates'}, 1, $extrahead, 'maintenance');

&openbigbox('100%', 'LEFT');

if ($uploadsettings{'ACTION'} eq $tr{'upload'}) {
	my @list;
	my $return = &downloadlist();
	if ($return =~ m/^200 OK/) {
		unless (open(LIST, ">${swroot}/patches/available")) {
			$errormessage .= $tr{'could not open available updates file'} ."<br />";
			goto ERROR;
		}
		flock LIST, 2;
		my @this = split(/----START LIST----\n/,$return);
		print LIST $this[1];
		close(LIST);
		@list = split(/\n/,$this[1]);
	} 
	else {
		unless(open(LIST, "${swroot}/patches/available")) {
			$errormessage .= $tr{'could not open available updates list'} ."<br />";
			goto ERROR;
		}
		@list = <LIST>;
		close(LIST);
		$errormessage .= $tr{'could not download the available updates list'} ."<br />";
	}
	unless (mkdir("/var/patches/$$",0700)) {
		$errormessage .= $tr{'could not create directory'} ." /var/patches/$$.<br />";
		goto ERROR;
	}
	unless (open(FH, ">/var/patches/$$/patch.tar.gz")) {
		$errormessage .= $tr{'could not open update for writing'} ."<br />";
		goto ERROR;
	}
	flock FH, 2;
	print FH $uploadsettings{'FH'};
	close(FH);

	my $md5sum;
	chomp($md5sum = `/usr/bin/md5sum /var/patches/$$/patch.tar.gz`);
	my $found = 0;
	my ($id,$md5,$title,$description,$date,$url);
	foreach (@list) {
		chomp();
		($id,$md5,$title,$description,$date,$url) = split(/\|/,$_);
		if ($md5sum =~ m/^$md5\s/) {
			$found = 1;
			last;
		}
	}
	unless ($found == 1) {
		$errormessage .= $tr{'this is not an authorised update'} ."<br />";
		goto ERROR;
	}
	unless (system("cd /var/patches/$$ && /usr/bin/tar xvfz patch.tar.gz > /dev/null") == 0) {
		$errormessage .= $tr{'this is not a valid archive'} ."<br />";
		goto ERROR;
	}
	unless (open(INFO, "/var/patches/$$/information")) {
		$errormessage .= $tr{'could not open update information file' ."<br />"};
		goto ERROR;
	}
	my $info = <INFO>;
	close(INFO);

	open(INS, "${swroot}/patches/installed") or $errormessage .= $tr{'could not open installed updates file'} ."<br />";
	while (<INS>) {
		my @temp = split(/\|/,$_);
		if($info =~ m/^$temp[0]/) {
			$errormessage .= $tr{'this update is already installed'} ."<br />";
			goto ERROR;
		}
	}
	chdir("/var/patches/$$");
	print STDERR "Going for installation attempt\n";

	if (system( '/usr/bin/setuids/installpackage', $$)) {
		$errormessage .= $tr{'package failed to install'} ."<br />";
		goto ERROR;
	}
	unless (open(IS, ">>${swroot}/patches/installed")) {
 		$errormessage .= $tr{'update installed but'} ."<br />";
	}
	flock IS, 2;
	my @time = gmtime();
	chomp($info);

	$time[4] = $time[4] + 1;
	$time[5] = $time[5] + 1900;
	$time[3] = "0$time[3]" if ($time[3] < 10);
	$time[4] = "0$time[4]" if ($time[4] < 10);

	print IS "$info|$time[5]-$time[4]-$time[3]\n";
	close(IS);
	&log("$tr{'the following update was successfully installedc'} $title"); 
}
elsif ($uploadsettings{'ACTION'} eq $tr{'refresh update list'}) {
	my $return = &downloadlist();
	if ($return =~ m/^200 OK/) {
		unless(open(LIST, ">${swroot}/patches/available")) {
			$errormessage .= $tr{'could not open available updates file'} ."<br />";
			goto ERROR;
		}
		flock LIST, 2;
		my @this = split(/----START LIST----\n/,$return);
		print LIST $this[1];
		close(LIST);
		
		&log($tr{'successfully refreshed updates list'});
	} 
	else {
		$errormessage .= $tr{'could not download the available updates list'} ."<br />";
	}
}

ERROR:

if (open(AV, "${swroot}/patches/available")) {
	while (<AV>) {
		next if $_ =~ m/^#/;
		chomp $_;
		my @temp = split(/\|/,$_);
		my ($summary) = ( $temp[3] =~ /^(.{0,80})/ );
		$updates{ $temp[ 0 ] } = { name => $temp[2], summary => $summary, description => $temp[3], date => $temp[4], info => $temp[5], size => $temp[6], md5 => $temp[1] };
	}
	close (AV);
}
else {
	$errormessage .= $tr{'could not open the available updates file'} ."<br />";
}

if (open (PF, "${swroot}/patches/installed")) {
	while (<PF>) {
		my @temp = split(/\|/,$_);
		$updates{$temp[0]}{'installed'} = "---";
	}
	close (PF);
}
else {
	$errormessage .= $tr{'could not open the installed updates file'} ."<br />";
}

&alertbox($errormessage, "", $infomessage);

# Display options for adding / installing etc updates

&openbox();

my $available_count = 0;
foreach my $update ( sort keys %updates ) {
	next if ( defined $updates{$update}{'installed'} );
	$available_count ++;
}

my $height = 250;

print <<END
<br/>
<div style='height: ${height}px; overflow: auto;'>
<table class='blank' style='margin:0 0 0 1em; width:95%'>
END
;

foreach my $update ( sort keys %updates ) {
	next if ( defined $updates{$update}{'installed'} );
	print <<END
<tr>
	<td style='width: 15%;' ><a href='$updates{$update}{'info'}' onclick='window.open(this.href); return false'>$updates{$update}{'name'}</a></td>
	<td onClick="toggle('update-$update');" class='expand' title='Click to expand/hide'>$updates{$update}{'summary'}...</td>
	<td style='width: 10%; text-align:right'>$updates{$update}{'date'}</td>
</tr>
<tr>
	<td colspan='3' style='padding-left:2em'>
	<table class='expand' id='update-$update' style='display:none'>
	<tr>
		<td>$updates{$update}{'description'}</td>
	</tr>	
	</table></td>
</tr>
END
;
}

print <<END
<tr>
	<td></td>
</tr>
</table>
END
;

my $installed_count = 0;
foreach my $update ( sort keys %updates ) {
	next if ( not defined $updates{$update}{'installed'} );
	$installed_count ++;
}

if ( $installed_count > 0 ) {
	print <<END
		<p style='margin:0 0 0 1em'><strong>$tr{'installed updates'}</strong></p>
		<p style='margin:.5em 0 0 0; color: #808080; text-align:center'>
			The following updates have already been applied to your Smoothwall Express system.</p>
END
;
}

print <<END
<table class='blank' style='margin:0 0 0 1.5em; width:95%'>
END
;

foreach my $update ( sort keys %updates ) {
	next if ( not defined $updates{$update}{'installed'} );
	$updates{$update}{'name'} = "update?-???" if ($updates{$update}{'name'} eq "");
	$updates{$update}{'summary'} = "Update summary not found; the patch list wasn't retrieved or you are testing." if ($updates{$update}{'summary'} eq "");
	$updates{$update}{'description'} = "Update description not found." if ($updates{$update}{'description'} eq "");
	print <<END
<tr>
	<td style='width: 15%;' ><a style='color: #808080;' href='$updates{$update}{'info'}' onclick='window.open(this.href); return false'>$updates{$update}{'name'}</a></td>
	<td onClick="toggle('update-$update');" class='expand' style='color: #8080ff;' title='Click to expand/hide'>$updates{$update}{'summary'}...</td>
	<td style='width: 10%; text-align: right; color:#808080' >$updates{$update}{'date'}</td>
</tr>
<tr>
	<td colspan='3' style='padding-left:2em'>
		<table class='expand' id='update-$update' style='display:none'>
		<tr>
			<td style='color: #808080;' >$updates{$update}{'description'}</td>
		</tr>	
		</table>
		<!-- <script type="text/javascript">toggle('update-$update');</script> --></td>
</tr>
END
;
}

print <<END
<tr>
	<td></td>
</tr>
</table>
</div>
END
;

&closebox();
&openbox();

print <<END
<table class='blank'>
<tr>
	<td id='progressbar'>
		<table class='progressbar' style='width: 380px;'>
		<tr>
			<td id='progress' class='progressbar' style='width: 1px;'>&nbsp;</td>
			<td class='progressend'>&nbsp;</td>
		</tr>
		</table>
		<span id='status'></span></td>
	<td>&nbsp;</td>
	
	<td style='width: 350px; text-align: right;'>
		<form action='/cgi-bin/updates.cgi' method='post'><div>
		<input type='submit' name='ACTION' value='$tr{'refresh update list'}'>
		<input type='submit' name='ACTION' value='$tr{'update'}'></div></form></td>
	<td style='text-align: right;' id='actionsection'></td>
</tr>
</table>
END
;

&closebox();

print <<END
	<div id='manualinstall'>
END
;

&openbox( $tr{'install new update'} );

print <<END
$tr{'to install an update'}
<form method='post' action='/cgi-bin/updates.cgi' enctype='multipart/form-data'>
	<table class='blank'>
	<tr>
		<td>$tr{'upload update file'}</td>
		<td><input type="file" name="FH"> <input type='submit' name='ACTION' value='$tr{'upload'}'></td>
	</tr>
	</table>
</form>
END
;

&closebox();

print <<END
</div>
<script type="text/javascript">
	var add = "<input type='button' value='Advanced >>' onClick=\\"toggle('manualinstall');\\">";
	document.getElementById('actionsection').innerHTML += add;
	toggle('manualinstall');
</script>
END
;

&closebigbox();


# update downloads etc need to be dealt with at the end of the page (otherwise
# we would find ourselves with a blank page that doesn't seem to be doing a 
# great deal.
# Since the updates are "running" in the background all we "need" to do is 
# periodically test for updates


# firstly, simulate the action of the "closepage()" function, but ommit
# the </html> tags

&closepage( "update" );

if ($uploadsettings{'ACTION'} eq "$tr{'update'}" ) {
	use lib "/usr/lib/smoothwall/";

	&progressReport ( "Performing Update" );

	# determine the list of updates we currently require.

	my %required;
	
	foreach my $update ( sort keys %updates ) {
		next if ( defined $updates{$update}->{'installed'} );
		$required{ $update } = $updates{$update};
	}

	# Get the # of updates to fetch
	my $updatesNeeded = scalar(keys %required);
	if ( $updatesNeeded == 0 ) {
		&progressReport ( "All updates installed" );
	}
	else {
		&progressReport ( "System requires ".$updatesNeeded." update(s)" );

		print <<END
<script type="text/javascript">
	document.getElementById('progress').style.width = '1px';
	document.getElementById('progress').style.background = '#a0a0ff';
</script>
END
;

		# the progress bar is 380pixels wide
		# hence we need the following bits of information.

		my $width_per_update = ( 380 / ($updatesNeeded) );
		my $complete = 0;

		sub update
		{
			my ( $percent ) = @_;
			my $distance = ( $complete * $width_per_update ) + int( int( $width_per_update / 100 ) * $percent );
			$distance = 1 if ( $distance <= 0 );

			print <<END
<script type="text/javascript">
	document.getElementById('progress').style.width = '${distance}px';
</script>
END
;
		}
	
		my $error;
		my $filename;
		my $req;

		# Fetch each update in turn
		foreach my $req ( sort keys %required ) {
			&progressReport ( "Download update #$req ($required{$req}{'name'})" );
			&usleep ( 250000 );

			my ( $down, $percent, $speed );
		
			my $uri = "http://downloads.smoothwall.org/updates/3.1/";
			$filename = "3.1-$required{$req}{'name'}.tar.gz";
			&progressReport ("updatename='$filename'");
	
			# Start the DL in the background, logging to /var/patches/pending/*.log
			&download( $uri, $filename );

			my $stop = 0;

			# Monitor the download.
			do { 
				# Get wget's progress
				( $down, $percent, $speed, $required{$req}{'file'} ) = &progress( $filename );
				$percent =~ s/\%//;

				my $distance = ( $complete * $width_per_update ) + int( ( $width_per_update / 100 ) * $percent );
				$distance = 1 if ( $distance <= 0 );

				print <<END
<script type="text/javascript">
	document.getElementById('progress').style.width = '${distance}px';
</script>
END
;
				print STDERR "$filename ${percent}% complete\n";

				if ( $percent eq "100" ) {
					$stop = 1;
				}
				elsif ( not defined $percent or $percent eq "" ) {
					&progressReport ( "Update #$req NOT fetched; wget probably aborted\n");
					&progressReport ( "Updates: could not download $filename; aborted. Only $complete of $updatesNeeded fetched" );
					goto CLOSEHTML;
				}
				else {
					$stop = 0;
				}
				&usleep ( 100000 ); 
			}
			while ( $stop == 0 );

			# Get wget's final progress
			( $down, $percent, $speed, $required{$req}->{'file'} ) = &progress( $filename );
			&progressReport ( "Update #$req fetched ($percent):\n    $required{$req}->{'md5'}\n    ($required{$req}->{'size'})\n$required{$req}->{'file'}\n" );

			# Bump completed count
			$complete++;
			my $comp = $width_per_update * $complete; 

			print <<END
<script type="text/javascript">
	document.getElementById('progress').style.width = '${comp}px';
</script>
END
;
		}

		&progressReport ( "$complete of $updatesNeeded fetched" );

		foreach $req ( sort keys %required ) {
			&progressReport ( "Installing update $req" );

			print STDERR Dumper $required{$req};
		 	my $worked = apply( $required{$req}->{'file'} );

			if ( not defined $worked ) {
				&progressReport ("$errormessage");
				$error = $errormessage;
				last;
			} 
		}

		if ($error) {
			&progressReport ("Update $req failed to install - update aborted.");

			print <<END
<script type="text/javascript">
	document.getElementById('progress').style.width = '1px';
	document.getElementById('progress').style.background = 'none';
</script>
END
;
		}
		else {
			&progressReport ("Updates installed.");

			print <<END
<script type="text/javascript">
	document.getElementById('progress').style.background = 'none';
	document.location = "/cgi-bin/updates.cgi";
</script>
END
;

		}		
	}

}

# Label used to short-circuit operation when not all needed updates are downloaded.
# This ensures that the HTML is properly 'closed'.
CLOSEHTML:

print <<END
</body>
</html>
END
;


sub apply
{
	my ( $f ) = @_;
	print STDERR "Applying Patch $f\n";
	
	unless (mkdir("/var/patches/$$",0700)) {
		$errormessage .= $tr{'could not create directory'} +"/var/patches/$$<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}

	unless (open(FH, ">/var/patches/$$/patch.tar.gz")) {
		$errormessage .= $tr{'could not open update for writing'} +"/var/patches/$$/patch.tar.gz<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}

	&progressReport ( "apply(): writing /var/patches/$$/patch.tar.gz" );
	
	if ( defined $f ) {
		use File::Copy;
		move( $f, "/var/patches/$$/patch.tar.gz" );
	}
	else {
		flock FH, 2;
		print FH $uploadsettings{'FH'};
		close(FH);
	}

	my $md5sum;
	chomp($md5sum = `/usr/bin/md5sum /var/patches/$$/patch.tar.gz`);
	if ($md5sum eq "d41d8cd98f00b204e9800998ecf8427e") {
		$errormessage .= "patch.tar.gz is empty?!? (MD5 sum = d41d8...8427e)<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}
	my $found = 0;
	my ($id,$md5,$title,$description,$date,$url);
	&progressReport ( "apply(): looking for md5" );

	unless(open(LIST, "${swroot}/patches/available")) {
		$errormessage .= $tr{'could not open available updates list'} ."<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}
	my @list = <LIST>;
	close(LIST);

	foreach (@list) {
		chomp();
		($id,$md5,$title,$description,$date,$url) = split(/\|/,$_);
		&progressReport ( "apply(): compare MD5 Sum of $f ($md5sum) against $title ($md5)" );

		if ($md5sum =~ m/^$md5\s/) {
			$found = 1;
			last;
		}
		&usleep ( 500000 );
	}
	unless ($found == 1) {
		$errormessage .= $tr{'this is not an authorised update'} +"; the md5sums do not match<br />";
		&progressReport ( "apply(): $md5 $errormessage" );
		tidy();
		return undef;
	}
	&progressReport ( "apply(): unpack patch tarball..." );

	unless (system("/usr/bin/tar", "xfz", "/var/patches/$$/patch.tar.gz", "-C", "/var/patches/$$") == 0) {
		$errormessage .= $tr{'this is not a valid archive'} ."<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}
	&progressReport ( "apply(): get information file..." );

	unless (open(INFO, "/var/patches/$$/information")) {
		$errormessage .= $tr{'could not open update information file'} ."<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}
	my $info = <INFO>;
	close(INFO);

	&progressReport ("apply(): already installed?");

	unless (open(INS, "${swroot}/patches/installed")) {
		$errormessage .= $tr{'could not open installed updates file'} ."<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}

	while (<INS>) {
		my @temp = split(/\|/,$_);
		if($info =~ m/^$temp[0]/) {
			$errormessage .= $tr{'this update is already installed'} ."<br />";
			&progressReport ( "apply() failed: $errormessage" );
			tidy();
			return undef;
		}
	}
	chdir("/var/patches/$$");
	close(INS);
	
	&progressReport ("apply(): run installpackage to install the update");

	if (system( '/usr/bin/setuids/installpackage', $$)) {
		$errormessage .= $tr{'smoothd failure'} ."<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}
	
	unless (open(IS, ">>${swroot}/patches/installed")) {
 		$errormessage .= $tr{'update installed but'} ."<br />";
		&progressReport ( "apply() failed: $errormessage" );
		tidy();
		return undef;
	}

	flock IS, 2;
	my @time = gmtime();
	chomp($info);
	$time[4] = $time[4] + 1;
	$time[5] = $time[5] + 1900;
	$time[3] = "0$time[3]" if ($time[3] < 10);
	$time[4] = "0$time[4]" if ($time[4] < 10);
	print IS "$info|$time[5]-$time[4]-$time[3]\n";

	close(IS);
	tidy();
	
	&progressReport ( "apply(): $title was installed" );
	&log("$tr{'the following update was successfully installedc'} $title"); 
}


sub tidy
{
	&progressReport ( "tidy(): tidying up" );

	opendir(CUSTOM, "/var/patches/$$/");
	my @files = readdir (CUSTOM);
	closedir(CUSTOM);

	foreach my $file (@files) {
		&progressReport ( "tidy(): unlinking $file" );
		next if ( $file =~ /^\..*/ );
		unlink "/var/patches/$$/$file";
	}
	&progressReport ( "tidy(): remove directory $$" );
	rmdir "/var/patches/$$";
}


sub progressReport
{
	my ($statusStr) = @_;
	print <<END
<script type="text/javascript">
	document.getElementById('status').innerHTML = "$statusStr";
</script>
END
;
	print STDERR "$statusStr\n";
	&usleep ( 250000 );
}
