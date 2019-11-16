# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = glibc
VERSION = 2.18

EXTENSION = .tar.bz2

BASE_URL =  ftp://ftp.gnu.org/gnu/glibc
TZ_VERSION = 2018g
TZ_TARBALL = tzdata$(TZ_VERSION).tar.gz
TZ_URL =  http://www.iana.org/time-zones/repository/releases/$(TZ_TARBALL)

COMPILE_DIR = $(DIR)-compile

DOWNLOAD = yes
download:
	@$(DL_CMD) $(BASE_URL)/$(PACKAGE)-$(VERSION)$(EXTENSION)
	@$(DL_CMD) $(TZ_URL)

# Phase 1 compile
#
ifeq ($(BUILD_PHASE), Stage_1)

# Phase 1 glibc builds with phase 1 binutils/gcc (SWE_TGT)
CONFIG_OPTS = \
	      --host=$(SWE_TGT) \
              --build=$(FINAL_TGT) \
              --target=$(FINAL_TGT) \
	      --prefix=$(TOOLS_DIR) \
	      --disable-profile \
	      --enable-kernel=2.6.32  \
	      --with-headers=$(TOOLS_DIR)/include \
	      libc_cv_forced_unwind=yes \
	      libc_cv_ctors_header=yes \
	      libc_cv_c_cleanup=yes
#	      --enable-add-ons \

PREPARE = yes
# Prepare
$(DIR)/: download
	tar -xvf $(DOWNLOADS_DIR)/$(DIR)$(EXTENSION)
	mkdir -p $(COMPILE_DIR)
ifeq ($(mARCH),$(ARCH32))
ifeq ($(mARCH),i386)
	echo "CFLAGS += -march=i486 -mtune=generic" > $(COMPILE_DIR)/configparms
else
	echo "CFLAGS += -march=$(mARCH) -mtune=generic" > $(COMPILE_DIR)/configparms
endif
endif
	cd $(DIR); sed -i -e 's/static __m128i/inline &/' sysdeps/x86_64/multiarch/strstr.c
	cd $(DIR); sed -i -e 's/3\.79/4.* | 3.79/' configure


COMPILE = yes
INSTALL = yes
BUILDTARBALL = yes

compile: configure
	cd $(DIR); sed -i 's/ -lgcc_s//' Makeconfig
	$(MAKE) ${JOBS} -C $(COMPILE_DIR)

install: compile
	$(MAKE) -C $(COMPILE_DIR) install
endif


# Final compile
#

ifeq ($(BUILD_PHASE), Final)

BUILD = --build=$(SWE_TGT)

CONFIG_OPTS = \
              --host=$(FINAL_TGT) \
              --build=$(FINAL_TGT) \
              --target=$(FINAL_TGT) \
	      --prefix=$(PKG_DIR) \
	      --disable-profile \
	      --enable-kernel=2.6.32 \
	      --libexecdir=/usr/lib/glibc \
	      --enable-obsolete-rpc

#	      --enable-add-ons \

PREPARE = yes
# Prepare
$(DIR)/: download
	tar -xvf $(DOWNLOADS_DIR)/$(DIR)$(EXTENSION)
	cd $(DIR); \
	  DL=$$(readelf -l /bin/sh | sed -n 's@.*interpret.*/tools\(.*\)]$$@\1@p') \
	  sed -i "s|libs -o|libs -L/usr/lib -Wl,-dynamic-linker=$$DL -o|" \
	  scripts/test-installation.pl; \
	  unset DL
	cd $(DIR); \
	  sed -i 's|@BASH@|/bin/bash|' elf/ldd.bash.in; \
	  sed -i -e 's/"db1"/& \&\& $$name ne "nss_test1"/' \
	    scripts/test-installation.pl; \
	  sed -i '195,213 s/PRIVATE_FUTEX/FUTEX_CLOCK_REALTIME/' \
	    nptl/sysdeps/unix/sysv/linux/x86_64/pthread_rwlock_timed{rd,wr}lock.S
	mkdir -p $(COMPILE_DIR)
ifeq ($(mARCH),$(ARCH32))
ifeq ($(mARCH),i386)
	echo "CFLAGS += -march=i486 -mtune=generic -O3 -pipe" > $(COMPILE_DIR)/configparms
else
	echo "CFLAGS += -march=$(mARCH) -mtune=generic -O3 -pipe" > $(COMPILE_DIR)/configparms
endif
endif
	cd $(DIR); sed -i -e 's/static __m128i/inline &/' sysdeps/x86_64/multiarch/strstr.c
	cd $(DIR); sed -i -e 's/3\.79/4.* | 3.79/' configure


COMPILE = yes
INSTALL = yes

compile: configure
	$(MAKE) ${JOBS} -C $(COMPILE_DIR)
	cp -v $(DIR)/iconvdata/gconv-modules $(COMPILE_DIR)/iconvdata
	mkdir -p $(PKG_ROOT)/etc && touch $(PKG_ROOT)/etc/ld.so.conf

# post-compile is an 'orphan': a standalone target to run the tests
post-compile: compile
	+cd $(COMPILE_DIR); $(MAKE) $(JOBS) -k check 2>&1 | tee glibc-check-log
	+cd $(COMPILE_DIR); grep Error glibc-check-log

install: compile
	mkdir -p $(PKG_ROOT)/lib
	mkdir -p $(PKG_ROOT)/usr/lib

ifeq ($(BITS_64), yes)
	(cd $(PKG_ROOT); ln -s lib lib64)
	(cd $(PKG_ROOT)/usr; ln -s lib lib64)
endif

	touch $(PKG_ROOT)/etc/ld.so.conf
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) install_root=$(PKG_ROOT) install
	cd $(COMPILE_DIR); cp -v ../glibc-2.18/sunrpc/rpc/*.h $(PKG_ROOT)/usr/include/rpc
	cd $(COMPILE_DIR); cp -v ../glibc-2.18/sunrpc/rpcsvc/*.h $(PKG_ROOT)/usr/include/rpcsvc
	cd $(COMPILE_DIR); cp -v ../glibc-2.18/nis/rpcsvc/*.h $(PKG_ROOT)/usr/include/rpcsvc
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) localedata/install-locales
	( \
	  cd $(COMPILE_DIR); \
	  tar -xf $(DOWNLOADS_DIR)/$(TZ_TARBALL); \
	  ZONEINFO=$(PKG_ROOT)/usr/share/zoneinfo; \
	  mkdir -pv $$ZONEINFO/{posix,right}; \
	  for tz in etcetera southamerica northamerica europe africa antarctica \
	      asia australasia backward pacificnew solar87 solar88 solar89 \
	      systemv; do \
	    zic -L /dev/null   -d $$ZONEINFO       -y "sh yearistype.sh" $${tz}; \
	    zic -L /dev/null   -d $$ZONEINFO/posix -y "sh yearistype.sh" $${tz}; \
	    zic -L leapseconds -d $$ZONEINFO/right -y "sh yearistype.sh" $${tz}; \
	  done; \
	  cp -v zone.tab iso3166.tab $$ZONEINFO; \
	  zic -d $$ZONEINFO -p America/New_York; \
	)
endif

BUILDTARBALL = yes

# buildtarball
$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: install
	@tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) .
	@tar -xvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C / --exclude ./etc/localtime

include ../Makefile.rules
