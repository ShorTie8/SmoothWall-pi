# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = iputils
VERSION = s20100214

BASE_URL = http://www.skbuff.net/iputils

EXTENSION=.tar.bz2


CONFIGURE = yes
INSTALL = yes

configure: patch
	sed -i -e 's/^\(DEFINES.*\)/\1$(CFLAGS)/' $(DIR)/Makefile

install: compile
	@mkdir -p $(PKG_ROOT)
	@install -m 4755 -D $(DIR)/ping $(PKG_ROOT)$(PKG_DIR)/bin/ping

include ../Makefile.rules
