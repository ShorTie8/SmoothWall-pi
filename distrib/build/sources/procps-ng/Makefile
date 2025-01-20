# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# ShorTie added a /etc/sysctl.conf 10/12/2019
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = procps-ng
VERSION = 4.0.5
EXTENSION = .tar.xz

BASE_URL = http://sourceforge.net/projects/procps-ng/files/Production/

ifeq ($(BUILD_PHASE), Final)
PKG_DIR =

CONFIG_OPTS += --prefix= --exec-prefix= \
	       --datarootdir=/usr/share \
	       --libexecdir=/usr/libexec \
	       --includedir=/usr/include
endif

CONFIGURE = yes
INSTALL = yes

CONFIG_OPTS += --prefix=/ --includedir=/usr/include --datarootdir=/usr/share
configure: $(DIR)/
	@echo; echo; echo "configure"; echo
	cd $(DIR); LIBS=-ltinfo ./configure $(CONFIG_OPTS)
	#cd $(DIR); sed -i -e 's/-lncurses/& -ltinfo/' Makefile

install: compile
	@echo; echo; echo "install"; echo
	mkdir -p $(PKG_ROOT)/etc
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@echo; echo; echo "cp -v sysctl.conf"; echo
	cp -v sysctl.conf $(PKG_ROOT)/etc/sysctl.conf
	#rm -f $(PKG_ROOT)/lib/libproc.so
		
include ../Makefile.rules
