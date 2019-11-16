# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = fping
VERSION = 3.13

BASE_URL = http://fping.org/dist
EXTENSION = .tar.gz

CONFIG_OPTS += --sbindir=/sbin --enable-ipv4 --enable-ipv6

INSTALL = yes
install: compile
	$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	cd $(PKG_ROOT)/sbin; \
	chmod 4755 fping*; \
	/sbin/setcap cap_net_raw+ep fping; \
	/sbin/setcap cap_net_raw+ep fping6

include ../Makefile.rules
