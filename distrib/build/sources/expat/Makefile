# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = expat
VERSION = 2.2.7

BASE_URL = https://sourceforge.net/projects/expat/files/expat/$(VERSION)

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) install DESTDIR=$(PKG_ROOT)

include ../Makefile.rules
