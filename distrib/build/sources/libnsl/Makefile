# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libnsl
VERSION = 2.0.1
TARBALL = v$(VERSION)
BASE_URL = https://github.com/thkukuk/libnsl/archive/refs/tags

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	(cd $(DIR); ./autogen.sh)
	(cd $(DIR); ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))


include ../Makefile.rules
