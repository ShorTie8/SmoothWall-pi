# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = dnsmasq
VERSION =  2.92
BASE_URL = http://www.thekelleys.org.uk/dnsmasq/

CONFIGURE = yes
configure: $(DIR)/
	@true

COMPILE = yes
compile: configure
	@$(MAKE) $(JOBS) -C $(DIR) CFLAGS="$(CFLAGS) -DHAVE_ISC_READER"

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@cd $(DIR); \
        install -s -D src/dnsmasq $(PKG_ROOT)$(PKG_DIR)/bin/dnsmasq;

include ../Makefile.rules
