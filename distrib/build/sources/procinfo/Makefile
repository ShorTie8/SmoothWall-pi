# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = procinfo
VERSION = 18

BASE_URL = http://www.kozmix.org/src/

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: $(DIR)/
	@true
	
compile: configure
	@$(MAKE) $(JOBS) -C $(COMPILE_DIR) LDLIBS=-ltinfo

install: compile
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) -C $(COMPILE_DIR) prefix=$(PKG_ROOT)$(PKG_DIR) install
	
include ../Makefile.rules
