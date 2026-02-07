# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = samba
VERSION = 3.6.25

BASE_URL = http://www.samba.org/samba/ftp/stable/

COMPILE_DIR = $(DIR)/source3

CONFIGURE = yes

configure: $(DIR)/
#	@( cd $(COMPILE_DIR); ./configure --prefix=/usr; ./config.status; )
ifeq ($(mARCH), aarch64)
	for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf ../glibc/glibc-*/scripts/$$(basename $${i}) $${i}; \
	done
endif
	cd $(COMPILE_DIR); ./configure $(CONFIG_OPTS)

COMPILE = yes

compile: configure
	@$(MAKE) ${JOBS} -C $(COMPILE_DIR)

include ../Makefile.rules
