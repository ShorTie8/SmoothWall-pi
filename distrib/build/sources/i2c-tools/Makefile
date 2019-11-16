# SmoothWall Build system.
#
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = i2c-tools
VERSION = 4.1
BASE_URL = https://mirrors.edge.kernel.org/pub/software/utils/i2c-tools

COMPILE = yes
compile: patch
	@echo; echo; echo "compile"; echo
	make $(JOBS) PREFIX= -C $(DIR)

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)
	make PREFIX= -C $(DIR) DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
