# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libunwind
VERSION = 1.8.3
BASE_URL = https://github.com/libunwind/libunwind/releases/download/v$(VERSION)

CONFIG_OPTS += --disable-static

PATCH = yes
patch: $(DIR)/
	##	First, fix a problem when building with gcc-15:
	cd $(DIR); sed -i '/func.s/s/s//' tests/Gtest-nomalloc.c

include ../Makefile.rules
