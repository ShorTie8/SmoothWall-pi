# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = hddtemp
VERSION = 0.3-beta15

BASE_URL = http://ftp.debian.org/debian/pool/main/h/hddtemp/

DIR = $(PACKAGE)-$(VERSION)
TARBALL = $(PACKAGE)_$(VERSION).orig
HDTEMPDB = hddtemp.db

PATCH_FILE1 = hddtemp_0.3-beta15-54.diff.gz
PATCH_URL1 = https://ftp.debian.org/debian/pool/main/h/hddtemp/hddtemp_0.3-beta15-54.diff.gz
#PATCH_FILE2 = REG_EIP.patch
#PATCH_FILE2 = hddtemp-0.3_beta15-dontwake.patch
PATCH_FILE3 = hddtemp-0.3_beta15-iconv.patch
PATCH_FILE4 = hddtemp-0.3_beta15-nls.patch

CFLAGS += -std=gnu17

ifeq ($(mARCH), arm64)
ReConfigure = yes
endif

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@install -D $(COMPILE_DIR)/src/hddtemp $(PKG_ROOT)/usr/sbin/hddtemp
	@install -D hddtemp.db $(PKG_ROOT)/usr/share/misc/hddtemp.db

include ../Makefile.rules
