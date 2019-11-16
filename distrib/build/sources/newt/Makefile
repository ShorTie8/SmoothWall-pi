include ../Makefile.conf

PACKAGE = newt
VERSION = 0.52.12

NO_PARA = yes

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = http://www.mirrorservice.org/sites/www.ibiblio.org/gentoo/distfiles/

PATCH_FILE1 = no-python.patch

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) -C $(COMPILE_DIR) instroot=$(PKG_ROOT) install

include ../Makefile.rules
