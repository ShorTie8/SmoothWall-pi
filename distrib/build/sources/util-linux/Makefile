# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = util-linux
VER_MM = 2.28
VERSION = $(VER_MM)

export NO_CHECK_CERT = 1

BASE_URL = http://www.kernel.org/pub/linux/utils/util-linux/v$(VER_MM)/

ifeq ($(BUILD_PHASE), Stage_3)

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

CONFIG_OPTS = \
            --prefix=/tools                \
            --without-python               \
            --disable-makeinstall-chown    \
            --disable-silent-rules         \
            --without-systemdsystemunitdir \
            PKG_CONFIG=""

configure: $(DIR)/
	cd $(DIR); ./configure $(CONFIG_OPTS) --prefix=$(TOOLS_DIR) 

compile: configure
	$(MAKE) $(JOBS) -C $(COMPILE_DIR)

install: compile
	cd $(COMPILE_DIR); make install
endif


ifeq ($(BUILD_PHASE), Final)

PRE_CONFIGURE = LDFLAGS=-ltinfo
#CFG_OPTS := $(CONFIG_OPTS)
CONFIG_OPTS += --enable-arch --enable-partx --enable-write --with-ncurses

endif


include ../Makefile.rules
