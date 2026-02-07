include ../Makefile.conf

PACKAGE = siproxd
VERSION = 0.8.2

BASE_URL = http://downloads.sourceforge.net/project/$(PACKAGE)/$(PACKAGE)/$(VERSION)/

PATCH_FILE1 = siproxd_pidfilechange.patch
PATCH_FILE2 = ltdl.patch

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
