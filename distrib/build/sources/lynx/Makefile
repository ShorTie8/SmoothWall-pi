include ../Makefile.conf

PACKAGE = lynx
#VERSION = 2.8.9rel.1
VERSION = 2.9.2
EXTENSION = .tar.bz2
LICENCE_FILE = $(DIR)/COPYING

BASE_URL = https://invisible-mirror.net/archives/lynx/tarballs

TARBALL = $(PACKAGE)$(VERSION)

#DIR = $(PACKAGE)$(subst .,-,$(VERSION))
#DIR = lynx2.8.9rel.1

CONFIG_OPTS += --with-screen=ncurses

include ../Makefile.rules
