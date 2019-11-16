# Copyright 2004-2013 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = busybox
VERSION = 1.20.2

BASE_URL = http://busybox.net/downloads/
EXTENSION = .tar.bz2

LICENCE_FILE = $(DIR)/LICENSE

PKG_DIR = /opt/busybox

PATCH_FILE1 = libbb.h.patch

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@cp -avR config $(COMPILE_DIR)/.config
#	@$(MAKE) $(JOBS) -C $(DIR) oldconfig

compile: configure
	+$(MAKE) ${JOBS} -C $(COMPILE_DIR) V=1

install: compile
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) $(JOBS) -C $(COMPILE_DIR) CONFIG_PREFIX=$(PKG_ROOT)$(PKG_DIR) install
	@for I in $$($(PKG_ROOT)$(PKG_DIR)/bin/busybox --list); do \
	    ln -svf busybox $(PKG_ROOT)$(PKG_DIR)/bin/$$I; done

include ../Makefile.rules
