#! /usr/bin/perl

# 7/2014; YourPadre investigated and found size differences between 32- and
#   64-bit Linux. His findings and suggestions are incorporated.

# 32- and 64-bit are different
my $sysType, $pattern, $structSize;
$sysType=`uname -m`;
$pattern = "l!l!ssl";
$structSize = 24 if ($sysType =~ "x86_64");
$structSize = 16 if ($sysType =~ "i.86");

# Variables named as used by linux kernel; see linux/input.h
$EV_KEY = 1;
$KEY_POWER = 116;
# The event value wanted is '1'; (pressed, I think)

# Find which input device is the power button
$getH = 0;
$event = "";
while ($event eq "") {
  open (eventHDL, "</proc/bus/input/devices");
  while (<eventHDL>) {
    next unless (/^S:.*LNXPWRBN/ or /^H:/);
    if (/^S:.*LNXPWRBN/) {
      $getH = 1;
      next;
    }
    if ($getH and /^H:/) {
      chomp;
      @hFields = split;
      $event = $hFields[2];
      close (eventHDL);
      break;
    }
  }

  # Clearly didn't find it, so wait minute and try again
  if ($event ne "") {
    break;
  } else {
    close (eventHDL);
    sleep 60;
  }
}

# Open the power button event node
open (eventHDL, "</dev/input/$event");
while (true) {
  if (sysread(eventHDL, $buf, $structSize) == $structSize) {
    # Unpack the structure
    ($a, $b, $type, $code, $value) = unpack($pattern, $buf);
    # And shut down if the stars align
    if ($type == $EV_KEY and $code == $KEY_POWER and $value == 1) {
      system('logger -t "powerControl" "Power button pressed; shutting down..."');
      system('shutdown -h -P -t 2 now "Power button pressed"');
    }
  } else {
    close (eventHDL);
    sleep 10;
    open (eventHDL, "</dev/input/$event");
  }
}

