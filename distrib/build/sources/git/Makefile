# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = git
VERSION = 2.9.5

EXTENSION = .tar.gz

BASE_URL = https://www.kernel.org/pub/software/scm/git

ifeq ($(BUILD_PHASE), Stage_3)
CONFIG_OPTS += --with-openssl --without-curl --without-tcltk --without-python
else
CONFIG_OPTS += --with-openssl --without-tcltk
endif

include ../Makefile.rules
