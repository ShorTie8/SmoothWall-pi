# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = kernel-headers
VERSION = 0.0

CFG_TYPE := $(KERNEL_TYPE)-$(mARCH)

download:
	@$(DL_CMD) $(KERNELHEADER_URL)

install: download
	@tar -xvf $(DOWNLOADS_DIR)/linux-$(KERNELHEADERVER).tar.xz
ifeq ($(BUILD_PHASE), Stage_1)
	+cd linux-$(KERNELHEADERVER); \
	  make mrproper; \
	  sed -e 's/^CONFIG_LOCALVERSION=.*$$/CONFIG_LOCALVERSION="$(KERNEL_TYPE)"/' ../../linuxheaders.config$(CFG_TYPE) > .config; \
	  make silentoldconfig; \
	  make headers_check; \
	  ln -s ../arch/x86/include/asm include/asm; \
	  cp arch/x86/include/generated/asm/* arch/x86/include/asm/; \
	  make INSTALL_HDR_PATH=dest headers_install; \
	  cp -rv dest/include/* $(TOOLS_DIR)/include
endif
ifeq ($(BUILD_PHASE), Final)
	+mkdir -p $(PKG_ROOT); \
	cd linux-$(KERNELHEADERVER); \
	  make ${JOBS} mrproper
	cd linux-$(KERNELHEADERVER); \
	  sed -e 's/^CONFIG_LOCALVERSION=.*$$/CONFIG_LOCALVERSION="$(KERNEL_TYPE)"/' ../../linuxheaders.config$(CFG_TYPE) > .config; \
	  make silentoldconfig
	cd linux-$(KERNELHEADERVER); \
	  make ${JOBS} prepare
	cd linux-$(KERNELHEADERVER); \
	  make ${JOBS} headers_check
	cd linux-$(KERNELHEADERVER); \
	  make ${JOBS} INSTALL_HDR_PATH=$(PKG_ROOT)$(PKG_DIR) headers_install
	cd linux-$(KERNELHEADERVER); \
	  find $(PKG_ROOT)$(PKG_DIR)/include \( -name .install -o -name ..install.cmd \) -delete
endif

build-tarball: install
	@(cd $(PKG_ROOT); \
	tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz .; \
	tar -xvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C /);

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf linux-$(KERNELHEADERVER)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

all: build-tarball
