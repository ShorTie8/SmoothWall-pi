# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libusb-compat
VER_MM = 0.1
VERSION = $(VER_MM).12

DLPACKAGE = libusb

TARBALL = $(PACKAGE)-$(VERSION)
EXTENSION = .tar.gz

BASE_URL = https://github.com/libusb/libusb-compat-0.1/archive/refs/tags/v0.1.8.tar.gz

# They moved the legacy lib again. Adjust accordingly.
DOWNLOAD = yes
download:
	@$(PRE_DL) $(DL_CMD) $(BASE_URL)/$(DLPACKAGE)-$(VERSION)$(EXTENSION) $(MD5)

PREPARE = yes
$(DIR)/: download
	@tar -xf $(DOWNLOADS_DIR)/$(DLPACKAGE)-$(VERSION)$(EXTENSION)
	@mv $(DLPACKAGE)-$(VERSION) $(PACKAGE)-$(VERSION)
ifeq ($(mARCH), aarch64)
	for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf ../glibc/glibc-*/scripts/$$(basename $${i}) $${i}; \
	done
endif

include ../Makefile.rules
