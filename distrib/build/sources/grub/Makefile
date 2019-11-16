# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

# Confuser: This is grub-legacy, which is still, inexplicably, named grub.
#   So it's built as grub, but tarred and stored as grub-legacy.
#   Grub-legacy is installed in .../distrib.
#   Grub is installed in installroot and runtimeroot.
#   Grub and grub-legacy do not need to co-exist in any filesystem.
# Grub is also needed to convert the ISO to flash. Thus it has to be
#   available in the installroot initramfs and it has to be available
#   via /distrib in the chroot build environment.
# Grub-legacy is not needed in the build environment or in the installroot
#   tree; it is needed only on the installed hard drive.

include ../Makefile.conf

PACKAGE = grub
VERSION = 0.97

ifeq ($(BITS_32), yes)

TARBALL = grub-$(VERSION)
BASE_URL = ftp://alpha.gnu.org/gnu/grub/

COMPILE_DIR = $(PACKAGE)-$(VERSION)-compile

PATCH_FILE1 = grub-fedora-17.patch
PATCH_FILE2 = serial.c.patch
PATCH_FILE3 = builtins.c.patch
#PATCH_FILE4 = stage2.c.patch

PRE_CONFIGURE = LDFLAGS=-static CFLAGS="$(CFLAGS) -Os -Wall -fno-reorder-functions"
CONFIG_OPTS += --prefix=$(PKG_DIR)

reconf: patch
	cd $(DIR); autoreconf --force

CONFIGURE = yes
configure: reconf
	(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
	(cd $(COMPILE_DIR); $(PRE_CONFIGURE) ../$(DIR)/configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=${PKG_ROOT} install
	mkdir -pv ${PKG_ROOT}/boot/grub
	cp -av ${PKG_ROOT}/usr/share/grub/*/* $(PKG_ROOT)/boot/grub
	touch ${PKG_ROOT}/boot/grub/default

BUILDTARBALL = yes
$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: install
	@tar cvfz $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) .
	@cp $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz \
	    $(DOWNLOADS_DIR)/smoothwall-$(PACKAGE)-$(mARCH).tar.gz
	@tar xvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C /

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(PACKAGE)-$(VERSION)
	@rm -rf $(COMPILE_DIR)
	@rm -rf $(PKG_ROOT)

endif

ifeq ($(BITS_64), yes)
BASE_URL = http://downloads.smoothwall.org/buildmirror

TARBALL = smoothwall-$(PACKAGE)-$(ARCH32)

INSTALL = yes
CLEAN = yes

install: download
	$(MAKE) clean
	@mkdir $(PKG_ROOT)
	@tar -xvf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION) -C $(PKG_ROOT)

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(PACKAGE)-$(VERSION)
	@rm -rf $(DIR) $(DIR)-compile
	@rm -rf $(PKG_ROOT)
        
endif

include ../Makefile.rules
