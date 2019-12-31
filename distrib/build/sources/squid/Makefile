# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = squid
VERSION = 4.9

BASE_URL = http://www.squid-cache.org/Versions/v4

CONFIG_OPTS += --disable-arch-native \
	       --enable-async-io \
	       --enable-delay-pools \
	       --enable-follow-x-forwarded-for \
	       --enable-http-violations \
	       --enable-linux-netfilter \
	       --enable-poll \
	       --enable-removal-policies="heap,lru" \
	       --enable-ssl-crtd \
	       --enable-storeio="aufs,diskd" \
	       --libdir=/usr/lib \
	       --localstatedir=/var \
	       --with-dl \
	       --with-large-files \
	       --with-libcap \
	       --with-logdir=/var/log/squid \
	       --with-max_fd=8192 \
	       --with-openssl \
	       --with-swapdir=/var/spool/squid

INSTALL_LANGUAGES = English

CONFIGURE = yes

configure: patch
	@echo; echo; echo "configure"; echo
	/bin/sh -c "ulimit -n 8192; cd $(DIR); ./configure $(CONFIG_OPTS) --prefix=/$(PKG_DIR)"


INSTALL = yes

install: compile
	@echo; echo; echo "install"; echo
	mkdir -p $(PKG_ROOT)
	+$(MAKE) -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	mkdir -p $(PKG_ROOT)/var/smoothwall/proxy
	touch $(PKG_ROOT)/var/smoothwall/proxy/squid.conf
	chown nobody:nobody $(PKG_ROOT)/var/smoothwall/proxy/squid.conf
	chmod 664 $(PKG_ROOT)/var/smoothwall/proxy/squid.conf
	rm -f $(PKG_ROOT)/usr/etc/squid.conf
	ln -s /var/smoothwall/proxy/squid.conf $(PKG_ROOT)/usr/etc/squid.conf


BUILDTARBALL = yes

SQUID_BITS = ./usr/bin/ ./usr/libexec/ ./usr/sbin/squid \
             ./usr/etc/mime.conf ./usr/share/ ./var/smoothwall/proxy/squid.conf

$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: install
	@echo; echo; echo "build tarball"
	tar -zcf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) $(SQUID_BITS)
	@echo "install tarball"
	tar -xf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C /

include ../Makefile.rules
