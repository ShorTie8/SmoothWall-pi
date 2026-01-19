# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = openssl
VERSION = 3.6.0
BASE_URL = https://github.com/openssl/openssl/releases/download/openssl-$(VERSION)

CONFIGURE = yes
configure: $(DIR)/
	@echo; echo; echo "Configure"; echo
	@(cd $(DIR); \
	  ./config --prefix=$(PKG_DIR) \
			--libdir=lib \
			--openssldir=$(PKG_DIR)/lib/ssl \
			shared \
			zlib-dynamic \
			no-docs \
			no-ssl)

COMPILE = yes
compile: configure
	@echo; echo; echo "compile"; echo
	+@$(MAKE) $(JOBS) -C $(PACKAGE)-$(VERSION)

INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	@mkdir -vp $(PKG_ROOT)
	@sed -i '/INSTALL_LIBS/s/libcrypto.a libssl.a//' $(DIR)/Makefile
	@make -C $(DIR) INSTALL_PREFIX=$(PKG_ROOT) install

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -vp $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
