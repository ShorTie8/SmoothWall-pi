# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile.conf

PACKAGE = ExtUtils-PkgConfig
VERSION = 1.16

BASE_URL = https://cpan.metacpan.org/authors/id/X/XA/XAOC

CONFIGURE = yes
CLEAN = yes

configure: $(DIR)/
	@echo; echo "configure"
	cd $(DIR); perl Makefile.PL

INSTALL = yes
install: compile
	@echo; echo "install"
	mkdir -p $(PKG_ROOT)
	$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@echo; echo "install in /"
	# Also need 'installed' for the rest of the modules
	tar cf - -C ${PKG_ROOT} . | tar xf - -C /

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)

include ../../../Makefile.rules
