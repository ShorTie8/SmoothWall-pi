# SmoothWall Build system.
#
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.
#
# Many Thankz to Ben Hutchings for the howto and key.

include ../Makefile.conf

PACKAGE = crda
VERSION = 4.14
#BASE_URL = https://mirrors.edge.kernel.org/pub/software/network/crda
#BASE_URL = https://git.kernel.org/pub/scm/linux/kernel/git/mcgrof/crda.git/snapshot

#### or github
VERSION +=.git
gitCommitID = f4ef2531698fb9ba006e8b31a223b3269be8bc7c
BASE_URL = https://git.kernel.org/pub/scm/linux/kernel/git/mcgrof/crda.git/snapshot
DIR = $(PACKAGE)-$(gitCommitID)
TARBALL = $(PACKAGE)-$(gitCommitID)
#### end github

#

#export CFLAGS = -O$(if $(findstring noopt,$(DEB_BUILD_OPTIONS)),0,2)

PRE_COMPILE = v=1 \
	RUNTIME_PUBKEY_ONLY=1
	# \
	#USE_OPENSSL=1  \#keys-ssl.c:63:22: error: 'keys' defined but not used [-Werror=unused-variable]


#PRE_COMPILE = v=1 USE_OPENSSL=1
#	LDLIBREG=-Wl,-rpath,$(LIBDIR) \

#	LIBDIR=/lib/crda \
#	REG_BIN=/lib/crda/regulatory.bin \
#	RUNTIME_PUBKEY_DIR=/lib/crda/pubkeys \
#	UDEV_RULE_DIR=/lib/udev/rules.d \
#	WERROR= \
	
#export DH_VERBOSE = 1

COMPILE = yes
compile: patch
	@echo; echo; echo "compile"; echo
	$(PRE_COMPILE) make $(JOBS) -C $(DIR)
	# $(CONFIG_OPTS)


INSTALL = yes
install: compile
	@echo; echo; echo "install"; echo
	mkdir -vp $(PKG_ROOT)/etc/defualt
	echo 'REGDOMAIN=US' > $(PKG_ROOT)/etc/defualt/crda
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install

	#install -D -m 0644 debian/crda.udev $(PKG_ROOT)/lib/udev/rules.d/60-crda.rules
	#install -D -o 0 -g 0 -m 755 debian/setregdomain $(PKG_ROOT)/crda/lib/crda/setregdomain
	#mkdir -vm 755 $(PKG_ROOT)/$(RUNTIME_PUBKEY_DIR)
	#install -D -m 0644 $(DIR)/pubkeys/*.pem debian/pubkeys/*.pem $(PKG_ROOT)/crda/lib/crda/pubkeys



include ../Makefile.rules
