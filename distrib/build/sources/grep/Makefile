# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = grep
VERSION = 2.21

BASE_URL = http://ftp.gnu.org/gnu/grep/
EXTENSION = .tar.xz

ifeq ($(BUILD_PHASE), Final)
PKG_DIR = 

CONFIG_OPTS += --prefix= --exec-prefix= \
	       --datarootdir=/usr/share \
	       --libexecdir=/usr/libexec \
	       --includedir=/usr/include
endif

include ../Makefile.rules
