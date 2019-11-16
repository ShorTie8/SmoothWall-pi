# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = imspector
VERSION = 20130214

BASE_URL = http://www.imspector.org/downloads/snapshots/

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

OPTS = PREFIX=$(PKG_ROOT)$(PKG_DIR)
DIR = imspector

export ADD_PLUGINS = dbfilterplugin.so censordfilterplugin.so catsloggingplugin.so dbresponderplugin.so

configure: patch
	cd $(DIR); sed -i -e 's/LIBS = -ldl/& -lcrypto/' Makefile
	sed -i -e 's/^\(CXXFLAGS.*\)/\1 $(CFLAGS)/' $(DIR)/Makefile

compile: configure
	@$(MAKE) $(JOBS) -C $(DIR) $(OPTS)

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(DIR) $(OPTS) install
	@rm -f $(PKG_ROOT)$(PKG_DIR)/etc/imspector/imspector.conf

include ../Makefile.rules
