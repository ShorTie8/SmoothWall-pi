# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = gcc
VERSION = $(GCC_VER)

BASE_URL = https://ftp.gnu.org/gnu/gcc/gcc-$(VERSION)
EXTENSION = $(GCC_EXT)

BASE_MPC = https://ftp.gnu.org/gnu/mpc
TAR_MPC = mpc-$(MPC_VER).tar.gz

BASE_GMP = https://ftp.gnu.org/gnu/gmp
TAR_GMP = gmp-$(GMP_VER).tar.xz

BASE_MPFR = https://ftp.gnu.org/gnu/mpfr
TAR_MPFR = mpfr-$(MPFR_VER).tar.bz2

BASE_ISL = https://gcc.gnu.org/pub/gcc/infrastructure
TAR_ISL = isl-$(ISL_VER).tar.bz2

COMPILE_DIR = $(DIR)-compile

DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo
	$(DL_CMD) $(BASE_GMP)/$(TAR_GMP)
	$(DL_CMD) $(BASE_MPFR)/$(TAR_MPFR)
	$(DL_CMD) $(BASE_MPC)/$(TAR_MPC)
	#$(DL_CMD) $(BASE_ISL)/$(TAR_ISL)
	$(DL_CMD) $(BASE_URL)/$(TARBALL)$(EXTENSION) $(MD5)

ifeq ($(mTUPLE), i586)
  GCC_flags = --with-cpu=pentium
else ifeq ($(mTUPLE), x86_64)
  GCC_flags =
else ifeq ($(mTUPLE), pi0w)
  GCC_flags = --with-cpu=arm1176jzf-s --with-float=hard
else ifeq ($(mTUPLE), rpi2 Opi-r1h2)
  GCC_flags = --with-cpu=cortex-a7 --with-fpu=neon-vfpv4 --with-float=hard
else ifeq ($(mTUPLE), rpi3)
  GCC_flags = --with-cpu=cortex-a53 --with-fpu=neon-fp-armv8 --with-float=hard 
else ifeq ($(mTUPLE), rpi4)
  # +crypto https://gist.github.com/fm4dd/c663217935dc17f0fc73c9c81b0aa845
  GCC_flags = --with-cpu=cortex-a72 --with-fpu=vfp --with-float=hard --enable-linker-build-id
else ifeq ($(mTUPLE), xu4)
  GCC_flags = --with-cpu=cortex-a15 --with-cpu=cortex-a7 --with-fpu=vfpv3-d16 --with-float=hard 
else ifeq ($(mTUPLE),$(filter $(mTUPLE),pi3-64 pi4-64))
  GCC_flags =  --with-arch=armv8-a+crc --with-cpu=cortex-a72 --enable-linker-build-id
else
  GCC_flags = Un-known GCC_flags
endif
 
# Tool Chain Build Stage 1
#
ifeq ($(BUILD_PHASE), Stage_1)

PREPARE = yes
$(DIR)/: download
	@echo; echo; echo "prepare"; echo
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_GMP); mv gmp-$(GMP_VER) gmp
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_MPFR); mv mpfr-$(MPFR_VER) mpfr
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_MPC); mv mpc-$(MPC_VER) mpc
	#cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_ISL); mv isl-$(ISL_VER) isl

PATCH = yes
patch: $(DIR)/
	@echo; echo; echo "patch"; echo
	@echo; echo "change the location of GCC's default dynamic linker to use the one installed in /tools."
	cd $(DIR); \
	for file in gcc/config/{{linux,i386/linux{,64}}.h,arm/linux-eabi.h,aarch64/aarch64-linux.h}; \
	do \
	  cp -uv $$file{,.orig}; \
	  sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
		  -e 's@/usr@/tools@g' $$file.orig > $$file; \
	  echo "" >> $$file; \
	  echo "#undef STANDARD_STARTFILE_PREFIX_1" >> $$file; \
	  echo "#undef STANDARD_STARTFILE_PREFIX_2" >> $$file; \
	  echo '#define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"' >> $$file; \
	  echo '#define STANDARD_STARTFILE_PREFIX_2 ""' >> $$file; \
	  touch $$file.orig; \
	done
	
#ifeq ($(mARCH), x86_64)
#	@echo; echo 'setting the default directory name for 64-bit libraries to “lib”:'
#	cd $(DIR); \
#		sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64
#endif

CONFIG_OPTS = $(GCC_flags) \
	      --target=$(SWE_TGT) \
	      --prefix=$(TOOLS_DIR) \
	      --with-glibc-version=2.11 \
	      --with-sysroot=$(ROOT) \
	      --with-newlib \
	      --without-headers \
	      --with-local-prefix=$(TOOLS_DIR) \
	      --with-native-system-header-dir=$(TOOLS_DIR)/include \
	      --disable-nls \
	      --disable-shared \
	      --disable-multilib \
	      --disable-decimal-float \
	      --disable-threads \
	      --disable-libatomic \
	      --disable-libgomp \
	      --disable-libmpx \
	      --disable-libquadmath \
	      --disable-libssp \
	      --disable-libvtv \
	      --disable-libstdcxx \
	      --enable-languages=c,c++

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	make -C $(COMPILE_DIR) install
endif # Stage 1


# Tool Chain Build Stage 2
#
ifeq ($(BUILD_PHASE), Stage_2)

PREPARE = yes
$(DIR)/: download
	@echo; echo; echo "prepare"; echo
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_GMP); mv gmp-$(GMP_VER) gmp
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_MPFR); mv mpfr-$(MPFR_VER) mpfr
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_MPC); mv mpc-$(MPC_VER) mpc
	#cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_ISL); mv isl-$(ISL_VER) isl

PATCH = yes
patch: $(DIR)/
	@echo; echo; echo "patch"; echo
	@echo "Create a full version of the internal header"
	cd $(DIR); cat gcc/limitx.h gcc/glimits.h gcc/limity.h > \
	  `dirname $$($$SWE_TGT-gcc -print-libgcc-file-name)`/include-fixed/limits.h

	@echo; echo "change the location of GCC's default dynamic linker to use the one installed in /tools."
	cd $(DIR); \
	for file in gcc/config/{{linux,i386/linux{,64}}.h,arm/linux-eabi.h,aarch64/aarch64-linux.h}; \
	do \
	  cp -uv $$file{,.orig}; \
	  sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
		  -e 's@/usr@/tools@g' $$file.orig > $$file; \
	  echo "" >> $$file; \
	  echo "#undef STANDARD_STARTFILE_PREFIX_1" >> $$file; \
	  echo "#undef STANDARD_STARTFILE_PREFIX_2" >> $$file; \
	  echo '#define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"' >> $$file; \
	  echo '#define STANDARD_STARTFILE_PREFIX_2 ""' >> $$file; \
	  touch $$file.orig; \
	done
	
#ifeq ($(mARCH), x86_64)
#	@echo; echo 'change the default directory name for 64-bit libraries to “lib”:'
#	cd $(DIR); sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64
#endif

PRE_CONFIGURE = \
		CC=$(SWE_TGT)-gcc \
		CXX=$(SWE_TGT)-g++ \
		AR=$(SWE_TGT)-ar \
		RANLIB=$(SWE_TGT)-ranlib

CONFIG_OPTS = $(GCC_flags) \
		--prefix=$(TOOLS_DIR) \
	    --with-local-prefix=$(TOOLS_DIR) \
	    --with-native-system-header-dir=$(TOOLS_DIR)/include \
	    --enable-languages=c,c++ \
	    --disable-libstdcxx-pch \
	    --disable-multilib \
	    --disable-bootstrap \
	    --disable-libgomp

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	make -C $(COMPILE_DIR) install
	ln -svf gcc $(TOOLS_DIR)/bin/cc
endif


# Final Build
#
ifeq ($(BUILD_PHASE), Final)

PATCH = yes
patch: $(DIR)/
	@echo; echo "patch"; echo
#ifeq ($(BITS_64), yes)
#	cd $(DIR); sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64
#endif
	rm -vf /usr/lib/gcc

PRE_CONFIGURE = SED=sed

CONFIG_OPTS = $(GCC_flags) \
		--prefix=$(PKG_DIR) \
	    --host=$(FINAL_TGT) \
	    --build=$(FINAL_TGT) \
	    --target=$(FINAL_TGT) \
		--enable-languages=c,c++ \
		--disable-multilib \
		--disable-bootstrap      \
		--with-system-zlib
 
INSTALL = yes
install: compile
	@echo; echo "install"; echo
	mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	cd $(PKG_ROOT)$(PKG_DIR)/bin; ln -svf gcc cc;
	cd $(PKG_ROOT)$(PKG_DIR)/lib; ln -svf $(PKG_DIR)/bin/cpp;
	ln -svf /usr/bin/cpp /lib
	ln -svf gcc /usr/bin/cc
endif

libgcc:
	gcc -v
	@echo
	tar -zcvf $(TARGET_DIR)/smoothwall-libgcc.tar.gz -C $(PKG_ROOT) $(PKG_DIR)/lib*/libgcc*

include ../Makefile.rules
