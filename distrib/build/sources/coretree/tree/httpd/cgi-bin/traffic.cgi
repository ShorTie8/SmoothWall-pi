#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
# Martin Houston <martin.houston@smoothwall.net>

#########
#########
###  12/2017: This script needs data validation!!!!!!
#########
#########

use lib "/usr/lib/smoothwall";
use header qw(:standard);
use smoothtype qw(:standard);
use smoothd qw(message);
use strict;
use warnings;

use Socket;

my (%cgiparams, %selected, %checked, %trafficsettings, %speed_labels, %settings, %netsettings, $default_block);

$cgiparams{'ACTION'} = '';

&showhttpheaders();
&getcgihash(\%cgiparams);

my $infomessage = '';
my $errormessage = '';
my $refresh = '';

# Two values are scale factor from full line speed for rate and ceiling
# 100% is full speed
# Values > 100 are actual bit rates
# The sum of the 'share' rates must not exceed 100%.
# as cannot promise more than the available bandwidth!

# HTB bandwidth sharing ratios.
# First value is the 'share' rate, used when there is bandwidth contention.
# The sum of the 'share' rates must never exceed 100%.
# Second is the maximum B/W the class may use, with or without contention.
# A rate is either a percentage of the link's bandwidth (<=100) OR an
# actual bit rate (>100, with NO multiplier).
# The 'share' rates indicate the relative proportion of the bandwidth each
#   contending stream will get. Thus, if there are only normal and admin
#   packets to send, each stream will get a 1/100:1/100 share (50%). If there
#   are normal, admin and isochronous (assume 10Mb/s outbound) streams, they
#   will receive 1/100:1/100:128/10000 shares of bandwidth.
# In the absence of contention (only one stream to transmit), isochron can use
#   up to 128000b/s, high (usually DNS) can use up to 20%, and the
#   rest can use up to 100%.
# As of 11/2014, trafficloader.pl uses each internal NIC's negotiated bit rate. This is
#   nearly always too fast; there should be a %age multipler in the UI to allow the
#   admin to specify the actual observed bit rate. 95% might not be unreasonable.

my %scale = (
	      normal => [     1,     100],
	        high => [     1,      20],
	         low => [     1,     100],
	    isochron => [128000,  128000],
	 smoothadmin => [     1,     100],
	    webcache => [     1,     100],
	    smallpkt => [     1,     100],
	localtraffic => [     1,     100],
);

my %prios = (
	         high => 0,
	       normal => 1,
	          low => 2,
            isochron => 3,
         smoothadmin => 4,
            webcache => 5,
);

my %classIDs = (
                none => 0,
                 all => 1,
              normal => 2,
                high => 3,
                 low => 4,
            isochron => 5,
         smoothadmin => 6,
            webcache => 7,
        localtraffic => 8,
            smallpkt => 9,
);

&readhash("${swroot}/ethernet/settings", \%netsettings );
&readhash("${swroot}/traffic/settings", \%trafficsettings );

# We have a "Save" request ...

if ( $cgiparams{'ACTION'} eq $tr{'save'} ) {
	# Turn our cgi parameters into the more compact settings from the checkboxes.
	# Value: 'on' or 'off'
	$cgiparams{'PERIPSTATS'} = 'on';
	for(qw/ENABLE PERIPSTATS/) {
		$trafficsettings{$_} = (defined $cgiparams{$_} ? 'on' : 'off');
	}

	# simple numeric quantities
	# Need separate GN/OR/PU/RD values here
	for(qw/INTERNAL_SPEED UPLOAD_SPEED DOWNLOAD_SPEED/) {
		$trafficsettings{$_} = $1 if defined $cgiparams{$_} && $cgiparams{$_} =~ /^(\d+)$/;
	}

	# classIDs are never redefined in the UI
	if( ($cgiparams{'DEFAULT_TRAFFIC'}) && ($classIDs{$cgiparams{'DEFAULT_TRAFFIC'}})) {
		$trafficsettings{'DEFAULT_TRAFFIC'} =  $cgiparams{'DEFAULT_TRAFFIC'};
	}
	
	# Now the rates and ceilings
	$trafficsettings{'DRATE'} = ('');
	$trafficsettings{'DCEIL'} = ('');
	$trafficsettings{'URATE'} = ('');
	$trafficsettings{'UCEIL'} = ('');
	
	for(keys %classIDs) {
		next if /^(all|none|(disabled))$/;
		# first downloads
		my $mulfactor = ($_ eq 'localtraffic' 
		    ? $trafficsettings{'INTERNAL_SPEED'}
		    : $trafficsettings{'DOWNLOAD_SPEED'});
		# <=100 is %age, >100 is b/s
		if ($scale{$_} <= 100) {
			$trafficsettings{'DRATE'} .= "$_," . int($scale{$_}->[0] * $mulfactor) / 100 . ',';
			$trafficsettings{'DCEIL'} .= "$_," . int($scale{$_}->[1] * $mulfactor) / 100 . ',';
		}
		else {
			$trafficsettings{'DRATE'} .= "$_," . $scale{$_}->[0] . ',';
			$trafficsettings{'DCEIL'} .= "$_," . $scale{$_}->[1] . ',';
		}
		# now uploads
		$mulfactor = ($_ eq 'localtraffic'
										? $trafficsettings{'INTERNAL_SPEED'}
										: $trafficsettings{'UPLOAD_SPEED'});
		# <=100 is %age, >100 is b/s
		if ($scale{$_} <= 100) {
			$trafficsettings{'URATE'} .= "$_," . int($scale{$_}->[0] * $mulfactor) / 100 . ',';
			$trafficsettings{'UCEIL'} .= "$_," . int($scale{$_}->[1] * $mulfactor) / 100 . ',';
		}
		else {
			$trafficsettings{'URATE'} .= "$_," . $scale{$_}->[0] . ',';
			$trafficsettings{'UCEIL'} .= "$_," . $scale{$_}->[1] . ',';
		}
	}

	# now the rules - these need to be collected from class choices
	# rest of rule must preexist - no suitable default!
	# class is 5th part of rule def and only one that is changed on this screen.
	for my $cgi (keys %cgiparams) {
		next unless $cgi =~ /^R_(\d+)_CLASS$/ && defined $classIDs{$cgiparams{$cgi}};
		# we have a valid class to assign
		my $rulenum = 'R_' . $1;
		if($trafficsettings{$rulenum}) {
			my($name,$tcp,$udp,$dir,$ports,$class,$comment) = split(/,/, $trafficsettings{$rulenum});

			$class = $cgiparams{$cgi};
			$trafficsettings{$rulenum} = join(',', $name,$tcp,$udp,$dir,$ports,$class,$comment);
		}
	}
		
	unless ($errormessage) {
		&writehash("${swroot}/traffic/settings", \%trafficsettings);

		my $success = message('trafficrestart');
		$infomessage .= $success ."<br />\n" if ($success);
		$errormessage .= "trafficrestart ".$tr{'smoothd failure'} ."<br />" unless ($success);
	}
}

&openpage($tr{'traffic configuration'}, 1, $refresh, 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage, "", $infomessage);

print "<form method='post' action='?'><div>";

# deal with the green settings.
&display_speeds( \%trafficsettings);

# deal with the green settings.
&display_rules( \%trafficsettings);

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


# Subroutine to deal with displayed bit rates.
#
sub display_speeds
{
	my ( $settings ) = @_;
	my($upload_speed_block,$download_speed_block,$internal_speed_block);
	my %selected = ();

	my @speeds = sort {$a <=> $b} keys %speed_labels; 

	my @ext_speeds = @speeds;
	my @int_speeds = @speeds;
		
	# Draw the general options box.
	&openbox($tr{'traffic general options'});
	my $enable_bit = ($settings->{'ENABLE'} eq 'on' ? 'checked' : '');

	print <<END
<table style='width:100%;'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'traffic enable'}</td>
	<td style='width: 25%;'><input name='ENABLE' type='checkbox' $enable_bit /></td>
	<td class='base' style='width:25%'>$tr{'traffic external up'}</td>
	<td style='width:25%'>
		<input type='text' name='UPLOAD_SPEED' value='$settings->{'UPLOAD_SPEED'}'
			size='11' style='text-align:right' id='upload_speed' 
			@{[jsvalidnumber('upload_speed', 0, 10000000000)]} >&nbsp;bits/sec</td>
</tr>
<tr>
	<td class='base'>$tr{'traffic internal speed'}</td>
	<td>
		<input type='text' name='INTERNAL_SPEED' value='$settings->{'INTERNAL_SPEED'}'
			size='11' style='text-align:right' id='internal_speed' 
			@{[jsvalidnumber('internal_speed', 0, 10000000000)]} />&nbsp;bits/sec</td>
	<td class='base' >$tr{'traffic external down'}</td>
	<td>
		<input type='text' name='DOWNLOAD_SPEED' value='$settings->{'DOWNLOAD_SPEED'}'
			size='11' style='text-align:right' id='download_speed' 
			@{[jsvalidnumber('download_speed', 0, 10000000000)]} />&nbsp;bits/sec</td>
</tr>
</table>
END
;

	&closebox();

	return;
}



# Subroutine to display the rules
#
sub display_rules
{
	my ( $settings ) = @_;

	my %default_traffic_labels = ( 
		 low => $tr{'traffic low'}, 
	     normal => $tr{'traffic normal'},
		high => $tr{'traffic high'}, 
	   isochron => $tr{'traffic isochronous'},
	);

	my %class_labels = ( 
		none => $tr{'traffic none'}, 
		 low => $tr{'traffic low'}, 
	     normal => $tr{'traffic normal'},
		high => $tr{'traffic high'}, 
	   isochron => $tr{'traffic isochronous'},
	);

	# Set a few menu options
	%selected = ($settings->{'DEFAULT_TRAFFIC'} => ' selected');
	my $default_block = 
		join('', 
			map {"<option value='$_'".($selected{$_} || '').">$default_traffic_labels{$_}</option>\n"} 
			(qw/low normal high isochron/)
		);

	my @rules = ();

	&openbox($tr{'traffic rules'});

	my %selected = ();

	print <<END
<table style='width: 100%;'>
<tr>
	<td class='base' colspan='3'>$tr{'traffic default'}</td>
	<td><select name='DEFAULT_TRAFFIC' title='Default Traffic: normal priority'>$default_block</select></td>
	<td colspan='2'></td>
</tr>
<tr>
	<td colspan='4' style='height:.5em'></td>
</tr>
END
;

	for my $rule (sort keys %{$settings}) {
		next unless $rule =~ /R_(\d+)$/;
		
		my ($name, $class, $title) = (split(',', $settings->{$rule}))[0,5,6];
		$title =~ s/'/&rsquo;/;
		%selected = ($class => ' selected');
		my $class_block =
			join('', 
				map {"\t\t<option value='$_'".($selected{$_} || '').">$class_labels{$_}</option>\n"} 
				(qw/none low normal high isochron/)
			);

		$name =~ s/_/ /g;
		push @rules, "
	<td class='base' style='width: 25%;'>$name:</td>
	<td style='width: 25%;'>
		<select name='${rule}_CLASS' title='$title'>
$class_block		</select></td>";
	}

	# 2 columns
	for (my $r = 0; $r <= $#rules; $r += 2) {
		$rules[$r+1] = '' unless defined $rules[$r+1];
		print "<tr>" .$rules[$r] . $rules[$r+1] . "
</tr>
";
	}

	print "
</table>
";

	&closebox();

	return;
}

sub is_running
{
	my $running = qx{/sbin/tc qdisc list | fgrep htb | wc -l};
	chomp $running; # lose \n or 0\n is considered true!
	return $running;
}

