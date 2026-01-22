# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = cmake
VERSION = 4.2.2

BASE_URL = https://cmake.org/files/v4.2

CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	cd $(DIR); sed -i '/"lib64"/s/64//' Modules/GNUInstallDirs.cmake
	cd $(DIR); ./bootstrap --prefix=/usr \
							--system-libs \
							--no-system-jsoncpp \
							--no-system-librhash

include ../Makefile.rules
