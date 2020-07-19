# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = curl
VERSION = 7.68.0

BASE_URL = https://curl.haxx.se/download
EXTENSION = .tar.xz

PKG_DIR = 

CONFIG_OPTS += --prefix=/usr --exec-prefix=/usr \
	       --datarootdir=/usr/share \
	       --libexecdir=/usr/libexec \
	       --includedir=/usr/include \
	       --libdir=/usr/lib \
	       --with-ssl=/usr \
	       --with-ca-path=/usr/lib/ssl/certs

include ../Makefile.rules
