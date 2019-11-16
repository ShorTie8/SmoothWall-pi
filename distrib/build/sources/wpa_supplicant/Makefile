# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = wpa_supplicant
#VERSION = 2.6
#VERSION = 2.7
VERSION = 2.9

BASE_URL = https://w1.fi/releases

#PATCH_FILE1 = wpa_supplicant-2.6-upstream_fixes-2.patch
#PATCH_URL1 = http://www.linuxfromscratch.org/patches/blfs/8.3/$(PATCH_FILE1)

CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	cd $(DIR)/wpa_supplicant; cp -v ../../default.config .config

COMPILE = yes
compile: configure
	@echo; echo; echo "compile"; echo
	cd $(DIR)/wpa_supplicant; $(MAKE) $(JOBS) BINDIR=/sbin LIBDIR=/lib

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)/etc/wpa_supplicant
	cd $(PKG_ROOT); install -dv sbin usr/share/man/man{5,8}
	install -D -v -m755 $(DIR)/wpa_supplicant/wpa_{cli,passphrase,supplicant} $(PKG_ROOT)/sbin/; \
	install -D -v -m644 $(DIR)/wpa_supplicant/wpa_supplicant.conf $(PKG_ROOT)/etc/wpa_supplicant/wpa_supplicant.conf.orig; \
	install -D -v -m644 wpa_supplicant.conf.sample  $(PKG_ROOT)/etc/wpa_supplicant/wpa_supplicant.conf.sample; \
	install -D -v -m644 ../busybox/busybox-*/examples/var_service/supplicant_if/wpa_supplicant.conf  $(PKG_ROOT)/etc/wpa_supplicant/wpa_supplicant.BB.conf.sample; \
	install -D -v -m644 $(DIR)/wpa_supplicant/doc/docbook/wpa_supplicant.conf.5 $(PKG_ROOT)/usr/share/man/man5/; \
	install -D -v -m644 $(DIR)/wpa_supplicant/doc/docbook/wpa_{cli,passphrase,supplicant}.8 $(PKG_ROOT)/usr/share/man/man8/

include ../Makefile.rules
