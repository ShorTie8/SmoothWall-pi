# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = bc
VERSION = 7.0.3
#BASE_URL = http://ftp.gnu.org/gnu/bc
BASE_URL = https://github.com/gavinhoward/bc/archive/$(VERSION)

CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	cd $(DIR); PREFIX=/usr CC=gcc CFLAGS="-std=c99" ./configure.sh -G -O3


include ../Makefile.rules
