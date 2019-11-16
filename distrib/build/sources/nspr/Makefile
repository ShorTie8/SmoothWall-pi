# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = nspr
VERSION = 4.17

BASE_URL = https://ftp.mozilla.org/pub/mozilla.org/$(PACKAGE)/releases/v$(VERSION)/src

export NO_CHECK_CERT = yes

DIR = $(PACKAGE)-$(VERSION)/nspr

CONFIG_OPTS = --prefix=$(PKG_DIR) \
	      --with-mozilla \
	      --with-pthreads
ifeq ($(BITS_64), yes)
  CONFIG_OPTS += --enable-64bit
endif

CONFIGURE = yes
configure: patch
	cd $(COMPILE_DIR); \
	  sed -ri 's#^(RELEASE_BINS =).*#\1#' pr/src/misc/Makefile.in; \
	  sed -i 's#$$(LIBRARY) ##' config/rules.mk; \
	  ./configure $(CONFIG_OPTS)

CLEAN = yes
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
