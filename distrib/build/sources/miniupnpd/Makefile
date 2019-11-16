# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = miniupnpd
VERSION = 2.0

BASE_URL = http://miniupnp.free.fr/files/

PATCH_FILE1 = umask.patch
PATCH_FILE2 = genconfig.patch

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

PRECONFIGURE = CONFIG_OPTIONS="--portinuse --vendorcfg --leasefile --pcp-peer --uda-version=1.1"

configure: patch
	cd $(DIR); $(PRECONFIGURE) make -f Makefile.linux config.h

compile: configure
	@make $(JOBS) -C $(DIR) -f Makefile.linux \
	  CFLAGS="$(CFLAGS) \
	    -DIPTABLES_143 -DUSE_NETFILTER \
	    -I../../iptables/iptables-$(IPTABLES_VER)/include" \
	  LDFLAGS="-L$(IPT_LIBEXEC) -lip4tc -lip6tc"

install: compile
	@mkdir -p $(PKG_ROOT)
	@install -D $(DIR)/miniupnpd $(PKG_ROOT)$(PKG_DIR)/sbin/miniupnpd
	@mkdir -p $(PKG_ROOT)/usr/etc
	@touch $(PKG_ROOT)/usr/etc/upnp.leases
	@chown 99:99 $(PKG_ROOT)/usr/etc/upnp.leases

include ../Makefile.rules
