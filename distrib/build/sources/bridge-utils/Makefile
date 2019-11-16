# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = bridge-utils
VERSION = 1.6

BASE_URL = https://www.kernel.org/pub/linux/utils/net/bridge-utils

CONFIGURE = yes
configure: patch
	@echo; echo; echo "autoconf"; echo
	cd $(DIR); autoconf -v
	@echo; echo; echo "configure"; echo
	cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure --prefix=/usr $(CONFIG_OPTS)

include ../Makefile.rules
