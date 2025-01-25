# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = daq
VERSION = 2.0.7
export NO_CHECK_CERT = 1

BASE_URL = https://www.snort.org/downloads/snort

DIR = $(PACKAGE)-$(VERSION)

CONFIG_OPTS += --disable-bundled-modules --enable-nfq-module \
	      --enable-pcap-module --enable-dump-module 

PREPARE = yes
$(DIR)/: download
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	echo "autoreconf"
	cd $(DIR); autoreconf

include ../Makefile.rules
