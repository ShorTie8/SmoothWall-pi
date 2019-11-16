# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = procinfo-ng
VERSION = 2.0.304

BASE_URL = http://sourceforge.net/projects/$(PACKAGE)/files/$(PACKAGE)/$(VERSION)
EXTENSION = .tar.bz2

COMPILE = yes
INSTALL = yes

compile: configure
	@cd $(COMPILE_DIR); sed -i -e 's/-lncurses/-lncurses -ltinfo/' Makefile
	@$(MAKE) $(JOBS) -C $(COMPILE_DIR)

install: compile
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) -C $(COMPILE_DIR) prefix=$(PKG_ROOT)$(PKG_DIR) install
	
include ../Makefile.rules
