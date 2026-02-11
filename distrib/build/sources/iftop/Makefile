# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = iftop
VERSION = 1.0pre4
BASE_URL = https://pdw.ex-parrot.com/iftop/download

PRE_CONFIGURE = LIBS=-ltinfo

PATCH_FILE1 = iftop-1.0_pre4-configure.ac.patch
PATCH_FILE2 = iftop-1.0_pre4-Makefile.am.patch
PATCH_FILE3 = iftop-1.0_pre4-tsent-set-but-not-used.patch
PATCH_FILE4 = iftop-1.0_pre4-ip6.arpa.patch
PATCH_FILE5 = iftop-1.0_pre4-fix-MAC-formatting.patch
PATCH_FILE6 = iftop-1.0_pre4-fno-common.patch
PATCH_FILE7 = iftop-1.0_pre4-allow-scales-beyond-1gbps.patch
PATCH_FILE8 = iftop-1.0_pre4-fix_c23.patch

PATCH = yes
patch: $(DIR)/
	@echo; echo "Patch";echo
	@echo "  Update config.guess/config.sub"
	for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf $(ROOT)/build/toolcrib/$$(basename $${i}) $${i}; done
	@echo; echo "bootstrap";echo
	cd $(DIR); ./bootstrap
	@echo; echo "Patch";echo
	(cd $(DIR); \
	for PATCH in $(PATCH_FILE1) $(PATCH_FILE2) $(PATCH_FILE3) $(PATCH_FILE4) \
			$(PATCH_FILE5) $(PATCH_FILE6) $(PATCH_FILE7) $(PATCH_FILE8); do \
	  echo $$PATCH; \
	  FILENAME=../$$PATCH; \
	  echo; echo $$FILENAME; \
	  [ -f $$FILENAME ] || exit 8; \
	  cat $$FILENAME | patch -p1 || exit 14; \
	done;)
	cd $(DIR); ./bootstrap

include ../Makefile.rules
