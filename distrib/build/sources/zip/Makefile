# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile
include ../Makefile.conf

PACKAGE = zip
VERSION = 30

TARBALL = $(PACKAGE)$(VERSION)
EXTENSION = .tar.gz

BASE_URL = http://sourceforge.net/projects/infozip/files/Zip%203.x%20%28latest%29/3.0/zip30.tar.gz/download

DIR = zip30
COMPILE_DIR = $(DIR)

CONFIGURE = yes
configure: patch
	@true

COMPILE = yes
compile: configure
	cd $(DIR); $(MAKE) $(JOBS) LOCAL_ZIP="$(CFLAGS)" prefix=/usr -f unix/Makefile generic_gcc

INSTALL = yes
install: compile
	cd $(DIR); $(MAKE) prefix=$(PKG_ROOT) -f unix/Makefile install

include ../Makefile.rules
