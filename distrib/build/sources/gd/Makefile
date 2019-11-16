# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = gd
VERSION = 2.0.33
#VERSION = 2.2.5
#TARBALL = $(PACKAGE)-$(VERSION)
#DIR = libgd-gd-$(VERSION)

BASE_URL = https://github.com/libgd/libgd/archive

ifeq ($(mARCH), arm64)
ReConfigure = yes
endif

include ../Makefile.rules
