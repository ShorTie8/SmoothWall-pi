include ../Makefile.conf

PACKAGE = ez-ipupdate
VERSION = 3.0.11b8

BASE_URL = http://downloads.smoothwall.org/buildmirror

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@install -D $(COMPILE_DIR)/ez-ipupdate $(PKG_ROOT)$(PKG_DIR)/bin/ez-ipupdate
	
include ../Makefile.rules
