# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ppp
VERSION = 2.4.7

BASE_URL = http://samba.org/ftp/ppp/

PATCH_FILE1 = pppstats-Makefile.patch

COMPILE = yes
INSTALL = yes

COMPILE_FLAGS = -DHAVE_PATHS_H -DIPX_CHANGE -DHAVE_MMAP -D_PATH_VARRUN=\\\"/var/run\\\"


compile: configure
	cd $(DIR); \
	  sed -i -e 's/^\(COPT.*\)/\1 $(CFLAGS)/' chat/Makefile; \
	  sed -i -e 's/^\(COPT.*\)/\1 $(CFLAGS)/' pppd/Makefile; \
	  sed -i -e 's/^\(COPT.*\)/\1 $(CFLAGS)/' pppd/plugins/Makefile; \
	  sed -i -e 's/^\(CFLAGS\s*=.*\)/\1 $(CFLAGS)/' pppd/plugins/rp-pppoe/Makefile; \
	  sed -i -e 's/^\(CFLAGS\s*=.*\)/\1 $(CFLAGS)/' pppd/plugins/pppoatm/Makefile; \
	  sed -i -e 's/^\(CFLAGS\s*=.*\)/\1 $(CFLAGS)/' pppd/plugins/radius/Makefile; \
	  sed -i -e 's/^\(CFLAGS.*\)/export \1 $(CFLAGS)/' pppstats/Makefile; \
	  sed -i -e 's/^\(CFLAGS.*\)/export \1 $(CFLAGS)/' pppdump/Makefile
	@make $(JOBS) -C $(DIR) COMPILE_FLAGS="$(COMPILE_FLAGS)"

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(DIR) DESTDIR=$(PKG_ROOT)$(PKG_DIR) install
	
include ../Makefile.rules
