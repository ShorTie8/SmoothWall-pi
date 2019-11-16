#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

my $graphcriticalcolour = "#ff0000";
my $graphwarningcolour  = "#ff5d00";
my $graphnominalcolour  = "#ffa200";
my $graphblankcolour    = "#ffffff";
my $graphbgcolour;

my $graphalertcritical = 90;
my $graphalertwarning  = 70;
my $errormessage = '';

&showhttpheaders();

&openpage($tr{'advanced status information'}, 1, '', 'about your smoothie');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

&openbox($tr{'memory'});

my @echo = `/usr/bin/free -ot`;
shift(@echo);

print <<END;
<br/>
<table style='width: 95%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th>&nbsp;</th>
	<th style='text-align: right; width: 6em'>$tr{'adv total'}</th>
	<th style='text-align: right; width: 6em'>$tr{'adv used'}</th>
	<th style='text-align: right; width: 6em'>$tr{'adv free'}</th>
	<th>&nbsp;</th>
	<th style='text-align: center; width: 150px;'>$tr{'adv used%'}</th>
	<th style='text-align: right; width: 6em;' >$tr{'adv shared'}</th>
	<th style='text-align: right; width: 6em;' >$tr{'adv buffers'}</th>
	<th style='text-align: right; width: 6em;' >$tr{'adv cached'}</th>
</tr>
END

foreach my $mline (@echo) {
	chomp($mline);

	my ($mdev, $mtotal, $mused, $mfree, $mshared, $mbuffers, $mcached) = split(/\s+/, $mline);
	my $mperc = 0;

	if ($mtotal) {
		$mperc = int((($mused/$mtotal)*100));
	}

	if ($mperc > $graphalertcritical) {
		$graphbgcolour = $graphcriticalcolour;
	} 
	elsif ($mperc > $graphalertwarning) {
		$graphbgcolour = $graphwarningcolour;
	}
	elsif ($mperc > 0) {
		$graphbgcolour = $graphnominalcolour;
	}
	else {
		$graphbgcolour = $graphblankcolour;
	}

	if ( $mdev eq "Total:" ) {
		print '<tr><td colspan="9"><hr></td></tr>';
	}
	if ($mdev eq 'Mem:') {
		$graphbgcolour = $graphnominalcolour;
	}
	print <<END;
<tr>
	<td style='text-align: right;'><code>$mdev</code></td>
	<td style='text-align: right;'><code>${mtotal}</code></td>
	<td style='text-align: right;'><code>${mused}K</code></td>
	<td style='text-align: right;'><code>${mfree}K</code></td>
	<td style='text-align: right;'><code>&nbsp;</code></td>
	<td style='text-align: right; width: 160px; white-space: nowrap;'>
		<table class='blank' style='width: 150px; border: 1px #505050 solid;'>
		<tr>
END

	if ($mperc < 1) {
		print "\t\t\t<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><code>$mperc%</code></td>\n";
	}
	else {
		print "\t\t\t<td style='background-color: $graphbgcolour; width: $mperc%; text-align: center;'><code>$mperc%</code></td>\n";
	}
	print <<END;
			<td style='background-color: $graphblankcolour;'>&nbsp;</td>
		</tr>
		</table></td>
END

	if ( (($mbuffers) && $mbuffers ne "") || (($mcached) && $mcached ne "") ) {
		print <<END;
	<td style='text-align: right;'><code>${mshared}K</code></td>
	<td style='text-align: right;'><code>${mbuffers}K</code></td>
	<td style='text-align: right;'><code>${mcached}K</code></td>
END
	}
	else {
		print <<END;
	<td></td>
	<td></td>
	<td></td>
END
	}
	print <<END;
</tr>
END
}

print <<END;
</table><br/>
END

&closebox();

&openbox($tr{'disk usage'});

@echo = `df -h`;
shift(@echo);

print <<END;
<br/>
<table style='width: 95%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align: left; width: 120px;'>$tr{ 'adv filesystem' }</th>
	<th style='text-align: left; width: 100px;'>$tr{ 'adv mount point' }</th>
	<th style='text-align: right; width: 80px;'>$tr{ 'adv size'}</th>
	<th style='text-align: right; width: 80px;'>$tr{ 'adv used'}</th>
	<th style='text-align: right; width: 100px;'>$tr{ 'adv available'}</th>
	<th>&nbsp;</th>
	<th style='text-align: center; width: 150px;'>$tr{ 'adv used%' }</th>
</tr>
END

foreach my $mount (@echo) {
   chomp($mount);
	my ($dev, $size, $size_used, $size_avail, $size_percentage, $mount_point) = split(/\s+/,$mount);

	$size_percentage =~ s/[^\d]//g;
	$size_percentage ||= 0;

	if (int($size_percentage) > $graphalertcritical) {
		$graphbgcolour = $graphcriticalcolour;
	}
	elsif (int($size_percentage) > $graphalertwarning) {
		$graphbgcolour = $graphwarningcolour;
	}
	elsif (int($size_percentage) > 0) {
		$graphbgcolour = $graphnominalcolour;
	}
	else {
		$graphbgcolour = $graphblankcolour;
	}

	print <<END;
<tr>
	<td><code>$dev</code></td>
	<td><code>$mount_point</code></td>
	<td style='text-align: right;'><code>$size</code></td>
	<td style='text-align: right;'><code>$size_used</code></td>
	<td style='text-align: right;'><code>$size_avail</code></td>
	<td><code>&nbsp;</code></td>
	<td>
		<table class='blank' style='width: 150px; border: 1px #505050 solid;'>
		<tr>
END

	if (int($size_percentage) < 1) {
		print "\t\t\t<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><code>${size_percentage}%</code></td>\n";
	}
	else {
		print "\t\t\t<td style='background-color: $graphbgcolour; width: ${size_percentage}%; text-align: center;'><code>${size_percentage}%</code></td>\n";
	}

	print <<END;
			<td style='background-color: $graphblankcolour;'>&nbsp;</td>
		</tr>
		</table></td>
</tr>
END
}

print <<END;
</table><br/>
END

&closebox();

&openbox($tr{'inode usage'});
@echo = `df -i`;
shift(@echo);

print <<END;
<br/>
<table style='width: 95%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align: left; width: 120px;'>$tr{ 'adv filesystem' }</th>
	<th style='text-align: left; width: 100px;'>$tr{ 'adv mount point' }</th>
	<th style='text-align: right; width: 80px;'>$tr{ 'adv inodes' }</th>
	<th style='text-align: right; width: 80px;'>$tr{ 'adv used' }</th>
	<th style='text-align: right; width: 100px;'>$tr{ 'adv free' }</th>
	<th>&nbsp;</th>
	<th style='text-align: center; width: 150px;'>$tr{ 'adv used%' }</th>
</tr>
END

foreach my $mount (@echo) {
   chomp($mount);
	my ($dev, $size, $size_used, $size_avail, $size_percentage, $mount_point) = split(/\s+/,$mount);

	$size_percentage =~ s/[^\d]//g;
	$size_percentage ||= 0;

	if (int($size_percentage) > $graphalertcritical) {
		$graphbgcolour = $graphcriticalcolour;
	}
	elsif (int($size_percentage) > $graphalertwarning) {
		$graphbgcolour = $graphwarningcolour;
	}
	elsif (int($size_percentage) > 0) {
		$graphbgcolour = $graphnominalcolour;
	}
	else {
		$graphbgcolour = $graphblankcolour;
	}

	print <<END;
<tr>
	<td ><code>$dev</code></td>
	<td ><code>$mount_point</code></td>
	<td style='text-align: right;'><code>$size</code></td>
	<td style='text-align: right;'><code>$size_used</code></td>
	<td style='text-align: right;'><code>$size_avail</code></td>
	<td><code>&nbsp;</code></td>
	<td>
		<table class='blank' style='width: 150px; border: 1px #505050 solid;'>
		<tr>
END

	if (int($size_percentage) < 1) {
		print "\t\t\t<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><code>${size_percentage}%</code></td>\n";
	}
	else {
		print "\t\t\t<td style='background-color: $graphbgcolour; width: ${size_percentage}%; text-align: center;'><code>${size_percentage}%</code></td>\n";
	}

	print <<END;
			<td style='background-color: $graphblankcolour;'>&nbsp;</td>
		</tr>
		</table></td>
</tr>
END
}

print <<END;
</table><br/>
END

&closebox();

&openbox($tr{'uptime and users'});

my @who = split /\n/, &pipeopen( '/usr/bin/w' );
my ( $time, $up, $users, $load ) = ( $who[0] =~/\s+([^\s]*)\s+up\s+([^,]*),\s+([^,]*),\s+(.*)/ );

print "<div style='text-align: center;'>$time,  up $up,  $users,  $load</div>";

print <<END;
<br/>
<table style='width: 95%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align: left;'>$tr{'adv user'}</th>
	<th style='text-align: left;'>$tr{'adv tty'}</th>
	<th style='text-align: left;'>$tr{'adv login'}</th>
	<th style='text-align: left;'>$tr{'adv idle'}</th>
	<th style='text-align: left;'>$tr{'adv jcpu'}</th>
	<th style='text-align: left;'>$tr{'adv pcpu'}</th>
	<th style='text-align: left;'>$tr{'adv what'}</th>
</tr>
END

shift @who;  # remove the header information
shift @who;  # remove the header information

foreach my $whol (@who){
	my ( $user, $tty, $login, $idle, $jcpu, $pcpu, $what ) = split /\s+/, $whol;
	print <<END;
<tr>
	<td>$user</td>
	<td>$tty</td>
	<td>$login</td>
	<td>$idle</td>
	<td>$jcpu</td>
	<td>$pcpu</td>
	<td>$what</td>
</tr>
END
}

print <<END;
</table><br/>
END

&closebox();

my %ethersettings;
&readhash(  "${swroot}/ethernet/settings", \%ethersettings );
my %devices;
$devices{$ethersettings{'GREEN_DEV'}} = $tr{'green'};
$devices{$ethersettings{'ORANGE_DEV'}} = $tr{'orange'};
$devices{$ethersettings{'RED_DEV'}} = $tr{'red'};
$devices{$ethersettings{'PURPLE_DEV'}} = $tr{'purple'};

&openbox($tr{'interfaces'});

print "<div class='list' style='margin:1.5em auto; padding:.1em 0 2em 0; width:95%; max-height:500px; overflow:auto;'>\n";

my $doRX = 0;
my $doTX = 0;

my @interfaces = split /\n\d+: /, &pipeopen( '/usr/sbin/ip', '-s', 'link' );
my @addrs = split /\n\d+: /, &pipeopen( '/usr/sbin/ip', 'addr' );
$interfaces[0] =~ s/^\d+:\s+//;
$addrs[0] =~ s/^\d+:\s+//;

for (my $i=0; $i<@interfaces; $i++) {
	$interfaces[$i] .= $addrs[$i];
}

foreach my $interface ( sort @interfaces ){
	my ($devicename, $macaddress, $ipaddress, $netmask, $mtu, $status, $states) =
		('', '', '', '', '', '', '');
	$devicename	= $1 if ( $interface =~ /^([^:]+)/ );
	$macaddress	= $1 if ( $interface =~ /link\/[^\s]+\s+(([0-9A-F]{2}:){5}[0-9A-F]{2})/i );
	$ipaddress	= $1 if ( $interface =~ /inet ((\d+\.){3}\d+)/ );
	# $3 is correct: nested groupings
	$netmask	= $3 if ( $interface =~ /inet ((\d+\.){3}\d+)(\/\d+)/ );
	$mtu		= $1 if ( $interface =~ /mtu (\d+)/ );
	$status	= $1 if ( $interface =~ /state\s+(\w+)\s+/ );
	$states	= $1 if ( $interface =~ /<([^>]+)>/ );

	# bytes, packets, errors, dropped, overrun, multicast
	my ( $rx, $rxp, $rxe, $rxd, $rxo, $rxm ) =
		( $interface =~ /RX: bytes.*\n\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/ );
	$rxe = "" if ($rxe eq "0");
	$rxd = "" if ($rxd eq "0");
	$rxo = "" if ($rxo eq "0");
	$rxm = "" if ($rxm eq "0");

	# bytes, packets, errors, dropped, carrier, collisions
	my ( $tx, $txp, $txe, $txd, $txc, $txx ) =
		( $interface =~ /TX: bytes.*\n\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/ );
	$txe = "" if ($txe eq "0");
	$txd = "" if ($txd eq "0");
	$txc = "" if ($txc eq "0");
	$txx = "" if ($txx eq "0");

	$devices{$devicename} = "Red" if ($devicename =~ /ppp/);
	$devices{$devicename} = "Ovpn" if ($devicename =~ /t(un|ap)/);
	$devicename = "$devicename ($devices{$devicename})" if ($devices{$devicename});

	print <<END;
<br />
<table class='box' style='width: 98%; margin: .05em auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th colspan='4'>$devicename</th>
</tr>
<tr>
	<td style='text-align: right; padding:0 .5em 0 0; width:17%;'>Status:</td>
	<td style='padding:0 .5em 0 0; width:21%;'>$status</td>
	<td style='text-align: right; padding:0 .5em 0 0; width:20%;'>Link States:</td>
	<td style='padding:0 .5em 0 0;'>$states</td>
</tr>
<tr>
	<td style='text-align: right; padding:0 .5em 0 0;'>IP Address:</td>
	<td style='padding:0 .5em 0 0;'>$ipaddress</td>
	<td style='text-align: right; padding:0 .5em 0 0;'>MAC Address:</td>
	<td style='padding:0 .5em 0 0;'>$macaddress</td>
</tr>
<tr>
	<td style='text-align: right; padding:0 .5em 0 0;'>Netmask:</td>
	<td style='padding:0 .5em 0 0;'>$netmask</td>
	<td style='text-align: right; padding:0 .5em 0 0;'>MTU:</td>
	<td style='padding:0 .5em 0 0;'>$mtu</td>
</tr>
<tr>
	<td style='text-align: right; padding:0 .5em 0 0;'>Sent packets / bytes:</td>
	<td style='padding:0 .5em 0 0;'>$txp / $tx</td>
	<td style='text-align: right; padding:0 .5em 0 0;'>Received packets / bytes:</td>
	<td style='padding:0 .5em 0 0;'>$rxp / $rx</td>
</tr>
<tr>
	<td style='text-align: right; padding:0 .5em 0 0;'>Errors (sent):</td>
	<td style='padding:0 .5em 0 0;'>$txe</td>
	<td style='text-align: right; padding:0 .5em 0 0;'>Errors (received):</td>
	<td style='padding:0 .5em 0 0;'>$rxe</td>
</tr>
<tr>
	<td style='text-align: right; padding:0 .5em 0 0;'>Dropped (sent):</td>
	<td style='padding:0 .5em 0 0;'>$txd</td>
	<td style='text-align: right; padding:0 .5em 0 0;'>Dropped (received):</td>
	<td style='padding:0 .5em 0 0;'>$rxd</td>
</tr>
<tr>
	<td style='text-align: right; padding:0 .5em 0 0;'>Carrier (sent):</td>
	<td style='padding:0 .5em 0 0;'>$txc</td>
	<td style='text-align: right; padding:0 .5em 0 0;'>Overruns (received):</td>
	<td style='padding:0 .5em 0 0;'>$rxo</td>
</tr>
<tr>
	<td style='text-align: right; padding:0 .5em 0 0;'>Collisions (sent):</td>
	<td style='padding:0 .5em 0 0;'>$txx</td>
	<td style='text-align: right; padding:0 .5em 0 0;'>Multicast (received):</td>
	<td style='padding:0 .5em 0 0;'>$rxm</td>
</tr>
</table>
END
}
print "</div>\n";

&closebox();

&openbox($tr{'routing'});

my @routes = split /\n/, &pipeopen( '/usr/sbin/ip', 'route' );

print <<END;
<br />
<table class='list' style='width: 95%; margin: auto auto 1em auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv destination'}</th>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv gateway'}</th>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv iface'}</th>
	<th style='padding-left:.5em; text-align:left;'>Source</th>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv metric'}</th>
	<th style='padding-left:.5em; text-align:left;'>Proto</th>
	<th style='padding-left:.5em; text-align:left;'>Scope</th>
</tr>
END

foreach my $routel (sort @routes){
	my $devicename;
	my ($destination, $gateway, $iface, $source, $proto, $scope, $metric) =
		('', '', '', '', '', '', '');
	$destination	= $1 if ($routel =~ /^([^\s]+)/);
	$gateway	= $1 if ($routel =~ /via\s+([^\s]+)/);
	$iface		= $1 if ($routel =~ /dev\s+([^\s]+)/);
	$source	= $1 if ($routel =~ /src\s+([^\s]+)/);
	$proto		= $1 if ($routel =~ /proto\s+([^\s]+)/);
	$scope		= $1 if ($routel =~ /scope\s+([^\s]+)/);
	$metric	= $1 if ($routel =~ /metric\s+([^\s]+)/);

	$devices{$iface} = "Red" if ($iface =~ /ppp/);
	$devices{$iface} = "Ovpn" if ($iface =~ /t(un|ap)/);

	$devicename = $iface;
	$devicename .= " ($devices{$iface})" if ($devices{$iface});

	print <<END;
<tr>
	<td style='padding-left:.5em;'>$destination</td>
	<td style='padding-left:.5em;'>$gateway</td>
	<td style='padding-left:.5em;'>$devicename</td>
	<td style='padding-left:.5em;'>$source</td>
	<td style='padding-left:.5em;'>$metric</td>
	<td style='padding-left:.5em;'>$proto</td>
	<td style='padding-left:.5em;'>$scope</td>
</tr>
END
}
print "</table>\n";

&closebox();
&openbox("$tr{'adv hardware'} <i>(PCI)</i>");

my @lspci = split /\n/, &pipeopen( '/usr/sbin/lspci' );

print <<END;
<br />
<table class='list' style='width: 95%; margin: auto auto 1em auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv address'}</th>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv type'}</th>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv device'}</th>
</tr>
END

foreach my $devl (@lspci){
	my ( $address, $type, $device ) = ( $devl =~/([^\s]*)\s+([^:]*):\s+(.*)/ );
	print <<END;
<tr>
	<td style='padding-left:.5em;'>$address</td>
	<td style='padding-left:.5em;'>$type</td>
	<td style='padding-left:.5em;'>$device</td>
</tr>
END
}
print "</table>\n";

&closebox();

&openbox($tr{'loaded modules'});

my @lsmod = split /\n/, &pipeopen( '/bin/lsmod' );

print "<div class='list' style='margin:1.5em auto; padding:0 0 1em 0; width:95%; max-height:400px; overflow:auto;'>\n";
print <<END;
<br />
<table class='box' style='width:98%; margin:1em auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv module'}</th>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv size'}</th>
	<th style='padding-left:.5em; text-align:left;'>$tr{'adv used by'}</th>
</tr>
END

shift @lsmod;  # remove the header information

foreach my $modl (@lsmod){
	my ( $module, $size, $usedby, $modules ) = split /\s+/, $modl;
	print <<END;
<tr>
	<td style='padding-left:.5em;'>$module</td>
	<td style='padding-left:.5em;'>$size</td>
	<td style='padding-left:.5em;'>$usedby</td>
</tr>
END
}
print "</table>\n";
print "</div>\n";

&closebox();

&openbox($tr{'kernel version'});
print "<pre style='margin-left:1em;'>";
system ('/bin/uname', '-a');
print "</pre>\n";
&closebox();

&alertbox('add', 'add');

&closebigbox();
&closepage();

