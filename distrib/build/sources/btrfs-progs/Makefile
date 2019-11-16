# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = btrfs-progs
VERSION = v4.15.1
EXTENSION = .tar.xz

BASE_URL = https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs

# PRECONFIGURE = ZSTD_CFLAGS=/usr/local ZSTD_LIBS=/usr/local/lib

CONFIG_OPTS += \
	PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" \
	--disable-convert \
	--disable-documentation
#		--bindir=/bin \
#		--libdir=/lib \
#	ZSTD_CFLAGS="" \
#	ZSTD_LIBS="-llibzstd" \
		

CONFIGURE = yes
configure: patch
	#(cd $(COMPILE_DIR); ./autogen.sh)
	(cd $(COMPILE_DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure $(CONFIG_OPTS))

include ../Makefile.rules
