# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../Makefile.versions
include ../../Makefile

GRUBFILES = grub.conf main.conf other.conf help.txt \
	    express_boot_install.xpm.gz express_boot_protect.xpm.gz

default:
	mkdir -p ../cdrom/boot/grub
	cp -a /build/buildroot/grub/usr/share/grub/i386-pc/* ../cdrom/boot/grub
	chown root:root $(GRUBFILES)
	cp -a $(GRUBFILES) ../cdrom/boot/grub/
	cp -R /build/buildroot/linux$(KERNEL_TYPE)/boot/vmlinuz-$(K_SWE_VERSION) ../cdrom/boot/vmlinuz
	cp ../installrootimage.gz ../cdrom/boot/iniramfs.igz
	echo -e "ISO boot prep complete\n\n\n\n\n"

clean:
	@rm -rf ../cdrom/boot
	@rm -rf tmp
