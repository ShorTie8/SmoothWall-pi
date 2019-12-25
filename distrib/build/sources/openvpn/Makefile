# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = openvpn
VERSION = 2.4.8
ReConfigure = yes
EXTENSION = .tar.xz
BASE_URL = https://swupdate.openvpn.org/community/releases
EASY_RSA_VERSION = 3.0.6
EASY_RSA_URL = https://github.com/OpenVPN/easy-rsa/archive/v$(EASY_RSA_VERSION)/easy-rsa-$(EASY_RSA_VERSION).tar.gz
ZERINA_URL = http://agcl.us/swemods/cheesman/zerina/ZERINA-1.0.0-either-beta04.tar.gz

DOWNLOAD = yes
download:
	@echo; echo; echo "download"
	$(DL_CMD) $(BASE_URL)/$(TARBALL)$(EXTENSION) $(MD5)
	$(DL_CMD) $(EASY_RSA_URL)
	$(DL_CMD) $(ZERINA_URL)

PREPARE = yes
$(DIR)/: download
	@echo; echo; echo "prepare"
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)

	@echo; echo; echo "prepare easy-rsa"
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/easy-rsa-$(EASY_RSA_VERSION).tar.gz

	@echo; echo; echo "prepare zerina"
	mkdir -vp $(DIR)/zerina/mod
	cd $(DIR)/zerina; tar -xf $(DOWNLOADS_DIR)/ZERINA-1.0.0-either-beta04.tar.gz
	cd $(DIR)/zerina; tar -xf zerina.tar.gz
	cd $(DIR)/zerina/mod; tar -xf ../runtime.tar.gz

CONFIG_OPTS += --enable-iproute2 --disable-plugin-auth-pam

INSTALL = yes
install: compile
	@echo; echo; echo "mkdir"
	mkdir -vp $(PKG_ROOT)/var/smoothwall/mods/zerina/{etc/rc.d,httpd,lib,ovpn,usr/lib/smoothwall}
	@echo; echo; echo "install"
	make -C $(DIR) DESTDIR=$(PKG_ROOT)/var/smoothwall/mods/zerina install
	@echo; echo; echo "easy-rsa"
	cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa init-pki
	# Your newly created PKI dir is: /build/sources/openvpn/openvpn-2.4.8/easy-rsa-3.0.6/easyrsa3/pki

	# Enter New CA Key Passphrase: 
	#cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa build-ca
	#cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa init-pki
	#cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa gen-req SmoothWall
	cd $(DIR)/easy-rsa-$(EASY_RSA_VERSION)/easyrsa3; ./easyrsa gen-dh

	@echo; echo; echo "install zerina mod"
	
	cp -v $(DIR)/zerina/mod/etc/rc.d/* $(PKG_ROOT)/var/smoothwall/mods/zerina/etc/rc.d
	cp -vR $(DIR)/zerina/mod/httpd/* $(PKG_ROOT)/var/smoothwall/mods/zerina/httpd
	cp -vR $(DIR)/zerina/mod/lib/* $(PKG_ROOT)/var/smoothwall/mods/zerina/lib
	cp -vR $(DIR)/zerina/mod/ovpn/* $(PKG_ROOT)/var/smoothwall/mods/zerina/ovpn
	cp -vR $(DIR)/zerina/mod/usr/lib/smoothwall/* $(PKG_ROOT)/var/smoothwall/mods/zerina/usr/lib/smoothwall
	#mkdir -vp $(PKG_ROOT)


include ../Makefile.rules
