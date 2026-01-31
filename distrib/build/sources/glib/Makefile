# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

##	cairo calls for 2.74.0

include ../Makefile.conf

PACKAGE = glib
VER_MM = 2.87
VERSION = $(VER_MM).2
EXTENSION = .tar.xz
BASE_URL =  https://download.gnome.org/sources/glib/$(VER_MM)

CONFIG_OPTS += --without-ffi

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	mkdir -vp $(PKG_ROOT)
	cd $(DIR); meson -Dprefix=$(PKG_ROOT)/$(PKG_DIR) builddir

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"; echo
	cd $(DIR); ninja -C builddir
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); ninja -C builddir install

include ../Makefile.rules

