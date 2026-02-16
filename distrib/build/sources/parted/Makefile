# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = parted
VERSION = 3.6
EXTENSION = .tar.xz
BASE_URL = http://ftp.gnu.org/gnu/parted/

CONFIG_OPTS += --disable-nls --disable-device-mapper --disable-silent-rules

PATCH = yes
 patch: $(DIR)/
	##	First, make the package compatible with gcc-15:
	cd $(DIR); sed -i 's/do_version ()/do_version (PedDevice** dev, PedDisk** diskp)/' parted/parted.c

include ../Makefile.rules
