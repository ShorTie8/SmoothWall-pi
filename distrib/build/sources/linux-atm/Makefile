# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = linux-atm
VERSION = 2.5.2

BASE_URL = https://sourceforge.net/projects/linux-atm/files/linux-atm/$(VERSION)

PATCH_FILE1 = led-main.c.patch

ifeq ($(mARCH), arm64)
ReConfigure = yes
endif

include ../Makefile.rules
