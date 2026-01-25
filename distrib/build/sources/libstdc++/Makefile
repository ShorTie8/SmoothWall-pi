# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2016
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = libstdc++
VERSION = $(GCC_VER)
EXTENSION = $(GCC_EXT)
BASE_URL = https://ftp.gnu.org/gnu/gcc/gcc-$(VERSION)
TARBALL = gcc-$(VERSION)
DIR = gcc-$(VERSION)
COMPILE_DIR = $(DIR)-compile

# Tool Chain Build Stage 1
#
ifeq ($(BUILD_PHASE), Stage_1)

DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo
	$(DL_CMD) $(BASE_URL)/$(TARBALL)$(EXTENSION) $(MD5)

PREPARE = yes
prepare: download
	@echo; echo; echo "prepare"; echo
	tar xf $(DOWNLOADS_DIR)/gcc-$(VERSION)$(EXTENSION)
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_GMP); mv gmp-$(GMP_VER) gmp
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_MPFR); mv mpfr-$(MPFR_VER) mpfr
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_MPC); mv mpc-$(MPC_VER) mpc
	#cd $(DIR); tar -xf $(DOWNLOADS_DIR)/$(TAR_ISL); mv isl-$(ISL_VER) isl
	mkdir -v $(COMPILE_DIR)

CONFIG_OPTS = \
	      --prefix=$(TOOLS_DIR) \
	      --host=$(SWE_TGT) \
	      --disable-multilib \
	      --disable-nls \
	      --disable-libstdcxx-threads \
	      --disable-libstdcxx-pch \
	      --with-gxx-include-dir=/tools/$(SWE_TGT)/include/c++/$(VERSION)

CONFIGURE = yes
configure: prepare
	@echo; echo; echo "configure"; echo
	cd $(COMPILE_DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ../$(DIR)/libstdc++-v3/configure $(CONFIG_OPTS)

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	$(MAKE) -C $(COMPILE_DIR) install

endif	#Stage_2

CLEAN = yes
clean:
ifndef BUILD_PHASE
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
else
	@echo " $(PACKAGE)"
	@echo; echo ; echo "clean"
	rm -rf $(DIR)
	rm -rf $(COMPILE_DIR)
endif


include ../Makefile.rules
