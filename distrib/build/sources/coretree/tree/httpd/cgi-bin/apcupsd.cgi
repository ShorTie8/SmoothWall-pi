#!/usr/bin/perl
#
# SmoothWall CGIs
#
# (c) SmoothWall Ltd, 2005

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );
use strict;
use warnings;

my (%apcupsdsettings, %checked, %selected);
my $refresh = '';

sub validemailaddr() {
	my ($email) = @_;
	my $okaddr = 1;
	my ($tmpnam, $tmphst) = split ("@", $email);
	$okaddr = 0 if ($tmpnam !~ /[a-zA-Z0-9._+-]*/ );
	$okaddr = 0 if (! (&validhostname ($tmphst) or &validip($tmphst)));
	return $okaddr;
}

&showhttpheaders();

$apcupsdsettings{'ACTION'} = '';
$apcupsdsettings{'EMAIL'} = '';
$apcupsdsettings{'ANNOY'} = '300';
$apcupsdsettings{'BATTDELAY'} = '10';
$apcupsdsettings{'BATTLEVEL'} = '15';
$apcupsdsettings{'CC'} = '';
$apcupsdsettings{'SMSEMAIL'} = '';
$apcupsdsettings{'ENABLE'} = 'off';
$apcupsdsettings{'ENABLEALERTS'} = 'off';
$apcupsdsettings{'FROM'} = '';
$apcupsdsettings{'KILLPOWER'} = 'off';
$apcupsdsettings{'SMTPSERVER'} = '';
$apcupsdsettings{'MSGANNOY'} = 'off';
$apcupsdsettings{'MSGBATTATTACH'} = 'off';
$apcupsdsettings{'MSGBATTDETACH'} = 'off';
$apcupsdsettings{'MSGCHANGEME'} = 'off';
$apcupsdsettings{'MSGCOMMFAILURE'} = 'off';
$apcupsdsettings{'MSGCOMMOK'} = 'off';
$apcupsdsettings{'MSGDOSHUTDOWN'} = 'off';
$apcupsdsettings{'MSGEMERGENCY'} = 'off';
$apcupsdsettings{'MSGENDSELFTEST'} = 'off';
$apcupsdsettings{'MSGFAILING'} = 'off';
$apcupsdsettings{'MSGKILLPOWER'} = 'off';
$apcupsdsettings{'MSGLOADLIMIT'} = 'off';
$apcupsdsettings{'MSGOFFBATTERY'} = 'off';
$apcupsdsettings{'MSGONBATTERY'} = 'off';
$apcupsdsettings{'MSGPOWERBACK'} = 'off';
$apcupsdsettings{'MSGPOWEROUT'} = 'off';
$apcupsdsettings{'MSGREMOTEDOWN'} = 'off';
$apcupsdsettings{'MSGRUNLIMIT'} = 'off';
$apcupsdsettings{'MSGSTARTSELFTEST'} = 'off';
$apcupsdsettings{'MSGTIMEOUT'} = 'off';
$apcupsdsettings{'NISPORT'} = '3551';
$apcupsdsettings{'POLLTIME'} = '60';
$apcupsdsettings{'RTMIN'} = '10';
$apcupsdsettings{'STANDALONE'} = '';
$apcupsdsettings{'TESTING'} = 'off';
$apcupsdsettings{'TO'} = '0';
$apcupsdsettings{'UPSAUTH'} = '';
$apcupsdsettings{'UPSIP'} = '';
$apcupsdsettings{'UPSMODE'} = '';
$apcupsdsettings{'UPSNAME'} = '';
$apcupsdsettings{'UPSPORT'} = '';
$apcupsdsettings{'UPSUSER'} = '';
$apcupsdsettings{'VALID'} = '';
$apcupsdsettings{'PORT'} = 25;
$apcupsdsettings{'ENABLEAUTH'} = '';
$apcupsdsettings{'SMTPS'} = '';
$apcupsdsettings{'STARTTLS'} = '';
$apcupsdsettings{'USER'} = '';
$apcupsdsettings{'EMAIL_PASSWORD'} = '';

&getcgihash(\%apcupsdsettings);

my $errormessage = '';
my $infomessage = '';

if ($apcupsdsettings{'ACTION'} eq $tr{'save and restart'}) {
	# First, validate all entry fields for blank or valid content
	if ($apcupsdsettings{'EMAIL'} ne "" and ! &validemailaddr($apcupsdsettings{'EMAIL'})) {
		$errormessage .= $tr{"apc invalid alert addr"} ."<br />";
	}
	if ($apcupsdsettings{'ANNOY'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid annoy time"} ."<br />";
	}
	if ($apcupsdsettings{'BATTDELAY'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid batt delay"} ."<br />";
	}
	if ($apcupsdsettings{'BATTLEVEL'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid batt level"} ."<br />";
	}
	if ($apcupsdsettings{'CC'} ne "" and ! &validemailaddr($apcupsdsettings{'CC'})) {
		$errormessage .= $tr{"apc invalid cc1 addr"} ."<br />";
	}
	if ($apcupsdsettings{'SMSEMAIL'} ne "" and ! &validemailaddr($apcupsdsettings{'SMSEMAIL'})) {
		$errormessage .= $tr{"apc invalid cc2 addr"} ."<br />";
	}
	if ($apcupsdsettings{'FROM'} ne "" and ! &validemailaddr($apcupsdsettings{'FROM'})) {
		$errormessage .= $tr{"apc invalid from addr"} ."<br />";
	}
	if ($apcupsdsettings{'SMTPSERVER'} ne "" and !&validip($apcupsdsettings{'SMTPSERVER'}) and 
	    ! &validhostname($apcupsdsettings{'SMTPSERVER'})) {
		$errormessage .= $tr{"apc invalid svr addr"} ."<br />";
	}
	if ($apcupsdsettings{'NISPORT'} ne "" and not &validport($apcupsdsettings{'NISPORT'}) ) {
		$errormessage .= $tr{"apc invalid nis port"} ."<br />";
	}
	if ($apcupsdsettings{'POLLTIME'} ne "" and $apcupsdsettings{'POLLTIME'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid poll time"} ."<br />";
	}
	if ($apcupsdsettings{'RTMIN'} ne "" and $apcupsdsettings{'RTMIN'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid min runtime"} ."<br />";
	}
	if ($apcupsdsettings{'TO'} ne "" and $apcupsdsettings{'TO'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid time out"} ."<br />";
	}
	if ($apcupsdsettings{'UPSAUTH'} =~ /[<>]/ ) {
		$errormessage .= $tr{"apc invalid password"} ."<br />";
	}

	my ($tmphost, $tmpport) = split(":",$apcupsdsettings{'UPSIP'});
	if (($tmphost) and not &validip($tmphost) and not &validhostname($tmphost)) {
		$errormessage .= $tr{"apc invalid ups ip host"} ."<br />";
	}
	if (($tmpport) and not &validport($tmpport)) {
		$errormessage .= $tr{"apc invalid ups ip port"} ."<br />";
	}
	if ($apcupsdsettings{'UPSMODE'} ne "" and $apcupsdsettings{'UPSMODE'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid ups mode"} ."<br />";
	}
	if ($apcupsdsettings{'UPSNAME'} =~ /[<>]/ ) {
		$errormessage .= $tr{"apc invalid ups name"} ."<br />";
	}

	if ($apcupsdsettings{'UPSPORT'} ne "" and 
	    $apcupsdsettings{'UPSPORT'} !~ /\/dev\/ttyS[0-9]+/ and
	    $apcupsdsettings{'UPSPORT'} !~ /\/dev\/ttyUSB[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid serial port"} ."<br />";
	}
	if ($apcupsdsettings{'UPSUSER'} =~ /[<>]/ ) {
		$errormessage .= $tr{"apc invalid username"} ."<br />";
	}


	# Now warn when things don't quite line up
	if ((($apcupsdsettings{'UPSMODE'} eq '0')
	  or ($apcupsdsettings{'UPSMODE'} eq '1')
	  or ($apcupsdsettings{'UPSMODE'} eq '2')
	  or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '5')) && ($apcupsdsettings{'TO'}) ne '0') {
		$errormessage .= $tr{"Pls Leave Shutdown After Time on Batt"} .'<br />';     
	}

	if  ((($apcupsdsettings{'UPSMODE'} eq '1') or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '5')) && ($apcupsdsettings{'UPSPORT'}) ne '' ) {
		$errormessage .= $tr{"Pls Leave Serial Blank USB PC"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '5' && (!(&validip($apcupsdsettings{'UPSIP'})))) {
		$errormessage .= $tr{"invalid ups IP"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '5' && $apcupsdsettings{'UPSUSER'} eq '' ) {
		$errormessage .= $tr{"Pls Enter Username"} .'<br />';
	}
        
	if ($apcupsdsettings{'UPSMODE'} eq '5' && $apcupsdsettings{'UPSAUTH'} eq '' ) {
		$errormessage .= $tr{"Pls Enter Password"} .'<br />';
	}

	if (($apcupsdsettings{'UPSMODE'} eq '0')
	 or ($apcupsdsettings{'UPSMODE'} eq '2')
	 or ($apcupsdsettings{'UPSMODE'} eq '6')
	 or ($apcupsdsettings{'UPSMODE'} eq '7')
	 or ($apcupsdsettings{'UPSMODE'} eq '8')
	 or ($apcupsdsettings{'UPSMODE'} eq '9')
	 or ($apcupsdsettings{'UPSMODE'} eq '10')
	 or ($apcupsdsettings{'UPSMODE'} eq '11')
	 or ($apcupsdsettings{'UPSMODE'} eq '12')
	 or ($apcupsdsettings{'UPSMODE'} eq '13')
	 or ($apcupsdsettings{'UPSMODE'} eq '14')
	 or ($apcupsdsettings{'UPSMODE'} eq '15')
	 or ($apcupsdsettings{'UPSMODE'} eq '16')
	 or ($apcupsdsettings{'UPSMODE'} eq '17')
	 or ($apcupsdsettings{'UPSMODE'} eq '18')) {
		unless ($apcupsdsettings{'UPSPORT'} =~ /^\/dev\/tty[A-Z][0-9]/ ) {
			$errormessage .= $tr{"Pls Enter Serial Port"} .'<br />';
		}
	}

	if ((($apcupsdsettings{'UPSMODE'} eq '6')
	  or ($apcupsdsettings{'UPSMODE'} eq '7')
	  or ($apcupsdsettings{'UPSMODE'} eq '8')
	  or ($apcupsdsettings{'UPSMODE'} eq '9')
	  or ($apcupsdsettings{'UPSMODE'} eq '10')
	  or ($apcupsdsettings{'UPSMODE'} eq '11')
	  or ($apcupsdsettings{'UPSMODE'} eq '12')
	  or ($apcupsdsettings{'UPSMODE'} eq '13')
	  or ($apcupsdsettings{'UPSMODE'} eq '14')
	  or ($apcupsdsettings{'UPSMODE'} eq '15')
	  or ($apcupsdsettings{'UPSMODE'} eq '16')
	  or ($apcupsdsettings{'UPSMODE'} eq '17')
	  or ($apcupsdsettings{'UPSMODE'} eq '18')) && ($apcupsdsettings{'TO'}) <= '119') {
		$errormessage .= $tr{"Pls Select Shutdown Time SimpleSig"} .'<br />';
	}

	if ((($apcupsdsettings{'UPSMODE'} eq '0')
	  or ($apcupsdsettings{'UPSMODE'} eq '1')
	  or ($apcupsdsettings{'UPSMODE'} eq '2')
	  or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '6')
	  or ($apcupsdsettings{'UPSMODE'} eq '7')
	  or ($apcupsdsettings{'UPSMODE'} eq '8')
	  or ($apcupsdsettings{'UPSMODE'} eq '9')
	  or ($apcupsdsettings{'UPSMODE'} eq '10')
	  or ($apcupsdsettings{'UPSMODE'} eq '11')
	  or ($apcupsdsettings{'UPSMODE'} eq '12')
	  or ($apcupsdsettings{'UPSMODE'} eq '13')
	  or ($apcupsdsettings{'UPSMODE'} eq '14')
	  or ($apcupsdsettings{'UPSMODE'} eq '15')
	  or ($apcupsdsettings{'UPSMODE'} eq '16')
	  or ($apcupsdsettings{'UPSMODE'} eq '17')
	  or ($apcupsdsettings{'UPSMODE'} eq '18')) && ($apcupsdsettings{'UPSIP'}) ne '') {
		$errormessage .= $tr{"Pls Leave IP Blank"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} ne '5' && $apcupsdsettings{'UPSUSER'} ne '' ) {
		$errormessage .= $tr{"Username Not Required"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} ne '5' && $apcupsdsettings{'UPSAUTH'} ne '' ) {
		$errormessage .= $tr{"Password Not Required"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'UPSPORT'}) ne '' ) {
		$errormessage .= $tr{"Pls Leave Serial Blank Slave"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'KILLPOWER'}) eq 'on') {
		$errormessage .= $tr{"UPS Killpower Incompatible Slave"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'UPSIP'}) eq '') {
		$errormessage .= $tr{"Pls Enter IP"} .'<br />';
	}

	if ($apcupsdsettings{'POLLTIME'} >= 301 || $apcupsdsettings{'POLLTIME'} <= 19 ) {
		$errormessage .= 'Invalid Poll time, enter a value between 20 and 300<br />';
	}

	# Don't validate email addrs, etc., if notifications are not enabled
	if ($apcupsdsettings{'ENABLEALERTS'} eq 'on') {
		if (! &validemailaddr($apcupsdsettings{'FROM'})) {
			$errormessage .= 'Please enter a valid From address<br />';
		}
	
		if (! &validemailaddr($apcupsdsettings{'EMAIL'})) {
			$errormessage .= 'Please enter a valid Alert To<br />';
		}
	
		if ($apcupsdsettings{'CC'} ne '') {
			unless ($apcupsdsettings{'CC'} =~ (/^[A-z0-9_\-\.]+[@][A-z0-9_\-.]+[A-z]{2,}$/)) {
				$errormessage .= 'Please enter a valid And To address<br />';
			}
		}
	
		if ($apcupsdsettings{'SMSEMAIL'} ne '') {
			unless ($apcupsdsettings{'SMSEMAIL'} =~ (/^[A-z0-9_\-\.]+[@][A-z0-9_\-.]+[A-z]{2,}$/)) {
				$errormessage .= 'Please enter a valid SMSemail address<br />';
		 	}
		}
	
		if ($apcupsdsettings{'SMTPSERVER'} eq '') {
			$errormessage .= 'Please enter valid mailserver<br />';
		}
	}

	if ($apcupsdsettings{'BATTLEVEL'} >= 96 || $apcupsdsettings{'BATTLEVEL'} <= 4 ) {
		$errormessage .= 'Please enter % of battery remaining between 5 and 95<br />';
	}

	if ($apcupsdsettings{'BATTDELAY'} >= 301 || $apcupsdsettings{'BATTDELAY'} <= -1 ) {
		$errormessage .= 'Invalid on battery response delay, enter a value between 0 and 300<br />';
	}

	if ($apcupsdsettings{'RTMIN'} <= 4 ) {
		$errormessage .= 'Invalid minimum runtime, enter a value of 5 or greater<br />';
	}

	if (length $apcupsdsettings{'UPSNAME'} > 8) {
		$errormessage .= 'Please use 8 characters or less for UPS name<br />';
	}

	if ($apcupsdsettings{'ANNOY'} eq '') {
		$errormessage .= 'Please enter Annoy Message Period<BR>Default is 300 Seconds<br />';
	}

ERROR:
	if ($errormessage) {
                $apcupsdsettings{'VALID'} = 'no'; }		
	else {
                $apcupsdsettings{'VALID'} = 'yes';
	}

	if ($apcupsdsettings{'VALID'} eq 'yes') {
		
		&log("APCupsd service restarted.");
	
		&writehash("/var/smoothwall/apcupsd/settings", \%apcupsdsettings);
		
		my $success = message("apcupsdwrite");
		$infomessage = $success."<br />" if ($success);
		$errormessage = "apcupsdwrite ".$tr{'smoothd failure'}."<br />" unless ($success);

		if ($apcupsdsettings{'ENABLE'} eq 'on') {
			$success = message("apcupsdrestart");
			$infomessage .= $success."<br />" if ($success);
			$errormessage .= "apcupsdrestart ".$tr{'smoothd failure'}."<br />" unless ($success);
		}
		else {
			$success = message("apcupsdstop");
			$infomessage .= $success."<br />" if ($success);
			$errormessage .= "apcupsdstop ".$tr{'smoothd failure'}."<br />" unless ($success);
		}
	}
}

if ($apcupsdsettings{'ACTION'} eq '' ) {
	$apcupsdsettings{'ENABLE'} = 'off';
	$apcupsdsettings{'NOLOGINTYPE'} = '0';
	$apcupsdsettings{'OPMODE'} = 'testing';

	if (-e "/var/smoothwall/apcupsd/settings") {
		&readhash("/var/smoothwall/apcupsd/settings", \%apcupsdsettings);
	}
}

if ($apcupsdsettings{'ACTION'} eq $tr{'restart'}) {
	&log("APCupsd service restarted.");

	if ($apcupsdsettings{'ENABLE'} eq 'on') {
		my $success = message("apcupsdrestart");
		$infomessage .= $success."<br />" if ($success);
		$errormessage .= "apcupsdrestart ".$tr{'smoothd failure'}."<br />" unless ($success);
	}
	else {
		$errormessage .= "Not Enabled!<br />";
	}
}

if ($apcupsdsettings{'ACTION'} eq $tr{'stop'}) {
	&log("APCupsd service stopped.");

	my $success = message("apcupsdstop");
	$infomessage = $success if ($success);
	$errormessage = "apcupsdstop ".$tr{'smoothd failure'} unless ($success);
}

if ($apcupsdsettings{'ACTION'} eq $tr{'mail-test'}) {
	system ("/usr/bin/smoothwall/upsd-notify.pl", "APCUPSD Test Message.");
	if (-e "/dev/shm/upsd-notify_failed") {
		$errormessage = $tr{'unsuccesful mail'};
		unlink ("/dev/shm/upsd-notify_failed");
	}
	&readhash("/var/smoothwall/apcupsd/settings", \%apcupsdsettings);
}

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$apcupsdsettings{'ENABLE'}} = 'CHECKED';

$checked{'ENABLEALERTS'}{'off'} = '';
$checked{'ENABLEALERTS'}{'on'} = '';
$checked{'ENABLEALERTS'}{$apcupsdsettings{'ENABLEALERTS'}} = 'CHECKED';

$selected{'OPMODE'}{'testing'} = '';
$selected{'OPMODE'}{'full'} = '';
$selected{'OPMODE'}{$apcupsdsettings{'OPMODE'}} = 'SELECTED';

$checked{'STANDALONE'}{'off'} = '';
$checked{'STANDALONE'}{'on'} = '';
$checked{'STANDALONE'}{$apcupsdsettings{'STANDALONE'}} = 'CHECKED';

$checked{'KILLPOWER'}{'off'} = '';
$checked{'KILLPOWER'}{'on'} = '';
$checked{'KILLPOWER'}{$apcupsdsettings{'KILLPOWER'}} = 'CHECKED';

$selected{'UPSMODE'}{'0'} = '';
$selected{'UPSMODE'}{'1'} = '';
$selected{'UPSMODE'}{'2'} = '';
$selected{'UPSMODE'}{'3'} = '';
$selected{'UPSMODE'}{'4'} = '';
$selected{'UPSMODE'}{'5'} = '';
$selected{'UPSMODE'}{'6'} = '';
$selected{'UPSMODE'}{'7'} = '';
$selected{'UPSMODE'}{'8'} = '';
$selected{'UPSMODE'}{'9'} = '';
$selected{'UPSMODE'}{'10'} = '';
$selected{'UPSMODE'}{'11'} = '';
$selected{'UPSMODE'}{'12'} = '';
$selected{'UPSMODE'}{'13'} = '';
$selected{'UPSMODE'}{'14'} = '';
$selected{'UPSMODE'}{'15'} = '';
$selected{'UPSMODE'}{'16'} = '';
$selected{'UPSMODE'}{'17'} = '';
$selected{'UPSMODE'}{'18'} = '';
$selected{'UPSMODE'}{$apcupsdsettings{'UPSMODE'}} = 'SELECTED';

$selected{'NOLOGINTYPE'}{'0'} = '';
$selected{'NOLOGINTYPE'}{'1'} = '';
$selected{'NOLOGINTYPE'}{'2'} = '';
$selected{'NOLOGINTYPE'}{'3'} = '';
$selected{'NOLOGINTYPE'}{$apcupsdsettings{'NOLOGINTYPE'}} = 'SELECTED';

$checked{'MSGPOWEROUT'}{'off'} = '';
$checked{'MSGPOWEROUT'}{'on'} = '';
$checked{'MSGPOWEROUT'}{$apcupsdsettings{'MSGPOWEROUT'}} = 'CHECKED';

$checked{'MSGPOWERBACK'}{'off'} = '';
$checked{'MSGPOWERBACK'}{'on'} = '';
$checked{'MSGPOWERBACK'}{$apcupsdsettings{'MSGPOWERBACK'}} = 'CHECKED';

$checked{'MSGKILLPOWER'}{'off'} = '';
$checked{'MSGKILLPOWER'}{'on'} = '';
$checked{'MSGKILLPOWER'}{$apcupsdsettings{'MSGKILLPOWER'}} = 'CHECKED';

$checked{'MSGEMERGENCY'}{'off'} = '';
$checked{'MSGEMERGENCY'}{'on'} = '';
$checked{'MSGEMERGENCY'}{$apcupsdsettings{'MSGEMERGENCY'}} = 'CHECKED';

$checked{'MSGCHANGEME'}{'off'} = '';
$checked{'MSGCHANGEME'}{'on'} = '';
$checked{'MSGCHANGEME'}{$apcupsdsettings{'MSGCHANGEME'}} = 'CHECKED';

$checked{'MSGFAILING'}{'off'} = '';
$checked{'MSGFAILING'}{'on'} = '';
$checked{'MSGFAILING'}{$apcupsdsettings{'MSGFAILING'}} = 'CHECKED';

$checked{'MSGANNOY'}{'off'} = '';
$checked{'MSGANNOY'}{'on'} = '';
$checked{'MSGANNOY'}{$apcupsdsettings{'MSGANNOY'}} = 'CHECKED';

$checked{'MSGCOMMFAILURE'}{'off'} = '';
$checked{'MSGCOMMFAILURE'}{'on'} = '';
$checked{'MSGCOMMFAILURE'}{$apcupsdsettings{'MSGCOMMFAILURE'}} = 'CHECKED';

$checked{'MSGCOMMOK'}{'off'} = '';
$checked{'MSGCOMMOK'}{'on'} = '';
$checked{'MSGCOMMOK'}{$apcupsdsettings{'MSGCOMMOK'}} = 'CHECKED';

$checked{'MSGONBATTERY'}{'off'} = '';
$checked{'MSGONBATTERY'}{'on'} = '';
$checked{'MSGONBATTERY'}{$apcupsdsettings{'MSGONBATTERY'}} = 'CHECKED';

$checked{'MSGOFFBATTERY'}{'off'} = '';
$checked{'MSGOFFBATTERY'}{'on'} = '';
$checked{'MSGOFFBATTERY'}{$apcupsdsettings{'MSGOFFBATTERY'}} = 'CHECKED';

$checked{'MSGTIMEOUT'}{'off'} = '';
$checked{'MSGTIMEOUT'}{'on'} = '';
$checked{'MSGTIMEOUT'}{$apcupsdsettings{'MSGTIMEOUT'}} = 'CHECKED';

$checked{'MSGLOADLIMIT'}{'off'} = '';
$checked{'MSGLOADLIMIT'}{'on'} = '';
$checked{'MSGLOADLIMIT'}{$apcupsdsettings{'MSGLOADLIMIT'}} = 'CHECKED';

$checked{'MSGRUNLIMIT'}{'off'} = '';
$checked{'MSGRUNLIMIT'}{'on'} = '';
$checked{'MSGRUNLIMIT'}{$apcupsdsettings{'MSGRUNLIMIT'}} = 'CHECKED';

$checked{'MSGDOSHUTDOWN'}{'off'} = '';
$checked{'MSGDOSHUTDOWN'}{'on'} = '';
$checked{'MSGDOSHUTDOWN'}{$apcupsdsettings{'MSGDOSHUTDOWN'}} = 'CHECKED';

$checked{'MSGREMOTEDOWN'}{'off'} = '';
$checked{'MSGREMOTEDOWN'}{'on'} = '';
$checked{'MSGREMOTEDOWN'}{$apcupsdsettings{'MSGREMOTEDOWN'}} = 'CHECKED';

$checked{'MSGSTARTSELFTEST'}{'off'} = '';
$checked{'MSGSTARTSELFTEST'}{'on'} = '';
$checked{'MSGSTARTSELFTEST'}{$apcupsdsettings{'MSGSTARTSELFTEST'}} = 'CHECKED';

$checked{'MSGENDSELFTEST'}{'off'} = '';
$checked{'MSGENDSELFTEST'}{'on'} = '';
$checked{'MSGENDSELFTEST'}{$apcupsdsettings{'MSGENDSELFTEST'}} = 'CHECKED';

$checked{'MSGBATTATTACH'}{'off'} = '';
$checked{'MSGBATTATTACH'}{'on'} = '';
$checked{'MSGBATTATTACH'}{$apcupsdsettings{'MSGBATTATTACH'}} = 'CHECKED';

$checked{'MSGBATTDETACH'}{'off'} = '';
$checked{'MSGBATTDETACH'}{'on'} = '';
$checked{'MSGBATTDETACH'}{$apcupsdsettings{'MSGBATTDETACH'}} = 'CHECKED';

$checked{'ENABLEAUTH'}{'off'} = '';
$checked{'ENABLEAUTH'}{'on'} = '';
$checked{'ENABLEAUTH'}{$apcupsdsettings{'ENABLEAUTH'}} = 'CHECKED';

$checked{'SMTPS'}{'off'} = '';
$checked{'SMTPS'}{'on'} = '';
$checked{'SMTPS'}{$apcupsdsettings{'SMTPS'}} = 'CHECKED';

$checked{'STARTTLS'}{'off'} = '';
$checked{'STARTTLS'}{'on'} = '';
$checked{'STARTTLS'}{$apcupsdsettings{'STARTTLS'}} = 'CHECKED';

&openpage('apcupsd', 1, "$refresh", 'services');

print <<END
<form method='POST' action='?' name='myform'><div>

<script type="text/javascript">

function ffoxSelectUpdate(elmt)
{
    if(!document.all) elmt.style.cssText = elmt.options[elmt.selectedIndex].style.cssText;
}

function CheckAuth()
{
	if(document.myform.SMTPS.checked == true)
	{
	document.myform.ENABLEAUTH.checked = true;
	document.myform.STARTTLS.checked = false;
	document.myform.PORT.value = '465';
	document.myform.USER.disabled = false;
	document.myform.USER.style.backgroundColor = '#FFDDDD';
	document.myform.EMAIL_PASSWORD.disabled = false;
	document.myform.EMAIL_PASSWORD.style.backgroundColor = '#FFDDDD';
	}
	else
	{
	document.myform.PORT.value = '25';
	}
}

function UncheckSMTPS()
{
	if (document.myform.ENABLEAUTH.checked == false)
	{
	document.myform.SMTPS.checked = false;
	document.myform.STARTTLS.checked = false;
	document.myform.PORT.value = '25';
	document.myform.USER.disabled = true;
	document.myform.USER.style.backgroundColor = '';
	document.myform.EMAIL_PASSWORD.disabled = true;
	document.myform.EMAIL_PASSWORD.style.backgroundColor = '';
	}
	else
	{
	document.myform.USER.disabled = false;
	document.myform.USER.style.backgroundColor = '#FFDDDD';
	document.myform.EMAIL_PASSWORD.disabled = false;
	document.myform.EMAIL_PASSWORD.style.backgroundColor = '#FFDDDD';	
	}
}

function CheckSTARTTLS()
{
	if(document.myform.STARTTLS.checked == true)
	{
	document.myform.ENABLEAUTH.checked = true;
	document.myform.SMTPS.checked = false;
	document.myform.STARTTLS.checked = true;
	document.myform.PORT.value = '587';
	document.myform.USER.disabled = false;
	document.myform.USER.style.backgroundColor = '#FFDDDD';
	document.myform.EMAIL_PASSWORD.disabled = false;
	document.myform.EMAIL_PASSWORD.style.backgroundColor = '#FFDDDD';
	}
	else
	{
	document.myform.PORT.value = '25';
	}
}

</script>
END
;

&alertbox($errormessage, "", $infomessage);

&openbox('APCupsd:');

print <<END;
<table style='width: 100%; border: none; margin:1em auto 0 auto;'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'enabledc'}</td>
	<td><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td class='base' style='width: 25%;'>$tr{'Standalone UPS'}:</td>
	<td><input type='checkbox' name='STANDALONE' $checked{'STANDALONE'}{'on'}></td>
</tr>
<tr>
	<td></td>
	<td></td>
	<td class='base'>$tr{'Turn off UPS on shutdown'}:</td>
	<td><input type='checkbox' name='KILLPOWER' $checked{'KILLPOWER'}{'on'}></td>
</tr>
<tr>
	<td colspan="4">
END

&openbox("$tr{'Operation Mode'}:");

my $setcolor = '#000000';
$setcolor = '#b59d00' if ( $selected{'OPMODE'}{'testing'} eq 'SELECTED' );
$setcolor = 'green' if ( $selected{'OPMODE'}{'full'} eq 'SELECTED' );

print <<END;
<p style='margin:1em 1em .25em 2em;'><span style='color:#b59d00; font-weight:bold;'>$tr{'TESTING'}</span>
	$tr{'will simulate the response to a power failure; it will not shutdown Smoothwall or the UPS'}.</p>
<p style='margin:.25em 1em 0 2em;'><span style='color:green; font-weight:bold;'>$tr{'Full Operations'}</span>
	$tr{'will shutdown Smoothwall in response to a power failure'}.</p>
<p style='margin:.25em 1em 0 2em; font-style:italic;'>
	$tr{'Do NOT select Full Operations Mode until you know that your configuration is OK'}</p>
<p style='margin:1em 1em .5em 4em;'>$tr{'Modec'}
	<select name='OPMODE' style='color: $setcolor;' onchange='ffoxSelectUpdate(this);'>
	<option value='testing' $selected{'OPMODE'}{'testing'} style='color:#b59d00;'>$tr{'TESTING'}</option>
	<option value='full' $selected{'OPMODE'}{'full'} style='color: green;'>$tr{'Full Operations'}</option>
	</select></p>
END

&closebox();


print <<END;
	</td>
</tr>
</table>
END
;
&closebox();

&openbox("$tr{'On Battery Configurationc'}");

print <<END
<table style='width: 100%; border: none; margin:1em auto 0 auto;'>
<tr>
	<td class='base' style='width: 37%;'>$tr{'Shutdown when remaining capacity less than'}:</td>
	<td style='width: 13%;'><input type='text' style='width: 3em;' name='BATTLEVEL' value='$apcupsdsettings{'BATTLEVEL'}'> %</td>
	<td class='base' style='width: 37%;'>$tr{'Shutdown when remaining time less than'}:</td>
	<td style='width: 13%;'><input type='text' style='width: 3em;' name='RTMIN' value='$apcupsdsettings{'RTMIN'}'> $tr{'min.'}</td>
</tr>
<tr>
	<td class='base'>$tr{'Wait before responding to On Battery alert for'}:</td>
	<td><input type='text' style='width: 3em;' name='BATTDELAY' value='$apcupsdsettings{'BATTDELAY'}'> $tr{'sec.'}</td>
	<td class='base'>$tr{'Shutdown after on battery for'}:<span style='font-size:7pt;'> (0 $tr{'Disables'})</span></td>
	<td><input type='text' style='width: 3em;' name='TO' value='$apcupsdsettings{'TO'}'> $tr{'sec.'}</td>
</tr>
<tr>
	<td class='base'>$tr{'Deny Shell Login when on battery'}:</td>
	<td>
		<select name='NOLOGINTYPE'>
		<option value='0' $selected{'NOLOGINTYPE'}{'0'}>$tr{'Never'}
		<option value='1' $selected{'NOLOGINTYPE'}{'1'}>$tr{'Percent'}
		<option value='2' $selected{'NOLOGINTYPE'}{'2'}>$tr{'Minutes'}
		<option value='3' $selected{'NOLOGINTYPE'}{'3'}>$tr{'Always'}
		</select></td>
	<td class='base'>$tr{'Send annoy message every'}:</td>
	<td><input type='text' style='width: 3em;' name='ANNOY' value='$apcupsdsettings{'ANNOY'}'> $tr{'sec.'}</td>
</tr>
</table>
END
;

&closebox();

&openbox("$tr{'Communication Configurationc'}");

print <<END
<table style='width: 100%; border: none; margin:1em auto 0 auto;'>
<tr>
	<td class='base' style='width:20%;'>$tr{'UPS Type'}:</td>
	<td style='width:10%;'>
		<select name='UPSMODE'>
		<option value='0' $selected{'UPSMODE'}{'0'}>SmartUPS (Serial)
		<option value='1' $selected{'UPSMODE'}{'1'}>SmartUPS (USB)
		<option value='2' $selected{'UPSMODE'}{'2'}>Modbus &nbsp;&nbsp;(Serial)
		<option value='3' $selected{'UPSMODE'}{'3'}>Modbus &nbsp;&nbsp;(USB)
		<option value='4' $selected{'UPSMODE'}{'4'}>Ethernet (Slave)
		<option value='5' $selected{'UPSMODE'}{'5'}>PCNET &nbsp;&nbsp;&nbsp;(TCP/IP)
		<option value='6' $selected{'UPSMODE'}{'6'}>940-0020B $tr{'Cable'}
		<option value='7' $selected{'UPSMODE'}{'7'}>940-0020C $tr{'Cable'}
		<option value='8' $selected{'UPSMODE'}{'8'}>940-0023A $tr{'Cable'}
		<option value='9' $selected{'UPSMODE'}{'9'}>940-0024B $tr{'Cable'}
		<option value='10' $selected{'UPSMODE'}{'10'}>940-0024C $tr{'Cable'}
		<option value='11' $selected{'UPSMODE'}{'11'}>940-0024G $tr{'Cable'}
		<option value='12' $selected{'UPSMODE'}{'12'}>940-0095A $tr{'Cable'}
		<option value='13' $selected{'UPSMODE'}{'13'}>940-0095B $tr{'Cable'}
		<option value='14' $selected{'UPSMODE'}{'14'}>940-0095C $tr{'Cable'}
		<option value='15' $selected{'UPSMODE'}{'15'}>940-0119A $tr{'Cable'}
		<option value='16' $selected{'UPSMODE'}{'16'}>940-0127A $tr{'Cable'}
		<option value='17' $selected{'UPSMODE'}{'17'}>940-0128A $tr{'Cable'}
		<option value='18' $selected{'UPSMODE'}{'18'}>940-1524C $tr{'Cable'}
		</select>
	</td>
	<td class='base' style='width:25%;'>$tr{'Master Address or Hostname'}:<BR><sup>$tr{'Append'} <span style='color:red;'>:&lt;$tr{'port'}&gt;</span> $tr{'if not default'} (3551)</sup></td>
	<td style='width:20%;'><input type='text' name='UPSIP' value='$apcupsdsettings{'UPSIP'}'></td>
</tr>
<tr>
	<td class='base'>$tr{'UPS Name (8 Char Max.)'}:</td>
	<td><input type='text' maxlength='8' name='UPSNAME' style='width:8em;' value='$apcupsdsettings{'UPSNAME'}'></td>
	<td class='base'>$tr{'Serial Port'}:</td>
	<td><input type='text' name='UPSPORT' value='$apcupsdsettings{'UPSPORT'}'></td>
</tr>
<tr>
	<td class='base'>$tr{'Polling Interval'}:</td>
	<td><input type='text' name='POLLTIME' style='width: 3em;' value='$apcupsdsettings{'POLLTIME'}'></td>
	<td class='base'>$tr{'PCNET username'}:</td>
	<td><input type='text' name='UPSUSER' value='$apcupsdsettings{'UPSUSER'}'></td>
</tr>
<tr>
	<td class='base'>$tr{'Network server listen port'}:<span style='font-size:7pt;'><br />$tr{'Leave blank for default'}</span></td>
	<td><input type='text' maxlength='5' name='NISPORT' style='width: 3em;' value='$apcupsdsettings{'NISPORT'}'></td>
	<td class='base'>$tr{'PCNET password'}:</td>
	<td><input type='password' name='UPSAUTH' value='$apcupsdsettings{'UPSAUTH'}'></td>
</tr>
</table>
END
;

&closebox();

print <<END;

<table style='width: 100%; text-align:center; border: none; margin:1em auto;'>
<tr>
	<td style='width: 33%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'save and restart'}'></td>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'restart'}'></td>
	<td style='width: 33%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'stop'}'></td>
</tr>
</table>
END

&openbox("$tr{'Alerts Configurationc'}");

print <<END
<table style='width: 100%; border: none; margin:1em auto 0 auto;'>
<tr>
	<td class='base' style='width:20%;'>$tr{'Enable Alerts'}:</td>
	<td style='width:15%;'><input type='checkbox' name='ENABLEALERTS' $checked{'ENABLEALERTS'}{'on'}></td>
	<td class='base' style='width:30%;'></td>
	<td style='width:20%;'></td>
</tr>
<tr>
	<td class='base'>$tr{'Send Alerts To'}:</td>
	<td colspan='2'><input type='text' name='EMAIL' style='width: 220px;' value='$apcupsdsettings{'EMAIL'}'></td>
	<td class='base' style='width: 90px;'>$tr{'Send Alerts From'}:</td>
       <td colspan='2'><input type='text' name='FROM' style='width: 220px;' value='$apcupsdsettings{'FROM'}'></td>
</tr>
<tr>
	<td class='base'><IMG SRC='/ui/img/blob.gif' ALT='*'>&nbsp;$tr{'And To'}:</td>
	<td colspan='2'><input type='text' name='CC' style='width: 220px;' value='$apcupsdsettings{'CC'}'></td>
	<td class='base'><IMG SRC='/ui/img/blob.gif' ALT='*'>&nbsp;$tr{'SMS Email Address'}:</td>
	<td colspan='2'><input type='text' name='SMSEMAIL' style='width: 220px;' value='$apcupsdsettings{'SMSEMAIL'}'></td>
</tr>
<tr>
	<td class='base'>$tr{'Mail Server'}:</td>
	<td colspan='2'><input type='text' name='SMTPSERVER' style='width: 220px;' value='$apcupsdsettings{'SMTPSERVER'}'></td>
	<td class='base'>Port:</td>
	<td colspan='2'><input type='text' name='PORT' style='width: 50px;' value='$apcupsdsettings{'PORT'}'></td>
</tr>
<tr style='height: 20px;'>
	<td></td>
</tr>
</table>

<table style='width: 100%; border: none; margin:1em auto 0 auto;'>
<tr>
	<td class='base'>$tr{'smtp-authc'}</td>
	<td style='width: 2em;'><input type='checkbox' name='ENABLEAUTH' $checked{'ENABLEAUTH'}{'on'} onClick='javaScript:UncheckSMTPS();'></td>
	<td class='base' style='width: 10em;'>$tr{'ssl-smtpsc'}</td>
	<td><input type='checkbox' name='SMTPS' $checked{'SMTPS'}{'on'} onClick='javaScript:CheckAuth();'></td>
	<td class='base' style='width:10em;'>User:</td>
	<td ><input type='text' name='USER' style='width: 15em;' value='$apcupsdsettings{'USER'}'></td>
</tr>
<tr>
	<td class='base' colspan='2'></td>
	<td class='base'>$tr{'starttlsc'}</td>
	<td><input type='checkbox' name='STARTTLS' $checked{'STARTTLS'}{'on'} onClick='javaScript:CheckSTARTTLS();'></td>
	<td class='base'>Password:</td>
	<td ><input type='password' name='EMAIL_PASSWORD' style='width: 15em;' value='$apcupsdsettings{'EMAIL_PASSWORD'}'></td>
</tr>
</table>
END
;

print <<END
<table style='width: 30%; border: none; margin:1em auto;'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' TITLE='$tr{'email-test-tip'}' value='$tr{'mail-test'}'></td>
</tr>
</table>
END
;

&openbox("$tr{'UPS Events'}:");

print <<END
<table style='width: 98%; border: none; margin:1em auto .5em auto;'>
<tr>
	<td style='text-align: right;'>$tr{'apc MSGCOMMFAILURE'}</td>
	<td><input type='checkbox' name='MSGCOMMFAILURE' $checked{'MSGCOMMFAILURE'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGPOWEROUT'}</td>
	<td><input type='checkbox' name='MSGPOWEROUT' $checked{'MSGPOWEROUT'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGONBATTERY'}</td>
	<td><input type='checkbox' name='MSGONBATTERY' $checked{'MSGONBATTERY'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGTIMEOUT'}</td>
	<td><input type='checkbox' name='MSGTIMEOUT' $checked{'MSGTIMEOUT'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGDOSHUTDOWN'}</td>
	<td><input type='checkbox' name='MSGDOSHUTDOWN' $checked{'MSGDOSHUTDOWN'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGBATTATTACH'}</td>
	<td><input type='checkbox' name='MSGBATTATTACH' $checked{'MSGBATTATTACH'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGSTARTSELFTEST'}</td>
	<td><input type='checkbox' name='MSGSTARTSELFTEST' $checked{'MSGSTARTSELFTEST'}{'on'}></td>
</tr>
<tr>
	<td style='text-align: right;'>$tr{'apc MSGCOMMOK'}</td>
	<td><input type='checkbox' name='MSGCOMMOK' $checked{'MSGCOMMOK'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGPOWERBACK'}</td>
	<td><input type='checkbox' name='MSGPOWERBACK' $checked{'MSGPOWERBACK'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGOFFBATTERY'}</td>
	<td><input type='checkbox' name='MSGOFFBATTERY' $checked{'MSGOFFBATTERY'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGLOADLIMIT'}</td>
	<td><input type='checkbox' name='MSGLOADLIMIT' $checked{'MSGLOADLIMIT'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGREMOTEDOWN'}</td>
	<td><input type='checkbox' name='MSGREMOTEDOWN' $checked{'MSGREMOTEDOWN'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGBATTDETACH'}</td>
	<td><input type='checkbox' name='MSGBATTDETACH' $checked{'MSGBATTDETACH'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGENDSELFTEST'}</td>
	<td><input type='checkbox' name='MSGENDSELFTEST' $checked{'MSGENDSELFTEST'}{'on'}></td>
</tr>
<tr>
	<td style='text-align: right;'></td><td></td>
	<td style='text-align: right;'>$tr{'apc MSGANNOY'}</td>
	<td><input type='checkbox' name='MSGANNOY' $checked{'MSGANNOY'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGEMERGENCY'}</td>
	<td><input type='checkbox' name='MSGEMERGENCY' $checked{'MSGEMERGENCY'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGRUNLIMIT'}</td>
	<td><input type='checkbox' name='MSGRUNLIMIT' $checked{'MSGRUNLIMIT'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGKILLPOWER'}</td>
	<td><input type='checkbox' name='MSGKILLPOWER' $checked{'MSGKILLPOWER'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGCHANGEME'}</td>
	<td><input type='checkbox' name='MSGCHANGEME' $checked{'MSGCHANGEME'}{'on'}></td>
	<td style='text-align: right;'>$tr{'apc MSGFAILING'}</td>
	<td><input type='checkbox' name='MSGFAILING' $checked{'MSGFAILING'}{'on'}></td>
</tr>
</table>
END
;

&closebox();

&closebox();

print <<END;

<table style='width: 100%; border: none; margin:1em auto;'>
<tr>
	<td style='width: 33%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'save and restart'}'></td>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'restart'}'></td>
	<td style='width: 33%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'stop'}'></td>
</tr>
</table>
</div></form>
END


if ( $apcupsdsettings{'ENABLE'} eq 'on' and -f "/var/run/apcupsd.pid" ) {
	&openbox("$tr{'UPS Status'}:");

	print "<div class='list' style='padding:.2em 1.25em; margin:1em;'><pre>\n";
	system ("/sbin/apcaccess");
	print "</pre></div>\n";

	&closebox();
}


&alertbox('add', 'add');

&closepage();
