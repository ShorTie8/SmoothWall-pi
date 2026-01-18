# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2010
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = httpd
VERSION = 2.4.66
LICENCE_FILE = $(DIR)/COPYING
BASE_URL = http://archive.apache.org/dist/httpd/

APR_VER = 1.7.6
BASE_APR = https://archive.apache.org/dist/apr
TAR_APR = apr-$(APR_VER).tar.gz

APR_UTIL_VER = 1.6.3
BASE_APR_UTIL= https://archive.apache.org/dist/apr
TAR_APR_UTIL = apr-util-$(APR_UTIL_VER).tar.gz

DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo
	$(DL_CMD) $(BASE_APR)/$(TAR_APR)
	$(DL_CMD) $(BASE_APR_UTIL)/$(TAR_APR_UTIL)
	$(DL_CMD) $(BASE_URL)/$(TARBALL)$(EXTENSION) $(MD5)

PREPARE = yes
$(DIR)/: download
	@echo; echo; echo "PrePare"; echo
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_APR); mv apr-$(APR_VER) srclib/apr
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_APR_UTIL); mv apr-util-$(APR_UTIL_VER) srclib/apr-util

CONFIG_OPTS += --enable-ssl --with-ssl=/usr \
	--with-included-apr --enable-mods-shared=all --enable-layout=RedHat

CONFIGURE = yes
INSTALL = yes

configure: patch
	@(cd $(DIR); ./configure $(CONFIG_OPTS) --prefix=$(PKG_DIR))

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@rm -rf $(PKG_ROOT)/{etc,var}

include ../Makefile.rules
