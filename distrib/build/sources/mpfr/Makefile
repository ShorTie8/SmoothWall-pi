# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = mpfr
VERSION = $(MPFR_VER)

BASE_URL = https://ftp.gnu.org/gnu/mpfr

EXTENSION = .tar.bz2

CONFIG_OPTS += --enable-thread-safe \
	      --docdir=/usr/share/doc/mpfr-$(MPFR_VER)

include ../Makefile.rules
