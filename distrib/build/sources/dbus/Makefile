# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = dbus
VERSION = 1.16.2
EXTENSION = .tar.xz
BASE_URL = https://dbus.freedesktop.org/releases/dbus

CONFIGURE = yes
configure: patch
	@echo -e "/n/n  Configure  /n"
	mkdir -vp $(PKG_ROOT)
	cd $(DIR); meson setup builddir \
					--prefix=$(PKG_ROOT)/$(PKG_DIR) \
					--buildtype=release \
					--wrap-mode=nofallback \
					-Dsystemd=disabled

COMPILE = yes
compile: configure
	@echo -e "/n/n  Compile  /n"
	cd $(DIR); ninja -C builddir
	
INSTALL = yes
install: compile
	@echo -e "/n/n  Install  /n"
	cd $(DIR); ninja -C builddir install
	echo; echo
#	chown -v root:messagebus /usr/libexec/dbus-daemon-launch-helper
#	chmod -v      4750       /usr/libexec/dbus-daemon-launch-helper

include ../Makefile.rules
