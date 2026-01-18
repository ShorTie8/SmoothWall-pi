# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = whois
VERSION = 5.6.5
TARBALL = v$(VERSION)
BASE_URL = https://github.com/rfc1036/whois/archive/refs/tags/v5.6.5.tar.gz

CONFIGURE = yes
configure: $(DIR)/
	@true
	
INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@install -D $(DIR)/whois $(PKG_ROOT)/usr/bin/whois
	@install -D $(DIR)/tld.conf $(PKG_ROOT)/etc/whois/tld.conf
	@install -D $(DIR)/sd.conf $(PKG_ROOT)/etc/whois/sd.conf
	
include ../Makefile.rules
