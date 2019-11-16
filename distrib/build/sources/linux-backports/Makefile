# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = backports
FROM_KNL = 4.4.2
VERSION = $(FROM_KNL)-1

BASE_URL = http://www.kernel.org/pub/linux/kernel/projects/$(PACKAGE)/stable/v$(FROM_KNL)
EXTENSION = .tar.xz

KLIB = /lib/modules/$(KERNEL_VER)
KLIB_BUILD = ../../linux/linux

CONFIGURE = yes
configure: patch
	cd $(DIR); sed -i -e 's=depmod -a=depmod -a $(KERNEL_VER)=' Makefile.real
	cp ../linuxbackports.config-$(mARCH) $(DIR)/.config
	cd $(DIR); $(MAKE) $(JOBS) KLIB=$(KLIB) KLIB_BUILD=$(KLIB_BUILD) oldconfig
	cp $(DIR)/.config ../linuxbackports.config-$(mARCH).new

COMPILE = yes
compile: configure
ifeq ($(BITS_64), yes)
	cd $(DIR); $(MAKE) $(JOBS) CFLAGS="-O2 -m64" CXXFLAGS="-O2 -m64" V=1 KLIB=$(KLIB) KLIB_BUILD=$(KLIB_BUILD) modules
else
	cd $(DIR); $(MAKE) $(JOBS) V=1 KLIB=$(KLIB) KLIB_BUILD=$(KLIB_BUILD) modules
endif

INSTALL = yes
install: compile
ifeq ($(BITS_64), yes)
	cd $(DIR); $(MAKE) $(JOBS) CFLAGS="-O2 -m64" CXXFLAGS="-O2 -m64" KLIB=$(PKG_ROOT) KLIB_BUILD=$(KLIB_BUILD) install
else
	cd $(DIR); $(MAKE) $(JOBS) KLIB=$(PKG_ROOT) KLIB_BUILD=$(KLIB_BUILD) install
endif
	

include ../Makefile.rules
