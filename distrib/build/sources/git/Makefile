# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = git
VERSION = 2.9.5

EXTENSION = .tar.gz

BASE_URL = https://www.kernel.org/pub/software/scm/git

ifeq ($(BUILD_PHASE), Stage_3)
CONFIG_OPTS += --with-openssl --without-curl --without-tcltk --without-python
else
CONFIG_OPTS += --with-openssl --without-tcltk
endif

COMPILE = yes
INSTALL = yes
CLEAN = yes

compile: configure
	@echo; echo; echo "compile"
	make $(JOBS) -C $(COMPILE_DIR) PREFIX=$(PKG_DIR) V=1

install: compile
	@echo; echo; echo "install"
	mkdir -vp $(PKG_ROOT)
	make -C $(COMPILE_DIR) PREFIX=$(PKG_DIR) DESTDIR=$(PKG_ROOT) install

clean:
ifndef BUILD_PHASE
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
else
	@echo; echo "clean"
	rm -rf $(DIR)
	rm -rf $(COMPILE_DIR)
	rm -rf $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	@echo; echo "BITS_64"
	mkdir -vp $(PKG_ROOT)/{lib,usr/lib}
	cd $(PKG_ROOT); ln -sv lib lib64
	cd $(PKG_ROOT)/usr; ln -sv lib lib64
endif
	rm -vf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
