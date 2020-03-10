#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw(:standard);
use smoothtype qw(:standard);
use smoothd qw(message);
use Socket;
use strict;
use warnings;

my (%cgiparams, %checked, %selected, %settings);
my ($macaddress, $ignoremtutext);

my ($reddev, $dhcpip, $dhcpgw, $dhcpnm, $dhcpdns1, $dhcpdns2, $reddhcp);
my (@temp, @split1, @ips2, $line);

my $errormessage = "";
my $tmpmessage = "";
my $refresh = '';
my $success = '';

my $aliasfile = "${swroot}/mods/fullfirewall/portfw/aliases";
my $configfile = "${swroot}/mods/fullfirewall/portfw/config";

$settings{'RED_IGNOREMTU'} = '';
$settings{'DNS1_OVERRIDE'} = '';
$settings{'DNS2_OVERRIDE'} = '';

$cgiparams{'ACTION'} = '';
$cgiparams{'DNS2'} = '';
$cgiparams{'DNS2'} = '';
$cgiparams{'RED_ADDRESS'} = '';
$cgiparams{"RED_NETMASK"} = '';
$cgiparams{"DEFAULT_GATEWAY"} = '';
$cgiparams{"DNS1"} = '';
$cgiparams{"DNS2"} = '';

$selected{'STATIC'} = "";
$selected{'DHCP'} = "";
$selected{'PPPOE'} = "";

&showhttpheaders();
&getcgihash(\%cgiparams);

&readhash("${swroot}/ethernet/settings", \%settings );
if ($settings{'RED_IGNOREMTU'} ne "off")
{
  $settings{'RED_IGNOREMTU'} = "on";
}

my $sweRed = "/var/smoothwall/red";

# File 'active' exists only when RED is up; that is, PPP is up and running, dhcpcd got an
#   address, or RED is STATIC. If PPP is down or dhcpcd lost the lease, the files are emptied
#   and 'active' is deleted. But the rest of the files should always exist, empty or not.

if (-f "$sweRed/active")
{
  # fetch the device name
  $reddev = &getValue("$sweRed/iface");
}
else
{
  $errormessage .= "The RED device is not active. Cannot determine the red device type at this time.<br />";
}

# Action a "Save" request ...

if ( defined $cgiparams{'ACTION'} and ( $cgiparams{'ACTION'} eq $tr{'save'} 
       or $cgiparams{'ACTION'} eq $tr{'ffc-remove secondary'} ) )
{
  if ( $cgiparams{'2ND_RED_ADDRESS'} ne '' or $cgiparams{'MASK_ADDRESS'} ne '' )
  {
    if ( $cgiparams{'2ND_RED_ADDRESS'} eq '' and $cgiparams{'MASK_ADDRESS'} ne '' ) 
    {
        $errormessage .= "You must have a secondary IP address to associate with 
             a mapped internal IP address  $cgiparams{'MASK_ADDRESS'}<br />\n";
    }

    unless ( $cgiparams{'2ND_RED_ADDRESS'} eq '')
    { 
       unless ( &validip( $cgiparams{'2ND_RED_ADDRESS'} ) )
       {
           $errormessage .= "$tr{'multi-ip invalid'} $cgiparams{'2ND_RED_ADDRESS'}<br />\n";
       }
    }

    unless ( $cgiparams{'MASK_ADDRESS'} eq '' )
    {
      unless ( &validip( $cgiparams{'MASK_ADDRESS'} ) )
      {
        $errormessage .= "$tr{'multi-ip invalid'} $cgiparams{'MASK_ADDRESS'}<br />\n";
      }
    }

    unless ($errormessage)
    {
      my ( $line, $coloralias, $ifalias, $ifreal, $enabled );
      my (@aliases);
      my $count = 0;

      # Calculate CIDR notation and network block size
      my $aladd   = $cgiparams{'2ND_RED_ADDRESS'};
      my $intadd  = $cgiparams{'MASK_ADDRESS'};

      if ( open( FILE, "$aliasfile" ) )
      {
          @aliases = <FILE>;
          close FILE;
      }

      # count the number of aliases in the file
      foreach $line (@aliases)
      {
        if ( $line =~ /^RED:/ )
        {
          $count++;
        }
      }

      if ( open( FILE, "$aliasfile" ) )
      {
        @aliases = <FILE>;
        close FILE;
      }

      # Adding an alias ---
      unless (open( FILE, ">>$aliasfile" ))
      {
        $errormessage .= "Unable to open $aliasfile<br />\n";
        
      }
      flock FILE, 2;
      $count++;
      $coloralias = "RED:$count";
      $ifalias    = "$reddev:$count";
      $ifreal     = "$reddev";
      $enabled    = "on";
      print FILE "$coloralias,$ifalias,$ifreal,$aladd,255.255.255.255,$aladd,$enabled,on,,$intadd\n";
      close FILE;

      $success = message('ifaliasup');

      unless ( $success eq 'Successfully brought up alias interfaces.' )
      {
          $errormessage .= "Error bringing up interfaces: $success<br />\n";
      }

      &log( $tr{'multi-ip ip address added or updated'} );

      $success = message('setportfw');

      unless ( $success eq 'Port forwarding rules set' )
      {
        $errormessage .= "Error setting portforwarding rules: $success<br />\n";
      }
    }
    $cgiparams{'2ND_RED_ADDRESS'} = '';
    $cgiparams{'MASK_ADDRESS'}      = '';
  }

  if ( $cgiparams{'ACTION'} eq $tr{'ffc-remove secondary'} )
  {
    if ( $cgiparams{'SECONDARY'} eq 'NONE')
    {
      $errormessage .= "There are no secondary RED IP addresses to remove.<br />\n";
    }

    my $sec_ip = $cgiparams{'SECONDARY'};
    my $sec_dev;

    # Bring down the aliases first
    $success = message('ifaliasdown');

    unless ( $success eq 'Successfully brought down alias interfaces.' )
    {
      $errormessage .= "Error bringing interfaces down: $success<br />";
    }
    my @times;
    my ( $count, $count2, $count3, $line, $line2, $line3, @split, @split2, @split3 );
    $count = 0;

    unless (open( FILE, "$aliasfile" ))
    {
      $errormessage .= "Unable to open $aliasfile<br />\n";
    }
    my @current = <FILE>;
    close(FILE);

    open( FILE, ">$aliasfile" ) or die 'Unable to open aliases file';
    flock FILE, 2;
    foreach $line ( @current )
    {
      chomp $line;
      @split = split /,/, $line;
      unless ( $split[3] eq $cgiparams{'SECONDARY'} )
      {
        print FILE "$line\n";
      }
      else
      {
        # Remove any forwarding rules associated with the deleted interface alias
        $sec_dev = $split[1];

        unless (open( TEMP, "$configfile" ))
        {
          $errormessage .= "Unable to open $configfile<br />\n";
          
        }
        my @temp2 = <TEMP>;
        close TEMP;

        unless (open( TEMP, ">$configfile" ))
        {
          $errormessage .= "Unable to open $configfile<br />\n";
          
        }
        foreach $line2 (@temp2)
        {
          $count2++;
          chomp $line2;
          @split2 = split /,/, $line2;
          @times = split /\+/, $line2;
          if ($times[1])
          {
            $split2[13] = "+$times[1]";
          }
          unless ( ( $sec_dev eq $split2[1] )
                or ( $sec_dev eq $split2[4] ) )
          {
            print TEMP "$count2,$split2[1],$split2[2],$split2[3],$split2[4],";
            print TEMP "$split2[5],$split2[6],$split2[7],$split2[8],$split2[9],";
            print TEMP "$split2[10],$split2[11],$split2[12],$split2[13]\n";
          } else {
            print TEMP "$count2,$split2[1],$split2[2],$split2[3],$split2[4],";
            print TEMP "$split2[5],$split2[6],$split2[7],$split2[8],off,";
            print TEMP "$split2[10],$split2[11],$split2[12],$split2[13]\n";
          }
        }
        close TEMP;
      }
    }
    close FILE;

    # Reorder the aliases
    unless (open( FILE, "$aliasfile" ))
    {
      $errormessage .= "Unable to open $aliasfile<br />\n";
      
    }
    flock FILE, 2;
    @current = <FILE>;
    close FILE;

    unless (open( FILE, ">$aliasfile" ))
    {
      $errormessage .= "Unable to open $aliasfile<br />\n";
      
    }
    flock FILE, 2;
    $count = 0;
    foreach $line (@current)
    {
      chomp $line;
      @split = split( /\,/, $line );
      my $alias    = $split[1];
      my $reth     = $split[2];
      my $raddress = $split[3];
      my $rnet     = $split[4];
      my $rbroad   = $split[5];
      my $rrunning = $split[6];
      my $renabled = $split[7];
      if ( $split[0] =~ /^RED:/ )
      {
        $count++;
        print FILE "RED:$count,$reddev:$count,$reth,$raddress,$rnet,";
        print FILE "$rbroad,$rrunning,$renabled,$split[8],$split[9]\n";

        # Check for alias in portfw config file
        my $pfalias = "$reddev:$count";
        unless (open( TEMP, "$configfile" ))
        {
          $errormessage .= "Unable to open $configfile<br />\n";
          
        }
        flock TEMP, 2;
        @temp = <TEMP>;
        close TEMP;

        unless (open( TEMP, ">$configfile" ))
        {
          $errormessage .= "Unable to open $configfile<br />\n";
          
        }
        flock TEMP, 2;
        foreach $line2 (@temp)
        {
          chomp $line2;
          my @current2 = split( /\,/, $line2 );
          @times = split( /\+/, $line2 );
          if ($times[1])
          {
              $current2[13] = "+$times[1]";
          }
          my $temp0    = $current2[0];
          my $temp1    = $current2[1];
          my $temp2    = $current2[2];
          my $temp3    = $current2[3];
          my $temp4    = $current2[4];
          my $temp5    = $current2[5];
          my $temp6    = $current2[6];
          my $temp7    = $current2[7];
          my $temp8    = $current2[8];
          my $temp9    = $current2[9];
          my $temp10   = $current2[10];
          my $temp11   = $current2[11];
          my $temp12   = $current2[12];
          my $temp13   = $current2[13];

          if ( $alias eq $temp1 )
          {
            print TEMP "$temp0,$pfalias,$temp2,$temp3,$temp4,";
            print TEMP "$temp5,$temp6,$temp7,$temp8,$temp9,$temp10,$temp11,$temp12,$temp13\n";
          }
          else
          {
            print TEMP "$line2\n";
          }
        }
        close TEMP;
      }
      else
      {
        print FILE "$line\n";
      }
    }
    close FILE;

    $success = message('ifaliasup');

    unless ( $success eq 'Successfully brought up alias interfaces.' )
    {
      $errormessage .= "Error bringing up interfaces: $success<br />\n";
    }

    $success = message('setportfw');

    unless ( $success eq 'Port forwarding rules set' )
    {
      $errormessage .= "Error setting portforwarding rules: $success<br />\n";
    }

    my $count1 = 0;
    unless (open( FILE, "$configfile" ))
    {
      $errormessage .= "Unable to open $configfile<br />\n";
      
    }
    @temp = <FILE>;
    close FILE;

    unless (open( FILE, ">$configfile" ))
    {
      $errormessage .= "Unable to open $configfile<br />\n";
      
    }
    flock FILE, 2;
    foreach $line (@temp)
    {
      $count1++;
      chomp $line;
      @split = split /,/, $line;
      @times = split( /\+/, $line );
      if ($times[1])
      {
        $split[13] = "+$split[13]";
      }
      print FILE "$count1,$split[1],$split[2],$split[3],$split[4],$split[5],";
      print FILE "$split[6],$split[7],$split[8],$split[9],$split[10],";
      print FILE "$split[11],$split[12],$split[13]\n";
    }
    close FILE;
  }

  # assign the settings over the top of their erstwhile counterparts.

  $settings{'GREEN_ADDRESS'} = $cgiparams{'GREEN_ADDRESS'} if ( defined $cgiparams{'GREEN_ADDRESS'} );
  $settings{'GREEN_NETMASK'} = $cgiparams{'GREEN_NETMASK'} if ( defined $cgiparams{'GREEN_NETMASK'} );

  $settings{'ORANGE_ADDRESS'} = $cgiparams{'ORANGE_ADDRESS'} if ( defined $cgiparams{'ORANGE_ADDRESS'} );
  $settings{'ORANGE_NETMASK'} = $cgiparams{'ORANGE_NETMASK'} if ( defined $cgiparams{'ORANGE_NETMASK'} );

  $settings{'PURPLE_ADDRESS'} = $cgiparams{'PURPLE_ADDRESS'} if ( defined $cgiparams{'PURPLE_ADDRESS'} );
  $settings{'PURPLE_NETMASK'} = $cgiparams{'PURPLE_NETMASK'} if ( defined $cgiparams{'PURPLE_NETMASK'} );

  $settings{'RED_TYPE'} = $cgiparams{'RED_TYPE'} if ( defined $cgiparams{'RED_TYPE'} );
  $settings{'RED_DHCP_HOSTNAME'} = $cgiparams{'RED_DHCP_HOSTNAME'} if ( defined $cgiparams{'RED_DHCP_HOSTNAME'} );
  $settings{'RED_ADDRESS'} = $cgiparams{'RED_ADDRESS'} if ( defined $cgiparams{'RED_ADDRESS'} );
  $settings{'RED_NETMASK'} = $cgiparams{'RED_NETMASK'} if ( defined $cgiparams{'RED_NETMASK'} );

  $settings{'DEFAULT_GATEWAY'} = $cgiparams{'DEFAULT_GATEWAY'} if ( defined $cgiparams{'DEFAULT_GATEWAY'} );
  $settings{'DNS1'} = $cgiparams{'DNS1'} if ( defined $cgiparams{'DNS1'} );
  $settings{'DNS2'} = $cgiparams{'DNS2'} if ( defined $cgiparams{'DNS2'} );

  $cgiparams{'RED_IGNOREMTU'} = "off" if ( %cgiparams && ! defined $cgiparams{'RED_IGNOREMTU'} );

  $settings{'RED_IGNOREMTU'} = $cgiparams{'RED_IGNOREMTU'} if ( defined $cgiparams{'RED_IGNOREMTU'} );
  $settings{'DNS1_OVERRIDE'} = $cgiparams{'DNS1_OVERRIDE'} if ( defined $cgiparams{'DNS1_OVERRIDE'} );
  $settings{'DNS2_OVERRIDE'} = $cgiparams{'DNS2_OVERRIDE'} if ( defined $cgiparams{'DNS2_OVERRIDE'} );
  $settings{'RED_MAC'} = $cgiparams{'RED_MAC'} if ( defined $cgiparams{'RED_MAC'} );

  # now some sanity checks of the settings we've just tried
  
  if ( not &validip( $settings{'GREEN_ADDRESS'} ))
  {
    $tmpmessage .= $tr{'the ip address for the green interface is invalid'}."<br />\n";
  }

  if ( not &validmask( $settings{'GREEN_NETMASK'} ))
  {
    $tmpmessage .= $tr{'the netmask for the green interface is invalid'}."<br />\n";
  }

  if ($tmpmessage eq "") {
    ( $settings{'GREEN_NETADDRESS'}, $settings{'GREEN_BROADCAST'} ) =
      &bcast_and_net( $settings{'GREEN_ADDRESS'}, $settings{'GREEN_NETMASK'} );
  }
  else {
      $errormessage .= $tmpmessage;
  }

  if ( defined $settings{'ORANGE_ADDRESS'} and $settings{'ORANGE_ADDRESS'} ne "" ) {
     $tmpmessage = '';
     if ( not &validip( $settings{'ORANGE_ADDRESS'} )) {
       $tmpmessage .= $tr{'the ip address for the orange interface is invalid'}."<br />\n";
     }
     if ( not &validmask( $settings{'ORANGE_NETMASK'} )) {
       $tmpmessage .= $tr{'the netmask for the orange interface is invalid'}."<br />\n";
     }
     if ($tmpmessage eq "") {
        ( $settings{'ORANGE_NETADDRESS'}, $settings{'ORANGE_BROADCAST'} ) =
        &bcast_and_net( $settings{'ORANGE_ADDRESS'}, $settings{'ORANGE_NETMASK'} );
     }
     else {
        $errormessage .= $tmpmessage;
     }
  }

  if ( defined $settings{'PURPLE_ADDRESS'} and $settings{'PURPLE_ADDRESS'} ne "" ) {
     $tmpmessage = '';
     if ( not &validip( $settings{'PURPLE_ADDRESS'} )) {
        $tmpmessage .= $tr{'the ip address for the purple interface is invalid'}."<br />\n";
     }
     if ( not &validmask( $settings{'PURPLE_NETMASK'} )) {
        $tmpmessage .= $tr{'the netmask for the purple interface is invalid'}."<br />\n";
     }
     if ($tmpmessage eq "") {
        ( $settings{'PURPLE_NETADDRESS'}, $settings{'PURPLE_BROADCAST'} ) = 
        &bcast_and_net( $settings{'PURPLE_ADDRESS'}, $settings{'PURPLE_NETMASK'} ); 
     }
     else {
        $errormessage .= $tmpmessage;
     }
  }

  if ( defined $settings{'RED_MAC'} and $settings{'RED_MAC'} ne "" and not &validmac( $settings{'RED_MAC'} ))
  {
    $errormessage .= $tr{'the spoofed mac address for the red interface is invalid'}."<br />\n";
  }

  if ( defined $settings{'RED_TYPE'} and $settings{'RED_TYPE'} ne "" )
  {
    # Check for RED address already in use
    my @temp;
    unless (open( FILE, "$aliasfile" ))
    {
      $errormessage .= "Unable to open $aliasfile<br />\n";
      
    }
    @temp = <FILE>;
    close FILE;

    $tmpmessage = '';
    if ( $settings{'RED_TYPE'} eq "STATIC" ) {
       if ( not &validip( $settings{'RED_ADDRESS'} )) {
          $tmpmessage .= $tr{'the ip address for the red interface is invalid'}."<br />\n";
       }
       if ( not &validmask( $settings{'RED_NETMASK'} )) {
          $tmpmessage .= $tr{'the netmask for the red interface is invalid'}."<br />\n";
       }
       if ( $settings{'DEFAULT_GATEWAY'} ne "" and not &validmask( $settings{'DEFAULT_GATEWAY'} )) {
          $tmpmessage .= $tr{'the default gateway is invalid'}."<br />\n";
       }
       if ( $settings{'DNS1'} ne "" and not &validmask( $settings{'DNS1'} )) {
          $tmpmessage .= $tr{'invalid primary dns'}."<br />\n";
       }
       if ( $settings{'DNS2'} ne "" and not &validmask( $settings{'DNS2'} )) {
          $tmpmessage .= $tr{'invalid secondary dns'}."<br />\n";
       }
       if ( (not defined $settings{'DNS1'} or $settings{'DNS1'} eq "") and
            ($settings{'DNS2'} and $settings{'DNS2'} ne "" ) ) {
          $tmpmessage .= $tr{'cannot specify secondary dns without specifying primary'}."<br />\n";
       }
       if ( $settings{'DNS1_OVERRIDE'} ne "" and not &validmask( $settings{'DNS1_OVERRIDE'} )) {
          $tmpmessage .= $tr{'invalid primary dns override'}."<br />\n";
       }
       if ( $settings{'DNS2_OVERRIDE'} ne "" and not &validmask( $settings{'DNS2_OVERRIDE'} )) {
          $tmpmessage .= $tr{'invalid secondary dns override'}."<br />\n";
       }
       if ( (not defined $settings{'DNS1_OVERRIDE'} or $settings{'DNS1_OVERRIDE'} eq "") and
            ($settings{'DNS2_OVERRIDE'} and $settings{'DNS2_OVERRIDE'} ne "" ) ) {
          $tmpmessage .= $tr{'cannot specify secondary dns override without specifying primary override'}."<br />\n";
       }
       if ($tmpmessage eq "") {
          ( $settings{'RED_NETADDRESS'}, $settings{'RED_BROADCAST'} ) = 
             &bcast_and_net( $settings{'RED_ADDRESS'}, $settings{'RED_NETMASK'} );
       }
       else {
          $errormessage .= $tmpmessage;
       }

      foreach $line (@temp)
      {
        chomp $line;
        if ($line =~ /^RED:/)
        {
          @split1 = split /,/, $line;
          push(@ips2, $split1[3]);
        }
      }

      foreach my $vars ( @ips2 )
      {
        if ( $vars eq $cgiparams{'RED_ADDRESS'}  or $vars eq $cgiparams{'2ND_RED_ADDRESS'} 
            or $cgiparams{'RED_ADDRESS'} eq $cgiparams{'2ND_RED_ADDRESS'} )
        {
          $errormessage .= $tr{'red in use'}."<br />\n";
          $cgiparams{'RED_ADDRESS'} = $settings{'RED_ADDRESS'};
        }
      }
      $settings{'RED_ADDRESS'} = $cgiparams{'RED_ADDRESS'};
      $settings{'DEFAULT_GATEWAY'} = $cgiparams{'DEFAULT_GATEWAY'};
    }
  }

  unless ($errormessage) {
     &writehash("${swroot}/ethernet/settings", \%settings);

     $success = message('cyclenetworking');
     $errormessage .= "$tr{'smoothd failure'}: cyclenetworking<br />\n" unless ($success);

     # cyclenetworking flushes iptables, which will make some services
     # inaccessible.
     #   - Rewrite configs that need to know about the change.
     #   - Restart all services which depend on firewall rules.

     # To prevent loss of DHCP & Proxy if mods exist, use the first one that is found.
     my @ovrride = </var/smoothwall/mods/*/usr/bin/smoothwall/writedhcp.pl /usr/bin/smoothwall/writedhcp.pl>;
     system("$ovrride[0]");
     @ovrride = </var/smoothwall/mods/*/usr/bin/smoothwall/writeproxy.pl /usr/bin/smoothwall/writeproxy.pl>;
     system("$ovrride[0]");

     foreach my $service (qw(dhcpd p3scan squid im sip)) {
        $success = message("${service}restart");
        $errormessage .= $success."<br />" if ($success);
        $errormessage .= "$tr{'smoothd failure'}: ${service}restart<br />\n" unless ($success);
     }
     $refresh = "<meta http-equiv='refresh' content='2;'>" unless ($errormessage =~ /fail/i || $errormessage =~ /$tr{'smoothd failure'}/);
   }
}

# Display some DHCP values in the UI
if (( $settings{'RED_TYPE'} ne "STATIC" )) {
	if (-s "${swroot}/red/local-ipaddress") {
		$cgiparams{'RED_ADDRESS'} = &readvalue("${swroot}/red/local-ipaddress");
	}
	if (-s "${swroot}/red/remote-ipaddress") {
		$cgiparams{'DEFAULT_GATEWAY'} = &readvalue("${swroot}/red/remote-ipaddress");
	}
	if (-s "${swroot}/red/dhcp-netmask") {
		$cgiparams{'RED_NETMASK'} = &readvalue("${swroot}/red/dhcp-netmask");
	}
	if (-s "${swroot}/red/dns1") {
		$cgiparams{'DNS1'} = &readvalue("${swroot}/red/dns1");
	}
	if (-s "${swroot}/red/dns2") {
		$cgiparams{'DNS2'} = &readvalue("${swroot}/red/dns2");
	}
}

&openpage($tr{'interfaces configuration'}, 1, $refresh, 'networking');

&alertbox($errormessage);

print "<form method='post' action='?'><div>\n";

# deal with the green, orange and purple settings.
&display_interface( \%settings, 'GREEN' );
&display_interface( \%settings, 'ORANGE' ) if ($settings{'ORANGE_DEV'});
&display_interface( \%settings, 'PURPLE' ) if ($settings{'PURPLE_DEV'});

# if red is on an etherNet, show some configuration options for it.
&display_red_interface( \%settings );

print <<END;
  <div style='text-align:center;'>
   <input type='submit' name='ACTION' value='$tr{'save'}' style='margin-right:8em'>
   <input type='submit' name='ACTION' value='$tr{'ffc-remove secondary'}' style='margin-left:8em' onClick="if(confirm('Removing a secondary RED IP address will disable any port forwarding rules associated with that secondary address. You may then go to the main Firewall Control UI page and/or the external access UI page to edit or remove those rules as needed.')) {return true;} return false;"></td>
  </div>
</form>
END

&alertbox('add','add');

&closepage();

sub display_interface
{
  my ( $settings, $prefix ) = @_;

  my $interface = $settings{"${prefix}_DEV"};

  # Get the MAC address
  if (open (MACADDR, "/sys/class/net/${interface}/address"))
  {
    $macaddress = <MACADDR>;
    chomp $macaddress;
    close (MACADDR);
  }
  else
  {
    $macaddress = "";
  }

  # Get the driver name and bus
  if (open (DRIVER, "/bin/ls -C1 /sys/class/net/${interface}/device/driver/module/drivers|"))
  {
    $_ = <DRIVER>;
    chomp;
    my ($bus, $driver) = split(/:/);
    $settings{"${prefix}_DISPLAYBUS"} = $bus;
    $settings{"${prefix}_DISPLAYDRIVER"} = $driver;
    close (DRIVER);
  }

  &openbox("${prefix}:");

  print <<END;
    <table style='width: 100%;'>
    <tr>
      <td class='base' style='width: 25%;'>$tr{'physical interface'}</td>
      <td style='width: 25%;'><b>$interface</b></td>
      <td class='base' style='width: 25%;'>$tr{'ip addressc'}</td>
      <td style='width: 25%;'><input type='text' name='${prefix}_ADDRESS' value='$settings{"${prefix}_ADDRESS"}' id='${prefix}address' @{[jsvalidip("${prefix}address",'true')]}></td>
    </tr>
    <tr>
      <td class='base'>$tr{'nic type'}</td>
      <td><b>$settings{"${prefix}_DISPLAYDRIVER"} ($settings{"${prefix}_DISPLAYBUS"})</b></td>
      <td class='base'>$tr{'netmaskc'}</td>
      <td><input type='text'  name='${prefix}_NETMASK' value='$settings{"${prefix}_NETMASK"}' id='${prefix}mask' @{[jsvalidmask("${prefix}mask",'true')]}></td>
    </tr>
    <tr>
      <td class='base'>$tr{'mac addressc'}</td>
      <td><b>$macaddress</b></td>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
    </tr>
  </table>
END

  &closebox();

  return;
}

sub display_red_interface
{
  my ( $settings ) = @_;

  my $interface = $settings{"RED_DEV"};

  # Get the MAC address
  if (open (MACADDR, "/sys/class/net/${interface}/address"))
  {
    $macaddress = <MACADDR>;
    chomp $macaddress;
    close (MACADDR);
  }
  else
  {
    $macaddress = "";
  }

  # Get the driver name and bus
  if (open (DRIVER, "/bin/ls -C1 /sys/class/net/${interface}/device/driver/module/drivers|"))
  {
    $_ = <DRIVER>;
    chomp;
    my ($bus, $driver) = split(/:/);
    $settings{"RED_DISPLAYBUS"} = $bus;
    $settings{"RED_DISPLAYDRIVER"} = $driver;
    close (DRIVER);
  }

  my @temp3;
  my $flag = '';
  my $cnt = 0;
  my $var;
  my @ips;
  my $tmp;

  if (open( FILE, "$aliasfile" ))
  {
    @temp3 = <FILE>;
    close FILE;
  }

  foreach $line (@temp3)
  {
    chomp $line;
    if ($line =~ /^RED:/)
    {
      $flag = 'true';
      @split1 = split /,/, $line;
      push(@ips, $split1[3]);
    }
  }


  &openbox("RED:");

  $selected{$settings{'RED_TYPE'}} = " selected";
  $selected{$cgiparams{'SECONDARY'}} = " selected";

  my $ignoremtuchecked;
  if ($settings{'RED_IGNOREMTU'} eq "on")
  {
    $ignoremtuchecked = " checked='checked'";
  }
  else
  {
    $ignoremtuchecked = "";
  }

  print <<END;
    <table style='width: 100%;'>
    <tr>
      <td class='base' style='width: 25%;'>$tr{'physical interface'}</td>
      <td style='width: 25%;'><b>$interface</b></td>
      <td class='base' style='width: 25%;'>$tr{'connection method'}</td>
      <td style='width: 25%;'>
      <script type='text/javascript'>
function optify( field )
{
  var inputval = document.getElementById(field).value;
  if ( inputval == 'DHCP' ){
    _show('hostname');
    _show('ignoremtu');
    _hide('ipaddress');
    _show('2ndipaddress');
    _show('maskipaddress');
    _hide('netmask');
    _hide('gateway');
    _hide('primary');
    _hide('secondary');
    _show('primaryoverride');
    _show('secondaryoverride');
  } else if ( inputval == 'STATIC' ){
    _hide('hostname');
    _hide('ignoremtu');
    _show('ipaddress');
    _show('2ndipaddress');
    _show('maskipaddress');
    _show('netmask');
    _show('gateway');
    _show('primary');
    _show('secondary');
    _show('primaryoverride');
    _show('secondaryoverride');
  } else if ( inputval == 'PPPOE' ){
    _hide('hostname');
    _hide('ignoremtu');
    _hide('ipaddress');
    _show('2ndipaddress');
    _show('maskipaddress');
    _hide('netmask');
    _hide('gateway');
    _hide('primary');
    _hide('secondary');
    _hide('primaryoverride');
    _hide('secondaryoverride');
  }
}
      </script>
      <select name='RED_TYPE' id='type' onChange='optify("type");'>
        <option value='STATIC' $selected{'STATIC'}>$tr{'static'}</option>
        <option value='DHCP'   $selected{'DHCP'}>DHCP</option>
        <option value='PPPOE'  $selected{'PPPOE'}>PPPoE</option>
      </select>
      </td>
    </tr>
    <tr>
      <td class='base'>$tr{'nic type'}</td>
      <td><b>$settings{'RED_DISPLAYDRIVER'} ($settings{'RED_DISPLAYBUS'})</b></td>
      <td class='base'>$tr{'dhcp hostname'}</td>
      <td>
        <span class='input' id='hostnameText'>$settings{'RED_DHCP_HOSTNAME'}</span>
        <input id='hostname' @{[jsvalidhostname('hostname','true')]} type='text'
               style='display:none'
               name='RED_DHCP_HOSTNAME' value='$settings{"RED_DHCP_HOSTNAME"}'>
      </td>
    </tr>
    <tr>
      <td class='base'>$tr{'mac addressc'}</td>
      <td><b>$macaddress</b></td>
      <td class='base'>$tr{'ip addressc'}</td>
END


# Include both display-only and input fields, but display only one.
#   %settings: static values
#   %cgiparams: static values overridden with DHCP/PPPoE values, then with
#     DNS override values.


# use 'current' address
print <<END;
      <td style='width: 25%;'>
        <span class='input' id='ipaddressText'>$cgiparams{'RED_ADDRESS'}</span>
        <input id='ipaddress' @{[jsvalidip('ipaddress','true')]} type='text'
               style='display:none'
               name='RED_ADDRESS' value='$settings{"RED_ADDRESS"}'>
      </td>
    </tr>
    <tr>
      <td class='base'>Secondary Red $tr{'ip addressc'}</td>
      <td style='width: 25%;'>
        <span class='input' id='2ndipaddressText'>$cgiparams{'2ND_RED_ADDRESS'}</span>
        <input id='2ndipaddress'  @{[jsvalidip('2ndipaddress')]}  type='text'
                 name='2ND_RED_ADDRESS' value='$settings{'2ND_RED_ADDRESS'}'
                 title='Enter a secondary RED IP address here'>
      </td>
      <td class='base'>Secondary IP address(es):</td>
      <td style='width: 25%;'>
        <select name='SECONDARY'>
END

    if (defined $flag)
    {
      $cnt = 0;
      foreach $var (@ips)
      {
        $cnt++;
        print "<option value='$var' $selected{$var}>RED:$cnt $var</option>\n";
      }
    }

    if ($flag eq '')
    {
      print "<option value='NONE' $selected{'NONE'}>None</option>\n";
    }


print <<END;
        </select>
      </td>
    </tr>
    <tr>
      <td class='base'>Map from $tr{'ip addressc'}</td>
      <td>
        <span class='input' id='maskipaddressText'>$settings{'MASK_ADDRESS'}</span>
        <input id='maskipaddress'  @{[jsvalidip('maskipaddress')]}  type='text'
                 name='MASK_ADDRESS' value='$settings{'MASK_ADDRESS'}'
                 title='Map outgoing connections from this internal IP address to the secondary RED address above, if needed. Otherwise leave blank.'>
      </td>
    </tr>
    <tr>
    <tr>
      <td rowspan='6' colspan='2'>
END


  &openbox("Overrides");

  if ($ignoremtuchecked eq '')
  {
    $ignoremtutext = 'Not checked';
  }
  else
  {
    $ignoremtutext = 'Checked';
  }

print <<END;
        <table style='width:100%'>
          <tr>
            <td class='base'>$tr{'ignore mtu'}</td>
            <td style='width: 25%;'>
              <span class='input' id='ignoremtuText'>$ignoremtutext</span>
              <input id='ignoremtu'  type='checkbox' 
                     style='display:none'
                     name='RED_IGNOREMTU'$ignoremtuchecked>
            </td>
          </tr>
          <tr>
            <td class='base' style='width: 25%;'>$tr{'primary dns override'}</td>
            <td style='width: 25%;'>
              <span class='input' id='primaryoverrideText'>$settings{'DNS1_OVERRIDE'}</span>
              <input id='primaryoverride'
                     @{[jsvalidip('primaryoverride','true')]}
                     type='text' name='DNS1_OVERRIDE'
                     style='display:none'
                     value='$settings{"DNS1_OVERRIDE"}'>
            </td>
          </tr>
          <tr>
            <td class='base' style='width: 25%;'>$tr{'secondary dns override'}</td>
            <td style='width: 25%;'>
              <span class='input' id='secondaryoverrideText'>$settings{'DNS2_OVERRIDE'}</span>
              <input id='secondaryoverride'
                     @{[jsvalidip('secondaryoverride','true')]}
                     type='text' name='DNS2_OVERRIDE'
                     style='display:none'
                     value='$settings{"DNS2_OVERRIDE"}'>
            </td>
          </tr>
          <tr>
            <td class='base' style='width: 25%;'>$tr{'mac spoof'}</td>
            <td style='width: 25%;'>
              <input id='macspoof'
                     @{[jsvalidmac('macspoof','true')]}
                     type='text' name='RED_MAC'
                     value='$settings{"RED_MAC"}'>
            </td>
          </tr>
        </table>
END


  &closebox();


print <<END;
      </td>
    </tr>
    <tr>
      <td class='base'>$tr{'netmaskc'}</td>
      <td style='width: 25%;'>
        <span class='input' id='netmaskText'>$cgiparams{'RED_NETMASK'}</span>
        <input id='netmask' @{[jsvalidmask('netmask','true')]} type='text'
               style='display:none'
               name='RED_NETMASK' value='$settings{"RED_NETMASK"}'>
      </td>
    </tr>
    <tr>
      <td class='base' style='width: 25%;'>$tr{'default gateway'}</td>
      <td style='width: 25%;'>
        <span class='input' id='gatewayText'>$cgiparams{'DEFAULT_GATEWAY'}</span>
        <input id='gateway' @{[jsvalidip('gateway','true')]} type='text'
               style='display:none'
               name='DEFAULT_GATEWAY' value='$settings{"DEFAULT_GATEWAY"}'>
      </td>
    </tr>
    <tr>
      <td class='base' style='width: 25%;'>$tr{'primary dns'}</td>
      <td style='width: 25%;'>
        <span class='input' id='primaryText'>$cgiparams{'DNS1'}</span>
        <input id='primary' @{[jsvalidip('primary','true')]} type='text'
               style='display:none'
               name='DNS1' value='$settings{"DNS1"}'>
      </td>
    </tr>
    <tr>
      <td class='base'>$tr{'secondary dns'}</td>
      <td style='width: 25%;'>
        <span class='input' id='secondaryText'>$cgiparams{'DNS2'}</span>
        <input id='secondary' @{[jsvalidip('secondary','true')]} type='text'
               style='display:none'
               name='DNS2' value='$settings{"DNS2"}'>
      </td>
    </tr>
  </table>
END


  &closebox();

  push @_validation_items, "optify('type')" ;

  return;
}

sub bcast_and_net
{
  my ( $address, $netmask ) = @_;
  
  if (!$address || !$netmask) { return ('', ''); }

  my $addressint = inet_aton($address);
  my $netmaskint = inet_aton($netmask);

  my $netaddressint = $addressint & $netmaskint;

  my $netaddress = inet_ntoa($netaddressint);
  my $broadcast  = inet_ntoa($netaddressint | ~$netmaskint);

  return ( $netaddress, $broadcast );
}

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
