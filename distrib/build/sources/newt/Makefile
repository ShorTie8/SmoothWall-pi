include ../Makefile.conf

PACKAGE = newt
VERSION = 0.52.21

NO_PARA = yes

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = https://releases.pagure.org/newt

#PATCH_FILE1 = no-python.patch

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) -C $(COMPILE_DIR) instroot=$(PKG_ROOT) install

include ../Makefile.rules
