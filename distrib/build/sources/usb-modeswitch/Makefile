# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = usb-modeswitch
VERSION = $(shell perl xml2txt.pl release $(PACKAGE))
PKG_URL = $(shell perl xml2txt.pl target $(PACKAGE))
#$(info VERSION=$(VERSION))
#$(info PKG_URL=$(PKG_URL))

DATA_PACKAGE = usb-modeswitch-data
DATA_VERSION = $(shell perl xml2txt.pl release $(DATA_PACKAGE))
DATA_PKG_URL = $(shell perl xml2txt.pl target $(DATA_PACKAGE))
#$(info DATA_VERSION=$(DATA_VERSION))
#$(info DATA_PKG_URL=$(DATA_PKG_URL))

EXTENSION = .tar.bz2

DOWNLOAD = yes
download:
	@$(PRE_DL) $(DL_CMD) $(PKG_URL) $(MD5)
	@$(PRE_DL) $(DL_CMD) $(DATA_PKG_URL) $(MD5)

PREPARE = yes
$(PACKAGE)-$(VERSION)/: download
	tar -xvf $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION)$(EXTENSION)
	tar -xvf $(DOWNLOADS_DIR)/$(DATA_PACKAGE)-$(DATA_VERSION)$(EXTENSION)


CONFIGURE = yes
configure: patch
	@true

COMPILE = yes
compile: configure
	cd $(DIR); make $(JOBS)

INSTALL = yes
install: compile
	cd $(DIR); make DESTDIR=$(PKG_ROOT) install
	cd $(DATA_PACKAGE)-$(DATA_VERSION); make DESTDIR=$(PKG_ROOT) install

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(PACKAGE)-$(VERSION) $(DATA_PACKAGE)-$(DATA_VERSION)
	@rm -f usb-modeswitch-versions.xml $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz

include ../Makefile.rules
