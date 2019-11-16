# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = procps-ng
VERSION = 3.3.6
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
	cd $(DIR); LIBS=-ltinfo ./configure $(CONFIG_OPTS)
	#cd $(DIR); sed -i -e 's/-lncurses/& -ltinfo/' Makefile

install: compile
	mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	#rm -f $(PKG_ROOT)/lib/libproc.so
		
include ../Makefile.rules
