# Copyright Neal P. Murphy
# Licensed under Smoothwall Express' GPLv2

include ../Makefile.conf

PACKAGE = setkerneltz
VERSION = 0.0

DOWNLOAD = yes
COMPILE = yes
INSTALL = yes
CLEAN = yes

download:
	@true

compile:
	make -C $(DIR)

install: compile
	@mkdir -p $(PKG_ROOT)/usr/bin/smoothwall
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install

clean:
	@echo -n " $(PACKAGE)"
	@rm -f $(DIR)/$(PACKAGE)
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
