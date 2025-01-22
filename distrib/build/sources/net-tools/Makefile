# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

##	https://www.linuxfromscratch.org/blfs/view/stable/basicnet/net-tools.html

include ../Makefile.conf

PACKAGE = net-tools
VERSION = 2.10
EXTENSION = .tar.xz
BASE_URL = https://sourceforge.net/projects/net-tools/files

CONFIGURE = yes
configure: patch
	cp -v config.h $(DIR)


include ../Makefile.rules
