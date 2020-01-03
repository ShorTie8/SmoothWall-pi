# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile.conf

PACKAGE = Net-SSLeay
VERSION = 1.88

BASE_URL = https://cpan.metacpan.org/authors/id/C/CH/CHRISN

CONFIGURE = yes
CLEAN = yes

configure: $(DIR)/
	@echo; echo "configure"
	# Do you want to run external tests?
	cd $(DIR); echo 'n' | perl Makefile.PL

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
