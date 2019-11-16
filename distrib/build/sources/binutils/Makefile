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
BASE_URL = http://ftp.gnu.org/gnu/binutils
COMPILE_DIR = $(DIR)-compile

# Tool Chain Build Stage_1
#
ifeq ($(BUILD_PHASE), Stage_1)

CONFIG_OPTS = \
		--prefix=$(TOOLS_DIR) \
		--target=$(SWE_TGT) \
		--with-sysroot=$(ROOT) \
		--with-lib-path=$(TOOLS_DIR)/lib \
		--disable-nls \
		--disable-werror

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
ifeq ($(BITS_64), yes)
	mkdir -pv $(TOOLS_DIR)/lib
	ln -sv lib $(TOOLS_DIR)/lib64
endif
	$(MAKE) -C $(COMPILE_DIR) install
endif # Stage 1


# Tool Chain Build Stage_2
#
ifeq ($(BUILD_PHASE), Stage_2)

PRE_CONFIGURE = CC=$(SWE_TGT)-gcc \
	        AR=$(SWE_TGT)-ar RANLIB=$(SWE_TGT)-ranlib

CONFIG_OPTS = \
		--prefix=$(TOOLS_DIR) \
		--disable-nls \
		--with-lib-path=$(TOOLS_DIR)/lib \
		--with-sysroot
#		--disable-werror
ifeq ($(mARCH), arm64)
CONFIG_OPTS += --host=$(SWE_TGT)
endif

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	$(MAKE) -C $(COMPILE_DIR) install
	
	@ # Get ready for second adjusting
	@echo; echo; echo 'Prepare the linker for the “Re-adjusting” phase'; echo
	$(MAKE) -C $(COMPILE_DIR)/ld clean
	$(MAKE) $(JOBS) -C $(COMPILE_DIR)/ld LIB_PATH=/usr/lib:/lib
	cp -v  $(COMPILE_DIR)/ld/ld-new $(TOOLS_DIR)/bin
endif # Stage 2


# Final Build Stage
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
	@echo; echo; echo "patch"; echo
	cd $(DIR); tar -xvf ../../../downloads/gmp-$(GMP_VER).tar.xz; mv gmp-$(GMP_VER) gmp
	cd $(DIR); tar -xvf ../../../downloads/mpfr-$(MPFR_VER).tar.bz2; mv mpfr-$(MPFR_VER) mpfr

COMPILE = yes
compile: configure
	@echo; echo; echo "compile"; echo
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) tooldir=$(PKG_DIR)
	
INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
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
