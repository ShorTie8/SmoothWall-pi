# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libbpf
VERSION = 1.6.2
TARBALL = v$(VERSION)
DIR = $(PACKAGE)-$(VERSION)/src
BASE_URL = https://github.com/libbpf/libbpf/archive/refs/tags

CONFIGURE = yes
configure: patch
	true

include ../Makefile.rules
