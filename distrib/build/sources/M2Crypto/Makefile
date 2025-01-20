# SmoothWall Build system.
#
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = M2Crypto
VERSION = 0.43.0
BASE_URL = https://files.pythonhosted.org/packages/74/18/3beedd4ac48b52d1a4d12f2a8c5cf0ae342ce974859fba838cbbc1580249
# https://github.com/mcepl/M2Crypto/archive/refs/tags/0.42.0.tar.gz

COMPILE = yes
compile: patch
	@echo; echo; echo "compile"; echo
	cd $(DIR); python setup.py build

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)
	#cd $(DIR); python setup.py DESTDIR=$(PKG_ROOT) install
	cd $(DIR); python setup.py install

include ../Makefile.rules
