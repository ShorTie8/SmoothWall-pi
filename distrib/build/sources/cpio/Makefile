# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = cpio
VERSION = 2.11

BASE_URL = http://ftp.gnu.org/gnu/cpio/

LICENCE_FILE = $(DIR)/COPYING

PRE_CONFIGURE = CFLAGS="$(CFLAGS)"

CONFIG_OPTS += --prefix=/usr \
	      --bindir=/bin \
	      --disable-silent-rules \
	      --with-rmt=/usr/sbin/rmt

PREPARE = yes

$(DIR)/: download
	tar -xvf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	cd $(DIR); sed -i -e '/gets is a/d' gnu/stdio.in.h

include ../Makefile.rules
