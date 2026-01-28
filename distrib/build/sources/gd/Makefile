# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = gd
VERSION = 2.3.3
DIR = libgd-gd-$(VERSION)
#ReConfigure = yes
BASE_URL = https://github.com/libgd/libgd/archive

CONFIGURE = yes
configure: patch
	@echo; echo; echo "bootstrap"
	cd $(DIR); ./bootstrap.sh
	@echo; echo; echo "Configure"; echo
	(cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))


include ../Makefile.rules
