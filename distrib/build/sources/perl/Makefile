# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

#  <Grinnz> ShorTie: odd middle numbers are development releases, not for end user consumption

include ../Makefile.conf

PACKAGE = perl
VERSION = 5.36.0
BASE_URL = https://www.cpan.org/src/5.0

# Fix build with GCC 15
CFLAGS += -std=gnu17

# Toolchain, Stage 3 build perl
#
ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS = -des -D prefix=$(TOOLS_DIR) -D vendorprefix=$(TOOLS_DIR)

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"
	cd $(DIR) && ./configure.gnu --prefix=$(TOOLS_DIR) \
		-des -Dlibs="-lpthread -lm" -Uloclibpth -Ulocincpth

COMPILE = yes
compile: configure
	@echo; echo; echo "Compile"
	make $(JOBS) -C $(DIR) # perl utilities ext/Errno/pm_to_blib

INSTALL = yes
install: compile
	@echo; echo; echo "Install"
	cd $(COMPILE_DIR); \
	  cp -v perl cpan/podlators/pod2man $(TOOLS_DIR)/bin; \
	  mkdir -pv $(TOOLS_DIR)/lib/perl5/$(VERSION); \
	  cp -Rv lib/* $(TOOLS_DIR)/lib/perl5/$(VERSION)
endif

# Final build
#
ifeq ($(BUILD_PHASE),Final)
CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"
	(cd $(COMPILE_DIR); \
	./configure.gnu --prefix=/$(PKG_DIR) -Dpager="/bin/less -isR" -Dusethreads);
endif


include ../Makefile.rules
