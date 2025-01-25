# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = snort
VERSION = 2.9.20
export NO_CHECK_CERT = 1

BASE_URL = https://www.snort.org/downloads/snort

CONFIG_OPTS += --enable-gre --enable-targetbased --enable-ppm --enable-sourcefire \
	      --enable-perfprofiling --enable-zlib --enable-non-ether-decoders

PREPARE = yes
$(DIR)/: download
	@tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)

INSTALL = yes
install: compile
	@ # Disable problematic rule(s)
	@cd $(COMPILE_DIR)/preproc_rules; sed -i -e 's/\(alert ( msg: "STREAM5_NO_3WHS"; sid: 20; gid: 129\)/#\1/' preprocessor.rules
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@mkdir -p $(PKG_ROOT)/var/smoothwall/snort/rules/
	@mkdir -p $(PKG_ROOT)/var/smoothwall/snort/preproc_rules/
	@mkdir -p $(PKG_ROOT)/var/smoothwall/snort/so_rules/
	@mkdir -p $(PKG_ROOT)/var/smoothwall/snort/reputation_lists/
	@touch $(PKG_ROOT)/var/smoothwall/snort/rules/local.rules
	@touch $(PKG_ROOT)/var/smoothwall/snort/rules/deleted.rules
	@touch $(PKG_ROOT)/var/smoothwall/snort/reputation_lists/black.list
	@touch $(PKG_ROOT)/var/smoothwall/snort/reputation_lists/white.list
	@install -D $(COMPILE_DIR)/etc/unicode.map \
	    $(PKG_ROOT)/var/smoothwall/snort/unicode.map
	@install -D $(COMPILE_DIR)/etc/classification.config \
	    $(PKG_ROOT)/var/smoothwall/snort/classification.config
	@install -D $(COMPILE_DIR)/etc/reference.config \
	    $(PKG_ROOT)/var/smoothwall/snort/reference.config
	@install -D $(COMPILE_DIR)/preproc_rules/preprocessor.rules \
	    $(PKG_ROOT)/var/smoothwall/snort/preproc_rules/preprocessor.rules
	@install -D $(COMPILE_DIR)/preproc_rules/decoder.rules \
	    $(PKG_ROOT)/var/smoothwall/snort/preproc_rules/decoder.rules
	@chown nobody:nobody -R $(PKG_ROOT)/var/smoothwall/
	@mkdir -p $(PKG_ROOT)/$(MODULE_DIR)/usr/lib/smoothwall
	@echo $(VERSION) > $(PKG_ROOT)/$(MODULE_DIR)/usr/lib/smoothwall/snortversion
	SNORT_OPTS=`echo -n "$(CONFIG_OPTS)" | sed -e 's/ +/ /'`; \
	  sed -i -e '/OPTIONS :/s@:.*$$@: '"$$SNORT_OPTS@" \
	      -e '/OPTIONS :/a #     SWE built : $(PACKAGE)-$(VERSION)' \
	      $(COMPILE_DIR)/etc/snort.conf
	sed -f snort.conf.sed < $(COMPILE_DIR)/etc/snort.conf > $(COMPILE_DIR)/etc/snort.conf-new
	install -D $(COMPILE_DIR)/etc/snort.conf-new $(PKG_ROOT)/etc/snort.conf
	chown root:root -R $(PKG_ROOT)/etc
	chmod 755 -R $(PKG_ROOT)/etc
	chmod 644 -R $(PKG_ROOT)/etc/snort.conf

include ../Makefile.rules
