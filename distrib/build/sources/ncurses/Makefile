# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ncurses
VERSION = 6.1

BASE_URL = https://ftp.gnu.org/gnu/ncurses/

#PATCH_FILE1 = ncurses-5.9-gcc5_buildfixes-1.patch
#PATCH_URL1 = http://www.linuxfromscratch.org/patches/downloads/ncurses/$(PATCH_FILE1)
COMPILE_DIR = $(DIR)-compile

ifeq ($(BUILD_PHASE), Stage_3)
#CONFIG_OPTS += --with-shared \
#    --without-debug --without-ada --enable-overwrite
CONFIG_OPTS = --prefix=/usr                \
            --host=$(SWE_TGT)              \
            --build=$(./config.guess)    \
            --mandir=/usr/share/man      \
            --with-manpage-format=normal \
            --with-shared                \
            --without-normal             \
            --with-cxx-shared            \
            --without-debug              \
            --without-ada                \
            --disable-stripping

CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	mkdir $(COMPILE_DIR)
	cd $(COMPILE_DIR); ../$(DIR)/configure
	@echo; echo; echo "include"; echo
	cd $(COMPILE_DIR); make -C include
	@echo; echo; echo "progs tic"; echo
	cd $(COMPILE_DIR); make -C progs tic
	(cd $(COMPILE_DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" $(PRE_CONFIGURE) ../$(DIR)/configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))

else
CONFIG_OPTS += --with-shared \
				--without-debug \
				--with-termlib \
				--with-pkg-config \
				--enable-pc-files
#				--enable-widec

##	Added update 12
INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)
	+$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	rm $(PKG_ROOT)/usr/lib/libncurses.so
	echo "INPUT(libncurses.so.6 -ltinfo)" > $(PKG_ROOT)/usr/lib/libncurses.so

endif

include ../Makefile.rules
