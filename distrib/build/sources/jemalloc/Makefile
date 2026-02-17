# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = jemalloc
VERSION = 5.3.0
TARBALL = $(VERSION)
BASE_URL = https://github.com/jemalloc/jemalloc/archive/refs/tags

CONFIG_OPTS += \
		--enable-prof \
		--enable-xmalloc`\
		--enable-lazy-lock \
		--enable-prof-libunwind`

PATCH = yes
 patch: $(DIR)/
	cd $(DIR); ./autogen.sh

include ../Makefile.rules
