# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = shadow
VERSION = 4.18.0
EXTENSION = .tar.xz
BASE_URL = https://github.com/shadow-maint/shadow/releases/download/$(VERSION)

CONFIG_OPTS= --without-libbsd --with-selinux=no

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@rm -f $(PKG_ROOT)/bin/sg $(PKG_ROOT)/bin/vigr

include ../Makefile.rules
