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
VERSION = 7.0.3

TARBALL = $(PACKAGE)-$(VERSION)
EXTENSION = .tar.xz
#EXTENSION = .tar.gz

BASE_URL = http://roy.marples.name/downloads/dhcpcd/

#export pkgName = $(PACKAGE)
#export gitURL = git://roy.marples.name/dhcpcd.git
#export gitCommitID = 8998244b8
#export gitBranch = $(VERSION)

DIR =  $(PACKAGE)-$(VERSION)

CONFIG_OPTS += --mandir=$(PKG_DIR)/man


INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/sbin

include ../Makefile.rules
