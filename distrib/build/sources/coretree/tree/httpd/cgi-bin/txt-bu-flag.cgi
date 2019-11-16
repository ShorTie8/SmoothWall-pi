#! /usr/bin/perl

use lib "/usr/lib/smoothwall";
use header qw( :standard );

print <<END
Pragma: no-cache
Cache-control: no-cache
Connection: close
content-type: text/html

END
;

my $flagfile = "${swroot}/backup/flag";

if (-e $flagfile) {
	open FLAG, $flagfile;
	read FLAG, $flag, 500;
	close FLAG;

	chomp $flag;
	print $flag;
}
