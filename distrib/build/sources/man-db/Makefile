# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = man-db
VERSION = 2.13.1
EXTENSION = .tar.xz
BASE_URL = https://download.savannah.gnu.org/releases/man-db

CONFIG_OPTS += \
		--docdir=/usr/share/doc/man-db-$(VERSION) \
		--sysconfdir=/etc \
		--disable-setuid \
		--enable-cache-owner=bin \
		--with-browser=/usr/bin/lynx \
		--with-vgrind=/usr/bin/vgrind \
		--with-grap=/usr/bin/grap \
		--with-systemdtmpfilesdir= \
		--with-systemdsystemunitdir=

include ../Makefile.rules
