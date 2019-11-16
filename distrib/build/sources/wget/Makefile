# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = wget
VERSION = 1.19.2

BASE_URL = ftp://ftp.gnu.org/gnu/wget
EXTENSION = .tar.gz

# Some sites disallow HTTP
ifeq ($(BUILD_PHASE), Stage_3)
CONFIG_OPTS += --with-ssl=openssl --with-libssl-prefix=$(PKG_DIR)
endif

ifeq ($(BUILD_PHASE), Final)
CONFIG_OPTS += --with-ssl=openssl
endif

COMPILE = yes
compile: configure
	$(MAKE) $(JOBS) -C $(COMPILE_DIR)
	echo "ca_certificate = /usr/lib/ssl/certs/ca-certificates.crt" \
	  >> $(COMPILE_DIR)/doc/sample.wgetrc

include ../Makefile.rules
