# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = texinfo
VERSION = 7.2

BASE_URL = https://ftp.gnu.org/gnu/texinfo

ifeq ($(BUILD_PHASE), Final)
PRE_CONFIGURE = LIBS=-ltinfo
endif

include ../Makefile.rules
