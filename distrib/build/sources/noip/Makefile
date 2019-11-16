include ../Makefile.conf

PACKAGE = noip
VERSION = 1.6.0

BASE_URL = http://downloads.smoothwall.org/buildmirror

EXTENSION = .tbz2

PREPARE = yes
INSTALL = yes
CONFIGURE = yes

$(DIR): download
	@tar xfvj $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)

configure: $(DIR)
	cd $(DIR); [ -f noip ] && rm -f noip
	sed -i -e 's/^\(ARCH.*\)/\1 $(CFLAGS)/' $(DIR)/Makefile

install: compile
	@install -D $(COMPILE_DIR)/noip $(PKG_ROOT)/$(PKG_DIR)/bin/noip

include ../Makefile.rules

