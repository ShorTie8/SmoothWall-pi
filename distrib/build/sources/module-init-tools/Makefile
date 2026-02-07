# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = module-init-tools
VERSION = 3.15
EXTENSION = .tar.xz

BASE_URL = http://www.kernel.org/pub/linux/utils/kernel/module-init-tools

PKG_DIR =

PRE_CONFIGURE = DOCBOOKTOMAN=/bin/true

CFLAGS += -std=gnu17

CONFIG_OPTS += --datarootdir=/usr/share

ifeq ($(mARCH), aarch64)
#ReConfigure = yes
CONFIGURE = yes
configure: $(DIR)/
	@echo; echo; echo "Configure"; echo
	@(cd $(DIR); \
		cd $(DIR); aclocal -I m4; \
		automake --add-missing --copy; \
		autoconf; \
		./config --prefix=$(PKG_DIR)
endif

include ../Makefile.rules
