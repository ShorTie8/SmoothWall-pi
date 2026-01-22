# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ncurses
VERSION = 6.6-20260103
EXTENSION = .tgz
BASE_URL = https://invisible-mirror.net/archives/ncurses/current
COMPILE_DIR = $(DIR)-compile

#PATCH_FILE1 = ncurses-5.9-gcc5_buildfixes-1.patch
#PATCH_URL1 = http://www.linuxfromscratch.org/patches/downloads/ncurses/$(PATCH_FILE1)

ifeq ($(BUILD_PHASE), Stage_3)
#CONFIG_OPTS += --with-shared \
#    --without-debug --without-ada --enable-overwrite
CONFIG_OPTS = --prefix=$(TOOLS_DIR) \
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
CONFIG_OPTS += \
		--mandir=/usr/share/man \
		--with-shared           \
		--without-debug         \
		--without-normal        \
		--with-cxx-shared       \
		--enable-pc-files       \
		--with-pkg-config-libdir=/usr/lib/pkgconfig
#				--enable-widec

##	Added update 12
INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)
	+$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install

##	Allow the linker to find non-wide-character ncurses libraries
	mkdir -vp $(PKG_ROOT)$(PREFIX)/lib/pkgconfig
	for lib in ncurses form panel menu; do \
		rm -vf $(PKG_ROOT)$(PREFIX)/lib/lib$${lib}.so; \
		echo "INPUT(-l$${lib}w)" > $(PKG_ROOT)$(PREFIX)/lib/lib$${lib}.so; \
		ln -sfv $${lib}w.pc $(PKG_ROOT)$(PREFIX)/lib/pkgconfig/$${lib}.pc; \
	  done


##	For old applications that look for -lcurses at build time are still buildable
#	rm $(PKG_ROOT)/usr/lib/libncurses.so
	echo "INPUT(libncurses.so.6 -ltinfo)" > $(PKG_ROOT)/usr/lib/libncurses.so
	ln -sv libncurses.so $(PKG_ROOT)/usr/lib/libcurses.so

endif

include ../Makefile.rules
