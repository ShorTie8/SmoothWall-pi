# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = sysklogd
VERSION = 1.5.1

BASE_URL = http://www.infodrom.org/projects/sysklogd/download/

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@true
	# fix problems that causes a segmentation fault under some conditions in klogd and fix an obsolete program construct:
	cd $(DIR); sed -i '/Error loading kernel symbols/{n;n;d}' ksym_mod.c
	cd $(DIR); sed -i 's/union wait/int/' syslogd.c

compile: configure
	@make $(JOBS) -C $(DIR) V=1 SKFLAGS="$(CFLAGS) -DSYSV -D_GNU_SOURCE"

install: compile
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/man/man{5,8} $(PKG_ROOT)$(PKG_DIR)/sbin
	@make -C $(COMPILE_DIR) MANDIR=$(PKG_ROOT)$(PKG_DIR)/man \
		BINDIR=$(PKG_ROOT)$(PKG_DIR)/sbin install

include ../Makefile.rules
