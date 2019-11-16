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
use smoothtype qw(:standard);
use strict;
use warnings;

my (%cgiparams, %selected, %checked);
my ($lastToken, $newToken, $rtnToken);
my $filename = "${swroot}/backup/config";
my $flagfile = "${swroot}/backup/flag";
my $maxwidth = 20;
my $refresh;

$cgiparams{'ACTION'} = '';

$cgiparams{'ENABLED'} = 'off';
$cgiparams{'STATE'} = 'idle';
$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'} = $tr{'log ascending'};

&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && 
    ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" )) {
	my @temp = split(',',$ENV{'QUERY_STRING'});
	$cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
	$cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

my $infomessage = '';
my $errormessage = '';
my $extramessage = '';
my @service = ();

my @temp;
my $count; my $command;
my @selectedui; my @selectedsetup; my @selectedmodules;


# Generate a new token and the previous token on each entry.
my $tmp;
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
my $life = 30;  # seconds
my $toSum = $tmp . int($time/$life) ."\n";
$newToken = sha1_hex $toSum;
$toSum = $tmp . int($time/$life - 1) ."\n";
$lastToken = sha1_hex $toSum;

# Clear these, just in case
undef $time;
undef $toSum;
undef $tmp;

$rtnToken = $cgiparams{'Token'};

if ($cgiparams{'ACTION'} eq $tr{'bu restore'}) { 
	# Require token to prevent XSS.
	if ($rtnToken !~ /[0-9a-f]/ or ($rtnToken ne $newToken and $rtnToken ne $lastToken)) {
		$errormessage = "$tr{'token error 1'}<br /><br />$tr{'token error 2'}<br />";
		$refresh = '<meta http-equiv="refresh" content="6; url=index.cgi">';
		goto ERROR;
	}

	my $fileName = $cgiparams{'fileName'};
	$fileName =~ s/.*\\//;

	# Validate archive filename
	if (!&validarchivename($fileName)) {
		$errormessage .= "$tr{'invalid archive name'}<br />";
	}

	else {
		# Did the supplied filename match the template?
		if ($fileName =~ /[a-zA-Z0-9-]+_[0-9-]+_Express_[0-9.]+_[a-zA-Z]+_settings\.tar/) {
			# Open the destination file
			if (open(ARCHIVEFILE, ">$swroot/tmp/backup.tar")) {
				flock ARCHIVEFILE, 2;
				print ARCHIVEFILE $cgiparams{'ARCHIVE'};
				close(ARCHIVEFILE);
		
				my $fileType = `/usr/bin/file $swroot/tmp/backup.tar`;
		
				if ($fileType =~ /tar archive/) {
					system("tar xf $swroot/tmp/backup.tar -C $swroot/restore");
		
		        		if (-f "$swroot/restore/version" && -f "$swroot/restore/backup.dat") {
						# Do the restore
						my $success = message('restoresettings');
						$infomessage .= "$success<br />" if ($success);
						$errormessage .= "Could not restore settings.<br />" unless ($success);
					}
					else {
						$errormessage .= "$tr{'bu not settings archive'}</br />";
						print STDERR "$tr{'bu not settings archive'}\n";
					}
				}
				else {
					$errormessage .= "$tr{'bu not tar archive'} '$fileType'<br />";
					print STDERR "$tr{'bu not tar archive'} '$fileType'\n";
				}
			}
			else {
				$errormessage .= $tr{'bu could not save archive to disk'} ."<br />";
			}
		}
		else {
			$errormessage .= $tr{'bu wrong filename template'} ."<br />";
		}
		# Always clean up the tailings,
		unlink("$swroot/restore/backup.tar");
	        unlink("$swroot/restore/version");
		unlink ("$swroot/tmp/backup.tar");
	}
}

elsif ($cgiparams{'ACTION'} eq $tr{'create settings backup file'}) {
	unless ($errormessage) {
		system('/etc/rc.d/backupscript');

		if (system('/usr/bin/tar', '-C', "${swroot}/backup", '-cf', "${swroot}/tmp/backup.tar", 'backup.dat', 'version')) {
			$errormessage = $tr{'unable to create settings backup file'};
		}
		else {
			my $HOST = `uname -n`; chomp $HOST;
			my $DATE = `date  +"%Y-%m-%d"`; chomp $DATE;
			my %productsettings;
			&readhash("${swroot}/main/productdata", \%productsettings);
			my $PRODUCT = $productsettings{'PRODUCT'};
			my $VERSION = $productsettings{'VERSION'};
			my $REVISION = $productsettings{'REVISION'};
			my $FNAME = "${HOST}_${DATE}_${PRODUCT}_${VERSION}_${REVISION}_settings";

			# Get the archive file
			undef $/;
			open (FILE, "${swroot}/tmp/backup.tar");
			$_= <FILE>;
			close (FILE);
			my $tarLength = length;

			# Send it to the browser
			print "Content-type: application/octect-stream\n";
			print "Content-length: \"$tarLength\"\n";
			print "Content-disposition: attachment; filename=\"$FNAME.tar\"\n\n";
			print;

			# Delete the files
			unlink "${swroot}/tmp/backup.tar";
			unlink "${swroot}/backup/backup.dat";
			unlink "${swroot}/backup/version";

			# Done
			close(STDOUT);
			exit;
		}		
	}
}

# There is no action for 'Add Drive'; it is handled in javascript

if ($cgiparams{'ACTION'} eq $tr{'remove'}) {
	if (open(FILE, "$filename")) {
		my @current = <FILE>;
		close(FILE);

		my $count = 0;
		my $id = 0;
		my $line;
		foreach $line (@current) {
			$id++;
			$count++ if ($cgiparams{$id} eq "on");
		}
		$errormessage .= $tr{'nothing selected'} if ($count == 0);
		unless ($errormessage) {
			if (open(FILE, ">$filename")) {
				flock FILE, 2;
				my $id = 0;
				foreach $line (@current) {
					$id++;
					print FILE "$line" unless ($cgiparams{$id} eq "on");
				}
				close(FILE);
				# Write settings file
				system('/usr/bin/smoothwall/backup_sys -S');
			}
		}
		else {
			$errormessage .= "Could not write config file.<br />\n";
		}
	}
	else {
		$errormessage .= "Could not read config file.<br />\n";
	}
}

# Place to skip all actions if needed.
ERROR:

&showhttpheaders();

&openpage($tr{'bu pnp backup'}, 1, $refresh, 'services');

&openbigbox('100%', 'LEFT');

# Include the simple_monitor function
print <<END;
<script type='text/javascript' src='/ui/js/monitor.js'></script>
<script type='text/javascript' src='/ui/js/backup_monitor.js'></script>
<script type='text/javascript' src='/ui/js/backup_add_drive.js'></script>
<script type='text/javascript'>
	// Schedule the first one
	var backupState = 'start';  // Initial state
	var lastFileno = 0;         // Detect when progress bar should change
	var whichBar = 0;           // Which progress bar
	var maxwidth = '${maxwidth}';
	var removePrompt = '$tr{'bu remove drive'}';
	var backupMonitorObj = new Object();
	var addDriveMonitorObj = new Object();
	var addDriveOneShotObj = new Object();

	simpleMonitor(backupMonitorObj, '/cgi-bin/txt-bu-flag.cgi', handleFlag);
</script>
END

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'bu pnp monitor and media'});
&openbox($tr{'bu backup statusc'});

# Read .../backup/flag into $flag
open FLAG, $flagfile;
read FLAG, my $flag, 500;
close FLAG;

print <<END
<table width='100%' cellpadding='0' cellspacing='0'>
<tr>
	<td colspan='3'><p class='close' id='buStatus' style='height:2.5em; margin-left:4em'></p></td>
</tr>
<tr>
	<td class='base' style='width:20%; margin:1px'>$tr{'bu var backupc'}</td>
	<td style='margin:1px'>
	   <div style='width:${maxwidth}em; height:100%; border:lightgrey 1px solid;'>
		<div class='progressbar'
		   id='buProgressVar' style='width:0; height:100%; background-color:#000090'>&nbsp;</div>
	   </div></td>
	<td style='margin:1px' class='progressend'>&nbsp;</td>
</tr>
<tr>
	<td class='base' style='width:20%'>$tr{'bu total backupc'}</td>
	<td style='margin:1px'>
	   <div style='width:${maxwidth}em; height:100%; border:lightgrey 1px solid;'>
		<div class='progressbar' id='buProgressTotal'
		   style='width:0; height:100%; background-color:#000090'>&nbsp;</div>
	   </div></td>
	<td class='progressend' style='margin:1px'>&nbsp;</td>
</tr>
</table>
END
;

&closebox();

&openbox($tr{'bu media mgmtc'});

&openbox($tr{'bu add new drivec'});

print<<END;
<table class='blank'>
<tr>
	<td align='center' style='width: 20%;text-align:center'>
	   <input id='buAddDrive' type='submit' name='ACTION' value='$tr{"bu add drive"}'
		onclick='simpleMonitor(addDriveMonitorObj, "/cgi-bin/txt-bu-startAdd.cgi", handleAddFlag); return false;'
		style='margin:.2em; text-align:center'><br />
	   <input id='buOK' type='submit' disabled='disabled' name='ACTION' value='$tr{"bu ok"}'
		onclick='simpleMonitor(addDriveOneShotObj, "/cgi-bin/txt-bu-setRsp.cgi?rsp="+buNameEntry.value, no_op);
		return false;' style='margin:.2em; text-align:center'><br />
	   <input id='buCancel' type='submit' disabled='disabled' name='ACTION' value='$tr{"bu cancel"}'
		onclick='simpleMonitor(addDriveOneShotObj, "/cgi-bin/txt-bu-cancelAdd.cgi", no_op); return false;'
		style='margin:.2em; text-align:center'></td>
	<td style='width:75%'><p id='buPrompt'>$tr{'bu default prompt'}</p>
	   <div id='buInput' style='display:none'>
	   <p style='display:inline-block; text-align:right; margin-right:.5em'>$tr{'bu name'}:</p>
	   <input id='buNameEntry' type='text' name='driveName' style='width:50%'
		onkeyup='if (buNameEntry.value.match(/^[a-zA-Z0-9_-]+\$/) == null)
		buNameEntry.style.backgroundColor="#ffdddd";
	   else
		buNameEntry.style.backgroundColor="";
		;'>
	   <p style='display:inline-block; margin-right:.5em; font-style:italic;'>
		allowed: (A-Z, a-z, 0-9, _, -)</p></div>
	</td>
</tr>
</table>
<div id='debug' style='border:green 2pt solid; display:none'></div>
END
  
&closebox();

&openbox($tr{'bu remove drivec'});

my %render_settings =
(
	'url'     => "/cgi-bin/backup.cgi?[%COL%],[%ORD%]",
	'columns' => 
	[
		{ 
			column => '1',
			title  => "$tr{'bu name'}",
			size   => 20,
			valign => 'top',
			sort   => 'cmp',
		},
		{
			column => '2',
			title  => "$tr{'bu id'}",
			size   => 70,
			sort   => 'cmp'
		},
		{
			title  => "$tr{'mark'}", 
			size   => 10,
			mark   => ' ',
		},

	]
);

&displaytable($filename, \%render_settings, $cgiparams{'ORDER'}, $cgiparams{'COLUMN'} );

print <<END
<table class='blank'>
<tr>
	<td style='width: 50%; text-align:center;'><input type='submit' name='ACTION' value="$tr{'remove'}"></td>
</tr>
</table>
END
;

&closebox();

&closebox();
&closebox();

&openbox($tr{'bu settings backup'});

&openbox($tr{'bu save settingsc'});
print <<END
<p style='margin:1em 2em;'>
  $tr{'settings backup instructions long'}
</p>
END
;

print "<div class='base' style='text-align:center; font-size:x-large;'>$extramessage</div>\n";

print <<END
<table style='width: 80%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align:center;'><input type='submit' name='ACTION' value='$tr{'create settings backup file'}'></td>
</tr>
</table>
</form>
END
;

&closebox();

&openbox($tr{'bu restore settingsc'});

print <<END;
<div style='margin:1em 2em 0 2em;'>
  <form method='post' action='/cgi-bin/backup.cgi' enctype='multipart/form-data'>
    <input type='hidden' name='Token' value='$newToken'>
    <input id='fileName' type='hidden' name='fileName' value=''>
  <p>
    $tr{'bu restore settings long'}
  </p>
  <p style='margin:.5em 3em;'>
    <input type='file'
           name='ARCHIVE'
           style='margin-right:5em; width:30em;'
           onchange='document.getElementById("fileName").value = this.value;'>
  </p>
  <p style='margin:1em 0 .3em 0; width:100%; text-align:center;'>
    <input type='submit' name='ACTION' value='$tr{'bu restore'}' style='text-align:center'>
  </p>

  </form>
</div>
END

&closebox();

&closebox();

print "</div>\n";

&alertbox('add','add');

&closebigbox();
&closepage();
