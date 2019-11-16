# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = man-pages
VERSION = 3.65

EXTENSION = .tar.xz

BASE_URL = https://www.kernel.org/pub/linux/docs/man-pages/

INSTALL = yes

install: patch
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)
	@$(MAKE) -C $(DIR) prefix=$(PKG_ROOT)$(PKG_DIR) install

include ../Makefile.rules
