# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libcap
VERSION = 2.77
BASE_URL = https://git.kernel.org/pub/scm/libs/libcap/libcap.git/snapshot

CONFIGURE = yes
configure: patch
	##	Prevent a static library from being installed
	cd $(DIR); sed -i '/install -m.*STA/d' libcap/Makefile

CONFIG_OPTS = GOLANG=no prefix=/usr exec_prefix= lib_prefix=/usr

COMPILE = yes
compile: configure
	@echo -e "/n/n  Compile /n"
	cd $(DIR); $(MAKE) $(JOBS) $(CONFIG_OPTS)

INSTALL = yes
install: compile
	@echo -e "/n/n  Install /n"
	cd $(DIR); make DESTDIR=$(PKG_ROOT) install $(CONFIG_OPTS)

include ../Makefile.rules
