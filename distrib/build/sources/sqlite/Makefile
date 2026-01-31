# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = sqlite-autoconf
VERSION = 3510200

BASE_URL = http://www.sqlite.org/2026

#CONFIG_OPTS = --enable-threadsafe \
 #              LIBS=-ltinfo LDFLAGS=-ltinfo

CONFIG_OPTS = --prefix=/usr \
			--disable-static \
			--enable-fts{4,5} \
			CPPFLAGS="-D SQLITE_ENABLE_COLUMN_METADATA=1 \
			-D SQLITE_ENABLE_UNLOCK_NOTIFY=1 \
			-D SQLITE_ENABLE_DBSTAT_VTAB=1 \
			-D SQLITE_SECURE_DELETE=1"

include ../Makefile.rules
