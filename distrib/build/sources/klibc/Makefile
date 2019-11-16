# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = klibc
VER_MM = 2.0
VERSION = $(VER_MM).4

EXTENSION = .tar.xz

BASE_URL = http://www.kernel.org/pub/linux/libs/klibc/$(VER_MM)/

DOWNLOAD = yes
download:
	@NO_CHECK_CERT= $(DL_CMD) $(BASE_URL)/$(TARBALL)$(EXTENSION) $(MD5)

CONFIGURE = yes
configure: patch
	true

COMPILE = yes
compile: configure
	cd $(DIR); \
	  $(MAKE) $(JOBS) V=1 prefix=/usr KLIBCKERNELSRC=/build/sources/kernel-headers/linux-$(KERNELHEADERVER)/usr/


INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)
	cd $(DIR); \
	  sed -i -e 's=SRC) ARCH=SRC)/../ ARCH=' scripts/Kbuild.install; \
	  $(MAKE) V=1 INSTALLROOT=$(PKG_ROOT) prefix=/usr KLIBCKERNELSRC=/build/sources/kernel-headers/linux-$(KERNELHEADERVER)/usr install

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
	@rm -rf linux-$(KLIBKERNVER)
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
