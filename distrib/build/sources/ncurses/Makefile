# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ncurses
VERSION = 6.1

BASE_URL = https://ftp.gnu.org/gnu/ncurses/

#PATCH_FILE1 = ncurses-5.9-gcc5_buildfixes-1.patch
#PATCH_URL1 = http://www.linuxfromscratch.org/patches/downloads/ncurses/$(PATCH_FILE1)

ifeq ($(BUILD_PHASE), Stage_3)
CONFIG_OPTS += --with-shared \
    --without-debug --without-ada --enable-overwrite
else
CONFIG_OPTS += --with-shared \
				--without-debug \
				--with-termlib \
				--with-pkg-config \
				--enable-pc-files
endif

include ../Makefile.rules
