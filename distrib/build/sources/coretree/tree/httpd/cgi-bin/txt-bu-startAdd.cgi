#! /usr/bin/perl

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use POSIX qw(setsid);

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

my $flagfile = "${swroot}/backup/addFlag";

system ("touch $flagfile");
sleep 1;

# Start the program in the background
my $pid = fork();
if (defined $pid && $pid == 0) {
	setsid();
	close(STDIN);
	close(STDOUT);
	close(STDERR);
	sleep 1;
	my $pid = fork();
	if (defined $pid && $pid == 0) {
		#exec("/usr/bin/smoothwall/backup_sys -V </dev/null >/dev/null 2>&1");
		exec("bash -x /usr/bin/smoothwall/backup_sys -V </dev/null > /var/smoothwall/backup/add.log 2>&1");
		exit 255;
	}
	exit;
}
wait;

system ("/usr/bin/inotifywait -e close_write $flagfile >/var/smoothwall/backup/inot.log 2>&1");

if (-e $flagfile) {
	open FLAG, $flagfile;
	read FLAG, $flag, 500;
	close FLAG;
	chomp $flag;
	print $flag;
}

exit;
