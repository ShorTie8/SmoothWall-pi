# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile.conf

PACKAGE = Archive-Zip
VERSION = 1.67

BASE_URL = https://cpan.metacpan.org/authors/id/P/PH/PHRED

CONFIGURE = yes
CLEAN = yes

configure: $(DIR)/
	#@+cd $(DIR); echo 'y' | perl Makefile.PL
	@+cd $(DIR); perl Makefile.PL

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)

include ../../../Makefile.rules
