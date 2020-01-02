# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = openvpn
VERSION = 2.4.8
EXTENSION = .tar.xz

BASE_URL = https://swupdate.openvpn.org/community/releases
EASY_RSA_VERSION = 3.0.6
EASY_RSA_URL = https://github.com/OpenVPN/easy-rsa/archive/v$(EASY_RSA_VERSION)/easy-rsa-$(EASY_RSA_VERSION).tar.gz
ZERINA_URL = http://agcl.us/swemods/cheesman/zerina/ZERINA-1.0.0-either-beta04.tar.gz

DOWNLOAD = yes
download:
	@echo; echo "download"
	$(DL_CMD) $(BASE_URL)/$(TARBALL)$(EXTENSION) $(MD5)
	$(DL_CMD) $(EASY_RSA_URL)
	$(DL_CMD) $(ZERINA_URL)

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
	@echo; echo "mkdir"
	mkdir -vp $(PKG_ROOT)
	#mkdir -vp $(PKG_ROOT)/var/smoothwall/mods/zerina/{etc/rc.d,httpd,lib,ovpn,usr/lib/smoothwall}
	@echo; echo "1st-install"
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	#make -C $(DIR) DESTDIR=$(PKG_ROOT)/var/smoothwall/mods/zerina install

redo: 1st-install
	@echo; echo "redo prepare"
	rm -rf $(DIR)
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)

	@echo; echo "prepare easy-rsa"
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/easy-rsa-$(EASY_RSA_VERSION).tar.gz

CONFIGURE = yes
configure: redo
	@echo; echo; echo "2nd configure, enable-password-save=no"
	cd $(DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" ./configure $(CONFIG_OPTS) --enable-password-save=no


INSTALL = yes
install: compile
	@echo; echo; echo "2nd install"
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	#make -C $(DIR) DESTDIR=$(PKG_ROOT)/var/smoothwall/mods/zerina install

	@echo; echo; echo "easy-rsa"
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/easy-rsa-$(EASY_RSA_VERSION).tar.gz
	@echo; echo "easyrsa init-pki"
	cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa init-pki
	# Your newly created PKI dir is: /build/sources/openvpn/openvpn-2.4.8/easy-rsa-3.0.6/easyrsa3/pki

	# Enter New CA Key Passphrase: 
	#cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa build-ca
	#cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa init-pki
	#cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa gen-req SmoothWall
	cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa gen-dh

	@echo; echo; echo "prepare zerina"
	mkdir -vp $(DIR)/zerina/mod
	cd $(DIR)/zerina; tar -xf $(DOWNLOADS_DIR)/ZERINA-1.0.0-either-beta04.tar.gz
	cd $(DIR)/zerina; tar -xf zerina.tar.gz
	cd $(DIR)/zerina/mod; tar -xf ../runtime.tar.gz

	#@echo; echo; echo "install zerina mod"
	
	#cp -v $(DIR)/zerina/mod/etc/rc.d/* $(PKG_ROOT)/var/smoothwall/mods/zerina/etc/rc.d
	#cp -vR $(DIR)/zerina/mod/httpd/* $(PKG_ROOT)/var/smoothwall/mods/zerina/httpd
	#cp -vR $(DIR)/zerina/mod/lib/* $(PKG_ROOT)/var/smoothwall/mods/zerina/lib
	#cp -vR $(DIR)/zerina/mod/ovpn/* $(PKG_ROOT)/var/smoothwall/mods/zerina/ovpn
	#cp -vR $(DIR)/zerina/mod/usr/lib/smoothwall/* $(PKG_ROOT)/var/smoothwall/mods/zerina/usr/lib/smoothwall
	#mkdir -vp $(PKG_ROOT)


include ../Makefile.rules
