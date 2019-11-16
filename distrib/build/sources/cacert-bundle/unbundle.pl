#! /usr/bin/perl -w

my $certLines = "";
my $last1st = "";
my $last2nd = "";
my $filename = "";

# Read the bundled certs and unpack
if (open BUNDLE, "<ca-certificates.crt") {
  while (<BUNDLE>) {
    next if /^#/;
    next if /^$/;
  
    if ($_ =~ /BEGIN CERT/) {
      # Begin? Save the filename, clear queued lines
      $filename = $last2nd;
      $certLines = "";
    }

    if ($_ =~ /END CERT/) {
      # End? Write and reset
      printf("%s\n", $filename);
      if (open (outFILE, ">$filename.pem")) {
        print outFILE $certLines;
        print outFILE $_;
        close (outFILE);
      }
      $filename = "";
      $last1st = "";
      $last2nd = "";
      $certLines = "";
    }
  
    else {
      # Otherwise assemble the cert, change chars as needed, keep the previous two lines
      $certLines .= $_;
      chomp;
      s/[ \/]/_/g;
      s/[()]/=/g;
      $last2nd = $last1st;
      $last1st = $_;
    }
  }
  close(BUNDLE);
}

else {
  # File should exist, so fail badly.
  exit -1;
}
