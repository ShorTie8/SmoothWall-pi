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

ifeq ($(mARCH), x86_64)
PATCH_FILE1 = expect-5.45.4-gcc15-1.patch
PATCH_URL1 = https://www.linuxfromscratch.org/patches/lfs/12.4/expect-5.45.4-gcc15-1.patch
endif

ifeq ($(mARCH), arm64)
ReConfigure = yes
CFLAGS += -Wall -g -ansi -D_SVID_SOURCE -D_POSIX_SOURCE
endif

CONFIG_OPTS += \
		--with-tcl=/$(PKG_DIR)/lib \
		--with-tclinclude=$(PKG_DIR)/include \
		--disable-rpath

CONFIGURE = yes
configure: patch
	##	Expect needs PTYs to work.
	## Verify that the PTYs are working properly inside the chroot environment by performing a simple test:
	##	This test fails on final build, but normally not built .. :(~
	@echo; echo; echo -n "PTY's test,  "
	#python3 -c 'from pty import spawn; spawn(["echo", "ok"])'
	@echo; echo; echo "Configure"; echo
	cd $(DIR); cp -v configure{,.orig}; \
	  sed 's:/usr/local/bin:/bin:' configure.orig > configure
	(cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))

INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	@cd $(COMPILE_DIR); make SCRIPTS="" DESTDIR=$(PKG_ROOT) install
	#@ln -svf expect5.45.4/libexpect5.45.4.so $(PKG_ROOT)/lib

include ../Makefile.rules
