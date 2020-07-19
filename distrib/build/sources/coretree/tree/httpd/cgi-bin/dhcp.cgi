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
use smoothtype qw( :standard );
use Socket qw( inet_aton );
use Time::Local;
use List::Util ( first );
use oui_vendor;

use strict;
use warnings;

# Get the date/time now and arrange it in the right format
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=gmtime(time);
$year += 1900;
++$mon;

# Insert leading zeros where necessary
$mon  = 0 . $mon  if ($mon  < 10);
$mday = 0 . $mday if ($mday < 10);
$hour = 0 . $hour if ($hour < 10);
$min  = 0 . $min  if ($min  < 10);
$sec  = 0 . $sec  if ($sec  < 10);
my $timenow = "$year/$mon/$mday $hour:$min:$sec";

my ($info, $alive_static, $unreachable_static, $alive_dyn, $unreachable_dyn);
my (%cgiparams, %checked, %selected, %dhcpsettings, %netsettings, @list, @tempenv, @scanlist);

my $ifcolor= 'black';
my $bdcolor= 'rgba(255,255,255,1)';
my $broadcast = '';
my $errormessage = '';
my $infomessage = '';
my $success = '';
my $subnet = 'green';
my $noscan = 0;	# $noscan = 0 to skip scanning when editing statics.
my $infobox = ''; 	# $infobox = 'info' to use instead of error alert

$subnet = &readvalue("$swroot/dhcp/ifcol") if (-s "$swroot/dhcp/ifcol");
unlink ("$swroot/dhcp/ifcol");

&showhttpheaders();

$cgiparams{'wakemac'} = '';
$cgiparams{'wakebc'} = '';
$cgiparams{'subnet'} = '';

$netsettings{'GREEN_DRIVER'} = '';
$netsettings{'GREEN_ADDRESS'} = '';
$netsettings{'GREEN_NETADDRESS'} = '';
$netsettings{'GREEN_NETMASK'} = '';

$netsettings{'PURPLE_DRIVER'} = '';
$netsettings{'PURPLE_ADDRESS'} = '';
$netsettings{'PURPLE_NETADDRESS'} = '';
$netsettings{'PURPLE_NETMASK'} = '';

$netsettings{'ORANGE_DRIVER'} = '';
$netsettings{'ORANGE_ADDRESS'} = '';
$netsettings{'ORANGE_NETADDRESS'} = '';
$netsettings{'ORANGE_NETMASK'} = '';

&readhash("${swroot}/ethernet/settings", \%netsettings);

$dhcpsettings{'ACTION'} = '';

$dhcpsettings{'ENABLE'} = 'off';
$dhcpsettings{'SHOW_NETSTAT'} = 'off';
$dhcpsettings{'SHOW_DYNAMIC'} = 'off';
$dhcpsettings{'SHOW_STALE'} = 'off';
$dhcpsettings{'SHOW_STATIC'} = 'off';
$dhcpsettings{'START_ADDR'} = '';
$dhcpsettings{'END_ADDR'} = '';
$dhcpsettings{'DNS1'} = '';
$dhcpsettings{'DNS2'} = '';
$dhcpsettings{'DOMAIN_NAME'} = '';
$dhcpsettings{'DEFAULT_LEASE_TIME'} = '60';
$dhcpsettings{'MAX_LEASE_TIME'} = '120';

$dhcpsettings{'BOOT_SERVER'} = '';
$dhcpsettings{'BOOT_FILE'} = '';
$dhcpsettings{'BOOT_ROOT'} = '';
$dhcpsettings{'BOOT_ENABLE'} = 'off';
$dhcpsettings{'DENYUNKNOWN'} = 'off';

$dhcpsettings{'STATIC_HOST'} = '';
$dhcpsettings{'STATIC_DESC'} = '';
$dhcpsettings{'STATIC_MAC'} = '';
$dhcpsettings{'STATIC_IP'} = '';
$dhcpsettings{'DEFAULT_ENABLE_STATIC'} = 'off';

# Default sort on IP address
$dhcpsettings{'COLUMN_ONE'} = 2;
$dhcpsettings{'ORDER_ONE'} = $tr{'log ascending'};
$dhcpsettings{'COLUMN_TWO'} = 2;
$dhcpsettings{'ORDER_TWO'} = $tr{'log ascending'};

&getcgihash(\%dhcpsettings);

if ($ENV{'QUERY_STRING'} && $dhcpsettings{'ACTION'} eq "" ) {
	# Look for table sorting and interface info in the cgi string:
	if ($ENV{'QUERY_STRING'} =~ /,/ ) {
		$noscan = 1;
		@tempenv = split (',',$ENV{'QUERY_STRING'});
  		$subnet = $tempenv[4] if ($tempenv[4]);
  		$dhcpsettings{'SUBNET'}  = $subnet;
  		$dhcpsettings{'ORDER_TWO'}  = $tempenv[3] if ($tempenv[3]);
  		$dhcpsettings{'COLUMN_TWO'} = $tempenv[2] if ($tempenv[2]);
  		$dhcpsettings{'ORDER_ONE'}  = $tempenv[1] if ($tempenv[1]);
		$dhcpsettings{'COLUMN_ONE'} = $tempenv[0] if ($tempenv[0]);
	}
	# Look for wakeup info in the cgi string:
	elsif ($ENV{'QUERY_STRING'} =~ /&/ ) {
		my @values = split (/&/,$ENV{'QUERY_STRING'});
		foreach my $i (@values) {
			my ($name, $data) = split (/=/,$i);
			$cgiparams{"$name"} = $data;
		}
	}
}

# WAKEUP
if ($cgiparams{'wakemac'} && $cgiparams{'wakebc'}) {
	&wakeup ($cgiparams{'wakemac'}, $cgiparams{'wakebc'}, $cgiparams{'subnet'});
}

# ACTION = CLEANLEASES
if ($dhcpsettings{'ACTION'} eq $tr{'dhcpwol-clean-leases'}) {
	&clean_leases;
}

# ACTION = SAVE
if ($dhcpsettings{'ACTION'} eq $tr{'save'}) {
	&action_save;
}

# ACTION = ADD
if ($dhcpsettings{'ACTION'} eq $tr{'add'}) {
	&action_add;
}

# ACTION = REMOVE or EDIT
if ($dhcpsettings{'ACTION'} eq $tr{'remove'} || $dhcpsettings{'ACTION'} eq $tr{'edit'}) {
	&action_remove_edit;
}

# ACTION = NOTHING or 'SELECT'
if ($dhcpsettings{'ACTION'} eq '' || $dhcpsettings{'ACTION'} eq $tr{'select'}) {
	&action_nothing_select;
}

# RUN DHCP LEASE TABLE
if ($dhcpsettings{'SHOW_DYNAMIC'} eq 'on') {
	&dhcp_lease_table;
}

# RUN NEW DHCP STATIC TABLE
if ($dhcpsettings{'SHOW_STATIC'} eq 'on'){
	&get_broadcast;
	&dhcp_static_table;
}

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$dhcpsettings{'ENABLE'}} = 'CHECKED';

$checked{'DENYUNKNOWN'}{'off'} = '';
$checked{'DENYUNKNOWN'}{'on'} = '';
$checked{'DENYUNKNOWN'}{$dhcpsettings{'DENYUNKNOWN'}} = 'CHECKED';

$checked{'SHOW_NETSTAT'}{'off'} = '';
$checked{'SHOW_NETSTAT'}{'on'} = '';
$checked{'SHOW_NETSTAT'}{$dhcpsettings{'SHOW_NETSTAT'}} = 'CHECKED';

$checked{'SHOW_DYNAMIC'}{'off'} = '';
$checked{'SHOW_DYNAMIC'}{'on'} = '';
$checked{'SHOW_DYNAMIC'}{$dhcpsettings{'SHOW_DYNAMIC'}} = 'CHECKED';

$checked{'SHOW_STATIC'}{'off'} = '';
$checked{'SHOW_STATIC'}{'on'} = '';
$checked{'SHOW_STATIC'}{$dhcpsettings{'SHOW_STATIC'}} = 'CHECKED';

$checked{'SHOW_STALE'}{'off'} = '';
$checked{'SHOW_STALE'}{'on'} = '';
$checked{'SHOW_STALE'}{$dhcpsettings{'SHOW_STALE'}} = 'CHECKED';

$checked{'BOOT_ENABLE'}{'on'} = '';
$checked{'BOOT_ENABLE'}{'off'} = '';
$checked{'BOOT_ENABLE'}{$dhcpsettings{'BOOT_ENABLE'}} = 'CHECKED';

$checked{'DEFAULT_ENABLE_STATIC'}{'on'} = '';
$checked{'DEFAULT_ENABLE_STATIC'}{'off'} = '';
$checked{'DEFAULT_ENABLE_STATIC'}{$dhcpsettings{'DEFAULT_ENABLE_STATIC'}} = 'CHECKED';

$selected{'SUBNET'}{'green'} = '';
$selected{'SUBNET'}{'purple'} = '';
$selected{'SUBNET'}{'orange'} = '';
$selected{'SUBNET'}{$dhcpsettings{'SUBNET'}} = 'SELECTED';

&openpage($tr{'dhcp configuration'}, 1, '', 'services');
print "<FORM METHOD='POST' action='?' name='myform'><div>\n";

&alertbox($errormessage, "", $infomessage);

print <<END
<script type="text/javascript">
function AutoFillStaticHost()
{
	if(!document.getElementById) return false;
	var HostField = document.getElementById("static_host");
	var defaultValue = "<Type hostname here>";

	if (HostField.value == '')
	{
	HostField.value = defaultValue; HostField.style.border='2px solid red';
	}
	
	HostField.onfocus = function()
	{
		if(HostField.value == defaultValue)
		{
		HostField.style.border='';
		HostField.value = "";
		} 
	}
	HostField.onblur = function()
	{
		if(HostField.value == "")
		{
		HostField.style.border='2px solid red';
		HostField.value = defaultValue;
		}
	}
	
	var staticIP = document.getElementById("static_ip").value;
	SplitIP = staticIP.split(".");
	SplitIP[3] = "";
	var static_ip = SplitIP.join(".");
	document.getElementById("static_ip").value = static_ip;
}

function ffoxSelectUpdate(elmt)
{
    if(!document.all) elmt.style.cssText = elmt.options[elmt.selectedIndex].style.cssText;
}

function CheckDyn()
{
	if(document.myform.SHOW_DYNAMIC.checked)
	{
	document.myform.SHOW_STALE.disabled = false;
	}
	else
	{
	document.myform.SHOW_STALE.checked = false;
	document.myform.SHOW_STALE.disabled = true;
	}
}
</script>
END
;

&openbox("$tr{'preferences'}:");
print <<END
<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align: right;'>$tr{'dhcpwol-show conns'}:</td>
	<td><input type='checkbox' name='SHOW_NETSTAT' $checked{'SHOW_NETSTAT'}{'on'}></td>
	<td style='text-align: right;'>$tr{'dhcpwol-show dyn'}:</td>
	<td><input type='checkbox' name='SHOW_DYNAMIC' $checked{'SHOW_DYNAMIC'}{'on'} onClick='javaScript:CheckDyn();'></td>
	<td style='text-align: right;'>$tr{'dhcpwol-show stale'}:</td>
	<td><input type='checkbox' name='SHOW_STALE' $checked{'SHOW_STALE'}{'on'}></td>
	<td style='text-align: right;'>$tr{'dhcpwol-show state'}:</td>
	<td><input type='checkbox' name='SHOW_STATIC' $checked{'SHOW_STATIC'}{'on'}></td>
</tr>
</table>
<p>
<table style='width: 50%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;
&closebox();

# Remind to save the settings
&note if (-e "${swroot}/dhcp/uptodate");

&openbox($tr{'global settingsc'});
print <<END
<table class='centered'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'network boot enabledc'}</td>
	<td style='width: 25%;'><input type='checkbox' name='BOOT_ENABLE' $checked{'BOOT_ENABLE'}{'on'}></td>
	<td style='width: 25%;'></td>
	<td style='width: 25%;'></td>
</tr>
<tr>
	<td class='base'>$tr{'boot serverc'}</td>
	<td><input type='text' name='BOOT_SERVER' value='$dhcpsettings{'BOOT_SERVER'}'></td>
	<td class='base'>$tr{'boot filenamec'}</td>
	<td><input type='text' name='BOOT_FILE' value='$dhcpsettings{'BOOT_FILE'}'></td>
</tr>
<tr>
	<td class='base'>$tr{'root pathc'}</td>
	<td colspan='3'><input type='text' name='BOOT_ROOT' size='32' value='$dhcpsettings{'BOOT_ROOT'}'></td>
	<td></td>
	<td></td>
</tr>
</table>
END
;
&closebox();

# PRINT ESTABLISHED CONNECTIONS
if ($dhcpsettings{'SHOW_NETSTAT'} eq 'on'){
	&openbox($tr{'dhcpwol-consc'});
	my @lines = split (/\n/, &pipeopen( '/usr/sbin/ss', '-tuna' ));

	print <<END
<br/>
<table style='width: 100%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr align='left'>
	<th>Protocol</th>
	<th>Recv-Q</th>
	<th>Send-Q</th>
	<th>Local Address:Port</th>
	<th>Peer Address:Port</th>
	<th>State</th>
</tr>
END
;

	shift @lines; # remove the header information

	foreach my $line (@lines){
		my ( $proto, $state, $recvq, $sendq, $local, $remote ) = split (/\s+/, $line);
		if ( $state =~ /ESTAB/ ) {
			print <<END
<tr>
	<td>$proto</td>
	<td>$recvq</td>
	<td>$sendq</td>
	<td>$local</td>
	<td>$remote</td>
	<td>$state</td>
</tr>
END
;
		}
	}
	print "</table>\n";
	&closebox();
}

# Extract the selected iface color
if ( $selected{'SUBNET'}{'green'} eq 'SELECTED' )
{$ifcolor = 'green'; $bdcolor = 'rgba(0,200,0,0.25);';}
if ( $selected{'SUBNET'}{'purple'} eq 'SELECTED' )
{$ifcolor = 'purple'; $bdcolor = 'rgba(150,0,200,0.25);';}
if ( $selected{'SUBNET'}{'orange'} eq 'SELECTED' )
{$ifcolor = 'orange'; $bdcolor = 'rgba(255,140,0,0.35);';}

# START INTERFACE BOX
&openbox($tr{'interface'}, $bdcolor);

# GREEN
my $Gon = 'on' if (-s "${swroot}/dhcp/green");
my $greenenabled = '';
if ($netsettings{'GREEN_DEV'}) {
	if ($Gon) {
		$greenenabled = "<span style='font-style:italic; font-weight:bold;'>(<span style='color:green;'>$tr{'green'}</span>: $tr{'enabled'};</span>";
	}
	else {
		$greenenabled = "<span style='font-style:italic; font-weight:bold;'>(<span style='color:green;'>$tr{'green'}</span>: $tr{'disabled'};</span>";
	}
}

# PURPLE
my $Pon = 'on' if (-s "${swroot}/dhcp/purple");
my $purpleenabled = '';
if ($netsettings{'PURPLE_DEV'}) {
	if ($Pon) {
		$purpleenabled = "<span style='font-style:italic; font-weight:bold;'><span style='color:purple;'>$tr{'purple'}</span>: $tr{'enabled'};</span>";
	}
	else {
		$purpleenabled = "<span style='font-style:italic; font-weight:bold;'><span style='color:purple;'>$tr{'purple'}</span>: $tr{'disabled'};</span>";
	}
}

# ORANGE
my $Oon = 'on' if (-s "${swroot}/dhcp/orange");
my $orangeenabled = '';
if ($netsettings{'ORANGE_DEV'}) {
	if ($Oon) {
		$orangeenabled = "<span style='font-style:italic; font-weight:bold;'><span style='color:orange;'>$tr{'orange'}</span>: $tr{'enabled'})</span>";
	}
	else {
		$orangeenabled = "<span style='font-style:italic; font-weight:bold;'><span style='color:orange;'>$tr{'orange'}</span>: $tr{'disabled'})</span>";
	}
}

print <<END
<INPUT TYPE='hidden' NAME='CHECKSUBNET' VALUE='$dhcpsettings{'SUBNET'}'>

<table style='width:100%; margin:6pt 0;'>
<tr>
	<td style='width: 25%;'>
	<SELECT NAME='SUBNET' style='color: $ifcolor;' onchange='document.getElementById("choose_IF").click();'>
	<OPTION VALUE='green' $selected{'SUBNET'}{'green'} style='color: green;'>GREEN
END
;

if ($netsettings{'PURPLE_DEV'}) {
	print "\t<OPTION VALUE='purple' $selected{'SUBNET'}{'purple'} style='color: purple;'>PURPLE\n";
}

if (($netsettings{'ORANGE_DEV'}) && -e "${swroot}/dhcp/settings-orange") {
	print "\t<OPTION VALUE='orange' $selected{'SUBNET'}{'orange'} style='color: orange;'>ORANGE\n";
}

print <<END
	</SELECT></td>
	<td style='width: 10%;'><INPUT TYPE='submit' id='choose_IF' NAME='ACTION' VALUE='$tr{'select'}' style='display:none'></td>
	<td style='width: 65%;'>&nbsp;$greenenabled $purpleenabled $orangeenabled</td>
</tr>
</table>
<br />
END
;

# START DHCP BOX
&openbox('DHCP:');

print <<END
<table class='centered'>
<tr>
	<td class='base'>$tr{'enabledc'}</td>
	<td><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td class='base'>$tr{'dhcpwol-deny unknown'}</td>
	<td><input type='checkbox' name='DENYUNKNOWN' $checked{'DENYUNKNOWN'}{'on'}></td>
	<td></td>
	<td></td>
</tr>
<tr style='height: 8px;'>
	<td></td>
</tr>
<tr>
	<td class='base' style='width: 25%;'>$tr{'start address'}</td>
	<td style='width: 25%;'><input type='text' name='START_ADDR' value='$dhcpsettings{'START_ADDR'}' 
		id='start_addr' @{[jsvalidip('start_addr')]} ></td>
	<td class='base' style='width: 25%;'>$tr{'end address'}</td>
	<td style='width: 25%;'><input type='text' name='END_ADDR' value='$dhcpsettings{'END_ADDR'}' 
		id='end_addr' @{[jsvalidip('end_addr')]} ></td>
</tr>
<tr>
	<td class='base'>$tr{'primary dns'}</td>
	<td><input type='text' name='DNS1' value='$dhcpsettings{'DNS1'}' id='dns1' 
		@{[jsvalidip('dns1','true')]} ></td>
	<td class='base'>$tr{'secondary dns'}</td>
	<td><input type='text' name='DNS2' value='$dhcpsettings{'DNS2'}' id='dns2' 
		@{[jsvalidip('dns2','true')]}  ></td>
</tr>
<tr>
	<td class='base'>$tr{'primary ntp'}</td>
	<td><input type='text' name='NTP1' value='$dhcpsettings{'NTP1'}' id='ntp1' 
		@{[jsvalidip('ntp1','true')]} ></td>
	<td class='base'>$tr{'secondary ntp'}</td>
	<td><input type='text' name='NTP2' value='$dhcpsettings{'NTP2'}' id='ntp2' 
		@{[jsvalidip('ntp2','true')]}  ></td>
</tr>
<tr>
	<td class='base'>$tr{'primary wins'}</td>
	<td><input type='text' name='WINS1' value='$dhcpsettings{'WINS1'}' id='wins1' 
		@{[jsvalidip('wins1','true')]} ></td>
	<td class='base'>$tr{'secondary wins'}</td>
	<td><input type='text' name='WINS2' value='$dhcpsettings{'WINS2'}' id='wins2' 
		@{[jsvalidip('wins2','true')]}  ></td>
</tr>
<tr>
	<td class='base'>$tr{'default lease time'}</td>
	<td><input type='text' name='DEFAULT_LEASE_TIME' value='$dhcpsettings{'DEFAULT_LEASE_TIME'}' 
		id='default_lease_time' @{[jsvalidnumber('default_lease_time',1,11000)]}></td>
	<td class='base'>$tr{'max lease time'}</td>
	<td><input type='text' name='MAX_LEASE_TIME' value='$dhcpsettings{'MAX_LEASE_TIME'}' 
		id='max_lease_time' @{[jsvalidnumber('max_lease_time',1,11000)]}></td>
</tr>
<tr>
	<td class='base'><IMG SRC='/ui/img/blob.gif' alt='*'>&nbsp;$tr{'domain name suffix'}</td>
	<td><input type='text' name='DOMAIN_NAME' value='$dhcpsettings{'DOMAIN_NAME'}' 
		id='domain_name' @{[jsvalidregex('domain_name','^([a-zA-Z])+([\.a-zA-Z0-9_-])+$','true')]} ></td>
	<td class='base'>$tr{'nis_domainc'}</td>
	<td><input type='text' name='NIS_DOMAIN' value='$dhcpsettings{'NIS_DOMAIN'}' 
		id='nis_domain' @{[jsvalidregex('nis_domain','^([a-zA-Z])+([\.a-zA-Z0-9_-])+$','true')]} ></td>
</tr>
<tr>
	<td class='base'>$tr{'primary nisc'}</td>
	<td><input type='text' name='NIS1' value='$dhcpsettings{'NIS1'}' 
		id='nis1' @{[(jsvalidip('nis1','true'))]}></td>
	<td class='base'>$tr{'secondary nisc'}</td>
	<td><input type='text' name='NIS2' value='$dhcpsettings{'NIS2'}' 
		id='nis2' @{[(jsvalidip('nis2','true'))]}></td>
</tr>
</table>

<table style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='width: 20px;'></td>
	<td><IMG SRC='/ui/img/blob.gif' ALT='*'> $tr{'this field may be blank'}</td>
</tr>
</table>

<table class='centered'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;

&closebox();

# START DHCP LEASE BOX

if ($dhcpsettings{'SHOW_DYNAMIC'} eq 'on') {
	&openbox($tr{'dhcpwol-dyn'});
	$alive_dyn = 0;
	$unreachable_dyn = 0;
	open (LEASES, "$swroot/dhcp/tempfile");
	while (<LEASES>) {
		$alive_dyn++ if /Machine Powered ON/;
		$unreachable_dyn++ if /Machine OFF/;
	}
	close (LEASES);

	print <<END
<table style='width: 25%; border: 1px solid; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align: center; background-color: #E9E8E8;'>
		<span style='color:#03BB03; font-weight:bold;'>Alive: $alive_dyn</span> - 
		<span style='color:red; font-weight:bold;'>Unreachable: $unreachable_dyn</span></td>
</tr>
</table>
<br />
END
;
	my %render_settings =
	(
		'url'     => "/cgi-bin/dhcp.cgi?$dhcpsettings{'COLUMN_ONE'},$dhcpsettings{'ORDER_ONE'},[%COL%],[%ORD%],$subnet",
		'columns' =>
		[
			{
				column => '6',
				title  => "Hostname",
				size   => 20,
				sort   => 'cmp'
			},
			{
				column => '2',
				title  => "IP Address",
				size   => 15,
				sort   => '\&ipcompare'
			},
			{
				column => '5',
				title  => "MAC Address",
				size   => 20,
				sort   => 'cmp'
			},
			{
				column => '3',
				title  => "Lease Started",
				size   => 20,
				sort   => 'cmp'
			},
			{
				column => '4',
				title  => "Lease Expires",
				size   => 20,
				sort   => 'cmp'
			},
			{
				column => '7',
				title  => "Active",
				rotate => '60',
				sort   => 'cmp'
			},
		]
	);

	&displaytable("/$swroot/dhcp/tempfile", \%render_settings, $dhcpsettings{'ORDER_TWO'}, $dhcpsettings{'COLUMN_TWO'});

	if (-s "/$swroot/dhcp/tempfile") {

		print <<END
<table style='width: 20%; border: none; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align: center;'>
		<input type='submit' name='ACTION' value='$tr{'dhcpwol-clean-leases'}' 
		onClick='return confirm("$tr{'dhcpwol-confirm'} ?");'></td>
</tr>
</table>
END
;
	}
	&closebox();
}

# START NEW STATIC ASSIGNMENT BOX

#print "<a id='static'></a>\n";

&openbox($tr{'add a new static assignment'});

print <<END
<a name="statichost"></a>
<table class='centered'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'hostnamec'}</td>
	<td style='width: 25%;'><input type='text' name='STATIC_HOST' value='$dhcpsettings{'STATIC_HOST'}' 
		id='static_host' @{[jsvalidregex('static_host','^([a-zA-Z])+([\.a-zA-Z0-9_-])+$')]}></td>
	<td class='base' style='width: 25%;'>$tr{'descriptionc'}</td>
	<td style='width: 25%;'><input type='text' name='STATIC_DESC' value='$dhcpsettings{'STATIC_DESC'}' 
		id='static_desc' @{[jsvalidregex('static_desc','^([a-zA-Z0-9_-]+)$','true')]} ></td>
</tr>
<tr>
	<td class='base'>$tr{'mac addressc'}</td>
	<td><input type='text' name='STATIC_MAC' value='$dhcpsettings{'STATIC_MAC'}' 
		id='static_mac' @{[(jsvalidmac('static_mac'))]} ></td>
	<td class='base'>$tr{'ip addressc'}</td>
	<td><input type='text' name='STATIC_IP' value='$dhcpsettings{'STATIC_IP'}' 
		id='static_ip' @{[(jsvalidip('static_ip'))]}></td>
</tr>
<tr>
	<td class='base'>$tr{'enabledc'}</td>
	<td><input type='checkbox' name='DEFAULT_ENABLE_STATIC' $checked{'DEFAULT_ENABLE_STATIC'}{'on'}></td>
	<td style='text-align: right;'><input type='submit' name='ACTION' value='$tr{'add'}'></td>
	<!-- <td style='text-align: right;'><input type='submit' name='ACTION' value='$tr{'add'}'></td> -->
	<td></td>
</tr>
</table>
END
;
&closebox();

# START NEW CURRENT STATIC ASSIGNMENT BOX
if ($dhcpsettings{'SHOW_STATIC'} eq 'on'){
	&openbox($tr{'current static assignments'});
	$alive_static = 0;
	$unreachable_static = 0;
	if (open (LEASES, "/$swroot/dhcp/tempstatic_$dhcpsettings{'SUBNET'}")) {
		while (<LEASES>) {
			$alive_static++ if /Machine Powered ON/;
			$unreachable_static++ if /Machine OFF/;
		}
		close (LEASES);
	} else {
		$errormessage .= "Couldn't open tempstatic for $dhcpsettings{'SUBNET'}<br />";
	}

	print <<END
<table style='width: 25%; border: 1px solid; margin-left:auto; margin-right:auto'>
<tr>
	<td style='text-align: center; background-color: #E9E8E8;'>
		<span style='color:#03BB03; font-weight:bold;'>Alive: $alive_static</span> - 
		<span style='color:red; font-weight:bold;'>Unreachable: $unreachable_static</span></td>
</tr>
</table>
<br />
END
;
	my %render_settings =
	(
		'url'     => "/cgi-bin/dhcp.cgi?[%COL%],[%ORD%],$dhcpsettings{'COLUMN_TWO'},$dhcpsettings{'ORDER_TWO'},$subnet",
		'columns' =>
		[
			{
				column => '1',
				title  => "Hostname",
				size   => 30,
				sort   => 'cmp',
				maxrowspan => 2,
			},
			{
				column => '3',
				title  => "IP address",
				size   => 20,
				sort   => \&ipcompare,
			},
			{
				column => '2',
				title  => "MAC Address",
				size   => 20,
				sort   => 'cmp',
			},
			{
				column => '6',
				title  => "$tr{'enabledtitle'}",
				size   => 10,
				rotate => 60,
				tr     => 'onoff',
				align  => 'center',
			},
			{
				column => '5',
				title  => "Active",
				size   => 10,
				rotate => 60,
				sort   => 'cmp',
			},
			{
				title  => "$tr{'mark'}",
				mark   => ' ',
				rotate => 60,
				align  => 'center',
			},
			{
				column => '4',
				title  => "$tr{'description'}",
				break  => 'line',
				align  => 'left',
				spanadj => -1,
			}
		]
	);

	&displaytable("/$swroot/dhcp/tempstatic_$dhcpsettings{'SUBNET'}", \%render_settings, $dhcpsettings{'ORDER_ONE'}, $dhcpsettings{'COLUMN_ONE'} );

}
else {

# START ORIGINAL CURRENT STATIC ASSIGNMENT BOX
	&openbox($tr{'current static assignments'});
	my %render_settings =
	(
		'url'     => "/cgi-bin/dhcp.cgi?[%COL%],[%ORD%],$dhcpsettings{'COLUMN_TWO'},$dhcpsettings{'ORDER_TWO'},$subnet",
		'columns' =>
		[
			{ 
				column     => '1',
				title      => "$tr{'hostname'}",
				size       => 30,
				maxrowspan => 2,
				sort       => 'cmp',
			},
			{
				column     => '3',
				title      => "$tr{'ip address'}",
				size       => 25,
				sort       => \&ipcompare,
			},
			{
				column     => '2',
				title      => "$tr{'mac address'}",
				size       => 25,
				sort       => 'cmp',
			},
			{
				column     => '5',
				title      => "$tr{'enabledtitle'}",
				size       => 10,
				rotate     => '60',
				tr         => 'onoff',
				align      => 'center',
			},
			{
				title  => "$tr{'mark'}",
				mark   => ' ',
				rotate => 60,
				align  => 'center',
			},
			{ 
				column     => '4',
				title      => "$tr{'description'}",
				break      => 'line',
				align      => 'left',
				spanadj    => -1,
			}
		]
	);

#	&displaytable( "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}", \%render_settings, $dhcpsettings{'ORDER_ONE'}, $dhcpsettings{'COLUMN_ONE'} );
	open (STATIC, "<", "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}");
	my @staticconfig = <STATIC>;
	close (STATIC);
	for (my $i=0; $i<=$#staticconfig; $i++) {
		my @temp = split (/\,/,$staticconfig[$i]);
		# Ah, this line is supposed to strip the HTML out of the settings file. But only the temp settings file.
		my $vendor = &macvendor($temp[1] =~ /(([0-9A-F]{2}:){5}[0-9A-F]{2})/);
		$staticconfig[$i] =~ s+,(([0-9A-F]{2}:){5}[0-9A-F]{2}),+,<span onMouseOver='return Tip(\"$vendor\");' onmouseout='UnTip();'>$1</span>,+;
		$staticconfig[$i] =~ s/,/|/g;
	}
	&displaytable( \@staticconfig, \%render_settings, $dhcpsettings{'ORDER_ONE'}, $dhcpsettings{'COLUMN_ONE'} );
}

print <<END
<table class='blank'>
<tr>
	<td style='text-align: center; width: 50%;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
	<td style='text-align: center; width: 50%;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();
&closebox();
&note if (-e "${swroot}/dhcp/uptodate");

print <<END
</div></form>
<table width='100%'>
  <td align='right'>
    <p style='font-size:8pt; margin:0 1em 0 0'>
      <i>Adapted from DHCP-WoL vSW3.1-V3.0</i>
    </p>
  </td>
</tr>
</table>
<br>
END
;
#print "&emsp;Took ".(time - $^T)." Secs";
&closepage();

# CLEAN LEASES
sub clean_leases {
	message('dhcpdclean');
}


# IP2#
sub ip2number {
	my $ip = $_[0];

	if (!($ip =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/)) {
		return 0;
	}
	else {
		return ($1*(256*256*256))+($2*(256*256))+($3*256)+($4);
	}
}


# SAVE
sub action_save {
	unless ($dhcpsettings{'NIS_DOMAIN'} eq "" || $dhcpsettings{'NIS_DOMAIN'} =~ /^([a-zA-Z])+([\.a-zA-Z0-9_-])+$/) {
		$errormessage .= $tr{'invalid domain name'}."<br />";
	}

	if ($dhcpsettings{'SUBNET'} ne 'green' && $dhcpsettings{'SUBNET'} ne 'purple' && $dhcpsettings{'SUBNET'} ne 'orange') {
		$errormessage .= $tr{'invalid input'}."<br />";
	}

	if ($dhcpsettings{'SUBNET'} ne $dhcpsettings{'CHECKSUBNET'}) {
		$errormessage .= $tr{'dhcpwol-select'}."<br />";
	}

	# Start and End must be set
	if ($dhcpsettings{'ENABLE'} eq "on" && $dhcpsettings{'START_ADDR'} eq "") {
		$errormessage .= $tr{'invalid start address'}."<br />";
	}
	if ($dhcpsettings{'ENABLE'} eq "on" && $dhcpsettings{'END_ADDR'} eq "") {
		$errormessage .= $tr{'invalid end address'}."<br />";
	}

	# If set, Start and End must be correct
	if ($dhcpsettings{'START_ADDR'} ne "" && $dhcpsettings{'END_ADDR'} ne "") {
		if (!(&validip($dhcpsettings{'START_ADDR'}))) {
			$errormessage .= $tr{'invalid start address'}."<br />";
		}
	
		if (!(&validip($dhcpsettings{'END_ADDR'}))) {
			$errormessage .= $tr{'invalid end address'}."<br />";
		}
	
		if (!(&ip2number($dhcpsettings{'END_ADDR'}) > &ip2number($dhcpsettings{'START_ADDR'}))) {
			$errormessage .= $tr{'end must be greater than start'}."<br />";
		}
	}

	if (open (FILE, "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}")) {
		my @current = <FILE>;
		close(FILE);

		foreach my $line (@current) {
			chomp ($line);
			my @temp = split (/\,/,$line);
			if ($temp[4] eq 'on') {
				unless(!((&ip2number($temp[2]) <= &ip2number($dhcpsettings{'END_ADDR'}) && (&ip2number($temp[2]) >= &ip2number($dhcpsettings{'START_ADDR'}))))) {
					$errormessage .= $tr{'dynamic range cannot overlap static'}."<br />";
					# Only report once
					last;
				}
			}
		}
	} else {
		$errormessage .= "Unable to open $dhcpsettings{'SUBNET'} static settings<br />";
	}

	if ($dhcpsettings{'DNS1'}) {
		$errormessage .= $tr{'invalid primary dns'}."<br />" if (!(&validip($dhcpsettings{'DNS1'})));
	}

	if (!($dhcpsettings{'DNS1'}) && $dhcpsettings{'DNS2'}) {
		$errormessage .= $tr{'cannot specify secondary dns without specifying primary'}."<br />";
	}

	if ($dhcpsettings{'DNS2'}) {
		$errormessage .= $tr{'invalid secondary dns'}."<br />" if (!(&validip($dhcpsettings{'DNS2'})));
	}

	if ($dhcpsettings{'NTP1'}) {
		$errormessage .= $tr{'invalid primary ntp'}."<br />" if (!(&validip($dhcpsettings{'NTP1'})));
	}

	if (!($dhcpsettings{'NTP1'}) && $dhcpsettings{'NTP2'}) {
		$errormessage .= $tr{'cannot specify secondary ntp without specifying primary'}."<br />";
	}

	if ($dhcpsettings{'NTP2'}) {
		$errormessage .= $tr{'invalid secondary ntp'}."<br />" if (!(&validip($dhcpsettings{'NTP2'})));
	}

	if (!($dhcpsettings{'WINS1'}) && $dhcpsettings{'WINS2'}) {
		$errormessage .= $tr{'cannot specify secondary wins without specifying primary'}."<br />";
	}

	if ($dhcpsettings{'WINS1'}) {
		$errormessage .= $tr{'invalid primary wins'}."<br />" if (!(&validip($dhcpsettings{'WINS1'})));
	}

	if ($dhcpsettings{'WINS2'}) {
		$errormessage .= $tr{'invalid secondary wins'}."<br />" if (!(&validip($dhcpsettings{'WINS2'})));
	}

	if (!($dhcpsettings{'DNS1'}) && $dhcpsettings{'DNS2'}) {
		$errormessage .= $tr{'cannot specify secondary dns without specifying primary'}."<br />";
	}

	if (!($dhcpsettings{'NIS_DOMAIN'}) && $dhcpsettings{'NIS1'}) {
		$errormessage .= $tr{'cannot specify nis server without specifying nis domain'}."<br />";
	}

	if (!($dhcpsettings{'NIS1'}) && $dhcpsettings{'NIS2'}) {
		$errormessage .= $tr{'cannot specify secondary nis without specifying primary'}."<br />";
	}

	if ($dhcpsettings{'NIS1'}) {
		$errormessage .= $tr{'invalid primary nis'}."<br />" if (!(&validip($dhcpsettings{'NIS1'})));
	}

	if ($dhcpsettings{'NIS2'}) {
		$errormessage .= $tr{'invalid secondary nis'}."<br />" if (!(&validip($dhcpsettings{'NIS2'})));
	}

	unless (!$dhcpsettings{'DOMAIN_NAME'} || $dhcpsettings{'DOMAIN_NAME'} =~ /^([a-zA-Z])+([\.a-zA-Z0-9_-])+$/) {
		$errormessage .= $tr{'invalid domain name'}."<br />";
	}

	if (!($dhcpsettings{'DEFAULT_LEASE_TIME'} =~ /^\d+$/)) {
		$errormessage .= $tr{'invalid default lease time'}."<br />";
	}

	if (!($dhcpsettings{'MAX_LEASE_TIME'} =~ /^\d+$/)) {
		$errormessage .= $tr{'invalid max lease time'}."<br />";
	}

	unless ($errormessage) {

		my %tempsettings;

		for (qw/BOOT_ENABLE BOOT_SERVER BOOT_FILE BOOT_ROOT SHOW_NETSTAT SHOW_DYNAMIC SHOW_STATIC SHOW_STALE/) {
			$tempsettings{$_} = $dhcpsettings{$_};
		}
   
		&writehash("${swroot}/dhcp/global", \%tempsettings);
      
		for (qw/BOOT_ENABLE BOOT_SERVER BOOT_FILE BOOT_ROOT SHOW_NETSTAT SHOW_DYNAMIC SHOW_STATIC 
			SHOW_STALE STATIC_HOST STATIC_DESC STATIC_MAC STATIC_IP 
			DEFAULT_ENABLE_STATIC ORDER_ONE COLUMN_ONE ORDER_TWO COLUMN_TWO/) {
			delete $dhcpsettings{$_};
		}

		&writehash("${swroot}/dhcp/settings-$dhcpsettings{'SUBNET'}", \%dhcpsettings);

		$dhcpsettings{'STATIC_HOST'} = '';
		$dhcpsettings{'STATIC_DESC'} = '';
		$dhcpsettings{'STATIC_MAC'} = '';
		$dhcpsettings{'STATIC_IP'} = '';
		$dhcpsettings{'DEFAULT_ENABLE_STATIC'} = 'on';

		$dhcpsettings{'COLUMN_ONE'} = 2;
		$dhcpsettings{'ORDER_ONE'} = $tr{'log ascending'};
		$dhcpsettings{'COLUMN_TWO'} = 2;
		$dhcpsettings{'ORDER_TWO'} = $tr{'log ascending'};

		system("/usr/bin/smoothwall/writedhcp.pl");

		unlink ("${swroot}/dhcp/uptodate");

		$success = message('dhcpdrestart');
		$infomessage .= "$success<br />" if ($success);
		$errormessage .= "DHCP RESTART: $tr{'smoothd failure'}<br />" unless ($success);

		system('/usr/bin/smoothwall/writehosts.pl');

		$success = message('dnsproxyhup');
		$infomessage .= "$success<br />" if ($success);
		$errormessage .= "DNSProxy SIGHUP: $tr{'smoothd failure'}<br />" unless ($success);
		&readhash("${swroot}/dhcp/global", \%dhcpsettings);

		# Save the IF we're dealing with so we can display it again.
		&writevalue("/$swroot/dhcp/ifcol", $dhcpsettings{'SUBNET'});
	}
}


# ADD
sub action_add {
	my ($iface, $ifsubnet, $ifmask, $mac);

	# Get the current interface network/Mask
	if ($dhcpsettings{'SUBNET'} eq 'green') { 
		$ifsubnet = $netsettings{'GREEN_NETADDRESS'};
		$ifmask = $netsettings{'GREEN_NETMASK'};
	}
	elsif ($dhcpsettings{'SUBNET'} eq 'orange') {
		$ifsubnet = $netsettings{'ORANGE_NETADDRESS'};
		$ifmask = $netsettings{'ORANGE_NETMASK'};
	}
	elsif ($dhcpsettings{'SUBNET'} eq 'purple') { 
		$ifsubnet = $netsettings{'PURPLE_NETADDRESS'};
		$ifmask = $netsettings{'PURPLE_NETMASK'};
	}

	# Check the IP address is within the network
	my $withinnetwork = 0;
	$withinnetwork = ( in_subnet( $dhcpsettings{'STATIC_IP'}, "$ifsubnet\/$ifmask" ) ) if ($dhcpsettings{'STATIC_IP'});

	# Munge the MAC into something good.
	if ($dhcpsettings{'STATIC_MAC'} =~ /^(([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2})$/) {
		$mac = $dhcpsettings{'STATIC_MAC'};
		$mac =~ s/[^0-9a-f]//ig;
		$mac = uc($mac);
		$mac =~ /^(..)(..)(..)(..)(..)(..)$/;
		$mac = "$1:$2:$3:$4:$5:$6";
	}
	$dhcpsettings{'STATIC_MAC'} = $mac if (&validmac($mac));

	# Error checking:
	$errormessage .= "$tr{'dhcpwol-nohost'}<br />" unless ($dhcpsettings{'STATIC_HOST'});
	$errormessage .= "$tr{'dhcpwol-invalidhost'}<br />" unless ($dhcpsettings{'STATIC_HOST'} =~ /^([a-zA-Z])+([\.a-zA-Z0-9_-])+$/);
	$errormessage .= "$tr{'mac address not valid'}<br />" unless (&validmac($dhcpsettings{'STATIC_MAC'}));
	$errormessage .= "$tr{'ip address not valid'}<br />" unless (&validip($dhcpsettings{'STATIC_IP'}));
	$errormessage .= "$tr{'dhcpwol-IP address not'} of: <span style='font-weight:bold;'>".$ifsubnet." \/ ".$ifmask."</span><br />" unless ($withinnetwork==1);
	$errormessage .= "$tr{'description contains bad characters'}<br />" unless($dhcpsettings{'STATIC_DESC'} =~ /^([a-zA-Z 0-9]*)$/);
	if ($dhcpsettings{'DEFAULT_ENABLE_STATIC'} eq 'on') {
		$errormessage .= "$tr{'static must be outside dynamic range'}<br />" unless (!((&ip2number($dhcpsettings{'STATIC_IP'}) <= &ip2number($dhcpsettings{'END_ADDR'}) && (&ip2number($dhcpsettings{'STATIC_IP'}) >= &ip2number($dhcpsettings{'START_ADDR'})))));
	}

	open (FILE, "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") || die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	foreach my $line (@current) {
		chomp($line);
		my @temp = split (/\,/,$line);
		if ($dhcpsettings{'DEFAULT_ENABLE_STATIC'} eq 'on') {

			my ( $cleanmac ) = $temp[1] =~ /(([0-9A-F]{2}:){5}[0-9A-F]{2})/;

			if (($dhcpsettings{'STATIC_HOST'} eq $temp[0]) && ($temp[4] eq 'on')) {
				$errormessage .= "$tr{'hostnamec'} <span style='font-weight:bold;'>$temp[0]</span> $tr{'already exists and has assigned ip'} $tr{'ip address'} <span style='font-weight:bold;'>$temp[2]</span><br />";
			}
			if (($dhcpsettings{'STATIC_MAC'} eq $cleanmac) && ($temp[4] eq 'on')) {
				$errormessage .= "$tr{'mac address'} <span style='font-weight:bold;'>$temp[1]</span> ($tr{'hostnamec'} $temp[0]) $tr{'already assigned to ip'} $tr{'ip address'} <span style='font-weight:bold;'>$temp[2]</span><br />";
			}
			if (($dhcpsettings{'STATIC_IP'} eq $temp[2]) && ($temp[4] eq 'on')) {
				$errormessage .= "$tr{'ip address'} <span style='font-weight:bold;'>$temp[2]</span> $tr{'ip already assigned to'} $tr{'mac address'} <span style='font-weight:bold;'>$temp[1]</span> ($tr{'hostnamec'} $temp[0])<br />";
			}
		}
	}



	unless ($errormessage) {
		open (FILE, ">>${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") || die 'Unable to open config file.';
		flock FILE, 2;
		my $vendor = &macvendor($dhcpsettings{'STATIC_MAC'});
		print FILE "$dhcpsettings{'STATIC_HOST'},$dhcpsettings{'STATIC_MAC'},$dhcpsettings{'STATIC_IP'},$dhcpsettings{'STATIC_DESC'},$dhcpsettings{'DEFAULT_ENABLE_STATIC'}\n";
		close(FILE);
	
		for (qw/STATIC_HOST STATIC_MAC STATIC_IP STATIC_DESC DEFAULT_ENABLE_STATIC/) {
			$dhcpsettings{$_} = '';
			$dhcpsettings{'DEFAULT_ENABLE_STATIC'} = 'on';
			
		}
		system ('/bin/touch', "${swroot}/dhcp/uptodate");
	}
}


# REMOVE & EDIT
sub action_remove_edit {
	open (FILE, "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") || die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $count = 0;
	my $id = 0;
	my $line;
	foreach $line (@current) {
		$id++;
		$count++ if (($dhcpsettings{$id}) && $dhcpsettings{$id} eq "on");
	}
	$errormessage .= $tr{'nothing selected'} ."<br />" if ($count == 0);
	$errormessage .= $tr{'you can only select one item to edit'} ."<br />" if ($count > 1 && $dhcpsettings{'ACTION'} eq $tr{'edit'});

	unless ($errormessage) {
		open (FILE, ">${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") || die 'Unable to open config file.';
		flock FILE, 2;
		$id = 0;
		foreach $line (@current) {
			$id++;
			unless (($dhcpsettings{$id}) && $dhcpsettings{$id} eq "on") {
				print FILE "$line";
			}
			elsif ($dhcpsettings{'ACTION'} eq $tr{'edit'}) {
				chomp($line);
				my @temp = split (/\,/,$line);
				$dhcpsettings{'STATIC_HOST'} = $temp[0];
				( $temp[1] ) = $temp[1] =~ m/(([0-9A-F]{2}:){5}[0-9A-F]{2})/; # Clean up the MAC.
				$dhcpsettings{'STATIC_MAC'} = $temp[1];
				$dhcpsettings{'STATIC_IP'} = $temp[2];
				$dhcpsettings{'STATIC_DESC'} = $temp[3] || '';
				$dhcpsettings{'DEFAULT_ENABLE_STATIC'} = $temp[4];
			}
		}
		close(FILE);
		unless ($dhcpsettings{'ACTION'} eq $tr{'edit'}) {
			system ('/bin/touch', "${swroot}/dhcp/uptodate");
		}
	}
}


# NOTHING & SELECT
sub action_nothing_select {
	my $c = $dhcpsettings{'COLUMN_ONE'};
	my $o = $dhcpsettings{'ORDER_ONE'};
	my $d = $dhcpsettings{'COLUMN_TWO'};
	my $p = $dhcpsettings{'ORDER_TWO'};

	if ($dhcpsettings{'ACTION'} eq '') {
		$subnet = "green" if ($subnet eq '');	# Set the default interface
		$subnet = $cgiparams{'subnet'} if ($cgiparams{'subnet'}); # Overwrite it if returning from a 'wakeup'.
	}
	else {
		$subnet = $dhcpsettings{'SUBNET'};		# Or use the IF setting if there's an ACTION.
	}

	&ifcolor;
	undef %dhcpsettings;

	$dhcpsettings{'START_ADDR'} = '';
	$dhcpsettings{'END_ADDR'} = '';
	$dhcpsettings{'DNS1'} = '';
	$dhcpsettings{'DNS2'} = '';
	$dhcpsettings{'NTP1'} = '';
	$dhcpsettings{'NTP2'} = '';
	$dhcpsettings{'NIS1'} = '';
	$dhcpsettings{'NIS2'} = '';
	$dhcpsettings{'WINS1'} = '';
	$dhcpsettings{'WINS2'} = '';
	$dhcpsettings{'DOMAIN_NAME'} = '';
	$dhcpsettings{'NIS_DOMAIN'} = '';

	$dhcpsettings{'BOOT_SERVER'} = '';
	$dhcpsettings{'BOOT_FILE'} = '';
	$dhcpsettings{'BOOT_ROOT'} = '';
	$dhcpsettings{'BOOT_ENABLE'} = 'off';

 	$dhcpsettings{'ENABLE'} = 'off';
	$dhcpsettings{'DEFAULT_LEASE_TIME'} = '60';
	$dhcpsettings{'MAX_LEASE_TIME'} = '120';

	$dhcpsettings{'SHOW_NETSTAT'} = 'off';
	$dhcpsettings{'SHOW_DYNAMIC'} = 'off';
	$dhcpsettings{'SHOW_STALE'} = 'off';
	$dhcpsettings{'SHOW_STATIC'} = 'off';

	$dhcpsettings{'STATIC_HOST'} = '';
	$dhcpsettings{'STATIC_DESC'} = '';
	$dhcpsettings{'STATIC_MAC'} = '';
	$dhcpsettings{'STATIC_IP'} = '';
	$dhcpsettings{'DEFAULT_ENABLE_STATIC'} = 'on';
	$dhcpsettings{'DENYUNKNOWN'} = 'off';

	$dhcpsettings{'COLUMN_ONE'} = $c;
	$dhcpsettings{'ORDER_ONE'} = $o;
	$dhcpsettings{'COLUMN_TWO'} = $d;
	$dhcpsettings{'ORDER_TWO'} = $p;

	&readhash("${swroot}/dhcp/global", \%dhcpsettings);
	&readhash("${swroot}/dhcp/settings-$subnet", \%dhcpsettings);
	$dhcpsettings{'SUBNET'} = $subnet;
	$noscan = 1 unless (($errormessage) || ($ENV{'QUERY_STRING'}));
}

# DHCP LEASE CODE
sub dhcp_lease_table {
	### Simple DHCP Lease Viewer (2007-0905) put together by catastrophe
	# - Borrowed "dhcpLeaseData" subroutine from dhcplease.pl v0.2.5 (DHCP Pack v1.3) for SWE2.0
	# by Dane Robert Jones and Tiago Freitas Leal
	# - Borrowed parts of "displaytable" subroutine from smoothtype.pm
	# (SmoothWall Express "Types" Module) from SWE3.0 by the SmoothWall Team
	# - Josh DeLong - 09/15/07 - Added unique filter
	# - Josh DeLong - 09/16/07 - Fixed sort bug and added ability to sort columns
	# - Josh DeLong - 10/1/07 - Rewrote complete dhcp.cgi to use this code
	###

	my $match = 0;
	my $leaseCount = -1;
	my $dhcptmpfile = "/$swroot/dhcp/tempfile";
	my $dhcpstart = substr($dhcpsettings{'START_ADDR'}, 0, rindex($dhcpsettings{'START_ADDR'}, ".") + 1);

	my (@dhcplIPAddy, @dhcplStart, @dhcplEnd, @dhcplMACAddy, @dhcplHostName, @dhcplState, @dhcplBinding);
	my (%leasecounter, %dupcounter);

	$alive_dyn = 0;
	$unreachable_dyn = 0;
			
	# Load the DHCP Lease File into an array
	open (LEASES, "/usr/etc/dhcpd.leases") || die "Unable to open $!"; 
	my @leasesFILENAME = (<LEASES>); 
	close (LEASES);
	chomp (@leasesFILENAME);

	foreach my $i (0..$#leasesFILENAME) {
		my $datLine = $leasesFILENAME[$i];

		next if ($datLine =~ /^\s*#/);	# Skip comment lines
		next if ($datLine eq '');		# Skip empty lines

		for ($datLine) {
			# Remove open brace, double quotes, end ';' and leading/training spaces, 
			s/\{|\"|\;//g;
			s/^\s+//;
			s/\s+$//;
		}

		if ($datLine =~ /^lease\s+((\d+\.){3}\d+)/) {
			$leasecounter{$datLine} = grep { /$datLine/ } @leasesFILENAME;	# How many leases for this address are there?
			$dupcounter{$datLine} = 0 unless ($dupcounter{$datLine});	# Set this counter to 0 if it's the first time seen.
			$dupcounter{$datLine}++;						# Increment the counter every time we see this lease.

			next if ($leasecounter{$datLine} > $dupcounter{$datLine});	# Skip unless it's the last entry.

			$match = 1;								# Mark as a last match.
			$leaseCount++;							# Increment the number of valid leases found.
			$dhcplIPAddy[$leaseCount] = $1;					# Get IP address.
			next;									# Move on to next line if we have a match.
		}
		if ($datLine =~ /^starts\s+\d*\s*(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2})/) {
			$dhcplStart[$leaseCount] = $1 if ($leaseCount > -1 && $match == 1);	# Get lease start date & time.
			next;
		}
		if ($datLine =~ /^ends\s+\d*\s*(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2})/) {
			$dhcplEnd[$leaseCount] = $1 if ($leaseCount > -1 && $match == 1);	# Get lease end date & time.
			next;
		}
		if ($datLine =~ /^hardware ethernet\s+(([0-9a-f]{2}:){5}[0-9a-f]{2})/) {
			$dhcplMACAddy[$leaseCount] = uc($1) if ($leaseCount > -1 && $match == 1);	# Get MAC address & make Upper Case.
			next;
		}
		if ($datLine =~ /^(client-)?hostname\s+(.+)$/) {
			$dhcplHostName[$leaseCount] = $2 if ($leaseCount > -1 && $match == 1);	# Get hostname
			next;
		}
		$match = 0 if ($datLine =~ /^\}/);						# Reset the match marker.
	}

	&get_broadcast;
	&arpscan if ($noscan == 1);

	open (FILE, ">$dhcptmpfile") || die 'Unable to open dhcp tempfile file.';
	flock FILE, 2;

	for (my $i = $#dhcplIPAddy; $i >= 0; $i--) {
		my $LINEnumber = $i+1;
		my $dhcpprintvar = "True";
		my (@dhcptemparray, @dhcplstate);

		if ($i eq $#dhcplIPAddy) {
			push(@dhcptemparray, $dhcplIPAddy[$i]);
		}
		else {
			foreach my $IP (@dhcptemparray) {
				$dhcpprintvar = "False" if ($IP =~ $dhcplIPAddy[$i]);
			}
		}

		$dhcpprintvar = "False" if (index($dhcplIPAddy[$i], $dhcpstart) == -1 );

		my $vendor = &macvendor($dhcplMACAddy[$i]);
		my ( $cleanmac ) = $dhcplMACAddy[$i] =~ /(([0-9A-F]{2}:){5}[0-9A-F]{2})/;

		# Printing values to temp file
		if ($dhcpprintvar =~ "True") {
			my $leaseStart = UTC2LocalString($dhcplStart[$i]);
			my $leaseEnd   = UTC2LocalString($dhcplEnd[$i]);
			$dhcplHostName[$i] ||= '';

			if ($dhcpsettings{'SHOW_STALE'} eq 'on') {
				push(@dhcptemparray, $dhcplIPAddy[$i]);

				if (&scanlist ($dhcplIPAddy[$i])) {
					# Click to prefill static assignment with dynamic one  (original idea: Dane Jones. Included by Tiago in DHCP pack v.1.3 for SWE 2.0) 
					$dhcplstate[$i] = "<a href='#statichost' onClick=\"javascript: document.myform.STATIC_HOST.value = ''; document.myform.STATIC_DESC.value = ''; document.myform.STATIC_MAC.value = '$dhcplMACAddy[$i]'; document.myform.STATIC_IP.value = '$dhcplIPAddy[$i]'; AutoFillStaticHost(); // return false;\"><img src='/ui/img/ok.png' TITLE='Host is ON; click to pre-fill new static assignment' alt='OK'></a>,on";
					$alive_dyn++;
					push(@dhcptemparray,$dhcplstate[$i])
				}
				else {
					# WOL mod by English Neo adapted from SWE 2.0
					$dhcplstate[$i] = "<a href='dhcp.cgi?wakemac&#61;$cleanmac&amp;wakebc&#61;$broadcast&amp;subnet&#61;$dhcpsettings{'SUBNET'}'><img src='/ui/img/na.png' TITLE='Host is OFF; click to turn host on' ALT='OFF'></a>,off";
					$unreachable_dyn++;
				}
				print FILE "$LINEnumber,$dhcplIPAddy[$i],$leaseStart,$leaseEnd,<span onMouseOver='return Tip(\"$vendor\");' onmouseout='UnTip();'>$dhcplMACAddy[$i]</span>,$dhcplHostName[$i],$dhcplstate[$i],\n";
			}
			else {
				if ($dhcplEnd[$i] gt $timenow ) {
					push(@dhcptemparray, $dhcplIPAddy[$i]);
					# WOL mod by English Neo adapted from SWE 2.0
					$dhcplstate[$i] = "<a href='dhcp.cgi?wakemac&#61;$cleanmac&amp;wakebc&#61;$broadcast&amp;subnet&#61;$dhcpsettings{'SUBNET'}'><img src='/ui/img/na.png' TITLE='Host is OFF; click to turn host ON' ALT='OFF'></a>,off";

					if (&scanlist ($dhcplIPAddy[$i])) {
						$dhcplstate[$i] = "<a href='#statichost' onClick=\"javascript: document.myform.STATIC_HOST.value = ''; document.myform.STATIC_DESC.value = ''; document.myform.STATIC_MAC.value = '$dhcplMACAddy[$i]'; document.myform.STATIC_IP.value = '$dhcplIPAddy[$i]'; AutoFillStaticHost(); // return false;\"><img src='/ui/img/ok.png' TITLE='Host is ON; click to pre-fill new static assignment' alt='OK'></a>,on";
						push(@dhcptemparray,$dhcplstate[$i])
					}
					print FILE "$LINEnumber,$dhcplIPAddy[$i],$leaseStart,$leaseEnd,<span onMouseOver='return Tip(\"$vendor\");' onmouseout='UnTip();'>$dhcplMACAddy[$i]</span>,$dhcplHostName[$i],$dhcplstate[$i],\n";
				}
			}
		}
	}
	close(FILE);
}

# START STATIC ASSIGNMENT STATUS CODE
sub dhcp_static_table {
	my $base = "/$swroot/dhcp";
	my @scanstatic;

	# Which interfaces have static hosts?
	my @static_files = ( 'green' );
	push (@static_files, 'purple') if ($netsettings{'PURPLE_DEV'} && -s "${swroot}/dhcp/staticconfig-purple");
	push (@static_files, 'orange') if ($netsettings{'ORANGE_DEV'} && -s "${swroot}/dhcp/staticconfig-orange");

	## Scan for live hosts. P de L 18/9/2009
	if ($noscan == 1) {
		&arpscan unless ($dhcpsettings{'SHOW_DYNAMIC'} eq 'on');
	}

	foreach my $file (@static_files) {
		open (IN, "<${swroot}/dhcp/staticconfig-$file") || die "Unable to open staticconfig-$file file.";
		open (OUT, ">$base/tempstatic_$file") || die "Unable to open tempstatic_$file file.";

		while (<IN>) {
			chomp ($_);
			my @temp = split (/,/);

			my ( $cleanmac ) = $temp[1] =~ /(([0-9A-F]{2}:){5}[0-9A-F]{2})/;
			my $vendor = &macvendor($cleanmac);

			if (&scanlist($temp[2])) {
				print OUT "$temp[0],<span onMouseOver='return Tip(\"$vendor\");' onmouseout='UnTip();'>$temp[1]</span>,$temp[2],$temp[3],<img src='/ui/img/ok.png' TITLE='Host is ON' alt='ON'>,$temp[4]\n";
			}
			else {
				print OUT "$temp[0],<span onMouseOver='return Tip(\"$vendor\");' onmouseout='UnTip();'>$temp[1]</span>,$temp[2],$temp[3],<a href='dhcp.cgi?wakemac&#61;$cleanmac&amp;wakebc&#61;$broadcast&amp;subnet&#61;$dhcpsettings{'SUBNET'}'>";
				print OUT "<img src='/ui/img/na.png' TITLE='Host is OFF; click to turn host ON' ALT='OFF'></a>,$temp[4]\n";
			}
		}
		close (IN);
		close (OUT);
	}
}

# Note box
sub note {
	&openbox($tr{'note'});
	print <<END;
<table class='centered'>
<tr>
	<td class='base' style='width: 80%; text-align: center;'><span style='color: red; font-size: 1.2em; font-weight: bold;'>$tr{'there are unsaved changes'}</span></td>
</tr>
</table>
END
	&closebox();
}

# Get Broadcast
sub get_broadcast {
	$broadcast = $netsettings{'GREEN_BROADCAST'} if ($dhcpsettings{'SUBNET'} eq 'green');
	$broadcast = $netsettings{'ORANGE_BROADCAST'} if ($dhcpsettings{'SUBNET'} eq 'orange');
	$broadcast = $netsettings{'PURPLE_BROADCAST'} if ($dhcpsettings{'SUBNET'} eq 'purple');
}

# Get IF
sub ifcolor {
	$ifcolor = 'green' if ($subnet =~ /green/i);
	$ifcolor = 'purple' if ($subnet =~ /purple/i);
	$ifcolor = 'orange' if ($subnet =~ /orange/i);
}

# Scan the current network for live hosts
sub arpscan {
	# Get the current interface
	my ($iface, $ifsubnet, $ifmask, $name, $MAC, $IP, $key, $brace, $num, $date, @scanlist);

	if ($dhcpsettings{'SUBNET'} eq 'green') {
		$iface = $netsettings{'GREEN_DEV'}; 
		$ifsubnet = $netsettings{'GREEN_NETADDRESS'};
		$ifmask = $netsettings{'GREEN_NETMASK'};
	}
	elsif ($dhcpsettings{'SUBNET'} eq 'orange') {
		$iface = $netsettings{'ORANGE_DEV'}; 
		$ifsubnet = $netsettings{'ORANGE_NETADDRESS'};
		$ifmask = $netsettings{'ORANGE_NETMASK'};
	}
	elsif ($dhcpsettings{'SUBNET'} eq 'purple') {
		$iface = $netsettings{'PURPLE_DEV'}; 
		$ifsubnet = $netsettings{'PURPLE_NETADDRESS'};
		$ifmask = $netsettings{'PURPLE_NETMASK'};
	}

	if ($dhcpsettings{'SHOW_STATIC'} eq 'on') {
		# Get the static assignments for current IF and push into an array.
		open (STATIC, "</var/smoothwall/dhcp/staticconfig-$subnet") || die "Can't open $subnet static file!";
		while (<STATIC>) {
			chomp;
			($name, $MAC, $IP) = split (/,/);
			push @scanlist, "$IP\n";
		}
		close (STATIC);
	}

	# Get the active leases for current IF and push into an array.
	open (LEASES, "</usr/etc/dhcpd.leases") || die "Can't open dhcpd.leases!";
	while (<LEASES>) {
		chomp;
		if ($_ =~ /^lease/) {
			($key, $IP, $brace) = split (/\s+/);
			next;
		}
		if ($_ =~ /^\s+ends/) {
			$_ =~ s/^\s+//;	# Remove leading spaces.
			($key, $num, $date) = split (/\s+/, $_, 3);
			$date =~ s/;//;
			my $withinnetwork = ( &in_subnet( $IP, "$ifsubnet\/$ifmask" ) ) if ($IP);
			# Verify the lease is unexpired, the IP is in the LAN and it isn't a duplicate.
			push @scanlist, "$IP\n" if (($IP) && $date gt $timenow && $withinnetwork == 1 && ((grep { /$IP/ } @scanlist) == 0));
			next;
		}
	}
	close (LEASES);

	# Print the scanlist array to a file.
	open (ARPLIST, ">/$swroot/dhcp/scanip") || die "Can't open scanip!";
	print ARPLIST @scanlist;
	close (ARPLIST);

	#Use the file created to scan for live hosts
	system ("/sbin/fping -c 1 -t 200 -f /$swroot/dhcp/scanip >/dev/null 2>&1");
	@list = `ip n show`;
	unlink ("/$swroot/dhcp/scanip");
}

# Scans the array produced to check if the current host is live.
sub scanlist {
	return (grep { /^$_[0]\s+.*lladdr/ } @list);
}

# Match the MAC Vendor
sub macvendor {
	my $manmac = $_[0];
	$manmac =~ s/://g;
	$manmac = substr($manmac, 0, 6);

	my $vendor = $oui_vendor_html{$manmac};
	$vendor = "Unknown Vendor" unless defined $vendor;

	return $vendor;
}

# Check if IP is within subnet
sub in_subnet($$) {
	my $newip = shift;
	my $ifsubnet = shift;

	my $ip_long = ip2long( $newip );

	if( $ifsubnet=~ m|(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$| ) {
		my $ifsubnet = ip2long($1);
		my $ifmask = ip2long($2);

		return 1 if( ($ip_long & $ifmask)==$ifsubnet );
	}
	return 0;
}

# Convert IP
sub ip2long($) {
	return( unpack( 'N', inet_aton(shift) ) );
}

# Send magic Packet
sub wakeup {
	# (c) 1999 by Marc Heuse <mheuse@kpmg.com>, the GPL applies to this code. 

	my $IP="255.255.255.0";				# limited broadcast ip (default) 
	my $SUBNET="green";					# subnet (default) 
	my $PORT="9";						# udp port (default) 
	my $INIT_STREAM="\377\377\377\377\377\377";	# (don't change this) 

	require 5.002; 
	use Socket; 

	my $ETHERNET_ID = $_[0];
	$IP = $_[1] if ($_[1]);
	$SUBNET = $_[2] if ($_[2]);
	$PORT = $_[3] if ($_[3]);

	my $protocol = getprotobyname('udp');
	socket(S, &PF_INET, &SOCK_DGRAM, $protocol) || die "can't create socket\n";
	setsockopt(S, SOL_SOCKET, SO_REUSEADDR, 1);
	setsockopt(S, SOL_SOCKET, SO_BROADCAST, 1);
	bind(S, sockaddr_in(0, INADDR_ANY)) || die "can't bind\n";

	my $ipaddr = inet_aton($IP) || die "unknown host: $IP\n";
	my $paddr = sockaddr_in($PORT, $ipaddr) || die "sockaddr failed\n";

	$ETHERNET_ID =~ s/[:-]//g;
	$ETHERNET_ID = pack "H12", $ETHERNET_ID;

	my $WAKE_UP = $INIT_STREAM;
	my $i=0;
	while ($i<16) {
		$WAKE_UP = $WAKE_UP . $ETHERNET_ID;
		$i++;
	}

	# send three times to be sure the system gets the packet
	send (S, $WAKE_UP,0,$paddr) || die "Send failed: $!\n";
	send (S, $WAKE_UP,0,$paddr);
	send (S, $WAKE_UP,0,$paddr);

	# Display a message then refresh the page.
	$infomessage .= "$tr{'dhcpwol-wakeup'}. MAC: <B>$cgiparams{'wakemac'}</B> Broadcast: <B>$cgiparams{'wakebc'}</B><br />";

	# Save the current interface to a temp file so we can reload the same page after the message display.
	&writevalue("/$swroot/dhcp/ifcol", $SUBNET);
}

sub infobox {
	my $thiserror = $_[0];
	my $additional = $_[1];
	if ( ($thiserror) && $additional eq 'info' ) {
		print "<br />";
		print "<table class='info'>";
		print "<tr>";
		print "	<td class='infoimg'><img src='/ui/img/Info.png' alt='info'></td><td class='info'>$thiserror</td>";
		print "</tr>";
		print "</table>";
	}
	else {
		&alertbox($thiserror);
	}
}
