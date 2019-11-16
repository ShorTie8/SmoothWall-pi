# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = xtables-addons
VERSION =  $(XTABLES_ADDONS_VER)

EXTENSION = .tar.xz

BASE_URL = http://downloads.sourceforge.net/project/xtables-addons/Xtables-addons

CONFIG_OPTS += --with-gnu-ld \
	       --with-kbuild=/build/sources/linux$(KERNEL_TYPE)/linux/

COMPILE = yes
compile: configure
	+$(PRE_COMPILE) $(MAKE) ${JOBS} -C $(COMPILE_DIR) V=1

include ../Makefile.rules
