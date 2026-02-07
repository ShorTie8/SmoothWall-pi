# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libdaq
VERSION = 3.0.24
TARBALL = v$(VERSION)
BASE_URL = https://github.com/snort3/libdaq/archive/refs/tags

CONFIG_OPTS += --disable-bundled-modules --enable-nfq-module \
	      --enable-pcap-module --enable-dump-module 

PREPARE = yes
$(DIR)/: download
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	echo "./bootstrap"
	cd $(DIR); ./bootstrap

include ../Makefile.rules
