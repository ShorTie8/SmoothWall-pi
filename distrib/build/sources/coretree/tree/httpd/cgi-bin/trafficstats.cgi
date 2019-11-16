#!/usr/bin/perl

use lib "/usr/lib/smoothwall";
#use header qw(:standard);
use strict;
use warnings;

my (%incaddr, %outaddr, @out);
my $ADDRS_TO_SHOW = 5;
my $BARS = '';

print <<END
Pragma: no-cache
Cache-control: no-cache
Connection: close
content-type: text/html

END
;

# We must pry to see if bwbars or someone else is the caller.
my @query=split(/&/, $ENV{'QUERY_STRING'});
foreach my $i (@query) {
	my ($nm, $vl) = split(/=/, $i);
	if ($nm eq 'BARS') {
		$BARS = $vl;
	}
}
#warn "BARS=$BARS";

#my  = ();
open INPUT, "</var/log/quicktrafficstats";

while ( my $line = <INPUT> ) {
	next if ( not $line =~ /^cur_/ );

	my ( $rule, $interface, $value ) = ( $line =~ /cur_(inc|out)_rate_([^=]+)=([\d\.]+)$/i );

	# Skip 0.0.0.0 if bwbars is the caller
	next if ($interface =~ /0.0.0.0.*/ && $BARS ne "");

	# Skip if 0 bps and the caller is NOT bwbars
	next if ($value == 0 && $BARS eq "");

	if ($interface =~ /^\d+\.\d+\.\d+\.\d+/) {
		if($rule eq 'out') {
			$outaddr{$interface} = [$value,$line];
		}
		if($rule eq 'inc') {
			$incaddr{$interface} = [$value,$line];
		}
	}
	else {
		push @out, $line;
	}
}

my @biggest_users = sort { $incaddr{$b}->[0] cmp $incaddr{$a}->[0]; } keys %incaddr;
my $num_users = scalar(@biggest_users);

# Truncate to the top five if bwbars is NOT the caller
if(($num_users > $ADDRS_TO_SHOW) && ($BARS eq "")) {
	splice(@biggest_users,$ADDRS_TO_SHOW);
	#warn "Ignoring " . ($num_users - $ADDRS_TO_SHOW);
}
print @out;

for (@biggest_users) {
	# Traffic may be zero in one direction only, which would have been removed by line 44.
	# Stop undefined variables being printed by making sure both inc & out values exist.
	if (($incaddr{$_}->[1]) && ($outaddr{$_}->[1])) {
		print $incaddr{$_}->[1], $outaddr{$_}->[1];
	}
}
print "\n";
close INPUT;

