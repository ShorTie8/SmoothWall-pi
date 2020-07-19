#! /usr/bin/perl

# Neal P. Murphy, copyright 2020, all rights reserved.
# This script is licensed under the GPL v2.


# Simple perl script that deletes expired ISC dhcpd leases (more than 30 days old)
#   from the lease file and clears dhcpd's old lease file.


my ($leaseStart, $leaseEnd, $leaseExpires, $leaseLine);
my (@leaseArray, @leaseSplit);

my $dhcpleasefile = "/usr/etc/dhcpd.leases";
my $olddhcpleasefile = "/usr/etc/dhcpd.leases~";

# 'Today', for comparison
my $today = `/bin/date +%Y%m%d`;

# Load the DHCP Lease File into an array
if (open (LEASES, $dhcpleasefile)) {
	@leaseArray = (<LEASES>); 
	close (LEASES);
	chomp (@leaseArray);

	# Go through all the lines
	foreach my $i (0..$#leaseArray) {
		my $leaseLine = $leaseArray[$i];

		# Skip comments and empty lines
		next if ($leaseLine =~ /^\s*#/);
		next if ($leaseLine eq '');

		# Remove open brace, double quotes, end ';' and leading/trailing spaces, 
		for ($leaseLine) {
			s/\{|\"|\;//g;
			s/^\s+//;
			s/\s+$//;
		}

		# Start of lease; save index, prep end index and Expire date
		if ($leaseLine =~ /^lease\s+((\d+\.){3}\d+)/) {
			$leaseStart = $i;
			$leaseEnd = -1;
			$leaseExpires = "";
			next;
		}

		# Expire date, save only YYYY-MM-DD
		if ($leaseLine =~ /^ends\s+\d*\s*(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2})/) {
			$leaseExpires = $leaseArray[$i];
			$leaseExpires =~ s/.*(\d{4}\/\d{2}\/\d{2}).*/$1/;
			next;
		}

		# End of lease, mark for erasure if lease is too old
		if ($leaseLine =~ /^\}/) {
			$leaseEnd = $i;
			# Now compute and 'clear'
			@leaseSplit = split("/", $leaseExpires);
			$leaseDate = `/bin/date -d "$leaseSplit[0]-$leaseSplit[1]-$leaseSplit[2] +1 month" +%Y%m%d`;
			if ($leaseDate lt $today) {
				for (my $idx=$leaseStart; $idx<=$leaseEnd; $idx++) {
					$leaseArray[$idx] = "[<-ERASE->]";
				}
			}
			next;
		}
	}
} else {
	print (STDERR "Couldn't open $dhcpleasefile to scrub it.\n");
	exit 1;
}

# Write scrubbed lease file
if (open (FILE, ">$dhcpleasefile")) {
	flock FILE, 2;

	foreach my $i (0..$#leaseArray) {
		my $leaseLine = $leaseArray[$i];
		print FILE "$leaseLine\n" unless ($leaseLine eq "[<-ERASE->]");
	}

	close (FILE);
} else {
	print (STDERR "Couldn't open $dhcpleasefile to save leases.\n");
	exit 1;
}

# Clear dhcpd's old file, too
if (system ("/bin/echo -n > $olddhcpleasefile")) {
	print (STDERR "Couldn't clear $olddhcpleasefile\n");
	exit 1;
}

exit 0;
