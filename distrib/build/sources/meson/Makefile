# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = meson
VERSION = 1.8.3
BASE_URL = https://github.com/mesonbuild/meson/releases/download/$(VERSION)

COMPILE = yes
compile: $(DIR)/
	@echo; echo; echo "Compile"; echo
	cd $(DIR); python3 setup.py build
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); python3 setup.py install --root=$(PKG_ROOT)

include ../Makefile.rules
