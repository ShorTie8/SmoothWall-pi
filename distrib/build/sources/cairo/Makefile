# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = cairo
VERSION = 1.18.4
EXTENSION = .tar.xz
BASE_URL = https://www.cairographics.org/releases

CONFIG_OPTS = --enable-xml

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	mkdir -vp $(PKG_ROOT)
	cd $(DIR); meson setup --prefix=$(PKG_DIR) $(PKG_ROOT)

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"; echo
	cd $(DIR); ninja -C $(PKG_ROOT) --prefix=$(PKG_DIR)
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); ninja -C $(PKG_ROOT) install

include ../Makefile.rules

