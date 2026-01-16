# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = eudev
VERSION = 3.2.14
#VERSION = 3.2.6
#VERSION = 3.2.7
#VERSION = 3.2.8

##	BASE_URL = http://dev.gentoo.org/~blueness/eudev
BASE_URL = https://github.com/eudev-project/eudev/releases/download/v$(VERSION)

#CFLAGS += -std=gnu17

#PATCH_FILE1 = udev-watch.c.patch
#PATCH_FILE1 = fix-gperf-3.1.patch
#PATCH_FILE1 = 60-network-bridges.patch

PKG_DIR = 

# VERSION = 3.2.5
CONFIG_OPTS += \
	      --bindir=/sbin            \
              --config-cache            \
	      --disable-silent-rules    \
              --disable-static          \
	      --datarootdir=/usr/share  \
              --enable-manpages         \
	      --enable-rule_generator   \
	      --includedir=/usr/include \
	      --libdir=/lib             \
	      --libexecdir=/lib         \
	      --prefix=/usr             \
	      --sbindir=/sbin           \
	      --sysconfdir=/etc         \
              --with-rootprefix=""      \
              --with-rootlibdir=/lib

#CONFIG_OPTS += \
#		--bindir=/sbin          \
#		--sbindir=/sbin         \
#		--libdir=/usr/lib       \
#		--sysconfdir=/etc       \
#		--libexecdir=/lib       \
#		--with-rootprefix=      \
#		--with-rootlibdir=/lib  \
#		--enable-manpages       \
#		--disable-static        \
#		--config-cache

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@echo; echo; echo "Configure"; echo
	#exit 44
	#cp -v 60-network-bridges.rules $(COMPILE_DIR)/rules
	##chmod -v 0644 $(COMPILE_DIR)/rules/60-network-bridges.rules
	cd $(DIR); \
	  ( echo 'HAVE_BLKID=1'; \
	    echo 'BLKID_LIBS="-lblkid"'; \
	    echo 'BLKID_CFLAGS="-I/tools/include"') > config.cache
	@echo; echo; echo "configure"; echo
	cd $(DIR); ./configure $(CONFIG_OPTS)

compile: configure
	@echo; echo; echo "Compile"; echo
	# Udev insists on making the docs even though expressly told not to
	# So brutally bypass it
	#@cd $(DIR); sed -i -e 's=.*http://docbook.*=\ttrue=' Makefile
	# *Now* we can build
	#@$(MAKE) $(JOBS) -C $(COMPILE_DIR) $(CONFIG_OPTS)
	LIBRARY_PATH=/tools/lib make $(JOBS) -C $(DIR)

install: compile
	mkdir -vp $(PKG_ROOT)
	@echo; echo; echo "Install"; echo
	@echo; echo; echo "Check"; echo
	#make LD_LIBRARY_PATH=/tools/lib check
	@echo; echo; echo "Install"; echo
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	cd $(PKG_ROOT); rm -rf usr/lib*;
	cd $(PKG_ROOT); install -dv etc/udev/rules.d;
	cd $(PKG_ROOT); install -dv lib/firmware;
	cd $(PKG_ROOT); install -dv lib/udev/devices/pts;
	cd $(PKG_ROOT); install -dv lib/udev/devices/shm;
	cd $(PKG_ROOT)/lib/udev/rules.d; \
	    sed -i -e 's/\(^ENV{MATCHADDR}=="52:54:00:.*generator_end"\)/#\1/' \
	           -e 's/\(^SUBSYSTEMS=="xen"\)/#\1/' \
	           -e 's/\(^ENV{MATCHADDR}=="\?\[2367abef\]:\*".*\)/#\1/' \
	           -e 's/\(^ENV{MATCHADDR}=="00:0c:29:.*generator_end"\)/#\1/' \
	           -e 's/\(^ENV{MATCHADDR}=="00:15:5d:.*generator_end"\)/#\1/' \
	       75-persistent-net-generator.rules
	#install -v -m 644 60-network-bridges.rules $(PKG_ROOT)/lib/udev/rules.d/60-network-bridges.rules
	#install -v -m 755 network-bridges $(PKG_ROOT)/lib/udev/network-bridges

include ../Makefile.rules
