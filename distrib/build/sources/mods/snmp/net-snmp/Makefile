include ../../../Makefile.conf

PACKAGE = net-snmp
VERSION = 5.7.2.1

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = http://sourceforge.net/projects/net-snmp/files/net-snmp/5.7.2.1

CONFIG_OPTS = --with-defaults --disable-applications --disable-manuals --disable-scripts

PATCH_FILE1 = net-snmp-pidfix.patch

INSTALL = yes

install: compile
	-mkdir $(PKG_ROOT)
	@make -C $(DIR) INSTALL_PREFIX=$(PKG_ROOT) install

include ../../../Makefile.rules
