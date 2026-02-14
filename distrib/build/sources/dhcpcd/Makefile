# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

###
# 2016-05-02
# When dhcpcd is included in an update, be sure to add ./usr/etc/dhcpcd.conf
# to coretree.list
###

include ../Makefile.conf

PACKAGE = dhcpcd
VERSION = 10.3.0
EXTENSION = .tar.xz
TARBALL = $(PACKAGE)-$(VERSION)
DIR =  $(PACKAGE)-$(VERSION)
BASE_URL = https://github.com/NetworkConfiguration/dhcpcd/releases/download/v$(VERSION)/

CONFIG_OPTS += --mandir=$(PKG_DIR)/man --disable-privsep

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/sbin

include ../Makefile.rules
