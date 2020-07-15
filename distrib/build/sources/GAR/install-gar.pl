#!/usr/bin/perl

use lib "/usr/lib/smoothwall";
use header  qw( :standard );

my %netsettings;
my $flag = '';
my $line;

readhash("/var/smoothwall/ethernet/settings", \%netsettings);
readhash("/var/smoothwall/main/productdata", \%prodata);

print "...Stopping GAR\n\n";
system("/usr/bin/smoothcom GARstop");

print "...Backing up settings and config files (if needed)\n\n";
if (-e "/var/smoothwall/mods/GAR/settings") {
  system("/bin/cp -f /var/smoothwall/mods/GAR/settings /tmp/GARsettings");
  system("/bin/cp -f /var/smoothwall/mods/GAR/etc/GAR.ignore /tmp");
  system("/bin/cp -f /var/smoothwall/mods/GAR/etc/GAR.target /tmp");
}

print "...Editing mod .conf files\n";

if (-f "/var/smoothwall/red/active")
{
  # fetch the addresses
  $netsettings{'RED_DEV'} = &getValue("/var/smoothwall/red/iface");
}

open(FILE, "/var/smoothwall/mods-available/GAR/etc/GAR.conf") or die 'Unable to open config file';
my @temp = <FILE>;
close FILE;

my $line;
open(FILE, ">/var/smoothwall/mods-available/GAR/etc/GAR.conf") or die 'Unable to open config file';
foreach $line (@temp) {
  chomp $line;
  if ($line =~ /^Interface/) {
    print FILE "Interface     $netsettings{'RED_DEV'}\n";
  } else {
    print FILE "$line\n";
  }
}
close FILE;

# Populate GAR ignore file with LAN NIC and RED DNS addresses
open (FILE, "</var/smoothwall/red/dns1") or die 'Unable to open dns file';
my $dns1 = <FILE>;
close FILE;
chomp $dns1;

open (FILE, "</var/smoothwall/red/dns2") or die 'Unable to open dns file';
my $dns2 = <FILE>;
close FILE;
chomp $dns2;

open (FILE, ">/var/smoothwall/mods-available/GAR/etc/GAR.ignore") or die 'Unable to open GAR ignore file';
print FILE "$dns1\n";
if ($dns2) { print FILE "$dns2\n" }
close FILE;

print "...Restarting smoothd\n";
system("/usr/bin/killall smoothd");
sleep 0.1;
system("/usr/sbin/smoothd");

system("/bin/touch", '/var/smoothwall/mods-available/GAR/installed');

print "Installation of GAR mod complete...\n\n";

EXIT:

# Function getValue() opens the specified file, reads the single line in it, and closes the
#   file. If the open() fails, the default value is "" (NULL string). 
sub getValue
{
  my ($file) = @_;

  # If the open fails, the var will be empty (NULL string).
  my $value = "";

  # Give it a go.
  if (open(FILE, "<$file"))
  {
    # There is one line; it has no terminating NL.
    $value = <FILE>;
    close FILE;
    # This chomp isn't needed for this specific purpose, but is here to make the
    #   function a little more generic.
    chomp $value;
  }

  # Return the value even if nothing was read.
  return $value;
}

