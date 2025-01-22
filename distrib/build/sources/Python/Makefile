# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = Python
##	distutils not in 3.12.x
VERSION = 3.11.9
EXTENSION = .tar.xz

BASE_URL = http://www.python.org/ftp/python/$(VERSION)

CONFIG_OPTS += \
		--enable-shared     \
		--with-system-expat \
		--with-system-ffi   \
		--with-system-gdbm  \
		--with-ensurepip=yes

COMPILE = yes
compile: configure
	@find $(COMPILE_DIR) -type d -exec chmod o=rx {} \;
	@find $(COMPILE_DIR) -type f -exec chmod o=r {} \;
	@chmod -R o+rw $(COMPILE_DIR)
	@make ${JOBS} -C $(COMPILE_DIR)

include ../Makefile.rules
