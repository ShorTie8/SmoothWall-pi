# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libxcrypt
VERSION = 4.5.2
DIR = libxcrypt-$(VERSION)
TARBALL = v$(VERSION)
BASE_URL = https://github.com/besser82/libxcrypt/archive/refs/tags

##	ReConfigure = yes	##	autoupdate: command not found

PREPARE = yes	##	autoreconf: command not found
$(DIR)/: download
	@echo; echo "PrePare"
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
#	@cp -v ../glibc/glibc-2.42/scripts/config.guess $(DIR)/config.guess
#	@cp -v ../glibc/glibc-2.42/scripts/config.sub $(DIR)/config.sub
#	cd $(DIR); ./autogen.sh
	cd $(DIR); libtoolize --copy --force
	cd $(DIR); autoreconf --install

CONFIG_OPTS += --disable-static \
			--enable-hashes=strong,glibc \
			--enable-obsolete-api \
			--disable-failure-tokens
		
include ../Makefile.rules
