# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = at
VERSION = 3.1.23

BASE_URL = http://ftp.debian.org/debian/pool/main/a/at
TARBALL = $(PACKAGE)_$(VERSION).orig
DIR = $(PACKAGE)-$(VERSION)

PATCH_FILE1 = no-sendmail.patch
#PATCH_FILE2 = at_3.1.20-3.debian.tar.xz
#PATCH_URL2 = http://ftp.debian.org/debian/pool/main/a/at/$(PATCH_FILE2)

PREPARE = yes
$(DIR)/: download
	@echo; echo "prepare"
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
ifeq ($(mARCH), aarch64)
	for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf ../glibc/glibc-*/scripts/$$(basename $${i}) $${i}; \
	done
endif

#PATCH = yes
#patch: $(DIR)/
#	@echo; echo; echo "patch"
#	cd $(DIR); patch -p1 < ../$(PATCH_FILE1) 
#	tar -xf $(DOWNLOADS_DIR)/$(PATCH_FILE2)
#	cd $(DIR); for p in $$(cat ../debian/patches/series); do \
#		echo; echo $$p; \
#		patch -p1 < ../debian/patches/$$p; \
#	done

CONFIG_OPTS += --with-jobdir=/var/spool/atjobs --with-atspool=/var/spool/atspool --without-sendmail \
	       --with-daemon_username=nobody --with-daemon_groupname=nobody

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) IROOT=$(PKG_ROOT) install

include ../Makefile.rules
