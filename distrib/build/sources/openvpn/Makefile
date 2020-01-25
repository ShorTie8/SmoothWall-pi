# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = openvpn
VERSION = 2.3.8
EXTENSION = .tar.xz

BASE_URL = https://swupdate.openvpn.org/community/releases

# added iproute2 to fix
#configure: error: route utility is required but missing

# enable-password-save ?? why double compile ????
#configure: WARNING: unrecognized options: --disable-nls, --enable-password-save

CONFIG_OPTS +=  --enable-iproute2 \
				--enable-lzo=yes \
				--enable-crypto=yes \
				--enable-plugin-auth-pam=no \
				--enable-plugin-down-root=no \
				--enable-debug=yes \
				--enable-ofb-cfb=no  \
				--enable-x509-alt-username=no

1st-configure: patch
	@echo; echo; echo "1st-configure, --enable-password-save=yes"
	cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure $(CONFIG_OPTS) --enable-password-save=yes

1st-compile: 1st-configure
	@echo; echo; echo "1st-compile"
	make $(JOBS) -C $(DIR)

1st-install: 1st-compile
	@echo; echo "1st-install"
	mkdir -vp $(PKG_ROOT)
	mkdir -vp $(PKG_ROOT)/var/smoothwall/mods/zerina/{include,usr/bin64}
	@echo; echo "1st-install"
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@echo; echo "1st-install move"
	mv -v $(PKG_ROOT)/usr/sbin/openvpn $(PKG_ROOT)/var/smoothwall/mods/zerina/usr/bin64/openvpn_enable_passwd_save

redo: 1st-install
	@echo; echo "redo prepare"
	rm -rf $(DIR)
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)

CONFIGURE = yes
configure: redo
	@echo; echo; echo "2nd configure, enable-password-save=no"
	cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure $(CONFIG_OPTS) --enable-password-save=no


INSTALL = yes
install: compile
	@echo; echo; echo "2nd install"
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
@echo; echo "move"
	mv -v $(PKG_ROOT)/usr/sbin/openvpn $(PKG_ROOT)/var/smoothwall/mods/zerina/usr/bin64/openvpn_no_enable_passwd_save
	mv -v $(PKG_ROOT)/usr/include/openvpn-plugin.h $(PKG_ROOT)/var/smoothwall/mods/zerina/include/no-openvpn-plugin.h
	@echo; echo "ls"
	ls -l $(PKG_ROOT)/var/smoothwall/mods/zerina/include
	@echo
	ls -l $(PKG_ROOT)/var/smoothwall/mods/zerina/usr/bin64

include ../Makefile.rules
