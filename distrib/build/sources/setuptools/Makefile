# SmoothWall Build system.
#
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = setuptools
#VERSION = 41.0.1
#EXTENSION = .zip
#BASE_URL = https://files.pythonhosted.org/packages/1d/64/a18a487b4391a05b9c7f938b94a16d80305bf0369c6b0b9509e86165e1d3

VERSION = 40.8.0
EXTENSION = .tar.xz
DIR = python-$(PACKAGE)-$(VERSION)
TARBALL = python-$(PACKAGE)_$(VERSION).orig
BASE_URL = http://deb.debian.org/debian/pool/main/p/python-setuptools
#/python-setuptools_40.8.0.orig.tar.xz

#PREPARE = yes
#$(DIR)/: download
#	@echo; echo "prepare"
#	unzip -q $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
#	unzip: Command not found



COMPILE = yes
compile: patch
	@echo; echo; echo "compile"; echo
	cd $(DIR); python setup.py build

INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)
	# invalid command name 'DESTDIR=/build/buildroot/setuptools'
	#cd $(DIR); python setup.py DESTDIR=$(PKG_ROOT) install
	# don't really need a tarball, just for M2Crypto setup
	cd $(DIR); python setup.py install

include ../Makefile.rules
