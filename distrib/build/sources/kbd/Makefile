# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = kbd
# anything newer needs pam
VERSION = 1.15.3

EXTENSION = .tar.xz

BASE_URL = https://www.kernel.org/pub/linux/utils/kbd

ifeq ($(mARCH), arm64)
ReConfigure = yes
endif

include ../Makefile.rules
