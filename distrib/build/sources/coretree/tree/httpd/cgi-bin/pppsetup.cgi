#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothtype qw( :standard );
use strict;
use warnings;

my (%pppsettings, %temppppsettings, %isdnsettings, %netsettings, %adslsettings);
my (%selected, %checked, @profilenames);
my $maxprofiles = 5;

# Get ISDN settings so we can see if ISDN is enabled or not.
$isdnsettings{'ENABLED'} = 'off';
$adslsettings{'ENABLED'} = 'off';
&readhash("${swroot}/isdn/settings", \%isdnsettings);
&readhash("${swroot}/adsl/settings", \%adslsettings);

# Get PPPoE settings so we can see if PPPoE is enabled or not.
&readhash("${swroot}/ethernet/settings", \%netsettings);

&showhttpheaders();

$pppsettings{'ACTION'} = '';
$pppsettings{'VALID'} = '';

$pppsettings{'PROFILENAME'} = '';

$pppsettings{'COMPORT'} = '';
$pppsettings{'DTERATE'} = '';
$pppsettings{'TELEPHONE'} = '';
$pppsettings{'SPEAKER'} = 'off';
$pppsettings{'DIALMODE'} = '';
$pppsettings{'MAXRETRIES'} = '';
$pppsettings{'TIMEOUT'} = '';
$pppsettings{'PERSISTENT'} = 'off';
$pppsettings{'DIALONDEMAND'} = 'off';
$pppsettings{'DIALONDEMANDDNS'} = 'off';
$pppsettings{'AUTOCONNECT'} = 'off';
$pppsettings{'AUTOREBOOT'} = 'off';
$pppsettings{'SENDCR'} = 'off';

$pppsettings{'SERVICENAME'} = '';
$pppsettings{'CONCENTRATORNAME'} = '';

$pppsettings{'USERNAME'} = '';
$pppsettings{'PASSWORD'} = '';
$pppsettings{'AUTH'} = '';
$pppsettings{'LOGINSCRIPT'} = '';

$pppsettings{'DNS'} = '';
$pppsettings{'DNS1'} = '';
$pppsettings{'DNS2'} = '';

$pppsettings{'STAYUP'} = 'off';
$pppsettings{'STAYUP_TIME'} = '';

&getcgihash(\%pppsettings);

my $infomessage = '';
my $errormessage = '';

# (Deliberate space/tab mis-alignment)
if  ($pppsettings{'ACTION'} ne '' &&
     (-e '/var/run/ppp-smooth.pid' || -e "${swroot}/red/active") &&
     ($netsettings{'RED_TYPE'} ne "STATIC" &&
      $netsettings{'RED_TYPE'} ne "DHCP")
    ) {
	$errormessage .= $tr{'unable to alter profiles while red is active'} ."<br />\n";
	# read in the current vars
	%pppsettings = ();
	$pppsettings{'VALID'} = '';
	&readhash("${swroot}/ppp/settings", \%pppsettings);
}
elsif ($pppsettings{'ACTION'} eq $tr{'save'}) {
	unless ($pppsettings{'COMPORT'} =~ /^(ttyS0|ttyS1|ttyS2|ttyS3|isdn1|isdn2|pppoe|adsl|ttyUSB0|ttyUSB1|ttyUSB2|ttyUSB3|ttyUSB4||ttyUSB5|ttyUSB6|ttyUSB7)$/) {
		$errormessage .= $tr{'invalid input'}."<br />";

	}
	unless ($pppsettings{'DTERATE'} =~ /^(9600|19200|38400|57600|115200|230400|460800|1000000|2000000|4000000)$/) {
		$errormessage .= $tr{'invalid input'}."<br />";
	}
	unless ($pppsettings{'DIALMODE'} =~ /^(T|P)$/) {
		$errormessage .= $tr{'invalid input'}."<br />";
	}
	unless ($pppsettings{'AUTH'} =~
		/^(pap-or-chap|standard-login-script|demon-login-script|other-login-script)$/) {
		$errormessage .= $tr{'invalid input'}."<br />";
	}

	if ($pppsettings{'USERNAME'} eq '') {
		$errormessage .= $tr{'username not set'}."<br />"; 
	}
	elsif 	($pppsettings{'USERNAME'} !~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+\/_ ]*$/ ) {
		$errormessage .= $tr{'invalid username'}."<br />";
		$pppsettings{'USERNAME'} = '';
	}

	if ($pppsettings{'PASSWORD'} eq '') {
		$errormessage .= $tr{'password not set'}."<br />";
	}
	elsif ($pppsettings{'PASSWORD'} !~ /^[\w\d\.\-,\(\)\@\$\!\%\^\&\*=\+\/_ ]*$/ ) {
		$errormessage .= $tr{'invalid password'}."<br />";
		$pppsettings{'PASSWORD'} = '';
	}

	if ($pppsettings{'PROFILENAME'} eq '') {
		$errormessage .= $tr{'profile name not given'}."<br />";
		$pppsettings{'PROFILENAME'} = '';
	}

	unless ($pppsettings{'COMPORT'} eq 'pppoe' || $pppsettings{'COMPORT'} eq 'adsl') {
		if ($pppsettings{'TELEPHONE'} eq '') {
			$errormessage .= $tr{'telephone not set'}."<br />"; 
		}
		if (!($pppsettings{'TELEPHONE'} =~ /^[\d\*\#\,]+$/)) {
			$errormessage .= $tr{'bad characters in the telephone number field'}."<br />";
		}
	}
	if ($pppsettings{'DIALONDEMAND'} eq 'on' &&
		($pppsettings{'COMPORT'} eq 'pppoe' || $pppsettings{'COMPORT'} eq 'adsl')) {
		$errormessage .= $tr{'dial on demand for this interface is not supported'}."<br />";
		$pppsettings{'DIALONDEMAND'} = 'off';
	}
	if ($pppsettings{'DIALONDEMANDDNS'} eq 'on' &&
		($pppsettings{'COMPORT'} eq 'pppoe' || $pppsettings{'COMPORT'} eq 'adsl')) {
		$errormessage .= $tr{'dial on demand for this interface is not supported'}."<br />";
		$pppsettings{'DIALONDEMANDDNS'} = 'off';
	}


	if ($pppsettings{'TIMEOUT'} eq '') {
		$errormessage .= $tr{'idle timeout not set'}."<br />";
	}
	unless ($pppsettings{'TIMEOUT'} =~ /^\d+$/) {
                $errormessage .= $tr{'only digits allowed in the idle timeout'}."<br />";
	}
	if ($pppsettings{'LOGINSCRIPT'} =~ /[.\/ ]/ ) {
		$errormessage .= $tr{'bad characters in script field'}."<br />"; 
	}


	if ($pppsettings{'DNS'} eq 'Manual') {
		unless (&validip($pppsettings{'DNS1'})) {
			$errormessage .= $tr{'invalid primary dns'}."<br />";
			$pppsettings{'DNS'} = 'Automatic'
		}
	}

	if ($pppsettings{'DNS2'}) {
		unless (&validip($pppsettings{'DNS2'})) {
			$errormessage .= $tr{'invalid secondary dns'}."<br />";
		}
	}
	if ($pppsettings{'MAXRETRIES'} eq '') {
		$errormessage .= $tr{'max retries not set'}."<br />";
	}
	if (!($pppsettings{'MAXRETRIES'} =~ /^\d+$/)) {
		$errormessage .= $tr{'only digits allowed in max retries field'}."<br />";
	}
	if ($adslsettings{'ENABLED'} eq 'on' && $pppsettings{'COMPORT'} eq 'adsl') {
		if ($adslsettings{'DEVICE'} eq 'ALCATEL' && !-e "${swroot}/adsl/mgmt.o") {
			$errormessage .= $tr{'no usb adsl firmware'}."<br />";
		}
	}
	if ($isdnsettings{'ENABLED'} eq 'on' && $pppsettings{'COMPORT'} =~ /^isdn/) {
		unless ($pppsettings{'STAYUP_TIME'} =~ /^\d+$/) {
			$errormessage .= 'Minimum time to keep second channel up is not a number.'."<br />";
		}
	}


	if ($errormessage) {
		$pppsettings{'VALID'} = 'no';
	}
	else {
		$pppsettings{'VALID'} = 'yes';
	}

	# write cgi vars to the file.
	&writehash("${swroot}/ppp/settings-$pppsettings{'PROFILE'}", \%pppsettings);

	# make link and write secret file.
	&updatesettings();
	&writesecrets();

	&log("$tr{'profile saved'} $pppsettings{'PROFILENAME'}");
	$infomessage = "$tr{'profile saved'} $pppsettings{'PROFILENAME'}";
}
elsif ($pppsettings{'ACTION'} eq $tr{'select'}) {
	%temppppsettings = ();
	$temppppsettings{'PROFILE'} = '';
	&readhash("${swroot}/ppp/settings-$pppsettings{'PROFILE'}", \%temppppsettings);

	if ($temppppsettings{'PROFILE'} ne '') {
		# make link.
		&updatesettings(); 

		# read in the new params "early" so we can write secrets.
		%pppsettings = ();
		&readhash("${swroot}/ppp/settings", \%pppsettings);

		&writesecrets();

		&log("$tr{'profile made current'} $pppsettings{'PROFILENAME'}"); 
		$infomessage = "$tr{'profile made current'} $pppsettings{'PROFILENAME'}";
	}
	else {
		$errormessage .= $tr{'the selected profile is empty'} ."<br />\n";
		%pppsettings = ();		 
		$pppsettings{'VALID'} = '';	 
		&readhash("${swroot}/ppp/settings", \%pppsettings);
	}		
}
elsif ($pppsettings{'ACTION'} eq $tr{'delete'}) {

	truncate ("${swroot}/ppp/settings-$pppsettings{'PROFILE'}", 0);

	foreach my $key (keys(%pppsettings)) {
		$_ = '';
	}
	&readhash("${swroot}/ppp/settings", \%pppsettings);			

	&log("$tr{'profile deleted'} $pppsettings{'PROFILENAME'}");
	$infomessage = "$tr{'profile deleted'} $pppsettings{'PROFILENAME'}";
}
else {
	# read in the current vars

	foreach my $key (keys(%pppsettings)) {
		$_ = '';
	}
	&readhash("${swroot}/ppp/settings", \%pppsettings);
}

# read in the profile names into @profilenames.
my $c;
for ($c = 1; $c <= $maxprofiles; $c++) {
 	%temppppsettings = ();
	$temppppsettings{'PROFILENAME'} = $tr{'empty'};
	&readhash("${swroot}/ppp/settings-$c", \%temppppsettings);
	$profilenames[$c] = $temppppsettings{'PROFILENAME'};
}

if ($pppsettings{'VALID'} eq '') {
	$pppsettings{'PROFILE'} = 1;
	$pppsettings{'PROFILENAME'} = $tr{'unnamed'};
	$pppsettings{'COMPORT'} = 'ttyS0';
	$pppsettings{'DTERATE'} = 115200;
	$pppsettings{'SPEAKER'} = 'on';
	$pppsettings{'PERSISTENT'} = 'off';
	$pppsettings{'DIALONDEMAND'} = 'off';
	$pppsettings{'DIALONDEMANDDNS'} = 'off';
	$pppsettings{'AUTOCONNECT'} = 'off';
	$pppsettings{'AUTOREBOOT'} = 'off';
	$pppsettings{'SERVICENAME'} = '';
	$pppsettings{'CONCENTRATORNAME'} = '';
	$pppsettings{'DIALMODE'} = 'T';
	$pppsettings{'MAXRETRIES'} = 10;
	$pppsettings{'TIMEOUT'} = 15;
	$pppsettings{'AUTH'} = 'pap-or-chap';
	$pppsettings{'DNS'} = 'Automatic';
	$pppsettings{'STAYUP'} = 'off';
	$pppsettings{'STAYUP_TIME'} = '30';
	$pppsettings{'SENDCR'} = 'off';
	$pppsettings{'TELEPHONE'} = '';
	$pppsettings{'USERNAME'} = '';
	$pppsettings{'PASSWORD'} = '';
	$pppsettings{'LOGINSCRIPT'} = '';
	$pppsettings{'DNS1'} = '';
	$pppsettings{'DNS2'} = '';
}


for ($c = 1; $c <= $maxprofiles; $c++) {
	$selected{'PROFILE'}{$c} = '';
}

$selected{'PROFILE'}{$pppsettings{'PROFILE'}} = 'SELECTED';

$selected{'COMPORT'}{'ttyS0'} = '';
$selected{'COMPORT'}{'ttyS1'} = '';
$selected{'COMPORT'}{'ttyS2'} = '';
$selected{'COMPORT'}{'ttyS3'} = '';
$selected{'COMPORT'}{'isdn1'} = '';
$selected{'COMPORT'}{'isdn2'} = '';
$selected{'COMPORT'}{'pppoe'} = '';
$selected{'COMPORT'}{'adsl'} = '';
$selected{'COMPORT'}{'ttyUSB0'} = '';
$selected{'COMPORT'}{'ttyUSB1'} = '';
$selected{'COMPORT'}{'ttyUSB2'} = '';
$selected{'COMPORT'}{'ttyUSB3'} = '';
$selected{'COMPORT'}{'ttyUSB4'} = '';
$selected{'COMPORT'}{'ttyUSB5'} = '';
$selected{'COMPORT'}{'ttyUSB6'} = '';
$selected{'COMPORT'}{'ttyUSB7'} = '';
$selected{'COMPORT'}{$pppsettings{'COMPORT'}} = 'SELECTED';

$selected{'DTERATE'}{'9600'} = '';
$selected{'DTERATE'}{'19200'} = '';
$selected{'DTERATE'}{'38400'} = '';
$selected{'DTERATE'}{'57600'} = '';
$selected{'DTERATE'}{'115200'} = '';
$selected{'DTERATE'}{'230400'} = '';
$selected{'DTERATE'}{'460800'} = '';
$selected{'DTERATE'}{'1000000'} = '';
$selected{'DTERATE'}{'2000000'} = '';
$selected{'DTERATE'}{'4000000'} = '';
$selected{'DTERATE'}{$pppsettings{'DTERATE'}} = 'SELECTED';

$checked{'SPEAKER'}{'off'} = '';
$checked{'SPEAKER'}{'on'} = '';
$checked{'SPEAKER'}{$pppsettings{'SPEAKER'}} = 'CHECKED';

$selected{'DIALMODE'}{'T'} = '';
$selected{'DIALMODE'}{'P'} = '';
$selected{'DIALMODE'}{$pppsettings{'DIALMODE'}} = 'SELECTED';

$checked{'PERSISTENT'}{'off'} = '';
$checked{'PERSISTENT'}{'on'} = '';
$checked{'PERSISTENT'}{$pppsettings{'PERSISTENT'}} = 'CHECKED';

$checked{'DIALONDEMAND'}{'off'} = '';
$checked{'DIALONDEMAND'}{'on'} = '';
$checked{'DIALONDEMAND'}{$pppsettings{'DIALONDEMAND'}} = 'CHECKED';

$checked{'DIALONDEMANDDNS'}{'off'} = '';
$checked{'DIALONDEMANDDNS'}{'on'} = '';
$checked{'DIALONDEMANDDNS'}{$pppsettings{'DIALONDEMANDDNS'}} = 'CHECKED';

$checked{'AUTOCONNECT'}{'off'} = '';
$checked{'AUTOCONNECT'}{'on'} = ''; 
$checked{'AUTOCONNECT'}{$pppsettings{'AUTOCONNECT'}} = 'CHECKED';

$checked{'AUTOREBOOT'}{'off'} = '';
$checked{'AUTOREBOOT'}{'on'} = ''; 
$checked{'AUTOREBOOT'}{$pppsettings{'AUTOREBOOT'}} = 'CHECKED';

$checked{'SENDCR'}{'off'} = '';
$checked{'SENDCR'}{'on'} = '';
$checked{'SENDCR'}{$pppsettings{'SENDCR'}} = 'CHECKED';

$selected{'AUTH'}{'pap-or-chap'} = '';
$selected{'AUTH'}{'standard-login-script'} = '';
$selected{'AUTH'}{'demon-login-script'} = '';
$selected{'AUTH'}{'other-login-script'} = '';
$selected{'AUTH'}{$pppsettings{'AUTH'}} = 'SELECTED';

$checked{'DNS'}{'Automatic'} = '';
$checked{'DNS'}{'Manual'} = '';
$checked{'DNS'}{$pppsettings{'DNS'}} = 'CHECKED';

$checked{'STAYUP'}{'off'} = '';
$checked{'STAYUP'}{'on'} = '';
$checked{'STAYUP'}{$pppsettings{'STAYUP'}} = 'CHECKED';

&openpage($tr{'ppp setup'}, 1, '', 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='POST' action='?'><div>\n";

&openbox($tr{'profiles'});

print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:30%;'>
	<select name='PROFILE'>
END
;

for ($c = 1; $c <= $maxprofiles; $c++) {
	print "		<option value='$c' $selected{'PROFILE'}{$c}>$profilenames[$c]\n";
}

print <<END
	</select></td>
	<td style='width:10%;'><input type='submit' name='ACTION' value='$tr{'select'}'></td>
	<td style='width:10%;'><input type='submit' name='ACTION' value='$tr{'delete'}'></td>
	<td style='width:25%;' class='base'>$tr{'profile name'}</td>
	<td style='width:25%;'><input type='text' name='PROFILENAME' value='$pppsettings{'PROFILENAME'}'></td>
</tr>
</table>
END
;

&closebox();

&openbox($tr{'telephony'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'interface'}</td>
	<td style='width:25%;'>
	<select name='COMPORT'>
		<option value='ttyS0' $selected{'COMPORT'}{'ttyS0'}>$tr{'modem on com1'}
		<option value='ttyS1' $selected{'COMPORT'}{'ttyS1'}>$tr{'modem on com2'}
		<option value='ttyS2' $selected{'COMPORT'}{'ttyS2'}>$tr{'modem on com3'}
		<option value='ttyS3' $selected{'COMPORT'}{'ttyS3'}>$tr{'modem on com4'}
		<option value='ttyUSB0' $selected{'COMPORT'}{'ttyUSB0'}>$tr{'USB Serial 0'}
		<option value='ttyUSB1' $selected{'COMPORT'}{'ttyUSB1'}>$tr{'USB Serial 1'}
		<option value='ttyUSB2' $selected{'COMPORT'}{'ttyUSB2'}>$tr{'USB Serial 2'}
		<option value='ttyUSB3' $selected{'COMPORT'}{'ttyUSB3'}>$tr{'USB Serial 3'}
		<option value='ttyUSB4' $selected{'COMPORT'}{'ttyUSB4'}>$tr{'USB Serial 4'}
		<option value='ttyUSB5' $selected{'COMPORT'}{'ttyUSB5'}>$tr{'USB Serial 5'}
		<option value='ttyUSB6' $selected{'COMPORT'}{'ttyUSB6'}>$tr{'USB Serial 6'}
		<option value='ttyUSB7' $selected{'COMPORT'}{'ttyUSB7'}>$tr{'USB Serial 7'}
END
;

if ($isdnsettings{'ENABLED'} eq 'on') {
	print <<END
		<option value='isdn1' $selected{'COMPORT'}{'isdn1'}>$tr{'isdn1'}
		<option value='isdn2' $selected{'COMPORT'}{'isdn2'}>$tr{'isdn2'}
END
;
}

if ($netsettings{'RED_TYPE'} eq 'PPPOE') {
	print <<END
		<option value='pppoe' $selected{'COMPORT'}{'pppoe'}>PPPoE
END
;
}

if ($adslsettings{'ENABLED'} eq 'on') {
	print <<END
		<option value='adsl' $selected{'COMPORT'}{'adsl'}>ADSL
END
;
}

print <<END
	</select></td>
	<td style='width:25%;' class='base'>$tr{'computer to modem rate'}</td>
	<td style='width:25%;'>
	<select name='DTERATE'>
		<option value='9600' $selected{'DTERATE'}{'9600'}>9600
		<option value='19200' $selected{'DTERATE'}{'19200'}>19200
		<option value='38400' $selected{'DTERATE'}{'38400'}>38400
		<option value='57600' $selected{'DTERATE'}{'57600'}>57600
		<option value='115200' $selected{'DTERATE'}{'115200'}>115200
		<option value='230400' $selected{'DTERATE'}{'230400'}>230400
		<option value='460800' $selected{'DTERATE'}{'460800'}>460800
		<option value='1000000' $selected{'DTERATE'}{'1000000'}>1000000
		<option value='2000000' $selected{'DTERATE'}{'2000000'}>2000000
		<option value='4000000' $selected{'DTERATE'}{'4000000'}>4000000
	</select></td>
</tr>
<tr>
	<td class='base'>$tr{'number'}</td>
	<td><input type='text' name='TELEPHONE' value='$pppsettings{'TELEPHONE'}' id='telephone' 
		@{[jsvalidregex('telephone', '^[0-9\*\#\,]+$', 'true')]}></td>
	<td class='base'>$tr{'modem speaker on'}</td>
	<td><input type='checkbox' name='SPEAKER' value='on' $checked{'SPEAKER'}{'on'}></td>
</tr>
<tr>
	<td class='base'>$tr{'dialing mode'}</td>
	<td>
	<select name='DIALMODE'>
		<option value='T' $selected{'DIALMODE'}{'T'}>$tr{'tone'}
		<option value='P' $selected{'DIALMODE'}{'P'}>$tr{'pulse'}
	</select></td>
	<td class='base'>$tr{'maximum retries'}</td>
	<td><input type='text' name='MAXRETRIES' value='$pppsettings{'MAXRETRIES'}' id='maxretries' 
		@{[jsvalidnumber('maxretries','0','10000')]}></td>
</tr>
<tr>
	<td class='base'>$tr{'idle timeout'}</td>
	<td><input type='text' name='TIMEOUT' value='$pppsettings{'TIMEOUT'}' id='timeout' 
		@{[jsvalidnumber('timeout','0','10000')]}  ></td>
	<td class='base'>$tr{'persistent connection'}</td>
	<td><input type='checkbox' name='PERSISTENT' value='on' $checked{'PERSISTENT'}{'on'}></td>
</tr>
<tr>
	<td class='base'>$tr{'dod'}</td>
	<td><input type='checkbox' name='DIALONDEMAND' value='on' $checked{'DIALONDEMAND'}{'on'}></td>
	<td class='base'>$tr{'dod for dns'}</td>
	<td><input type='checkbox' name='DIALONDEMANDDNS' value='on' $checked{'DIALONDEMANDDNS'}{'on'}></td>
</tr>
<tr>
	<td class='base'>$tr{'connect on smoothwall restart'}</td>
	<td><input type='checkbox' name='AUTOCONNECT' value='on'$checked{'AUTOCONNECT'}{'on'}></td>
	<td class='base'>$tr{'automatic reboot'}</td>
	<td><input type='checkbox' name='AUTOREBOOT' value='on' $checked{'AUTOREBOOT'}{'on'}></td>
</tr>
<tr>
	<td class='base'>$tr{'send cr'}</td>
	<td><input type='checkbox' name='SENDCR' $checked{'SENDCR'}{'on'}></td>
	<td>&nbsp;</td>
	<td>&nbsp;</td>
</tr>
</table>
END
;

&closebox();

if ($netsettings{'RED_TYPE'} eq 'PPPOE') {
	&openbox($tr{'pppoe settings'});

	print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'service name'}</td>
	<td style='width:25%;'><input type='text' name='SERVICENAME' value='$pppsettings{'SERVICENAME'}'></td>
	<td style='width:25%;' class='base'>$tr{'concentrator name'}</td>
	<td style='width:25%;'><input type='text' name='CONCENTRATORNAME' value='$pppsettings{'CONCENTRATORNAME'}'></td>
</tr>
</table>
END
;
	&closebox();
}

if ($adslsettings{'ENABLED'} eq 'on') {
	if ($adslsettings{'DEVICE'} eq 'ALCATEL') {
		&openbox('Alcatel USB ADSL settings:');

		print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td class='base'>$tr{'firmwarec'}</td>
END
;
		if (-e "${swroot}/adsl/mgmt.o") {
			print "	<td style='width:50%; text-align:left' class='base'>$tr{'firmware present'}</td>\n";
		}
		else {
			print "	<td style='width:50%; text-align:left' class='base'>$tr{'firmware not present'}</td>\n"; }
		print <<END
	<td style='width:25%; text-align: center;'><A HREF='/cgi-bin/alcateladslfw.cgi'>$tr{'upload usb adsl firmware'}</A></td>
</tr>
</table>
END
;
		&closebox();
	}
}

if ($isdnsettings{'ENABLED'} eq 'on') {
	openbox('ISDN settings:');
	print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>Keep second channel up:</td>
	<td style='width:25%;'><input type='checkbox' name='STAYUP' $checked{'STAYUP'}{'on'}></td>
	<td style='width:25%;' class='base'>Minimum time to keep second channel up (sec):</td>
	<td style='width:25%;'><input type='text' name='STAYUP_TIME' value='$pppsettings{'STAYUP_TIME'}'></td>
</tr>
</table>
END
;
	&closebox();
}

&openbox($tr{'authentication'});
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'username'}</td>
	<td style='width:25%;'><input type='text' name='USERNAME' value='$pppsettings{'USERNAME'}' id='username' 
		@{[jsvalidregex('username','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+\/_ ]*$')]}></td>
	<td style='width:25%;' class='base'>$tr{'password'}</td>
	<td style='width:25%;'><input type='password' name='PASSWORD' value='$pppsettings{'PASSWORD'}' id='password' 
		@{[jsvalidregex('password','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+\/_ ]*$')]}></td>
</tr>
<tr>
	<td class='base'>$tr{'method'}</td>
	<td>
	<select name='AUTH'>
		<option value='pap-or-chap' $selected{'AUTH'}{'pap-or-chap'}>$tr{'pap or chap'}
		<option value='standard-login-script' $selected{'AUTH'}{'standard-login-script'}>$tr{'standard login script'}
		<option value='demon-login-script' $selected{'AUTH'}{'demon-login-script'}>$tr{'demon login script'}
		<option value='other-login-script' $selected{'AUTH'}{'other-login-script'}>$tr{'other login script'}
	</select></td>
	<td class='base'>$tr{'script name'}</td>
	<td><input type='text' name='LOGINSCRIPT' value='$pppsettings{'LOGINSCRIPT'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox('DNS:');
print <<END
<script type='text/javascript'>
function checkdns(option,field1, field2)
{
	var val = document.getElementById(option).value;
	if ( val == 'Automatic' ){
		_ok(field1);
		_ok(field2);
		document.getElementById(field1).disabled = true;
		document.getElementById(field2).disabled = true;
	} else {
		document.getElementById(field1).disabled = false;
		document.getElementById(field2).disabled = false;
		validip(field1,'false');
		validip(field2,'true');
	}
}
</script>
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width:25%;' class='base'>$tr{'type'}</td>
	<td style='width:25%; text-align:left' class='base'>
	<input type='radio' name='DNS' value='Manual' $checked{'DNS'}{'Manual'} id='r1' 
		onClick="checkdns('r1','dns1', 'dns2')">$tr{'manual'}
	<input type='radio' name='DNS' value='Automatic' $checked{'DNS'}{'Automatic'} id='r2' 
		onClick="checkdns('r2','dns1', 'dns2')" style='margin-left:1em'>$tr{'automatic'}
	</td>
	<td style='width:25%;'>&nbsp;</td>
	<td style='width:25%;'>&nbsp;</td>
</tr>
<tr>
	<td class='base'>$tr{'primary dns'}</td>
	<td><input type='text' name='DNS1' value='$pppsettings{'DNS1'}' id='dns1' 
		@{[jsvalidip('dns1')]}></td>
	<td class='base'>$tr{'secondary dns'}</td>
	<td><input type='text' name='DNS2' value='$pppsettings{'DNS2'}' id='dns2' 
		@{[jsvalidip('dns2','true')]}></td>
</tr>
</table>
END
;

&closebox();

push @_validation_items, "checkdns('r2','dns1','dns2')";
	
print <<END
<table style='width: 60%; border: none; margin-left:auto; margin-right:auto'>
<tr>
        <td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;

print "</div></form>\n";

&alertbox('add','add');
&closebigbox();
&closepage();

sub updatesettings
{
	# make a link from the selected profile to the "default" one.
 	unlink("${swroot}/ppp/settings");
	link("${swroot}/ppp/settings-$pppsettings{'PROFILE'}", "${swroot}/ppp/settings");
}

sub writesecrets
{
	my $stayup;

	# write secrets file.
	open(FILE, ">/${swroot}/ppp/secrets") or die "Unable to write secrets file.";
	flock(FILE, 2);
	my $username = $pppsettings{'USERNAME'};
	my $password = $pppsettings{'PASSWORD'};
	print FILE "'$username' * '$password'\n";
	chmod 0600, "${swroot}/ppp/secrets";
	close FILE;

	# write ibod.cf
	open (FILE, ">${swroot}/ppp/ibod.cf") or die 'Unable to create ibod.cf.';
	flock(FILE, 2);
	if ($pppsettings{'STAYUP'} eq 'on') {
		$stayup = 1;
	}
	else { 
		$stayup = 0;
	}
	print FILE "STAYUP $stayup\n";
	print FILE "STAYUP_TIME $pppsettings{'STAYUP_TIME'}\n";
	close FILE;
}
