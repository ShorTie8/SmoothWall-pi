# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ninja
VERSION = 1.13.2
TARBALL = v$(VERSION)
BASE_URL = https://github.com/ninja-build/ninja/archive/refs/tags

export NINJAJOBS = $(JOBS)

COMPILE = yes
compile: $(DIR)/
	@echo; echo; echo "Compile"; echo
	cd $(DIR); python3 configure.py --bootstrap --verbose
	
INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	cd $(DIR); install -vDm755 ninja $(PKG_ROOT)/usr/bin/ninja
	cd $(DIR); install -vDm644 misc/bash-completion $(PKG_ROOT)/usr/share/bash-completion/completions/ninja
	cd $(DIR); install -vDm644 misc/zsh-completion  $(PKG_ROOT)/usr/share/zsh/site-functions/_ninja

include ../Makefile.rules
