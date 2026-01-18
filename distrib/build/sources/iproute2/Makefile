# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = iproute2
VERSION = 6.9.0
EXTENSION=.tar.gz
BASE_URL = https://www.kernel.org/pub/linux/utils/net/iproute2/

PATHS = SBINDIR=/usr/sbin CONFDIR=/etc/iproute2 DOCDIR=/usr/share/doc/iproute2 MANDIR=/usr/share/man LIBDIR=/usr/lib/

CONFIGURE = yes
configure: patch
	@sed -i '/^TARGETS/s@ arpd@@g' $(COMPILE_DIR)/misc/Makefile

COMPILE = yes
compile: configure
	cd $(COMPILE_DIR); sed -i -e 's/^CCOPTS.*/CCOPTS = -O2 $(CFLAGS)/' Makefile
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) KERNEL_INCLUDE=/usr/include $(PATHS)
	ln -s $(DIR) $(PACKAGE)

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) MODDESTDIR=$(PKG_ROOT)/lib/tc $(PATHS) install

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
	@rm -f $(PACKAGE)
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
