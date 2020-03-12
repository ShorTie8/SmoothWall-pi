# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
#	For s-t-p,  RIP, ShorTie
#
# This code is distributed under the terms of the GPL v2.
#
# tar -cJf FFC-mod.tar.xz sources/FFC/Makefile sources/FFC/install sources/FFC/fullfirewall sources/FFC/sources

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = FFC
VERSION = 3.1.8

FFC_ROOT = distrib/var/smoothwall/mods/fullfirewall

PREPARE = yes
$(DIR)/:
	@echo; echo "prepare"
	mkdir -vp {$(DIR)/{libsmooth,setup},smoothd}

	@echo; echo "prepare smoothd for sysiptables.so"
	cp -v ../smoothd/smoothd-0.0/*.h smoothd
	cp -v ../smoothd/smoothd-0.0/*.cpp smoothd
	cp -v ../smoothd/smoothd-0.0/*.hpp smoothd
	cp -v ../smoothd/smoothd-0.0/default smoothd
	cp -v ../smoothd/smoothd-0.0/Makefile smoothd
	cp -v sources/sysiptables.cpp smoothd

	@echo; echo "prepare libsmooth+setup"
	cp -v ../libsmooth+setup/libsmooth+setup-0.0/setup/*.c $(DIR)/setup
	cp -v ../libsmooth+setup/libsmooth+setup-0.0/setup/*.h $(DIR)/setup
	cd $(DIR); cp -v ../sources/{main.c,setup.h,Makefile} setup

	@echo; echo "prepare libsmooth"
	cp -v ../libsmooth+setup/libsmooth+setup-0.0/libsmooth/*.c $(DIR)/libsmooth
	cp -v ../libsmooth+setup/libsmooth+setup-0.0/libsmooth/*.h $(DIR)/libsmooth
	cp -v ../libsmooth+setup/libsmooth+setup-0.0/libsmooth/makelangs.pl $(DIR)/libsmooth
	cp -v ../libsmooth+setup/libsmooth+setup-0.0/libsmooth/langs.h.temp $(DIR)/libsmooth
	cp -v ../libsmooth+setup/libsmooth+setup-0.0/libsmooth/Makefile $(DIR)/libsmooth

COMPILE = yes
compile: $(DIR)/
	@echo; echo; echo "compile smoothd/sysiptables.cpp"
	(IPTABLES_VER=$(IPTABLES_VER) make $(JOBS) -C smoothd)
	@echo; echo; echo "compile libsmooth"
	make $(JOBS) -C $(DIR)/libsmooth
	@echo; echo; echo "compile setup"
	make $(JOBS) -C $(DIR)/setup

INSTALL = yes
install: compile
	@echo; echo "mkdir's"
	mkdir -vp $(PKG_ROOT)/var/smoothwall/mods-available/FFC
	mkdir -vp distrib/{usr/sbin,var/smoothwall/mods}

	@echo; echo "populate distrib"
	cp -vR fullfirewall distrib/var/smoothwall/mods

	@echo; echo "install our sysiptables.so"
	install -D smoothd/sysiptables.so $(FFC_ROOT)/usr/lib/smoothd/sysiptables.so

	@echo; echo "install our setup"
	cp -v $(DIR)/setup/setup distrib/usr/sbin/setup

	@echo; echo "install install.sh"
	cp -v  install/install.sh $(PKG_ROOT)/var/smoothwall/mods-available/FFC

	@echo; echo "install install-ffc.pl"
ifeq ($(mTUPLE),$(mARCH))
	cp -v install/install-ffc.pl.orig distrib/var/smoothwall/mods/fullfirewall/install-ffc.pl
else
	cp -v install/install-ffc.pl.arm $(PKG_ROOT)/var/smoothwall/mods-available/FFC/install-ffc.pl
	@echo; echo "remove old perl junk"
	rm -vrf $(FFC_ROOT)/usr/lib/perl5/site_perl
endif

	@echo; echo "chown && chmod on httpd"
	cd $(FFC_ROOT); chown -v -R nobody:nobody httpd

	@echo
	cd $(FFC_ROOT); chown -v nobody:nobody portfw/protolist
	cd $(FFC_ROOT); chown -v nobody:nobody xtaccess/config

	@echo
	# They have moved Shell.pm since 5.14.4
	cd $(FFC_ROOT); sed -i 's/use Shell qw(rm touch);/use CPAN::Shell qw(rm touch);/' httpd/cgi-bin/advanced.cgi

	@echo; echo "create smoothwall-fullfirewall.tar.gz in PKG_ROOT"
	cd distrib; tar -zcvf $(PKG_ROOT)/var/smoothwall/mods-available/FFC/smoothwall-fullfirewall.tar.gz var

CLEAN = yes
clean:
ifndef BUILD_PHASE
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf distrib
	@rm -rf smoothd
else
	@echo " $(PACKAGE)"
	@echo; echo "clean"
	rm -rf $(DIR)
	rm -rf distrib
	rm -rf smoothd
	rm -rf $(PKG_ROOT)
	rm -vf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
