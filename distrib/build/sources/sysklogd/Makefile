# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = sysklogd
VERSION = 2.7.2

BASE_URL = https://github.com/troglobit/sysklogd/releases/download/v2.7.2

COMPILE = yes
compile: configure
	@make $(JOBS) -C $(DIR) V=1 SKFLAGS="$(CFLAGS) -DSYSV -D_GNU_SOURCE"

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/man/man{5,8} $(PKG_ROOT)$(PKG_DIR)/sbin
	@make -C $(COMPILE_DIR) MANDIR=$(PKG_ROOT)$(PKG_DIR)/man \
		BINDIR=$(PKG_ROOT)$(PKG_DIR)/sbin install

include ../Makefile.rules
