# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = dosfstools
VERSION = 3.0.26

BASE_URL = http://daniel-baumann.ch/files/software/dosfstools

TARBALL = $(PACKAGE)-$(VERSION)

DIR = $(PACKAGE)-$(VERSION)

CONFIGURE = yes
INSTALL = yes

configure: patch
	sed -i -e 's/^\(CFLAGS.*\)/\1 $(CFLAGS)/' $(DIR)/Makefile

install: compile
ifeq ($(BUILD_PHASE), Final)
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) PREFIX=$(PKG_ROOT) install
endif

include ../Makefile.rules
