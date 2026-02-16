include ../Makefile.conf

PACKAGE = newt
VERSION = 0.52.25
NO_PARA = yes
LICENCE_FILE = $(DIR)/COPYING
BASE_URL = https://releases.pagure.org/newt

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) -C $(COMPILE_DIR) instroot=$(PKG_ROOT) install

include ../Makefile.rules
