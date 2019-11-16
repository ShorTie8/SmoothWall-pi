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

TARBALL = $(FREESWAN_TYPE)-$(VERSION)

PATCH_FILE1 = makefile.patch
PATCH_FILE2 = setup.in.smoothwall.patch
PATCH_FILE3 = ipsec.init.in.patch

KNL_SRC = ../linux$(KERNEL_TYPE)/linux
MOD_DEST = /lib/modules/$(K_RAW_VERSION)$(KERNEL_TYPE)/kernel/net/ipsec

unpack: $(DIR)/
	@true

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	cp makefile.inc.local $(DIR)/Makefile.inc.local

CFLAGS:=$(CFLAGS) -fno-strict-aliasing
	#USERCOMPILE="-g -DGCC_LINT %{optflags} %{?efence} -fPIE -pie -fno-strict-aliasing -Wformat-nonliteral -Wformat-security" \

LIBRE_FLAGS:=\
	USERCOMPILE="-g -DGCC_LINT -fPIE -pie -fno-strict-aliasing -Wformat-nonliteral -Wformat-security" \
	V=1 \
	FINALLIBEXECDIR=/usr/libexec/ipsec \
	FINALRUNDIR=/var/run/pluto \
	KERNELRSC=$(KNL_SRC) \
	INC_RCDIRS=/etc/rc.d \
	INC_RCDEFAULT=/etc/rc.d \
	INC_USRLOCAL=/usr \
	MANTREE=/usr/share/man \
	USE_DNSSEC=false \
	USE_FIPSCHECK=false \
	USE_LABELED_IPSEC=false \
	USE_LINUX_AUDIT=false \
	USE_LDAP=false \
	USE_LIBCAP_NG=true \
	USE_LIBCURL=true \
	USE_NM=false \
	USE_NIC_OFFLOAD=false \
	USE_SECCOMP=false \
	USE_XAUTHPAM=false \
	USE_XFRM_HEADER_COPY=false \
	WERROR_CFLAGS=""

compile: configure
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) $(LIBRE_FLAGS) base
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) $(LIBRE_FLAGS) module

install: compile
	mkdir -p $(PKG_ROOT)${PKG_DIR}
	tput smso;echo "INSTALL";tput rmso;sleep 1
	$(MAKE) KERNEL_VER=$(KERNEL_VER) DESTDIR=$(PKG_ROOT) -C $(COMPILE_DIR) $(LIBRE_FLAGS) install-base
	$(MAKE) KERNEL_VER=$(KERNEL_VER) DESTDIR=$(PKG_ROOT) -C $(COMPILE_DIR) $(LIBRE_FLAGS) module_install
	rm -rf $(PKG_ROOT)$(PKG_DIR)/rc* $(PKG_ROOT)$(PKG_DIR)/etc/ipsec.conf $(PKG_ROOT)/var

include ../Makefile.rules
