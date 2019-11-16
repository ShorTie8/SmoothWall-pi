# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = install
VERSION = 0.0

compile:
	@make -C $(COMPILE_DIR)

install: compile
	@install -D $(COMPILE_DIR)/install/install $(TARGET_DIR)/$(PACKAGE)-0.0-$(mARCH)

all: install
	@true

clean:
	@echo -n " $(PACKAGE)"
	@make -C $(COMPILE_DIR) clean
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

download:
	@true

packageinfo.html: clean
	@echo "<li><span style='font-size:large;'>$(PACKAGE) $(VERSION)</span><br>" >>/tmp/packageinfo.html
	@tar --exclude .svn -zcvf /tmp/downloads/$(TARBALL).tar.gz $(DIR)
	@echo "Download: <a href='downloads/$(TARBALL).tar.gz'>$(TARBALL).tar.gz</a><br>" >>/tmp/packageinfo.html
	
