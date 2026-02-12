# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = LibML
VERSION = 2.0.0
DIR = libml-$(VERSION)
TARBALL = $(VERSION)
BASE_URL = https://github.com/snort3/libml/archive/refs/tags

CONFIGURE = yes
configure: patch
	@echo -e "\n\nConfigure\n"
	cd $(DIR); ./configure.sh

COMPILE = yes
compile: configure
	@echo -e "\n\nCompile\n"
	cd $(DIR)/build; make $(JOBS)

INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	mkdir -vp $(PKG_ROOT)
	cd $(DIR)/build; make $(JOBS) DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
