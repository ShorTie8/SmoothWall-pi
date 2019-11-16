# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2016
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = dtc
VERSION = 1.4.0

BASE_URL = https://git.kernel.org/pub/scm/utils/dtc/dtc.git/snapshot

CONFIGURE = yes
configure: patch
	cd $(DIR); patch < ../Makefile.patch

COMPILE = yes
compile: configure
	@echo; echo; echo "compile"; echo
	make $(JOBS) -C $(DIR) DESTDIR=/usr

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -p $(PKG_ROOT)
	$(MAKE) -C $(DIR) DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
