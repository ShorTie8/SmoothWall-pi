#!/usr/bin/perl

# Set up environment
use lib "/usr/lib/smoothwall";
use SmoothInstall qw( :standard );
use header  qw( :standard );

print "..You are about to remove the FFC mod from SWE 3.1\n\n";
print "..Are you sure this is what you want to do?\n\n";
print "Enter $GREEN [y] $NORMAL or $RED [n]: $NORMAL";
my $response = <STDIN>;
chomp $response;

until ( $response eq "y" or $response eq "n" )
{ do
	print "..That is $RED not a valid response!\n$NORMAL";
	print "..Please try again\n\n";
	print "Enter $GREEN [y]$NORMAL or $GREEN [n]:$NORMAL";
	chomp ( $response = <STDIN> );
}

if ( $response eq "n" ) {
	PRINT $YELLOW . "..Aborting uninstall. No files have been changed.\n\n";
	goto EXIT;
} elsif ($response eq "y" ) {
	print "..Are you uninstalling the FFC mod in order to apply an $RED official update\n$NORMAL";
	print "  to your Smoothwall Express 3.1 and, if so, do you want to restore only\n";
	print "  all SWE core files to original state and leave all mod files intact?\n";
	print "..($YELLOW No mod files $NORMAL will be affected by the official SWE update.)\n\n";

	print "Enter $GREEN [y] $NORMAL or $RED [n]: $NORMAL";
	my $response = <STDIN>;
	chomp $response;

	until ( $response eq "y" or $response eq "n" )
	{ do
		print "..That is $RED not a valid response!\n$NORMAL";
		print "..Please try again\n\n";
		print "Enter $GREEN [y]$NORMAL or $GREEN [n]:$NORMAL";
		chomp ( $response = <STDIN> );
	}

	if ( $response eq "n" ) {
		PRINT $YELLOW . "..Proceeding with complete removal of FFC for SWE 3.1.\n\n$NORMAL";
	} elsif ($response eq "y" ) {
		print "..Restoring all SWE 3.1 core files edited by FFC to original states.";
		sleep 1;
		print "		$YELLOW [DONE]\n$NORMAL";
		print "..Leaving all FFC mod files intact.\n\n";
		print "..$BLUE After installing$NORMAL the SWE update, you should run $YELLOW /var/smoothwall/mods/fullfirewall/edit-core.pl\n$NORMAL";
		print "  script to restore the edits to the core files needed by FFC to function correctly.\n\n";
		restore_core();
		goto EXIT1;
	}
}

print "..Do you wish to save the configuration files of this FFC installation?\n\n";
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
	PRINT $YELLOW . "..FFC configuration files deleted.\n\n$NORMAL";
} elsif ($response eq "y" ) {
	PRINT $YELLOW . "..Saving FFC configuration file\n\n$NORMAL";
       system("/usr/bin/tar zcf /tmp/ffc-config-backup.tgz /var/smoothwall/mods/fullfirewall/portfw/config /var/smoothwall/mods/fullfirewall/portfw/aliases /var/smoothwall/mods/fullfirewall/xtaccess/config");
	sleep 1;
}


unlink "/var/smoothwall/mods/fullfirewall/installed";
if (-d "/usr/lib/smoothwall/menu/3500_Firewall") {
  system("/bin/rm -rdf /usr/lib/smoothwall/menu/3500_Firewall");
}

system("/bin/mv -f /var/smoothwall/mods/fullfirewall/backup/setup /usr/sbin/setup");

system("/bin/rm -rdf /var/smoothwall/mods/fullfirewall");

restore_core();

EXIT1:

print "The system needs to be $RED rebooted$NORMAL for changes to take effect.\n";

EXIT:

sub restore_core
{
  my ($key, $filename);
  $key = "ffc1";
  $filename = "/etc/rc.d/rc.firewall.up";
  Remove($filename, $key);

  #$key = "ffc2";
  #Remove($filename, $key);

  $key = "ffc3";
  Remove($filename, $key);

  $key = "ffc4";
  Remove($filename, $key);

  $key = "ffc5";
  Remove($filename, $key);

  $key = "ffc6";
  Remove($filename, $key);

  $key = "ffc7";
  Remove($filename, $key);

  $key = "ffc8";
  Remove($filename, $key);

  $key = "ffc9";
  Remove($filename, $key);

  $key = "ffc10";
  Remove($filename, $key);

  $key = "ffc11";
  Remove($filename, $key);

  $key = "ffc12";
  Remove($filename, $key);

  $key = "ffc13";
  Remove($filename, $key);

  $key = "ffc14";
  Remove($filename, $key);

  $key = "ffc15";
  Remove($filename, $key);

  $key = "ffc16";
  Remove($filename, $key);

  open(FILE, "/etc/rc.d/rc.firewall.up") or die 'Unable to open rc.firewall.up';
  @lines = <FILE>;
  close FILE;

  open(FILE, ">/etc/rc.d/rc.firewall.up") or die 'Unable to open rc.firewall.up';
  foreach $pattern (@lines) {
    chomp $pattern;
    if ($pattern =~ /^\t\t--state NEW -j dmzholes/) {
      $pattern =~ s/dmzholes/ACCEPT/;
      print FILE "$pattern\n";
    } else {
      print FILE "$pattern\n";
    }
  }
  close FILE;

  $filename = "/etc/rc.d/rc.netaddress.up";
  $key = "ffc1";
  Remove($filename, $key);

  $key = "ffc2";
  Remove($filename, $key);

  $filename = "/etc/rc.d/rc.updatered";
  $key = "ffc1";
  Remove($filename, $key);
}
