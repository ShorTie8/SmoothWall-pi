# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = GeoIP
VERSION = 1.4.8

BASE_URL = http://www.maxmind.com/download/geoip/api/c

CONFIG_OPTS += --with-gnu-ld
CONFIGURE = yes
configure: patch
	cd $(COMPILE_DIR); \
	  autoreconf -v -f --install
	cd $(COMPILE_DIR); $(PRE_CONFIGURE) ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS)

include ../Makefile.rules
