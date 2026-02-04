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

####	Tool Chain Build Stage 3 ncurses	####
##
ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS = --prefix=$(TOOLS_DIR) \
            --host=$(SWE_TGT) \
            --build=$(./config.guess) \
            --mandir=/usr/share/man  \
            --with-manpage-format=normal \
            --with-shared \
            --with-cxx-shared \
            --without-ada \
            --without-debug \
            --without-normal \
            --disable-stripping

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	mkdir $(COMPILE_DIR)
	cd $(COMPILE_DIR); ../$(DIR)/configure
	@echo; echo; echo "Building include"; echo
	cd $(COMPILE_DIR); make -C include
	@echo; echo; echo "Building progs tic"; echo
	cd $(COMPILE_DIR); make -C progs tic
	(cd $(COMPILE_DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" $(PRE_CONFIGURE) ../$(DIR)/configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))

endif


####	Final Build ncurses		####
##
ifeq ($(BUILD_PHASE), Final)

CONFIG_OPTS += \
		--mandir=/usr/share/man \
		--with-shared \
		--with-termlib \
		--without-debug \
		--without-normal \
		--with-cxx-shared \
		--enable-pc-files \
		--with-pkg-config-libdir=/usr/lib/pkgconfig

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	mkdir $(COMPILE_DIR)
	cd $(COMPILE_DIR); ../$(DIR)/configure
	@echo; echo; echo "Building include"; echo
	cd $(COMPILE_DIR); make -C include
	@echo; echo; echo "Building progs tic"; echo
	cd $(COMPILE_DIR); make -C progs tic
	(cd $(COMPILE_DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" $(PRE_CONFIGURE) ../$(DIR)/configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))

INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)
	+$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install

	echo; echo
	##	Allow the linker to find non-wide-character ncurses libraries
	mkdir -vp $(PKG_ROOT)/usr/lib/pkgconfig
	(cd $(PKG_ROOT); \
	  for lib in ncurses form panel menu tinfo; do \
		rm -vf /usr/lib/lib$${lib}.so; \
		echo "INPUT(-l$${lib}w)" > /usr/lib/lib$${lib}.so; \
		ln -sfv $${lib}w.pc /usr/lib/pkgconfig/$${lib}.pc; \
	  done)

endif

include ../Makefile.rules
