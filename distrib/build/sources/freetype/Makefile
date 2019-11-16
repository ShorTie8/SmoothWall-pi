include ../Makefile.conf

PACKAGE = freetype
VERSION = 2.5.5

BASE_URL = http://download.savannah.gnu.org/releases/freetype/

EXTENSION = .tar.bz2

CONFIG_OPTS += --prefix=$(PKG_DIR)

CONFIGURE = yes

configure: patch
	(cd $(DIR); ./configure $(CONFIG_OPTS))

include ../Makefile.rules

