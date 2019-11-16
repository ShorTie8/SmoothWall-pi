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

# Get the response; there should be only *one* value passed via GET
my $response = $ENV{'QUERY_STRING'};
my ($rspName, $rspValue) = split (/=/, $response);

# The var name must be 'rsp'.
if ($rspName eq 'rsp') {
	# The response (drive's name) may consist of only a-z, A-Z, 0-9, '_' and '-'.
	# So lop off everything starting with the first 'illegal' char found.
	$rspValidate = $rspValue;
	$rspValidate =~ s/[^a-zA-z0-9_-].*//;

	# If the two are equal, drop the response into the response file.
	if ($rspValidate eq $rspValue) {
		open rspHdl, ">/var/smoothwall/backup/addResponse";
		print rspHdl $rspValue;
		close  rspHdl;
	}
}
# Otherwise assume miscreant and ignore it
# If needed, use Sys::Syslog to log the attempt
