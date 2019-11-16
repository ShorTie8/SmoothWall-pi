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

BASE_URL = http://downloads.sourceforge.net/project/libusb/$(DLPACKAGE)-$(VER_MM)%20%28LEGACY%29/$(VERSION)

# They moved the legacy lib again. Adjust accordingly.
DOWNLOAD = yes
download:
	@$(PRE_DL) $(DL_CMD) $(BASE_URL)/$(DLPACKAGE)-$(VERSION)$(EXTENSION) $(MD5)

PREPARE = yes
$(DIR)/: download
	@tar -xvf $(DOWNLOADS_DIR)/$(DLPACKAGE)-$(VERSION)$(EXTENSION)
	@mv $(DLPACKAGE)-$(VERSION) $(PACKAGE)-$(VERSION)

include ../Makefile.rules
