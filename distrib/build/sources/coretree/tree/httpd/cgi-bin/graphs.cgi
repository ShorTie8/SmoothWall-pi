#!/usr/bin/perl
#
# coded by Martin Pot 2003
# http://martybugs.net/smoothwall/rrdtool.cgi
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
# rrdtool.cgi

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use POSIX qw(strftime);
use strict;
use warnings;

my (%cgiparams, %netsettings, @graphs, $boxtitle);
my $name = '';
my $title = '';
my $errormessage = '';

my $METAs = q[
<meta http-equiv="Refresh" content="300"><meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Pragma" content="no-cache">
];

my @colours=("rgba(0,0,0,.1)", "rgba(0,0,0,.03)");

# Do some magic to align the columms.
sub colAlign()
{
	my ($widVal, $widUnit, $colVal) = @_;
	$colVal =~ s#$#</p>#;
	$colVal =~ s# #\<\/p\>\<p style='display:inline-block; margin:0; width:$widUnit; min-width:$widUnit; text-align:left'>#;
	$colVal =~ s#^#<p style='display:inline-block; width:$widVal; min-width:$widVal; margin:0 .25em 0 0; text-align:right'>#;

	return $colVal;
}

&readhash("${swroot}/ethernet/settings", \%netsettings);

# Get url parameters
my @values = split(/&/, $ENV{'QUERY_STRING'}) if ($ENV{'QUERY_STRING'});
foreach my $i (@values) {
	my ($varname, $mydata) = split(/=/, $i);
	$name = $mydata if ($varname eq 'i');
}

# check if viewing one interface only 
$title = " for $name interface" if ($name ne "");

&showhttpheaders();

&openpage($tr{'network traffic graphs'}."$title", 1, $METAs, 'about your smoothie');
&openbigbox('100%', 'LEFT');
&alertbox($errormessage);

my @message;
my @details;
my @addr_details;
my %stats;

&readhash('/var/log/trafficstats', \%stats);
	
my $timestamp = 'N/A';
$timestamp = strftime "%a %b %e %H:%M:%S %Y", localtime($stats{'last_update'}) if ($stats{'last_update'});
   
foreach my $iface ('eth0', 'eth1', 'eth2', 'eth3', 'ppp0', 'ippp0') {
	my %ifacestats;
	$ifacestats{'this_month_inc_total'} = '';

	foreach my $stat (keys %stats) {
		if ($stat =~ /_${iface}$/) {
			my $field = "$`";
			my $value = $stats{$stat};
			my $units;
			if ($field =~ /^cur/) {
				$units = "bit/s";
				if ($value > 1000) {
					$value /= 1000;
					$units = 'kbits/s';
				}
				if ($value > 1000) {
					$value /= 1000;
					$units = 'Mbits/s';
				}
				if ($value > 1000) {
					$value /= 1000;
					$units = 'Gbits/s';
				}
			}
			else {
				$units = 'kB';
				if ($value > 1000) {
					$value /= 1000;
					$units = 'MB';
				}
				if ($value > 1000) {
					$value /= 1000;
					$units = 'GB';
				}
				if ($value > 1000) {
					$value /= 1000;
					$units = 'TB';
				}
			}
			$value = sprintf("%0.1f", $value);
			$ifacestats{$field} = "$value $units";
		}
	}
	if ($ifacestats{'this_month_inc_total'}) {
		my ($value, $units) = split(/ /, $ifacestats{'this_month_inc_total'});
		if ($value > 0) {
			my $printableiface;
			if ($iface eq $netsettings{'GREEN_DEV'}) {
				$printableiface = 'Green';
			}
			elsif ($iface eq $netsettings{'ORANGE_DEV'}) {
				$printableiface = 'Orange';
			}
			elsif ($iface eq $netsettings{'PURPLE_DEV'}) {
				$printableiface = 'Purple';
			}
			elsif ($iface eq $netsettings{'RED_DEV'}) {
				$printableiface = 'Red';
			}
			elsif ($iface eq 'ppp0') {
				$printableiface = 'Modem';
			}
			elsif ($iface eq 'ippp0') {
				$printableiface = 'ISDN';
			}
			push @details, { Interface => $printableiface, %ifacestats };
		}
	}
}

my %addrstats = ();
foreach my $stat (keys %stats) {
	if($stat =~ /_(\d+\.\d+\.\d+\.\d+)/) {
		my $addr = $1 . $';
		my $field = $`;
		my $value = $stats{$stat};
		my $units;
		if ($field =~ /^cur/) {
			$units = "bit/s";
			if ($value > 1000) {
				$value /= 1000;
				$units = 'kbits/s';
			}
			if ($value > 1000) {
				$value /= 1000;
				$units = 'Mbits/s';
			}
			if ($value > 1000) {
				$value /= 1000;
				$units = 'Gbits/s';
			}
		}
		else {
			$units = 'kB';
			if ($value > 1000) {
				$value /= 1000;
				$units = 'MB';
			}
			if ($value > 1000) {
				$value /= 1000;
				$units = 'GB';
			}
			if ($value > 1000) {
				$value /= 1000;
				$units = 'TB';
			}
		}
		$value = sprintf("%0.1f", $value);
		$addrstats{$addr} = {} unless defined $addrstats{$addr};
		$addrstats{$addr}->{$field} = "$value $units";
	}
}

foreach my $addr (keys %addrstats) {
	if ($addrstats{$addr}->{'this_day_inc_total'}) {
		my ($value, $units) = split(/ /, $addrstats{$addr}->{'this_day_inc_total'});
		if ($value > 0) {
			my $pretty = $addr;

			$pretty =~ s/_/ /g;
			$pretty =~ s/(RED|GREEN|ORANGE|PURPLE)/<br \/>/g;
			push @addr_details, { Address => $pretty, %{$addrstats{$addr}} };
		}
	}
}

&openbox("Interface traffic statistics - ${timestamp}:");

print <<END
<div style="margin:1.5em auto; width:95%; max-height:400px; overflow:auto">
<table class='list'>
<tr>
	<th class='list' style='width: 15%;'>$tr{'traffic stats interface'}</th>
	<th class='list' style='width: 9%;'>$tr{'traffic stats period'}</th>
	<th class='list' style='width: 11%;'>$tr{'traffic stats direction'}</th>
	<th class='list' style='width: 15%;'>$tr{'traffic stats current rate'}</th>
	<th class='list' style='width: 12%;'>$tr{'traffic stats hour'}</th>
	<th class='list' style='width: 12%;'>$tr{'traffic stats day'}</th>
	<th class='list' style='width: 12%;'>$tr{'traffic stats week'}</th>
	<th class='list' style='width: 12%;'>$tr{'traffic stats month'}</th>
</tr>
END
;

my $widV = "3.5em";
my $widU = "2.5em";

my $rowCount = -1;

foreach my $row ( sort { $a->{'Interface'} cmp $b->{'Interface'} } @details ) {
	$rowCount++;
	print <<END
<tr style="background-color:$colours[$rowCount%2]">
	<td class='list' >$row->{ 'Interface' }</td>
	<td class='list' >$tr{'traffic stats current'}</td>
	<td class='list' >$tr{'traffic stats in'}</td>
END
;
	printf "	<td class='list' >%s</td>\n", &colAlign("4.0em", "4.0em", $row->{ 'cur_inc_rate' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_hour_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_day_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_week_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_month_inc_total' });

print <<END
</tr>
<tr style="background-color:$colours[$rowCount%2]">
	<td class='list' >&nbsp;</td>
	<td class='list' >&nbsp;</td>
	<td class='list' >$tr{'traffic stats out'}</td>
END
;
	printf "	<td class='list' >%s</td>\n", &colAlign("4.0em", "4.0em", $row->{ 'cur_out_rate' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_hour_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_day_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_week_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_month_out_total' });

print <<END
</tr>
<tr style="background-color:$colours[$rowCount%2]">
	<td class='list' >&nbsp;</td>
	<td class='list' >$tr{'traffic stats previous'}</td>
	<td class='list' >$tr{'traffic stats in'}</td>
	<td class='list' >&nbsp;</td>
END
;
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_hour_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_day_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_week_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_month_inc_total' });

print <<END
</tr>
<tr style="background-color:$colours[$rowCount%2]">
	<td class='list' >&nbsp;</td>
	<td class='list' >&nbsp;</td>
	<td class='list' >$tr{'traffic stats out'}</td>
	<td class='list' >&nbsp;</td>
END
;
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_hour_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_day_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_week_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_month_out_total' });
}

print "</table></div>";

&closebox();
# now per address stats


&openbox("Address traffic statistics - ${timestamp}:");

print <<END
<div style="margin:1.5em auto; width:95%; max-height:600px; overflow:auto">
<table class='list'>
<tr>
	<th class='list'  style='width: 15%;'>Address</th>
	<th class='list'  style='width: 9%;'>$tr{'traffic stats period'}</th>
	<th class='list'  style='width: 11%;'>$tr{'traffic stats direction'}</th>
	<th class='list'  style='width: 15%;'>$tr{'traffic stats current rate'}</th>
	<th class='list'  style='width: 12%;'>$tr{'traffic stats hour'}</th>
	<th class='list'  style='width: 12%;'>$tr{'traffic stats day'}</th>
	<th class='list'  style='width: 12%;'>$tr{'traffic stats week'}</th>
	<th class='list'  style='width: 12%;'>$tr{'traffic stats month'}</th>
</tr>
END
;

$rowCount = -1;
foreach my $row ( sort { $a->{'Address'} cmp $b->{'Address'} } @addr_details ) {
	$rowCount++;
	print <<END
<tr style="background-color:$colours[$rowCount%2]">
	<td class='list'  valign='top' rowspan=4>$row->{ 'Address' }</td>
	<td class='list' >$tr{'traffic stats current'}</td>
	<td class='list' >$tr{'traffic stats in'}</td>
END
;
	printf "	<td class='list' >%s</td>\n", &colAlign("4.0em", "4.0em", $row->{ 'cur_inc_rate' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_hour_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_day_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_week_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_month_inc_total' });

print <<END
</tr>
<tr style="background-color:$colours[$rowCount%2]">
	<td class='list' >&nbsp;</td>
	<td class='list' >$tr{'traffic stats out'}</td>
END
;
	printf "	<td class='list' >%s</td>\n", &colAlign("4.0em", "4.0em", $row->{ 'cur_out_rate' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_hour_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_day_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_week_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'this_month_out_total' });

print <<END
</tr>
<tr style="background-color:$colours[$rowCount%2]">
	<td class='list' >$tr{'traffic stats previous'}</td>
	<td class='list' >$tr{'traffic stats in'}</td>
	<td class='list' >&nbsp;</td>
END
;
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_hour_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_day_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_week_inc_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_month_inc_total' });

print <<END
</tr>
<tr style="background-color:$colours[$rowCount%2]">
	<td class='list' >&nbsp;</td>
	<td class='list' >$tr{'traffic stats out'}</td>
	<td class='list' >&nbsp;</td>
END
;
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_hour_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_day_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_week_out_total' });
	printf "	<td class='list' >%s</td>\n", &colAlign($widV, $widU, $row->{ 'prev_month_out_total' });
}

print "</table></div>";

&closebox();

my $rrddir = "/httpd/html/rrdtool";

# check if viewing summary graphs
if ($name eq "") {
	push (@graphs, ('green-day'));
	push (@graphs, ('orange-day')) if ($netsettings{'ORANGE_DEV'});
	push (@graphs, ('purple-day')) if ($netsettings{'PURPLE_DEV'});
	push (@graphs, ('red-day'));
}
else {
	push (@graphs, ("$name-day"));
	push (@graphs, ("$name-week"));
	push (@graphs, ("$name-month"));
	push (@graphs, ("$name-year"));
}


&openbox($tr{'interface traffic graphsc'});

my $lastdata = scalar localtime(`rrdtool last /var/lib/rrd/green.rrd`);
my $lastupdate = scalar localtime((stat("/var/lib/rrd/green.rrd"))[9]);
print "Last updated $lastupdate, with data to $lastdata<br />";

if ($name eq "") {
	$boxtitle = "Summary Interface traffic graphs:";
}
else {
	$boxtitle = "Detailed traffic graphs for $name interface:";
}

&openbox($boxtitle);

print qq|
<br />
<div style='text-align:center;'>
|;

my $found = 0;
my $graphname;

print qq|&laquo; <a href="?#graphs">return to graph summary</a><br /><br />| if ( $name ne "" );

foreach $graphname (@graphs) {
	if (-e "$rrddir/$graphname.png") {
		# check if displaying summary graphs
		my $graphinterface = (substr($graphname,0,index($graphname,"-")));
		if ($name eq "") {
			print "<a href='".$ENV{'SCRIPT_NAME'}."?i=".(substr($graphname,0,index($graphname,"-")))."&amp;#graphs'";
			print " title='click for detailed graphs for the ".$graphinterface." interface'>";
			print "<img alt='$graphname'";
		}
		else {
			print "<img alt='$graphname'";
		}
		print " style='border-style: none;' src='/rrdtool/$graphname.png'>";
		if ($name eq "") { 
			print qq|</a><br /><a href="?i=$graphinterface&amp;#graphs|;
			print qq|">click for detailed graphs for the $graphinterface interface</a> &raquo;|;
		}
		print "<br /><br />\n";
		$found = 1;
	}
}
print "<a name='graphs'></a>\n";

print "<CLASS='boldbase' style='font-weight:bold;'>$tr{'no graphs available'}</CLASS>" if (!$found);
print "<br />\n";
print "</div>";

&closebox();
&closebox();

&alertbox('add','add');
&closebigbox();
&closepage();
