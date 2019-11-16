# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = openldap
VERSION = 2.4.48

EXTENSION = .tgz

BASE_URL = https://www.openldap.org/software/download/OpenLDAP/openldap-release

CONFIG_OPTS += --with-tls=openssl

PREPARE = yes
$(DIR)/: download
	@echo; echo "prepare"
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
ifeq ($(mARCH), arm64)
	for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf ../glibc/glibc-*/scripts/$$(basename $${i}) $${i}; \
	done
endif

include ../Makefile.rules
