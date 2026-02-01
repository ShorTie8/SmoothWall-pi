# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libtirpc
VERSION = 1.3.6
EXTENSION = .tar.bz2
BASE_URL = https://downloads.sourceforge.net/libtirpc

PATCH_FILE1 = libtirpc-1.3.6-gcc15_fixes-1.patch
PATCH_URL1 = https://www.linuxfromscratch.org/patches/blfs/12.4/libtirpc-1.3.6-gcc15_fixes-1.patch

CONFIG_OPTS += --sysconfdir=/etc --disable-static --disable-gssapi

include ../Makefile.rules
