# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = wireless_tools
VERSION = 29

BASE_URL = https://hewlettpackard.github.io/wireless-tools

TARBALL = $(PACKAGE).$(VERSION)
DIR = $(TARBALL)

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@find $(DIR) -type d -exec chmod +rx {} \;
	@find $(DIR) -type f -exec chmod +r {} \;
	cd $(DIR); sed -i -e 's/^\(XCFLAGS=.*\)/\1 $(CFLAGS)/' Makefile
	@true

compile: configure
	@$(MAKE) $(JOBS) -C $(DIR) PREFIX=$(PKG_DIR)

install: compile
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) -C $(DIR) PREFIX=$(PKG_ROOT)$(PKG_DIR) install

include ../Makefile.rules
