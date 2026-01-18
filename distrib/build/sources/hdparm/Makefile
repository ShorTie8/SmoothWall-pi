# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = hdparm
VERSION = 9.56

BASE_URL = http://sourceforge.net/projects/hdparm/files/hdparm/

CONFIGURE = yes
configure: patch
	@true

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)/sbin
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
