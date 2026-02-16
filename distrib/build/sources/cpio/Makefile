# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = cpio
VERSION = 2.15
LICENCE_FILE = $(DIR)/COPYING
BASE_URL = http://ftp.gnu.org/gnu/cpio/

PRE_CONFIGURE = CFLAGS="$(CFLAGS)"

CONFIG_OPTS += --prefix=/usr \
	      --bindir=/bin \
	      --disable-silent-rules \
	      --with-rmt=/usr/sbin/rmt

PREPARE = yes
$(DIR)/: download
	tar -xvf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	cd $(DIR); sed -i -e '/gets is a/d' gnu/stdio.in.h
	##	Add a workaround for an issue shown by gcc15:
	cd $(DIR); sed -e "/^extern int (\*xstat)/s/()/(const char * restrict,  struct stat * restrict)/" \
					-i src/extern.h
	cd $(DIR); sed -e "/^int (\*xstat)/s/()/(const char * restrict,  struct stat * restrict)/" \
					-i src/global.c

include ../Makefile.rules
