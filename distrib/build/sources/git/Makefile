# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = git
VERSION = 2.9.3

EXTENSION = .tar.gz

BASE_URL = https://www.kernel.org/pub/software/scm/git/

CONFIG_OPTS += --with-openssl --without-curl --without-tcltk --without-python

COMPILE = yes
INSTALL = yes
CLEAN = yes

compile: configure
	make $(JOBS) -C $(COMPILE_DIR) PREFIX=$(PKG_DIR) V=1

install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) PREFIX=$(PKG_DIR) DESTDIR=$(PKG_ROOT) install

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
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
