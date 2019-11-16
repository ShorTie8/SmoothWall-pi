# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = zstd
VERSION = 1.3.4

BASE_URL = http://github.com/facebook/zstd/archive

TARBALL = v$(VERSION)

#DIR = $(PACKAGE)-$(VERSION)



DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo
	#$(DL_CMD) $(BASE_GMP)/$(TAR_GMP)
	$(DL_CMD) https://github.com/facebook/zstd/archive/v$(VERSION).tar.gz

COMPILE = yes
compile: patch
	$(MAKE) $(JOBS) -C $(COMPILE_DIR)


include ../Makefile.rules
