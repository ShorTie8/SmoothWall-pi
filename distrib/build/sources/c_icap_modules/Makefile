include ../Makefile.conf

PACKAGE = c_icap_modules
VERSION = 0.5.3

PACKAGE_ALT = c-icap

BASE_URL = http://downloads.sourceforge.net/project/$(PACKAGE_ALT)/$(PACKAGE_ALT)-modules/0.5.x

CONFIGURE = yes
configure: patch
	(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
ifneq ($(DIR), $(COMPILE_DIR))
	(cd $(COMPILE_DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" $(PRE_CONFIGURE) ../$(DIR)/configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))
else
	(cd $(COMPILE_DIR); CXXFLAGS="$(CFLAGS)" CFLAGS="$(CFLAGS)" $(PRE_CONFIGURE) ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS))
endif
	# Patch makefile's install
	cd $(COMPILE_DIR)/services/url_check; sed -i -e '/^INSTALL = / s/$$/ -D/' Makefile

include ../Makefile.rules
