# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = binutils
VERSION = $(BIN_VER)
EXTENSION = .tar.bz2
COMPILE_DIR = $(DIR)-compile
BASE_URL = http://ftp.gnu.org/gnu/binutils

# Tool Chain Build Stage 1 binutils
#
ifeq ($(BUILD_PHASE), Stage_1)

PATCH = yes
patch: $(DIR)/
	# Prevent installing libiberty to lib64.
	cd $(DIR) && sed -i 's%\(^MULTIOSDIR = \).*%\1 ../lib%' libiberty/Makefile.in

CONFIG_OPTS = \
		--prefix=$(TOOLS_DIR) \
		--target=$(SWE_TGT) \
		--with-sysroot=$(SWE_ROOT) \
		--with-lib-path=$(TOOLS_DIR)/lib \
		--disable-nls \
		--disable-werror \
		--enable-new-dtags \
		--enable-gprofng=no \
		--enable-64-bit-bfd \
		--enable-default-hash-style=gnu

INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
ifeq ($(BITS_64), yes)
	mkdir -pv $(TOOLS_DIR)/lib
	ln -sv lib $(TOOLS_DIR)/lib64
endif
	@echo; echo; echo "Installing binutils "; echo
	make -C $(COMPILE_DIR) DESTDIR=$(SWE_ROOT) install
endif # Stage 1

# Tool Chain Build Stage 2 binutils
#
ifeq ($(BUILD_PHASE), Stage_2)

PRE_CONFIGURE = CC=$(SWE_TGT)-gcc \
	        AR=$(SWE_TGT)-ar RANLIB=$(SWE_TGT)-ranlib

CONFIG_OPTS = \
		--prefix=$(TOOLS_DIR) \
		--build=$(SWE_TGT) \
		--host=$(SWE_TGT) \
		--target=$(SWE_TGT) \
		--disable-nls \
		--with-lib-path=$(TOOLS_DIR)/lib \
		--with-sysroot
#		--disable-werror

ifeq ($(mARCH), arm64)
CONFIG_OPTS += --host=$(SWE_TGT)
endif

INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	$(MAKE) -C $(COMPILE_DIR) install
	
	@ # Get ready for second adjusting
	@echo; echo; echo 'Prepare the linker for the “Re-adjusting” phase'; echo
	$(MAKE) -C $(COMPILE_DIR)/ld clean
	$(MAKE) $(JOBS) -C $(COMPILE_DIR)/ld LIB_PATH=/usr/lib:/lib
	cp -v  $(COMPILE_DIR)/ld/ld-new $(TOOLS_DIR)/bin
endif # Stage 2

# Final Build Stage binutils
#
ifeq ($(BUILD_PHASE), Final)

CONFIG_OPTS = \
		--prefix=$(PKG_DIR) \
	    --host=$(FINAL_TGT) \
	    --build=$(FINAL_TGT) \
	    --target=$(FINAL_TGT) \
		--disable-gold \
		--enable-ld=default \
		--enable-plugins \
		--enable-shared \
		--disable-werror \
		--with-system-zlib

PATCH = yes
patch: $(DIR)/
	@echo; echo; echo "Patch"; echo
	cd $(DIR); tar -xf ../../../downloads/gmp-$(GMP_VER).tar.xz; mv gmp-$(GMP_VER) gmp
	cd $(DIR); tar -xf ../../../downloads/mpfr-$(MPFR_VER).tar.bz2; mv mpfr-$(MPFR_VER) mpfr

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"; echo
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) tooldir=$(PKG_DIR)
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	mkdir -vp $(PKG_ROOT)$(PKG_DIR)/include
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) tooldir=$(PKG_DIR) install
	cp -v $(DIR)/include/libiberty.h $(PKG_ROOT)$(PKG_DIR)/include

	@echo; echo; echo "adjust"; echo
	gcc -print-libgcc-file-name

adjust:
	@echo; echo; echo "adjust"; echo
	gcc -print-libgcc-file-name
#	# Return specs file to 'au natural'
#	GCC_LIBNAM=`gcc -print-libgcc-file-name`; \
#	  GCC_LIBNAMDIR=`dirname $${GCC_LIBNAM}`; \
#	  rm -fv $${GCC_LIBNAMDIR}/specs
#
#	make -C $(COMPILE_DIR)/ld INSTALL=$(PKG_ROOT)$(PKG_DIR)/bin/install install
endif # Final

include ../Makefile.rules
