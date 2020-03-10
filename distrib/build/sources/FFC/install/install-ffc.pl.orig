#!/usr/bin/perl

use lib "/usr/lib/smoothwall";
use SmoothInstall qw( :standard );
use header  qw( :standard );
use smoothd qw( message );

my $flag = '';

open(FILE, "/var/smoothwall/patches/installed") or die "Unable to open patches file";
while (<FILE>) {
 if ($_ =~ /^008/) {
  $flag = 'y';
 }
} 
close FILE;

if ($flag ne 'y') {
 print "This mod requires that Update8 be installed.\n\n";
 print "Please update your SWE 3.1 to Update8 before proceeding with the installation of this mod.\n\n";
 goto EXIT;
}

my %prodata;
my $response;
my $flag = '';

&readhash("/var/smoothwall/main/productdata", \%prodata);

if (-e "/var/smoothwall/mods/fullfirewall/installed")
{
 PRINT $YELLOW . "There is a previous version of FFC installed...\n\n$NORMAL ";
 print "Please uninstall the previous version before installing this new version..\n\n";
 print "During the uninstall of FFC you will have the option of backing up your config files...\n";
 print "You may then restore your config files during installation of this update of FFC...\n\n";
 goto EXIT;
}

if (-d "/var/smoothwall/mods/fullfirewall/usr/lib/smoothwall/menu/5000_Logs")
{
 system("/bin/rm -rdf /var/smoothwall/mods/fullfirewall/usr/lib/smoothwall/menu/5000_Logs");
 system("/bin/rm -rdf /var/smoothwall/mods/fullfirewall/httpd/cgi-bin/logs.cgi/log.dat");
}

if (-e "/var/smoothwall/mods/fullfirewall/usr/lib/smoothwall/menu/6000_Tools")
{
 system("/bin/rm -rf /var/smoothwall/mods/fullfirewall/usr/lib/smoothwall/menu/6000_Tools");
 unlink "/var/smoothwall/mods/fullfirewall/httpd/cgi-bin/smoothinfo.cgi";
 unlink "/var/smoothwall/mods/fullfirewall/usr/lib/smoothd/syssmoothinfo.so";
 system("/bin/rm -rf /var/smoothwall/mods/fullfirewall/usr/bin/smoothwall/smoothinfo*");
}

my (@lines, $key, $pattern, $filename);

$filename = "/etc/rc.d/rc.firewall.up";
$key = "ffc1";
$pattern = "iptables -N portfwf";
CommentOut($filename, $key, $pattern);

#$key = "ffc2";
#$pattern = "iptables -A FORWARD -j portfwf";
#CommentOut($filename, $key, $pattern);

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

$key = "ffc3";
$pattern = "IPSEC itself";
@lines = ('# Port forwarding', '/sbin/iptables -N portfwf', '/sbin/iptables -N portfwi', '/sbin/iptables -N subnetchk', '/sbin/iptables -A FORWARD -j portfwf', '/sbin/iptables -A INPUT -j portfwi');
InsertBefore($filename, $key, $pattern, @lines);

$key = "ffc4";
$pattern = "/sbin/iptables -t nat -A PREROUTING -j portfw";
@lines = ('# Port forwarding', '/sbin/iptables -t nat -N portfw_pre', '/sbin/iptables -t nat -I PREROUTING -j portfw_pre', '/sbin/iptables -t nat -N portfw_post', '/sbin/iptables -t nat -I POSTROUTING -j portfw_post');
InsertAfter($filename, $key, $pattern, @lines);

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

system("/usr/bin/tar -jxf /tmp/ffc-modfiles.tar.bz2 -C /");
unlink "/tmp/ffc-modfiles.tar.bz2";

system("/bin/mv -f /usr/sbin/setup /var/smoothwall/mods/fullfirewall/backup/setup");

# If installing 32 bit
if ($prodata{'ARCH'} eq 'i586')
{
 print "Installing 32-bit version of mod...\n\n";
 system("/bin/mv -f /var/smoothwall/mods/fullfirewall/bin/setup /usr/sbin/setup");
}
# If installing 64 bit
elsif ($prodata{'ARCH'} eq 'x86_64')
{
 print "Installing 64-bit version of mod...\n\n";
 system("/bin/mv -f /var/smoothwall/mods/fullfirewall/bin/sysiptables64.so /var/smoothwall/mods/fullfirewall/usr/lib/smoothd/sysiptables.so");
 #system("/bin/mv -f /var/smoothwall/mods/fullfirewall/bin/syssmoothinfo64.so /var/smoothwall/mods/fullfirewall/usr/lib/smoothd/syssmoothinfo.so");
 system("/bin/mv -f /var/smoothwall/mods/fullfirewall/bin/setup-64 /usr/sbin/setup");
} else {
 print "ERROR: Unable to detect correct SWE architecture type!\n\n";
 print "Exiting installation.\n";
 goto EXIT;
}

system("/bin/touch", '/var/smoothwall/mods/fullfirewall/installed');

#print "Editing dispaliastab...\n";
#system("/usr/lib/smoothwall/fix-d-a-t.sh");
#unlink "/usr/lib/smoothwall/fix-d-a-t.sh";

# Determine the RED device
my $reddev = `/bin/cat /var/smoothwall/red/iface`;
chomp $reddev;

# Restart Smoothd to install new module
StopMod("/usr/sbin/smoothd", "Smoothd");
StartMod("/usr/sbin/smoothd", "Smoothd");

if (-e "/tmp/ffc-config-backup.tgz") {
  system("/usr/bin/tar zxvf /tmp/ffc-config-backup.tgz -C /");
  unlink "/tmp/ffc-config-backup.tgz";
  goto EXIT1;
}

if (-d "/var/smoothwall/mods/proxy") {
 if (-e "/var/smoothwall/mods/fullfirewall/httpd/cgi-bin/proxy.cgi") {
  unlink "/var/smoothwall/mods/fullfirewall/httpd/cgi-bin/proxy.cgi";
  system("/bin/rm -rf /var/smoothwall/mods/fullfirewall/usr/lib/menu/2000_Services");
 }
}

my ($configline, @config_file);

print "Checking for $GREEN existing stock incoming $NORMAL port forwarding rules $NORMAL or existing rules in $GREEN FFC format...$NORMAL\n\n";
if (-z "/var/smoothwall/portfw/config" and !(-e "/tmp/ffc-config-backup.tgz")) {
  print "No old port forwarding rules exist: conversion to FFC format not necessary...\n";
  print "Continuing with FFC installation...\n";
  sleep 2;
} elsif (-e "/tmp/ffc-config-backup.tgz") {
  print "There are config files from a previous FFC installation detected..\n\n";
  print "Would you like to restore them now?..\n\n";
  print "Enter $GREEN [y] $NORMAL or $RED [n]: $NORMAL";
  $response = <STDIN>;
  chomp $response;

  until ( $response eq "y" or $response eq "n" )
  { do
	print "That is $RED not a valid response!\n$NORMAL";
	print "Please try again\n\n";
	print "Enter $GREEN [y]$NORMAL or $GREEN [n]:$NORMAL";
	chomp ( $response = <STDIN> );
  }

  if ( $response eq "n" ) {
	print "Now proceeding with standard installation without restoration of previously saved files..\n\n";
  } elsif ($response eq "y" ) {
       print "Restoring configuration files (config and aliases) from previous installation of FFC..\n\n";
	if (-e "/tmp/ffc-config-backup.tgz") {
         system("/usr/bin/tar -zxf /tmp/ffc-config-backup.tgz -C /");
	  unlink "/tmp/ffc-config-backup.tgz";
         $flag = 'set';
	}
  }
}

if ($flag eq '') {
 if (-z "/var/smoothwall/portfw/config") {
  system("/bin/touch", '/var/smoothwall/mods/fullfirewall/portfw/config');
  system("/bin/chown nobody:nobody /var/smoothwall/mods/fullfirewall/portfw/config");
 } elsif (!(-z "/var/smoothwall/portfw/config")) {
  print "Converting old port forwarding rules to FFC format, if any exist...\n\n";
  open (FILE, "/var/smoothwall/portfw/config") or die 'Unable to open portfw config file';
  my @temp = <FILE>;
  close FILE;

  my $line;
  my $cnt = 0;
  my @split;
  foreach $line (@temp) {
   chomp $line;
   @split = split (/\,/, $line);
   $cnt++;
   if ($split[0] eq "tcp") {
    $split[0] = "6";
   } elsif ($split[0] eq "udp") {
    $split[0] = "17";
   } else {
    next;
   }
   $configline .= "$cnt,$reddev,0.0.0.0/0,$split[2],any,$split[3],$split[4],$split[0],ACCEPT,$split[5],off,off,,\n";
  }
# open(FILE, ">/var/smoothwall/portfw/config") or die 'Unable to open config file';
# close FILE;
 }

 # Setup default outgoing rules
 message('wrtdefaults');

 if ($configline) {
 open(FILE, ">>/var/smoothwall/mods/fullfirewall/portfw/config") or die 'Unable to open config file';
 print FILE "$configline";
 close FILE;

 $cnt = 0;
 open(FILE, "/var/smoothwall/mods/fullfirewall/portfw/config") or die 'Unable to open config file';
 my @temp = <FILE>;
 close FILE;

 open(FILE, ">/var/smoothwall/mods/fullfirewall/portfw/config") or die 'Unable to open config file';
 foreach $line (@temp) {
  chomp $line;
  $cnt++;
  @split = split /,/, $line;
  print FILE "$cnt,$split[1],$split[2],$split[3],$split[4],$split[5],$split[6],";
  print FILE "$split[7],$split[8],$split[9],$split[10],$split[11],$split[12],$split[13]\n";
 }
 close FILE;
 }
 sleep 2;
}

EXIT1:

print "Converting old $GREEN external access rules $NORMAL to $GREEN FFC format $NORMAL if they exist...\n\n";
if (!(-z "/var/smoothwall/xtaccess/config")) {
	$configline = '';
	open(FILE, "/var/smoothwall/xtaccess/config") or die 'Unable to open xtaccess config';
	my @rules = <FILE>;
	close FILE;

	foreach $line (@rules) {
		chomp $line;
		@split = split(/\,/, $line);
		if ($split[0] eq "tcp") {
			$configline .= "$reddev,6,$split[1],$split[2],$split[3],$split[4]\n";
		} elsif ($split[0] eq "udp") {
			$configline .= "$reddev,17,$split[1],$split[2],$split[3],$split[4]\n";
		} else {
			$configline .= "$line\n";
		}
	}
	open(FILE, ">/var/smoothwall/mods/fullfirewall/xtaccess/config") or die 'Unable to open xtaccess config file';
	flock FILE, 2;
	print FILE "$configline";
	close FILE;
}

if (-d "/usr/lib/smoothwall/menu/3500_Firewall") {
  system("/bin/rm -rdf /usr/lib/smoothwall/menu/3500_Firewall");
}

PRINT $CYAN . "The system needs to be rebooted for changes to take effect.\n \n$NORMAL";
PRINT $CYAN . "Please enter [y] to reboot system now or enter [n] to reboot later.\n \n$NORMAL";
print "Enter $GREEN [y] $NORMAL or $RED [n]: $NORMAL";
$response = <STDIN>;
chomp $response;

until ( $response eq "y" or $response eq "n" )
{ do
	print "That is $RED not a valid response!\n$NORMAL";
	print "Please try again\n\n";
	print "Enter $GREEN [y]$NORMAL or $GREEN [n]:$NORMAL";
	chomp ( $response = <STDIN> );
}

if ( $response eq "n" ) {
	PRINT $YELLOW . "Full Firewall Control mod installation not complete until reboot is done...\n \n$NORMAL";
	PRINT $YELLOW . "Please remember to reboot your system later for changes to take effect\n$NORMAL";
	PRINT $YELLOW . "Please post in the SmoothWall 3.1 Homebrew Forum for any help\n \n$NORMAL";
} elsif ($response eq "y" ) {
	PRINT $YELLOW . "Full Firewall Control mod installation is complete\n \n";
	PRINT $YELLOW . "Please post in the SmoothWall 3.1 Homebrew Forum for any help\n \n";
	sleep 3;
	system("/usr/bin/smoothcom systemrestart");
}

EXIT:
