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
TARBALL = $(PACKAGE)$(VERSION)
DIR = $(PACKAGE)$(VERSION)
BASE_URL = http://prdownloads.sourceforge.net/expect

# Tool Chain Build Stage 3 expect
#
ifeq ($(BUILD_PHASE), Stage_3)

CFLAGS += -Wall -g -ansi -D_SVID_SOURCE -D_POSIX_SOURCE

CONFIG_OPTS = --prefix=$(TOOLS_DIR) \
		--target=$(SWE_TGT) \
		--with-tcl=/$(TOOLS_DIR)/lib \
		--with-tclinclude=$(TOOLS_DIR)/include \
		--with-x=no \
		--disable-werror

CONFIGURE = yes
configure: patch
	cp -v /tools/share/automake-1.18/config.guess $(DIR)/config.guess
	cp -v /tools/share/automake-1.18/config.guess $(DIR)/tclconfig/config.guess
	cp -v /tools/share/automake-1.18/config.sub $(DIR)/config.sub
	cp -v /tools/share/automake-1.18/config.sub $(DIR)/tclconfig/config.sub
	cd $(DIR); autoconf
	cd $(DIR); cp -v configure{,.orig}; \
	  sed 's:/usr/local/bin:/bin:' configure.orig > configure
ifeq ($(mARCH), arm64)
	cd $(DIR); libtoolize --install --copy --force --automake
	cd $(DIR); autoreconf -vif
endif
	cd $(DIR); ./configure $(CONFIG_OPTS)

INSTALL = yes
install: compile
	@cd $(COMPILE_DIR); make SCRIPTS="" DESTDIR=$(PKG_ROOT) install
endif

include ../Makefile.rules
