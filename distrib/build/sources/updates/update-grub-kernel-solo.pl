#! /usr/bin/perl

# Copyright Neal P. Murphy, July 2015
#
# This program is licensed under the terms of the GNU Public License, version 2.

# Use this script when updating pkgs that work only with the new kernel.

# Grab the new kernel version from the command line
my ($newkern) = @ARGV;
shift @ARGV;

# Open the grub conf files
open presentConf, "</boot/grub/grub.conf";
open newConf, ">/boot/grub/newkernel.conf";

# Dump the first lines to each destination
while ((<presentConf>))
{
  print newConf;

  # Only down to the 'background' line
  last if ($_ =~ /^background=.*/);
}

# Do the rest of the lines
while ((<presentConf>))
{
  # If it's present, forget the previous 'old kernel'; we only do two.
  last if ($_ =~ /^## Old Kernel/);

  $newLine = $_;

  # Adjust for the new kernel
  $newLine =~ s/vmlinuz-[^ ]+/vmlinuz-$newkern/g;
  $newLine =~ s/initrd-[^ ]+\.gz/initrd-$newkern\.gz/g;
  print newConf $newLine;

}

# Close so it can be replaced
close(newConf);
close(presentConf);

rename "/boot/grub/newkernel.conf", "/boot/grub/grub.conf";
chmod 644, "/boot/grub/grub.conf";
if (-f "/boot/grub/oldkernel.conf") { unlink "/boot/grub/oldkernel.conf"; }
