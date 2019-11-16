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

#print <<END
#<p>
#	<a href='/cgi-bin/txt-bu-startAdd.cgi'>StartAdd</a><br>
#	<a href='/cgi-bin/txt-bu-cancelAdd.cgi'>CancelAdd</a><br>
#	<a href='/cgi-bin/txt-bu-addflag.cgi'>View flag</a><br>
#	<a href='/cgi-bin/txt-bu-setRsp.cgi?rsp=PatTest'>Set Name (PatTest)</a><br>
#</p>
#END
#;

# Signal the program abort
my $flagfile = "${swroot}/backup/CANCELadd";
system ("touch $flagfile");
