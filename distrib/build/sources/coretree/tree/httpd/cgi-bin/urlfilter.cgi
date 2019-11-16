#!/usr/bin/perl
#
# This code is distributed under the terms of the GPL
#
# (c) 2004-2008 marco.s - http://www.urlfilter.net
#
# $Id: urlfilter.cgi,v 1.5 2008/05/17 00:00:00 marco.s Exp $
#

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use strict;
use warnings;

use IO::Socket;

my (%netsettings, %mainsettings, %proxysettings, %filtersettings, %tcsettings, %uqsettings, %besettings, 
	%updatesettings, %checked, %selected);
my (@repositorylist, @repositoryfiles, @categories, @selectedcategories, @filtergroups, @tclist, @uqlist, 
	@source_urllist, @clients, @temp);
my $swbin = '/usr/bin/smoothwall';
my $http_port='81';
my $id=0;
my $line='';
my $i=0;
my $n=0;
my $time='';
my $filesize;
my $category='';
my $section='';
my $blacklist='';
my $blistbackup='';

my $changed = 'no';
my $tcfile = "${swroot}/urlfilter/timeconst";
my $uqfile = "${swroot}/urlfilter/userquota";
my $dbdir = "${swroot}/urlfilter/blacklists";
my $editdir = "${swroot}/urlfilter/editor";
my $repository = "/httpd/html/repository";
my $hintcolour = '#FFFFCC';

my $sourceurlfile = "${swroot}/urlfilter/autoupdate/autoupdate.urls";
my $updconffile = "${swroot}/urlfilter/autoupdate/autoupdate.conf";
my $updflagfile = "${swroot}/urlfilter/blacklists/.autoupdate.last";

my $errormessage='';
my $infomessage='';
my $updatemessage='';
my $restoremessage='';
my $buttontext='';
my $source_name='';
my $source_url='';
my $blacklistage=0;
my $lastslashpos=0;

my $toggle='';
my $gif='';
my $led='';
my $ldesc='';
my $gdesc='';

my $refresh = q[
<style type="text/css">
textarea {
	white-space: pre;
	word-wrap: normal;
	margin:0 2em 0 0;
}
</style>
];


mkdir("$dbdir") if (! -d $dbdir);
system("touch $tcfile") if (! -e $tcfile);
system("touch $uqfile") if (! -e $uqfile);
system("touch $sourceurlfile") if (! -e $sourceurlfile);

$proxysettings{'ENABLE'} = '';
$proxysettings{'ENABLE_PURPLE'} = '';
$proxysettings{'ENABLE_FILTER'} = '';

&readhash("${swroot}/ethernet/settings", \%netsettings);
&readhash("${swroot}/main/settings", \%mainsettings);
&readhash("${swroot}/proxy/settings", \%proxysettings);

if (-e "${swroot}/proxy/advanced/settings") {
	undef %proxysettings;
	&readhash("${swroot}/proxy/advanced/settings", \%proxysettings);
}

&readblockcategories;

open(FILE, $tcfile);
@tclist = <FILE>;
close(FILE);

open(FILE, $uqfile);
@uqlist = <FILE>;
close(FILE);

open(FILE, $sourceurlfile);
@source_urllist = <FILE>;
close(FILE);

foreach $category (@filtergroups) {
	$filtersettings{$category} = '';
}

$filtersettings{'ACTION'} = '';
$filtersettings{'VALID'} = '';

$filtersettings{'ENABLE_CUSTOM_BLACKLIST'} = 'off';
$filtersettings{'ENABLE_CUSTOM_WHITELIST'} = 'off';
$filtersettings{'ENABLE_CUSTOM_EXPRESSIONS'} = 'off';
$filtersettings{'BLOCK_EXECUTABLES'} = 'off';
$filtersettings{'BLOCK_AUDIO-VIDEO'} = 'off';
$filtersettings{'BLOCK_ARCHIVES'} = 'off';
$filtersettings{'ENABLE_REWRITE'} = 'off';
$filtersettings{'UNFILTERED_CLIENTS'} = '';
$filtersettings{'BANNED_CLIENTS'} = '';
$filtersettings{'SHOW_CATEGORY'} = 'off';
$filtersettings{'SHOW_URL'} = 'off';
$filtersettings{'SHOW_IP'} = 'off';
$filtersettings{'ENABLE_DNSERROR'} = 'off';
$filtersettings{'ENABLE_JPEG'} = 'off';
$filtersettings{'REDIRECT_PAGE'} = '';
$filtersettings{'MSG_TEXT_1'} = '';
$filtersettings{'MSG_TEXT_2'} = '';
$filtersettings{'MSG_TEXT_3'} = '';
$filtersettings{'ENABLE_EXPR_LISTS'} = 'off';
$filtersettings{'BLOCK_IP_ADDR'} = 'off';
$filtersettings{'BLOCK_ALL'} = 'off';
$filtersettings{'ENABLE_EMPTY_ADS'} = 'off';
$filtersettings{'ENABLE_GLOBAL_WHITELIST'} = 'off';
$filtersettings{'ENABLE_SAFESEARCH'} = 'off';
$filtersettings{'ENABLE_LOG'} = 'off';
$filtersettings{'ENABLE_USERNAME_LOG'} = 'off';
$filtersettings{'ENABLE_CATEGORY_LOG'} = 'off';
$filtersettings{'CHILDREN'} = '5';
$filtersettings{'ENABLE_AUTOUPDATE'} = 'off';
$filtersettings{'ENABLE_FULLBACKUP'} = 'off';

&getcgihash(\%filtersettings);

%tcsettings = %filtersettings;
%uqsettings = %filtersettings;
%besettings = %filtersettings;

if (($filtersettings{'ACTION'} eq $tr{'save'}) ||
    ($filtersettings{'ACTION'} eq $tr{'urlfilter save and restart'}) ||
    ($filtersettings{'ACTION'} eq $tr{'urlfilter upload file'}) ||
    ($filtersettings{'ACTION'} eq $tr{'urlfilter remove file'}) ||
    ($filtersettings{'ACTION'} eq $tr{'urlfilter upload background'}) ||
    ($filtersettings{'ACTION'} eq $tr{'urlfilter upload blacklist'}) ||
    ($filtersettings{'ACTION'} eq $tr{'urlfilter backup'}) ||
    ($filtersettings{'ACTION'} eq $tr{'urlfilter restore'})) {

	# Validate data
	@clients = split(/\n/,$filtersettings{'UNFILTERED_CLIENTS'});
	foreach (@clients) {
		s/^\s+//g; s/\s+$//g; s/\s+-\s+/-/g; s/\s+/ /g; s/\n//g;
		$errormessage .= $tr{'urlfilter invalid ip or mask error'} ."<br />\n" if (/.*-.*-.*/);
		@temp = split(/-/);
		foreach (@temp) {
			unless ((&validipormask($_)) || (&validipandmask($_))) {
				$errormessage .= $tr{'urlfilter invalid ip or mask error'} ."<br />\n";
			}
		}
	}
	@clients = split(/\n/,$filtersettings{'BANNED_CLIENTS'});
	foreach (@clients) {
		s/^\s+//g; s/\s+$//g; s/\s+-\s+/-/g; s/\s+/ /g; s/\n//g;
		$errormessage .= $tr{'urlfilter invalid ip or mask error'} ."<br />\n" if (/.*-.*-.*/);
		@temp = split(/-/);
		foreach (@temp) {
			unless ((&validipormask($_)) || (&validipandmask($_))) {
				$errormessage .= $tr{'urlfilter invalid ip or mask error'} ."<br />\n";
			}
		}
	}
	goto ERROR if ($errormessage);

	if (!($filtersettings{'CHILDREN'} =~ /^\d+$/) || ($filtersettings{'CHILDREN'} < 1)) {
		$errormessage .= $tr{'urlfilter invalid num of children'} ."<br />\n";
		goto ERROR;
	}

	# Make sure it's a proper URL
	if ((!($filtersettings{'REDIRECT_PAGE'} eq '')) && (!($filtersettings{'REDIRECT_PAGE'} =~ /^https?:\/\//))) {
		$filtersettings{'REDIRECT_PAGE'} = "http://".$filtersettings{'REDIRECT_PAGE'};
	}


	# upload/download/file management
	if ($filtersettings{'ACTION'} eq $tr{'urlfilter remove file'}) {
		if (-e "$repository/$filtersettings{'ID'}") {
			unlink("$repository/$filtersettings{'ID'}");
		}
		$filtersettings{'ACTION'} = $tr{'urlfilter manage repository'};
	}

	if ($filtersettings{'ACTION'} eq $tr{'urlfilter upload file'}) {
		&getcgihash(\%filtersettings, {'wantfile' => 1, 'filevar' => 'UPLOADFILE'});

		$filtersettings{'ACTION'} = $tr{'urlfilter manage repository'};
		$_ = $filtersettings{'UPLOADFILE'};
		tr/\\/\//;
		$_ = substr($_,rindex($_,"/")+1);
		if ($_) {
			if (copy($filtersettings{'UPLOADFILE'}, "$repository/$_") != 1) {
				$errormessage .= $! ."<br />\n";
				goto ERROR;
			}
		}

	}
	
	if ($filtersettings{'ACTION'} eq $tr{'urlfilter upload blacklist'}) {
		open(BL, ">${swroot}/urlfilter/blacklists.tar.gz");
		flock BL,2;
		print BL $filtersettings{'UPDATEFILE'};
		close BL;
	
		mkdir("${swroot}/urlfilter/update") if (!(-d "${swroot}/urlfilter/update"));

		my $exitcode = system("/usr/bin/tar --no-same-owner -xzf ${swroot}/urlfilter/blacklists.tar.gz -C ${swroot}/urlfilter/update");
		
		if ($exitcode > 0) {
			$errormessage .= $tr{'urlfilter tar error'} ."<br />\n";
		}
		else {
			if (-d "${swroot}/urlfilter/update/category") {
				system("mv ${swroot}/urlfilter/update/category ${swroot}/urlfilter/update/blacklists");
			}

			if (-d "${swroot}/urlfilter/update/BL") {
				system("mv ${swroot}/urlfilter/update/BL ${swroot}/urlfilter/update/blacklists");
			}

			if (!(-d "${swroot}/urlfilter/update/blacklists")) {
				$errormessage .= $tr{'urlfilter invalid content'} ."<br />\n";
			}
			else {
				system("cp -r ${swroot}/urlfilter/update/blacklists/* $dbdir");

				&readblockcategories;
				&readcustomlists;

				&writeconfigfile;

				$updatemessage = $tr{'urlfilter upload success'};

				my $success = message('sgprebuild');
				$infomessage .= $success ."<br />\n" if ($success and $success !~ /fail/i);
				$errormessage .= "sgprebuild ".$tr{'smoothd failure'}."<br \>" unless ($success and $success !~ /fail/i);
				$refresh .= '<meta http-equiv="refresh" content="2;">' unless ($errormessage =~ /fail/i || $errormessage =~ /$tr{'smoothd failure'}/);

				system("logger -t installpackage[urlfilter] \"URL filter blacklist - Blacklist update from local source completed\"");
			}
		}
		if (-d "${swroot}/urlfilter/update") {
			system("rm -rf ${swroot}/urlfilter/update");
		}
		if (-e "${swroot}/urlfilter/blacklists.tar.gz") {
			unlink("${swroot}/urlfilter/blacklists.tar.gz");
		}
		goto ERROR if ($errormessage);
	}
	
	if ($filtersettings{'ACTION'} eq $tr{'urlfilter backup'}) {
		$blistbackup = ($filtersettings{'ENABLE_FULLBACKUP'} eq 'on') ? "blacklists" : "blacklists/custom";
		if (system("/usr/bin/tar -C ${swroot}/urlfilter -czf ${swroot}/urlfilter/backup.tar.gz settings timeconst userquota autoupdate $blistbackup")) {
			$errormessage .= $tr{'urlfilter backup error'} ."<br />\n";
			goto ERROR;
		}
		else {
			print "Content-type: application/gzip\n";
			print "Content-length: ";
			print (-s "${swroot}/urlfilter/backup.tar.gz");
			print "\n";
			print "Content-disposition: attachment; filename=urlfilter-backup.tar.gz\n\n";

			open (FILE, "${swroot}/urlfilter/backup.tar.gz");
			while (<FILE>) { print; }
			close (FILE);

			if (-e "${swroot}/urlfilter/backup.tar.gz") {
				unlink("${swroot}/urlfilter/backup.tar.gz");
			}
			exit;
		}
	}

	if ($filtersettings{'ACTION'} eq $tr{'urlfilter restore'}) {
		open(BU, ">${swroot}/urlfilter/backup.tar.gz");
		flock BU,2;
		print BU $filtersettings{'UPDATEFILE'};
		close BU;

		if (!(-d "${swroot}/urlfilter/restore")) {
			mkdir("${swroot}/urlfilter/restore");
		}

		my $exitcode = system("/usr/bin/tar --no-same-owner --preserve-permissions -xzf ${swroot}/urlfilter/backup.tar.gz -C ${swroot}/urlfilter/restore");
		if ($exitcode > 0) {
			$errormessage .= $tr{'urlfilter tar error'} ."<br />\n";
		}
		else {
			if (!(-e "${swroot}/urlfilter/restore/settings")) {
				$errormessage .= $tr{'urlfilter invalid restore file'} ."<br />\n";
			}
			else {
				system("cp -rp ${swroot}/urlfilter/restore/* ${swroot}/urlfilter/");
				&readblockcategories;
				&readcustomlists;
				&writeconfigfile;

				$restoremessage = $tr{'urlfilter restore success'};
			}
		}

		if (-e "${swroot}/urlfilter/backup.tar.gz") {
			unlink("${swroot}/urlfilter/backup.tar.gz");
		}
		if (-d "${swroot}/urlfilter/restore") {
			system("rm -rf ${swroot}/urlfilter/restore");
		}
		goto ERROR if ($errormessage);
	}

	if ($filtersettings{'ACTION'} eq $tr{'save'}) {
              $filtersettings{'VALID'} = 'yes';
		&savesettings;
		$infomessage .= $tr{'urlfilter settings saved'} ."<br />";
	}

	if ($filtersettings{'ACTION'} eq $tr{'urlfilter save and restart'}) {
		if ((!($proxysettings{'ENABLE'} eq 'on')) && (!($proxysettings{'ENABLE_PURPLE'} eq 'on'))) {
			$errormessage .= $tr{'urlfilter web proxy service required'} ."<br />\n";
			goto ERROR;
		}
		if (!($proxysettings{'ENABLE_FILTER'} eq 'on')) {
			$errormessage .= $tr{'urlfilter not enabled'} ."<br />\n";
			goto ERROR;
		}

              $filtersettings{'VALID'} = 'yes';
		&savesettings;
		$infomessage .= $tr{'urlfilter settings saved'} ."<br />";

		system("chown -R nobody.nobody $dbdir");

		if (-e "$dbdir/custom/allowed/domains.db") {
			unlink("$dbdir/custom/allowed/domains.db");
		}
		if (-e "$dbdir/custom/allowed/urls.db") {
			unlink("$dbdir/custom/allowed/urls.db");
		}
		if (-e "$dbdir/custom/blocked/domains.db") {
			unlink("$dbdir/custom/blocked/domains.db");
		}
		if (-e "$dbdir/custom/blocked/urls.db") {
			unlink("$dbdir/custom/blocked/urls.db");
		}
		&setpermissions ($dbdir);

		my $success = message('squidrestart');
		$infomessage .= $success if ($success and $success !~ /fail/i);
                $errormessage .= "squidrestart ".$tr{'smoothd failure'}."<br \>" unless ($success and $success !~ /fail/i);
	}
}

if ($filtersettings{'ACTION'} eq $tr{'urlfilter save schedule'}) {
	if (($filtersettings{'UPDATE_SOURCE'} eq 'custom') && ($filtersettings{'CUSTOM_UPDATE_URL'} eq '')) {
		$errormessage .= $tr{'urlfilter custom url required'} ."<br />\n";
	}
	else {
		open (FILE, ">$updconffile");
		print FILE "ENABLE_AUTOUPDATE=$filtersettings{'ENABLE_AUTOUPDATE'}\n";
		print FILE "UPDATE_SCHEDULE=$filtersettings{'UPDATE_SCHEDULE'}\n";
		print FILE "UPDATE_SOURCE=$filtersettings{'UPDATE_SOURCE'}\n";
		print FILE "CUSTOM_UPDATE_URL=$filtersettings{'CUSTOM_UPDATE_URL'}\n";
		close FILE;

		my $success = message('sgautoupdate');
		$infomessage = $success if ($success and $success !~ /fail/i);
		$errormessage .= "sgautoupdate ".$tr{'smoothd failure'}."<br \>" unless ($success and $success !~ /fail/i);
	}
}

if ($filtersettings{'ACTION'} eq $tr{'urlfilter update now'}) {
	if ($filtersettings{'UPDATE_SOURCE'} eq 'custom') {
		if ($filtersettings{'CUSTOM_UPDATE_URL'} eq '') {
			$errormessage .= $tr{'urlfilter custom url required<br />'};
		}
		else {
			if (system("${swbin}/autoupdate.pl $filtersettings{'CUSTOM_UPDATE_URL'} &")) {
				$errormessage .= "Failed to start rules update via $filtersettings{'CUSTOM_UPDATE_URL'}.<br />";
			}
			else {
				$infomessage = $tr{'urlfilter rules updated'} ." via $filtersettings{'CUSTOM_UPDATE_URL'}.<br />";
			}
		}
	}
	else {
		if (system("${swbin}/autoupdate.pl $filtersettings{'UPDATE_SOURCE'} &")) {
			$errormessage .= "Failed to start rules update via $filtersettings{'UPDATE_SOURCE'}.<br />";
		}
		else {
			$infomessage = $tr{'urlfilter rules updated'} ." via $filtersettings{'UPDATE_SOURCE'}.<br />";
		}
	}
}


if (-e "${swroot}/urlfilter/settings") {
	&readhash("${swroot}/urlfilter/settings", \%filtersettings);
}

&readcustomlists;

ERROR:

if ($errormessage) {
	$filtersettings{'VALID'} = 'no';
}

$checked{'ENABLE_CUSTOM_BLACKLIST'}{'off'} = '';
$checked{'ENABLE_CUSTOM_BLACKLIST'}{'on'} = '';
$checked{'ENABLE_CUSTOM_BLACKLIST'}{$filtersettings{'ENABLE_CUSTOM_BLACKLIST'}} = "checked='checked'";

$checked{'ENABLE_CUSTOM_WHITELIST'}{'off'} = '';
$checked{'ENABLE_CUSTOM_WHITELIST'}{'on'} = '';
$checked{'ENABLE_CUSTOM_WHITELIST'}{$filtersettings{'ENABLE_CUSTOM_WHITELIST'}} = "checked='checked'";

$checked{'ENABLE_CUSTOM_EXPRESSIONS'}{'off'} = '';
$checked{'ENABLE_CUSTOM_EXPRESSIONS'}{'on'} = '';
$checked{'ENABLE_CUSTOM_EXPRESSIONS'}{$filtersettings{'ENABLE_CUSTOM_EXPRESSIONS'}} = "checked='checked'";

$checked{'BLOCK_EXECUTABLES'}{'off'} = '';
$checked{'BLOCK_EXECUTABLES'}{'on'} = '';
$checked{'BLOCK_EXECUTABLES'}{$filtersettings{'BLOCK_EXECUTABLES'}} = "checked='checked'";

$checked{'BLOCK_AUDIO-VIDEO'}{'off'} = '';
$checked{'BLOCK_AUDIO-VIDEO'}{'on'} = '';
$checked{'BLOCK_AUDIO-VIDEO'}{$filtersettings{'BLOCK_AUDIO-VIDEO'}} = "checked='checked'";

$checked{'BLOCK_ARCHIVES'}{'off'} = '';
$checked{'BLOCK_ARCHIVES'}{'on'} = '';
$checked{'BLOCK_ARCHIVES'}{$filtersettings{'BLOCK_ARCHIVES'}} = "checked='checked'";

$checked{'ENABLE_REWRITE'}{'off'} = '';
$checked{'ENABLE_REWRITE'}{'on'} = '';
$checked{'ENABLE_REWRITE'}{$filtersettings{'ENABLE_REWRITE'}} = "checked='checked'";

$checked{'SHOW_CATEGORY'}{'off'} = '';
$checked{'SHOW_CATEGORY'}{'on'} = '';
$checked{'SHOW_CATEGORY'}{$filtersettings{'SHOW_CATEGORY'}} = "checked='checked'";

$checked{'SHOW_URL'}{'off'} = '';
$checked{'SHOW_URL'}{'on'} = '';
$checked{'SHOW_URL'}{$filtersettings{'SHOW_URL'}} = "checked='checked'";

$checked{'SHOW_IP'}{'off'} = '';
$checked{'SHOW_IP'}{'on'} = '';
$checked{'SHOW_IP'}{$filtersettings{'SHOW_IP'}} = "checked='checked'";

$checked{'ENABLE_DNSERROR'}{'off'} = '';
$checked{'ENABLE_DNSERROR'}{'on'} = '';
$checked{'ENABLE_DNSERROR'}{$filtersettings{'ENABLE_DNSERROR'}} = "checked='checked'";

$checked{'ENABLE_JPEG'}{'off'} = '';
$checked{'ENABLE_JPEG'}{'on'} = '';
$checked{'ENABLE_JPEG'}{$filtersettings{'ENABLE_JPEG'}} = "checked='checked'";

$checked{'ENABLE_EXPR_LISTS'}{'off'} = '';
$checked{'ENABLE_EXPR_LISTS'}{'on'} = '';
$checked{'ENABLE_EXPR_LISTS'}{$filtersettings{'ENABLE_EXPR_LISTS'}} = "checked='checked'";

$checked{'BLOCK_IP_ADDR'}{'off'} = '';
$checked{'BLOCK_IP_ADDR'}{'on'} = '';
$checked{'BLOCK_IP_ADDR'}{$filtersettings{'BLOCK_IP_ADDR'}} = "checked='checked'";

$checked{'BLOCK_ALL'}{'off'} = '';
$checked{'BLOCK_ALL'}{'on'} = '';
$checked{'BLOCK_ALL'}{$filtersettings{'BLOCK_ALL'}} = "checked='checked'";

$checked{'ENABLE_EMPTY_ADS'}{'off'} = '';
$checked{'ENABLE_EMPTY_ADS'}{'on'} = '';
$checked{'ENABLE_EMPTY_ADS'}{$filtersettings{'ENABLE_EMPTY_ADS'}} = "checked='checked'";

$checked{'ENABLE_GLOBAL_WHITELIST'}{'off'} = '';
$checked{'ENABLE_GLOBAL_WHITELIST'}{'on'} = '';
$checked{'ENABLE_GLOBAL_WHITELIST'}{$filtersettings{'ENABLE_GLOBAL_WHITELIST'}} = "checked='checked'";

$checked{'ENABLE_SAFESEARCH'}{'off'} = '';
$checked{'ENABLE_SAFESEARCH'}{'on'} = '';
$checked{'ENABLE_SAFESEARCH'}{$filtersettings{'ENABLE_SAFESEARCH'}} = "checked='checked'";

$checked{'ENABLE_LOG'}{'off'} = '';
$checked{'ENABLE_LOG'}{'on'} = '';
$checked{'ENABLE_LOG'}{$filtersettings{'ENABLE_LOG'}} = "checked='checked'";

$checked{'ENABLE_USERNAME_LOG'}{'off'} = '';
$checked{'ENABLE_USERNAME_LOG'}{'on'} = '';
$checked{'ENABLE_USERNAME_LOG'}{$filtersettings{'ENABLE_USERNAME_LOG'}} = "checked='checked'";

$checked{'ENABLE_CATEGORY_LOG'}{'off'} = '';
$checked{'ENABLE_CATEGORY_LOG'}{'on'} = '';
$checked{'ENABLE_CATEGORY_LOG'}{$filtersettings{'ENABLE_CATEGORY_LOG'}} = "checked='checked'";

foreach $category (@filtergroups) {
	$checked{$category}{'off'} = '';
	$checked{$category}{'on'} = '';
	$checked{$category}{$filtersettings{$category}} = "checked='checked'";
}

&showhttpheaders();

&openpage($tr{'urlfilter configuration'}, 1, $refresh, 'services');

&openbigbox('100%', 'left');

&alertbox($errormessage, "", $infomessage);


if ($updatemessage) {
	print "<p>\n";
	&openbox("$tr{'urlfilter update results'}:");
	print "<class name='base'><br>$updatemessage\n";
	print "&nbsp;</class>\n";
	&closebox();
}

if ($restoremessage) {
	print "<p>\n";
	&openbox("$tr{'urlfilter restore results'}:");
	print "<class name='base'><br>$restoremessage\n";
	print "&nbsp;</class>\n";
	&closebox();
}

print "<form method='post' action='$ENV{'SCRIPT_NAME'}' enctype='multipart/form-data'><div>\n";

if (($proxysettings{'ENABLE_FILTER'} eq 'on')) {
	if (($proxysettings{'ENABLE'} eq 'on')) {
		&openbox("$tr{'urlfilter enabled msg'} $tr{'urlfilter proxy enabled msg'}");
	}
	else {
		&openbox("$tr{'urlfilter enabled msg'} $tr{'urlfilter proxy disabled msg'}");
	}
}
else {
	if (($proxysettings{'ENABLE'} eq 'on')) {
		&openbox("$tr{'urlfilter disabled msg'} $tr{'urlfilter proxy enabled msg'}");
	}
	else {
		&openbox("$tr{'urlfilter disabled msg'} $tr{'urlfilter proxy disabled msg'}");
	}
}
&closebox();

&openbox("$tr{'urlfilter block categories'}:");

print "<table width='100%' cellspacing='0' cellpadding='0'>";

if (@categories == 0) {
print <<END
<tr>
	<td><i>$tr{'urlfilter no categories'}</i></td>
	<td>&nbsp;</td>
	<td>&nbsp;</td>
	<td>&nbsp;</td>
</tr>
END
;
}

my $totalCats = @categories;
my $totalCols = 4;
my $totalRows = int($totalCats/$totalCols);
$totalRows++ if (($totalCats % $totalCols) > 0);

for ($n=0; $n<$totalRows; $n++) {
	print "<tr>\n";
	for ($i=0; $i<$totalCols; $i++) {
		if (($n + $totalRows*$i) < @categories) {
			print "<td style='width:20%;' class='base'>@categories[$n + $totalRows*$i]:</td>\n";
			print "<td style='width:3%;'><input type='checkbox' name=@filtergroups[$n + $totalRows*$i] $checked{@filtergroups[$n + $totalRows*$i]}{'on'} /></td>\n";
		}
	}
	print "</tr>\n";
}
print "</table>";

&closebox();

&openbox('URL Filter Control:');
print <<END
<table style='width:100%'>
<tr>
	<td style='width:50%; text-align:center'>
		<input type='submit' name='ACTION' value='$tr{'save'}' /></td>
	<td style='width:50%; text-align:center'>
		<input type='submit' name='ACTION' value='$tr{'urlfilter save and restart'}' /></td>
</tr>
</table>
END
;
&closebox();

&openbox("$tr{'urlfilter custom blacklist'}:");
print <<END
<div>
	<p style='margin:1em 0 1.5em 1em; text-align:right; display:inline-block'>$tr{'enable'}</p>
	<p style='margin:1em 0 1.5em .5em; text-align:left; display:inline-block'>
		<input type='checkbox' name='ENABLE_CUSTOM_BLACKLIST' $checked{'ENABLE_CUSTOM_BLACKLIST'}{'on'} /></p>
</div>

<table style='margin:0 1em 0 2em'>
<tr>
	<td colspan='2' style='text-align:center'>
		<p style='margin:0 2em 0 0'>
			$tr{'urlfilter blocked domains'}&nbsp;<img src='/ui/img/blob.gif' alt='*' />
		</p>
	</td>
	<td colspan='2' style="text-align:center">
		<p style='margin:0 0 0 2em'>
			$tr{'urlfilter blocked urls'}&nbsp;<img src='/ui/img/blob.gif' alt='*' />
		</p>
	</td>
</tr>
<tr>
	<td colspan='2' style='text-align:center'>
		<textarea name='CUSTOM_BLACK_DOMAINS' cols='36' rows='6'>
END
;

if (-e "$dbdir/custom/blocked/domains") {
	open(FILE,"$dbdir/custom/blocked/domains");
	my @data = <FILE>;
	close(FILE);
	print @data;
}

print <<END
</textarea></td>
	<td colspan='2' style='text-align:center'>
		<textarea name='CUSTOM_BLACK_URLS' cols='36' rows='6'>
END
;

if (-e "$dbdir/custom/blocked/urls") {
	open(FILE,"$dbdir/custom/blocked/urls");
	my @data = <FILE>;
	close(FILE);
	print @data;
}

print <<END
		</textarea></td>
</tr>
</table>
END
;

&closebox();

&openbox("$tr{'urlfilter custom whitelist'}:");
print <<END
<div>
	<p style='margin:1em 0 1.5em 1em; text-align:right; display:inline-block'>
		$tr{'enable'}
	</p>
	<p style='margin:1em 0 1.5em .5em; text-align:left; display:inline-block'>
		<input type='checkbox' name='ENABLE_CUSTOM_WHITELIST' $checked{'ENABLE_CUSTOM_WHITELIST'}{'on'} />
	</p>
</div>
<table style='margin:0 1em 0 2em'>
<tr>
	<td colspan='2' style='text-align:center'>
		<p style='margin:0 2em 0 0'>$tr{'urlfilter allowed domains'}&nbsp;<img src='/ui/img/blob.gif' alt='*' />
		</p></td>
	<td colspan='2' style="text-align:center">
		<p style='margin:0 0 0 2em'>$tr{'urlfilter allowed urls'}&nbsp;<img src='/ui/img/blob.gif' alt='*' />
		</p>
	</td>
</tr>
<tr>
	<td colspan='2' style='text-align:center'>
		<textarea name='CUSTOM_WHITE_DOMAINS' cols='36' rows='6'>
END
;

if (-e "$dbdir/custom/allowed/domains") {
	open(FILE,"$dbdir/custom/allowed/domains");
	my @data = <FILE>;
	close(FILE);
	print @data;
}

print <<END
</textarea></td>
	<td colspan='2' style='text-align:center'>
		<textarea name='CUSTOM_WHITE_URLS' cols='36' rows='6'>
END
;

if (-e "$dbdir/custom/allowed/urls") {
	open(FILE,"$dbdir/custom/allowed/urls");
	my @data = <FILE>;
	close(FILE);
	print @data;
}

print <<END
		</textarea></td>
</tr>
</table>
END
;
&closebox();

&openbox("$tr{'urlfilter custom expression list'}:");
print <<END
<div>
	<p style='margin:1em 0 1.5em 1em; text-align:right; display:inline-block'>
		$tr{'enable'}
	</p>
	<p style='margin:1em 0 1.5em .5em; text-align:left; display:inline-block'>
		<input type='checkbox' name='ENABLE_CUSTOM_EXPRESSIONS' $checked{'ENABLE_CUSTOM_EXPRESSIONS'}{'on'} />
	</p>
</div>
<table width='100%'>
<tr>
	<td colspan='4' style='text-align:center'>
		<p style='margin:0 2em 0 0'>
			$tr{'urlfilter blocked expressions'}&nbsp;<img src='/ui/img/blob.gif' alt='*' />
		</p>
	</td>
</tr>
<tr>
	<td colspan='4' style='text-align:center'>
		<textarea name='CUSTOM_EXPRESSIONS' cols='80' rows='6' style='margin:0 0 0 0'>
END
;

if (-e "$dbdir/custom/blocked/expressions") {
        open(FILE,"$dbdir/custom/blocked/expressions");
        my @data = <FILE>;
        close(FILE);
        print @data;
}

print <<END
		</textarea></td>
</tr>
</table>
END
;

&closebox();

&openbox('URL Filter Control:');
print <<END
<table style='width:100%'>
<tr>
	<td style='width:50%; text-align:center'>
		<input type='submit' name='ACTION' value='$tr{'save'}' />
	</td>
	<td style='width:50%; text-align:center'>
		<input type='submit' name='ACTION' value='$tr{'urlfilter save and restart'}' />
	</td>
</tr>
</table>
END
;

&closebox();

&openbox("$tr{'urlfilter file ext block'}:");
print <<END
<table width='100%' style='margin-top:1em'>
<tr>
	<td style='width:25%;' class='base'>$tr{'urlfilter block executables'}:</td>
	<td style='width:12%;'><input type='checkbox' name='BLOCK_EXECUTABLES' $checked{'BLOCK_EXECUTABLES'}{'on'} /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter block audio-video'}:</td>
	<td><input type='checkbox' name='BLOCK_AUDIO-VIDEO' $checked{'BLOCK_AUDIO-VIDEO'}{'on'} /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter block archives'}:</td>
	<td><input type='checkbox' name='BLOCK_ARCHIVES' $checked{'BLOCK_ARCHIVES'}{'on'} /></td>
	<td>&nbsp;</td>
	<td>&nbsp;</td>
</tr>
</table>
END
;
&closebox();

&openbox("$tr{'urlfilter network access control'}:");
print <<END
<table style='margin:1em 1em 0 2em'>
<tr>
	<td colspan='2' style='text-align:center'>
		<p style='margin:0 2em 0 0'>
			$tr{'urlfilter unfiltered clients'}&nbsp;<img src='/ui/img/blob.gif' alt='*' />
		</p></td>
	<td colspan='2' style="text-align:center">
		<p style='margin:0 0 0 2em'>
			$tr{'urlfilter banned clients'}&nbsp;<img src='/ui/img/blob.gif' alt='*' />
		</p></td>
</tr>
<tr>
	<td colspan='2' style='text-align:center'>
		<textarea name='UNFILTERED_CLIENTS' cols='36' rows='6'>
END
;

# transform from pre1.5 client definitions
$filtersettings{'UNFILTERED_CLIENTS'} =~ s/^\s+//g;
$filtersettings{'UNFILTERED_CLIENTS'} =~ s/\s+$//g;
$filtersettings{'UNFILTERED_CLIENTS'} =~ s/\s+-\s+/-/g;
$filtersettings{'UNFILTERED_CLIENTS'} =~ s/\s+/ /g;

@clients = split(/ /,$filtersettings{'UNFILTERED_CLIENTS'});
undef $filtersettings{'UNFILTERED_CLIENTS'};
foreach (@clients) {
	$filtersettings{'UNFILTERED_CLIENTS'} .= "$_\n";
}

print $filtersettings{'UNFILTERED_CLIENTS'} if ($filtersettings{'UNFILTERED_CLIENTS'});

print <<END
		</textarea></td>
	<td colspan='2' style='text-align:center'>
		<textarea name='BANNED_CLIENTS' cols='36' rows='6'>
END
;

# transform from pre1.5 client definitions
$filtersettings{'BANNED_CLIENTS'} =~ s/^\s+//g;
$filtersettings{'BANNED_CLIENTS'} =~ s/\s+$//g;
$filtersettings{'BANNED_CLIENTS'} =~ s/\s+-\s+/-/g;
$filtersettings{'BANNED_CLIENTS'} =~ s/\s+/ /g;

@clients = split(/ /,$filtersettings{'BANNED_CLIENTS'});
undef $filtersettings{'BANNED_CLIENTS'};
foreach (@clients) {
	$filtersettings{'BANNED_CLIENTS'} .= "$_\n";
}

print $filtersettings{'BANNED_CLIENTS'} if ($filtersettings{'BANNED_CLIENTS'});

print <<END
		</textarea></td>
</tr>
</table>
END
;
&closebox();

&openbox("$tr{'urlfilter block settings'}:");
print <<END
<table width='100%' style='margin-top:1em'>
<tr>
	<td style='width:25%;' class='base'>$tr{'urlfilter show category'}:</td>
	<td style='width:3%;'><input type='checkbox' name='SHOW_CATEGORY' $checked{'SHOW_CATEGORY'}{'on'} /></td>
	<td style='width:20%;' class='base'><img src='/ui/img/blob.gif' alt='*' />&nbsp;$tr{'urlfilter redirectpage'}:</td>
	<td><input type='text' name='REDIRECT_PAGE' value='$filtersettings{'REDIRECT_PAGE'}' size='45' /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter show url'}:</td>
	<td><input type='checkbox' name='SHOW_URL' $checked{'SHOW_URL'}{'on'} /></td>
	<td class='base'><img src='/ui/img/blob.gif' alt='*' />&nbsp;$tr{'urlfilter msg text 1'}:</td>
	<td><input type='text' name='MSG_TEXT_1' value='$filtersettings{'MSG_TEXT_1'}' size='45' /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter show ip'}:</td>
	<td><input type='checkbox' name='SHOW_IP' $checked{'SHOW_IP'}{'on'} /></td>
	<td class='base'><img src='/ui/img/blob.gif' alt='*' />&nbsp;$tr{'urlfilter msg text 2'}:</td>
	<td><input type='text' name='MSG_TEXT_2' value='$filtersettings{'MSG_TEXT_2'}' size='45' /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter show dnserror'}:</td>
	<td><input type='checkbox' name='ENABLE_DNSERROR' $checked{'ENABLE_DNSERROR'}{'on'} /></td>
	<td class='base'><img src='/ui/img/blob.gif' alt='*' />&nbsp;$tr{'urlfilter msg text 3'}:</td>
	<td><input type='text' name='MSG_TEXT_3' value='$filtersettings{'MSG_TEXT_3'}' size='45' /></td>
</tr>
</table>
END
;
&closebox();

&openbox("$tr{'urlfilter advanced settings'}:");
print <<END
<table width='100%'>
<tr>
	<td style='width:40%;' class='base'>$tr{'urlfilter enable expression lists'}:</td>
	<td style='width:3%;'><input type='checkbox' name='ENABLE_EXPR_LISTS' $checked{'ENABLE_EXPR_LISTS'}{'on'} /></td>
	<td style='width:40%;' class='base'>$tr{'urlfilter enable log'}:</td>
	<td><input type='checkbox' name='ENABLE_LOG' $checked{'ENABLE_LOG'}{'on'} /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter safesearch'}:</td>
	<td><input type='checkbox' name='ENABLE_SAFESEARCH' $checked{'ENABLE_SAFESEARCH'}{'on'} /></td>
	<td class='base'>$tr{'urlfilter username log'}:</td>
	<td><input type='checkbox' name='ENABLE_USERNAME_LOG' $checked{'ENABLE_USERNAME_LOG'}{'on'} /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter empty ads'}:</td>
	<td><input type='checkbox' name='ENABLE_EMPTY_ADS' $checked{'ENABLE_EMPTY_ADS'}{'on'} /></td>
	<td class='base'>$tr{'urlfilter category log'}:</td>
	<td><input type='checkbox' name='ENABLE_CATEGORY_LOG' $checked{'ENABLE_CATEGORY_LOG'}{'on'} /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter block ip'}:</td>
	<td><input type='checkbox' name='BLOCK_IP_ADDR' $checked{'BLOCK_IP_ADDR'}{'on'} /></td>
	<td class='base'>$tr{'urlfilter children'}:</td>
	<td><input type='text' name='CHILDREN' value='$filtersettings{'CHILDREN'}' size='5' /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter block all'}:</td>
	<td><input type='checkbox' name='BLOCK_ALL' $checked{'BLOCK_ALL'}{'on'} /></td>
	<td class='base'>$tr{'urlfilter whitelist always allowed'}:</td>
	<td><input type='checkbox' name='ENABLE_GLOBAL_WHITELIST' $checked{'ENABLE_GLOBAL_WHITELIST'}{'on'} /></td>
</tr>
</table>
END
;

&closebox();

&openbox('URL Filter Control:');
print <<END;
<table style='width:100%'>
<tr>
	<td style='width:50%; text-align:center'>
		<input type='submit' name='ACTION' value='$tr{'save'}' />
	</td>
	<td style='width:50%; text-align:center'>
		<input type='submit' name='ACTION' value='$tr{'urlfilter save and restart'}' />
	</td>
</tr>
</table>
END
&closebox();

print "</div></form>\n";

print "<form method='post' action='$ENV{'SCRIPT_NAME'}' enctype='multipart/form-data'><div>";
&openbox("$tr{'urlfilter blacklist update'}:");

print <<END
<table width='100%'>
<tr>
	<td>
		<p style='margin:1em'>$tr{'urlfilter upload information'}</p>
		<p style='margin:1em'>$tr{'urlfilter upload text'}:</p>
	</td>
</tr>
</table>
<table width='100%'>
<tr>
	<td style='width:50%; text-align:center'><input type='file' name='UPDATEFILE' /></td>
	<td style='width:50%; text-align:center'>
		<input type='submit' name='ACTION' value='$tr{'urlfilter upload blacklist'}' /></td>
</tr>
</table>
END
;

&closebox();

print "</div></form>";

print "<form method='post' action='$ENV{'SCRIPT_NAME'}' enctype='multipart/form-data'><div>";
&openbox("$tr{'urlfilter automatic blacklist update'}:");

print <<END
<table width='100%'>
END
;

$updatesettings{'ENABLE_AUTOUPDATE'} = '';
$updatesettings{'UPDATE_SCHEDULE'} = 'monthly';
$updatesettings{'UPDATE_SOURCE'} = '';
$updatesettings{'CUSTOM_UPDATE_URL'} = '';

if (-e "$updconffile") {
	&readhash("$updconffile", \%updatesettings);
}

$checked{'ENABLE_AUTOUPDATE'}{'off'} = '';
$checked{'ENABLE_AUTOUPDATE'}{'on'} = '';
$checked{'ENABLE_AUTOUPDATE'}{$updatesettings{'ENABLE_AUTOUPDATE'}} = "checked='checked'";

$selected{'UPDATE_SCHEDULE'}{'daily'} = '';
$selected{'UPDATE_SCHEDULE'}{'weekly'} = '';
$selected{'UPDATE_SCHEDULE'}{'monthly'} = '';
$selected{'UPDATE_SCHEDULE'}{$updatesettings{'UPDATE_SCHEDULE'}} = "selected='selected'";

foreach (@source_urllist) {
	chomp;
	$source_name = substr($_,0,rindex($_,","));
	$source_url = substr($_,index($_,",")+1);
	$selected{'UPDATE_SOURCE'}{$source_url} = '';
}
$selected{'UPDATE_SOURCE'}{'custom'} = '';
$selected{'UPDATE_SOURCE'}{$updatesettings{'UPDATE_SOURCE'}} = "selected='selected'";

if (-e "$updflagfile") {
	$blacklistage = int(-M "$updflagfile");
	print <<END;
<tr>
	<td colspan='4'>
		<p style='margin:0 0 1em 1em'>
			<b>[</b> <small><i>$tr{'urlfilter blacklist age 1'} <b>$blacklistage</b> $tr{'urlfilter blacklist age 2'}</i></small> <b>]</b>
		</p></td>
</tr>
END
}

print <<END
<tr>
	<td style='width:25%;' class='base'>$tr{'urlfilter enable automatic blacklist update'}:</td>
	<td style='width:65%;'><input type='checkbox' name='ENABLE_AUTOUPDATE' $checked{'ENABLE_AUTOUPDATE'}{'on'} /></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter automatic update schedule'}:</td>
	<td><select name='UPDATE_SCHEDULE'>
		<option value='daily' $selected{'UPDATE_SCHEDULE'}{'daily'}>$tr{'urlfilter daily'}</option>
		<option value='weekly' $selected{'UPDATE_SCHEDULE'}{'weekly'}>$tr{'urlfilter weekly'}</option>
		<option value='monthly' $selected{'UPDATE_SCHEDULE'}{'monthly'}>$tr{'urlfilter monthly'}</option>
	</select></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter select source'}:</td>
	<td colspan='2'>
	<select name='UPDATE_SOURCE'>
END
;

foreach (@source_urllist) {
	chomp;
	$source_name = substr($_,0,rindex($_,","));
	$source_url = substr($_,index($_,",")+1);
	print "		<option value='$source_url' $selected{'UPDATE_SOURCE'}{$source_url}>$source_name</option>\n";
}

print <<END
		<option value='custom' $selected{'UPDATE_SOURCE'}{'custom'}>$tr{'urlfilter custom url'}</option>
	</select></td>
</tr>
<tr>
	<td class='base'>$tr{'urlfilter custom url'}:</td>
	<td><input type='text' name='CUSTOM_UPDATE_URL' value='$updatesettings{'CUSTOM_UPDATE_URL'}' size='65' /></td>
</tr>
</table>

<table width='100%'>
<tr>
	<td style='text-align:center; width:50%'>
		<input type='submit' name='ACTION' value='$tr{'urlfilter save schedule'}'></td>
	<td style='text-align:center; width:50%'>
		<input type='submit' name='ACTION' value='$tr{'urlfilter update now'}'></td>
</tr>
</table>
END
;

&closebox();

print "</div></form>";

$checked{'ENABLE_FULLBACKUP'}{'off'} = '';
$checked{'ENABLE_FULLBACKUP'}{'on'} = '';
$checked{'ENABLE_FULLBACKUP'}{$filtersettings{'ENABLE_FULLBACKUP'}} = "checked='checked'";



print "<form method='post' action='$ENV{'SCRIPT_NAME'}' enctype='multipart/form-data'><div>";
&openbox("Backup and Restore Settings:");

print <<END
<table style='margin-top:1em; width:100%'>
<tr>
	<td style='width:25%;' class='base'>$tr{'urlfilter enable full backup'}:</td>
	<td style='width:25%;'><input type='checkbox' name='ENABLE_FULLBACKUP' $checked{'ENABLE_FULLBACKUP'}{'on'} /></td>
	<td colspan='2' style='text-align:center; width:50%'><input type='submit' name='ACTION' value='$tr{'urlfilter backup'}' /></td>
</tr>
<tr>
	<td colspan='4' style='height:1em'></td>
</tr>
<tr>
	<td colspan='4'>
		<p style='margin:0 0 0 1em'>Choose archive to restore:</p></td>
</tr>
<tr>
	<td colspan='2'style='text-align:center'><input type='file' name='UPDATEFILE' /></td>
	<td colspan='2' style='text-align:center'>
		<input type='submit' name='ACTION' value='$tr{'urlfilter restore'}' /></td>
</tr>
</table>
END
;

&closebox();

print <<END
</div></form>
<table width='100%'>
<tr>
	<td>
		<p style='margin:0 0 0 1em'>
			<img src='/ui/img/blob.gif' alt='*' style='vertical-align: text-top;'>&nbsp;$tr{'this field may be blank'}
		</p>
	</td>
	<td align='right'>
		<p style='font-size:8pt; margin:0 1em 0 0'>
			<i>Adapted from <a href='http://www.urlfilter.net'
			onclick="window.open(this.href); return false">URL Filter 1.7.1</a></i>
		</p>
	</td>
</tr>
</table>
<br>
END
;

&closebigbox();

&closepage();

# -------------------------------------------------------------------

sub savesettings
{
	# transform to pre1.5 client definitions
	@clients = split(/\n/,$filtersettings{'UNFILTERED_CLIENTS'});
	undef $filtersettings{'UNFILTERED_CLIENTS'};
	foreach(@clients) {
		s/^\s+//g; s/\s+$//g; s/\s+-\s+/-/g; s/\s+/ /g; s/\n//g;
		$filtersettings{'UNFILTERED_CLIENTS'} .= "$_ ";
	}
	$filtersettings{'UNFILTERED_CLIENTS'} =~ s/\s+$//;

	# transform to pre1.5 client definitions
	@clients = split(/\n/,$filtersettings{'BANNED_CLIENTS'});
	undef $filtersettings{'BANNED_CLIENTS'};
	foreach(@clients) {
		s/^\s+//g; s/\s+$//g; s/\s+-\s+/-/g; s/\s+/ /g; s/\n//g;
		$filtersettings{'BANNED_CLIENTS'} .= "$_ ";
	}
	$filtersettings{'BANNED_CLIENTS'} =~ s/\s+$//;

	&writeconfigfile;

	delete $filtersettings{'CUSTOM_BLACK_DOMAINS'};
	delete $filtersettings{'CUSTOM_BLACK_URLS'};
	delete $filtersettings{'CUSTOM_WHITE_DOMAINS'};
	delete $filtersettings{'CUSTOM_WHITE_URLS'};
	delete $filtersettings{'CUSTOM_EXPRESSIONS'};
	delete $filtersettings{'BACKGROUND'};
	delete $filtersettings{'UPDATEFILE'};

	&writehash("${swroot}/urlfilter/settings", \%filtersettings);
}

# -------------------------------------------------------------------

sub readblockcategories
{
	undef(@categories);

	&getblockcategory ($dbdir);

	foreach (@categories) {
		$_ = substr($_,length($dbdir)+1);
	}

	@filtergroups = @categories;

	foreach (@filtergroups) {
		s/\//_SLASH_/g;
		s/ /_SPACE_/g;
        	tr/a-z/A-Z/;
		$_ = "FILTER_".$_;
	}
}

# -------------------------------------------------------------------

sub getblockcategory
{
	foreach $category (<$_[0]/*>) {

		if (-d $category) {
			if ((-e "$category/domains") || (-e "$category/urls")) {
				unless ($category =~ /\bcustom\b/) {
					push(@categories,$category);
				}
			}
			$category =~ s/ /\\ /g;
			&getblockcategory ($category);
		}
	}
}

# -------------------------------------------------------------------

sub readcustomlists
{
	if (-e "$dbdir/custom/blocked/domains") {
		open(FILE,"$dbdir/custom/blocked/domains");
		delete $filtersettings{'CUSTOM_BLACK_DOMAINS'};
		while (<FILE>) {
			$filtersettings{'CUSTOM_BLACK_DOMAINS'} .= $_
		}
		close(FILE);
	}

	if (-e "$dbdir/custom/blocked/urls") {
		open(FILE,"$dbdir/custom/blocked/urls");
		delete $filtersettings{'CUSTOM_BLACK_URLS'};
		while (<FILE>) {
			$filtersettings{'CUSTOM_BLACK_URLS'} .= $_
		}
		close(FILE);
	}

	if (-e "$dbdir/custom/blocked/expressions") {
		open(FILE,"$dbdir/custom/blocked/expressions");
		delete $filtersettings{'CUSTOM_EXPRESSIONS'};
		while (<FILE>) {
			$filtersettings{'CUSTOM_EXPRESSIONS'} .= $_
		}
		close(FILE);
	}

	if (-e "$dbdir/custom/allowed/domains") {
		open(FILE,"$dbdir/custom/allowed/domains");
		delete $filtersettings{'CUSTOM_WHITE_DOMAINS'};
		while (<FILE>) {
			$filtersettings{'CUSTOM_WHITE_DOMAINS'} .= $_
		}
		close(FILE);
	}
	if (-e "$dbdir/custom/allowed/urls") {
		open(FILE,"$dbdir/custom/allowed/urls");
		delete $filtersettings{'CUSTOM_WHITE_URLS'};
		while (<FILE>) {
			$filtersettings{'CUSTOM_WHITE_URLS'} .= $_
		}
		close(FILE);
	}
}

# -------------------------------------------------------------------

sub aggregatedconstraints
{
	my $aggregated;
	my @old;
	my @new;
	my @tmp1;
	my @tmp2;
	my $x;

	if (-e $tcfile) {
		open(TC, $tcfile);
		@old = <TC>;
		close(TC);

		while (@old > 0) {
			$aggregated = 0;
			$x = shift(@old);
			chomp($x);
			@tmp1 = split(/\,/,$x);
			$tmp1[16] = '';

			foreach (@new) {
				@tmp2 = split(/\,/);
				if (($tmp1[15] eq 'on') && ($tmp2[15] eq 'on')) {
					if (($tmp1[0] eq $tmp2[0]) &&
					    ($tmp1[12] eq $tmp2[12]) &&
					    ($tmp1[13] eq $tmp2[13]) &&
					    ($tmp1[14] eq $tmp2[14])) {
						$aggregated = 1;
						$tmp2[16] .= "    weekly ";
						$tmp2[16] .= "m" if ($tmp1[1] eq 'on');
						$tmp2[16] .= "t" if ($tmp1[2] eq 'on');
						$tmp2[16] .= "w" if ($tmp1[3] eq 'on');
						$tmp2[16] .= "h" if ($tmp1[4] eq 'on');
						$tmp2[16] .= "f" if ($tmp1[5] eq 'on');
						$tmp2[16] .= "a" if ($tmp1[6] eq 'on');
						$tmp2[16] .= "s" if ($tmp1[7] eq 'on');
						$tmp2[16] .= " $tmp1[8]:$tmp1[9]-$tmp1[10]:$tmp1[11]\n";
						$_ = join(",",@tmp2);
					}

				}
			}
			if (!$aggregated) {
				$tmp1[16] .= "    weekly ";
				$tmp1[16] .= "m" if ($tmp1[1] eq 'on');
				$tmp1[16] .= "t" if ($tmp1[2] eq 'on');
				$tmp1[16] .= "w" if ($tmp1[3] eq 'on');
				$tmp1[16] .= "h" if ($tmp1[4] eq 'on');
				$tmp1[16] .= "f" if ($tmp1[5] eq 'on');
				$tmp1[16] .= "a" if ($tmp1[6] eq 'on');
				$tmp1[16] .= "s" if ($tmp1[7] eq 'on');
				$tmp1[16] .= " $tmp1[8]:$tmp1[9]-$tmp1[10]:$tmp1[11]\n";
				$x = join(",",@tmp1);
				push(@new,$x);
			}
		}
	}

	return @new;

}

# -------------------------------------------------------------------

sub setpermissions
{
	my $bldir = $_[0];

	foreach $category (<$bldir/*>) {
        	 if (-d $category) {
			system("chmod 755 $category &> /dev/null");
			foreach $blacklist (<$category/*>) {
         			system("chmod 644 $blacklist &> /dev/null") if (-f $blacklist);
         			system("chmod 755 $blacklist &> /dev/null") if (-d $blacklist);
			}
        	 	system("chmod 666 $category/*.db &> /dev/null");
			&setpermissions ($category);
		}
	 }
}

# -------------------------------------------------------------------

sub writeconfigfile
{
	my $executables = "\\.\(ade|adp|asx|bas|bat|chm|com|cmd|cpl|crt|dll|eml|exe|hiv|hlp|hta|inc|inf|ins|isp|jse|jtd|lnk|msc|msh|msi|msp|mst|nws|ocx|oft|ops|pcd|pif|plx|reg|scr|sct|sha|shb|shm|shs|sys|tlb|tsp|url|vbe|vbs|vxd|wsc|wsf|wsh\)\$";
	my $audiovideo = "\\.\(aiff|asf|avi|dif|divx|flv|mov|movie|mp3|mpe?g?|mpv2|ogg|ra?m|snd|qt|wav|wma|wmf|wmv\)\$";
	my $archives = "\\.\(bin|bz2|cab|cdr|dmg|gz|hqx|rar|smi|sit|sea|tar|tgz|zip\)\$";

	my $ident = " anonymous";

	my $defaultrule='';
	my $tcrule='';
	my $redirect='';
	my $qredirect='';

	my $idx;

	my @ec=();
	my @tc=();
	my @uq=();

	mkdir("$dbdir/custom") if (!(-d "$dbdir/custom"));
	mkdir("$dbdir/custom/blocked") if (!(-d "$dbdir/custom/blocked"));
	mkdir("$dbdir/custom/allowed") if (!(-d "$dbdir/custom/allowed"));

	open(FILE, ">/$dbdir/custom/blocked/domains");
	@temp = split(/\n/,$filtersettings{'CUSTOM_BLACK_DOMAINS'});
	foreach (@temp) {
		s/^\s+//g; s/\s+$//g; s/\n//g;
		print FILE "$_\n" unless ($_ eq '');
	}
	close(FILE);

	open(FILE, ">/$dbdir/custom/blocked/urls");
	@temp = split(/\n/,$filtersettings{'CUSTOM_BLACK_URLS'});
	foreach (@temp) {
		s/^\s+//g; s/\s+$//g; s/\n//g;
		print FILE "$_\n" unless ($_ eq '');
	}
	close(FILE);

	open(FILE, ">/$dbdir/custom/blocked/expressions");
	@temp = split(/\n/,$filtersettings{'CUSTOM_EXPRESSIONS'});
	foreach (@temp) {
		s/^\s+//g; s/\s+$//g; s/\n//g;
		print FILE "$_\n" unless ($_ eq '');
	}
	close(FILE);

	open(FILE, ">/$dbdir/custom/blocked/files");
	print FILE "$executables\n" if ($filtersettings{'BLOCK_EXECUTABLES'} eq 'on');
	print FILE "$audiovideo\n" if ($filtersettings{'BLOCK_AUDIO-VIDEO'} eq 'on');
	print FILE "$archives\n" if ($filtersettings{'BLOCK_ARCHIVES'} eq 'on');
	close(FILE);

	open(FILE, ">/$dbdir/custom/allowed/domains");
	@temp = split(/\n/,$filtersettings{'CUSTOM_WHITE_DOMAINS'});
	foreach (@temp) {
		s/^\s+//g; s/\s+$//g; s/\n//g;
		unless ($_ eq '') { print FILE "$_\n"; }
	}
	close(FILE);

	open(FILE, ">/$dbdir/custom/allowed/urls");
	@temp = split(/\n/,$filtersettings{'CUSTOM_WHITE_URLS'});
	foreach (@temp) {
		s/^\s+//g; s/\s+$//g; s/\n//g;
		unless ($_ eq '') { print FILE "$_\n"; }
	}
	close(FILE);

	$ident = "" if ($filtersettings{'ENABLE_USERNAME_LOG'} eq 'on');

	if ($filtersettings{'REDIRECT_PAGE'} eq '') {
		if (($filtersettings{'SHOW_CATEGORY'} eq 'on') ||
		    ($filtersettings{'SHOW_URL'} eq 'on') ||
		    ($filtersettings{'SHOW_IP'} eq 'on')) {
			$redirect .= "&category=%t" if ($filtersettings{'SHOW_CATEGORY'} eq 'on');
			$redirect .= "&url=%u" if ($filtersettings{'SHOW_URL'} eq 'on');
			$redirect .= "&ip=%a" if ($filtersettings{'SHOW_IP'} eq 'on');
			$redirect  =~ s/^&/?/;
			$redirect = "http://$netsettings{'GREEN_ADDRESS'}:$http_port/redirect.cgi".$redirect; 
		}
		else {
			$redirect="http://$netsettings{'GREEN_ADDRESS'}:$http_port/redirect.cgi";
		}
	}
	else {
		$redirect=$filtersettings{'REDIRECT_PAGE'};
	}

	$redirect  = "302:http://0.0.0.0" if ($filtersettings{'ENABLE_DNSERROR'} eq 'on');

	undef $defaultrule;

	$defaultrule .= "custom-allowed " if ($filtersettings{'ENABLE_CUSTOM_WHITELIST'} eq 'on');

	if ($filtersettings{'BLOCK_ALL'} eq 'on') {
		$defaultrule .= "none";
	}
	else {
		$defaultrule .= "!in-addr " if ($filtersettings{'BLOCK_IP_ADDR'} eq 'on');

		for ($i=0; $i <= @filtergroups; $i++) {
			if (($filtergroups[$i]) && $filtersettings{$filtergroups[$i]} eq 'on') {
				$defaultrule .= "!$categories[$i] ";
			}
		}
		$defaultrule .= "!custom-blocked " if ($filtersettings{'ENABLE_CUSTOM_BLACKLIST'} eq 'on');
		$defaultrule .= "!custom-expressions " if ($filtersettings{'ENABLE_CUSTOM_EXPRESSIONS'} eq 'on');
		if (($filtersettings{'BLOCK_EXECUTABLES'} eq 'on') ||
		    ($filtersettings{'BLOCK_AUDIO-VIDEO'} eq 'on') ||
		    ($filtersettings{'BLOCK_ARCHIVES'} eq 'on')) {
			$defaultrule .= "!files ";
		}
		$defaultrule .= "any";
	}

	$defaultrule =~ s/\//_/g;

	open(FILE, ">${swroot}/urlfilter/squidGuard.conf") or die "Unable to write squidGuard.conf file";
	flock(FILE, 2);

	print FILE "logdir /var/log/squidGuard\n";
	print FILE "dbhome $dbdir\n\n";

	undef @repositoryfiles;
	if ($filtersettings{'ENABLE_REWRITE'} eq 'on') {
		@repositorylist = <$repository/*>;
		foreach (@repositorylist) {
			push(@repositoryfiles,substr($_,rindex($_,"/")+1)) if (!-d);
		}
	}

	if ((($filtersettings{'ENABLE_REWRITE'} eq 'on') && (@repositoryfiles)) ||
	    ($filtersettings{'ENABLE_SAFESEARCH'} eq 'on')) {
		print FILE "rewrite rew-rule-1 {\n";

		if (($filtersettings{'ENABLE_REWRITE'} eq 'on') && (@repositoryfiles)) {
			print FILE "    # rewrite localfiles\n";
			foreach (@repositoryfiles) {
				print FILE "    s@.*/$_\$\@http://$netsettings{'GREEN_ADDRESS'}:$http_port/repository/$_\@i\n";
			}
		}

		if ($filtersettings{'ENABLE_SAFESEARCH'} eq 'on') {
			print FILE "    # rewrite safesearch\n";
			print FILE "    s@(.*\\Wgoogle\\.\\w+/(webhp|search|imghp|images|grphp|groups|frghp|froogle)\\?)(.*)(\\bsafe=\\w+)(.*)\@\\1\\3safe=strict\\5\@i\n";
			print FILE "    s@(.*\\Wgoogle\\.\\w+/(webhp|search|imghp|images|grphp|groups|frghp|froogle)\\?)(.*)\@\\1safe=strict\\\&\\3\@i\n";
			print FILE "    s@(.*\\Wsearch\\.yahoo\\.\\w+/search\\W)(.*)(\\bvm=\\w+)(.*)\@\\1\\2vm=r\\4\@i\n";
			print FILE "    s@(.*\\Wsearch\\.yahoo\\.\\w+/search\\W.*)\@\\1\\\&vm=r\@i\n";
			print FILE "    s@(.*\\Walltheweb\\.com/customize\\?)(.*)(\\bcopt_offensive=\\w+)(.*)\@\\1\\2copt_offensive=on\\4\@i\n";
		}

		print FILE "}\n\n";

		if ((!($filtersettings{'UNFILTERED_CLIENTS'} eq '')) &&
		    ($filtersettings{'ENABLE_SAFESEARCH'} eq 'on')) {
			print FILE "rewrite rew-rule-2 {\n";
			if (($filtersettings{'ENABLE_REWRITE'} eq 'on') && (@repositoryfiles)) {
				print FILE "    # rewrite localfiles\n";

				foreach (@repositoryfiles) {
					print FILE "    s@.*/$_\$\@http://$netsettings{'GREEN_ADDRESS'}:$http_port/repository/$_\@i\n";
				}
			}
			else {
				print FILE "    # rewrite nothing\n";
			}
			print FILE "}\n\n";
		}
	}

	if (!($filtersettings{'UNFILTERED_CLIENTS'} eq '')) {
		print FILE "src unfiltered {\n";
		print FILE "    ip $filtersettings{'UNFILTERED_CLIENTS'}\n";
		print FILE "}\n\n";
	}

	if (!($filtersettings{'BANNED_CLIENTS'} eq '')) {
		print FILE "src banned {\n";
		print FILE "    ip $filtersettings{'BANNED_CLIENTS'}\n";

		if ($filtersettings{'ENABLE_LOG'} eq 'on') {
			if ($filtersettings{'ENABLE_CATEGORY_LOG'} eq 'on') {
				print FILE "    logfile       ".$ident." banned.log\n";
			}
			else {
				print FILE "    logfile       ".$ident." urlfilter.log\n";
			}
		}
		print FILE "}\n\n";
	}

	if (-e $uqfile) {
		open(UQ, $uqfile);
		@uqlist = <UQ>;
		close(UQ);

		if (@uqlist > 0) {
			$idx=0;
			foreach (@uqlist) {
				chomp;
				@uq = split(/\,/);
				if ($uq[4] eq 'on') {
					$idx++;
					$uq[0] = $uq[0] * 60;
					if ($uq[1] eq '0') {
						$uq[1] = 3600 if ($uq[2] eq 'hourly');
						$uq[1] = 86400 if ($uq[2] eq 'daily');
						$uq[1] = 604800 if ($uq[2] eq 'weekly');
					}
					$uq[3] =~ s/\|/ /g;
					print FILE "src quota-$idx {\n";
					print FILE "    user $uq[3]\n";
					print FILE "    userquota $uq[0] $uq[1] $uq[2]\n";
					print FILE "}\n\n";
				}
			}

		}
	}

	@tclist = &aggregatedconstraints;

	if (@tclist > 0) {
		$idx=0;
		foreach (@tclist) {
			chomp;
			@tc = split(/\,/);
			if ($tc[15] eq 'on') {
				$idx++;
				print FILE "src network-$idx {\n";
				@clients = split(/ /,$tc[12]);
				@temp = split(/-/,$clients[0]);
				if ( (&validipormask($temp[0])) || (&validipandmask($temp[0]))) {
					print FILE "    ip $tc[12]\n";
				}
				else {
					print FILE "    user";
					@clients = split(/ /,$tc[12]);
					foreach $line (@clients) {
						$line =~ s/(^\w+)\\(\w+$)/$1%5c$2/;
						print FILE " $line";
					}
					print FILE "\n";
				}

				if (($filtersettings{'ENABLE_LOG'} eq 'on') && ($tc[14] eq 'block') && ($tc[13] eq 'any')) {
					if ($filtersettings{'ENABLE_CATEGORY_LOG'} eq 'on') {
						print FILE "    logfile       ".$ident." timeconst.log\n";
					}
					else {
						print FILE "    logfile       ".$ident." urlfilter.log\n";
					}
				}
				print FILE "}\n\n";
			}
		}

		$idx=0;
		foreach (@tclist) {
			chomp;
			@tc = split(/\,/);
			if ($tc[15] eq 'on') {
				$idx++;
				print FILE "time constraint-$idx {\n";
				print FILE "$tc[16]\n";
				print FILE "}\n\n";
			}
		}
	}

	foreach $category (@categories) {
		$blacklist = $category;
		$category =~ s/\//_/g;
		print FILE "dest $category {\n";

		if (-e "$dbdir/$blacklist/domains") {
			print FILE "    domainlist     $blacklist/domains\n";
		}
		if (-e "$dbdir/$blacklist/urls") {
			print FILE "    urllist        $blacklist/urls\n";
		}
		if ((-e "$dbdir/$blacklist/expressions") &&
		    ($filtersettings{'ENABLE_EXPR_LISTS'} eq 'on')) {
			print FILE "    expressionlist $blacklist/expressions\n";
		}
		if ((($category eq 'ads') || ($category eq 'adv')) &&
		    ($filtersettings{'ENABLE_EMPTY_ADS'} eq 'on')) {
			print FILE "    redirect       http://$netsettings{'GREEN_ADDRESS'}:$http_port/ui/img/urlfilter/1x1.gif\n";
		}
		if ($filtersettings{'ENABLE_LOG'} eq 'on') {
			if ($filtersettings{'ENABLE_CATEGORY_LOG'} eq 'on') {
				print FILE "    logfile       $ident $category.log\n";
			}
			else {
				print FILE "    logfile       $ident urlfilter.log\n";
			}
		}
		print FILE "}\n\n";
		$category = $blacklist;
	}
	
	print FILE "dest files {\n";
	print FILE "    expressionlist custom/blocked/files\n";

	if ($filtersettings{'ENABLE_LOG'} eq 'on') {
		if ($filtersettings{'ENABLE_CATEGORY_LOG'} eq 'on') {
			print FILE "    logfile       $ident files.log\n";
		}
		else {
			print FILE "    logfile       $ident urlfilter.log\n";
		}
	}
	print FILE "}\n\n";

	print FILE "dest custom-allowed {\n";
	print FILE "    domainlist     custom/allowed/domains\n";
	print FILE "    urllist        custom/allowed/urls\n";
	print FILE "}\n\n";

	print FILE "dest custom-blocked {\n";
	print FILE "    domainlist     custom/blocked/domains\n";
	print FILE "    urllist        custom/blocked/urls\n";

	if ($filtersettings{'ENABLE_LOG'} eq 'on') {
		if ($filtersettings{'ENABLE_CATEGORY_LOG'} eq 'on') {
			print FILE "    logfile       $ident custom.log\n";
		}
		else {
			print FILE "    logfile       $ident urlfilter.log\n";
		}
	}
	print FILE "}\n\n";

	print FILE "dest custom-expressions {\n";
	print FILE "    expressionlist custom/blocked/expressions\n";
	if ($filtersettings{'ENABLE_LOG'} eq 'on') {
		if ($filtersettings{'ENABLE_CATEGORY_LOG'} eq 'on') {
			print FILE "    logfile       $ident custom.log\n";
		}
		else {
			print FILE "    logfile       $ident urlfilter.log\n";
		}
	}
	print FILE "}\n\n";

	print FILE "acl {\n";
	if (!($filtersettings{'UNFILTERED_CLIENTS'} eq '')) {
		print FILE "    unfiltered {\n";
		print FILE "        pass all\n";

		if ($filtersettings{'ENABLE_SAFESEARCH'} eq 'on') {
			print FILE "        rewrite rew-rule-2\n";
		}
		print FILE "    }\n\n";
	}

	if (!($filtersettings{'BANNED_CLIENTS'} eq '')) {
		print FILE "    banned {\n";
		print FILE "        pass ";

		if (($filtersettings{'ENABLE_CUSTOM_WHITELIST'} eq 'on') && ($filtersettings{'ENABLE_GLOBAL_WHITELIST'} eq 'on')) {
			print FILE "custom-allowed ";
		}
		print FILE "none\n";
		print FILE "    }\n\n";
	}

	if (-s $uqfile) {
		open(UQ, $uqfile);
		@uqlist = <UQ>;
		close(UQ);

		$idx=0;
		foreach (@uqlist) {
			chomp;
			@uq = split(/\,/);
			if ($uq[4] eq 'on') {
				$idx++;
				$qredirect = $redirect;
				$qredirect =~ s/\%t/\%q\%20-\%20\%i/;
				print FILE "    quota-$idx {\n";
				print FILE "        pass ";
				if (($filtersettings{'ENABLE_CUSTOM_WHITELIST'} eq 'on') &&
				    ($filtersettings{'ENABLE_GLOBAL_WHITELIST'} eq 'on')) {
					print FILE "custom-allowed ";
				}
				print FILE "none\n";
				unless ($redirect eq $qredirect) {
					print FILE "        redirect $qredirect\n";
				}
				print FILE "    }\n\n";
			}
		}
	}

	if (@tclist > 0) {
		$idx=0;
		foreach (@tclist) {
			chomp;
			@tc = split(/\,/);
			@ec = split(/\|/,$tc[13]);

			foreach (@ec) { s/\//_/g; }
			if ($tc[15] eq 'on') {
				$idx++;
				print FILE "    network-$idx $tc[0] constraint-$idx {\n";
				print FILE "        pass ";

				if ($filtersettings{'BLOCK_ALL'} eq 'on') {
					if ($tc[14] eq 'block') {
						if ((@ec == 1) && ($ec[0] eq 'any')) {
							if (($filtersettings{'ENABLE_CUSTOM_WHITELIST'} eq 'on') &&
							    ($filtersettings{'ENABLE_GLOBAL_WHITELIST'} eq 'on')) {
								print FILE "custom-allowed ";
							}
							print FILE "none";
						}
						else {
							print FILE $defaultrule;
						}
					}
					else {
						foreach (@ec) {
							print FILE "$_ ";
						}
						print FILE $defaultrule unless ((@ec == 1) && ($ec[0] eq 'any'));
					}
				}
				else {
					if ($tc[14] eq 'block') {
						$tcrule = $defaultrule;
						if ($filtersettings{'ENABLE_CUSTOM_WHITELIST'} eq 'on') {
							$tcrule =~ s/custom-allowed //;
							print FILE "custom-allowed " unless ((@ec == 1) &&
								($ec[0] eq 'any') &&
								($filtersettings{'ENABLE_GLOBAL_WHITELIST'} eq 'off'));
						}
						if ((@ec == 1) && ($ec[0] eq 'any')) {
							print FILE "none";
						}
						else {
							foreach (@ec) {
								print FILE "!$_ " unless (index($defaultrule,"!".$_." ") ge 0);
							}
						}
						print FILE $tcrule unless ((@ec == 1) && ($ec[0] eq 'any'));
					}
					else {
						$tcrule = $defaultrule;
						if ((@ec == 1) && ($ec[0] eq 'any')) {
							print FILE "any";
						}
						else {
							foreach (@ec) {
								$tcrule = "$_ ".$tcrule unless (index($defaultrule,"!".$_." ") ge 0);
								$tcrule =~ s/!$_ //;
							}
							print FILE $tcrule;
						}
					}
				}
				print FILE "\n";
				print FILE "    }\n\n";
			}
		}
	}

	print FILE "    default {\n";
	print FILE "        pass $defaultrule\n";
	if (($filtersettings{'ENABLE_LOG'} eq 'on') && ($filtersettings{'BLOCK_ALL'} eq 'on')) {
		if ($filtersettings{'ENABLE_CATEGORY_LOG'} eq 'on') {
			print FILE "        logfile".$ident." default.log\n";
		}
		else {
			print FILE "        logfile".$ident." urlfilter.log\n";
		}
	}
	if ((($filtersettings{'ENABLE_REWRITE'} eq 'on') && (@repositoryfiles)) ||
	    ($filtersettings{'ENABLE_SAFESEARCH'} eq 'on')) {
		print FILE "        rewrite rew-rule-1\n";
	}
	print FILE "        redirect $redirect\n";
	print FILE "    }\n";
	print FILE "}\n";

	close FILE;
}

# -------------------------------------------------------------------
