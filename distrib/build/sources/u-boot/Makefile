# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2016
#
# This code is distributed under the terms of the GPL v2.

# http://www.linuxfromscratch.org/blfs/view/svn/basicnet/libnl.html

include ../Makefile.conf

PACKAGE = u-boot
VERSION = 5422_4.4.4_v5.3
TARBALL = 5422_4.4.4_v5.3

BASE_URL = https://github.com/hardkernel/u-boot/archive

DIR = u-boot-5422_4.4.4_v5.3
#COMPILE_DIR = $(DIR)-compile

DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo
	$(DL_CMD) $(BASE_URL)/$(TARBALL).tar.gz
#	mkdir -v $(COMPILE_DIR)

CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	cd $(DIR); make odroid_config

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)/{boot,usr/bin}
	install -m 0755 -D $(DIR)/sd_fuse/sd_fusing.sh $(PKG_ROOT)/boot
	install -m 0755 -D $(DIR)/sd_fuse/bl* $(PKG_ROOT)/boot
	install -m 0755 -D $(DIR)/sd_fuse/tzsw.bin.hardkernel $(PKG_ROOT)/boot
	install -m 0755 -D $(DIR)/sd_fuse/u-boot.bin.hardkernel $(PKG_ROOT)/boot
	install -m 0755 -D $(DIR)/tools/mkimage $(PKG_ROOT)/usr/bin
	
#	cp -v $(DIR)/sd_fuse/sd_fusing.sh $(PKG_ROOT)/boot
#	cp -v $(DIR)/sd_fuse/bl* $(PKG_ROOT)/boot
#	cp -v $(DIR)/sd_fuse/tzsw.bin.hardkernel $(PKG_ROOT)/boot
#	cp -v $(DIR)/sd_fuse/u-boot.bin.hardkernel $(PKG_ROOT)/boot
#	cp -v $(DIR)/tools/mkimage $(PKG_ROOT)/usr/bin

#	mkdir -vp $(PKG_ROOT)/usr/{bin,share/5422_uboot}
#	cp -v $(DIR)/sd_fuse/sd_fusing.sh $(PKG_ROOT)/usr/bin
#	cp -v $(DIR)/sd_fuse/bl* $(PKG_ROOT)/usr/share/5422_uboot
#	cp -v $(DIR)/sd_fuse/tzsw.bin.hardkernel $(PKG_ROOT)/usr/share/5422_uboot
#	cp -v $(DIR)/sd_fuse/u-boot.bin.hardkernel $(PKG_ROOT)/usr/share/5422_uboot
#	cp -v $(DIR)/tools/mkimage $(PKG_ROOT)/usr/bin

	# ??
	# cp -v $(DIR)/tools/mkimage ../media-sdcard/mkimage

include ../Makefile.rules

