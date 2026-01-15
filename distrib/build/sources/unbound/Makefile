# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = unbound
VERSION = 1.24.2

BASE_URL = https://nlnetlabs.nl/downloads/unbound

CONFIG_OPTS += --prefix=/usr \
	       --sysconfdir=/etc \
	       --disable-static \
	       --with-pidfile=/var/run/unbound.pid

include ../Makefile.rules
