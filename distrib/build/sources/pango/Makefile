# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = pango
VER_MM = 1.90
VERSION = $(VER_MM).0
EXTENSION = .tar.xz
#PRE_CONFIGURE = ENABLE_GTK_DOC_FALSE=''

BASE_URL = https://download.gnome.org/sources/pango/$(VER_MM)

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	mkdir -vp $(PKG_ROOT)
	echo; echo; meson -h install; echo; echo
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

