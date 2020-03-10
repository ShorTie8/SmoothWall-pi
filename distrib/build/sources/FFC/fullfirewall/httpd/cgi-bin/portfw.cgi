#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
#
# Updated 02/24/2008 - Stanford Prescott MD v3.0-0.9 and v3.0-0.9.1 beta versions
#  - Ported Drew S. Dupont's (NetWhiz) Full Firewall Control mod and Toby Long-Leather's (TobyLL) Multiple IPs mod to SmoothWall
#	3.0 and combined the two into one mod
#  - Converted NetWhiz's setportfw setuid wrapper to a SmoothD module. Added code to bring down and bring up new interface aliases
#	to the new sysportfw.so smoothd module and removed the code from the rc.netaddress.down and rc.netaddress.up scripts
#  - Adding or removing aliases no longer requires a network restart. The individual aliases are brought up and down as needed
#  - Revamped how the GUI handles adding, editing and removing interface aliases
#  - When an alias is removed any associated portfw rules with that alias are also removed
#  - Added ability to enable/disable portfw rules without editing or deleting them
#  - Added "smoothtype" javascript checks to address and netmask entries for aliases
#  - Changed the aliases display table to SWE 3.0 displaytable format
#  Updated 06/19/2008
#  - Removed ability to add LAN aliases
#  - Added ability to add a LAN IP to be associated with an alias for outbound SNAT "server mapping"
#  Final release 06/28/2008
#  - sysportfw.so completely rewritten by Steve Pittman (aka MtnLion) for improved bouncing port forwards
#  - and SNAT outbound masking for 1:1 server mapping to an alias
#  Many updates too numerous to list right now. 10/2/2010
#  - Code contributed by Steve McNeil to enable control of subnet check routine from GUI
#  Many more changes to combine incoming, outgoing and internal frowarding into a single UI for SWE 3.1. 8/10/2013
#  - Integration of x-table add-on modules.
#
use lib "/usr/lib/smoothwall";
use lib "/var/smoothwall/mods/fullfirewall/usr/lib/perl5";
use lib "/var/smoothwall/mods/fullfirewall/usr/lib/perl5/site_perl/5.14.4";

use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );

use Socket;
use NetAddr::IP;
use Net::Netmask;
use Stans::modlib;

my (%netsettings, %availablenetdevices, %settings);
&readhash( "${swroot}/ethernet/settings", \%netsettings );
&readhash("${swroot}/mods/fullfirewall/DETAILS", \%versionsettings);

my $gdev = $netsettings{'GREEN_DEV'};
my $pdev = $netsettings{'PURPLE_DEV'};
my $odev = $netsettings{'ORANGE_DEV'};

if ( -e "${swroot}/mods/fullfirewall/portfw/settings" ) {
    &readhash( "${swroot}/mods/fullfirewall/portfw/settings", \%settings );
}

# Subroutine for sorting things numerically instead of as strings
sub numerically { $a <=> $b; }

my $filedir   = "${swroot}/mods/fullfirewall";
my $aliasfile = "$filedir/portfw/aliases";
my $settings  = "${swroot}/ethernet/settings";
my $hashfile = "$filedir/portfw/confighash";
my @colours   = ( "RED", "GREEN" );
if ( $netsettings{'ORANGE_DEV'} ) {
    push( @colours, "ORANGE" );
}
if ( $netsettings{'PURPLE_DEV'} ) {
    push( @colours, "PURPLE" );
}

# Determine red interface type and ip address
my $sweRed = "/var/smoothwall/red";
my $redip = '';

# File 'active' exists only when RED is up; that is, PPP is up and running, dhcpcd got an
#   address, or RED is STATIC. If PPP is down or dhcpcd lost the lease, the files are emptied
#   and 'active' is deleted. But the rest of the files should always exist, empty or not.

if (-f "$sweRed/active")
{
  # fetch the addresses
  $netsettings{'RED_DEV'} = &getValue("$sweRed/iface");
  $redip = &getValue("$sweRed/local-ipaddress");
}
else
{
  $errormessage .= "Red is not active.<br />";
}

my ( %cgiparams, %selected, %checked );
my $filename = "$filedir/portfw/config";

&showhttpheaders();

$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'}  = $tr{'log ascending'};

if ( $ENV{'QUERY_STRING'} and ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" ) )
{
    my @temp = split( ',', $ENV{'QUERY_STRING'} );
    $cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[1] and $temp[1] ne "" );
    $cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[0] and $temp[0] ne "" );
}

$cgiparams{'OLDID'}           = 0;
$cgiparams{'ENABLED'}         = 'off';
$cgiparams{'ADDRESS_ENABLED'} = 'off';

$cgiparams{'RULE_COUNT'}  = 0;
$cgiparams{'DESCRIPTION'} = '';
&getcgihash( \%cgiparams );

my $errormessage = '';
my $updatebutton = 0;

# Check for add or update action
if (   $cgiparams{'ACTION'} eq $tr{'add'} or $cgiparams{'ACTION'} eq $tr{'ffc-update'} )
{
    my $src_if    = $cgiparams{'SRC_IFACE'};
    my $dst_if    = $cgiparams{'DEST_IFACE'};
    my $protocol  = $cgiparams{'PROTOCOL'};
    my $service   = $cgiparams{'SERVICE'};
    my $dst_port  = $cgiparams{'DEST_PORT'};
    my (@proxy, @vars, $var);

    &writehash("$hashfile", \%cgiparams);

    my $sipmac = $cgiparams{'SRC_IPMAC'};
    my $dipmac = $cgiparams{'DEST_IPMAC'};

    if ( $sipmac =~ /^\!/ ) {
       $sipmac =~ s/^\!//;
    }

    if (($cgiparams{'SRC_IFACE'} ne $netsettings{'RED_DEV'} and !($cgiparams{'SRC_IFACE'} =~ /:/)) and $cgiparams{'NEW_DEST_PORT'} ne "") {
       $errormessage .= "You cannot redirect to another port with an outgoing rule!<br />";
    }

    if ($cgiparams{'SRC_IFACE'} eq $cgiparams{'DEST_IFACE'}) {
       $errormessage .= "You cannot forward an interface to itself!<br />";
    }

    unless ($dst_port =~ /[a-zA-Z]/) {
       @vars = split /,/, $dst_port;
       foreach $var (@vars) {
         if ($var =~ /:/) {
           unless (&validportrange($var)) {
             $errormessage .= "Invalid port range.<br />";
           }
         } else {
           unless (&validport($var)) {
             $errormessage .= "Invalid port number.<br />";
           }
         }
       }
    }

    # If the port begins with a letter, it's a service name
    if ($dst_port =~ /[a-zA-Z]/) {
      $service = $dst_port;
    }

    # Prepare the port numbers, or show 'not applicable'
    if ( $service eq "user" )
    {
      if ( $protocol eq "6" or $protocol eq "17" or $protocol eq "TCP&UDP" ) {
        if ($dst_port eq "") {
          $service = 'N/A';
        } else {
          $service = $dst_port;
        }
      } else {
        $service = 'N/A';
      }
    }
    
    $setproxy = 'off';

    # Get user-specified port nums/ranges
    if ($dst_port) {
      $service = $dst_port;
      $service =~ s/,/-/g;

      # Note if proxy is needed
      @proxy = split /-/, $service;
      foreach $var (@proxy) {
        if ($var eq '80' or $var eq '443') {
          $setproxy = 'on';
          last;
        }

        if ($var =~ /:/) {
          unless (&validportrange($var)) {
            $errormessage .= "Port range in original destination port $tr{'destination port numbers'}<br />";
          }
        }
      }
    }

    if ($service eq "Web") {
       $setproxy = 'on';
    }

    # Check for new destination port entry errors
    if ( $cgiparams{'NEW_DEST_PORT'} ) {
      unless ( &validportrange( $cgiparams{'NEW_DEST_PORT'} ) ) {
        $errormessage .= "Port range in new destination port $tr{'destination port numbers'}<br />";
      }
      if ($service =~ /-/ or $service =~ /[a-zA-Z]/) {
        $errormessage .= "Redirecting non-consecutive groups of ports is not allowed! Ports must be single or in a range.<br />";
      }
      if ($cgiparams{'NEW_DEST_PORT'} =~ /:/ and $service =~ /:/) {
        my @orig = split /:/, $service;
        my @new = split /:/, $cgiparams{'NEW_DEST_PORT'};

        my @orig_array = ($orig[0] .. $orig[1]);
        my @new_array = ($new[0] .. $new[1]);

        my $orig_size = @orig_array;
        my $new_size = @new_array;

        if ($orig_size != $new_size) {
          $errormessage .= "When redirecting incoming ports, port ranges must be equal in size!<br />";
        }
      }
    } else {
        $cgiparams{'NEW_DEST_PORT'} = 0;
    }


    # If a VPN service was specified, store the most specific name in 'protocol'
    if ( $cgiparams{'SERVICE'} eq "VPNs" ) {
      $protocol = "VPNs";
    }
    if ( $cgiparams{'SERVICE'} eq "500:4500" ) {
      $protocol = "IPSec";
    }
    if ( $cgiparams{'SERVICE'} eq "1723" ) {
      $protocol = "PPTP";
    }
    if ( $cgiparams{'SERVICE'} eq "1194:1195" ) {
      $protocol = "OpenVPN";
    }

    # PPTP protocol knows its ports; don't specify them
    if ($protocol eq "PPTP" or $protocol eq "IPSEC") {
      if ($service ne "user" and $port ne "") {
        $errormessage .= "$tr{'ffc-port and protocol'}<br />\n";
      }
    }

    # If XBox is selected, set protocol to UDP
    if ($service eq "XBox") {
      $protocol = '17';
    }

    # Currently only DNS
    if ($service eq 'Infrastructure') {
      $protocol = 'TCP&UDP';
    }

    if ( $cgiparams{'SRC_IPMAC'} eq '' ) {
      $cgiparams{'SRC_IPMAC'} = '0.0.0.0/0';
    }

    if ( $cgiparams{'DEST_IPMAC'} eq '' ) {
      $cgiparams{'DEST_IPMAC'} = '0.0.0.0/0';
    }

    #################
    # Error checking
    #################
    unless ( $cgiparams{'PROTOCOL'} eq "6"
        or $cgiparams{'PROTOCOL'} eq "17"
        or $cgiparams{'PROTOCOL'} eq "TCP&UDP" )
    {
        unless (!( $dst_port )
            and !( $cgiparams{'NEW_DEST_PORT'} ) )
        {
            $errormessage .= "You cannot specify a port with that protocol<br />";
        }
    }

    # Check for source/destination port being defined
    if ( ( $dst_port != 0 ) or ( $cgiparams{'NEW_DEST_PORT'} != 0 ) )
    {
        # Check for protocol being all
        if ( $cgiparams{'PROTOCOL'} eq 'all' ) {
          $errormessage .= "$tr{'error source-destination port protocol any'}<br />";
        }

        # Check for dest. IP/MAC being empty
        if ( $cgiparams{'DEST_IPMAC'} eq '' ) {
          $errormessage .= "$tr{'error source-destination port destination any'}<br />";
        }
    }

    # Check for source and destination ports being equal
    if ( ( $dst_port != 0 ) and ( $cgiparams{'NEW_DEST_PORT'} != 0 ) )
    {
        if ( $dst_port eq $cgiparams{'NEW_DEST_PORT'} ) {
            $cgiparams{'NEW_DEST_PORT'} = 0;
        }
    }

    # Check for source port being defined if destination port is defined-error if not
    if ( ( $service eq 'user' ) and ( $cgiparams{'NEW_DEST_PORT'} ne '' ) )
    {
      $errormessage .= "Source port must be defined if destination port is also defined!<br />";
    }

    #########################################
    # Check for IP's in subnets
    #########################################
    if ( !($sipmac =~ /:/ or $sipmac eq 'N/A')) { # Skip IP and subnet validation if a MAC address or no entry
      if ($sipmac =~ /-/) {
        @singleip = split /\-/, $sipmac;
      } else {
        $singleip[0] = $sipmac;
        $singleip[1] = $sipmac;
      }

      unless ( ( &validipormask($singleip[0]) and &validipormask($singleip[1]) ) or &validmac($sipmac) ) {
         if ( $sipmac ne '' ) {
             $errormessage .= "$tr{'source ip bad'}<br />";
         } else {
             $cgiparams{'SRC_IPMAC'} = '0.0.0.0/0';
             $sipmac = '0.0.0.0/0';
         }
      }

      my $defaultipobj   = new NetAddr::IP "default";
      my $localhostipobj = new NetAddr::IP "localhost";
      my $greenipobj     = new NetAddr::IP "$netsettings{'GREEN_ADDRESS'}/$netsettings{'GREEN_NETMASK'}";
      my $greengwobj    = new NetAddr::IP "$netsettings{'GREEN_ADDRESS'}";
      my $redgwobj      = $defaultipobj;
      my $orangeipobj   = $defaultipobj;
      my $orangegwobj   = $defaultipobj;
      my $purpleipobj   = $defaultipobj;
      my $purplegwobj   = $defaultipobj;
      my $srcipaddrobj  = "";
      my $destipaddrobj = "";

      if ( $redip ne '' ) {
        $redgwobj = new NetAddr::IP "$redip";
      } else {
        $redgwobj = $defaultipobj;
      }

      if ( $netsettings{'ORANGE_ADDRESS'} ne '' ) {
        $orangeipobj = new NetAddr::IP
          "$netsettings{'ORANGE_ADDRESS'}/$netsettings{'ORANGE_NETMASK'}";
        $orangegwobj = new NetAddr::IP "$netsettings{'ORANGE_ADDRESS'}";
      }

      if ( $netsettings{'PURPLE_ADDRESS'} ne '' ) {
        $purpleipobj = new NetAddr::IP
          "$netsettings{'PURPLE_ADDRESS'}/$netsettings{'PURPLE_NETMASK'}";
        $purplegwobj = new NetAddr::IP "$netsettings{'PURPLE_ADDRESS'}";
      }

      if ( &validip($sipmac) ) {
        $srcipaddrobj = new NetAddr::IP "$sipmac";

        if ( $localhostipobj eq $srcipaddrobj ) {
            $errormessage .= "$tr{'source ip bad local'}<BR />";
        }

        if ( $greengwobj eq $srcipaddrobj ) {
            $errormessage .= "$tr{'source ip bad gateway'}<BR />";
        } elsif ( !( $srcipaddrobj eq "" ) ) {
            if (   ( $orangegwobj eq $srcipaddrobj )
                or ( $purplegwobj eq $srcipaddrobj )
                or ( $redgwobj eq $srcipaddrobj ) )
            {
                $errormessage .= "$tr{'source ip bad gateway'}<BR />";
            }
        }

        if ( !( $srcipaddrobj == $defaultipobj ) ) {
            if ( $cgiparams{'SRC_IFACE'} eq $netsettings{'GREEN_DEV'} ) {
                unless ( $settings{'GREEN'} eq "off" ) {
                    if ( !$greenipobj->contains($srcipaddrobj) ) {
                        $errormessage .= "$tr{'source ip bad green'}<BR />";
                    }
                }
            } elsif ( ( $netsettings{'ORANGE_ADDRESS'} ne '' )
                and ( $cgiparams{'SRC_IFACE'} eq $netsettings{'ORANGE_DEV'} ) )
            {
                unless ( $settings{'ORANGE'} eq "off" ) {
                    if ( !$orangeipobj->contains($srcipaddrobj) ) {
                        $errormessage .= "$tr{'source ip bad orange'}<BR />";
                    }
                }
            } elsif ( ( $netsettings{'PURPLE_ADDRESS'} ne '' )
                and ( $cgiparams{'SRC_IFACE'} eq $netsettings{'PURPLE_DEV'} ) )
            {
                unless ( $settings{'PURPLE'} eq "off" ) {
                    if ( !$purpleipobj->contains($srcipaddrobj) ) {
                        $errormessage .= "$tr{'source ip bad purple'}<BR />";
                    }
                }
            } elsif ( ( $redip ne '' )
                and ( $cgiparams{'SRC_IFACE'} eq $netsettings{'RED_DEV'} ) )
            {
                if (
                    ( $greenipobj->contains($srcipaddrobj) )
                    or ( ( !( $orangeipobj == $defaultipobj ) )
                        and $orangeipobj->contains($srcipaddrobj) )
                    or ( ( !( $purpleipobj == $defaultipobj ) )
                        and $purpleipobj->contains($srcipaddrobj) )
                   )
                {
                    $errormessage .= "$tr{'source ip bad red'}<BR />";
                }
            }
        }
      }

      if ($dipmac =~ /-/) {
        @singleip = split /\-/, $dipmac;
      } else {
        $singleip[0] = $dipmac;
        $singleip[1] = $dipmac;
      }

      unless ( (&validipormask($singleip[0]) and &validipormask($singleip[1])) or $dipmac eq '' ) {
        if ( $sipmac ne '' ) {
           $errormessage .= "$tr{'destination ip bad'}<br />";
        } else {
           $cgiparams{'DEST_IPMAC'} = '0.0.0.0/0';
           $dipmac = '0.0.0.0/0';
        }


        $destipaddrobj = new NetAddr::IP "$cgiparams{'DEST_IPMAC'}";

        if ( $localhostipobj eq $destipaddrobj ) {
            $errormessage .= "$tr{'destination ip bad local'}<BR />";
        }

        if ( $greengwobj eq $destipaddrobj ) {
            $errormessage .= "$tr{'destination ip bad gateway'}<BR />";
        } elsif ( !( $destipaddrobj eq "" ) ) {
            if (   ( $orangegwobj eq $destipaddrobj )
                or ( $purplegwobj eq $destipaddrobj )
                or ( $redgwobj eq $destipaddrobj ) )
            {
                $errormessage .= "$tr{'destination ip bad gateway'}<BR />";
            }
        }

        # This code added by Steve McNeill to generate error messages from subnet checks
        if ( !( $destipaddrobj == $defaultipobj ) ) {
            if ( $cgiparams{'DEST_IFACE'} eq $netsettings{'GREEN_DEV'} ) {
                unless ( $settings{'GREEN'} eq "off" ) {
                    if ( !$greenipobj->contains($destipaddrobj) ) {
                        $errormessage .= "$tr{'destination ip bad green'}<BR />";
                    }
                }
            } elsif ( ( $netsettings{'ORANGE_ADDRESS'} ne '' )
                and ( $cgiparams{'DEST_IFACE'} eq $netsettings{'ORANGE_DEV'} ) )
            {
                unless ( $settings{'ORANGE'} eq "off" ) {
                    if ( !$orangeipobj->contains($destipaddrobj) ) {
                        $errormessage .= "$tr{'destination ip bad orange'}<BR />";
                    }
                }
            } elsif ( ( $netsettings{'PURPLE_ADDRESS'} ne '' )
                and ( $cgiparams{'DEST_IFACE'} eq $netsettings{'PURPLE_DEV'} ) )
            {
                unless ( $settings{'PURPLE'} eq "off" ) {
                    if ( !$purpleipobj->contains($destipaddrobj) ) {
                        $errormessage .= "$tr{'destination ip bad purple'}<BR />";
                    }
                }
            } elsif ( ( $redip ne '' )
                and ( $cgiparams{'DEST_IFACE'} eq $netsettings{'RED_DEV'} ) )
            {
               if (( $greenipobj->contains($destipaddrobj) )
                    or ( ( !( $orangeipobj == $defaultipobj ) )
                        and $orangeipobj->contains($destipaddrobj) )
                    or ( ( !( $purpleipobj == $defaultipobj ) )
                        and $purpleipobj->contains($destipaddrobj) ))
               {
                    $errormessage .= "$tr{'destination ip bad red'}<br />";
               }
            }
        }
      }
    }

    open(FILE, "$filedir/portfw/aliases") or die 'Unable to open aliases file';
    my @aliases = <FILE>;
    close FILE;

    my $comment;
    if ($cgiparams{'SRC_IFACE'} =~ /:/) {
      foreach $line (@aliases) {
        chomp $line;
        @temp = split /,/, $line;
        if ($temp[1] eq $cgiparams{'SRC_IFACE'} and $temp[9] ne '') { # Server IP address mapped to a secondary red IP
          $comment .= "$cgiparams{'DESCRIPTION'} " . " Secondary IP mapped to $temp[9]";
        } else { # Secondary red IP address but no LAN address mapped to it
          $comment = $cgiparams{'DESCRIPTION'};
        }
      }
    } else { # Primary red IP address
      $comment = $cgiparams{'DESCRIPTION'};
    }

      # Following section contributed by Neal Murphy. Thanks fest3er!
    unless ($errormessage) {
      # Whether adding or updating,
      #   1. Read config file into assoc. array
      #   2. Multiplying the order #s by 10 to give room for the new or moved one
      #   3. Add the new/moved one using index ((10 * ORDER_NUMBER) - 1)
      #   4. If moved, undef index 10 * OLDID
      #   5. Then sort the keys and write the entries with new order numbers.
      # Order numbers will now always be sequential from 1 to n, without gaps.
      # Boundary conditions are much less problematic.

      if (($cgiparams{'ACTION'} eq $tr{'ffc-update'}) or
          ($cgiparams{'ACTION'} eq $tr{'add'})) {
        my $cnt = 0;
        my $notadded = 1;
        my (%current, $line, $idx, $oldIdx, $newIdx, @temp, @time, $timeon, $timechk);

        # Read the file into assoc. array 'current', indexed by 10x the file's order numbers.
        open(FILE, "$filename") or die 'Unable to read config file.';
        while (<FILE>) {
          my @splt;
          chomp;
          @splt = split /,/, $_;
          $current{10*$splt[0]} = $_;
        }
        close(FILE);

        if ($cgiparams{'ORDER_NUMBER'} != $cgiparams{'OLDID'}) {
          # If an addition or update and the entry's order number changed, change its index and delete
          #   (undef) the original.

          # Prepare an empty entry; it'll be filled in a bit
          $newIdx = (10 * $cgiparams{'ORDER_NUMBER'}) - 1;
          $current{$newIdx} = "";
          # delete the old location only when moving an existing entry
          #   (ObviousMan: "Clearly, new entries don't have corresponding old entries."
          if ($cgiparams{'OLDID'} != 0) {
            my $oldIdx = (10 * $cgiparams{'OLDID'});
            undef $current{$oldIdx};
          }
        } else {
          # Same order, but we need $newIdx anyway.
          $newIdx = 10 * $cgiparams{'ORDER_NUMBER'};
        }

        # Now sort the keys and re-write the file in the correct order.

        open(FILE, ">$filename") or die 'Unable to open config file.';
          flock FILE, 2;

          # Rewrite the file, renumbering the rules from 1 to n, by 1.
          foreach $idx (sort numerically keys %current) { 
            next if (!defined $current{$idx});
            $cnt++;

            # Print the entry with its new order #
            if ($idx == $newIdx) {
              #$infomessage .= "New/Chg'd entry: $idx==$newIdx<br />\n";
              # Use cgiparms for new/updated/moved entry

              # Time frame to handle?
              if ($cgiparams{'TIMES'}) {
                $timeon = 'on';
                $timechk = "+$cgiparams{'TIMES'}";
              } else {
                $timeon = "off";
                $timechk = "";
              }
              # Shovel it out
              {
                my $outLine = "";
                $outLine .= "$cnt,$cgiparams{'SRC_IFACE'},";
                $outLine .= "$cgiparams{'SRC_IPMAC'},$service,";
                $outLine .= "$cgiparams{'DEST_IFACE'},$cgiparams{'DEST_IPMAC'},";
                $outLine .= "$cgiparams{'NEW_DEST_PORT'},$protocol,";
                $outLine .= "$cgiparams{'TARGET'},$cgiparams{'ENABLED'},";
                $outLine .= "$timeon,$setproxy,$comment,$timechk";
                print FILE "$outLine\n";
              }

            } else {

              # Get the untouched entry and fission it
              my @temp = split /,/, $current{$idx};
              my @times = split /\+/, $current{$idx};

              # Time frame to handle?
              if ($times[1]) {
                $timeon = 'on';
                $timechk = "+$times[1]";
              } else {
                $timeon = 'off';
                $timechk = "";
              }
              # Shovel it out
              {
                my $outLine = "";
                $outLine  = "$cnt,$temp[1],$temp[2],$temp[3],$temp[4],$temp[5],";
                $outLine .= "$temp[6],$temp[7],$temp[8],$temp[9],$timeon,$temp[11],$temp[12],$timechk";
                print FILE "$outLine\n";
              }
            }
          }
          close(FILE);
      }


      &writehash("$hashfile", \%cgiparams);
      if ($cgiparams{'ACTION'} eq $tr{'add'}) {
        &log($tr{'ffc-forwarding rule added'});
      } else {
        &log($tr{'ffc-forwarding rule updated'});
      }
      $success = message('setportfw');

      unless ( $success eq 'Port forwarding rules set' ) {
        $errormessage .= "Error setting portforwarding rules: " . "$success" . "<br />\n";

        open( FILE, "$filename" ) or die 'Unable to open config file.';
        @current = <FILE>;
        close FILE;

        $cnt = 1;
        open( FILE, ">$filename" ) or die 'Unable to open config file.';
        flock FILE, 2;

        # Remove the offending line from the config file so it doesn't get
        #  listed in the UI display table
        foreach $line (@current) {
          chomp $line;
          @temp = split /,/, $line;
          @times = split /\+/, $line;

          # Time frame to handle?
          if ($times[1]) {
            $timeon = 'on';
            $timechk = "+$times[1]";
          } else {
            $timeon = 'off';
            $timechk = "";
          }

          if ( $temp[0] != $cgiparams{'ORDER_NUMBER'} ) {
            my $outLine = "";
            $outLine  = "$cnt,$temp[1],$temp[2],$temp[3],$temp[4],$temp[5],";
            $outLine .= "$temp[6],$temp[7],$temp[8],$temp[9],$timeon,";
            $outline .= "$temp[11],$temp[12],$timechk";
            print FILE "$outLine\n";
          }
          $cnt++;
         }
         close FILE;
      }
    }

    $cgiparams{'ORDER_NUMBER'} = "0";
    open( FILE, "$filename" ) or die 'Unable to open config file';
    while (<FILE>) {
        $cgiparams{'ORDER_NUMBER'}++;
    }
    close FILE;

    ############################################################################
    # Let's reset some variables used from the last POST action so they don't 
    #    cause problems later with the default UI page values
    #
    # $cgiparams{'ORDER_NUMBER'} is incremented so the next order
    #    number to be used for adding a new rule appears in the UI
    #
    # $cgiparams{'OLDID'} is a "flag" set from the POST ACTION of Edit
    #    to indicate that when the "working data" from the UI is POSTed with the
    #    Update button it will overwrite the rule being edited. When OLDID = 0
    #    then the "working data" from the UI is for creating a new rule
    #
    # $cgiparams{'TIMES'} is a hidden value containing the timed data created by 
    #    the timed access script that appears in the config file that is carried
    #    over from a POST ACTION of Edit when editing a rule with timed values
    #
    # The rest of the values being reset below are "working data" (not POST data)
    #     from the UI that will generate some default values to appear in the UI

    $cgiparams{'ORDER_NUMBER'}++;
    $cgiparams{'SRC_IPMAC'}     = '';
    $cgiparams{'DEST_IPMAC'}    = '';
    $cgiparams{'SRC_IFACE'}     = $netsettings{'RED_DEV'};
    $cgiparams{'DEST_IFACE'}    = $netsettings{'GREEN_DEV'};
    $cgiparams{'SERVICE'}       = 'user';
    $cgiparams{'DEST_PORT'}     = '';
    $cgiparams{'NEW_DEST_PORT'} = '';
    $cgiparams{'PROTOCOL'}      = '6';
    $cgiparams{'TARGET'}        = 'ACCEPT';
    $cgiparams{'ENABLED'}       = 'on';
    $cgiparams{'DESCRIPTION'}   = '';
    $cgiparams{'TIMED'}         = 'off';
    $cgiparams{'TIMES'}         = '';
    $cgiparams{'OLDID'}         = 0;
}

# Check for remove or edit
elsif ($cgiparams{'ACTION'} eq $tr{'remove'}
    or $cgiparams{'ACTION'} eq $tr{'edit'}
    or $cgiparams{'ACTION'} eq $tr{'ffc-enable rule'} )
{
    open( FILE, "$filename" ) or die 'Unable to open config file.';
    my @current = <FILE>;
    close(FILE);

    my $count = 0;
    my $id    = 0;
    my $line;

    foreach $line (@current) {
        $id++;

        if ( $cgiparams{$id} eq "on" ) {
            $count++;
        }
    }

    if ( $count == 0 ) {
        $errormessage .= "$tr{'nothing selected'}<br \>";
    }

    if ( $count > 1 and $cgiparams{'ACTION'} eq $tr{'edit'} ) {
        $errormessage .= "$tr{'you can only select one item to edit'}<br \>";
    }

    unless ($errormessage) {
        open( FILE, ">$filename" ) or die 'Unable to open config file.';
        flock FILE, 2;
        $id  = 0;
        $cnt = 1;
        $cgiparams{'ORDER_NUMBER'} = 1; # Start at "1" since we will display the next rule
                                        # order number to be created in the UI which is 1 
                                        # more than the actual rule count

        foreach $line (@current) {
            $id++;

            unless ( $cgiparams{$id} eq "on" ) {
                chomp $line;
                @temp = split /,/, $line;
                @times = split /\+/, $line;

                # Time frame to handle?
                if ($times[1]) {
                  $timeon = 'on';
                  $timechk = "+$times[1]";
                } else {
                  $timeon = 'off';
                  $timechk = "";
                }
                my $outLine = "";
                $outLine  = "$cnt,$temp[1],$temp[2],$temp[3],$temp[4],$temp[5],";
                $outLine .= "$temp[6],$temp[7],$temp[8],$temp[9],$timeon,$temp[11],$temp[12],$timechk";
                print FILE "$outLine\n";
                $cnt++;
                $cgiparams{'ORDER_NUMBER'}++;
            } elsif ( $cgiparams{'ACTION'} eq $tr{'edit'} ) {
                chomp($line);
                @temp = split /,/, $line;
                @times = split /\+/, $line;
                $cgiparams{'ORDER_NUMBER'}  = $temp[0];
                $cgiparams{'SRC_IFACE'}     = $temp[1];
                $cgiparams{'SRC_IPMAC'}     = $temp[2];

                # Replace "-" with "," to display multiports as comma separated values
                if ($temp[3] =~ /-/) {
                  $temp[3] =~ s/-/,/g;
                }
                $service                    = $temp[3];
                $cgiparams{'DEST_IFACE'}    = $temp[4];
                $cgiparams{'DEST_IPMAC'}    = $temp[5];
                $cgiparams{'NEW_DEST_PORT'} = $temp[6];
                $cgiparams{'PROTOCOL'}      = $temp[7];
                $cgiparams{'TARGET'}        = $temp[8];
                $cgiparams{'ENABLED'}       = $temp[9];
                $cgiparams{'TIMED'}         = $temp[10];
                $setproxy                   = $temp[11];
                $cgiparams{'DESCRIPTION'}   = $temp[12];
                $cgiparams{'TIMES'}         = $times[1];

                # Editing support
                $cgiparams{'OLDID'} = $id;
                $updatebutton = 1;
                print FILE "$line\n";
                $cnt++;
            } elsif ( $cgiparams{'ACTION'} eq $tr{'ffc-enable rule'} ) {
                chomp $line;
                my @temp = split( /\,/, $line );
                @times = split /\+/, $line;

                # Time frame to handle?
                if ($times[1]) {
                  $timeon = 'on';
                  $timechk = "+$times[1]";
                } else {
                  $timeon = 'off';
                  $timechk = "";
                }
                $temp[0] = $cnt++;
                if ( $temp[9] eq "on" ) {
                    $enabled = "off";
			$setproxy = "off";
                } else {
                    $enabled = "on";
			$setproxy = "on";
                }
                print FILE "$temp[0],$temp[1],$temp[2],$temp[3],";
                print FILE "$temp[4],$temp[5],$temp[6],$temp[7],";
                print FILE "$temp[8],$enabled,$timeon,$setproxy,$temp[12],$timechk\n";
                $cgiparams{'ORDER_NUMBER'}++;
                &log($tr{'ffc-forwarding rule disabled'});
            }
        }

        close FILE;

        ########################################################################################
        # If a rule or rules were selected for removal, no action would have been taken
        # in the routines above and the rules to be removed were not printed back to the
        # portfw/config file and have been effectively removed from the iptables rules.
        # So now we need to reset the UI to some default values.

        if ( $cgiparams{'ACTION'} eq $tr{'remove'} ) {
           $cgiparams{'SRC_IPMAC'}     = '';
           $cgiparams{'DEST_IPMAC'}    = '';
           $cgiparams{'SRC_IFACE'}     = $netsettings{'RED_DEV'};
           $cgiparams{'DEST_IFACE'}    = $netsettings{'GREEN_DEV'};
           $cgiparams{'DEST_PORT'}     = '';
           $cgiparams{'NEW_DEST_PORT'} = '';
           $cgiparams{'PROTOCOL'}      = '6';
           $cgiparams{'TARGET'}        = 'ACCEPT';
           $cgiparams{'ENABLED'}       = 'on';
           $cgiparams{'DESCRIPTION'}   = '';

           # Implied "Don't print the removed rule"
           &log( $tr{'ffc-forwarding rule removed'} );
        }
        unless ( $cgiparams{'ACTION'} eq $tr{'edit'} ) {
           my $success = message('setportfw');

           unless ( $success eq 'Port forwarding rules set' ) {
              $errormessage .= "Error setting portforwarding rules: $success<br \>";
           }
       }
    }
}

# Check for errormessage
if ( $errormessage ne '' ) {

    # Reset defaults for ip's/ports
    if ( $cgiparams{'SRC_IPMAC'} eq '0.0.0.0/0' ) {
        $cgiparams{'SRC_IPMAC'} = '';
    }

    if ( $cgiparams{'DEST_IPMAC'} eq '0.0.0.0/0' ) {
        $cgiparams{'DEST_IPMAC'} = '';
    }

    if ( $cgiparams{'DEST_PORT'} eq '0' ) {
        $cgiparams{'DEST_PORT'} = '';
    }

    if ( $cgiparams{'NEW_DEST_PORT'} eq '0' ) {
        $cgiparams{'NEW_DEST_PORT'} = '';
    }
}

# Get a rule count to display the next default order # in the UI display
open( FILE, "$filename" ) or die 'Unable to open config file.';
while (<FILE>) { $cgiparams{'RULE_COUNT'}++; }
close(FILE);
$cgiparams{'RULE_COUNT'}++;

# Check for normal page load with default UI page values
if ( $cgiparams{'ACTION'} eq '' ) {
    $cgiparams{'PROTOCOL'}        = '6';
    $cgiparams{'ENABLED'}         = 'on';
    $cgiparams{'ADDRESS_ENABLED'} = 'on';

    # Support for outbound firewall
    $cgiparams{'SRC_IFACE'}    = $netsettings{'RED_DEV'};
    $cgiparams{'DEST_IFACE'}   = $netsettings{'GREEN_DEV'};
    $cgiparams{'TARGET'}       = 'ACCEPT';
    $cgiparams{'ORDER_NUMBER'} = $cgiparams{'RULE_COUNT'};
    $cgiparams{'DESCRIPTION'}  = '';
    $cgiparams{'TIMED'}        = 'off';
    $cgiparams{'TIMES'}        = '';
}

# Determine the RED device to display in the UI
if ($netsettings{'RED_DEV'} eq "") {
  $netsettings{'RED_DEV'} = `cat /var/smoothwall/red/iface`;
  chomp $netsettings{'RED_DEV'};
}

# Go through all the IFs (zones)
foreach (keys %netsettings) {
  next if ($_ !~ /.*_DEV/);         #skip if value is not a net device
  next if ($netsettings{$_} eq ""); #skip if the zone doesn't exist

  $currIF = $netsettings{$_};

  # Set/clear
  my $primaryIdx = 0;
  my @primaries = ();
  my $thisIF = ();  # an empty array

  # Get all the IPv4 addrs for that IF
  open(ipAddr, "/usr/sbin/ip addr show dev $currIF|");
  while (<ipAddr>) {
    chomp;
    @inet4 = split;

    # We only care about IPv4 addrs
    next if ($inet4[0] ne "inet");

    # Convert the host address to a LAN (subnet) address
    $ipconv = new Net::Netmask($inet4[1]);
    $netAddr = $ipconv->base();
    # Add this netAddr if we haven't seen it before. This is used to
    # retain the display/assignment order and to group addresses
    # together.
    if (not defined ($thisIF{$netAddr})) {
      $primaries[$primaryIdx++] = $netAddr;
    }

    # append the host address to the list for that subnet
    @addrParts = split(/\//,$inet4[1]);
    $thisIF{$netAddr} .= "$addrParts[0],";
  }
  # Done with this 'ip addr' command
  close (ipAddr);

  # Now display the data in the proper order (not the random-ish
  # hash order). The first address put out for an IF will be the
  # first one assigned to it.
  $ifIDX = 0;
  for ($primaryIdx=0; $primaryIdx<@primaries; $primaryIdx++) {
    # Fetch the net address
    $netAddr = $primaries[$primaryIdx];
    # Fetch the list of addresses for that net
    $IFlist = $thisIF{$netAddr};
    $IFlist =~ s/,$//;

    # And display them (or assign them to a hash)
    @addrs = split (/,/, $IFlist);
    for ($idx=0; $idx<@addrs; $idx++) {
      if ($ifIDX == 0) {
        $availablenetdevices{$currIF} = $addrs[$idx];
      } else {
        $availablenetdevices{"$currIF:$ifIDX"} = $addrs[$idx];
      }
      $ifIDX++;
    }
  }
}

# Support for outbound firewall
$selected{'SRC_IFACE'}{''}  = '';
$selected{'DEST_IFACE'}{''} = '';

foreach $dev ( sort( keys(%availablenetdevices) ) ) {
    $selected{'SRC_IFACE'}{$dev}  = '';
    $selected{'DEST_IFACE'}{$dev} = '';
}

$selected{'SRC_IFACE'}{$cgiparams{'SRC_IFACE'}}    = 'selected';
$selected{'DEST_IFACE'}{$cgiparams{'DEST_IFACE'}}  = 'selected';
$selected{'SERVICE'}{$cgiparams{'SERVICE'}}        = 'selected';
$selected{'PROTOCOL'}{ $cgiparams{'PROTOCOL'} }    = 'selected';

$selected{'IF_ALIAS'}{'RED'}   = '';
$selected{'IF_ALIAS'}{'GREEN'} = '';
if ( $cgiparams{'ORANGE_DEV'} ) {
    $selected{'IF_ALIAS'}{'ORANGE'} = '';
}
if ( $cgiparams{'PURPLE_DEV'} ) {
    $selected{'IF_ALIAS'}{'PURPLE'} = '';
}
$selected{'IF_ALIAS'}{ $cgiparams{'IF_ALIAS'} } = 'selected';

$selected{'TARGET'}{'ACCEPT'}               = '';
$selected{'TARGET'}{'DROP'}                 = '';
$selected{'TARGET'}{'REJECT'}               = '';
$selected{'TARGET'}{'LOG'}                  = '';
$selected{'TARGET'}{ $cgiparams{'TARGET'} } = 'selected';

$checked{'ENABLED'}{'off'}                   = '';
$checked{'ENABLED'}{'on'}                    = '';
$checked{'ENABLED'}{ $cgiparams{'ENABLED'} } = 'checked';

# Protocol listing
open( TMP, "/etc/protocols" ) or die "Unable to open /etc/protocols\: $!\n";
my @protocols = <TMP>;
close(TMP);

my %availableprotocols;
open( FILE, ">$filedir/portfw/protolist" )
  or die 'Unable to write protocol list file';
foreach $line (@protocols) {
    chomp $line;

    if ( $line =~ m/^([a-z0-9]|\#\t[0-9]+\t+)/i ) {
        my @protoline = split( /\s+/, $line );
        print FILE "$protoline[1],$protoline[2]\n";
        if ( $#protoline == 3 ) {
            $protoline[3] =~ s/\b(\w)/\u\L$1/g;
            $availableprotocols{ $protoline[1] } =
              "$protoline[2] = $protoline[3]";
        } else {
            $protoline[2] =~ s/\b(\w)/\u\L$1/g;
            $availableprotocols{ $protoline[1] } = "$protoline[2]";
        }
    }
}
close FILE;

delete( $availableprotocols{'0'} );
delete( $availableprotocols{'41'} );
delete( $availableprotocols{'43'} );
delete( $availableprotocols{'44'} );
delete( $availableprotocols{'58'} );
delete( $availableprotocols{'59'} );
delete( $availableprotocols{'60'} );
delete( $availableprotocols{'253'} );
delete( $availableprotocols{'254'} );
delete( $availableprotocols{'255'} );
my @sortedprotocols = sort { $a <=> $b } keys(%availableprotocols);

&openpage( $tr{'full firewall control'}, 1, '', 'Full Firewall Control' );

&openbigbox( '100%', 'LEFT' );

&alertbox($errormessage);

# Javascript support lines
print
"<script type='application/javascript' SRC='/mods/fullfirewall/ui/js/utility.js'></script>";

print <<END
<script>
function ffoxSelectUpdate(elmt)
{
    if(!document.all) elmt.style.cssText = elmt.options[elmt.selectedIndex].style.cssText;
}
</script>
END
  ;

# Border for debug
my $border = 0;

######################################################################
# Mod for source ip, destination ip, and destination port edit display
######################################################################
if ( $cgiparams{'SRC_IPMAC'} eq '0.0.0.0/0' ) {
    $sourceipmac = '';
} else {
    $sourceipmac = $cgiparams{'SRC_IPMAC'};
}

if ( $cgiparams{'DEST_IPMAC'} eq '0.0.0.0/0' ) {
    $destinationipmac = '';
} else {
    $destinationipmac = $cgiparams{'DEST_IPMAC'};
}

if ( $cgiparams{'DEST_PORT'} eq '0' ) {
    $sourceport = '';
} else {
    $sourceport = $cgiparams{'DEST_PORT'};
}

if ( $cgiparams{'NEW_DEST_PORT'} eq '0' ) {
    $destinationport = '';
} else {
    $destinationport = $cgiparams{'NEW_DEST_PORT'};
}

if ($updatebutton) {
    $buttontext = $tr{'ffc-update'};
    $boxtext    = $tr{'update current rule'};
} else {
    $buttontext = $tr{'add'};
    $boxtext    = $tr{'add a new rule'};
}

print <<END
<style type="text/css">
option.red{color:red;}
option.green{color:green;}
option.orange{color:orange;}
option.purple{color:purple;}
</style>
END
;

##############################################

print "<form method='post'>\n";

# Check for running interfaces
open( FILE, "$aliasfile" ) or die 'Unable to open config file.';
my @aliases = <FILE>;
close FILE;

open( FILE, ">$aliasfile" ) or die 'Unable to open config file.';
foreach $line (@aliases) {
    chomp $line;
    @temp = split( /\,/, $line );
    my $alias = $temp[1];
    my $running;
    my @ip_addr = `ip addr show $alias`;
    foreach my $line2 (@ip_addr) {
        if ( ($line2 =~ /eth/ or $line2 =~ /ppp/) and $line2 =~ /UP/ ) {
            $running = "on";
            last;
        } else {
            $running = "off";
        }
    }
    print FILE "$temp[0],$temp[1],$temp[2],$temp[3],$temp[4],$temp[5],$running,$temp[7],$temp[8],$temp[9]\n";
}
close FILE;

&openbox($boxtext);

# Extract the initial iface color for SRC
my $SRC_COLOR = 'black';
$SRC_COLOR = 'green'
  if ( $selected{'SRC_IFACE'}{ $netsettings{'GREEN_DEV'} } eq 'selected' );

$SRC_COLOR = 'orange'
  if ( $selected{'SRC_IFACE'}{ $netsettings{'ORANGE_DEV'} } eq 'selected' );

$SRC_COLOR = 'purple'
  if ( $selected{'SRC_IFACE'}{ $netsettings{'PURPLE_DEV'} } eq 'selected' );

$SRC_COLOR = 'red'
  if ( $selected{'SRC_IFACE'}{$netsettings{'RED_DEV'}} eq 'selected' );

# Extract the initial iface color for DEST
my $DEST_COLOR = 'black';
$DEST_COLOR = 'green'
  if ( $selected{'DEST_IFACE'}{ $netsettings{'GREEN_DEV'} } eq 'selected' );

$DEST_COLOR = 'orange'
  if ( $selected{'DEST_IFACE'}{ $netsettings{'ORANGE_DEV'} } eq 'selected' );

$DEST_COLOR = 'purple'
  if ( $selected{'DEST_IFACE'}{ $netsettings{'PURPLE_DEV'} } eq 'selected' );

$DEST_COLOR = 'red'
  if ( $selected{'DEST_IFACE'}{$netsettings{'RED_DEV'}} eq 'selected' );

print qq!
<table style='width:100%;' style='margin:6pt 0'>
   <tr>
     <td class='base'>$tr{'source ifacec'}</td>
     <td><select style='color: $SRC_COLOR' onchange='ffoxSelectUpdate(this);' name='SRC_IFACE' title="Select RED for incoming rules. Any other color for outgoing or internal rules.">
!;

my @temp3;
open( FILE, "$aliasfile" ) or die 'Unable to open config file.';
@temp3 = <FILE>;
close FILE;

foreach $dev ( sort( keys(%availablenetdevices) ) ) {
    $dev =~ /(\:\d{1,3})/;
    my $devifacesub = $1;
    my $redaliasip;

    foreach $line (@temp3) {
        chomp $line;
        @split = split( /\,/, $line );
        if ( $split[0] eq "RED$devifacesub" and $dev =~ /:/ ) {
            $redaliasip = $split[3];
        }
    }

    if ( $netsettings{'GREEN_DEV'} and ( $dev =~ /$netsettings{'GREEN_DEV'}/ ) )
    {
        print "<option style='color: green' value='$dev' $selected{'SRC_IFACE'}{$dev}>GREEN$devifacesub - $dev</option>";
    } elsif ( $netsettings{'ORANGE_DEV'}
        and ( $dev =~ /$netsettings{'ORANGE_DEV'}/ ) )
    {
        print "<option style='color: orange' value='$dev' $selected{'SRC_IFACE'}{$dev}>ORANGE$devifacesub - $dev</option>";
    } elsif ( $netsettings{'PURPLE_DEV'}
        and ( $dev =~ /$netsettings{'PURPLE_DEV'}/ ) )
    {
        print "<option style='color: purple' value='$dev' $selected{'SRC_IFACE'}{$dev}>PURPLE$devifacesub - $dev</option>";
    } elsif ( $netsettings{'RED_DEV'} ) {
        print "<option style='color: red' value='$dev' $selected{'SRC_IFACE'}{$dev}>\n";
        if ($redaliasip) {
            print "RED$devifacesub $redaliasip\n";
        } else {
            print "RED$devifacesub - $dev\n";
        }
        print "</option>\n";
    } else {
        print "<option style='color: black' value='$dev' $selected{'SRC_IFACE'}{$dev}>$dev</option>";
    }
}

print qq!
		</select></td>
	<td class='base'>$tr{'new destination ifacec'}</td>
       <td><select style='color: $DEST_COLOR' onchange="ffoxSelectUpdate(this);" name='DEST_IFACE' title="Select RED for outgoing rules. Any other color for incoming or internal rules">
!;

foreach $dev ( sort( keys(%availablenetdevices) ) ) {
    if ( $dev =~ /(\:\d{1,3})/ ) {
        next;
    }
    if ( $netsettings{'GREEN_DEV'} and ( $dev =~ /$netsettings{'GREEN_DEV'}/ ) )
    {
        print "<option style='color: green' value='$dev' $selected{'DEST_IFACE'}{$dev}>GREEN - $dev</option>";
    } elsif ( $netsettings{'ORANGE_DEV'}
        and ( $dev =~ /$netsettings{'ORANGE_DEV'}/ ) )
    {
        print "<option style='color: orange' value='$dev' $selected{'DEST_IFACE'}{$dev}>ORANGE - $dev</option>";
    } elsif ( $netsettings{'PURPLE_DEV'}
        and ( $dev =~ /$netsettings{'PURPLE_DEV'}/ ) )
    {
        print "<option style='color: purple' value='$dev' $selected{'DEST_IFACE'}{$dev}>PURPLE - $dev</option>";
    } elsif ( $netsettings{'RED_DEV'} ) {
        print "<option style='color: red' value='$dev' $selected{'DEST_IFACE'}{$dev}>RED - $dev</option>";
        if ($redaliasip) {
            print "RED$devifacesub $redaliasip\n";
        } else {
            print "RED$devifacesub - $dev\n";
        }
        print "</option>\n";
    } else {
        print "<option style='color: black' value='$dev' $selected{'DEST_IFACE'}{$dev}>$dev</option>";
    }
}

print <<END
	</select></td>

</tr>
<tr>
	<td class='base' nowrap='nowrap'><img src='/ui/img/blob.gif' valign='top'>$tr{'source ippfc'}</td>
	<td><input type='text' name='SRC_IPMAC' value='$sourceipmac' size='18' title="External IPs if RED interface selected above. IPs in same subnet if LAN interface. Single IP, range or network."></td>
	<td class='base' nowrap='nowrap'><img src='/ui/img/blob.gif' valign='top'>$tr{'new destination ippfc'}</td>
	<td><input type='text' name='DEST_IPMAC' value='$destinationipmac' size='18' title="External IPs if RED interface selected above. IPs in same subnet if LAN interface. If LAN interface selected above, single IP only."></td>
</tr>
</table>
<table width='100%'>
<tr>
       @{[&portlist('SERVICE', $tr{'ffc-application servicec'}, 'DEST_PORT', $tr{'ffc-original destination portc'}, $service)]}
</tr>
<tr>
       <td class='base'>&nbsp;</td><td>&nbsp;</td>
	<td class='base' nowrap='nowrap'><img src='/ui/img/blob.gif' valign='top'><img src='/ui/img/blob.gif' valign='top'>$tr{'new destination portc'}</td>
	<td><input type='text' name='NEW_DEST_PORT' value='$destinationport' size='11' id='new_dest_port' @{[jsvalidport('new_dest_port')]} title='Used to forward the original destination port to a new destination port. Leave blank if not needed.'></td>

</tr>
</table>
<table style='width:100%;' style='margin:6pt 0'>
<tr>
			<td class='base' width='16%'>$tr{'protocol long'}</td>
			<td width='17%'><select name='PROTOCOL'>
END
  ;
if ( $cgiparams{'PROTOCOL'} eq 'all' ) {
    print "<option value='all' selected>All</option>";
} else {
    print "<option value='all'>All</option>";
}

if ( $cgiparams{'PROTOCOL'} eq '6' ) {
    print "<option value='6' selected>$availableprotocols{6}</option>";
} else {
    print "<option value='6'>$availableprotocols{6}</option>";
}

if ( $cgiparams{'PROTOCOL'} eq '17' ) {
    print "<option value='17' selected>$availableprotocols{17}</option>";
} else {
    print "<option value='17'>$availableprotocols{17}</option>";
}

if ( $cgiparams{'PROTOCOL'} eq 'TCP&UDP' ) {
    print "<option value='TCP&UDP' selected>TCP & UDP</option>";
} else {
    print "<option value='TCP&UDP'>TCP & UDP</option>";
}

if ( $cgiparams{'PROTOCOL'} eq '1' ) {
    print "<option value='1' selected>$availableprotocols{1}</option>";
} else {
    print "<option value='1'>$availableprotocols{1}</option>";
}

print <<END
	</select></td>
	<td class='base' width='16%'>$tr{'ffc-target'}</td>
		<td width='17%'><select name='TARGET'>
			<option value='ACCEPT' $selected{'TARGET'}{'ACCEPT'}>$tr{'target accept'}</option>
			<option value='REJECT' $selected{'TARGET'}{'REJECT'}>$tr{'target reject'}</option>
			<option value='DROP' $selected{'TARGET'}{'DROP'}>$tr{'target drop'}</option>
			<option value='LOG' $selected{'TARGET'}{'LOG'}>$tr{'target log'}</option>
			<option value='LOG&ACCEPT' $selected{'TARGET'}{'LOG&ACCEPT'}>LOG & ACCEPT</option>
			<option value='LOG&REJECT' $selected{'TARGET'}{'LOG&REJECT'}>LOG & REJECT</option>
			<option value='LOG&DROP' $selected{'TARGET'}{'LOG&DROP'}>LOG & DROP</option>
		</select></td>
		<td class='base' width='17%'>$tr{'order number'}</td>
		<td width='17%'><select name='ORDER_NUMBER'>
END
  ;

for ( $cnt = 1 ; $cnt < $cgiparams{'RULE_COUNT'} + 1 ; $cnt++ ) {
    if ( $cnt eq $cgiparams{'ORDER_NUMBER'} ) {
        print "<option value='$cnt' selected>$cnt</option>";
    } else {
        print "<option value='$cnt'>$cnt</option>";
    }
}

print <<END
		</select></td>
	</tr>
</table>
<table width='60%'>
	<tr>
		<td class='base' nowrap='nowrap'>$tr{'descriptionc'}</td> 
              <td><input type='text' name='DESCRIPTION' size='80' value='$cgiparams{'DESCRIPTION'}' id='description' @{[jsvalidcomment('description')]}></td>
	</tr>
</table>

<table style='width:100%; margin:6pt 0' border='$border'>
        <tr>
          <td style='width:50%; text-align:center'>
            $tr{'enabled'}
            <input type='checkbox' name='ENABLED' $checked{'ENABLED'}{'on'}>
          </td>
          <td style='width:50%; text-align:center'>
            <input type='submit' name='ACTION' value='$buttontext' onclick='return validate();'>
            <input type='hidden' name='OLDID' value='$cgiparams{'OLDID'}'>
            <input type='hidden' name='TIMED' value='$cgiparams{'TIMED'}'>
 	     <input type='hidden' name='TIMES' value='$cgiparams{'TIMES'}'>
	   </td>
	
	</tr>
</table>
<table width='100%'>
	<tr>
            <td align='left'><img src='/ui/img/blob.gif' valign='top'>&nbsp;$tr{'portfw source destination ip'}</td>
	</tr>
	<tr>
            <td align='left'><img src='/ui/img/blob.gif' valign='top'><img src='/ui/img/blob.gif' valign='top'>&nbsp;$tr{'portfw destination port'}</td>
	</tr>
</table>

<SCRIPT LANGUAGE='JavaScript' TYPE='text/javascript'>
<!--
	// validate function
	function validate() {
		// Vars
		var errorMessage = "";

		// Get form
		var form = document.forms['FIREWALL'];

		// Setup fields
		form.DESCRIPTION.humanname = 'Description';
		form.DESCRIPTION.checkspecialchars = true;
		form.DESCRIPTION.specialChars = /(,)/;

		// Check for errormessage
		if (errorMessage != '') {
			// Alert and return false
			alert("The following errors have occured:" + errorMessage);
			return false;
		}

		// Check for source and destination both being blank, warn if so
		if ((form.SRC_IPMAC.value == '') and (form.DEST_IPMAC.value == '')) {
			// Confirm you really want to do this
			if (!confirm("Are you sure you want to " + form.TARGET.options[form.TARGET.selectedIndex].text + " " + form.PROTOCOL.options[form.PROTOCOL.selectedIndex].text + " traffic from " + form.SRC_IFACE.options[form.SRC_IFACE.selectedIndex].text + " to " + form.DEST_IFACE.options[form.DEST_IFACE.selectedIndex].text + "?")) {
				// Return false if not wanted
				return false;
			}
		}

		// Check form
		if (checkForm(form)) {
			// Return true
			return true;
		}

		// Return false
		return false;
	}
-->
</SCRIPT>
END
  ;
&closebox();

&openbox( $tr{'current rules'} );

my $portmap     = portmap();
my $protocolmap = Stans::modlib::protocolmap();
my $ifcolorsmap = Stans::modlib::ifcolormap();

my %render_settings = (
    'url' =>
"/mods/fullfirewall/cgi-bin/portfw.cgi?[%COL%],[%ORD%],$cgiparams{'COLUMN'},$cgiparams{'ORDER'}",
    'columns' => [
        {
            column => '1',
            title  => 'Order',
            size   => 10,
            sort   => '<=>',
        },
        {
            column => '2',
            title  => 'Src Dev',
            size   => 15,
            sort   => 'cmp',
            tr     => \%{$ifcolorsmap},
        },
        {
            column => '3',
            title  => 'Source IP/MAC',
            size   => 15,
            sort   => 'cmp',
            tr     => { '0.0.0.0/0' => 'All' },
        },
        {
            column => '4',
            title  => 'Dest Port',
            size   => 10,
            sort   => 'cmp',
            tr     => \%{$portmap},
        },
        {
            column => '5',
            title  => 'Dest Dev',
            size   => 15,
            sort   => 'cmp',
            tr     => \%{$ifcolorsmap},
        },
        {
            column => '6',
            title  => 'Destination IP',
            size   => 15,
            sort   => 'cmp',
            tr     => { '0.0.0.0/0' => 'All' },
        },
        {
            column => '7',
            title  => 'New Dest Port',
            size   => 10,
            sort   => 'cmp',
            tr     => \%{$portmap},
        },
        {
            column => '8',
            title  => 'Protocol',
            size   => 10,
            sort   => 'cmp',
            tr     => \%{$protocolmap},
        },
        {
            column => '9',
            title  => "$tr{'ffc-targetc'}",
            size   => 10,
            sort   => 'cmp',
        },
        {
            column => '10',
            title  => "$tr{'enabledtitle'}",
            size   => 5,
            tr     => 'onoff',
            align  => 'center',
        },
        {
            column => '11',
            title  => 'Timed',
            size   => 10,
            tr     => 'onoff',
            align  => 'center',
        },
        {
            title => "$tr{'mark'}",
            size  => 5,
            mark  => ' ',
        },
        {
            column => '13',
            title  => "$tr{'comment'}",
            break  => 'line',
        },
        {
            column => '14',
            title  => "Time frames",
            break  => 'line',
        }
    ]
);

dispaliastab( $filename, \%render_settings, $cgiparams{'ORDER'}, $cgiparams{'COLUMN'} );

print qq!

<table width='100%' margin:6pt 0' border='$border'>
<tr>
	<td width='25%' align='center'><input type='SUBMIT' name='ACTION' value='$tr{'remove'}' onClick="if(confirm('You are about to completely remove port forwarding rules. Are you sure you want to do this?')) {return true;} return false;"></td>
	<td width='25%' align='center'><input type='SUBMIT' name='ACTION' value='$tr{'ffc-enable rule'}'></td>
	<td width='25%' align='center'><input type='SUBMIT' name='ACTION' value='$tr{'edit'}'></td>
	<td width='25%' align='center'><input type='SUBMIT' name='ACTION' value='Set Times' onclick="location='/mods/fullfirewall/cgi-bin/timedaccess.cgi'; return false;" title="Click for Timed Access"></td>
</tr>
</table>
!;

&closebox();

print qq!
<table width='100%'>
<tr>
	  <td align='right'>
    <p style='font-size:8pt; margin:0 1em 0 0'>
      <b><i>$versionsettings{'MOD_LONG_NAME'} $versionsettings{'MOD_VERSION'}</i></b>
    </p>
  </td>
</tr>
</table>
!;

&alertbox( 'add', 'add' );

&closebigbox();

&closepage();

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
