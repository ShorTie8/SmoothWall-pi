#!/usr/bin/perl -w

# $Id: IP.pm,v 1.24 2004/10/11 15:40:29 lem Exp $

package NetAddr::IP;

=pod

=head1 NAME

NetAddr::IP - Manages IPv4 and IPv6 addresses and subnets

=head1 SYNOPSIS

  use NetAddr::IP;

  my $ip = new NetAddr::IP 'loopback';

  print "The address is ", $ip->addr, " with mask ", $ip->mask, "\n" ;

  if ($ip->within(new NetAddr::IP "127.0.0.0", "255.0.0.0")) {
      print "Is a loopback address\n";
  }

				# This prints 127.0.0.1/32
  print "You can also say $ip...\n";

=head1 DESCRIPTION

This module provides an object-oriented abstraction on top of IP
addresses or IP subnets, that allows for easy manipulations. Many
operations are supported, as described below:

=head2 Overloaded Operators

Many operators have been overloaded, as described below:

=cut

require 5.006_000;
use Carp;
use Socket;
use strict;
use warnings;
require Exporter;

our @EXPORT_OK = qw(Compact);

our @ISA = qw(Exporter);

our $VERSION = '3.21';

				#############################################
				# These are the overload methods, placed here
				# for convenience.
				#############################################

use overload

    '+'		=> \&plus,

    '-'		=> \&minus,

    '++'	=> \&plusplus,

    '--'	=> \&minusminus,

    "="		=> sub {
	return _fnew NetAddr::IP [ $_[0]->{addr}, $_[0]->{mask}, 
				   $_[0]->{bits} ];
    },

    '""'	=> sub { $_[0]->cidr(); },

    'eq'	=> sub { 
	my $a = ref $_[0] eq 'NetAddr::IP' ? $_[0]->cidr : $_[0];
	my $b = ref $_[1] eq 'NetAddr::IP' ? $_[1]->cidr : $_[1];
	$a eq $b;
    },

    '=='	=> sub { 
	return 0 unless ref $_[0] eq 'NetAddr::IP';
	return 0 unless ref $_[1] eq 'NetAddr::IP';
	$_[0]->cidr eq $_[1]->cidr;
    },

    '>'		=> sub {
	return undef unless $_[0]->{bits} == $_[1]->{bits};
	return ($_[0]->numeric)[1] > ($_[1]->numeric)[1]
	    if scalar($_[0]->numeric()) == scalar($_[1]->numeric());
	return scalar($_[0]->numeric()) > scalar($_[1]->numeric());
    },

    '<'		=> sub {
	return undef unless $_[0]->{bits} == $_[1]->{bits};
	return ($_[0]->numeric)[1] < ($_[1]->numeric)[1]
	    if scalar($_[0]->numeric()) == scalar($_[1]->numeric());
	return scalar($_[0]->numeric()) < scalar($_[1]->numeric());
    },

    '>='	=> sub {
	return undef unless $_[0]->{bits} == $_[1]->{bits};
	return scalar($_[0]->numeric()) >= scalar($_[1]->numeric());
    },

    '<='	=> sub {
	return undef unless $_[0]->{bits} == $_[1]->{bits};
	return scalar($_[0]->numeric()) <= scalar($_[1]->numeric());
    },

    '<=>'		=> sub {

	return undef unless $_[0]->{bits} == $_[1]->{bits};
	return ($_[0]->numeric)[1] <=> ($_[1]->numeric)[1]
	    if scalar($_[0]->numeric()) == scalar($_[1]->numeric());
	return scalar($_[0]->numeric()) <=> scalar($_[1]->numeric());
    },

    'cmp'		=> sub {

	return undef unless $_[0]->{bits} == $_[1]->{bits};
	return ($_[0]->numeric)[1] <=> ($_[1]->numeric)[1]
	    if scalar($_[0]->numeric()) == scalar($_[1]->numeric());
	return scalar($_[0]->numeric()) <=> scalar($_[1]->numeric());
    },

    '@{}'	=> sub { 
	return [ $_[0]->hostenum ]; 
    };

=pod

=over

=item B<Assignment (C<=>)>

Has been optimized to copy one NetAddr::IP object to another very quickly.

=item B<Stringification>

An object can be used just as a string. For instance, the following code

	my $ip = new NetAddr::IP 'loopback';
        print "$ip\n";

Will print the string 127.0.0.1/8.

=item B<Equality>

You can test for equality with either C<eq> or C<==>. C<eq> allows the
comparison with arbitrary strings as well as NetAddr::IP objects. The
following example:

    if (NetAddr::IP->new('loopback') eq '127.0.0.1/8') 
       { print "Yes\n"; }

Will print out "Yes".

Comparison with C<==> requires both operands to be NetAddr::IP objects.

In both cases, a true value is returned if the CIDR representation of
the operands is equal.

=item B<Comparison via E<gt>, E<lt>, E<gt>=, E<lt>=, E<lt>=E<gt> and C<cmp>>

Those are numeric comparisons. All will return undef if you attempt to
compare a V4 subnet with a V6 subnet, when V6 becomes supported some
day.

In case the version matches, the numeric representation of the network
is compared through the corresponding operation. The netmask is
ignored for these comparisons, as there is no standard criteria to say
wether 10/8 is larger than 10/10 or not.

=item B<Dereferencing as an ARRAY>

You can do something along the lines of

	my $net = new NetAddr::IP $cidr_spec;
        for my $ip (@$net) {
	  print "Host $ip is in $net\n";
	}

However, note that this might generate a very large amount of items in
the list. You must be careful when doing this kind of expansion, as it
is very easy to consume huge amounts of resources. See below for
smarter ways to do loops and other constructions that are much more
conservative.

=item B<Addition of a constant>

Adding a constant to a NetAddr::IP object changes its address part to
point to the one so many hosts above the start address. For instance,
this code:

    print NetAddr::IP->new('loopback') + 5;

will output 127.0.0.6/8. The address will wrap around at the broadcast
back to the network address. This code:

    print NetAddr::IP->new('10.0.0.1/24') + 255;

outputs 10.0.0.0/24.

=cut

sub plus {
    my $ip	= shift;
    my $const	= shift;

    return $ip unless $const;

    my $b = $ip->{bits};
    my $a = $ip->{addr};
    my $m = $ip->{mask};
    
    my $hp = "$a" & ~"$m";
    my $np = "$a" & "$m";

    if ($b == 128)		# v6?
    {
	use Math::BigInt;

	my $num = new Math::BigInt 0;

	for (0 .. 15)
	{
	    $num <<= 8;
	    $num |= vec($hp, $_, 8);
	}

#  	warn "# add - before badd($const): $num\n";
	$num->badd($const);
#  	warn "# add - after badd($const): $num\n";

	for (reverse 0 .. 15)
	{
	    my $x = new Math::BigInt $num;
	    vec($hp, $_, 8) = $x & 0xFF;
	    $num >>= 8;
#  	    warn "# add - octet $_ == $num / ", vec($hp, $_, 8), "\n";
	}
    }
    else			# v4
    {
	vec($hp, 0, $b) += $const;
    }

    return _fnew NetAddr::IP [ "$np" | ("$hp" & ~"$m"), $m, $b];
}

=item B<Substraction of a constant>

The complement of the addition of a constant.

=cut

sub minus {
    my $ip	= shift;
    my $const	= shift;

    return plus($ip, -$const, @_);
}

				# Auto-increment an object
=pod

=item B<Auto-increment>

Auto-incrementing a NetAddr::IP object causes the address part to be
adjusted to the next host address within the subnet. It will wrap at
the broadcast address and start again from the network address.

=cut

sub plusplus {
    my $ip	= shift;

    my $a = $ip->{addr};
    my $m = $ip->{mask};

    my $hp = "$a" & ~"$m";
    my $np = "$a" & "$m";

    vec($hp, 0, 32) ++;

    $ip->{addr} = "$np" | ("$hp" & ~"$m");
    return $ip;
}

=item B<Auto-decrement>

Auto-decrementing a NetAddr::IP object performs exactly the opposite
of auto-incrementing it, as you would expect.

=cut

sub minusminus {
    my $ip	= shift;

    my $a = $ip->{addr};
    my $m = $ip->{mask};

    my $hp = "$a" & ~"$m";
    my $np = "$a" & "$m";

    vec($hp, 0, 32) --;

    $ip->{addr} = "$np" | ("$hp" & ~"$m");
    return $ip;
}

				#############################################
				# End of the overload methods.
				#############################################


# Preloaded methods go here.

				# This is a variant to ->new() that
				# creates and blesses a new object
				# without the fancy parsing of
				# IP formats and shorthands.

sub _fnew ($$) {
    my $type	= shift;
    my $class	= ref($type) || $type || "NetAddr::IP";
    my $r_addr	= shift;

    return 
	bless { addr => $r_addr->[0],
		mask => $r_addr->[1],
		bits => $r_addr->[2] },
	$class;
}

				# Returns 2 ** $bits -1 (ie,
				# $bits one bits)
sub _ones ($) {
    my $bits	= shift;
    return ~vec('', 0, $bits);
}

				# Validates that a mask is composed
				# of a contiguous set of bits
sub _contiguous ($$)
{
    my $mask	= shift;
    my $octets	= shift;

#    return 1 unless defined $mask and defined $octets;

    $octets /= 8;

    for my $o (0 .. $octets)
    {
	return unless grep { vec($mask, $o, 8) == $_ }
	(255, 254, 252, 248, 240, 224, 192, 128, 0);
    }

    return 1;
}

sub _to_quad ($) {
    my $vec = shift;
    return vec($vec, 0, 8) . '.' . 
	vec($vec, 1, 8) . '.' .
	    vec($vec, 2, 8) . '.' . 
		vec($vec, 3, 8);
}

sub _to_ipv6 ($) {
    my $vec = shift;
    my $r = '';

    foreach (0..3) {
	$r .= ':' . sprintf("%02x%02x:%02x%02x",
			    vec($vec, 4*$_, 8), vec($vec, 4*$_ + 1, 8),
			    vec($vec, 4*$_ + 2, 8), vec($vec, 4*$_ + 3, 8));
    }
    $r =~ s/^://;
    return $r;
}

sub do_prefix ($$$) {
    my $mask	= shift;
    my $faddr	= shift;
    my $laddr	= shift;

    if ($mask > 24) {
        return "$faddr->[0].$faddr->[1].$faddr->[2].$faddr->[3]-$laddr->[3]";
    }
    elsif ($mask == 24) {
        return "$faddr->[0].$faddr->[1].$faddr->[2].";
    }
    elsif ($mask > 16) {
        return "$faddr->[0].$faddr->[1].$faddr->[2]-$laddr->[2].";
    }
    elsif ($mask == 16) {
        return "$faddr->[0].$faddr->[1].";
    }
    elsif ($mask > 8) {
        return "$faddr->[0].$faddr->[1]-$laddr->[1].";
    }
    elsif ($mask == 8) {
        return "$faddr->[0].";
    }
    else {
        return "$faddr->[0]-$laddr->[0]";
    }
}

sub _parse_mask ($$) {
    my $mask	= lc shift;
    my $bits	= shift;

    my $bmask	= '';

    if ($bits == 128) {
	if (grep($mask eq $_ , qw(unspecified loopback))) {
	    for (0..3) {
	    	vec($bmask, $_, 32) = 0xFFFFFFFF;
	    }
	}
	elsif ($mask =~ /^(\d+)$/ && $1 <= 128) {
	    foreach (0..3) {
		if ($mask >= 32*($_ + 1)) {
		    vec($bmask, $_, 32) = 0xFFFFFFFF;
		}
		elsif ($mask > 32*$_) {
		    vec($bmask, $_, 32) = 0xFFFFFFFF;
		    vec($bmask, $_, 32) <<= (32*($_ + 1) - $mask);
		} 
		else {
			vec($bmask, $_, 32) = 0x0;
		}
	    }
	}
	else {
	     $bmask = undef;
	}
        return $bmask;
    }
    elsif ($mask eq 'default' or $mask eq 'any') {
	vec($bmask, 0, $bits) = 0x0;
    }
    elsif ($mask eq 'broadcast' or $mask eq 'host') {
	vec($bmask, 0, $bits) = _ones $bits;
    }
    elsif ($mask eq 'loopback') {
	vec($bmask, 0, 8) = 255;
	vec($bmask, 1, 8) = 0;
	vec($bmask, 2, 8) = 0;
	vec($bmask, 3, 8) = 0;
    }
    elsif ($mask =~ m/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/) {

	for my $i ($1, $2, $3, $4) {
	    return undef 
		unless grep { $i == $_ }
	    (255, 254, 252, 248, 240, 224, 192, 128, 0);
	}

	return undef if ($1 < $2 or $2 < $3 or $3 < $4);
	
	return undef if $2 != 0 and $1 != 255;
	return undef if $3 != 0 and $2 != 255;
	return undef if $4 != 0 and $3 != 255;
					   
	vec($bmask, 0, 8) = $1;
	vec($bmask, 1, 8) = $2;
	vec($bmask, 2, 8) = $3;
	vec($bmask, 3, 8) = $4;
    }
    elsif ($mask =~ m/^(\d+)$/ and $1 <= 32) {
	if ($1) {
	    vec($bmask, 0, $bits) = _ones $bits;
	    vec($bmask, 0, $bits) <<= ($bits - $1);
	} else {
	    vec($bmask, 0, $bits) = 0x0;
	}
    }
    elsif ($mask =~ m/^(\d+)$/) {
        vec($bmask, 0, $bits) = $1;
    }

    return $bmask;
}

sub _obits ($$) {
    my $lo = shift;
    my $hi = shift;

    return 0xFF if $lo == $hi;
    return (~ ($hi ^ $lo)) & 0xFF;
}

sub _v4 ($$$) {
    my $ip	= lc shift;
    my $mask	= shift;
    my $present	= shift;

    my $addr = '';
    my $a; 

    if ($ip eq 'default' or $ip eq 'any') {
	vec($addr, 0, 32) = 0x0;
    }
    elsif ($ip eq 'broadcast') {
	vec($addr, 0, 32) = _ones 32;
    }
    elsif ($ip eq 'loopback') {
	vec($addr, 0, 8) = 127;
	vec($addr, 3, 8) = 1;
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/
	   and $1 >= 0 and $1 <= 255
	   and $2 >= 0 and $2 <= 255
	   and $3 >= 0 and $3 <= 255
	   and $4 >= 0 and $4 <= 255)
    {
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = $2;
	vec($addr, 2, 8) = $3;
	vec($addr, 3, 8) = $4;
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)$/
	   and $1 >= 0 and $1 <= 255
	   and $2 >= 0 and $2 <= 255)
    {
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = ($present ? $2 : 0);
	vec($addr, 2, 8) = 0;
	vec($addr, 3, 8) = ($present ? 0 : $2);
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)\.(\d+)$/
	   and $1 >= 0 and $1 <= 255
	   and $2 >= 0 and $2 <= 255
	   and $3 >= 0 and $3 <= 255)
    {
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = $2;
	vec($addr, 2, 8) = ($present ? $3 : 0);
	vec($addr, 3, 8) = ($present ? 0 : $3);
    }
    elsif ($ip =~ m/^([xb\d]+)$/ and $1 >= 0 and $1 < 255 and $present) 
    {
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = 0;
	vec($addr, 2, 8) = 0;
	vec($addr, 3, 8) = 0;
    }
    elsif ($ip =~ m/^(-?[xb\d]+)$/) 
    {
	my $num = $1;
	$num += 2 ** 32 if $num < 0;
	vec($addr, 0, 32) = $1;
    }

				# The notations below, include an
				# implicit mask specification.

    elsif ($ip =~ m/^(\d+)\.$/ and $1 >= 0 and $1 <= 255) {
	#print "^(\\d+)\\.\$\n";
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = 0;
	vec($addr, 2, 8) = 0;
	vec($addr, 3, 8) = 0;
	vec($mask, 0, 32) = 0xFF000000;
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)-(\d+)\.?$/ 
	   and $1 >= 0 and $1 <= 255
	   and $2 >= 0 and $2 <= 255
	   and $3 >= 0 and $3 <= 255
	   and $2 <= $3) {
	#print "^(\\d+)\\.(\\d+)-(\\d+)\\.?\$\n";
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = $2;
	vec($addr, 2, 8) = 0;
	vec($addr, 3, 8) = 0;

	vec($mask, 0, 32) = 0x0;
	vec($mask, 0, 8) = 0xFF;
	vec($mask, 1, 8) = _obits $2, $3;
    }
    elsif ($ip =~ m/^(\d+)-(\d+)\.?$/ 
	   and $1 >= 0 and $1 <= 255
	   and $2 >= 0 and $2 <= 255
	   and $1 <= $2) {
	#print "^(\\d+)-(\\d+)\\.?\$\n";
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = 0;
	vec($addr, 2, 8) = 0;
	vec($addr, 3, 8) = 0;

	vec($mask, 0, 32) = 0x0;
	vec($mask, 0, 8) = _obits $1, $2;
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)\.$/ and $1 >= 0 
	   and $1 <= 255 and $2 >= 0 and $2 <= 255) 
    {
	#print "^(\\d+)\\.(\\d+)\\.\$\n";
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = $2;
	vec($addr, 2, 8) = 0;
	vec($addr, 3, 8) = 0;
	vec($mask, 0, 32) = 0xFFFF0000;
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)\.(\d+)-(\d+)\.?$/ 
	   and $1 >= 0 and $1 <= 255
	   and $2 >= 0 and $2 <= 255
	   and $3 >= 0 and $3 <= 255
	   and $4 >= 0 and $4 <= 255
	   and $3 <= $4) {
	#print "^(\\d+)\\.(\\d+)\\.(\\d+)-(\\d+)\\.?\$\n";
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = $2;
	vec($addr, 2, 8) = $3;
	vec($addr, 3, 8) = 0;

	vec($mask, 0, 32) = 0x0;
	vec($mask, 0, 8) = 0xFF;
	vec($mask, 1, 8) = 0xFF;
	vec($mask, 2, 8) = _obits $3, $4;
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)\.(\d+)\.$/ and $1 >= 0 
	   and $1 <= 255 and $2 >= 0 and $2 <= 255
	   and $3 >= 0 and $3 <= 255) 
    {
	#print "^(\\d+)\\.(\\d+)\\.(\\d+)\\.\$\n";
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = $2;
	vec($addr, 2, 8) = $3;
	vec($addr, 3, 8) = 0;
	vec($mask, 0, 32) = 0xFFFFFF00;
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)\.(\d+)\.(\d+)-(\d+)$/ 
	   and $1 >= 0 and $1 <= 255
	   and $2 >= 0 and $2 <= 255
	   and $3 >= 0 and $3 <= 255
	   and $4 >= 0 and $4 <= 255
	   and $5 >= 0 and $5 <= 255
	   and $4 <= $5) {
	#print "^(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)-(\\d+)\$\n";
	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = $2;
	vec($addr, 2, 8) = $3;
	vec($addr, 3, 8) = $4;

	vec($mask, 0, 8) = 0xFF;
	vec($mask, 1, 8) = 0xFF;
	vec($mask, 2, 8) = 0xFF;
	vec($mask, 3, 8) = _obits $4, $5;
    }
    elsif ($ip =~ m/^(\d+)\.(\d+)\.(\d+)\.(\d+)
	   \s*-\s*(\d+)\.(\d+)\.(\d+)\.(\d+)$/x
	   and $1 >= 0 and $1 <= 255
	   and $2 >= 0 and $2 <= 255
	   and $3 >= 0 and $3 <= 255
	   and $4 >= 0 and $4 <= 255
	   and $5 >= 0 and $5 <= 255
	   and $6 >= 0 and $6 <= 255
	   and $7 >= 0 and $7 <= 255
	   and $8 >= 0 and $8 <= 255)
    {
	my $last = '';

	vec($addr, 0, 8) = $1;
	vec($addr, 1, 8) = $2;
	vec($addr, 2, 8) = $3;
	vec($addr, 3, 8) = $4;

	vec($last, 0, 8) = $5;
	vec($last, 1, 8) = $6;
	vec($last, 2, 8) = $7;
	vec($last, 3, 8) = $8;

	vec($mask, 0, 8) = _obits $1, $5;
	vec($mask, 1, 8) = _obits $2, $6;
	vec($mask, 2, 8) = _obits $3, $7;
	vec($mask, 3, 8) = _obits $4, $8;
    }
    elsif (($a = gethostbyname($ip)) and defined($a)
	   and ($a ne pack("C4", 0, 0, 0, 0))) {
	if ($a and inet_ntoa($a) =~ m!^(\d+)\.(\d+)\.(\d+)\.(\d+)$!)  {
	    vec($addr, 0, 8) = $1;
	    vec($addr, 1, 8) = $2;
	    vec($addr, 2, 8) = $3;
	    vec($addr, 3, 8) = $4;
	}
    }
    elsif (!$present and length($ip) == 4) {
	my @o = unpack("C4", $ip);

	vec($addr, $_, 8) = $o[$_] for 0 .. 3;
	vec($mask, 0, 32) = 0xFFFFFFFF;
    }
    else {
#	croak "Cannot obtain an IP address out of $ip";
	return undef;
    }

    return { addr => $addr, mask => $mask, bits => 32 };
}

sub expand_v6 ($) {
    my $pat = shift;

    if (length($pat) < 4) {
	$pat = ('0' x (4 - length($pat))) . $pat;
    }
    return $pat;
}

sub _v6_part ($$$) {
    my $addr = shift;
    my $four = shift;
    my $n = shift;

    my($a, $b);

    return undef unless length($four) == 4;
    $four =~ /^(.{2})(.{2})/;
    ($a, $b) = ($1, $2);

    vec($addr, 2*$n, 8) = hex($a);
    vec($addr, 2*$n + 1, 8) = hex($b);

    return $addr;
}

sub _v6 ($$$) {
    my $ip	= lc shift;
    my $mask	= shift;
    my $present	= shift;

    my $addr = '';
    my $colons; 
    my $expanded;
    my @ip;

    if ($ip eq 'unspecified') {
	$ip = '::';
    }
    elsif ($ip eq 'loopback') {
	$ip = '::1';
    }
    elsif ($ip =~ /:::/ || $ip =~ /::.*::/) {
	return;
    }
    return unless $ip =~ /^[\da-f\:]+$/i;

    $colons = ($ip =~ tr/:/:/);
    return unless $colons >= 2 && $colons <= 7;
    $expanded = ':0' x (9 - $colons);
    $expanded =~ s/0$// if ($ip =~ /^[\da-f]+::[\da-f]+$/);
#    warn "# colons = $colons\n";
#    warn "# expanded = $expanded\n";
    $ip =~ s/::/$expanded/;
    $ip = '0' . $ip if $ip =~ /^:/;
#    warn "# ip = $ip\n";
    # .:.:.:.:.:.:.:.
    @ip = split(/:/, $ip);
    grep($_ = expand_v6($_), @ip);;
    for (0..$#ip) {
    	$addr = _v6_part($addr, $ip[$_], $_);
        return unless defined $addr;
    }

    return { addr => $addr, mask => $mask, bits => 128 };
}

sub new4 ($$;$) {
    new($_[0], $_[1], $_[2]);
}

=pod

=back

=head2 Serializing and Deserializing

This module defines hooks to collaborate with L<Storable> for
serializing C<NetAddr::IP> objects, through compact and human readable
strings. You can revert to the old format by invoking this module as

  use NetAddr::IP ':old_storable';

You must do this if you have legacy data files containing NetAddr::IP
objects stored using the L<Storable> module.

=cut

sub import
{
    unless (grep { $_ eq ':old_storable' } @_)
    {
	*{STORABLE_freeze} = sub 
	{
	    my $self = shift;
	    return $self->cidr();	# use stringification
	};
	*{STORABLE_thaw} = sub 
	{
	    my $self	= shift;
	    my $cloning	= shift;	# Not used
	    my $serial	= shift;
	    
	    my $ip = new NetAddr::IP $serial;
	    $self->{addr} = $ip->{addr};
	    $self->{mask} = $ip->{mask};
	    $self->{bits} = $ip->{bits};
	    return;
	};
    }

    @_ = grep { $_ ne ':old_storable' } @_;
    NetAddr::IP->export_to_level(1, @_);
}

=pod

=head2 Methods

=over

=item C<-E<gt>new([$addr, [ $mask|IPv6 ]])>

This method creates a new IPv4 address with the supplied address in
C<$addr> and an optional netmask C<$mask>, which can be omitted to get
a /32 mask.

C<$addr> can be almost anything that can be resolved to an IP address
in all the notations I have seen over time. It can optionally contain
the mask in CIDR notation.

B<prefix> notation is understood, with the limitation that the range
speficied by the prefix must match with a valid subnet.

Addresses in the same format returned by C<inet_aton> or
C<gethostbyname> are also understood, although no mask can be
specified for them.

If called with no arguments, 'default' is assumed.

IPv6 addresses according to RFC 1884 are also supported, except IPv4
compatible IPv6 addresses.

=cut

sub new ($$;$) {
    my $type	= $_[0];
    my $class	= ref($type) || $type || "NetAddr::IP";
    my $ip	= lc $_[1];
    my $hasmask	= 1;
    my $bits;
    my $mask;

    $ip = 'default' unless defined $ip;
    $bits = $ip =~ /:/ ? 128 : 32;

    if (@_ == 2) {
	if ($ip =~ m!^(.+)/(.+)$!) {
	    $ip		= $1;
	    $mask	= $2;
	}
	elsif (grep { $ip eq $_ } (qw(default any broadcast loopback))) 
	{
	    $mask	= $ip;
	}
    }

    if (defined $_[2]) {
	if ($_[2] =~ /^ipv6$/i) {
	    if (grep { $ip eq $_ } (qw(unspecified loopback))) {
		$bits	= 128;
	    	$mask	= _parse_mask $ip, $bits;
	    }
	    else {
		return undef;
	   }
	}
	else {
	    $mask	= _parse_mask $_[2], $bits;
	}
	return undef unless defined $mask;
    }
    elsif (defined $mask) {
	$mask 		= _parse_mask $mask, $bits;
	return undef unless defined $mask;
    }
    else {
	$hasmask	= 0;
	$mask 		= _parse_mask $bits, $bits;
	return undef unless defined $mask;
    }

    my $self = $bits == 32 ? _v4($ip, $mask, $hasmask)
			   : _v6($ip, $mask, $hasmask);

    return unless $self;
    return unless _contiguous $self->{mask}, $self->{bits};

    return bless $self, $class;
}

=pod

=item C<-E<gt>broadcast()>

Returns a new object refering to the broadcast address of a given
subnet. The broadcast address has all ones in all the bit positions
where the netmask has zero bits. This is normally used to address all
the hosts in a given subnet.

=cut

sub broadcast ($) {
    my $self	= shift;
    return $self->_fnew($self->_broadcast);
}

sub _broadcast ($) {
    my $self	= shift;
    my $a = $self->{addr};
    my $m = $self->{mask};
    my $c = '';

    vec($c, 0, $self->{bits}) = _ones $self->{bits};
    vec($c, 0, $self->{bits}) ^= vec($m, 0, $self->{bits});

    return [ "$a" | ~ "$m" | $c, $self->{mask}, $self->{bits} ];
}

=pod

=item C<-E<gt>network()>

Returns a new object refering to the network address of a given
subnet. A network address has all zero bits where the bits of the
netmask are zero. Normally this is used to refer to a subnet.

=cut

sub network ($) {
    my $self	= shift;
    return $self->_fnew($self->_network);
}

sub _network ($) {
    my $self	= shift;
    my $a = $self->{addr};
    my $m = $self->{mask};

    return [ "$a" & "$m", $self->{mask}, $self->{bits} ];
}

=pod

=item C<-E<gt>addr()>

Returns a scalar with the address part of the object as a
dotted-quad. This is useful for printing or for passing the address
part of the NetAddr::IP object to other components that expect an IP
address.

=cut

sub addr ($) {
    my $self	= shift;
    $self->{bits} == 32 ? _to_quad $self->{addr}
			: _to_ipv6 $self->{addr};
}


=pod

=item C<-E<gt>mask()>

Returns a scalar with the mask as a dotted-quad.

=cut

sub mask ($) {
    my $self	= shift;
    $self->{bits} == 32 ? _to_quad $self->{mask}
			: _to_ipv6 $self->{mask};
}

=pod

=item C<-E<gt>masklen()>

Returns a scalar the number of one bits in the mask.

=cut

sub masklen ($) {
    my $self	= shift;
    my $bits	= 0;

    for (my $i = 0;
	 $i < $self->{bits};
	 $i ++) 
    {
	$bits += vec($self->{mask}, $i, 1);
    }

    return $bits;
}

=pod

=item C<-E<gt>bits()>

Returns the wide of the address in bits. Normally 32 for v4 and 128 for v6.

=cut

sub bits { return $_[0]->{bits}; }

=pod

=item C<-E<gt>version()>

Returns the version of the address or subnet. Currently this can be
either 4 or 6.

=cut

sub version { return $_[0]->{bits} == 32 ? 4 : 6; }

=pod

=item C<-E<gt>cidr()>

Returns a scalar with the address and mask in CIDR notation. A
NetAddr::IP object I<stringifies> to the result of this function.

=cut

sub cidr ($) {
    my $self	= shift;
    return $self->addr . '/' . $self->masklen;
}

=pod

=item C<-E<gt>aton()>

Returns the address part of the NetAddr::IP object in the same format
as the C<inet_aton()> function. This should ease a bit the code
required to deal with "old-style" sockets.

=cut

sub aton {
    my $self = shift;
    return pack "C4", split /\./, $self->addr;
}

=pod

=item C<-E<gt>range()>

Returns a scalar with the base address and the broadcast address
separated by a dash and spaces. This is called range notation.

=cut

sub range ($) {
    my $self = shift;
    my $mask = $self->masklen;

    return undef if $self->{bits} > 32;
    return $self->network->addr . ' - ' . $self->broadcast->addr;
}

=pod

=item C<-E<gt>prefix()>

Returns a scalar with the address and mask in prefix
representation. This is useful for some programs, which expect its
input to be in this format. This method will include the broadcast
address in the encoding.

=cut

sub prefix ($) {
    my $self = shift;
    my $mask = $self->masklen;

    return undef if $self->{bits} > 32;
    return $self->addr if $mask == 32;

    my @faddr = split (/\./, $self->first->addr);
    my @laddr = split (/\./, $self->broadcast->addr);

    return do_prefix $mask, \@faddr, \@laddr;
}

=pod

=item C<-E<gt>nprefix()>

Just as C<-E<gt>prefix()>, but does not include the broadcast address.

=cut

sub nprefix ($) {
    my $self = shift;
    my $mask = $self->masklen;

    return undef if $self->{bits} > 32;
    return $self->addr if $mask == 32;

    my @faddr = split (/\./, $self->first->addr);
    my @laddr = split (/\./, $self->last->addr);

    return do_prefix $mask, \@faddr, \@laddr;
}

=pod

=item C<-E<gt>numeric()>

When called in a scalar context, will return a numeric representation
of the address part of the IP address. When called in an array
contest, it returns a list of two elements. The first element is as
described, the second element is the numeric representation of the
netmask.

This method is essential for serializing the representation of a
subnet.

=cut

sub numeric ($) {
    my $self	= shift;
    if ($self->version == 4)
    {
	return 
	    wantarray() ? ( vec($self->{addr}, 0, 32), 
			    vec($self->{mask}, 0, 32) ) :
				vec($self->{addr}, 0, 32);
    }
    else
    {
	my $n = new Math::BigInt 0;
	my $m = new Math::BigInt 0 if wantarray;
	for (0 .. 3)
	{
	    $n <<= 32;
	    $n += vec($self->{addr}, $_, 32);
	    if (wantarray)
	    {
		$m <<= 32;
		$m += vec($self->{mask}, $_, 32);
	    }
	}
	return wantarray ? ($n, $m) : $n;
    }
}

=pod

=item C<-E<gt>wildcard()>

When called in a scalar context, returns the wildcard bits
corresponding to the mask, in dotted-quad format.

When called in an array context, returns a two-element array. The
first element, is the address part. The second element, is the
wildcard translation of the mask.

=cut

sub wildcard ($) {
    my $self	= shift;
    return undef if $self->{bits} > 32;
    return wantarray() ? ($self->addr, _to_quad ~$self->{mask}) :
	_to_quad ~$self->{mask};
			      
}

=pod

=item C<-E<gt>short()>

Returns the address part in a short or compact notation. (ie,
127.0.0.1 becomes 127.1). Works with both, V4 and V6. Note that
C<compact_addr> is now deprecated.

=cut

sub _compact_v6 ($) {
    my $addr = shift;

    my @o = split /:/, $addr;
    return $addr unless @o and grep { $_ =~ m/^0+$/ } @o;

    my @candidates	= ();
    my $start		= undef;

    for my $i (0 .. $#o)
    {
	if (defined $start)
	{
	    if ($o[$i] !~ m/^0+$/)
	    {
		push @candidates, [ $start, $i - $start ];
		$start = undef;
	    }
	}
	else
	{
	    $start = $i if $o[$i] =~ m/^0+$/;
	}
    }

    push @candidates, [$start, 8 - $start] if defined $start;

    my $l = (sort { $b->[1] <=> $a->[1] } @candidates)[0];

    return $addr unless defined $l;

    $addr = $l->[0] == 0 ? '' : join ':', @o[0 .. $l->[0] - 1];
    $addr .= '::';
    $addr .= join ':', @o[$l->[0] + $l->[1] .. $#o];
    $addr =~ s/(^|:)0{1,3}/$1/g;

    return $addr;
}

sub short ($)
{
    my $self = shift;
    my $addr = $self->addr;
    if ($self->{bits} == 32)
    {
	my @o = split(/\./, $addr, 4);
	splice(@o, 1, 2) if $o[1] == 0 and $o[2] == 0;
	return join '.', @o;
    }
    else
    {
	return _compact_v6 _to_ipv6 $self->{addr};
    }
}

*{compact_addr} = \&short;

=pod

=item C<$me-E<gt>contains($other)>

Returns true when C<$me> completely contains C<$other>. False is
returned otherwise and C<undef> is returned if C<$me> and C<$other>
are of different versions.

Note that C<$me> and C<$other> must be C<NetAddr::IP> objects.

=cut

sub contains ($$) {
    my $a	= shift;
    my $b	= shift;

    my $bits	= $a->{bits};

    my $mask;
    
				# Both must be of the same length...
    return undef
	unless $bits == $b->{bits};

				# $a must be less specific than $b...
    my ($a_addr, $a_mask) = $a->numeric;
    my ($b_addr, $b_mask) = $b->numeric;

    return 0 unless $a_mask <= $b_mask;

				# A default address always contains
    return 1 if ($a_mask == 0x0);

    return ($a_addr & $a_mask) == ($b_addr & $a_mask);
}

=pod

=item C<$me-E<gt>within($other)>

The complement of C<-E<gt>contains()>. Returns true when C<$me> is
completely con tained within C<$other>.

Note that C<$me> and C<$other> must be C<NetAddr::IP> objects.

=cut

sub within ($$) {
    return contains($_[1], $_[0]);
}

=pod

=item C<-E<gt>split($bits)>

Returns a list of objects, representing subnets of C<$bits> mask
produced by splitting the original object, which is left
unchanged. Note that C<$bits> must be longer than the original
mask in order for it to be splittable.

Note that C<$bits> can be given as an integer (the length of the mask)
or as a dotted-quad. If omitted, a host mask is assumed.

=cut

sub split ($;$) {
    return @{$_[0]->splitref($_[1])};
}

=pod

=item C<-E<gt>splitref($bits)>

A (faster) version of C<-E<gt>split()> that returns a reference to a
list of objects instead of a real list. This is useful when large
numbers of objects are expected.

=cut

sub splitref ($;$) {
    my $self	= shift;
    my $mask	= _parse_mask shift || $self->{bits}, $self->{bits};

    my $bits	= $self->{bits};

    my @ret;

    if (vec($self->{mask}, 0, $bits) 
	<= vec($mask, 0, $bits))
    {
	my $num		= '';
	my $v		= '';

	my $net	= $self->network->{addr};
	$net = "$net" & "$mask";

	my $to = $self->broadcast->{addr};
	$to = "$to" & "$mask";

	if ($bits == 128)
	{
	    use Math::BigInt;

	    my $n = new Math::BigInt 0;
	    my $t = new Math::BigInt 0;
	    my $u = new Math::BigInt 0;
	    my $x = '';

	    for (0 .. 15)
	    {
		vec($num, $_, 8) = _ones 8;
		vec($num, $_, 8) ^= vec($mask, $_, 8);
		$n <<= 8;
		$t <<= 8;
		$u <<= 8;
		$n |= vec($net, $_, 8);
		$t |= vec($to, $_, 8);
		$u |= vec($num, $_, 8);
	    }

#    	    warn "# splitref $self $mask\n";
#      	    warn "# net = ", $self->network, "\n";
#      	    warn "# bro = ", $self->broadcast, "\n";

#      	    warn "# before, n = $n\n";
#      	    warn "# before, t = $t\n";
#      	    warn "# before, u = $u\n";

	    $u++;
	    my $i = $n->copy;

	    do {
		
		my $j = $i->copy;

#      		warn "# i = $i\n";
#      		warn "# j = $j\n";
#      		warn "# n = $n\n";
#      		warn "# u = $u\n";
#      		warn "# t = $t\n";
#      		warn "###\n";

		for (reverse 0 .. 15)
		{
		    vec($v, $_, 8) = ($j & 0xFF);
		    $j >>= 8;
		}

		push @ret, $self->_fnew([ $v, $mask, $bits ]);
#		warn "# add ", $self->_fnew([$v, $mask, $bits]), "\n";
		$i += $u;
	    } while ($i <= $t);
	}
	else
	{
	    vec($num, 0, $bits) = _ones $bits;
	    vec($num, 0, $bits) ^= vec($mask, 0, $bits);
	    vec($num, 0, $bits) ++;

	    for (my $i	= vec($net, 0, $bits);
		 $i 	<= vec($to, 0, $bits);
		 $i 	+= vec($num, 0, $bits))
	    {
		vec($v, 0, $bits) = $i;
		push @ret, $self->_fnew([ $v, $mask, $bits ]);
	    }
	}
    }

    return \@ret;
}

=pod

=item C<-E<gt>hostenum()>

Returns the list of hosts within a subnet.

=cut

sub hostenum ($) {
    return @{$_[0]->hostenumref};
}

=pod

=item C<-E<gt>hostenumref()>

Faster version of C<-E<gt>hostenum()>, returning a reference to a list.

=cut

sub hostenumref ($) {
    my $r = $_[0]->splitref(32);
    if ($_[0]->mask ne '255.255.255.255') {
	splice(@$r, 0, 1);
	splice(@$r, scalar @$r - 1, 1);
    }
    return $r;
}

=pod

=item C<$me-E<gt>compact($addr1, $addr2, ...)>

Given a list of objects (including C<$me>), this method will compact
all the addresses and subnets into the largest (ie, least specific) 
subnets possible that contain exactly all of the given objects.

Note that in versions prior to 3.02, if fed with the same IP subnets 
multiple times, these subnets would be returned. From 3.02 on, a more
"correct" approach has been adopted and only one address would be
returned.

Note that C<$me> and all C<$addr>-n must be C<NetAddr::IP> objects.

=cut

sub compact {
    return @{compactref(\@_)};
}

*Compact = \&compact;

=pod

=item C<$me-E<gt>compactref(\@list)>

As usual, a faster version of =item C<-E<gt>compact()> that returns a
reference to a list. Note that this method takes a reference to a list
instead.

Note that C<$me> must be a C<NetAddr::IP> object.

=cut

sub compactref ($) {
    my @addr = sort @{$_[0]} 
    or return [];

    my $bits = $addr[0]->{bits};
    my $changed;

    do {
	$changed = 0;
	for (my $i = 0;
	     $i <= $#addr - 1;
	     $i ++)
	{
	    my $lip = $addr[$i];
	    my $hip = $addr[$i + 1];

	    if ($lip->contains($hip)) {
		splice(@addr, $i + 1, 1);
		++ $changed;
		-- $i;
	    }
	    elsif (vec($lip->{mask}, 0, $bits) 
		   == vec($hip->{mask}, 0, $bits)) 
	    {
		my $la = $lip->{addr};
		my $ha = $hip->{addr};
		my $nb = '';
		my $na = '';
		my $nm = '';

		vec($nb, 0, $bits) = 
		    vec($na, 0, $bits) = 
			vec($la, 0, $bits);
		vec($nb, 0, $bits) ^= vec($ha, 0, $bits);
		vec($na, 0, $bits) ^= vec($nb, 0, $bits);
		vec($nm, 0, $bits) = vec($lip->{mask}, 0, $bits);
		vec($nm, 0, $bits) <<= 1;

		if (("$la" & "$nm") eq ("$ha" & "$nm"))
		{
		    if ("$la" eq "$ha") {
			splice(@addr, $i + 1, 1);
		    }
		    else {
			$addr[$i] = ($lip->_fnew([ "$na" & "$nm", 
						   $nm, $bits ]));
			splice(@addr, $i + 1, 1);
		    }

		    -- $i;
		    ++ $changed;
		}
	    }
	}
    } while ($changed);

    return \@addr;
}

=pod

=item C<-E<gt>first()>

Returns a new object representing the first useable IP address within
the subnet (ie, the first host address).

=cut

sub first ($) {
    my $self	= shift;

    return $self->network + 1;
}

=pod

=item C<-E<gt>last()>

Returns a new object representing the last useable IP address within
the subnet (ie, one less than the broadcast address).

=cut

sub last ($) {
    my $self	= shift;

    return $self if $self->masklen == $self->{bits};

    return $self->broadcast - 1;
}

=pod

=item C<-E<gt>nth($index)>

Returns a new object representing the I<n>-th useable IP address within
the subnet (ie, the I<n>-th host address).  If no address is available
(for example, when the network is too small for C<$index> hosts),
C<undef> is returned.

=cut

sub nth ($$) {
    my $self    = shift;
    my $count   = shift;

    return undef if ($count < 1 or $count > $self->num ());
    return $self->network + $count;
}

=pod

=item C<-E<gt>num()>

Returns the number of useable addresses IP addresses within the
subnet, not counting the broadcast address.

=cut

sub num ($) {
    my $self	= shift;
    return ~vec($self->{mask}, 0, $self->{bits}) & 0xFFFFFFFF;
}

				# Output a vec() as a dotted-quad

1;

__END__

=back

=head2 EXPORT

None by default.


=head1 HISTORY

$Id: IP.pm,v 1.24 2004/10/11 15:40:29 lem Exp $

=over

=item 0.01

=over


=item *

original  version;  Basic testing  and  release  to CPAN  as
version 0.01. This is considered beta software.

=back


=item 0.02

=over


=item *

Multiple changes  to fix endiannes issues. This  code is now
moderately tested on Wintel and Sun/Solaris boxes.

=back


=item 0.03

=over


=item *

Added -E<gt>first and -E<gt>last methods. Version changed to 0.03.

=back


=item 1.00

=over


=item *

Implemented -E<gt>new_subnet. Version changed to 1.00.

=item *

less croak()ing when improper input  is fed to the module. A
more consistent 'undef' is returned now instead to allow the
user to better handle the error.

=back


=item 1.10

=over


=item *

As  per  Marnix   A.   Van  Ammers  [mav6@ns02.comp.pge.com]
suggestion, changed  the syntax of the loop  in host_enum to
be the same of the enum method.

=item *

Fixed the MS-DOS ^M  at the end-of-line problem. This should
make the module easier to use for *nix users.

=back


=item 1.20

=over


=item *

Implemented -E<gt>compact and -E<gt>expand methods.

=item *

Applying for official name

=back


=item 1.21

=over


=item *

Added  -E<gt>addr_number and  -E<gt>mask_bits.  Currently  we return
normal  numbers (not  BigInts).   Please test  this in  your
platform and report any problems!

=back


=item 2.00

=over


=item *

Released under the new *official* name of NetAddr::IP

=back


=item 2.10

=over


=item *

Added support for -E<gt>new($min, $max, $bits) form

=item *

Added -E<gt>to_numeric. This helps serializing objects

=back


=item 2.20

=over


=item *

Chris Dowling  reported that  the sort method  introduced in
v1.20  for -E<gt>expand  and -E<gt>compact  doesn't always  return a
number under perl versions < 5.6.0.  His fix was applied and
redistributed.  Thanks Chris!

=item *

This module is hopefully released with no CR-LF issues!

=item *

Fixed a warning about uninitialized values during make test

=back


=item 2.21

=over


=item *

Dennis  Boylan pointed  out a  bug under  Linux  and perhaps
other platforms  as well causing the  error "Sort subroutine
didn't         return         single        value         at
/usr/lib/perl5/site_perl/5.6.0/NetAddr/IP.pm  line  299,  E<lt>E<gt>
line 2." or similar. This was fixed.

=back


=item 2.22

=over


=item *

Some changes  suggested by Jeroen Ruigrok  and Anton Berezin
were included. Thanks guys!

=back


=item 2.23

=over


=item *

Bug fix for /XXX.XXX.XXX.XXX netmasks under v5.6.1 suggested
by Tim Wuyts. Thanks!

=item *

Tested the module under MACHTYPE=hppa1.0-hp-hpux11.00. It is
now  konwn to  work  under Linux  (Intel/AMD), Digital  Unix
(Alpha),   Solaris  (Sun),  HP-UX11   (HP-PA-RISC),  Windows
9x/NT/2K (using ActiveState on Intel).

=back


=item 2.24

=over


=item *

A spurious  warning when  expand()ing with -w  under certain
circumstances  was removed. This  involved using  /31s, /32s
and the same netmask as the input.  Thanks to Elie Rosenblum
for pointing it out.

=item *

Slight change  in license terms to ease  redistribution as a
Debian package.

=back


=item 3.00

This is  a major rewrite, supposed  to fix a number  of issues pointed
out in earlier versions.

The goals for this version include getting rid of BigInts, speeding up
and also  cleaning up the code,  which is written in  a modular enough
way so  as to allow IPv6  functionality in the  future, taking benefit
from most of the methods.

Note that no effort has  been made to remain backwards compatible with
earlier versions. In particular, certain semantics of the earlier
versions have been removed in favor of faster performance.

This  version  was tested  under  Win98/2K (ActiveState  5.6.0/5.6.1),
HP-UX11 on PA-RISC (5.6.0), RedHat  Linux 6.2 (5.6.0), Digital Unix on
Alpha (5.6.0), Solaris on Sparc (5.6.0) and possibly others.

=item 3.01

=over

=item * 

Added C<-E<gt>numeric()>.

=item *

C<-E<gt>new()> called with no parameters creates a B<default>
NetAddr::IP object.

=back

=item 3.02

=over

=item *

Fxed C<-E<gt>compact()> for cases of equal subnets or
mutually-contained IP addresses as pointed out by Peter Wirdemo. Note
that now only distinct IP addresses will be returned by this method.

=item *

Fixed the docs as suggested by Thomas Linden.

=item *

Introduced overloading to ease certain common operations.

=item *

    Fixed compatibility issue with C<-E<gt>num()> on 64-bit processors.

=back

=item 3.03

=over

=item *

Added more comparison operators.

=item *

As per Peter Wirdemo's suggestion, added C<-E<gt>wildcard()> for
producing subnets in wildcard format.

=item *

Added C<++> and C<+> to provide for efficient iteration operations
over all the hosts of a subnet without C<-E<gt>expand()>ing it.

=back

=item 3.04

=over

=item *

Got rid of C<croak()> when invalid input was fed to C<-E<gt>new()>.

=item *

As suggested by Andrew Gaskill, added support for prefix
notation. Thanks for the code of the initial C<-E<gt>prefix()>
function.

=back

=item 3.05

=over

=item *

Added support for range notation, where base and broadcast addresses
are given as arguments to C<-E<gt>new()>.

=back

=item 3.06

=over

=item *

Andrew Ruthven pointed out a bug related to proper interpretation of
"compact" CIDR blocks. This was fixed. Thanks!

=back

=item 3.07

=over

=item *

Sami Pohto pointed out a bug with C<-E<gt>last()>. This was fixed.

=item *

A small bug related to parsing of 'localhost' was fixed.

=back

=item 3.08

=over

=item *

By popular request, C<-E<gt>new()> now checks the sanity of the netmasks
it receives. If the netmask is invalid, C<undef> will be returned.

=back

=item 3.09

=over

=item *

Fixed typo that invalidated otherwise correct masks. This bug appeared in 3.08.

=back

=item 3.10

=over

=item *

Fixed relops. Semantics where adjusted to remove the netmask from the
comparison. (ie, it does not make sense to say that 10.0.0.0/24 is >
10.0.0.0/16 or viceversa).

=back

=item 3.11

=over

=item *

Thanks to David D. Zuhn for contributing the C<-E<gt>nth()> method.

=item *

tutorial.htm now included in the  distribution. I hope this helps some
people to better  understand what kind of stuff can  be done with this
module.

=item *

C<'any'> can be used as a synonim of C<'default'>. Also, C<'host'> is
now a valid (/32) netmask.

=back

=item 3.12

=over

=item *

Added CVS control files, though this is of no relevance to the community.

=item *

Thanks to Steve Snodgrass for pointing out a bug in the processing of
the special names such as default, any, etc. A fix was produced and
adequate tests were added to the code.

=item *

First steps towards "regexp free" parsing.

=item *

Documentation revisited and reorganized within the file, so that it
helps document the code.

=item *

Added C<-E<gt>aton()> and support for this format in
C<-E<gt>new()>. This makes the code helpful to interface with
old-style socket code.

=back

=item 3.13

=over

=item *

Fixes a warning related to 'wrapping', introduced in 3.12 in
C<pack()>/C<unpack()> for the new support for C<-E<gt>aton()>.

=back

=item 3.14

=over

=item *

C<Socket::gethostbyaddr> in Solaris seems to behave a bit different
from other OSes. Reversed change in 3.13 and added code around this
difference.

=back

=item 3.14_1

This is an interim release just to incorporate the v6 patches
contributed.  No extensive testing has been done with this support
yet. More tests are needed.

=over

=item *

Preliminary support for IPv6 contributed by Kadlecsik Jozsi
E<lt>kadlec at sunserv.kfki.huE<gt>. Thanks a lot!

=item *

IP.pm and other files are enconded in ISO-8859-1 (Latin1) so that I
can spell my name properly.

=item *

Tested under Perl 5.8.0, no surprises found.

=back

=item 3.14_2

Minor development release.

=over

=item *

Added C<-E<gt>version> and C<-E<gt>bits>, including testing.

=item *

C<Compact> can now be exported if the user so requests.

=item *

Fixed a bug when octets in a dotted quad were > 256 (ie, were not
octets). Thanks to Anton Berezin for pointing this out.

=back

=item 3.14_3

Fixed a bug pointed out by Brent Imhoff related to the implicit
comparison that happens within C<Compact()>. The netmask was being
ignored in the comparison (ie, 10/8 was considered the same as
10.0/16). Since some people have requested that 10.0/16 was considered
larger than 10/8, I added this change, which makes the bug go
away. This will be the last '_' release, pending new bugs.

Regarding the comparison of subnets, I'm still open to debate so as to
wether 10.0/16 > 10/8. Certainly 255.255.0.0 > 255.0.0.0, but 2 ** 24
are more hosts than 2 ** 16. I think we might use gt & friends for
this semantic and make everyone happy, but I won't do anything else
here without (significant) feedback.

=item 3.14_4

As noted by Michael, 127/8 should be 127.0.0.0/8 and not
0.0.0.128/8. Also, improved docs on the usage of contains() and
friends.

=item 3.15

Finally. Added POD tests (and fixed minor doc bug in IP.pm). As
reported by Anand Vijay, negative numbers are assumed to be signed
ints and converted accordingly to a v4 address. split() and nth() now
work with IPv6 addresses (Thanks to Venkata Pingali for
reporting). Tests were added for v6 base functionality and
splitting. Also tests for bitwise aritmethic with long integers has
been added. I'm afraid Math::BigInt is now required.

Note that IPv6 might not be as solid as I would like. Be careful...

=item 3.16

Fixed a couple of (minor) bugs in shipped tests in the last
version. Also, fixed a small pod typo that caused code to show up in
the documentation.

=item 3.17

Fixed IP.pm so that all test could pass in Solaris machines. Thanks to
all who reported this.

=item 3.18

Fixed some bugs pointed out by David Lloyd, having to do with the
module packaging and version requirements. Thanks David!

=item 3.19

Fixed a bug pointed out by Andrew D. Clark, regarding proper parsing
of IP ranges with non-contiguous masks. Thanks Andrew!

=item 3.20

Suggestion by Reuland Olivier gave birth to C<short()>, which provides
for a compact representation of the IP address. Rewrote C<_compact> to
find the longest sequence of zeros to compact. Reuland also pointed
out a flaw in contains() and within(), which was fixed. Thanks
Reuland!

Fixed rt bug #5478 in t/00-load.t.

=item 3.21

Fixed minor v-string problem pointed out by Steve Snodgrass (Thanks
Steve!). NetAddr::IP can now collaborate with Storable to serialize
itself.

=back

=head1 AUTHOR

Luis E. Muñoz <luismunoz@cpan.org>

=head1 WARRANTY

This software comes with the  same warranty as perl itself (ie, none),
so by using it you accept any and all the liability.

=head1 LICENSE

This software is (c) Luis E. Muñoz.  It can be used under the terms of
the perl artistic license provided  that proper credit for the work of
the  author is  preserved in  the form  of this  copyright  notice and
license for this module.

=head1 SEE ALSO

perl(1).

=cut

