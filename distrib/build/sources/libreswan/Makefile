# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = $(FREESWAN_TYPE)
VERSION = $(FREESWAN_VER)

BASE_URL = https://download.libreswan.org

#### or github
## you need full commitID for DIR to work
## to update, since your playing
## rm -v downloads/libreswan-3.29.tar.g*
#gitCommitID = c75b7a09764fe18b54bcc7b57d2a7013f3ccbfe7
#gitCommitID = a993a13879c3367445dd6907bc77d2cabe9c270c
#BASE_URL = https://github.com/libreswan/libreswan/archive/$(gitCommitID)
#DIR = $(FREESWAN_TYPE)-$(gitCommitID)
#### end github

TARBALL = $(FREESWAN_TYPE)-$(VERSION)

PATCH_FILE1 = makefile.patch
#PATCH_FILE1 = kernel.mk.patch
PATCH_FILE2 = setup.in.smoothwall.patch
PATCH_FILE3 = ipsec.init.in.patch
PATCH_FILE4 = ipsec_kversion.h.patch
#PATCH_FILE5 = pf_key.c.patch

KNL_SRC = ../linux$(KERNEL_TYPE)/linux
MOD_DEST = /lib/modules/$(K_RAW_VERSION)$(KERNEL_TYPE)/kernel/net/ipsec

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@echo; echo; echo "configure"; echo
	@cp -v makefile.inc.local $(DIR)/Makefile.inc.local
	@echo; cat $(DIR)/Makefile.inc.local; echo
	
# <LetoTo> ShorTie: try: make USE_KLIPS=true module module_install
# Debian ENABLE_SELINUX = USE_LABELED_IPSEC=true USE_LINUX_AUDIT=true

# USE_DNSSEC=true \
# lib/libswan/unbound.c:35:52: fatal error: unbound-event.h: No such file or directory

# USE_FIPSCHECK=true \
# programs/pluto/plutomain.c:102:51: fatal error: fipscheck.h: No such file or directory
# A kernel compiled with CONFIG_CRYPTO_FIPS=y
#  can be booted in fips mode by specifying fips=1 as kernel parameter. 

# USE_LABELED_IPSEC=true \
# programs/pluto/security_selinux.h:18:29: fatal error: selinux/selinux.h: No such file or directory

# USE_LINUX_AUDIT=true \ Got Workin with swig and audit
# programs/pluto/log.h:215:51: fatal error: libaudit.h: No such file or directory

# Include LDAP support (currently used for fetching CRLs)
# USE_LDAP=true \ Works

# Support for Network Manager
# USE_NM=true \ Works

# USE_NIC_OFFLOAD=true \ Works

# USE_SECCOMP=true \
# include/lswseccomp.h:24:21: fatal error: seccomp.h: No such file or directory

# USE_XAUTHPAM=true \
# programs/pluto/pam_conv.c:32:61: fatal error: security/pam_appl.h: No such file or directory

# USE_XFRM_HEADER_COPY=true \ Works

CFLAGS:=$(CFLAGS) -fno-strict-aliasing
	#USERCOMPILE="-g -DGCC_LINT %{optflags} %{?efence} -fPIE -pie -fno-strict-aliasing -Wformat-nonliteral -Wformat-security" \

LIBRE_FLAGS:=\
	INITSYSTEM=sysvinit \
	ARCH=$(mARCH) V=1 \
	USERCOMPILE="-g -DGCC_LINT -fPIE -pie -fno-strict-aliasing -Wformat-nonliteral -Wformat-security" \
	DEST_DIR=/build/buildroot/libreswan \
	FINALLIBEXECDIR=/usr/libexec/ipsec \
	FINALRUNDIR=/var/run/pluto \
	KERNELRSC=/build/sources/linux/linux \
	INC_RCDIRS=/etc/rc.d \
	INC_RCDEFAULT=/etc/rc.d \
	INC_USRLOCAL=/usr \
	USE_KLIPS=true \
	USE_DNSSEC=false \
	USE_FIPSCHECK=false \
	USE_LABELED_IPSEC=false \
	USE_LINUX_AUDIT=true \
	USE_LDAP=true \
	USE_LIBCAP_NG=true \
	USE_LIBCURL=true \
	USE_NM=true \
	USE_NIC_OFFLOAD=true \
	USE_SECCOMP=false \
	USE_XAUTHPAM=false \
	USE_XFRM_HEADER_COPY=true \
	WERROR_CFLAGS=""

#export NSS_LDFLAGS = -lnss3 -lfreebl3 -lnssutil3
#NSS_LDFLAGS = -L/usr/pkg/lib/nss -Wl,-rpath,/usr/pkg/lib/nss -lnss3 -lfreebl3 -lssl3

compile: configure
	@echo; echo; echo "compile base"; echo
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) $(LIBRE_FLAGS) base

	@echo; echo; echo "compile module"; echo
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) $(LIBRE_FLAGS) module
	#@echo; echo; echo "compile module"; echo
	#make $(JOBS) -C $(COMPILE_DIR) USE_KLIPS=true module

install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)
	#${PKG_DIR}
	#mkdir -vp $(PKG_ROOT)$(MOD_DEST)
	#mkdir -vp $(PKG_ROOT)/lib/modules/$(K_RAW_VERSION)$(KERNEL_TYPE)
	@echo; echo; echo "install-base"; echo
	$(MAKE) KERNEL_VER=$(KERNEL_VER) DESTDIR=$(PKG_ROOT) -C $(COMPILE_DIR) $(LIBRE_FLAGS) install-base

	@echo; echo; echo "module_install"; echo
	$(MAKE) KERNEL_VER=$(KERNEL_VER) DESTDIR=$(PKG_ROOT) -C $(COMPILE_DIR) $(LIBRE_FLAGS) module_install
	rm -vrf $(PKG_ROOT)$(PKG_DIR)/rc* $(PKG_ROOT)$(PKG_DIR)/etc/ipsec.conf $(PKG_ROOT)/var

include ../Makefile.rules
