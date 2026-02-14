# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = squid
VERSION = 7.4
TARBALL = SQUID_7_4
DIR = squid-SQUID_7_4
BASE_URL = https://github.com/squid-cache/squid/archive/refs/tags

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
	cd $(DIR); ./bootstrap.sh
	@echo; echo; echo "Configure"; echo
	@/bin/sh -c "ulimit -n 8192; cd $(DIR); ./configure $(CONFIG_OPTS) --prefix=/$(PKG_DIR)"


INSTALL = yes
install: compile
	@echo -e "/n/n  Install  /n"
	mkdir -vp $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	mkdir -vp $(PKG_ROOT)/var/smoothwall/proxy
	touch $(PKG_ROOT)/var/smoothwall/proxy/squid.conf
	chown -v nobody:nobody $(PKG_ROOT)/var/smoothwall/proxy/squid.conf
	chmod -v 664 $(PKG_ROOT)/var/smoothwall/proxy/squid.conf
	rm -vf $(PKG_ROOT)/usr/etc/squid.conf
	mkdir -vp $(PKG_ROOT)/usr/{bin,etc,libexec,share}
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
