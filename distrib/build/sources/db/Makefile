# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = db
VERSION = 4.6.21.NC

BASE_URL = http://download.oracle.com/berkeley-db/

CONFIG_OPTS= --prefix=/usr --enable-compat185 --enable-dbm --enable-cxx \
	     --disable-static

PATCH_FILE1 = ../Makefile.in.patch

DIR = $(PACKAGE)-$(VERSION)/build_unix

PATCH = yes
CONFIGURE = yes
CLEAN = yes

patch: $(DIR)/
	@(cd $(DIR)/..; cat $(PATCH_FILE1) | patch -p1)

configure: patch
	cd $(DIR); ../dist/configure $(CONFIG_OPTS)

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(PACKAGE)-$(VERSION)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
