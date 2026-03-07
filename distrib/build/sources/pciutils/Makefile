# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = pciutils
VERSION = 3.14.0
BASE_URL = https://github.com/pciutils/pciutils/releases/download/v$(VERSION)

COMPILE = yes
compile: $(DIR)/
	@$(MAKE) $(JOBS) -C $(COMPILE_DIR) PREFIX=/$(PKG_DIR)

include ../Makefile.rules
