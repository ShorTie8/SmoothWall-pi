#! /usr/bin/perl

# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

my (%netsettings, $bgcolor);
my $errormessage = '';
our $table1colour;
my $initial_position = "10";
my @bars;
my @bar_names;
my $oururl = "/cgi-bin/trafficstats.cgi?BARS=1";
my @devices;
my %deviceRates;
my $i = 0;

my $METAs = q[
<meta http-equiv="Refresh" content="300"><meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Pragma" content="no-cache">
];

&readhash("${swroot}/ethernet/settings", \%netsettings);
&showhttpheaders();

&openpage("Realtime bandwidth bars", 1, $METAs, 'about your smoothie');
&openbigbox('100%', 'LEFT');

&alertbox();

# Is SWE3
open (HDL, "/usr/sbin/ip link | egrep 'ppp[0-9]+:' | sed -e 's/^[0-9]*: //' -e 's/:.*//'|");
my @PPPdevices = <HDL>;
close (HDL);
chomp @PPPdevices;

# Get NIC bit rates
if ( $netsettings{'GREEN_DEV'}) {
	$devices[$i++] = $netsettings{'GREEN_DEV'};
	$deviceRates{$netsettings{'GREEN_DEV'}} = &getLinkSpeed($netsettings{'GREEN_DEV'}, "string");
}
if ( $netsettings{'ORANGE_DEV'}) {
	$devices[$i++] = $netsettings{'ORANGE_DEV'};
	$deviceRates{$netsettings{'ORANGE_DEV'}} = &getLinkSpeed($netsettings{'ORANGE_DEV'}, "string");
}
if ( $netsettings{'PURPLE_DEV'}) {
	$devices[$i++] = $netsettings{'PURPLE_DEV'};
	$deviceRates{$netsettings{'PURPLE_DEV'}} = &getLinkSpeed($netsettings{'PURPLE_DEV'}, "string");
}
if ($netsettings{'RED_TYPE'} eq 'STATIC' or $netsettings{'RED_TYPE'} eq 'DHCP') {
	$devices[$i++] = $netsettings{'RED_DEV'};
	$deviceRates{$netsettings{'RED_DEV'}} = &getLinkSpeed($netsettings{'RED_DEV'}, "string");
}
else {
	# Must be PPP; get from PPPdevices (ppp0 or ippp0)
	if ($PPPdevices[0]) {
		$devices[$i] = $PPPdevices[0];
		$deviceRates{$devices[$i++]} = "";
	}
}

# Scan the current network for live hosts:
my (@scanlist, @if_files);

# Push interfaces with static assignments into an array
push (@if_files, 'green')  if (-s "${swroot}/dhcp/staticconfig-green");
push (@if_files, 'purple') if (-s "${swroot}/dhcp/staticconfig-purple");
push (@if_files, 'orange') if (-s "${swroot}/dhcp/staticconfig-orange");

# Get the static assignments for each IF and push into an array.
if (@if_files) {
	foreach (@if_files) {
		open (STATIC, "<${swroot}/dhcp/staticconfig-$_") || die "Can't open $_ static file!";
		while (<STATIC>) {
			chomp;
			my ($name, $MAC, $IP) = split (/,/);
			push @scanlist, "$IP\n";
		}
		close (STATIC);
	}
}

# Get the leases and push into the array.
open (LEASES, "</usr/etc/dhcpd.leases") || die "Can't open dhcpd.leases!";
while (<LEASES>) {
	chomp;
	if ($_ =~ /^lease/) {
		my ($key, $IP, $brace) = split (/\s+/);
		# Verify the lease isn't a duplicate.
		push @scanlist, "$IP\n" if (($IP) && ((grep { /$IP/ } @scanlist) == 0));
		next;
	}
}
close (LEASES);

# Print the @scanlist array to a file.
open (ARPLIST, ">${swroot}/traffic/scanip") || die "Can't open scanip!";
print ARPLIST @scanlist;
close (ARPLIST);

#Use the scanip file created to ping listed hosts and refresh the ARP cache
system ("/sbin/fping -c 1 -t 200 -f ${swroot}/traffic/scanip >/dev/null 2>&1");
my @list = `ip n show`;
unlink ("${swroot}/traffic/scanip");

&openbox('Bandwidth bars:');
&realtime_graphs();
&closebox();

&closebigbox();
&closepage($errormessage);


#
# Start of functions
#

# Scans the array to check if the current host is live
sub scanlist {
	return (grep { /^$_[0]\s+.*lladdr/ } @list);
}

sub printableiface 
{
	my $iface = shift;
	my %ifaces = (
		$netsettings{'GREEN_DEV'} => 'Green',
		$netsettings{'ORANGE_DEV'} => 'Orange',
		$netsettings{'PURPLE_DEV'} => 'Purple',
		$netsettings{'RED_DEV'} => 'Red',
		'ppp0' => 'Red (PPP)',
		'ippp0' => 'Red (ISDN)');
	return $ifaces{$iface} || $iface;
}
			
sub realtime_graphs 
{
	print "<div id='dbg'></div>";

	# construct the bar graphs accordingly.

	my (%interfaces, %addresses);
	my ($interface);

	open INPUT, "</var/log/quicktrafficstats";
	while ( my $line = <INPUT> ) {
		next if ( not $line =~ /^cur_(inc|out)_rate/ );
		my $rule = $&;
		$line = $';
		
		# $iface and $value are local: they must be fresh each time through the loop
		my ($iface, $value);
		($iface, $value ) = ( $line =~ /_([^=]+)=([\d\.]+)$/i );
		# Delete the trailing space, if any
		$iface =~ s/ $//;
		# Change remaining spaces to "_"
		$iface =~ s/ /_/g;
		$interfaces{ $iface }{ $rule } = $value;
		if($iface =~ /^(\d+\.\d+\.\d+\.\d+)/ && $rule eq 'cur_out_rate') {
			$addresses{$iface} = $value if (&scanlist($1));
		}
	}
	push @devices, (sort keys %addresses);

	print "\n<div style='border:1px solid #7f7f7f; margin: 2em;'>\n";

	my @rules;

	foreach $interface ( @devices ){
		my $iftitle = $interface;
		$iftitle =~ s/_/ /g;
		$iftitle =~ s/(GREEN|RED|ORANGE|PURPLE)//;
		$iftitle = &printableiface($iftitle);
		if ($iftitle eq 'Red') {
			$bgcolor = '#ffaaaa';
		}
		elsif ($iftitle eq 'Red (PPP)') {
			$bgcolor = '#ffaaaa';
		}
		elsif ($iftitle eq 'Red (ISDN)') {
			$bgcolor = '#ffaaaa';
		}
		elsif ($iftitle eq "Green") {
			$bgcolor = "#bbffbb";
		}
		elsif ($iftitle eq "Purple") {
			$bgcolor = "#ddaaff";
		}
		elsif ($iftitle eq "Orange") {
			$bgcolor = "#ffaa77";
		}
		else {
			$bgcolor = "";
		}
		$deviceRates{$interface} = '' if (not defined $deviceRates{$interface});

	print qq[
<table id='IF_${interface}_container'
	style='width: 100%; border-collapse: collapse; border:none; margin-left: auto;
	margin-right: auto; background-color:$bgcolor' cellspacing='0' cellpadding='0'>
<tr>
	<td colspan='2' style='background-position: top left; background-repeat: no-repeat; vertical-align: top;'>
		<table style='width: 100%; margin-left: auto; margin-right: auto;
			border: none; border-collapse: collapse;' cellspacing='0' cellpadding='0'>
		<tr>
			<td colspan='6' style='background-color:#c3d1e5; height:2px'></td>
		</tr>
		<tr>
			<td colspan='2' style='width: 85px; text-align: left; background-color:#c3d1e5;'>
				&nbsp;<strong>$iftitle</strong>$deviceRates{$interface}</td>
			<td style='width:400px; background-color:#c3d1e5'>
				<table style='width: 100% border: 0; border-collapse: collapse;'
					cellpadding='0' cellspacing='0'>
				<tr>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; border-left: 1px solid #505050;
						border-right: 1px solid #505050; text-align: right;'>10&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>100&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>1k&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>10&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>100&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>1M&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>10&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>100&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>1G&nbsp;</td>
					<td style='height: 8px; overflow: hidden; font-size: 6pt; color: #303030;
						background-color:#c3d1e5; width: 39px; 
						border-right: 1px solid #505050; text-align: right;'>10&nbsp;</td>
				</tr>
				</table>
			</td>
			<td style='height:10px; width: 4px; margin:0; background-color:#c3d1e5'>&nbsp;</td>
			<td style='height:10px; width:55px; margin:0; background-color:#c3d1e5' 
				id='cur_${interface}_rate'></td>
			<td style='width: 2.5%; margin:0; background-color:#c3d1e5'>&nbsp;</td>
		</tr>
		<tr>
			<td colspan='6' style='background-color:none; height:5px'></td>
		</tr>
];

	foreach my $section ( keys %{$interfaces{$interface}} ) {
		my $colour = "rgba(0,0,0,.03)";	# This should be aligned with table1colour in smoothtype 
		my $title  = $section;
		
		if ( $section eq "cur_inc_rate" ) {
			$title  = "Incoming";
			$colour = "#5f5f9f";
		} elsif ( $section = "cur_out_rate" ) {
			$title  = "Outgoing";
			$colour = "#9f5f5f";
		}

		print qq[
		<tr>
			<td style='width: 2.5%; margin:0; background-color:none'>&nbsp;</td>
			<td style='height:10px; text-align:right;'>$title&nbsp;</td>
			<td style='height:10px; background-color: #efefef; font-size:0; margin:0; padding: 0px'>
				<div style='height:10pt; width: 0px; font-size:0; margin:0; padding:0; border: 0px;
				background-color: $colour;' id='${section}_${interface}_bar'>&nbsp;</div></td>
			<td style='height:10px; vertical-align: top;'>&nbsp;</td>
			<td style='height:10px' id='${section}_${interface}_rate'></td>
			<td style='width: 2.5%; margin:0; background-color:none'>&nbsp;</td>
		</tr>
		<tr style='height: 5px;'><td colspan='3'></td></tr>
];

		push @rules, "${section}_${interface}";
	}

	print qq[
		</table>
	</td>
</tr>
<tr>
	<td colspan='2'></td>
</tr>
</table>
];

	}

	print "</div><script type='text/javascript'>\n";
	&show_script( \@rules );
	print "</script>\n";
	print "<script type='text/javascript'> monitor(); </script>\n";
}



sub show_script
{
	my ( $rules ) = @_;

	print qq {
var interfaces 	= new Array();
var old 	= new Array();
var cur 	= new Array();
var ifclass 	= new Array();
var ofclass 	= new Array();
var ifnames 	= new Array();
	};

	for ( my $i = 0 ; $i < scalar( @$rules ) ; $i++ ) {

		print qq {
interfaces[$i] = '$rules->[$i]';
cur['$rules->[$i]'] = 0;
old['$rules->[$i]'] = 0;
};
	}

	my $i = 0;

	foreach my $interface ( @devices ) {

		print qq {
ifclass['$interface'] = 19;
ofclass['$interface'] = 19;
ifnames[ $i ] = '$interface';
};

	$i++;
	}

	print qq#
var dbg = document.getElementById('dbg');

function xmlhttpPost()
{
	var xmlHttpReq = false;
	var self = this;


	if (window.XMLHttpRequest) {
		// Mozilla/Safari
		self.xmlHttpReq = new XMLHttpRequest();
	}
	else if (window.ActiveXObject) {
		// IE
	self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
	}

	self.xmlHttpReq.open('GET', "$oururl", true);
	self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	self.xmlHttpReq.onreadystatechange = function() {
		if ( self.xmlHttpReq && self.xmlHttpReq.readyState == 4) {
			updatepage(self.xmlHttpReq.responseText);
		}
	}

	self.xmlHttpReq.send( null );
}

var splitter = /^cur_(inc|out)_rate_([^=]+)=([\\d\\.]+)\$/i;

function updatepage(str){
	var rows = str.split( '\\n' );
	
	dbg.innerHTML = "";

	for ( var i = 0; i < rows.length ; i++ ) {
		if ( rows[ i ] != "" ) {
			// Split and tidy
			var results = splitter.exec(rows[i]);	
			results[2] = results[ 2 ].replace(/ \$/, "");
			results[2] = results[ 2 ].replace(/ /g, "_");

			// Set the id 'prefix'
			var id = 'cur_' + results[ 1 ] + '_rate_' + results[2];

			// Skip if a 'new' item hasn't been drawn in this window
			if ( !document.getElementById( id + '_rate' ) ){
				continue;
			}

			var divider = 0;
			var rate = 0;
			
			// The divider is based on the full bit rate. It
			//   is crowbarred to stay within the lines.
			divider = (40 * Math.log(results[3])/Math.log(10));
			if (divider == -Infinity) {
				divider = 0;
			}
			if (divider < 0) {
				divider = 0;
			}
			if (divider > 400) {
				divider = 400;
			}

			// The displayed rate is adjusted to use multipliers.
			if ( results[ 3 ] < 1000 ) {
				rate = parseFloat( results[3] )+'     ';
				rate = String(rate).substring(0,5);
				rate += " b/s";
			}
			else if ( results[ 3 ] < (1000*1000) ) {
				results[3] /= 1000;
				rate = parseFloat( results[3] )+'     ';
				rate = String(rate).substring(0,5);
				rate += " kb/s";
			}
			else if ( results[ 3 ] < (1000*1000*1000) ) {
				results[3] /= 1000*1000;
				rate = parseFloat( results[3] )+'     ';
				rate = String(rate).substring(0,5);
				rate += " Mb/s";
			} else if ( results[ 3 ] < (1000*1000*1000*1000) ) {
				results[3] /= 1000*1000*1000;
				rate = parseFloat( results[3] )+'     ';
				rate = String(rate).substring(0,5);
				rate += " Gb/s";
			}


			old[ id ] = cur[ id ];
			cur[ id ] = parseInt( divider );

			// Set the bar width and textual rate
			document.getElementById( id + '_bar' ).style.width = cur[ id ] + 'px';
			document.getElementById( id + '_rate' ).innerHTML = rate;
		}

	}
	setTimeout( "xmlhttpPost()", 1000 );
}

function monitor()
{
	xmlhttpPost();
}

#;

#
# End of large script

# End of sub show_script
}
