# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = iptables
VERSION =  $(IPTABLES_VER)

EXTENSION = .tar.bz2
BASE_URL = http://www.netfilter.org/projects/iptables/files

CONFIG_OPTS += --prefix=/usr --mandir=/usr/man --docdir=/usr/doc \
	        --enable-devel --enable-libipq


CONFIGURE = yes
COMPILE = yes
INSTALL = yes

#CONFIG_OPTS = --enable-libipq

configure: $(DIR)/ patch
	(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
ifneq ($(DIR), $(COMPILE_DIR))
	(cd $(COMPILE_DIR); ../$(DIR)/configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))
else
	(cd $(COMPILE_DIR); ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))
endif

export V = 1
compile: configure
	make $(JOBS) -C $(COMPILE_DIR) COPT_FLAGS='$(CFLAGS)' PREFIX=$(PKG_DIR)


install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@mkdir -p $(PKG_ROOT)/sbin
	@(cd $(PKG_ROOT)/sbin; rm -f iptables; ln -s /usr/sbin/iptables)

include ../Makefile.rules
