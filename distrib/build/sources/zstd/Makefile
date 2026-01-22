# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = zstd
VERSION = 1.5.7
TARBALL = v$(VERSION)
BASE_URL = http://github.com/facebook/zstd/archive

COMPILE = yes
compile: $(DIR)/
	@echo; echo; echo "Compile"; echo
	+$(PRE_COMPILE) $(MAKE) ${JOBS} -C $(COMPILE_DIR)

include ../Makefile.rules
