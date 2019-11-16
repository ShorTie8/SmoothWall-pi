# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = openntpd
VERSION = 5.7p4

BASE_URL = ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/

PATCH_FILE1 = openntpd-username.patch

CONFIG_OPTS += --with-privsep-user=ntpd --localstatedir=/var

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	cd $(COMPILE_DIR); make DESTDIR=$(PKG_ROOT) install
	# We don't want the default ntpd.conf
	rm -rf $(PKG_ROOT)/usr/etc

include ../Makefile.rules
