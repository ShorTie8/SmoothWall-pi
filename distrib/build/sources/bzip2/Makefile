# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = bzip2
VERSION = 1.0.6

BASE_URL = https://sourceforge.net/projects/bzip2/files

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

PATCH_FILE1 = prefix-symlinks.patch

configure : patch
	@true

compile : configure
	@make -C $(DIR) CC="gcc $(CFLAGS)"

install : compile
	@make -C $(DIR) PREFIX=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules

