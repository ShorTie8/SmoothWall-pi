# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = lz4
VERSION = 1.9.2

BASE_URL = https://github.com/lz4/lz4/archive/v$(VERSION)/lz4-$(VERSION).tar.gz

CONFIGURE = yes
configure: patch
	@true

include ../Makefile.rules
