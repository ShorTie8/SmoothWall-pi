# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = kernel-headers
#VERSION = $(KERNEL_VER)
VERSION = $(KERNELHEADERVER)

CFG_TYPE := $(KERNEL_TYPE)-$(mTUPLE)-$(KERNEL_MMR)
#CFG_TYPE := $(KERNEL_TYPE)-$(mARCH)

download:
	@echo; echo "download"
	$(DL_CMD) $(KERNEL_URL)

install: download
ifeq ($(mARCH),$(mTUPLE))
	tar -xf $(DOWNLOADS_DIR)/linux-$(KERNELHEADERVER).tar.xz
else ifeq ($(mTUPLE),$(filter $(mTUPLE),pi0w rpi2 rpi3 pi3-64 rpi4 pi4-64 rpi5))
	tar -xf $(DOWNLOADS_DIR)/linux-rpi-$(KERNEL_VER).tar.gz
	#unzip -q $(DOWNLOADS_DIR)/linux-$(KERNEL_COM).zip
	mv linux-$(KERNEL_COM) linux-$(KERNEL_VER)
else
	$(info Unsupported kernel-headers)
	$(error FAIL)
endif





ifeq ($(BUILD_PHASE), Stage_1)
	+cd linux-$(KERNELHEADERVER); \
	  make mrproper; \
	  make ARCH=$(mARCH) INSTALL_HDR_PATH=dest headers_install; \
	  cp -rv dest/include/* $(TOOLS_DIR)/include
endif

ifeq ($(BUILD_PHASE), Final)
#	sed -i -e '/SO_REUSEPORT/c #define SO_REUSEPORT	15' linux-${KERNELHEADERVER}/include/asm-generic/socket.h
	+mkdir -vp $(PKG_ROOT); \
	cd linux-$(KERNEL_VER); \
	  make mrproper
	cd linux-$(KERNEL_VER); \
	  make ARCH=$(mARCH) INSTALL_HDR_PATH=$(PKG_ROOT)$(PKG_DIR) headers_install
	find $(PKG_ROOT)$(PKG_DIR)/include \( -name .install -o -name ..install.cmd \) -delete
endif

build-tarball: install
	@(cd $(PKG_ROOT); \
	echo; echo; echo "build-tarball"; \
	tar -zcf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz .; \
	echo; echo; echo "install tarball"; \
	tar -xvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C /);

clean:
ifndef BUILD_PHASE
	@echo -n " $(PACKAGE)"
	@rm -rf linux-$(KERNEL_VER)
else
	@echo " $(PACKAGE)"
	@echo; echo "clean"
	rm -f linux
	rm -rf linux-$(KERNEL_VER)
endif

ifeq ($(BUILD_PHASE), Final)
	rm -rf $(PKG_ROOT)
	rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

all: build-tarball
