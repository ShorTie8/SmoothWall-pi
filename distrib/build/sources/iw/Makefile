# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = iw
VERSION = 5.0.1
EXTENSION = .tar.xz
BASE_URL = https://www.kernel.org/pub/software/network/iw

COMPILE = yes
compile: patch
	@echo; echo; echo "compile"; echo
	make $(JOBS) -C $(DIR)

include ../Makefile.rules
