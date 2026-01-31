# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = fribidi
VERSION = 1.0.16
EXTENSION = .tar.xz
BASE_URL = https://github.com/fribidi/fribidi/releases/download/v$(VERSION)

CONFIGURE = yes
configure: patch
	mkdir -vp $(PKG_ROOT)
	cd $(DIR); meson -Dprefix=$(PKG_ROOT)/$(PKG_DIR) --buildtype=release builddir

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"; echo
	cd $(DIR); ninja -C builddir
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); ninja -C builddir install

include ../Makefile.rules

