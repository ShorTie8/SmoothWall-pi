# SmoothWall Build system.
#
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = M2Crypto
VERSION = 0.47.0
DIR = m2crypto-$(VERSION)
TARBALL = m2crypto-$(VERSION)
BASE_URL = https://files.pythonhosted.org/packages/8b/19/409bcaf2820beb0cb6e52e807c6af3ac535edd494e599c7eceb01c6534c1

COMPILE = yes
compile: patch
	@echo; echo; echo "compile"; echo
	cd $(DIR); python3 setup.py build

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)
	#cd $(DIR); python setup.py DESTDIR=$(PKG_ROOT) install
	cd $(DIR); python3 setup.py install

include ../Makefile.rules
