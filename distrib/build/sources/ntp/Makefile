# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ntp
VERSION = 4_2_8P18
TARBALL = NTP_$(VERSION)
DIR =  ntp-$(TARBALL)
BASE_URL = https://github.com/ntp-project/ntp/archive/refs/tags

CONFIG_OPTS += --prefix=${PKG_DIR} --sysconfdir=/etc \
		--with-binsubdir=sbin --with-lineeditlibs=readline LIBS=-ltinfo

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	(cd $(DIR); ./bootstrap)
	(cd $(DIR); ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@install -D $(COMPILE_DIR)/ntpdate/ntpdate $(PKG_ROOT)/usr/sbin/ntpdate 
	@install -D $(COMPILE_DIR)/ntpq/ntpq $(PKG_ROOT)/usr/sbin/ntpq 

include ../Makefile.rules
