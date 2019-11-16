# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = hostapd
VERSION = 2.9

BASE_URL = https://w1.fi/releases
COMPILE_DIR = $(DIR)/hostapd

CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	cd $(COMPILE_DIR); cp defconfig .config
#	cd $(COMPILE_DIR); sed -i 's/CONFIG_DRIVER_NL80211=y/#CONFIG_DRIVER_NL80211=y/' .config
	cd $(COMPILE_DIR); sed -i 's@#LIBS += -L$<path to libnl library files>@LIBS += -L/usr/include/@' .config
	cd $(COMPILE_DIR); sed -i 's@#CONFIG_LIBNL32=y@CONFIG_LIBNL32=y@' .config
	cd $(COMPILE_DIR); sed -i 's@export BINDIR ?= /usr/local/bin/@export BINDIR ?= /usr/sbin/@' Makefile

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)/etc/hostapd/logwatch
	$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	install -v -m644 $(DIR)/hostapd/hostapd.conf $(PKG_ROOT)/etc/hostapd/hostapd.conf.orig
	install -v -m644 $(DIR)/hostapd/logwatch/hostapd.conf $(PKG_ROOT)/etc/hostapd/logwatch/hostapd.conf
	#install -v -m644 hostapd.conf $(PKG_ROOT)/etc/hostapd/hostapd.conf
	install -v -m644 hostapd.green.conf $(PKG_ROOT)/etc/hostapd/hostapd.green.conf
	install -v -m644 hostapd.orange.conf $(PKG_ROOT)/etc/hostapd/hostapd.orange.conf
	install -v -m644 hostapd.purple.conf $(PKG_ROOT)/etc/hostapd/hostapd.purple.conf

include ../Makefile.rules
