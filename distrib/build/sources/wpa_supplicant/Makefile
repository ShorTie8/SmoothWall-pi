# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = wpa_supplicant
VERSION = 2.6

BASE_URL = https://w1.fi/releases

PATCH_FILE1 = wpa_supplicant-2.6-upstream_fixes-1.patch

CONFIGURE = yes

configure: $(DIR)/
	cd $(DIR)/wpa_supplicant; cp ../../default.config .config

COMPILE = yes
compile: configure
	@cd $(DIR)/wpa_supplicant; $(MAKE) $(JOBS) BINDIR=/sbin LIBDIR=/lib

INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)
	cd $(PKG_ROOT); install -dv sbin usr/share/man/man{5,8}
	install -D -v -m755 $(DIR)/wpa_supplicant/wpa_{cli,passphrase,supplicant} $(PKG_ROOT)/sbin/; \
	install -D -v -m644 $(DIR)/wpa_supplicant/doc/docbook/wpa_supplicant.conf.5 $(PKG_ROOT)/usr/share/man/man5/; \
	install -D -v -m644 $(DIR)/wpa_supplicant/doc/docbook/wpa_{cli,passphrase,supplicant}.8 $(PKG_ROOT)/usr/share/man/man8/

include ../Makefile.rules
