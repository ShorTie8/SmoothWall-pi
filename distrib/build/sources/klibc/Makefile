# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

# in deconfig
# CONFIG_AEABI is not set


PACKAGE = klibc
VER_MM = 2.0
VERSION = $(VER_MM).4
EXTENSION = .tar.gz
BASE_URL = http://www.kernel.org/pub/linux/libs/klibc/$(VER_MM)/
export NO_CHECK_CERT = 1

PATCH_FILE1 = klibc_2.0.4-9.debian.tar.xz
PATCH_URL1 = http://http.debian.net/debian/pool/main/k/klibc/$(PATCH_FILE1)

ifeq ($(mTUPLE),$(mARCH))
  ARM_STUFF = 
else ifeq ($(mTUPLE), pi0w)
  ARM_STUFF = ARCH=arm CONFIG_AEABI=y CPU_ARCH=armv6 CPU_TUNE=arm1176jzf-s CONFIG_KLIBC_THUMB=n KBUILD_VERBOSE=1
else ifeq ($(mTUPLE), rpi2)
  ARM_STUFF = ARCH=arm CONFIG_AEABI=y CPU_ARCH=armv7-a CPU_TUNE=cortex-a7 CONFIG_KLIBC_THUMB=y KBUILD_VERBOSE=1
else ifeq ($(mTUPLE), rpi3)
  ARM_STUFF = ARCH=arm CONFIG_AEABI=y CPU_ARCH=armv8-a CPU_TUNE=cortex-a53 CONFIG_KLIBC_THUMB=y KBUILD_VERBOSE=1
else ifeq ($(mTUPLE), rpi4)
  ARM_STUFF = ARCH=arm CONFIG_AEABI=y CPU_ARCH=armv7 CPU_TUNE=cortex-a72 CONFIG_KLIBC_THUMB=y KBUILD_VERBOSE=1
else ifeq ($(mTUPLE), xu4)
  ARM_STUFF = ARCH=arm CONFIG_AEABI=y CPU_ARCH=armv7-a CPU_TUNE=cortex-a15 CONFIG_KLIBC_THUMB=y KBUILD_VERBOSE=1
#else
#	$(info Un-known klibc)
#	$(error FAIL)
endif

PATCH = yes
patch: $(DIR)/
	@true

CONFIGURE = yes
configure: patch
	@echo; echo; echo "patch"
	# We use configure instead of patch, because there is no configure
	tar -xf $(DOWNLOADS_DIR)/$(PATCH_FILE1)
	cd $(DIR); for p in $$(cat ../debian/patches/series); do \
		echo; echo $$p; \
		patch -p1 < ../debian/patches/$$p; \
	done

COMPILE = yes
compile: configure
	@echo; echo; echo "compile"; echo
	# KLIBCKERNELSRC defualts to ./usr, not valid in chroot, so use /usr instead
	cd $(DIR); \
	  $(MAKE) $(JOBS) V=1 prefix=/usr KLIBCKERNELSRC=/usr $(ARM_STUFF)


INSTALL = yes
install: compile
	@echo; echo; echo "compile"; echo
	mkdir -vp $(PKG_ROOT)$(PKG_DIR)
	cd $(DIR); \
	  sed -i -e 's=SRC) ARCH=SRC)/../ ARCH=' scripts/Kbuild.install; \
	  $(MAKE) V=1 INSTALLROOT=$(PKG_ROOT) prefix=/usr KLIBCKERNELSRC=/usr $(ARM_STUFF) install

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf debian
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
