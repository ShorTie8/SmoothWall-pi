#!/usr/bin/perl

use lib "/usr/lib/smoothwall";
use SmoothInstall qw( :standard );

print "..You are about to edit the SWE core files used by the FFC mod to restore all FFC functions.\n\n";
print "..Is this what you want to do?\n\n";
print "Enter $GREEN [y] $NORMAL or $RED [n]: $NORMAL";
$response = <STDIN>;
chomp $response;

until ( $response eq "y" or $response eq "n" )
{ do
	print "..That is $RED not a valid response!\n$NORMAL";
	print "..Please try again\n\n";
	print "Enter $GREEN [y]$NORMAL or $GREEN [n]:$NORMAL";
	chomp ( $response = <STDIN> );
}

if ( $response eq "n" ) {
	print "..Aborting the edit of core files.\n";
	goto EXIT;
} elsif ($response eq "y" ) {
	print "..Proceeding with editing of SWE core files to restore FFC function.\n";
	sleep 1;
}
my (@lines, $key, $pattern, $filename);

$filename = "/etc/rc.d/rc.firewall.up";
$key = "ffc1";
$pattern = "iptables -N portfwf";
CommentOut($filename, $key, $pattern);

#$key = "ffc2";
#$pattern = "iptables -A FORWARD -j portfwf";
#CommentOut($filename, $key, $pattern);

$key = "ffc3";
$pattern = "Spoof protection for RED";
@lines = ('# Port forwarding', '/sbin/iptables -N portfwf', '/sbin/iptables -N portfwi', '/sbin/iptables -N subnetchk', '/sbin/iptables -A FORWARD -m state --state NEW -j portfwf', '/sbin/iptables -A INPUT -m state --state NEW -j portfwi');
InsertBefore($filename, $key, $pattern, @lines);

$key = "ffc4";
$pattern = "/sbin/iptables -t nat -A PREROUTING -j portfw";
@lines = ('# Port forwarding', '/sbin/iptables -t nat -N portfw_pre', '/sbin/iptables -t nat -I PREROUTING -j portfw_pre', '/sbin/iptables -t nat -N portfw_post', '/sbin/iptables -t nat -I POSTROUTING -j portfw_post');
InsertBefore($filename, $key, $pattern, @lines);

$key = "ffc5";
$pattern = "/sbin/iptables -A FORWARD -i ppp0 -j portfwf";
CommentOut($filename, $key, $pattern);

$key = "ffc6";
$pattern = "/sbin/iptables -A FORWARD -i ippp0 -j portfwf";
CommentOut($filename, $key, $pattern);

$key = "ffc7";
$pattern = '^if \[ "\$RED_DEV" != "" \]; then.\t/sbin/iptables -A FORWARD -i \$RED_DEV -j portfwf.fi';
CommentOut($filename, $key, $pattern);

$key = "ffc8";
$pattern = '/sbin/iptables -A FORWARD -m mark --mark 1 -j portfwf';
CommentOut($filename, $key, $pattern);

$key = "ffc9";
$pattern = '^if \[ "\$ORANGE_DEV" != "" \]; then.\t/sbin/iptables -A FORWARD -m mark --mark 2 -j portfwf.fi';
CommentOut($filename, $key, $pattern);

$key = "ffc10";
$pattern = '^if \[ "\$PURPLE_DEV" != "" \]; then.\t/sbin/iptables -A FORWARD -m mark --mark 3 -j portfwf.fi';
CommentOut($filename, $key, $pattern);

$key = "ffc11";
$pattern = '/sbin/iptables -N timedaction.#/sbin/iptables -A timedaction -j LOG --log-prefix "Denied-by-filter:tim-act "./sbin/iptables -A timedaction -p tcp -m state --state ESTABLISHED -j REJECT --reject-with tcp-reset./sbin/iptables -A timedaction -j REJECT --reject-with icmp-admin-prohibited';
CommentOut($filename, $key, $pattern);

$key = "ffc12";
$pattern = '/sbin/iptables -A INPUT -j timedaccess./sbin/iptables -A FORWARD -j timedaccess';
@lines = ('/sbin/iptables -A INPUT -j timedaccess', '/sbin/iptables -A timedaccess -j RETURN');
Change($filename, $key, $pattern, @lines);

$key = "ffc13";
$pattern = '/sbin/iptables -N outgreen./sbin/iptables -N outorange./sbin/iptables -N outpurple./sbin/iptables -N allows';
CommentOut($filename, $key, $pattern);

$key = "ffc14";
$pattern = '/sbin/iptables -N outbound./sbin/iptables -A outbound -p icmp -j ACCEPT./sbin/iptables -A outbound -j allows./sbin/iptables -A outbound -i \$GREEN_DEV -j outgreen.if \[ "\$ORANGE_DEV" != "" \]; then.\t/sbin/iptables -A outbound -i \$ORANGE_DEV -j outorange.fi.if \[ "\$PURPLE_DEV" != "" \]; then.\t/sbin/iptables -A outbound -i \$PURPLE_DEV -j outpurple.fi';
CommentOut($filename, $key, $pattern);

$key = "ffc15";
$pattern = '/sbin/iptables -A FORWARD -m state --state NEW -o ppp0 -j outbound./sbin/iptables -A FORWARD -m state --state NEW -o ippp0 -j outbound.if \[ "\$RED_DEV" != "" \]; then.\t/sbin/iptables -A FORWARD -m state --state NEW -o \$RED_DEV -j outbound.fi';
CommentOut($filename, $key, $pattern);

$key = "ffc16";
$pattern = '/sbin/iptables -A INPUT -i lo -j ACCEPT\n\n';
@lines = ('# Setup chains for controlling outgoing conns. Place them
# here so that setting timed access on outgoing rules can immediately
# shut down all outgoing traffic from a source device or machine if desired
/sbin/iptables -N tofcScreen    # FORWARD prescreen; some traffic is always allowed
/sbin/iptables -N tofcPrxScreen # INPUT prescreen; some traffic is always allowed
/sbin/iptables -N tofcfwd2Int   # Filter inbound packets
/sbin/iptables -N tofcfwd2Ext   # Filter outbound packets
/sbin/iptables -N tofcproxy     # Filter proxied outbound conns in INPUT
/sbin/iptables -N tofcblock     # The final arbiter

# Put a default blocker in tofcblock; setportfw will replace it soon enough.
/sbin/iptables -A tofcblock -j REJECT

# Never touch certain traffic; filter the rest
#   Always accept outbound ICMP
/sbin/iptables -A tofcScreen -p icmp -j ACCEPT
#   Always accept related conns
#     There is no way to determine which TOFC entry would apply, so we have to
#     blindly accept them
/sbin/iptables -A tofcScreen -m connmark --mark ${related}/${connRelMask} -j ACCEPT
#   send packets from RED to tofcfwd2Int
if [ "$RED_DEV" != "" ]; then
  /sbin/iptables -A tofcScreen -i $RED_DEV -j tofcfwd2Int
fi
/sbin/iptables -A tofcScreen -i ppp0 -j tofcfwd2Int
/sbin/iptables -A tofcScreen -i ippp0 -j tofcfwd2Int
#   send the rest to tofcfwd2Ext
/sbin/iptables -A tofcScreen -j tofcfwd2Ext
/sbin/iptables -A tofcPrxScreen -j tofcproxy

# Send all outbound and proxied outbound conns to the tofc chains
/sbin/iptables -A FORWARD -m connmark --mark ${typeOutbound}/${connTypeMask} -j tofcScreen
/sbin/iptables -A INPUT -m connmark --mark ${typeInt2FW}/${connTypeMask} -j tofcPrxScreen

');
InsertAfter($filename, $key, $pattern, @lines);

open(FILE, "$filename") or die 'Unable to open config file';
@lines = <FILE>;
close FILE;

open(FILE, ">$filename") or die 'Unable to open config file';
foreach $pattern (@lines) {
  chomp $pattern;
  if ($pattern =~ /^\t\t--state NEW -j ACCEPT/) {
    $pattern =~ s/ACCEPT/dmzholes/;
    print FILE "$pattern\n";
  } else {
    print FILE "$pattern\n";
  }
}
close FILE;

print "Done editing rc.firewall.up...\n\n";

$filename = "/etc/rc.d/rc.netaddress.up";
$key = "ffc1";
$pattern = 'echolog "e" "s" "" "  DMZ pinholes"
/usr/bin/smoothcom setinternal';
CommentOut($filename, $key, $pattern);

$key = "ffc2";
$pattern = 'echolog "e" "s" "" "  Timed Access IPs"
/usr/bin/smoothcom settimedaccess';
CommentOut($filename, $key, $pattern);

$filename = "/etc/rc.d/rc.updatered";
$key = "ffc1";
$pattern = 'echolog "E" "s" "" "..RED filtering"
/usr/bin/smoothcom setincoming

/usr/bin/smoothcom setoutgoing';
@lines = ('if [ ! -s "/var/smoothwall/mods/fullfirewall/portfw/config" ]; then
 echolog "E" "s" ""  "..setting up default outgoing rules"
 /usr/bin/smoothcom wrtdefaults
fi

echolog "E" "s" ""  "..RED aliases if they exist"
/usr/bin/smoothcom ifaliasup
echolog "E" "s" ""  "..incoming, outgoing and internal filtering"
/usr/bin/smoothcom setportfw
');
Change($filename, $key, $pattern, @lines);

print "Done editing rc.updatered...\n\n";

print "..Done editing SWE 3.1 core files to restore FFC function.\n";

EXIT:
