# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = patch
VERSION = 2.7.5

BASE_URL = ftp://ftp.gnu.org/gnu/patch

ifeq ($(BUILD_PHASE), Stage_3)
CONFIG_OPTS += --prefix=$(TOOLS_DIR)
endif

INSTALL = yes

install: compile
ifeq ($(BUILD_PHASE), Stage_3)
	@$(MAKE) -C $(COMPILE_DIR) install
else
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
endif

include ../Makefile.rules
