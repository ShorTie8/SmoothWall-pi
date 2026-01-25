# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = glib
VER_MM = 2.86
VERSION = $(VER_MM).1
EXTENSION = .tar.xz
BASE_URL =  https://download.gnome.org/sources/glib/$(VER_MM)

CONFIG_OPTS += --without-ffi

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	mkdir -vp $(PKG_ROOT)
	cd $(DIR); meson $(PKG_ROOT)

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"; echo
	cd $(DIR); ninja -C $(PKG_ROOT)
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); ninja -C $(PKG_ROOT) install


include ../Makefile.rules

