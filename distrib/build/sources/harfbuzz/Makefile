# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = harfbuzz
VERSION = 11.4.1
EXTENSION = .tar.xz
BASE_URL = https://github.com/harfbuzz/harfbuzz/releases/download/$(VERSION)

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	mkdir -vp $(PKG_ROOT)
	cd $(DIR); meson setup builddir -Dbuildtype=release -Db_lto=true -Dprefix=$(PKG_ROOT)/$(PKG_DIR)

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"; echo
	cd $(DIR); ninja -C builddir
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); ninja -C builddir install

include ../Makefile.rules

