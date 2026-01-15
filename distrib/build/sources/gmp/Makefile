# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = gmp
VERSION = $(GMP_VER)
EXTENSION = .tar.xz
BASE_URL = https://ftp.gnu.org/gnu/gmp

#ifeq ($(BITS_32), yes)
#PRE_CONFIGURE = ABI=32
#endif

##	 Fix build with GCC 15
##	GCC 15 (in development) defaults to -std=gnu23. This breaks one of
##	gmp-6.3.0's configure tests:
##	C23 removes unprototyped functions, which explains the error.
CFLAGS += -std=gnu17

CONFIG_OPTS += --enable-cxx

include ../Makefile.rules
