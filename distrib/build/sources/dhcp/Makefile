# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = dhcp
VERSION = 4.1-ESV-R13

BASE_URL = ftp://ftp.isc.org/isc/dhcp/$(VERSION/$(VERSION)

PRE_CONFIGURE = CFLAGS="-Wno-error $(CFLAGS)"

CONFIGURE = yes
INSTALL = yes

configure: patch
	@(cd $(COMPILE_DIR); $(PRE_CONFIGURE) ./configure);
	@echo >>$(COMPILE_DIR)/includes/site.h "#define _PATH_DHCPD_DB \"/usr/etc/dhcpd.leases\""
	@echo >>$(COMPILE_DIR)/includes/site.h "#define _PATH_DHCPD_CONF \"/usr/etc/dhcpd.conf\""

install: compile
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/etc
	@touch $(PKG_ROOT)$(PKG_DIR)/etc/dhcpd.leases
	@install -D $(COMPILE_DIR)/server/dhcpd $(PKG_ROOT)$(PKG_DIR)/sbin/dhcpd
	@install -D $(COMPILE_DIR)/relay/dhcrelay $(PKG_ROOT)$(PKG_DIR)/sbin/dhcrelay

	
include ../Makefile.rules
