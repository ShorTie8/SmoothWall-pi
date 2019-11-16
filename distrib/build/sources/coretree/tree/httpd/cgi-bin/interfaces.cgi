#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw(:standard);
use smoothtype qw(:standard);
use smoothd qw(message);
use Socket;
use strict;
use warnings;

my (%cgiparams, %checked, %selected, %settings);
my ($macaddress, $ignoremtutext);

my $infomessage = "";
my $errormessage = "";
my $tmpmessage = "";
my $refresh = '';
my $success = '';

$settings{'RED_IGNOREMTU'} = '';
$settings{'DNS1_OVERRIDE'} = '';
$settings{'DNS2_OVERRIDE'} = '';

$cgiparams{'ACTION'} = '';
$cgiparams{'DNS2'} = '';
$cgiparams{'DNS2'} = '';
$cgiparams{'RED_ADDRESS'} = '';
$cgiparams{"RED_NETMASK"} = '';
$cgiparams{"DEFAULT_GATEWAY"} = '';
$cgiparams{"DNS1"} = '';
$cgiparams{"DNS2"} = '';

$selected{'STATIC'} = "";
$selected{'DHCP'} = "";
$selected{'PPPOE'} = "";

&showhttpheaders();
&getcgihash(\%cgiparams);

&readhash("${swroot}/ethernet/settings", \%settings );
if ($settings{'RED_IGNOREMTU'} ne "off") {
	$settings{'RED_IGNOREMTU'} = "on";
}

# Action a "Save" request ...

if ( $cgiparams{'ACTION'} eq $tr{'save'} ) {
	# assign the settings over the top of their erstwhile counterparts.

	$settings{'GREEN_ADDRESS'} = $cgiparams{'GREEN_ADDRESS'} if ( defined $cgiparams{'GREEN_ADDRESS'} );
	$settings{'GREEN_NETMASK'} = $cgiparams{'GREEN_NETMASK'} if ( defined $cgiparams{'GREEN_NETMASK'} );

	$settings{'ORANGE_ADDRESS'} = $cgiparams{'ORANGE_ADDRESS'} if ( defined $cgiparams{'ORANGE_ADDRESS'} );
	$settings{'ORANGE_NETMASK'} = $cgiparams{'ORANGE_NETMASK'} if ( defined $cgiparams{'ORANGE_NETMASK'} );

	$settings{'PURPLE_ADDRESS'} = $cgiparams{'PURPLE_ADDRESS'} if ( defined $cgiparams{'PURPLE_ADDRESS'} );
	$settings{'PURPLE_NETMASK'} = $cgiparams{'PURPLE_NETMASK'} if ( defined $cgiparams{'PURPLE_NETMASK'} );

	$settings{'RED_TYPE'} = $cgiparams{'RED_TYPE'} if ( defined $cgiparams{'RED_TYPE'} );
	$settings{'RED_DHCP_HOSTNAME'} = $cgiparams{'RED_DHCP_HOSTNAME'} if ( defined $cgiparams{'RED_DHCP_HOSTNAME'} );
	$settings{'RED_ADDRESS'} = $cgiparams{'RED_ADDRESS'} if ( defined $cgiparams{'RED_ADDRESS'} );
	$settings{'RED_NETMASK'} = $cgiparams{'RED_NETMASK'} if ( defined $cgiparams{'RED_NETMASK'} );

	$settings{'DEFAULT_GATEWAY'} = $cgiparams{'DEFAULT_GATEWAY'} if ( defined $cgiparams{'DEFAULT_GATEWAY'} );
	$settings{'DNS1'} = $cgiparams{'DNS1'} if ( defined $cgiparams{'DNS1'} );
	$settings{'DNS2'} = $cgiparams{'DNS2'} if ( defined $cgiparams{'DNS2'} );

	$cgiparams{'RED_IGNOREMTU'} = "off" if ( %cgiparams && ! defined $cgiparams{'RED_IGNOREMTU'} );

	$settings{'RED_IGNOREMTU'} = $cgiparams{'RED_IGNOREMTU'} if ( defined $cgiparams{'RED_IGNOREMTU'} );
	$settings{'DNS1_OVERRIDE'} = $cgiparams{'DNS1_OVERRIDE'} if ( defined $cgiparams{'DNS1_OVERRIDE'} );
	$settings{'DNS2_OVERRIDE'} = $cgiparams{'DNS2_OVERRIDE'} if ( defined $cgiparams{'DNS2_OVERRIDE'} );
	$settings{'RED_MAC'} = $cgiparams{'RED_MAC'} if ( defined $cgiparams{'RED_MAC'} );

	# now some sanity checks of the settings we've just tried
  
	$tmpmessage = '';
	if ( not &validip( $settings{'GREEN_ADDRESS'} )) {
		$tmpmessage .= $tr{'the ip address for the green interface is invalid'}."<br />\n";
	}

	if ( not &validmask( $settings{'GREEN_NETMASK'} )) {
		$tmpmessage .= $tr{'the netmask for the green interface is invalid'}."<br />\n";
	}
	if ($tmpmessage eq "") {
		( $settings{'GREEN_NETADDRESS'}, $settings{'GREEN_BROADCAST'} ) =
			&bcast_and_net( $settings{'GREEN_ADDRESS'}, $settings{'GREEN_NETMASK'} );
	}
	else {
		$errormessage .= $tmpmessage;
	}

	if ( defined $settings{'ORANGE_ADDRESS'} and $settings{'ORANGE_ADDRESS'} ne "" ) {
		$tmpmessage = '';
		if ( not &validip( $settings{'ORANGE_ADDRESS'} )) {
			$tmpmessage .= $tr{'the ip address for the orange interface is invalid'}."<br />\n";
		}
		if ( not &validmask( $settings{'ORANGE_NETMASK'} )) {
			$tmpmessage .= $tr{'the netmask for the orange interface is invalid'}."<br />\n";
		}
		if ($tmpmessage eq "") {
			( $settings{'ORANGE_NETADDRESS'}, $settings{'ORANGE_BROADCAST'} ) =
			&bcast_and_net( $settings{'ORANGE_ADDRESS'}, $settings{'ORANGE_NETMASK'} );
		}
		else {
			$errormessage .= $tmpmessage;
		}
	}

	if ( defined $settings{'PURPLE_ADDRESS'} and $settings{'PURPLE_ADDRESS'} ne "" ) {
		$tmpmessage = '';
		if ( not &validip( $settings{'PURPLE_ADDRESS'} )) {
			$tmpmessage .= $tr{'the ip address for the purple interface is invalid'}."<br />\n";
		}
		if ( not &validmask( $settings{'PURPLE_NETMASK'} )) {
			$tmpmessage .= $tr{'the netmask for the purple interface is invalid'}."<br />\n";
		}
		if ($tmpmessage eq "") {
			( $settings{'PURPLE_NETADDRESS'}, $settings{'PURPLE_BROADCAST'} ) = 
			&bcast_and_net( $settings{'PURPLE_ADDRESS'}, $settings{'PURPLE_NETMASK'} ); 
		}
		else {
			$errormessage .= $tmpmessage;
		}
	}

	if ( defined $settings{'RED_MAC'} and $settings{'RED_MAC'} ne "" and not &validmac( $settings{'RED_MAC'} )) {
		$errormessage .= $tr{'the spoofed mac address for the red interface is invalid'}."<br />\n";
	}

	if ( defined $settings{'RED_TYPE'} and $settings{'RED_TYPE'} ne "" ) {
		$tmpmessage = '';
		if ( $settings{'RED_TYPE'} eq "DHCP" ) {
			if ( $settings{'DNS1_OVERRIDE'} ne "" and not &validip( $settings{'DNS1_OVERRIDE'} )) {
				$tmpmessage .= $tr{'invalid primary dns override'}."<br />\n";
			}
			if ( $settings{'DNS2_OVERRIDE'} ne "" and not &validip( $settings{'DNS2_OVERRIDE'} )) {
				$tmpmessage .= $tr{'invalid secondary dns override'}."<br />\n";
			}
			if ( (not defined $settings{'DNS1_OVERRIDE'} or $settings{'DNS1_OVERRIDE'} eq "") and
			     ($settings{'DNS2_OVERRIDE'} and $settings{'DNS2_OVERRIDE'} ne "" ) ) {
				$tmpmessage .= $tr{'cannot specify secondary dns override without specifying primary override'}."<br />\n";
			}
			$errormessage .= $tmpmessage;
		}
		if ( $settings{'RED_TYPE'} eq "STATIC" ) {
			if ( not &validip( $settings{'RED_ADDRESS'} )) {
				$tmpmessage .= $tr{'the ip address for the red interface is invalid'}."<br />\n";
			}
			if ( not &validmask( $settings{'RED_NETMASK'} )) {
				$tmpmessage .= $tr{'the netmask for the red interface is invalid'}."<br />\n";
			}
			if ( $settings{'DEFAULT_GATEWAY'} ne "" and not &validip( $settings{'DEFAULT_GATEWAY'} )) {
				$tmpmessage .= $tr{'the default gateway is invalid'}."<br />\n";
			}
			if ( $settings{'DNS1'} ne "" and not &validip( $settings{'DNS1'} )) {
				$tmpmessage .= $tr{'invalid primary dns'}."<br />\n";
			}
			if ( $settings{'DNS2'} ne "" and not &validip( $settings{'DNS2'} )) {
				$tmpmessage .= $tr{'invalid secondary dns'}."<br />\n";
			}
			if ( (not defined $settings{'DNS1'} or $settings{'DNS1'} eq "") and
			     ($settings{'DNS2'} and $settings{'DNS2'} ne "" ) ) {
				$tmpmessage .= $tr{'cannot specify secondary dns without specifying primary'}."<br />\n";
			}
			if ( $settings{'DNS1_OVERRIDE'} ne "" and not &validip( $settings{'DNS1_OVERRIDE'} )) {
				$tmpmessage .= $tr{'invalid primary dns override'}."<br />\n";
			}
			if ( $settings{'DNS2_OVERRIDE'} ne "" and not &validip( $settings{'DNS2_OVERRIDE'} )) {
				$tmpmessage .= $tr{'invalid secondary dns override'}."<br />\n";
			}
			if ( (not defined $settings{'DNS1_OVERRIDE'} or $settings{'DNS1_OVERRIDE'} eq "") and
			     ($settings{'DNS2_OVERRIDE'} and $settings{'DNS2_OVERRIDE'} ne "" ) ) {
				$tmpmessage .= $tr{'cannot specify secondary dns override without specifying primary override'}."<br />\n";
			}
			if ($tmpmessage eq "") {
				( $settings{'RED_NETADDRESS'}, $settings{'RED_BROADCAST'} ) = 
				    &bcast_and_net( $settings{'RED_ADDRESS'}, $settings{'RED_NETMASK'} );
			}
			else {
				$errormessage .= $tmpmessage;
			}
		}
	}

	unless ($errormessage) {
		&writehash("${swroot}/ethernet/settings", \%settings);

		$success = message('cyclenetworking');
		$infomessage .= "$success<br /><br />\n" if ($success);
		$errormessage .= "$tr{'smoothd failure'}: cyclenetworking<br />\n" unless ($success);

		# cyclenetworking flushes iptables, which will make some services
		# inaccessible.
		#   - Rewrite configs that need to know about the change.
		#   - Restart all services which depend on firewall rules.

		# To prevent loss of DHCP & Proxy if mods exist, use the first one that is found.
		my @ovrride = </var/smoothwall/mods/*/usr/bin/smoothwall/writedhcp.pl /usr/bin/smoothwall/writedhcp.pl>;
		system("$ovrride[0]");
		@ovrride = </var/smoothwall/mods/*/usr/bin/smoothwall/writeproxy.pl /usr/bin/smoothwall/writeproxy.pl>;
		system("$ovrride[0]");

		foreach my $service (qw(dhcpd p3scan squid im sip)) {
			$success = message("${service}restart");
			$infomessage .= $success ."<br />" if ($success);
			$errormessage .= "$tr{'smoothd failure'}: ${service}restart<br />\n" unless ($success);
		}
	}
}

# Display some DHCP values in the UI
if (( $settings{'RED_TYPE'} ne "STATIC" )) {
	if (-s "${swroot}/red/local-ipaddress") {
		$cgiparams{'RED_ADDRESS'} = &readvalue("${swroot}/red/local-ipaddress");
	}
	if (-s "${swroot}/red/remote-ipaddress") {
		$cgiparams{'DEFAULT_GATEWAY'} = &readvalue("${swroot}/red/remote-ipaddress");
	}
	if (-s "${swroot}/red/dhcp-netmask") {
		$cgiparams{'RED_NETMASK'} = &readvalue("${swroot}/red/dhcp-netmask");
	}
	if (-s "${swroot}/red/dns1") {
		$cgiparams{'DNS1'} = &readvalue("${swroot}/red/dns1");
	}
	if (-s "${swroot}/red/dns2") {
		$cgiparams{'DNS2'} = &readvalue("${swroot}/red/dns2");
	}
}

&openpage($tr{'interfaces configuration'}, 1, $refresh, 'networking');
&openbigbox('100%', 'LEFT');
&alertbox($errormessage, "", $infomessage);

print "<form method='post' action='?'><div>\n";

# deal with the green, orange and purple settings.
&display_interface( \%settings, 'GREEN' );
&display_interface( \%settings, 'ORANGE' ) if ($settings{'ORANGE_DEV'});
&display_interface( \%settings, 'PURPLE' ) if ($settings{'PURPLE_DEV'});

# if red is on an etherNet, show some configuration options for it.
&display_red_interface( \%settings );

print <<END
  <div style='text-align:center;'><input type='submit' name='ACTION' value='$tr{'save'}'></div>
</div></form>
END
;

&closebigbox();
&closepage();


sub display_interface
{
	my ( $settings, $prefix ) = @_;

	my $interface = $settings{"${prefix}_DEV"};

	# Get the MAC address
	if (open (MACADDR, "/sys/class/net/${interface}/address")) {
		$macaddress = <MACADDR>;
		chomp $macaddress;
		close (MACADDR);
	}
	else {
		$macaddress = "";
	}

	# Get the driver name and bus
	if (open (DRIVER, "/bin/ls -C1 /sys/class/net/${interface}/device/driver/module/drivers|")) {
		$_ = <DRIVER>;
		chomp;
		my ($bus, $driver) = split(/:/);
		$settings{"${prefix}_DISPLAYBUS"} = $bus;
		$settings{"${prefix}_DISPLAYDRIVER"} = $driver;
		close (DRIVER);
	}

	&openbox("${prefix}:");

	print <<END
<table style='width: 100%;'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'physical interface'}</td>
	<td style='width: 25%;'><b>$interface</b></td>
	<td class='base' style='width: 25%;'>$tr{'ip addressc'}</td>
	<td style='width: 25%;'><input type='text' name='${prefix}_ADDRESS' value='$settings{"${prefix}_ADDRESS"}' 
		id='${prefix}address' @{[jsvalidip("${prefix}address")]}></td>
</tr>
<tr>
	<td class='base'>$tr{'nic type'}</td>
	<td><b>$settings{"${prefix}_DISPLAYDRIVER"} ($settings{"${prefix}_DISPLAYBUS"})</b></td>
	<td class='base'>$tr{'netmaskc'}</td>
	<td><input type='text' name='${prefix}_NETMASK' value='$settings{"${prefix}_NETMASK"}' 
		id='${prefix}mask' @{[jsvalidmask("${prefix}mask")]}></td>
</tr>
<tr>
	<td class='base'>$tr{'mac addressc'}</td>
	<td><b>$macaddress</b></td>
	<td>&nbsp;</td>
	<td>&nbsp;</td>
</tr>
</table>
END
;

	&closebox();

	return;
}

sub display_red_interface
{
	my ( $settings ) = @_;

	my $interface = $settings{"RED_DEV"};

	# Get the MAC address
	if (open (MACADDR, "/sys/class/net/${interface}/address")) {
		$macaddress = <MACADDR>;
		chomp $macaddress;
		close (MACADDR);
	}
	else {
		$macaddress = "";
	}

	# Get the driver name and bus
	if (open (DRIVER, "/bin/ls -C1 /sys/class/net/${interface}/device/driver/module/drivers|")) {
		$_ = <DRIVER>;
		chomp;
		my ($bus, $driver) = split(/:/);
		$settings{"RED_DISPLAYBUS"} = $bus;
		$settings{"RED_DISPLAYDRIVER"} = $driver;
		close (DRIVER);
	}

	&openbox("RED:");

	$selected{$settings{'RED_TYPE'}} = " selected";

	my $ignoremtuchecked;
	if ($settings{'RED_IGNOREMTU'} eq "on") {
		$ignoremtuchecked = " checked='checked'";
	}
	else {
		$ignoremtuchecked = "";
	}

	print <<END
<table style='width: 100%;'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'physical interface'}</td>
	<td style='width: 25%;'><b>$interface</b></td>
	<td class='base' style='width: 25%;'>$tr{'connection method'}</td>
	<td style='width: 25%;'>

<script type='text/javascript'>

function optify( field )
{
	var inputval = document.getElementById(field).value;
	if ( inputval == 'DHCP' ){
		_show('hostname');
		_hide('ignoremtu');
		_hide('ipaddress');
		_hide('netmask');
		_hide('gateway');
		_hide('primary');
		_hide('secondary');
		_show('primaryoverride');
		_show('secondaryoverride');
	}
	else if ( inputval == 'STATIC' ){
		_hide('hostname');
		_hide('ignoremtu');
		_show('ipaddress');
		_show('netmask');
		_show('gateway');
		_show('primary');
		_show('secondary');
		_show('primaryoverride');
		_show('secondaryoverride');
	}
	else if ( inputval == 'PPPOE' ){
		_hide('hostname');
		_hide('ignoremtu');
		_hide('ipaddress');
		_hide('netmask');
		_hide('gateway');
		_hide('primary');
		_hide('secondary');
		_hide('primaryoverride');
		_hide('secondaryoverride');
	}
}

</script>
	<select name='RED_TYPE' id='type' onChange='optify("type");'>
		<option value='STATIC' $selected{'STATIC'}>$tr{'static'}</option>
		<option value='DHCP'   $selected{'DHCP'}>DHCP</option>
		<option value='PPPOE'  $selected{'PPPOE'}>PPPoE</option>
	</select></td>
</tr>
<tr>
	<td class='base'>$tr{'nic type'}</td>
	<td><b>$settings{'RED_DISPLAYDRIVER'} ($settings{'RED_DISPLAYBUS'})</b></td>
	<td class='base'>$tr{'dhcp hostname'}</td>
	<td><span class='input' id='hostnameText'>$settings{'RED_DHCP_HOSTNAME'}</span>
		<input id='hostname' @{[jsvalidhostname('hostname')]} type='text'
		style='display:none'
		name='RED_DHCP_HOSTNAME' value='$settings{"RED_DHCP_HOSTNAME"}'></td>
</tr>
<tr>
	<td class='base'>$tr{'mac addressc'}</td>
	<td><b>$macaddress</b></td>
	<td class='base'>$tr{'ip addressc'}</td>
END
;

	# Include both display-only and input fields, but display only one.
	#   %settings: static values
	#   %cgiparams: static values overridden with DHCP/PPPoE values, then with
	#     DNS override values.


	# use 'current' address
	print <<END
	<td style='width: 25%;'><span class='input' id='ipaddressText'>$cgiparams{'RED_ADDRESS'}</span>
		<input id='ipaddress' @{[jsvalidip('ipaddress')]} type='text'
		style='display:none' name='RED_ADDRESS' value='$settings{"RED_ADDRESS"}'></td>
</tr>
<tr>
	<td rowspan='6' colspan='2'>
END
;

	&openbox("Overrides");

	if ($ignoremtuchecked eq '') {
		$ignoremtutext = 'N/A';
	}
	else {
		$ignoremtutext = 'Checked';
	}

	print <<END
<table style='width:100%'>
<tr>
	<td class='base'>$tr{'ignore mtu'}</td>
	<td style='width: 25%;'><span class='input' id='ignoremtuText'>$ignoremtutext</span>
		<input id='ignoremtu'  type='checkbox' style='display:none'
		name='RED_IGNOREMTU'$ignoremtuchecked></td>
</tr>
<tr>
	<td class='base' style='width: 25%;'>$tr{'primary dns override'}</td>
	<td style='width: 25%;'><span class='input' id='primaryoverrideText'>$settings{'DNS1_OVERRIDE'}</span>
		<input id='primaryoverride' 
		@{[jsvalidip('primaryoverride','true')]}
		type='text' name='DNS1_OVERRIDE' style='display:none' value='$settings{"DNS1_OVERRIDE"}'></td>
</tr>
<tr>
	<td class='base' style='width: 25%;'>$tr{'secondary dns override'}</td>
	<td style='width: 25%;'><span class='input' id='secondaryoverrideText'>$settings{'DNS2_OVERRIDE'}</span>
		<input id='secondaryoverride' 
		@{[jsvalidip('secondaryoverride','true')]}
		type='text' name='DNS2_OVERRIDE' style='display:none' value='$settings{"DNS2_OVERRIDE"}'></td>
</tr>
<tr>
	<td class='base' style='width: 25%;'>$tr{'mac spoof'}</td>
	<td style='width: 25%;'><input id='macspoof' 
		@{[(jsvalidregex('macspoof','^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})$','true'))]}
		type='text' name='RED_MAC' value='$settings{"RED_MAC"}'></td>
</tr>
</table>
END
;

	&closebox();


	print <<END
	</td>
</tr>
<tr>
	<td class='base'>$tr{'netmaskc'}</td>
	<td style='width: 25%;'><span class='input' id='netmaskText'>$cgiparams{'RED_NETMASK'}</span>
		<input id='netmask' @{[jsvalidmask('netmask')]} type='text'
		style='display:none' name='RED_NETMASK' value='$settings{"RED_NETMASK"}'></td>
</tr>
<tr>
	<td class='base' style='width: 25%;'>$tr{'default gateway'}</td>
	<td style='width: 25%;'><span class='input' id='gatewayText'>$cgiparams{'DEFAULT_GATEWAY'}</span>
		<input id='gateway' @{[jsvalidip('gateway')]} type='text'
		style='display:none' name='DEFAULT_GATEWAY' value='$settings{"DEFAULT_GATEWAY"}'></td>
</tr>
<tr>
	<td class='base' style='width: 25%;'>$tr{'primary dns'}</td>
	<td style='width: 25%;'><span class='input' id='primaryText'>$cgiparams{'DNS1'}</span>
		<input id='primary' @{[jsvalidip('primary')]} type='text'
		style='display:none' name='DNS1' value='$settings{"DNS1"}'></td>
</tr>
<tr>
	<td class='base'>$tr{'secondary dns'}</td>
	<td style='width: 25%;'><span class='input' id='secondaryText'>$cgiparams{'DNS2'}</span>
		<input id='secondary' @{[jsvalidip('secondary','true')]} type='text'
		style='display:none' name='DNS2' value='$settings{"DNS2"}'></td>
</tr>
</table>
END
;

	&closebox();

	push @_validation_items, "optify('type')" ;

	return;
}

sub bcast_and_net
{
	my ( $address, $netmask ) = @_;
  
	return ('', '') if (!$address || !$netmask);

	my $addressint = inet_aton($address);
	my $netmaskint = inet_aton($netmask);

	my $netaddressint = $addressint & $netmaskint;

	my $netaddress = inet_ntoa($netaddressint);
	my $broadcast  = inet_ntoa($netaddressint | ~$netmaskint);

	return ( $netaddress, $broadcast );
}
