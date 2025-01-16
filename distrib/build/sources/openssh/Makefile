# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = openssh
VERSION = 9.3p1

BASE_URL = http://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/

PATCH_FILE1 = log.c.patch

CONFIG_OPTS += --with-md5-passwords --with-pid-dir=/var/run

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@rm -f $(PKG_ROOT)$(PKG_DIR)/etc/sshd_config

include ../Makefile.rules
