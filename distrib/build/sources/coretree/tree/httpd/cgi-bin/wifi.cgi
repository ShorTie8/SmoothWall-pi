#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team & ShorTie

use lib "/usr/lib/smoothwall";
use header qw(:standard);
use smoothtype qw(:standard);
use smoothd qw(message);
use strict;
use warnings;
#use diagnostics;

# Define our Hashes
my (%cgiparams, %checked, %selected, %settings);
my (%greenwifi, %orangewifi, %purplewifi);

my $infomessage = "";
my $errormessage = "";
my $tmpmessage = "";
my $refresh = '';
my $success = '';

$cgiparams{'ACTION'} = '';

&showhttpheaders();
&getcgihash(\%cgiparams);

$greenwifi{'ssid'} = '';
$greenwifi{'wpa_passphrase'} = '';
$orangewifi{'ssid'} = '';
$orangewifi{'wpa_passphrase'} = '';
$purplewifi{'ssid'} = '';
$purplewifi{'wpa_passphrase'} = '';

&readhash("${swroot}/ethernet/settings", \%settings );
&readhash("/etc/hostapd/hostapd.green.conf", \%greenwifi );
&readhash("/etc/hostapd/hostapd.orange.conf", \%orangewifi );
&readhash("/etc/hostapd/hostapd.purple.conf", \%purplewifi );

$settings{'GREEN_SSID'} = $greenwifi{'ssid'};
$settings{'GREEN_WPA_PASSPHRASE'} = $greenwifi{'wpa_passphrase'};
$settings{'ORANGE_SSID'} = $orangewifi{'ssid'};
$settings{'ORANGE_WPA_PASSPHRASE'} = $orangewifi{'wpa_passphrase'};
$settings{'PURPLE_SSID'} = $purplewifi{'ssid'};
$settings{'PURPLE_WPA_PASSPHRASE'} = $purplewifi{'wpa_passphrase'};


# Action a "Save" request ...

# Green
if ( $cgiparams{'ACTION'} eq "Save Green wifi" ) {
	&log("wifi.cgi ACTION eq Save Green wifi");
	$infomessage .= 'ACTION eq Save Green wifi' ."<br />\n";

	&log("greenwifi ssid is $greenwifi{'ssid'}");
	&log("settings GREEN_SSID is $settings{'GREEN_SSID'}");
	&log("greenwifi wpa_passphrase is $greenwifi{'wpa_passphrase'}");
	&log("settings GREEN_WPA_PASSPHRASE is $settings{'GREEN_WPA_PASSPHRASE'}");

	# now some sanity checks of the settings we've just tried
  
	$tmpmessage = '';
	
	if ($cgiparams{'GREEN_SSID'} ne '' and 
		$cgiparams{'GREEN_SSID'} !~ /^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+-\/_ ]*$/ ) {
		$errormessage .= $tr{"invalid green GREEN_SSID"}."<br />\n";
	}

	if ($cgiparams{'GREEN_WPA_PASSPHRASE'} ne '' and 
	    $cgiparams{'GREEN_WPA_PASSPHRASE'} !~ /^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+\/_ ]{8,63}$/ ) {
		&log("green interface has invalid  GREEN_WPA_PASSPHRASE");
		$errormessage .= $tr{"invalid green GREEN_WPA_PASSPHRASE"}."<br />\n";
	}

	else {
		$errormessage .= $tmpmessage;
	}

	unless ($errormessage) {

		# assign the settings over the top of their erstwhile counterparts.

		&log("assign the settings over the top of their erstwhile counterparts.");
		$greenwifi{'ssid'} = $cgiparams{'GREEN_SSID'};
		$greenwifi{'wpa_passphrase'} = $cgiparams{'GREEN_WPA_PASSPHRASE'};

		&log("greenwifi ssid is now $greenwifi{'ssid'}");
		&log("greenwifi wpa_passphrase is now $greenwifi{'wpa_passphrase'}");

		# update hash

		&log("update hash");
		&writehash("/etc/hostapd/hostapd.green.conf", \%greenwifi );
		
		&log("reread hash");
		&readhash("/etc/hostapd/hostapd.green.conf", \%greenwifi );
		
		&log("reset hashes");
		$settings{'GREEN_SSID'} = $greenwifi{'ssid'};
		$settings{'GREEN_WPA_PASSPHRASE'} = $greenwifi{'wpa_passphrase'};

		#system ("/usr/sbin/wifi restart green");
		#system ("/usr/sbin/wifi restart green >/dev/null 2>&1");

		#$success = message('cyclenetworking');
		#$infomessage .= "$success<br /><br />\n" if ($success);
		#$errormessage .= "$tr{'smoothd failure'}: cyclenetworking<br />\n" unless ($success);

		$infomessage .= '  ' ."<br />\n";
		$infomessage .= 'Settings changed, Pleaze reboot !!' ."<br />\n";
	}
}


# Orange
if ( $cgiparams{'ACTION'} eq "Save Orange wifi" ) {
	&log("wifi.cgi ACTION eq Save Orange wifi");
	$infomessage .= 'ACTION eq Save Orange wifi' ."<br />\n";

	# now some sanity checks of the settings we've just tried
  
	$tmpmessage = '';
	
	if ($cgiparams{'ORANGE_SSID'} ne '' and 
		$cgiparams{'ORANGE_SSID'} !~ /^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+-\/_ ]*$/ ) {
		$errormessage .= $tr{"invalid orange ORANGE_SSID"}."<br />\n";
	}

	if ($cgiparams{'ORANGE_WPA_PASSPHRASE'} ne '' and 
	    $cgiparams{'ORANGE_WPA_PASSPHRASE'} !~ /^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+\/_ ]{8,63}$/ ) {
		&log("orange interface has invalid  ORANGE_WPA_PASSPHRASE");
		$errormessage .= $tr{"invalid orange ORANGE_WPA_PASSPHRASE"}."<br />\n";
	}

	else {
		$errormessage .= $tmpmessage;
	}

	unless ($errormessage) {

		# assign the settings over the top of their erstwhile counterparts.

		&log("assign the settings over the top of their erstwhile counterparts.");
		$orangewifi{'ssid'} = $cgiparams{'ORANGE_SSID'};
		$orangewifi{'wpa_passphrase'} = $cgiparams{'ORANGE_WPA_PASSPHRASE'};

		&log("orangewifi ssid is now $orangewifi{'ssid'}");
		&log("orangewifi wpa_passphrase is now $orangewifi{'wpa_passphrase'}");

		# update hash

		&log("update hash");
		&writehash("/etc/hostapd/hostapd.orange.conf", \%orangewifi );
		
		&log("reread hash");
		&readhash("/etc/hostapd/hostapd.orange.conf", \%orangewifi );
		
		&log("reset hashes");
		$settings{'ORANGE_SSID'} = $orangewifi{'ssid'};
		$settings{'ORANGE_WPA_PASSPHRASE'} = $orangewifi{'wpa_passphrase'};

		#system ("/usr/sbin/wifi restart orange");
		#system ("/usr/sbin/wifi restart orange >/dev/null 2>&1");

		#$success = message('cyclenetworking');
		#$infomessage .= "$success<br /><br />\n" if ($success);
		#$errormessage .= "$tr{'smoothd failure'}: cyclenetworking<br />\n" unless ($success);

		$infomessage .= '  ' ."<br />\n";
		$infomessage .= 'Settings changed, Pleaze reboot !!' ."<br />\n";
	}
}


# Purple
if ( $cgiparams{'ACTION'} eq "Save Purple wifi" ) {
	&log("wifi.cgi ACTION eq Save Purple wifi");
	$infomessage .= 'ACTION eq Save Purple wifi' ."<br />\n";

	# now some sanity checks of the settings we've just tried
  
	$tmpmessage = '';
	
	if ($cgiparams{'PURPLE_SSID'} ne '' and 
		$cgiparams{'PURPLE_SSID'} !~ /^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+-\/_ ]*$/ ) {
		$errormessage .= $tr{"invalid purple PURPLE_SSID"}."<br />\n";
	}

	if ($cgiparams{'PURPLE_WPA_PASSPHRASE'} ne '' and 
	    $cgiparams{'PURPLE_WPA_PASSPHRASE'} !~ /^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+\/_ ]{8,63}$/ ) {
		&log("purple interface has invalid  PURPLE_WPA_PASSPHRASE");
		$errormessage .= $tr{"invalid purple PURPLE_WPA_PASSPHRASE"}."<br />\n";
	}

	else {
		$errormessage .= $tmpmessage;
	}

	unless ($errormessage) {

		# assign the settings over the top of their erstwhile counterparts.

		&log("assign the settings over the top of their erstwhile counterparts.");
		$purplewifi{'ssid'} = $cgiparams{'PURPLE_SSID'};
		$purplewifi{'wpa_passphrase'} = $cgiparams{'PURPLE_WPA_PASSPHRASE'};

		&log("purplewifi ssid is now $purplewifi{'ssid'}");
		&log("purplewifi wpa_passphrase is now $purplewifi{'wpa_passphrase'}");

		# update hash

		&log("update hash");
		&writehash("/etc/hostapd/hostapd.purple.conf", \%purplewifi );
		
		&log("reread hash");
		&readhash("/etc/hostapd/hostapd.purple.conf", \%purplewifi );
		
		&log("reset hashes");
		$settings{'PURPLE_SSID'} = $purplewifi{'ssid'};
		$settings{'PURPLE_WPA_PASSPHRASE'} = $purplewifi{'wpa_passphrase'};

		#system ("/usr/sbin/wifi restart purple");
		#system ("/usr/sbin/wifi restart purple >/dev/null 2>&1");

		#$success = message('cyclenetworking');
		#$infomessage .= "$success<br /><br />\n" if ($success);
		#$errormessage .= "$tr{'smoothd failure'}: cyclenetworking<br />\n" unless ($success);

		$infomessage .= '  ' ."<br />\n";
		$infomessage .= 'Settings changed, Pleaze reboot !!' ."<br />\n";
	}
}

# End Action a "Save" request ...

&openpage($tr{'wifi interfaces configuration'}, 1, $refresh, 'services');
#&openpage($tr{'wifi interfaces configuration'}, 1, '', '');
&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='post' action='?'><div>\n";

# deal with the green, orange and purple settings.
&display_interface( \%settings, 'GREEN' );
&display_interface( \%settings, 'ORANGE' ) if ($settings{'ORANGE_DEV'});
&display_interface( \%settings, 'PURPLE' ) if ($settings{'PURPLE_DEV'});

print <<END

</div></form>
END
;

&closebigbox();
&closepage();

sub display_interface
{
	my ( $settings, $prefix ) = @_;

	&openbox("${prefix}:");

	print <<END
<table style='width: 100%;'>
<tr>
	<td style='width:56%;' class='base'>$tr{'Country_Code'}</td>
	<td><b>$settings{Country_Code}</b></td>
</tr>

<table style='width: 100%;'>
<tr>
	<td class='base'>$tr{'brg_namec'}</td>
	<td><b>$settings{"${prefix}_BRG"}</b></td>
	<td class='base'>$tr{'brg_macc'}</td>
	<td><b>$settings{"${prefix}_BRG_MAC"}</b></td>
</tr>

<tr>
	<td class='base'>$tr{'wifi devicec'}</td>
	<td><b>$settings{"${prefix}_WIFI"}</b></td>
	<td class='base'>$tr{'net addressc'}</td>
	<td><b>$settings{"${prefix}_NETADDRESS"}</b></td>
</tr>

<tr>
	<td class='base'>$tr{'nic devicec'}</td>
	<td><b>$settings{"${prefix}_BRG_DEV"}</b></td>
	<td class='base'>$tr{'addressc'}</td>
	<td><b>$settings{"${prefix}_ADDRESS"}</b></td>
</tr>

<tr>
	<td style='width:25%;' class='base'>$tr{'ssid'}</td>
	<td style='width:25%;'><input type='text' name='${prefix}_SSID' value='$settings{"${prefix}_SSID"}' id='ssid' 
		@{[jsvalidregex('ssid','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+-\/_ ]*$')]}></td>
	<td style='width:25%;' class='base'>$tr{'password'}</td>
	<td style='width:25%;'><input type='text' name='${prefix}_WPA_PASSPHRASE' value='$settings{"${prefix}_WPA_PASSPHRASE"}' id='wpa_passphrase' 
		@{[jsvalidregex('wpa_passphrase','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+\/_ ]{8,63}$')]}></td>
</tr>

<table style='width: 100%;'>
<tr>
        <td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{"${prefix}save"}'></td>
</tr>

</table>
END
;

	&closebox();

	return;
}

