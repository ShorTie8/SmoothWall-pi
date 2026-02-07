# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = sysfsutils
VERSION = 2.1.0

BASE_URL = http://iweb.dl.sourceforge.net/project/linux-diag/sysfsutils/2.1.0

CONFIG_OPTS += --disable-static --enable-shared --sysconfdir=/usr/etc

PREPARE = yes
$(DIR)/: download
	@echo; echo "prepare"
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
ifeq ($(mARCH), aarch64)
	for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf ../glibc/glibc-*/scripts/$$(basename $${i}) $${i}; \
	done
endif

include ../Makefile.rules
