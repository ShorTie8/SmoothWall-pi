# SmoothWall Build system.
#
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = wireless-regdb
VERSION = 2019.06.03
BASE_URL = https://mirrors.edge.kernel.org/pub/software/network/wireless-regdb

INSTALL = yes
install: patch
	@echo; echo; echo "install"; echo
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	install -m 644 -t $(PKG_ROOT)/usr/lib/crda/pubkeys/ $(DIR)/sforshee.x509.pem

include ../Makefile.rules
