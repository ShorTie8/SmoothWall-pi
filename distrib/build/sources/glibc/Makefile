# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = glibc
VERSION = 2.42
EXTENSION = .tar.bz2
COMPILE_DIR = $(DIR)-compile
BASE_URL =  https://ftp.gnu.org/gnu/glibc
TZ_VERSION = 2025a
TZ_TARBALL = tzdata$(TZ_VERSION).tar.gz
TZ_URL =  http://www.iana.org/time-zones/repository/releases/$(TZ_TARBALL)

PATCH_FILE1 = glibc-$(VERSION)-fhs-1.patch
PATCH_URL1 = https://www.linuxfromscratch.org/patches/lfs/12.4/glibc-2.42-fhs-1.patch

PATCH_FILE2 = glibc-2.42-upstream_fixes-1.patch
PATCH_URL2 = http://linuxfromscratch.org/patches/downloads/glibc/$(PATCH_FILE2)

DOWNLOAD = yes
download:
	@echo; echo; echo "Downloading glibc "; echo
	@$(DL_CMD) $(BASE_URL)/$(PACKAGE)-$(VERSION)$(EXTENSION)
	@$(DL_CMD) $(TZ_URL)

# Tool Chain Build Stage 1 glibc
#
ifeq ($(BUILD_PHASE), Stage_1)

CONFIG_OPTS = \
		--prefix=$(TOOLS_DIR) \
		--host=$(SWE_TGT) \
		--enable-kernel=3.2  \
		--enable-obsolete-rpc \
		--with-headers=$(TOOLS_DIR)/include \
		--disable-werror \
		libc_cv_forced_unwind=yes \
		libc_cv_c_cleanup=yes
#		--disable-werror

INSTALL = yes
install: compile
	@echo; echo; echo "Installing glibc "; echo
	make -C $(COMPILE_DIR) DESTDIR=$(SWE_ROOT) install

endif # Stage 1

# Final compile glibc
#
ifeq ($(BUILD_PHASE), Final)

PATCH = yes
patch: $(DIR)/
	@echo; echo; echo "PrePare"; echo
	mkdir -vp $(COMPILE_DIR)
	@echo; echo; echo "Patch"; echo
	cd $(DIR); ln -sfv $(TOOLS_DIR)/lib/gcc /usr/lib

	@echo; echo "links"
ifeq ($(mARCH), x86_64)
	ln -sfv ld-linux-x86-64.so.2 /lib/ld-lsb-x86-64.so.3
else ifeq ($(mARCH), arm64)
	ln -sfv ld-linux-aarch64.so.1 /lib/ld-lsb-aarch64.so.2
else
	ln -sfv ld-linux.so.2 /lib/ld-lsb.so.3
endif
	# Remove a file that may be left over from a previous build attempt:
	rm -vf /usr/include/limits.h

CONFIG_OPTS = \
	      --prefix=$(PKG_DIR) \
	      --build=$(FINAL_TGT) \
	      --enable-kernel=3.2 \
	      --enable-obsolete-rpc \
	      --libexecdir=/usr/lib/glibc \
	      --enable-stack-protector=strong \
	--disable-profile \
	--enable-kernel=5.4.0 \
	--enable-add-ons \
	--without-selinux \
	--enable-experimental-malloc \
	--enable-bind-now \
	--enable-fortify-source \
	--enable-stack-protector=strong \
	--disable-crypt \
	--disable-build-nscd \
	--disable-nscd \
	      libc_cv_slibdir=/lib

ifeq ($(mARCH), x86_64)
CONFIG_OPTS += \
		--enable-cet \
		--enable-sframe
endif

ifeq ($(mARCH), arm64)
CONFIG_OPTS += \
		--enable-memory-tagging \
		--enable-sframe
endif
CONFIGURE = yes
configure: patch
	@echo; echo "Configure"; echo
	(cd $(COMPILE_DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" $(PRE_CONFIGURE) ../$(DIR)/configure $(CONFIG_OPTS))
	unset GCC_INCDIR

COMPILE = yes
compile: configure
	@echo; echo "Compiling"; echo
	$(MAKE) ${JOBS} -C $(COMPILE_DIR)
	cp -v $(DIR)/iconvdata/gconv-modules $(COMPILE_DIR)/iconvdata
	mkdir -p $(PKG_ROOT)/etc && touch $(PKG_ROOT)/etc/ld.so.conf

# post-compile is an 'orphan': a standalone target to run the tests
post-compile: compile
	@echo; echo "Post-Compile"
	+cd $(COMPILE_DIR); $(MAKE) $(JOBS) -k check 2>&1 | tee glibc-check-log
	+cd $(COMPILE_DIR); grep Error glibc-check-log

INSTALL = yes
install: compile
#install: post-compile
	@echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)/lib
	mkdir -vp $(PKG_ROOT)/usr/lib
ifeq ($(BITS_64), yes)
	mkdir -vp $(PKG_ROOT)/lib64
	mkdir -vp $(PKG_ROOT)/usr/lib64
	(cd $(PKG_ROOT); ln -sv lib lib64)
	(cd $(PKG_ROOT)/usr; ln -sv lib lib64)
endif

	touch $(PKG_ROOT)/etc/ld.so.conf
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) install_root=$(PKG_ROOT) install
	cd $(COMPILE_DIR); cp -v ../glibc-$(VERSION)/sunrpc/rpc/*.h $(PKG_ROOT)/usr/include/rpc
	@echo; echo "install-locales"; echo
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) localedata/install-locales
	( \
	  cd $(COMPILE_DIR); \
	  tar -xf $(DOWNLOADS_DIR)/$(TZ_TARBALL); \
	  ZONEINFO=$(PKG_ROOT)/usr/share/zoneinfo; \
	  mkdir -pv $$ZONEINFO/{posix,right}; \
	  for tz in etcetera southamerica northamerica europe africa antarctica \
	      asia australasia backward pacificnew \
	      systemv; do \
	    zic -L /dev/null   -d $$ZONEINFO       -y "sh yearistype.sh" $${tz}; \
	    zic -L /dev/null   -d $$ZONEINFO/posix -y "sh yearistype.sh" $${tz}; \
	    zic -L leapseconds -d $$ZONEINFO/right -y "sh yearistype.sh" $${tz}; \
	  done; \
	  cp -v zone.tab iso3166.tab $$ZONEINFO; \
	  zic -d $$ZONEINFO -p America/New_York; \
	)
#endif

# buildtarball
BUILDTARBALL = yes
$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: install
	@echo; echo "Buildtarball"
	tar -zcf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) .
	@echo; echo "install tarball"
	tar -xf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C / --exclude ./etc/localtime

endif # Final

include ../Makefile.rules
