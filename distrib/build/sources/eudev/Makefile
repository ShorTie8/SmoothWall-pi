# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = eudev
VERSION = 3.2

BASE_URL = http://dev.gentoo.org/~blueness/eudev

#PATCH_FILE1 = udev-watch.c.patch

PKG_DIR = 

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


CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	cd $(COMPILE_DIR); \
	  ( echo 'HAVE_BLKID=1'; \
	    echo 'BLKID_LIBS="-lblkid"'; \
	    echo 'BLKID_CFLAGS="-I/tools/include"') > config.cache
	cd $(COMPILE_DIR); ./configure $(CONFIG_OPTS)

compile: configure
	# Udev insists on making the docs even though expressly told not to
	# So brutally bypass it
	#@cd $(DIR); sed -i -e 's=.*http://docbook.*=\ttrue=' Makefile
	# *Now* we can build
	@$(MAKE) $(JOBS) -C $(COMPILE_DIR)

install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
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


include ../Makefile.rules
