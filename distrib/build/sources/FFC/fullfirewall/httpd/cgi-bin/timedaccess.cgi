#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# SmoothWall is (c) The SmoothWall Team
#
# Modifications of this script are (c) Stanford Prescott
#
#################################################################################################
#                                                                                               #
# June 10, 2009 changed how exceptions for VPN protocols are written. Selecting                 #
# IPSEC, for example, will write all the rules necessary for IPSEC protocols and ports          #
#                                                                                               #
# June 7, 2011 A number of small changes and fixes up to this date.                             #
#  -Fixed a problem with selecting all ports                                                    #
#  -Added ability to remove only time frames from an exception and leave the exception in place #
#  -Smoothd module enhanced and updated courtesy of Steve Pittman (MtnLion)                     #
#                                                                                               #
# August 2011 More modifications for use of the xtables-addons xt_iprange xt_multiport and      #
#   xt_time. Also ported this mod to Roadster                                                   #
#                                                                                               #
#################################################################################################

use lib "/usr/lib/smoothwall";
use lib "/var/smoothwall/mods/fullfirewall/usr/lib/perl5";
use lib "/var/smoothwall/mods/fullfirewall/usr/lib/perl5/site_perl/5.14.4";

use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );
use NetAddr::IP;
use Stans::modlib;

# Subroutine for sorting things numerically instead of as strings
sub numerically { $a <=> $b; }

# 0 - turn debuggerer off
# 1 - show informational debuggerer stuff
my $debuggerer = 0;

my $moddir = '/var/smoothwall/mods/fullfirewall/portfw';
my $config = "$moddir/config";

my @hour = ( 0 .. 23 );
my @minute = ( '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', 10 .. 59 );

my $errormessage = '';
my $infomessage = '';
my $updatebutton = 0;

my ( %interfaces, %settings, %netsettings, %cgiparams, %selected, %checked );
my ($templine, @configs);

$cgiparams{'ACTION'} = '';

$cgiparams{'COLUMN'} = 1;
$cgiparams{'ORDER'} = $tr{'log ascending'};

$cgiparams{'OLDID'} = 0;
$cgiparams{'ORDER_NUMBER'} = '';
$cgiparams{'RULE_COUNT'} = 0;
$cgiparams{'RULEENABLED'} = 'on';

&getcgihash(\%cgiparams);

&readhash("${swroot}/ethernet/settings", \%netsettings);

$infomessage .= "<pre>\n";
#$infomessage .= "ENV\n";
#foreach $i (sort keys %ENV) {
#  $infomessage .= "  $i->$ENV{$i}\n";
#  }
#$infomessage .= "\n";
$infomessage .= "cgiparams\n";
foreach $i (sort keys %cgiparams) {
  $infomessage .= "  $i->$cgiparams{$i}\n";
  }
$infomessage .= "</pre>\n";

if ($ENV{'QUERY_STRING'} && ( not defined $cgiparams{'ACTION'} or $cgiparams{'ACTION'} eq "" ))
{
  my @temp = split(',',$ENV{'QUERY_STRING'});
  $cgiparams{'ORDER'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
  $cgiparams{'COLUMN'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

if ($cgiparams{'ACTION'} eq '') {
  $cgiparams{'RULEENABLED'} = 'on';
}

my $order;
my @temp;
my $line;
my $configline;
my @splitline;
my $splitline;
my ( $interface, $enabled, $timed, $port, $ipmac, $protocol, $comment );

# Only check actions if it has (a) value.
if (defined $cgiparams{'ACTION'} and $cgiparams{'ACTION'} ne "")
{
  # Action: add timeframe
  if ( $cgiparams{'ACTION'} eq $tr{'ffc-schedule'} )
  {
    $infomessage .= "add timeframe clicked<br />\n";

    my $sminute = $cgiparams{'START_MINUTE'};
    my $shour   = $cgiparams{'START_HOUR'};
    my $eminute = $cgiparams{'END_MINUTE'};
    my $ehour   = $cgiparams{'END_HOUR'};
    my $timestart = "$shour:$sminute";
    my $timestop = "$ehour:$eminute";

    if ($shour eq $ehour and $sminute eq $eminute) {
      $errormessage .= "Start time cannot equal End time!<BR />\n";
    }
      unless ($errormessage) {
    my ($Sun, $Mon, $Tue, $Wed, $Thu, $Fri, $Sat, $days);
    my $flag = '';
    # Convert days of week to numerical values and build days of week argument
    my $cnt = 0;
    if ($cgiparams{'DAY_6'} eq "on") {
      $sun = 'Sun ';
      $flag = 1;
      $cnt++;
    }
    if ($cgiparams{'DAY_0'} eq "on") {
      $mon = 'Mon ';
      $flag = 1;
      $cnt++;
    }
    if ($cgiparams{'DAY_1'} eq "on") {
      $tue = 'Tue ';
      $flag = 1;
      $cnt++;
    }
    if ($cgiparams{'DAY_2'} eq "on") {
      $wed = 'Wed ';
      $flag = 1;
      $cnt++;
    }
    if ($cgiparams{'DAY_3'} eq "on") {
      $thu = 'Thu ';
      $flag = 1;
      $cnt++;
    }
    if ($cgiparams{'DAY_4'} eq "on") {
      $fri = 'Fri ';
      $flag = 1;
      $cnt++;
    }
    if ($cgiparams{'DAY_5'} eq "on") {
      $sat = 'Sat ';
      $flag = 1;
      $cnt++;
    }
    if (defined $flag) {
      $days = "$mon$tue$wed$thu$fri$sat$sun";
      chop $days;
    }

    if ($cgiparams{'DAY_9'} eq "on" and $flag eq '') {
      $days = '';
    }

    if ($cnt == 7) {
      $timedays = 'Every day';
    } else {
      $timedays = $days;
    }

    my $timedisp = "$timedays $timestart to $timestop";

    if (open(FILE, "$config")) {
      @temp = <FILE>;
      close FILE;
    }
    open(FILE, ">$config") or die 'unable to open config file';
    flock FILE, 2;
    $id = 0;

    foreach $line (@temp)
    {
      $id++;
      chomp($line);
      my @cfg_ln = split /,/, $line;
      unless ($cgiparams{$id} eq "on") {
        print FILE "$line\n";
    # Let's handle if a user enters a time frame that spans MN
      } elsif ($shour > $ehour) {
        my $timestop2 = "23:59:59";
        $timedisp = "$cfg_ln[8] from $timestart to $timestop2 on $timedays";
        if ($cfg_ln[10] eq 'off') {
          $cfg_ln[10] = 'on';
          $cfg_ln[13] = "+$timedisp";
        } else {
          $cfg_ln[13] = "$cfg_ln[13] | $timedisp";
        }
        push (@cfg_ln, $days, $timestart, $timestop2);

        $timestart2 = "00:00:00";
        $cfg_ln[13] = "$cfg_ln[13] | $cfg_ln[8] from $timestart2 to $timestop on $timedays";
        push (@cfg_ln, $days, $timestart2, $timestop);
        my $cfg_ln_cnt = @cfg_ln;
        for (my $i = 0; $i < $cfg_ln_cnt; $i++) {
          print FILE "$cfg_ln[$i],";
        }
        print FILE "\n";
    # This bit for the user who is careful and enters appropriate time frames
      } else { 
        $timedisp = "$cfg_ln[8] from $timestart to $timestop on $timedays";
        if ($cfg_ln[10] eq 'off') {
          $cfg_ln[10] = 'on';
          $cfg_ln[13] = "+$timedisp";
        } else {
          $cfg_ln[13] = "$cfg_ln[13] | $timedisp";
        }
        push (@cfg_ln, $days, $timestart, $timestop);
        my $cfg_ln_cnt = @cfg_ln;
        for (my $i = 0; $i < $cfg_ln_cnt; $i++) {
          print FILE "$cfg_ln[$i],";
        }
        print FILE "\n";
      }
    }
    close FILE;

    $success = message('setportfw');

    unless (defined $success) {
      $errormessage .= "Unable to set timed access.<BR />\n"; }
   }
    undef $cgiparams{'START_MINUTE'};
    undef $cgiparams{'START_HOUR'};
    undef $cgiparams{'END_MINUTE'};
    undef $cgiparams{'END_HOUR'};
  }

  # Action: remove-timeframe
  if ($cgiparams{'ACTION'} eq $tr{'ffc-remove-tf'})
  {
    open(FILE, "$config") or die 'Unable to open config file.';
    my @current = <FILE>;
    close(FILE);

    my $count = 0;
    my $id = 0;
    my $line;

    # Count the # of entries checked for changing
    foreach $line (@current)
    {
      $id++;
      if ($cgiparams{$id} eq "on") {
        $count++; 
      }
    }

    if ($count == 0) {
      $errormessage .= "$tr{'nothing selected'}<BR />\n";  }

    if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
      $errormessage .= "$tr{'you can only select one item to edit'}<BR />\n";  }

    unless ($errormessage)
    {
      open(FILE, ">$config") or die 'Unable to open config file.';
      flock FILE, 2;
      $id = 0;
      $count = 1;
      foreach $line (@current)
      {
        $id++;

        unless ($cgiparams{$id} eq "on") {
          # This is not the 'droid we are looking for.
          chomp $line;
          @temp = split /,/, $line;
          @times = split /\+/, $line;
          if ($times[1]) {
            $temp[13] = "+$times[1]";
          }
          $temp[0] = $count;
          print FILE "$temp[0],$temp[1],$temp[2],$temp[3],$temp[4],";
          print FILE "$temp[5],$temp[6],$temp[7],$temp[8],$temp[9],";
          print FILE "$temp[10],$temp[11],$temp[12],$temp[13]\n";
          $count++; 
        } else {
          # Only if stripping the 'droid's day timer
          chomp $line;
          @temp = split /,/, $line;
          $temp[0] = $count;
          print FILE "$temp[0],$temp[1],$temp[2],$temp[3],$temp[4],$temp[5],$temp[6],";
          print FILE "$temp[7],$temp[8],$temp[9],off,$temp[11],$temp[12],\n";
          $count++;
        }
      }
      close(FILE);

      my $success = &message('setportfw');

      unless (defined $success) {
        $errormessage .= "$tr{'smoothd failure'}<BR />\n"; }
    }
  }

  # Action: enable/disable-timeframe
  if ($cgiparams{'ACTION'} eq $tr{'ffc-enable-tf'})
  {
    open(FILE, "$config") or die 'Unable to open config file.';
    my @current = <FILE>;
    close(FILE);

    my $count = 0;
    my $id = 0;
    my $line;
    my $onoff;

    # Count the # of entries checked for changing
    foreach $line (@current)
    {
      $id++;
      if ($cgiparams{$id} eq "on") {
        $count++; 
      }
    }

    if ($count == 0) {
      $errormessage .= "$tr{'nothing selected'}<BR />\n";  }

    unless ($errormessage)
    {
      open(FILE, ">$config") or die 'Unable to open config file.';
      flock FILE, 2;
      $id = 0;
      $count = 1;
      foreach $line (@current)
      {
        $id++;

        unless ($cgiparams{$id} eq "on") {
          # This is not the 'droid we are looking for.
          chomp $line;
          @temp = split /,/, $line;
          @times = split /\+/, $line;
          if ($times[1]) {
            $temp[13] = "+$times[1]";
          }
          $temp[0] = $count;
          print FILE "$temp[0],$temp[1],$temp[2],$temp[3],$temp[4],";
          print FILE "$temp[5],$temp[6],$temp[7],$temp[8],$temp[9],";
          print FILE "$temp[10],$temp[11],$temp[12],$temp[13]\n";
          $count++; 
        } else {
          chomp $line;
          @temp = split /,/, $line;
          @times = split /\+/, $line;
          if ($times[1]) {
            $temp[13] = "+$times[1]";
          }
          $temp[0] = $count;
	   if ($temp[10] eq 'on') {
	      $onoff = 'off';
	   } else {
		$onoff = 'on';
          }
          print FILE "$temp[0],$temp[1],$temp[2],$temp[3],$temp[4],$temp[5],$temp[6],";
          print FILE "$temp[7],$temp[8],$temp[9],$onoff,$temp[11],$temp[12],$temp[13]\n";
          $count++;
        }
      }
      close(FILE);

      my $success = &message('setportfw');

      unless (defined $success) {
        $errormessage .= "$tr{'smoothd failure'}<BR />\n"; }
    }
  }
  #
  # Finished with action handling
}

# Start HTML generation
#
$infomessage .= "generating HTML<br />\n";

&showhttpheaders();

# If it exists, pull the error log into $errormessage and delete the file.
if (-f "$moddir/configErrors.log") {
  open (ceHdl, "<$moddir/configErrors.log");
  while (<ceHdl>) {
    if (! /^  /) {
      if ($errormessage ne "") {
        $errormessage .= "</p>\n";
      }
      $errormessage .= "<p style='margin-left:18pt;text-indent:-18pt;font-size:9pt'>$_";
    } else {
      s/^  //;
      $errormessage .= "<br>$_";
    }
  }
  unlink "$moddir/configErrors.log";
}


open(FILE, "$config") or die 'Unable to open config file.';
while (<FILE>) { $cgiparams{'RULE_COUNT'}++; }
close(FILE);
$cgiparams{'RULE_COUNT'}++;
#$cgiparams{'ORDER_NUMBER'} = $cgiparams{'RULE_COUNT'};

$selected{'START_HOUR'}{$cgiparams{'START_HOUR'}} = " selected";
$selected{'START_MINUTE'}{$cgiparams{'START_MINUTE'}} = " selected";
$selected{'END_HOUR'}{$cgiparams{'END_HOUR'}} = " selected";
$selected{'END_MINUTE'}{$cgiparams{'END_MINUTE'}} = " selected";
$selected{'RULE_ACTION'}{$cgiparams{'RULE_ACTION'}} = " selected";

$selected{'TARGET'}{'ACCEPT'} = '';
$selected{'TARGET'}{'DROP'} = '';  
$selected{'TARGET'}{'REJECT'} = '';  
$selected{'TARGET'}{'LOG'} = '';  
$selected{'TARGET'}{$cgiparams{'TARGET'}} = 'selected';

&openpage($tr{'ffc-timed filtering'}, 1, '', 'networking');

print <<END

<script>
function ffoxSelectUpdate(elmt)
{
        if(!document.all) elmt.style.cssText =
        elmt.options[elmt.selectedIndex].style.cssText;
}
</script>
<script language="javascript" type="text/javascript">
  function checkWkends(form)
  {
    if (form.DAY_8.checked)
    {
      form.DAY_0.checked = '';
      form.DAY_1.checked = '';
      form.DAY_2.checked = '';
      form.DAY_3.checked = '';
      form.DAY_4.checked = '';
      form.DAY_5.checked = 'checked';
      form.DAY_6.checked = 'checked';
      form.DAY_7.checked = '';
      form.DAY_9.checked = '';
    }
    else
    {
      form.DAY_5.checked = '';
      form.DAY_6.checked = '';
    }
  }
  function checkWkdays(form)
  {
    if (form.DAY_7.checked)
    {
      form.DAY_0.checked = 'checked';
      form.DAY_1.checked = 'checked';
      form.DAY_2.checked = 'checked';
      form.DAY_3.checked = 'checked';
      form.DAY_4.checked = 'checked';
      form.DAY_5.checked = '';
      form.DAY_6.checked = '';
      form.DAY_8.checked = '';
      form.DAY_9.checked = '';
    }
    else
    {
      form.DAY_0.checked = '';
      form.DAY_1.checked = '';
      form.DAY_2.checked = '';
      form.DAY_3.checked = '';
      form.DAY_4.checked = '';
    }
  }
  function checkAlldays(form) 
  {
    if (form.DAY_9.checked)
    {
      form.DAY_0.checked = 'checked';
      form.DAY_1.checked = 'checked';
      form.DAY_2.checked = 'checked';
      form.DAY_3.checked = 'checked';
      form.DAY_4.checked = 'checked';
      form.DAY_5.checked = 'checked';
      form.DAY_6.checked = 'checked';
      form.DAY_7.checked = '';
      form.DAY_8.checked = '';
    }
    else
    {
      form.DAY_0.checked = '';
      form.DAY_1.checked = '';
      form.DAY_2.checked = '';
      form.DAY_3.checked = '';
      form.DAY_4.checked = '';
      form.DAY_5.checked = '';
      form.DAY_6.checked = '';
    }
  }
</script>

END
;

&openbigbox('100%', 'LEFT');

if ($debuggerer == 1 and $infomessage ne "") {
  print qq!
<div style="margin:4pt; color:black; background-color:#f0fff0; border:1px solid black">
  <p style="margin:4pt"><b>Informational messages</b></p>
  <div style="margin:0pt 12pt 12pt 12pt">
    $infomessage
  </div>
</div>
!;
}

&alertbox("$errormessage");

my $unused = 6;
my $ifcolor;
my $dispcolor;
my $width = 90 / $unused;

print qq!
<form method='post'>
!;

&openbox();

print qq!
<div align='center'>
  <p class='base' style='margin:0 0 8pt 0'>
    <img src='/ui/img/blob.gif'>
    <i>$tr{'ffc-select rule'}</i>
  </p>
  <table width='50%' align='center'>
    <tr>
      <td class='base' width='15%'>$tr{'fromc'}</td>
      <td width='35%'>
        <select name='START_HOUR'>
!;

foreach (@hour) {
  print "        <option value='$_' $selected{'START_HOUR'}{$_}>$_</option>\n";
}

print qq!
        </select>
        :
        <select name='START_MINUTE'>
!;

foreach (@minute) {
  print "        <option value='$_' $selected{'START_MINUTE'}{$_}>$_</option>\n";
}

print qq!
        </select>
      </td>
      <td class='base' width='15%'>$tr{'toc'}</td>
      <td width='35%'>
        <select name='END_HOUR'>
!;

foreach (@hour) {
  print "        <option value='$_' $selected{'END_HOUR'}{$_}>$_</option>\n";
}

print qq!
        </select>
        :
        <select name='END_MINUTE'>
!;

foreach (@minute) {
  print "        <option value='$_' $selected{'END_MINUTE'}{$_}>$_</option>\n";
}

print qq!
        </select>
      </td>
    </tr>
  </table>
</div>

<div align='center' id='checkBoxes'>
  <table width='50%'>
    <tr>
!;

for (my $day = 0; $day < 10; $day++)
{
  if ($day == 7)
  {
    print qq!
    </tr>
  </table>
  <table width='40%' align='center'>
    <tr>
      <td class='base' width='33%'>$tr{"ffc-day $day"}:</td>
      <td>
        <input type='radio' name='DAY_$day' $checked{"DAY_${day}"}{'on'}
               onClick='javaScript:checkWkdays(this.form);' >
      </td>
!;
  }
  elsif ($day == 8)
  {
    print qq!
      <td class='base' width='33%'>$tr{"ffc-day $day"}:</td>
      <td>
        <input type='radio' name='DAY_$day' $checked{"DAY_${day}"}{'on'}
               onClick='javaScript:checkWkends(this.form);'>
      </td>
!;
  }
  elsif ($day == 9)
  {
    print qq!
      <td class='base' width='34%'>$tr{"ffc-day $day"}:</td>
      <td>
        <input type='radio' name='DAY_$day' $checked{"DAY_${day}"}{'on'}
               onClick='javaScript:checkAlldays(this.form);'>
      </td>
!;
  }
  else
  {
    print qq!
      <td class='base'>$tr{"ffc-day $day"}:</td>
      <td>
        <input type='checkbox' name='DAY_$day' $checked{"DAY_${day}"}{'on'}>
      </td>
!;

  }
}

print qq!
    </tr>
  </table>
</div>
<div align='center'>
  <table width='100%'>
    <tr>
      <td style='text-align: center;'>
        <input type='submit' name='ACTION' value='$tr{'ffc-schedule'}'>
      </td>
    </tr>
  </table>
</div>
!;

&closebox();

&openbox($tr{'current exceptions'});

my $portmap     = portmap();
my $protocolmap = Stans::modlib::protocolmap();
my $ifcolorsmap = Stans::modlib::ifcolormap();

my %render_settings = (
    'url' => "/cgi-bin/mods/fullfirewall/timedaccess.cgi?[%COL%],[%ORD%],$cgiparams{'COLUMN'},$cgiparams{'ORDER'}",
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
            tr     => { '0.0.0.0/0' => 'Any' },
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

dispaliastab( $config, \%render_settings, $cgiparams{'ORDER'}, $cgiparams{'COLUMN'} );

print qq!
<p class='base' style='margin:0'>
  <br>
</p>

<table class='blank'>
  <tr>
    <td style='width: 50%; text-align: center;'>
      <input type='submit' name='ACTION' value='$tr{'ffc-remove-tf'}'>
    </td>
    <td style='width: 50%; text-align: center;'>
      <input type='submit' name='ACTION' value='Enable/Disable Times'>
    </td>
  </tr>
</table>
!;

&closebox();

&alertbox( 'add', 'add' );

&closebigbox();

&closepage();
