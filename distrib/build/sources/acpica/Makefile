# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = acpica
VERSION = unix2-20140325

BASE_URL = https://acpica.org/sites/acpica/files/

export NO_CHECK_CERT

CONFIGURE = yes
configure: $(DIR)/
	true

COMPILE = yes
compile: configure
	$(MAKE) $(JOBS) -C $(COMPILE_DIR)/generate/unix

INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)$(PKG_DIR)/bin
	$(MAKE) INSTALLDIR=$(PKG_ROOT)$(PKG_DIR)/bin install -C $(COMPILE_DIR)/generate/unix

include ../Makefile.rules
