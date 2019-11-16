# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile.conf

PACKAGE = Net-SSLeay
VERSION = 1.82

BASE_URL = http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/

CONFIGURE = yes
CLEAN = yes

configure: $(DIR)/
	#@+cd $(DIR); perl Makefile.PL
	# Do you want to run external tests?
	@+cd $(DIR); echo 'y' | perl Makefile.PL

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
