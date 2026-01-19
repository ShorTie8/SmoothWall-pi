include ../Makefile.conf

PACKAGE = freetype
VERSION = 2.14.1
EXTENSION = .tar.xz
BASE_URL = http://download.savannah.gnu.org/releases/freetype/

CONFIG_OPTS += --prefix=$(PKG_DIR)

CONFIGURE = yes
configure: patch
	(cd $(DIR); ./configure $(CONFIG_OPTS))

include ../Makefile.rules

