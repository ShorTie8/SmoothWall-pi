# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = pcmciautils
VERSION = 018
EXTENSION=.tar.bz2

DIR = $(PACKAGE)-$(VERSION)

#BASE_URL = http://www.kernel.org/pub/linux/utils/kernel/pcmcia
#NOTE: As of 04/07/2012, only versions through 009 were available at the above link.
BASE_URL = http://pkgs.fedoraproject.org/repo/pkgs/$(PACKAGE)/$(PACKAGE)-$(VERSION)$(EXTENSION)/5d85669b3440baa4532363da6caaf1b4

CONFIGURE = yes
configure: $(DIR)/
	@true

export V = 1

include ../Makefile.rules
