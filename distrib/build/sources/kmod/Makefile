# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = kmod
VERSION = 22

BASE_URL = http://www.kernel.org/pub/linux/utils/kernel/kmod/
EXTENSION = .tar.xz

export NO_CHECK_CERT = 1

CONFIG_OPTS = --prefix=/usr          \
              --bindir=/bin          \
              --sysconfdir=/etc      \
              --with-rootlibdir=/lib \
	      --disable-silent-rules \
              --with-zlib
              #--with-xz              \

INSTALL = yes
install: compile
	cd $(PKG_ROOT); mkdir -p sbin bin
	cd $(COMPILE_DIR); $(MAKE) DESTDIR=$(PKG_ROOT) install
	cd $(PKG_ROOT); for prog in depmod insmod lsmod modinfo modprobe rmmod; do \
	  ln -sv /bin/kmod sbin/$$prog; \
	done
	cd $(PKG_ROOT); ln -sv kmod bin/lsmod
	

include ../Makefile.rules
