# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = squidGuard
VERSION = 1.5-beta

BASE_URL = http://www.squidguard.org/Downloads/Devel

CONFIG_OPTS += --prefix=$(PKG_DIR) --exec_prefix=$(PKG_DIR) \
	      --with-sg-config=/var/smoothwall/urlfilter/squidGuard.conf \
	      --with-sg-logdir=/var/log/squidGuard \
	      --with-sg-dbhome=/var/smoothwall/urlfilter/blacklists \
	      --with-syslog=yes

PATCH_FILE1 = sg.h.in.patch

LDFLAGS = -L/usr/lib

INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)/usr/sbin $(PKG_ROOT)/var/smoothwall/urlfilter \
	  $(PKG_ROOT)/var/log/squidGuard
	cp $(DIR)/src/squidGuard $(PKG_ROOT)/usr/sbin
	sed -e 's!dbhome /usr/local/squidGuard/db!dbhome /var/smoothwall/urlfilter/blacklists!' \
	    -e 's!logdir /usr/local/squidGuard/log!logdir /var/log/squidGuard!' \
	  < $(DIR)/samples/sample.conf \
	  > $(PKG_ROOT)/var/smoothwall/urlfilter/squidGuard.conf
	chown -R root:root $(PKG_ROOT)/usr/sbin/squidGuard
	chmod 755 $(PKG_ROOT)/usr/sbin/squidGuard
	chown -R squid:squid $(PKG_ROOT)/var/log/squidGuard
	chmod 755 $(PKG_ROOT)/var/log/squidGuard
	chown -R nobody:nobody $(PKG_ROOT)/var/smoothwall/urlfilter
	chmod 644 $(PKG_ROOT)/var/smoothwall/urlfilter/squidGuard.conf


include ../Makefile.rules
