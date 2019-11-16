# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = slang
VER_MM = 2.3
VERSION = $(VER_MM).2

EXTENSION = .tar.bz2
BASE_URL = https://www.jedsoft.org/releases/slang

INSTALL = yes

install: compile
ifeq ($(BUILD_PHASE), Final)
	@mkdir -p $(PKG_ROOT)
endif
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@make -C $(COMPILE_DIR) DESTDIR=/ install
	@rm -f $(PKG_ROOT)$(PKG_DIR)/lib/libsnewt*.so*

include ../Makefile.rules
