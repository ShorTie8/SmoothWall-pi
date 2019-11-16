# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.
# https://wiki.strongswan.org/projects/strongswan/wiki/Autoconf

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = strongswan
# We pick the same as Debian wheezy for now, 4.5.2
#VERSION = 4.5.2
VERSION = 5.0.4
# 5.1.3 last with IPsec kernel interface to an older KLIPS version (removed with 5.2.0)
#VERSION = 5.1.3
#VERSION = 5.6.1
#VERSION = 5.6.2
BASE_URL = https://download.strongswan.org

# Apply Debian security patches
#PATCH_FILE1 = strongswan_4.5.2-1.5+deb7u10.debian.tar.gz
#PATCH_URL1 = http://security.debian.org/debian-security/pool/updates/main/s/strongswan/$(PATCH_FILE1)

#PATCH = yes
#patch: $(DIR)/
#	@echo; echo; echo "Apply Debian security patches"
#	tar -xf $(DOWNLOADS_DIR)/$(PATCH_FILE1)
#	cd $(DIR); for p in $$(cat ../debian/patches/series); do \
#		echo; echo $$p; \
#		patch -p1 < ../debian/patches/$$p; \
#	done


# https://wiki.strongswan.org/attachments/download/425/strongswan-init.patch
#PATCH_FILE1 = strongswan-init.patch

#		--enable-curl \
#		--enable-gcrypt \: error: gcrypt library not found

#		--enable-fast \
#checking for hdf_init in -lneo_utl... no
#      configure: error: ClearSilver library neo_utl not found!

#		--enable-kernel-pfroute \
# kernel_pfroute_net.c:20:23: fatal error: net/if_dl.h: No such file or directory
#		--enable-kernel-libipsec \
#		--enable-kernel-pfkey \
#		--enable-libipsec \
#		--enable-ipseckey \


# # this is a security-critical package, set all the options we can
# upto group=nogroup is basically by debian/rules
# without for smartcard pkcs11, but might be good to have

#--with-ipseclibdir=%{libdir}/ipsec \

CONFIG_OPTS += \
		--sysconfdir="/var/smoothwall/vpn" \
		--enable-gcrypt \
		--enable-curl \
		--enable-dhcp \
		--enable-farp \
		--enable-ldap \
		--enable-kernel-pfkey \
		--enable-kernel-klips \
		--enable-openssl \
		--enable-sqlite \
		--enable-ccm \
		--enable-ctr \
		--enable-gcm \
		--enable-eap-radius \
		--enable-eap-tls \
		--enable-eap-ttls \
		--enable-eap-peap \
		--enable-eap-mschapv2 \
		--enable-eap-identity \
		--disable-padlock \
		--with-group=nogroup


#		--sysconfdir="/var/smoothwall/vpn" \
#		--localstatedir="/var" \
#		--libexecdir="/usr/lib" \
#		--enable-ldap \
#		--enable-curl \
#		--with-capabilities=libcap \
#		--enable-mediation \
#		--enable-medsrv \
#		--enable-medcli \
#		--enable-openssl \
#		--enable-agent \
#		--enable-ctr \
#		--enable-ccm \
#		--enable-gcm \
#		--enable-addrblock \
#		--enable-eap-radius \
#		--enable-eap-identity \
#		--enable-eap-md5 \
#		--enable-eap-gtc \
#		--enable-eap-aka \
#		--enable-eap-mschapv2 \
#		--enable-eap-tls \
#		--enable-eap-ttls \
#		--enable-eap-tnc \
#		--enable-sqlite \
#		--enable-integrity-test \
#		--enable-ha \
#		--enable-dhcp \
#		--enable-farp \
#		--enable-led \
#		--enable-test-vectors \
#		--enable-nat-transport \
#		--enable-kernel-pfkey \
#		--enable-kernel-klips \
#		--enable-kernel-libipsec \
#		--with-group=nogroup \
#		--enable-xauth-eap \
#		--enable-xauth-noauth \
#		--enable-eap-radius \
#		--enable-eap-peap \
#		--disable-padlock \
#		--disable-chapoly

#		--with-linux-headers="$(SOURCES_DIR)/linux$(KERNEL_TYPE)/linux"
#	--with-user=strongswan
# --with-group=GROUP

include ../Makefile.rules
