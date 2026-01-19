# SmoothWall Build system.
#
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.
##	https://ftp.debian.org/debian/pool/main/p/python-setuptools/python-setuptools_44.1.1-1.debian.tar.xz

include ../Makefile.conf

PACKAGE = setuptools

VERSION = 44.1.1
EXTENSION = .tar.xz
DIR = python-$(PACKAGE)-$(VERSION)
TARBALL = python-$(PACKAGE)_$(VERSION).orig
BASE_URL = http://deb.debian.org/debian/pool/main/p/python-setuptools

COMPILE = yes
compile: patch
	@echo; echo; echo "Compile"; echo
	cd $(DIR); python3 setup.py build

INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	mkdir -vp $(PKG_ROOT)
	# invalid command name 'DESTDIR=/build/buildroot/setuptools'
	#cd $(DIR); python setup.py DESTDIR=$(PKG_ROOT) install
	# don't really need a tarball, just for M2Crypto setup
	cd $(DIR); python3 setup.py install

include ../Makefile.rules
