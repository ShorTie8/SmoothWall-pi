# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = shadow
#VERSION = 4.1.4.2
VERSION = 4.7
EXTENSION = .tar.xz

#BASE_URL = http://downloads.smoothwall.org/buildmirror
BASE_URL = https://github.com/shadow-maint/shadow/releases/download/4.7

INSTALL = yes

CONFIG_OPTS= --with-selinux=no

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@rm -f $(PKG_ROOT)/bin/sg $(PKG_ROOT)/bin/vigr

include ../Makefile.rules
