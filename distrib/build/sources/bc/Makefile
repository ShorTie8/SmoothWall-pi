# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = bc
VERSION = 1.06.95

BASE_URL = http://alpha.gnu.org/gnu/$(PACKAGE)

EXTENSION = .tar.bz2

PATCH_FILE1 = bc-1.06.95-memory_leak-1.patch

ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS += --prefix=$(TOOLS_DIR) \
	      --with-readline \
	       --mandir=$(TOOLS_DIR)/usr/share/man \
	       --infodir=$(TOOLS_DIR)/usr/share/info

else

CONFIG_OPTS += --with-readline \
	      --mandir=/usr/share/man \
	      --infodir=/usr/share/info

endif

include ../Makefile.rules
