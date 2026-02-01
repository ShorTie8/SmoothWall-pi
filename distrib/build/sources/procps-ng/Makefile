# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# ShorTie added a /etc/sysctl.conf 10/12/2019
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = procps-ng
VERSION = 4.0.5
EXTENSION = .tar.xz
BASE_URL = https://sourceforge.net/projects/procps-ng/files/Production

CONFIG_OPTS += \
	       --docdir=/usr/share/doc/procps-ng-4.0.5 \
	       --disable-static \
	       --disable-kill \
	       --enable-watch8bit

INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	mkdir -p $(PKG_ROOT)/etc
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@echo; echo; echo "cp -v sysctl.conf"; echo
	cp -v sysctl.conf $(PKG_ROOT)/etc/sysctl.conf
	#rm -f $(PKG_ROOT)/lib/libproc.so
		
include ../Makefile.rules
