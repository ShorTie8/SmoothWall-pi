# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = curl
VERSION = 7.67.0

BASE_URL = https://curl.haxx.se/download
EXTENSION = .tar.xz

PKG_DIR = 

CONFIG_OPTS += --prefix= --exec-prefix=/usr \
	       --datarootdir=/usr/share \
	       --libexecdir=/usr/libexec \
	       --includedir=/usr/include \
	       --with-ca-path=/usr/lib/ssl/certs

include ../Makefile.rules
