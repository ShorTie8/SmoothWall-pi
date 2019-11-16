# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = bison
VERSION = 3.4.1

BASE_URL = https://ftp.gnu.org/gnu/bison/
JOBS = -j1

ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS += --prefix=${TOOLS_DIR}

endif

PATCH = yes
patch: $(DIR)/
	#cd $(DIR); echo '#define YYENABLE_NLS 1' >> config.h
	cd $(DIR); sed -i '6855 s/mv/cp/' Makefile.in

include ../Makefile.rules
