# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = strace
VERSION = 6.18
EXTENSION = .tar.xz

BASE_URL = https://github.com/strace/strace/releases/download/v$(VERSION)

CFLAGS += -std=gnu17

ifeq ($(mARCH), arm64)
# <ldv> try --enable-mpers=check if you don't need 32-bit personality support on aarch64
CONFIG_OPTS += --enable-mpers=check
endif

include ../Makefile.rules
