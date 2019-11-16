# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = e2fsprogs
VERSION = 1.42.13

BASE_URL = http://downloads.sourceforge.net/project/$(PACKAGE)/$(PACKAGE)/v$(VERSION)/

COMPILE_DIR = $(DIR)-compile

ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS += --prefix=$(TOOLS_DIR) --enable-verbose-makecmds

INSTALL = yes
install: compile
	@make -C $(COMPILE_DIR) install-libs
	chmod -v u+w $(TOOLS_DIR)/lib/{libblkid,libuuid,libcom_err,libe2p,libext2fs,libss}.a

endif


ifeq ($(BUILD_PHASE), Final)

PKG_DIR=

CONFIG_OPTS += --prefix=/usr           \
               --bindir=/bin           \
               --with-root-prefix=""   \
               --enable-elf-shlibs     \
               --disable-libblkid      \
               --disable-libuuid       \
               --disable-uuidd         \
	       --enable-verbose-makecmds \
               --disable-fsck


PATCH = yes

patch: $(DIR)/
	sed -i 's@/bin/rm@$(TOOLS_DIR)&@' $(DIR)/lib/blkid/test_probe.in
#	sed -i -e "s/July/Jul/" $(DIR)/version.h

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install-libs
endif
	
include ../Makefile.rules
