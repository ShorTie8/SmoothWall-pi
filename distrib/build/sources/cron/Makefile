# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = cron
VERSION = 3.0pl1
DIR = $(PACKAGE)-$(VERSION).orig
TARBALL = $(PACKAGE)_$(VERSION).orig
BASE_URL = http://ftp.debian.org/debian/pool/main/c/cron/



PATCH_FILE1 = cron_3.0pl1-206.debian.tar.xz
PATCH_URL1 = https://ftp.debian.org/debian/pool/main/c/cron/cron_3.0pl1-206.debian.tar.xz
PATCH_FILE2 = smoothwall-pid.patch
PATCH_FILE3 = smoothinstall.patch

PREPARE = yes
$(DIR)/: download
	@echo; echo "PrePare"
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	cd $(COMPILE_DIR); tar -xf ../cron_3.0pl1-206.debian.tar.xz

PATCH = yes
patch: $(DIR)/
	@echo; echo "Patch";echo
	@(for PATCH in `cat $(DIR)/debian/patches/series`; do \
		echo; echo $$PATCH; \
		cd $(DIR); patch -p1 < debian/patches/$$PATCH; cd ..;\
	  done;)
	(cd $(DIR); \
	for PATCH in $(PATCH_FILE2) $(PATCH_FILE3) $(PATCH_FILE4); do \
	  echo $$PATCH; \
	  FILENAME=../$$PATCH; \
	  echo; echo $$FILENAME; \
	  [ -f $$FILENAME ] || exit 8; \
	  cat $$FILENAME | patch -p1 || exit 14; \
	done;)

CONFIGURE = yes
configure: patch
	cd $(COMPILE_DIR); sed -i -e 's/^\(CFLAGS.*\)/\1 $(CFLAGS)/' Makefile

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@mkdir -p $(PKG_ROOT)/usr/{bin,sbin} $(PKG_ROOT)/usr/share/man/cat{1,5,8}
	@$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
