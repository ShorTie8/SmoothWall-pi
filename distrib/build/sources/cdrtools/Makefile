# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = cdrtools
VERSION = 3.00

BASE_URL = http://downloads.smoothwall.org/buildmirror

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: $(DIR)/
	@true

compile: configure
	@$(MAKE) $(JOBS) -C $(COMPILE_DIR)

install: compile
	@mkdir -p $(PKG_ROOT)
	@install -D $(COMPILE_DIR)/mkisofs/OBJ/*/mkisofs $(PKG_ROOT)/sbin/mkisofs
	@install -D $(COMPILE_DIR)/cdrecord/OBJ/*/cdrecord $(PKG_ROOT)/sbin/cdrecord

include ../Makefile.rules
