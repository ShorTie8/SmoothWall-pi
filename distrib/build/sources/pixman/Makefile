# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = pixman
VERSION = 0.46.4
BASE_URL = http://cairographics.org/releases/

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	mkdir -vp $(PKG_ROOT)
	cd $(DIR); meson --prefix=$(PKG_DIR) $(PKG_ROOT)

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"; echo
	cd $(DIR); ninja -C $(PKG_ROOT)
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); ninja -C $(PKG_ROOT) install

include ../Makefile.rules

