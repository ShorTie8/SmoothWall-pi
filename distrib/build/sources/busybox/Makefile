# Copyright 2004-2013 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = busybox
VERSION = 1.37.0
EXTENSION = .tar.bz2
LICENCE_FILE = $(DIR)/LICENSE
PKG_DIR = /opt/busybox
BASE_URL = http://busybox.net/downloads/

CONFIGURE = yes
configure: patch
	@echo -e "\n\nConfigure\n"
	cp -av config $(DIR)/.config
	cd $(DIR); make oldconfig

COMPILE = yes
compile: configure
	@echo -e "\n\nCompile\n"
	$(MAKE) $(JOBS) -C $(DIR) V=1

INSTALL = yes
install: compile
	@echo -e "\n\ninstall\n"
	mkdir -vp $(PKG_ROOT)/bin
	#install -D -v -m755 $(DIR)/busybox $(PKG_ROOT)/bin/;
	$(MAKE) $(JOBS) -C $(DIR) CONFIG_PREFIX=$(PKG_ROOT)$(PKG_DIR) install
	@echo
	cp -v $(DIR)/busybo* $(PKG_ROOT)/bin
#	for I in $$($(PKG_ROOT)$(PKG_DIR)/bin/busybox --list); do \
#	    ln -svf busybox $(PKG_ROOT)$(PKG_DIR)/bin/$$I; done


BUILDTARBALL = yes
$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: install
	@echo; echo; echo "build-tarball"
	ls $(PKG_ROOT)/bin
	cd $(PKG_ROOT); \
		tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz bin/busybox bin/busybox.links

	#tar -zcf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) .
	echo "Need busybox.links"
	#tar -zcf /build/target/smoothwall-busybox.tar.gz -C /build/buildroot/busybox .
	#cd $(DIR); tar -zcf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz \
	#	busybox busybox.links busybox_unstripped busybox_unstripped.map busybox_unstripped.out


	ls $(DIR)/busy*
	@echo; echo; echo "install tarball"
	echo "Do not untar, or mess up chroot"
	#tar -zvxf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C /


include ../Makefile.rules
