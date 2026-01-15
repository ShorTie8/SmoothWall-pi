# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = pkg-config
VERSION =  0.29.2
BASE_URL = http://pkgconfig.freedesktop.org/releases

# Fix build with GCC 15
CFLAGS += -std=gnu17

CONFIG_OPTS += --with-internal-glib --disable-host-tool \
			--docdir=/usr/share/doc/pkg-config-$(VERSION)

include ../Makefile.rules
