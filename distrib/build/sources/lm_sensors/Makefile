# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = lm_sensors
VERSION = 3.4.0

EXTENSION = .tar.bz2

BASE_URL = https://ftp.gwdg.de/pub/linux/misc/lm-sensors
#BASE_URL = http://dl.lm-sensors.org/lm-sensors/releases/
#https://github.com/groeck/lm-sensors/archive/V3-4-0.tar.gz

PATCH_FILE1 = Makefile.patch

CONFIGURE = yes
COMPILE = yes
INSTALL = yes
CLEAN = yes

configure: patch
	@true

compile: configure
	make $(JOBS) -C $(DIR) PREFIX=$(PKG_DIR) all

install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(DIR) PREFIX=$(PKG_DIR) DESTDIR=$(PKG_ROOT) install

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
