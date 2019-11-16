include ../Makefile.conf

PACKAGE = squidclamav
VERSION = 6.16

BASE_URL = http://heanet.dl.sourceforge.net/project/$(PACKAGE)/$(PACKAGE)/$(VERSION)

PRE_CONFIGURE = LIBS=-ltinfo

CONFIG_OPTS = --with-c-icap

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
