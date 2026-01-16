# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = util-linux
VER_MM = 2.41
VERSION = $(VER_MM).3

BASE_URL = http://www.kernel.org/pub/linux/utils/util-linux/v$(VER_MM)/

ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS = \
		--prefix=/tools \
		--disable-liblastlog2 \
		--disable-silent-rules \
		--disable-makeinstall-chown \
		--without-python \
		--without-systemdsystemunitdir \
		PKG_CONFIG=""

CONFIGURE = yes
configure: $(DIR)/
	cd $(DIR); ./configure $(CONFIG_OPTS) --prefix=$(TOOLS_DIR) 

COMPILE = yes
compile: configure
	$(MAKE) $(JOBS) -C $(COMPILE_DIR)

INSTALL = yes
install: compile
	cd $(COMPILE_DIR); make install
endif


ifeq ($(BUILD_PHASE), Final)

PRE_CONFIGURE = LDFLAGS=-ltinfo
#CFG_OPTS := $(CONFIG_OPTS)
#--enable-arch --enable-partx --enable-write --with-ncurses
CONFIG_OPTS = \
		--bindir=/usr/bin \
		--libdir=/usr/lib     \
		--runstatedir=/run    \
		--sbindir=/usr/sbin   \
		--disable-chfn-chsh   \
		--disable-login       \
		--disable-nologin     \
		--disable-su          \
		--disable-setpriv     \
		--disable-runuser     \
		--disable-pylibmount  \
		--disable-liblastlog2 \
		--disable-static      \
		--without-python      \
		--without-systemd     \
		--without-systemdsystemunitdir        \
		ADJTIME_PATH=/var/lib/hwclock/adjtime \
		--docdir=/usr/share/doc/util-linux-2.41.1

CONFIGURE = yes
configure: $(DIR)/
	cd $(DIR); ./configure $(CONFIG_OPTS) --prefix=$(TOOLS_DIR) 


endif


include ../Makefile.rules
