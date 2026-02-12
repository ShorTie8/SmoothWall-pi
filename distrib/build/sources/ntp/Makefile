# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

##	/var/db/repos/gentoo/net-misc/ntp##

include ../Makefile.conf

PACKAGE = ntp
VERSION = 4_2_8P18
TARBALL = NTP_$(VERSION)
DIR =  ntp-$(TARBALL)
BASE_URL = https://github.com/ntp-project/ntp/archive/refs/tags

PATCH_FILE1 = ntp-4.2.8_p18-ipc-caps.patch # bug #533966
#PATCH_FILE2 = ntp-4.2.8-sntp-test-pthreads.patch # bug #563922
PATCH_FILE3 = ntp-4.2.8_p14-add_cap_ipc_lock.patch # bug #711530
PATCH_FILE4 = ntp-4.2.8_p15-configure-clang16.patch
PATCH_FILE5 = ntp-4.2.8_p18-c99.patch # bug #956643
PATCH_FILE6 = ntp-4.2.8_p18-r2-bind-fail-NULL-dereference.patch

PRE_CONFIGURE = LIBS=-lpthread

export PATH_RUBY=/bin/false

PATCH = yes
patch: $(DIR)/
	@echo; echo "Patch";echo
	@echo; echo "Patch";echo
	(cd $(DIR); \
	for PATCH in $(PATCH_FILE1) $(PATCH_FILE2) $(PATCH_FILE3) $(PATCH_FILE4) \
			$(PATCH_FILE5) $(PATCH_FILE6) $(PATCH_FILE7) $(PATCH_FILE8); do \
	  echo $$PATCH; \
	  FILENAME=../$$PATCH; \
	  echo; echo $$FILENAME; \
	  [ -f $$FILENAME ] || exit 8; \
	  cat $$FILENAME | patch -p1 || exit 14; \
	done;)

	# Make sure every build uses the same install layout, bug #539092
	cd $(DIR); find sntp/loc/ -type f '!' -name legacy -delete || die

#	@echo; echo "autoupdate"; cd $(DIR); autoupdate
	@#echo; echo "autoconf"; cd $(DIR); autoconf
#	@echo; echo "autoreconf -ifv"; cd $(DIR); autoreconf -ifv

	# Disable pointless checks.
	cd $(DIR); touch .checkChangeLog .gcc-warning FRC.html html/.datecheck || die

CONFIG_OPTS += \
		--sysconfdir=/etc \
		--with-binsubdir=sbin \
		--with-lineeditlibs=readline \
		LIBS=-ltinfo \
		LIBS=-lpthread

CONFIGURE = yes
configure: patch
	@echo; echo; echo "Configure"; echo
	@echo  -e "/n/n  bootstrap/n"
	(cd $(DIR); ./bootstrap)
	@echo "  update config.guess/config.sub"
	@for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf $(ROOT)/build/toolcrib/$$(basename $${i}) $${i}; done
	@echo; echo "autoconf"; cd $(DIR); autoconf
	(cd $(DIR); $(PRE_CONFIGURE) ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@install -D $(COMPILE_DIR)/ntpdate/ntpdate $(PKG_ROOT)/usr/sbin/ntpdate 
	@install -D $(COMPILE_DIR)/ntpq/ntpq $(PKG_ROOT)/usr/sbin/ntpq 

include ../Makefile.rules
