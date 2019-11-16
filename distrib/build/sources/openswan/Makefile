# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = $(FREESWAN_TYPE)
VERSION = $(FREESWAN_VER)

BASE_URL = http://www.openswan.org/download/

TARBALL = $(FREESWAN_TYPE)-$(VERSION)

PATCH_FILE1 = makefile.patch
PATCH_FILE2 = setup.in.patch
#PATCH_FILE3 = klips_proc_net.patch
#PATCH_FILE4 = ip_select_ident.patch

KNL_SRC = $(SOURCES_DIR)/linux$(KERNEL_TYPE)/linux
MOD_DEST = /lib/modules/$(K_RAW_VERSION)$(KERNEL_TYPE)/kernel/net/ipsec

unpack: $(DIR)/
	@true

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	rm -f /tools/bin/xmlto
	cp xmlto /tools/bin
	chmod 555 /tools/bin/xmlto
	@true
	
JOBS := -j 1

CFLAGS:=$(CFLAGS) -fno-strict-aliasing
compile: configure
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) V=1 USERCOMPILE='$(CFLAGS)' KLIPSCOMPILE='$(CFLAGS)' INC_USRLOCAL=$(PKG_DIR) FINALCONFDIR=$(PKG_DIR)/etc FINALRCDIR=$(PKG_DIR)/bin KERNELSRC=$(KNL_SRC) programs
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) V=1 USERCOMPILE='$(CFLAGS)' KLIPSCOMPILE='$(CFLAGS)' INC_USRLOCAL=$(PKG_DIR) FINALCONFDIR=$(PKG_DIR)/etc FINALRCDIR=$(PKG_DIR)/bin KERNELSRC=$(KNL_SRC) module


install: compile
ifeq ($(BUILD_PHASE), Final)
	@mkdir -p $(PKG_ROOT)${PKG_DIR}
endif
	@$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) INC_USRLOCAL=$(PKG_DIR) FINALCONFDIR=$(PKG_DIR)/etc FINALRCDIR=$(PKG_DIR)/bin KERNELSRC=$(KNL_SRC) install minstall
	@rm -rf $(PKG_ROOT)$(PKG_DIR)/rc* $(PKG_ROOT)$(PKG_DIR)/etc/ipsec.conf $(PKG_ROOT)/var


include ../Makefile.rules

# Obsolete as long as the patch works
	#mkdir -p $(PKG_ROOT)$(MOD_DEST)
	#mkdir -p $(MOD_DEST)
	#cp $(COMPILE_DIR)/modobj26/ipsec.ko $(PKG_ROOT)$(MOD_DEST)
	#cp $(COMPILE_DIR)/modobj26/ipsec.ko $(MOD_DEST)
