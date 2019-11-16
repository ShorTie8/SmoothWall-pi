# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = reiserfsprogs
VERSION = 3.6.24
EXTENSION = .tar.xz
BASE_URL = https://www.kernel.org/pub/linux/kernel/people/jeffm/reiserfsprogs/v$(VERSION)

ifeq ($(BUILD_PHASE), Final)

CFLAGS += -std=gnu89
CONFIG_OPTS = --prefix=/usr --sbindir=/sbin

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	ln -sf reiserfsck $(PKG_ROOT)/sbin/fsck.reiserfs
	ln -sf mkreiserfs $(PKG_ROOT)/sbin/mkfs.reiserfs
endif
	
include ../Makefile.rules
