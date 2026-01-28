# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile.conf

PACKAGE = File-Which
VERSION = 1.27
BASE_URL = https://cpan.metacpan.org/authors/id/P/PL/PLICEASE

CONFIGURE = yes
configure: $(DIR)/
	#@+cd $(DIR); perl Makefile.PL
	@+cd $(DIR); echo 'y' | perl Makefile.PL

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)

include ../../../Makefile.rules
