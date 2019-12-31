# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libuv
VERSION = v1.34.0

BASE_URL = https://dist.libuv.org/dist/$(VERSION)

CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	cd $(DIR); sh autogen.sh
	cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure  --disable-static $(CONFIG_OPTS)

include ../Makefile.rules
