# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = nss
VERSION = 3.33

BASE_URL = https://ftp.mozilla.org/pub/security/$(PACKAGE)/releases/NSS_3_33_RTM/src

DIR=$(PACKAGE)-$(VERSION)/nss

PATCH_FILE1 = nss-3.33-standalone-1.patch

DIR = $(PACKAGE)-$(VERSION)/nss

PATCH = yes
patch: $(DIR)/
	cd $(DIR); patch -Np2 -i ../../$(PATCH_FILE1)

CONFIGURE = yes
configure: patch
	true
	sed -i -e 's/\(OS_REL_CFLAGS.*-Di386\)/\1 -march=i586 -mtune=generic/' $(PACKAGE)-$(VERSION)/$(PACKAGE)/coreconf/Linux.mk

COMPILE = yes
MAKE_DEFS = BUILD_OPT=1 \
	    NSPR_INCLUDE_DIR=/usr/include/nspr \
	    NSS_USE_SYSTEM_SQLITE=1 \
	    USE_SYSTEM_ZLIB=1 \
	    ZLIB_LIBS=-lz
ifeq ($(BITS_64), yes)
  MAKE_DEFS += USE_64=1
endif

compile: configure
	cd $(DIR); make $(MAKE_DEFS)

INSTALL = yes
install: compile
	cd $(DIR)/../dist; \
	  mkdir -p ${PKG_ROOT}/usr/lib ${PKG_ROOT}/usr/bin ${PKG_ROOT}/usr/lib/pkgconfig; \
	  install -v -m755 Linux*/lib/*.so              ${PKG_ROOT}/usr/lib; \
	  install -v -m644 Linux*/lib/{*.chk,libcrmf.a} ${PKG_ROOT}/usr/lib; \
	  install -v -m755 -d                           ${PKG_ROOT}/usr/include/nss; \
	  cp -v -RL {public,private}/nss/*              ${PKG_ROOT}/usr/include/nss; \
	  chmod -v 644                                  ${PKG_ROOT}/usr/include/nss/*; \
	  install -v -m755 Linux*/bin/{certutil,nss-config,pk12util} ${PKG_ROOT}/usr/bin; \
	  install -v -m644 Linux*/lib/pkgconfig/nss.pc  ${PKG_ROOT}/usr/lib/pkgconfig


CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(PACKAGE)-$(VERSION)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	@mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz

include ../Makefile.rules
