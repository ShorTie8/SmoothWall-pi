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


CONFIG_OPTS += --prefix=$(PKG_DIR) --enable-cxx --enable-mpbsd

include ../Makefile.rules
