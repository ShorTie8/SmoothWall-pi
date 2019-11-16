# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = cacert-bundle
VERSION = 0.0

DOWNLOAD = yes
INSTALL = yes
CLEAN = yes

download:
	@true

install:
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)/lib/ssl/certs
	cd $(PKG_ROOT)/$(PKG_DIR)/lib/ssl/certs; \
	  /build/sources/cacert-bundle/mk-ca-bundle.pl ca-certificates.crt
	cd $(PKG_ROOT)/$(PKG_DIR)/lib/ssl/certs; \
	  rm -f certdata.txt
	cd $(PKG_ROOT)/$(PKG_DIR)/lib/ssl/certs; \
	  perl /build/sources/cacert-bundle/unbundle.pl
	cd $(PKG_ROOT)/$(PKG_DIR)/lib/ssl/certs; \
	  c_rehash .

clean:
	@echo -n " $(PACKAGE)"
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
