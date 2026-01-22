# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

##	https://www.linuxfromscratch.org/blfs/view/svn/general/luajit

include ../Makefile.conf

PACKAGE = LuaJIT
VERSION = 20250816
EXTENSION = .tar.xz
DIR = luajit-$(VERSION)
TARBALL = luajit-$(VERSION)
BASE_URL = https://anduin.linuxfromscratch.org/BLFS/luajit

#BASE_URL = https://github.com/openeuler-mirror/luajit/blob/master
##	https://github.com/openeuler-mirror/luajit/blob/master/0002-luajit-add-secure-compile-option-fstack.patch
##	https://github.com/openeuler-mirror/luajit/blob/master/luajit-2.1-update.patch

CONFIGURE = yes
configure: patch
	true

COMPILE = yes
compile: configure
	$(MAKE) ${JOBS} PREFIX=/usr -C $(DIR) amalg

#INSTALL = yes
#install: compile
#	mkdir -p $(PKG_ROOT)
#	$(MAKE) DESTDIR=$(PKG_ROOT) PREFIX=/usr -C $(COMPILE_DIR) install

include ../Makefile.rules
