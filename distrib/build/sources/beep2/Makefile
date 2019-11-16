# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = beep2
VERSION = 1.2a

JOBS =
BASE_URL =  http://www.kip.iis.toyama-u.ac.jp/~shingo/beep/package/src/

DOWNLOAD = yes
CONFIGURE = yes
INSTALL = yes
CLEAN = yes

download:
	@true

configure:
	@true
	
install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(DIR) PREFIX=$(PKG_ROOT)/usr/ install

clean:
	@echo -n " $(PACKAGE)"
	@make -C $(DIR) clean >/dev/null 2>&1
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
