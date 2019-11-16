# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = expect
VER_MM = 5.45
VERSION = $(VER_MM).4

BASE_URL = http://prdownloads.sourceforge.net/expect

TARBALL = $(PACKAGE)$(VERSION)

DIR = $(PACKAGE)$(VERSION)

ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS += --prefix=$(TOOLS_DIR) --with-tcl=/$(TOOLS_DIR)/lib \
	--with-tclinclude=$(TOOLS_DIR)/include --with-x=no

CONFIGURE = yes

configure: patch
	cd $(DIR); cp -v configure{,.orig}; \
	  sed 's:/usr/local/bin:/bin:' configure.orig > configure
ifeq ($(mARCH), arm64)
	cd $(DIR); libtoolize --install --copy --force --automake
	cd $(DIR); autoreconf -i
endif
	cd $(DIR); ./configure $(CONFIG_OPTS)

INSTALL = yes

install: compile
	@cd $(COMPILE_DIR); make SCRIPTS="" DESTDIR=$(PKG_ROOT) install
endif

include ../Makefile.rules
