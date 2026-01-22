# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libpsl
VERSION = 0.21.5
TARBALL = $(VERSION)
BASE_URL = https://github.com/rockdaboot/libpsl/archive/refs/tags


CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	cd $(DIR); mkdir -vp meson-compile

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"; echo
	cd $(DIR); ninja -C meson-compile
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); ninja -C meson-compile test

include ../Makefile.rules
