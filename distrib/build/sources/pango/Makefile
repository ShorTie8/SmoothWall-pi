# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = pango
VER_MM = 1.57
VERSION = $(VER_MM).0
EXTENSION = .tar.xz
#PRE_CONFIGURE = ENABLE_GTK_DOC_FALSE=''

BASE_URL = https://download.gnome.org/sources/pango/$(VER_MM)

PREPARE = yes
$(DIR)/: download
	@echo; echo "prepare"
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
ifeq ($(mARCH), arm64)
	for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf ../glibc/glibc-*/scripts/$$(basename $${i}) $${i}; \
	done
endif

CONFIG_OPTS += --prefix=/usr --without-x
INSTALL = yes
install: compile
	mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) install DESTDIR=$(PKG_ROOT)
	install -dv $(PKG_ROOT)$(PKG_DIR)/etc/pango

include ../Makefile.rules

