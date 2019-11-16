# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = coreutils
VERSION = 8.28

BASE_URL = https://ftp.gnu.org/gnu/coreutils
EXTENSION = .tar.xz

CONFIG_OPTS += --disable-silent-rules

# Tool Chain Build Stage_3
#
ifeq ($(BUILD_PHASE), Stage_3)
CONFIG_OPTS += --enable-install-program=hostname
endif # Stage 3

# # Final Build
#
ifeq ($(BUILD_PHASE), Final)

#CONFIG_OPTS += --enable-install-program=arch 

PATCH_FILE1 = coreutils-$(VERSION)-i18n-1.patch
PATCH_URL1 = http://www.linuxfromscratch.org/patches/downloads/coreutils/$(PATCH_FILE1)
#PATCH_FILE2 = coreutils-8.26-uname-1.patch
#PATCH_URL2 = http://www.linuxfromscratch.org/patches/downloads/coreutils/$(PATCH_FILE2)

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@(mkdir -p $(PKG_ROOT)/bin; \
	for FILE in basename cat chgrp chmod chown cp cut date dd df echo env false link ln \
		 ls mkdir mknod mv nice pwd rm rmdir sleep sort stty sync touch true uname unlink; \
	do \
		mv $(PKG_ROOT)$(PKG_DIR)/bin/$$FILE $(PKG_ROOT)/bin; \
	done);
	ln -s /bin/env $(PKG_ROOT)$(PKG_DIR)/bin/env
endif
	         
include ../Makefile.rules
