# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ppp
VERSION = 2.5.2
BASE_URL = http://samba.org/ftp/ppp/

CFLAGS += -std=gnu17

CONFIGURE = yes
configure: patch
	(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
	(cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" $(PRE_CONFIGURE) ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))
	(cd $(DIR); sed -i -e '/^HAVE_INET6=/s/^/#/' pppd/Makefile)


COMPILE = yes
compile: configure
	@make $(JOBS) -C $(DIR)

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(DIR) DESTDIR=$(PKG_ROOT)$(PKG_DIR) install
	
include ../Makefile.rules
