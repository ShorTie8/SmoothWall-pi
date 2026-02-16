# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = snort3
VERSION = 3.10.2.0
TARBALL = $(VERSION)
BASE_URL = https://github.com/snort3/snort3/archive/refs/tags

##	https://medium.com/@berkay.vagas/a-step-by-step-study-on-installing-and-configuring-snort3-in-a-virtualized-ubuntu-environment-e6d11a2a8530
## = wget https://archives.boost.io/release/1.77.0/source/boost_1_77_0.tar.gz

CONFIG_OPTS = --prefix=$(PKG_DIR) \
	      --builddir=build \
	      --build-type=Release \
	      --enable-hardened-build \
	      --enable-pie \
	      --enable-tsc-clock \
	      --disable-docs \
	      --with-luajit-includes=/usr/local/include/luajit-2.1 \
	      --with-luajit-libraries=/usr/local/lib/luajit-2.1
	       

CONFIGURE = yes
configure: patch
	@echo -e "\n\n  Configure  \n"
	cd $(DIR); ./configure_cmake.sh $(CONFIG_OPTS)

COMPILE = yes
compile: configure
	@echo -e "\n\n  Compile  \n"
	cd $(DIR)/build; make $(JOBS)

INSTALL = yes
install: compile
	@echo -e "\n\n  Install  \n"
	@ # Disable problematic rule(s)
	@cd $(COMPILE_DIR)/preproc_rules; sed -i -e 's/\(alert ( msg: "STREAM5_NO_3WHS"; sid: 20; gid: 129\)/#\1/' preprocessor.rules
	@mkdir -p $(PKG_ROOT)
	cd $(DIR)/build; make $(JOBS) DESTDIR=$(PKG_ROOT) install
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
