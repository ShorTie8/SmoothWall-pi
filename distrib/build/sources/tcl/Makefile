# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = tcl
TCL_MM = 8.6
VERSION = $(TCL_MM).9
DIR = $(PACKAGE)$(VERSION)
TARBALL = $(PACKAGE)$(VERSION)-src
BASE_URL = http://downloads.sourceforge.net/tcl

ifeq ($(BITS_64), yes)
CONFIG_OPTS += --enable-64bit
#CFLAGS += -m64
endif

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

compile: configure
	@echo; echo; echo "compile"; echo
	make $(JOBS) -C $(DIR)/unix

ifeq ($(BUILD_PHASE), Stage_3)
configure: patch
	@echo; echo; echo "configure"; echo
	(cd $(DIR)/unix; ./configure --prefix=$(TOOLS_DIR) $(CONFIG_OPTS))

install: compile
	@echo; echo; echo "install"; echo
	make -C $(DIR)/unix install
	chmod -v u+w $(TOOLS_DIR)/lib/libtcl$(TCL_MM).so
	make -C $(DIR)/unix install-private-headers
	rm -f $(TOOLS_DIR)/bin/tclsh
	ln -sv tclsh$(TCL_MM) $(TOOLS_DIR)/bin/tclsh
endif

ifeq ($(BUILD_PHASE), Final)
configure: patch
	@echo; echo; echo "configure"; echo
	(cd $(DIR)/unix; ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))

install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)
	make -C $(DIR)/unix INSTALL_ROOT=$(PKG_ROOT) install
	ln -s tclsh$(TCL_MM) $(PKG_ROOT)$(PKG_DIR)/bin/tclsh
endif

include ../Makefile.rules
