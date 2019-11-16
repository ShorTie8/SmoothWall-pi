# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

INSTALL_ROOT = installroot

include ../../Makefile.versions
include ../../Makefile

all: clean
	@mkdir isolinux

	@cp -R syslinux.cfg isolinux/isolinux.cfg
	@cp -R /build/buildroot/syslinux/usr/lib/syslinux/isolinux.bin isolinux/
	@cp -R dosfiles/message.txt dosfiles/message.lss isolinux/
	@cp -R /build/buildroot/kernel-runtime/boot/vmlinuz-$(KERNEL_VER)-$(KERNEL_PL)-runtime isolinux/vmlinuz

	@make -C ../installroot MEDIA=$(MEDIA)
	@cp -R ../$(INSTALL_ROOT)image.bz2 isolinux/initrd.img

clean:
	@rm -rf isolinux/
	@make -C ../installroot clean
