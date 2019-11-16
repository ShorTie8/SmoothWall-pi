# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = strace
VERSION = 4.21

EXTENSION = .tar.xz

BASE_URL = https://sourceforge.net/projects/strace/files/strace/$(VERSION)

ifeq ($(mARCH), arm64)
# <ldv> try --enable-mpers=check if you don't need 32-bit personality support on aarch64
CONFIG_OPTS += --enable-mpers=check
endif

include ../Makefile.rules
