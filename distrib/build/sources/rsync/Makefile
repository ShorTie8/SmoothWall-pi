# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = rsync
VERSION = 3.4.1

BASE_URL = http://rsync.samba.org/ftp/rsync/src

# Tool Chain Build Stage 3
#
ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS += --disable-lz4 \
				--disable-zstd \
				--disable-xxhash
endif

include ../Makefile.rules
