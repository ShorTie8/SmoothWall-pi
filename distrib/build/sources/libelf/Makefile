# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libelf
VERSION = 0.174
EXTENSION = .tar.bz2

TARBALL = elfutils-$(VERSION)

DIR = elfutils-$(VERSION)


# https://gcc.gnu.org/pub/elfutils/0.173/elfutils-0.173.tar.bz2
BASE_URL = https://gcc.gnu.org/pub/elfutils/$(VERSION)

INSTALL = yes
install: compile
	@echo; echo; echo "install"
	$(MAKE) -C $(DIR)/libelf DESTDIR=$(PKG_ROOT) install
	@echo
	mkdir -vp $(PKG_ROOT)/usr/lib/pkgconfig
	install -vm644 $(DIR)/config/libelf.pc $(PKG_ROOT)/usr/lib/pkgconfig

include ../Makefile.rules
