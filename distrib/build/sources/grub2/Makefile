# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.
#
# http://www.linuxfromscratch.org/lfs/view/development/chapter06/grub.html
# http://www.linuxfromscratch.org/lfs/view/development/chapter08/grub.html

include ../Makefile.conf

PACKAGE = grub2
VERSION = 2.02
DIR = grub-$(VERSION)
EXTENSION = .tar.xz
TARBALL = grub-$(VERSION)
BASE_URL = https://ftp.gnu.org/gnu/grub

CXXFLAGS=""
CFLAGS=""

#CONFIG_OPTS += --sbindir=/sbin  \

CONFIG_OPTS = --prefix=/usr \
			--sbindir=/sbin  \
			--sysconfdir=/etc \
			--disable-efiemu \
			--disable-werror

			#  \
			#--disable-werror


CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	(cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure $(CONFIG_OPTS))



#BUILDTARBALL = yes
#$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: install
#	tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) .

include ../Makefile.rules
