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
	#@+cd $(DIR); echo 'y' | perl Makefile.PL
	@+cd $(DIR); perl Makefile.PL

INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)
	+$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	# Also need 'installed' for the rst of the modules
	tar cvf - -C ${PKG_ROOT} . | tar xvf - -C /

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)

include ../../../Makefile.rules
