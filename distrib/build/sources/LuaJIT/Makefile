# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = LuaJIT
VERSION = 2.0.5

BASE_URL = http://luajit.org/download

CONFIGURE = yes
configure: patch
	true

COMPILE = yes
compile: configure
	$(MAKE) ${JOBS} PREFIX=/usr -C $(COMPILE_DIR)

INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)
	$(MAKE) DESTDIR=$(PKG_ROOT) PREFIX=/usr -C $(COMPILE_DIR) install

include ../Makefile.rules
