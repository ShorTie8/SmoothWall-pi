#!/usr/bin/perl
# QoS for Express
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team


#use strict;
use warnings;
use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothtype qw( :standard );
use Socket;

my (%netsettings, %trafficsettings, %localsettings);
readhash("${swroot}/ethernet/settings", \%netsettings);
# And get current RED IP
if (-f "${swroot}/red/active")
{
  if (open (FD, "<$swroot/red/local-ipaddress")) {
    my $addr = <FD>;
    close FD;
    chomp $addr;
    $netsettings{"RED_ADDRESS"} = $addr;
  }
}
readhash("${swroot}/traffic/settings", \%trafficsettings);
# Some day include localsettings
if (-e "${swroot}/traffic/localsettings")
{
  readhash("${swroot}/traffic/localsettings", \%localsettings);
}

# Faux PID file for status display
my $qosPidFile = "/var/run/qos.pid";

my @internal_interface = ();
my %internal_netaddress = ();
my %internal_netmask = ();

# Colorize addresses and CIDRs
for(qw/GREEN_DEV ORANGE_DEV PURPLE_DEV/) {
	if(defined $netsettings{$_} &&  $netsettings{$_} ne '') {
    
		push @internal_interface, $netsettings{$_};
		if(defined $trafficsettings{'PERIPSTATS'} && $trafficsettings{'PERIPSTATS'} eq 'on') {
			my $ad = $_;
			my $colour = $_;
			$ad =~ s/_DEV/_NETADDRESS/;
			$colour =~ s/_DEV//;
			$internal_netaddress{$colour} = $netsettings{$ad} if defined $netsettings{$ad} && $netsettings{$ad} ne '';
			$ad =~ s/_NETADDRESS/_NETMASK/;
			$internal_netmask{$colour} = $netsettings{$ad} if defined $netsettings{$ad} && $netsettings{$ad} ne '';
		}
	}
}

# iface always contains valid RED IF if it's active
my $external_interface = &readvalue('/var/smoothwall/red/iface');

my $internal_speed = $trafficsettings{'INTERNAL_SPEED'} || 100000000; # 100Mb sanity default
my $upload_speed = $trafficsettings{'UPLOAD_SPEED'} || 250000; # 250 kbit sanity default
my $download_speed =  $trafficsettings{'DOWNLOAD_SPEED'} || 500000; # 500 kbit

# Get NIC bit rates
my @devices;
my %deviceRates;
if ( $netsettings{'GREEN_DEV'}) {
	$devices[$i++] = $netsettings{'GREEN_DEV'};
	my $tmp = &getLinkSpeed($netsettings{'GREEN_DEV'}, "number") * 10**6 * 0.95;
	if ( $tmp == 0) { $tmp = $internal_speed * 0.95; }
	$deviceRates{$netsettings{'GREEN_DEV'}} = int ($tmp + 0.5);
}
if ( $netsettings{'ORANGE_DEV'}) {
	$devices[$i++] = $netsettings{'ORANGE_DEV'};
	my $tmp = &getLinkSpeed($netsettings{'ORANGE_DEV'}, "number") * 10**6 * 0.95;
	if ( $tmp == 0) { $tmp = $internal_speed * 0.95; }
	$deviceRates{$netsettings{'ORANGE_DEV'}} = int ($tmp + 0.5);
}
if ( $netsettings{'PURPLE_DEV'}) {
	$devices[$i++] = $netsettings{'PURPLE_DEV'};
	my $tmp = &getLinkSpeed($netsettings{'PURPLE_DEV'}, "number") * 10**6 * 0.95;
	if ( $tmp == 0) { $tmp = $internal_speed * 0.95; }
	$deviceRates{$netsettings{'PURPLE_DEV'}} = int ($tmp + 0.5);
}
# FIXME: this should handle RED_DEV--if set--when RED is PPPOE
if ($netsettings{'RED_TYPE'} eq 'STATIC' or $netsettings{'RED_TYPE'} eq 'DHCP')
{
	$devices[$i++] = $netsettings{'RED_DEV'};
	my $tmp = &getLinkSpeed($netsettings{'RED_DEV'}, "number") * 10**6 * 0.95;
	if ( $tmp == 0) { $tmp = $internal_speed * 0.95; }
	$deviceRates{$netsettings{'RED_DEV'}} = int ($tmp + 0.5);
} else {
	# Must be PPP; get from PPPdevices (ppp0 or ippp0)
	if ($PPPdevices[0])
	{
		$devices[$i] = $PPPdevices[0];
		$deviceRates{$devices[$i++]} = $upload_speed;
	}
}


# which class to use for things not otherwise classified
my $default_traffic = $trafficsettings{'DEFAULT_TRAFFIC'} || 'normal';
# tc classids are numeric, so need to map our names to these numbers

# Read the mask and shift
&readhash("/etc/rc.d/inc.bits-flags", \%connmarkMasks );
foreach $i (sort(keys(%connmarkMasks))) {
        next if ($i !~ /^tc/);
        $connmarkMasks{$i} =~ s/"//g;
}
my $markMask = $connmarkMasks{'tcMask'};
my $markShift = $connmarkMasks{'tcShift'};
#print STDERR "\$markMask=$markMask \$markShift=$markShift\n";
undef %connmarkMasks;

# There can be 31 class IDs (1-31); they are used in the HTB classes.
my %classIDs = (
                none => 0,
                 all => 1,
              normal => 2,
                high => 3,
                 low => 4,
            isochron => 5,
         smoothadmin => 6,
            webcache => 7,
        localtraffic => 8,
            smallpkt => 9,
);
# optional override - may want extra classes
if(defined $trafficsettings{CLASSIDS} && $trafficsettings{CLASSIDS} ne '') {
  %classIDs = split(',', $trafficsettings{CLASSIDS});
}

my %prio = (
	         'high' => 1,
	       'normal' => 2,
	          'low' => 3,
	     'isochron' => 0,
	  'smoothadmin' => 2,
	     'webcache' => 2,
	 'localtraffic' => 2,
	     'smallpkt' => 2,
);
# optional override - needed if want extra classes or to change the prorities of those already here
if(defined $trafficsettings{PRIO} && $trafficsettings{PRIO} ne '') {
  %prio = split(',', $trafficsettings{PRIO});
}

# Default ratios for data coming into the smoothie
#   These match 512/256 ADSL
my %drate = (
	'high' => 1,
	'normal' => 1,
	'low' => 1,
	'isochron' => 128000,
	'smoothadmin' => 1,
	'webcache' =>  1,
	'localtraffic' => 1,
	'smallpkt' => 1,
);


my %dceil = (
	'high' => 10,
	'normal' => 100,
	'low' => 100,
	'isochron' => 128000,
	'smoothadmin' => 100,
	'webcache' => 100,
	'localtraffic' => 100,
	'smallpkt' => 100,
);


# Note: all overrides should look in localsettings, too.

# Override with UI settings
if(defined $trafficsettings{DRATE} && $trafficsettings{DRATE} ne '') {
  %drate = split(',', $trafficsettings{DRATE});
}
if(defined $trafficsettings{DCEIL} && $trafficsettings{DCEIL} ne '') {
  %dceil = split(',', $trafficsettings{DCEIL});
}
if ( defined $localsettings{'isochron'})
{
  $drate{'isochron'} = $localsettings{'isochron'};
  $dceil{'isochron'} = $localsettings{'isochron'};
}

# add these even after import
foreach (@internal_interface)
{
	#print STDERR "_:$_ deviceRates:$deviceRates{$_}\n";
	$drate{$_} = $deviceRates{$_};
	$dceil{$_} = $deviceRates{$_};
}

# max rate we can send data
my %urate = (
	'normal' => 1,
	'high' => 1,
	'low' => 1,
	'isochron' => 128000,
	'smoothadmin' => 1,
	'webcache' => 1,
	'localtraffic' => 1,
	'smallpkt' => 1,
);

my %uceil = ( 
	'normal' => 100,
	'high' => 10,
	'low' => 100,
	'isochron' => 128000,
	'smoothadmin' => 100,
	'webcache' => 100,
	'localtraffic' => 100,
	'smallpkt' => 100,
);

# default extra options is just 'quantum 1500'
my %htbClassExtras = (
	'high' => 'quantum 1500 burst 6000',
	'normal' => 'quantum 1500 burst 6000',
	'low' => 'quantum 1500 burst 6000',
	'isochron' => 'quantum 1500 burst 1500',
	'smoothadmin' => 'quantum 1500 burst 12000',
	'webcache' => 'quantum 1500 burst 12000',
	'localtraffic' => 'quantum 24000',
	'smallpkt' => 'quantum 1500 burst 1500 cburst 15000',
);
  
  
# Override with UI settings
if(defined $trafficsettings{URATE} && $trafficsettings{URATE} ne '') {
  %urate = split(',', $trafficsettings{URATE});
}
if(defined $trafficsettings{UCEIL} && $trafficsettings{UCEIL} ne '') {
  %uceil = split(',', $trafficsettings{UCEIL});
}

# local overrides
if ( defined $localsettings{'isochron'})
{
  $urate{'isochron'} = $localsettings{'isochron'};
  $uceil{'isochron'} = $localsettings{'isochron'};
}

$urate{$external_interface} = $upload_speed;
$uceil{$external_interface} = $upload_speed;



# [
#  09/2013, fest3er; connmarks now must fit within (1 to 63) << 2^11
#  (6 bits). The TC classes now run from 1-63. Don't confuse the two.
#  Rule #s *are* connmarks; (1-31): special rules, (32-63): normal rules.
# ]

# Connection marks associated with 'special' classes (6, 7, 8)*2048
# In the case of special rules ONLY, classID*2048 is the connmark.
my %connmarks = (
	'smoothadmin' => $classIDs{'smoothadmin'},
	'webcache' => $classIDs{'webcache'},
	'localtraffic' => $classIDs{'localtraffic'},
);

# First connmark useable by user defined rule is 32 (32<<11 for the actual MARK)
# We start with total, other classes get added
my @classsortorder = ('total');

# The mangle chains we use

my $POSTR = 'trafficpostrouting';
my $INPUT = 'trafficinput';
my $OUTPUT = 'trafficoutput';
my $FORWARD = 'trafficforward';

# Remember the order in which connmarks are pushed onto the traf-tot tables.
my @rulenumbers = ();
my %connmark_to_class = ();



# Prepare the normal rules to implement.
# Protocol is always an array: may need to iterate TCP and UDP.
# Each rule must have a distinct rule # (R_xx).
# The rule # * 2048 is the connmark. Rule #s thus range from 32-63.
# They are in trafficsettings in the form:
#   R_{connmark}=name,enabled,tcp?udp?,(in|out),portrange,class,comment

my @rules = ();

for(sort keys %trafficsettings) {
  next unless /^R_(\d+)/; # just looking for rules
  my $cm = $1;
  my($name, $tcp, $udp, $dir, $port, $class, $comment) = split(',', $trafficsettings{$_});
#print STDERR "cm=$1 name=$name tcp=$tcp udp=$udp dir=$dir port=$port class=$class\n      comment=$comment\n";
  next if $class eq 'none'; # this one is being ignored
  my $protocol = [];
  push @{$protocol}, 'TCP' if $tcp eq 'on';
  push @{$protocol}, 'UDP' if $udp eq 'on';

  push @rules, {
    'name' => $name,
    'protocol' => $protocol,
    'direction' => $dir,
    'connmark' => "$cm",
    'port' => $port,
    'class' => $class,
    'comment' => $comment,
  };
}


# start with a clean slate always
removetraffic();

# maybe thats all we do...

if (! ($trafficsettings{'ENABLE'} eq 'on' &&
       -e '/var/smoothwall/red/active')) {
  # Default qdisc is now stochastic fair queuing (SFQ) to ensure no stream
  #   can hog the bandwidth. We'll try a 5-second periodic shuffle.
  tcqdisc("$external_interface root handle 1: sfq perturb 1");
  tcqdisc("$_ root handle 1: sfq perturb 1")
 	for @internal_interface;
  exit(0);
} else {

  # Set the root qdiscs
  
  # note that as download queueing is done at the internal interface
  # all internal interfaces have to have the same speed. i.e. have to
  # choose the speed of the lowest. This isnt so bad if we can assume
  # that all internals are at least as fast as the external.
  
  # Add root qdiscs for external and internal interfaces - specify where default traffic goes
  tcqdisc("$external_interface root handle 1: htb default $classIDs{$default_traffic}");
  tcqdisc("$_ root handle 1: htb default $classIDs{$default_traffic}")
   	for @internal_interface;
  
  # 'all' is the parent class of all for outgoing data, set at the speed of the external interface
  # Add RED's root class; root classes don't share bandwidth
  tcclass("$external_interface parent 1:0 classid 1:feed htb" .
          " rate $upload_speed quantum 6000");
  # RED UL class capped at RED UL speed
  tcclass("$external_interface parent 1:feed classid 1:$classIDs{'all'}" .
          " htb rate $upload_speed ceil $upload_speed quantum 6000");
  # RED localtraffic class, share=internal speed - RED DL; cap=internal
  # This isn't used yet, but could be deployed when a smoothie is used inside on fast net.
  
  my $ext_up = $deviceRates{$external_interface} - $upload_speed;
  if ($ext_up < $upload_speed) { $ext_up = $upload_speed; }
  #print STDERR "IF=$external_interface EXT=$deviceRates{$external_interface} UPL=$upload_speed SUB=$ext_up\n";
  
  tcclass("$external_interface parent 1:feed classid 1:$classIDs{'localtraffic'} htb" .
          " rate $ext_up ceil $deviceRates{$external_interface} prio $prio{'localtraffic'} quantum 24000");
  tcqdisc("$external_interface parent 1:$classIDs{'localtraffic'} handle $classIDs{'localtraffic'}: sfq perturb 1");
  
  for (@internal_interface) {
    # internal root class
    tcclass("$_ parent 1:0 classid 1:feed htb" .
            " rate $deviceRates{$_} quantum 12000");
  
    # RED DL class capped at RED DL speed
    tcclass("$_ parent 1:feed classid 1:$classIDs{'all'}" .
            " htb rate $download_speed ceil $download_speed quantum 6000");
    # Localtraffic class, share=internal speed; cap=internal - RED DL
    my $int_dn = $deviceRates{$_} - $download_speed;
    if ($int_dn <= $download_speed) { $int_dn = $download_speed; }
    #print STDERR "IF=$_ INT=$deviceRates{$_} UPL=$download_speed SUB=$int_dn\n";
  
    tcclass("$_ parent 1:feed classid 1:$classIDs{'localtraffic'} htb" .
            " rate $int_dn ceil $deviceRates{$_} prio $prio{'localtraffic'} quantum 24000");
    tcqdisc("$_ parent 1:$classIDs{'localtraffic'} handle $classIDs{'localtraffic'}: sfq perturb 1");
  }
  
  # We are doing a 'flat' scheme; all classes are direct children of the root class.
  # Extra options differ so we can create things with a simple loop.			  
  
  # Create the classes and their SFQ qdiscs.
  for my $tag (sort { $classIDs{$a} <=> $classIDs{$b} } keys %classIDs) {
    next if $tag =~ /^(all|none|localtraffic)$/;
  #print STDERR "# class '$tag'\n";
    stdclass($external_interface, $tag, $htbClassExtras{$tag}, \%urate, \%uceil, $upload_speed); 
    # note can only extablish QOS for an interface that is up at the time.
    stdclass($_, $tag, $htbClassExtras{$tag}, \%drate, \%dceil, $download_speed)
        for up_interfaces(@internal_interface); 
    push @classsortorder, $tag;
  }
  
  
  # Create the packet and byte counting chains.
  for my $dir (qw/up dn/) {
    iptables("-N ${external_interface}-${dir}-traf-tot");
  }
  
  
  # As we make rules, keep a running tally of which class each connmark refers
  # to so we can cross-reference connmarks to classes
  $connmark_to_class{$connmarks{'smoothadmin'}} = 'smoothadmin';
  $connmark_to_class{$connmarks{'webcache'}} = 'webcache';
  $connmark_to_class{$connmarks{'localtraffic'}} = 'localtraffic';
  
  # special smoothadmin rule - so can admin externally even when busy
  if(defined $classIDs{'smoothadmin'}) {
    iptables("-A $OUTPUT -o $external_interface --protocol TCP" .
          " -m connmark --mark 0/$markMask" .
  	" --match multiport --source-ports 81,441,222" .
  	" -j CONNMARK --set-mark " . $connmarks{'smoothadmin'}*2048 . "/$markMask");
    push @rulenumbers, $connmarks{'smoothadmin'};
  }
  
  # Webcache special rule - give squid something.
  # [NPN: dunno why squid gets 8080 and 8443. DG?]
  if (defined $classIDs{'webcache'}) {
    iptables("-A $OUTPUT -o $external_interface  --protocol TCP" .
             " -m connmark --mark 0/$markMask" .
  	   " --match multiport --destination-ports 80,8080,443,8443" .
  	   " -j CONNMARK --set-mark " . $connmarks{'webcache'}*2048 . "/$markMask");
    push @rulenumbers, $connmarks{'webcache'};
  }
  # collect per rule stats if chosen; create named accounting tables for each RED rule.
  if(defined $trafficsettings{'PERIPSTATS'} && $trafficsettings{'PERIPSTATS'} eq 'on') {
    iptables("-A $INPUT -m connmark --mark " . $connmarks{'smoothadmin'}*2048 . "/$markMask" .
      " -j ACCOUNT --addr $netsettings{'RED_ADDRESS'} --tname RED_Smoothadmin");
    iptables("-A $POSTR -m connmark --mark " . $connmarks{'smoothadmin'}*2048 . "/$markMask" .
      " -j ACCOUNT --addr $netsettings{'RED_ADDRESS'} --tname RED_Smoothadmin");
    iptables("-A $INPUT -m connmark --mark " . $connmarks{'webcache'}*2048 . "/$markMask" .
      " -j ACCOUNT --addr $netsettings{'RED_ADDRESS'} --tname RED_Squid");
    iptables("-A $POSTR -m connmark --mark " . $connmarks{'webcache'}*2048 . "/$markMask" .
      " -j ACCOUNT --addr $netsettings{'RED_ADDRESS'} --tname RED_Squid");
  }
  
  
  # Do not mark non-admin and non-squid localtraffic going out to external.
  # If it's leaving it isn't local!
  if(defined $classIDs{'localtraffic'}) {
    iptables("-A $OUTPUT -o $external_interface -j RETURN");
  
  # Mark all other output destinations as localtraffic; if the traffic starts here e.g.
  #   from the web proxy and is going inwards it should run at full line speed.
  # FIXME: (fest3er,9/2013) No, it shouldn't; squid traffic to inside should be limited
  #   by RED's DL speed; likewise, squid traffic to the outside must be limited to RED's
  #   UL speed. (And even this isn't good enough because there's no easy way to share
  #   bandwidth among IFs; clients on GREEN and PURPLE could 'overcommit' RED's DL B/W.)
  
    iptables("-A $OUTPUT  -j CONNMARK --set-mark " . $connmarks{'localtraffic'}*2048 . "/$markMask");
  
  # Do not mark localtraffic going in from external; if it has come from the
  #   outside, we want to shape it. 
    iptables("-A $FORWARD -i $external_interface -j RETURN");
  
  # Do not mark localtraffic going out to external; if it is going to the
  #   outside, we want to shape it.
    iptables("-A $FORWARD -o $external_interface -j RETURN");
  
  # Mark everything else being forwarded as localtraffic: internal
    iptables("-A $FORWARD -m connmark --mark 0/$markMask -j CONNMARK --set-mark " . $connmarks{'localtraffic'}*2048 . "/$markMask");
  }
  
  # Generate the defined rules except those marked 'special'.
  for my $rule (@rules) {
    # we are doing this on
    my ($name, $mark, $port, $class, $direction, $proto) = 
        @{$rule}{qw/name connmark port class direction protocol/};
    next if $port eq 'special';    # special rules are handled separately
    my ($sport, $dport) = '' x 2;
    
    if($port =~ /;/) {
      # multi ports: change ';' to ','
      $port =~ s/;/,/g;
      $sport = " --match multiport --source-ports $port";
      $dport = " --match multiport --destination-ports $port";
    }
    else {
      $sport = "--source-port $port";
      $dport = "--destination-port $port";
    }
    $connmarks{$name} = $mark;
    $connmark_to_class{$mark} = $class;
    if($direction eq 'in' || $direction eq 'both') {
      # Service is hosted on GN/OR/PU
      for my $p (@{$proto}) {
        # Output to RED, source port is here
        iptables("-A $POSTR -o $external_interface --protocol $p $sport" .
  	" -m connmark --mark 0/$markMask -j CONNMARK --set-mark " . $mark*2048 . "/$markMask");
        # Input from RED, destination port is here
        iptables("-A $POSTR -i $external_interface --protocol $p $dport" .
  	" -m connmark --mark 0/$markMask -j CONNMARK --set-mark " . $mark*2048 . "/$markMask");
      }
    }	
    if($direction eq 'out' || $direction eq 'both') {
      # Service is hosted on RD
      for my $p (@{$proto}) {
        # Input from RED, source port is here
        iptables("-A $POSTR -i $external_interface --protocol $p $sport" .
          " -m connmark --mark 0/$markMask -j CONNMARK --set-mark " . $mark*2048 . "/$markMask");
        # Output to RED, destination port is here
        iptables("-A $POSTR -o $external_interface --protocol $p $dport" .
          " -m connmark --mark 0/$markMask -j CONNMARK --set-mark " . $mark*2048 . "/$markMask");
      }
    }
    # collect per rule stats if chosen - so create named accounting tables for each directly connected
    # internal network.
    if(defined $trafficsettings{'PERIPSTATS'} && $trafficsettings{'PERIPSTATS'} eq 'on') {
      for(keys %internal_netaddress) {
        iptables("-A $POSTR -m connmark --mark " . $mark*2048 . "/$markMask" .
          " -j ACCOUNT --addr $internal_netaddress{$_}/$internal_netmask{$_} --tname ${_}_$name");
      }
    }
  }
  
  # Generate the 'special' rules
  for my $rule (@rules) {
    my ($name, $mark, $port, $class) = @{$rule}{qw/name connmark port class/};
    # we are doing this on
    $connmarks{$name} = $mark;
    $connmark_to_class{$mark} = $class;
    if($name eq 'Peer_to_Peer') {
        iptables("-A $POSTR -i $external_interface" .
          " -m connmark --mark 0/$markMask" .
          " -m ipp2p --edk --dc --kazaa --gnu --bit --apple" .
          " --winmx --soul --ares --mute --waste --xdcc" .
          " -j CONNMARK --set-mark " . $mark*2048 . "/$markMask");
    }
    if($name eq 'Voice_Over_IP') {
      # also assume EF diffserv mark set wants to
      # be treated as if it were VOIP
      iptables("-A $POSTR " .
        " -m connmark --mark 0/$markMask" .
        " -m dscp --dscp-class EF -j CONNMARK --set-mark " . $mark*2048 . "/$markMask");
      
    }
    if($name eq 'VPN') {
      # no ports involved - just shape protocols 50 and 51 (ipsec)
      iptables("-A $POSTR --protocol $_ " .
        " -m connmark --mark 0/$markMask" .
        " -j CONNMARK --set-mark " . $mark*2048 . "/$markMask") for 50..51;
    }
    # other fancy rules can go here
  }
    
  
  # MUST BE LAST! special rule for smallpkt - nothing to do with connections
  # will attach to any small packet that has not been associated with a connection already...
  iptables("-A $POSTR -m connmark --mark 0/$markMask" .
      " -j CLASSIFY --set-class 1:$classIDs{'smallpkt'} --match length --length 1:110")
    if defined $classIDs{'smallpkt'};
  
  # now jump to traf-tot table for connmark to class processing (and statistics gathering)
  # uploads qued on external interface
  iptables("-A $POSTR -o $external_interface -j ${external_interface}-up-traf-tot");
  # downloads queued on each internal NIC
  for my $if (@internal_interface) {
    iptables("-A $POSTR -o $if -j ${external_interface}-dn-traf-tot");
  }
  
  # now get to assign connmarks into classes, and do connmark for default as last
  for my $cm (sort keys %connmark_to_class, 0) {
    next if $cm == "0";
    my $class = $classIDs{$connmark_to_class{$cm}} || $classIDs{$default_traffic} ;
    push @rulenumbers, $cm;
    iptables("-A ${external_interface}-up-traf-tot -o $external_interface " .
      " -m connmark --mark " . $cm*2048 . "/$markMask" .
      " -j CLASSIFY --set-class 1:$class");
    
    for my $if (@internal_interface) {
      iptables("-A ${external_interface}-dn-traf-tot -o $if" .
        " -m connmark --mark " . $cm*2048 . "/$markMask" .
        " -j CLASSIFY --set-class 1:$class");
    }
  }
  
  # so can use trafficmon etc. - SmoothTraffic compatible descriptions of what is in iptables
  writesettings();
  
  # Create faux PID file for status
  open(PF, ">$qosPidFile") && close(PF);
  
  exit(0);
}
# end of main program....



# wrappers to eliminate repeated typing
sub tcqdisc {
  # If the (optional) second arg is defined, debug info will be dumped
  #   to STDERR (smoothderror log).
  my $args = shift;
  system(split(/\s+/,'/usr/sbin/tc qdisc add dev ' . $args));
  print STDERR "/usr/sbin/tc qdisc add dev $args\n" if defined $_[0];
}

sub tcclass {
  # If the (optional) second arg is defined, debug info will be dumped
  #   to STDERR (smoothderror log).
  my $args = shift;
  system(split(/\s+/,'/usr/sbin/tc class add dev ' . $args));
  print STDERR "/usr/sbin/tc class add dev $args\n" if defined $_[0];
}

sub stdclass {
  # If the (optional) arg $print is defined, debug info will be dumped
  #   to STDERR (smoothderror log).
  my($iface, $tag, $extra, $ratehash, $ceilhash, $speed, $print) = @_;
  $extra = 'quantum 1500' unless defined $extra;
  return if $tag eq 'none';

print STDERR "iface=$iface tag=$tag extra=$extra speed=$speed prio=$prio{$tag}\n" if defined $print;
  my ($myhash, $myceil);
  if ($ratehash->{$tag} <= 100) {
    $myrate = $speed * $ratehash->{$tag} / 100;
print STDERR "  %age myrate=$myrate\n" if defined $print;
  } else {
print STDERR "  bitr myrate=$myrate\n" if defined $print;
    $myrate = $ratehash->{$tag};
  }

  if ($ceilhash->{$tag} <= 100) {
    $myceil = $speed * $ceilhash->{$tag} / 100;
print STDERR "  %age myceil=$myceil\n" if defined $print;
  } else {
    $myceil = $ceilhash->{$tag};
print STDERR "  bitr myceil=$myceil\n" if defined $print;
  }

  tcclass("$iface parent 1:$classIDs{'all'} classid 1:$classIDs{$tag} htb " .
           "rate " . $myrate ." ceil " . $myceil ." prio $prio{$tag} $extra", $print);
  if ($prio{$tag} != 0) {
    # isochron gets default (pfifo-fast); all others get sfq.
    tcqdisc("$iface parent 1:$classIDs{$tag} handle $classIDs{$tag}: sfq perturb 1", $print);
  }
#  print STDERR <<END;
#tcclass("$iface parent 1:$classIDs{'all'} classid 1:$classIDs{$tag} htb " .
#         "rate " . $myrate ." ceil " . $myceil ." prio $prio{$tag} $extra", $print);
#tcqdisc("$iface parent 1:$classIDs{$tag} handle $classIDs{$tag}: sfq perturb 1", $print);
#END
}
  

sub iptables {
  # If the (optional) second arg is defined, debug info will be dumped
  #   to STDERR (smoothderror log).
  my $args = shift;
  system(split(/\s+/,'/usr/sbin/iptables -t mangle ' . $args));
  print STDERR "iptables -t mangle $args\n" if defined $_[0];
}

# clearing out traffic
sub removetraffic {
  # If the (optional) arg is defined, debug info will be dumped
  #   to STDERR (smoothderror log).
  $print = $_[0];

  for(qw/postrouting forward output input/) {
    iptables("-F traffic$_");
  }
  for my $if ($external_interface) {
    for my $dir (qw/up dn/) { 
      iptables("-F ${if}-${dir}-traf-tot");
      iptables("-X ${if}-${dir}-traf-tot");
    }
    # and axe the qdiscs
    system(split(/\s+/,"/usr/sbin/tc qdisc del root dev $if"));
    print STDERR "/usr/sbin/tc qdisc del root dev $if\n" if defined $print;
  }
  for my $if (@internal_interface) {
    system(split(/\s+/,"/usr/sbin/tc qdisc del root dev $if"));
    print STDERR "/usr/sbin/tc qdisc del root dev $if\n" if defined $print;
  }

  # remove the PID file to simulate 'off'
  unlink($qosPidFile);
}

# this is needed to make trafficmon and trafficlogger pick up per rule info
sub writesettings {
  my $settingsdir = '/var/smoothwall/traffic';
    # chosen_speeds
  if(open(FD, ">$settingsdir/chosen_speeds")) {
    print FD "red_download=${download_speed}bps\n";
    print FD "red_upload=${upload_speed}bps\n";
    for(@internal_interface) {
      print FD "$_=$deviceRates{$_}bps\n";
    }
    close(FD);
  }
  # classid to classname lookup
  if(open(FD, ">$settingsdir/classnames")) {
    for(sort keys %classIDs) {
      next if $_ eq 'none';
      print FD "1:$classIDs{$_}=$_\n";
    }
    close(FD);
  }
  # connmark to rulename lookup
  if(open(FD, ">$settingsdir/rulenames")) {
    print FD "0=DEFAULT\n";
    for(sort keys %connmarks) {
      print FD "$connmarks{$_}=$_\n";
    }
    close(FD);
  }
  # position in traf-tot to connmark map
  if(open(FD, ">$settingsdir/rulenumbers")) {
    for(my $i = 0; $i < scalar(@rulenumbers); $i++) {
      print FD "$i=$rulenumbers[$i]\n";
    }
    close(FD);
  }
  # order classes should be presented
  if(open(FD, ">$settingsdir/classsortorder")) {
    for(my $i = 0; $i < scalar(@classsortorder); $i++) {
      print FD "$i=$classsortorder[$i]\n";
    }
    close(FD);
  }
  # connmark to class lookup
  if(open(FD, ">$settingsdir/rule2class")) {
    print FD "0=DEFAULT\n";
    for(sort keys %connmark_to_class) {
      my $class = $classIDs{$connmark_to_class{$_}};
      print FD "$_=1:$class\n";
    }
    close(FD);
  }
  system(split(/\s+/,"/bin/chown -R nobody:nobody $settingsdir"));
  #print STDERR "/bin/chown -R nobody:nobody $settingsdir\n";

}
# Tests that the given parameter is up by using the SIOCGIFFLAGS ioctl on a socket.
# Yucky bit of hard coding here but these things are not likley to change.

sub isup {
  my $dev = shift;
  my $format = "a16S"; # 16 char interface name and short flags
  my $IFF_UP = 1;
  my $SIOCGIFFLAGS = 0x8913;
  my $ioctlarg = pack($format, $dev, 0);
  local (*SOCK);
  
  socket(SOCK, AF_UNIX, SOCK_STREAM, 0) or die "no socket";
  ioctl(SOCK, 0x8913, $ioctlarg);
  close(SOCK);
  
  my ($devname, $flag) = unpack("a16S", $ioctlarg);
  return $flag & $IFF_UP;
}

# returns list of interfaces which are up
sub up_interfaces {
  return grep(isup($_), @_);
}

