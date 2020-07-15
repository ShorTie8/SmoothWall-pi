# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
#	For wkitty42, ShorTie 2020
#
# This code is distributed under the terms of the GPL v2.
#
# tar -cJf GAR-mod.tar.xz sources/GAR/Makefile sources/GAR/Makefile.GAR sources/GAR/install.sh sources/GAR/uninstall.sh sources/GAR/install-gar.pl sources/GAR/stopsquid sources/GAR/settings sources/GAR/GAR.diff

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = GAR
VERSION = v4.0.6.7
GAR_URL = https://github.com/wkitty42/GAR/archive/master/GAR-$(VERSION).tar.gz

DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo
	echo "cloning git hub"
	mkdir -vp $(PKG_ROOT)/var/smoothwall/mods-available
	cd $(PKG_ROOT)/var/smoothwall/mods-available; git clone https://github.com/wkitty42/GAR
	cp -v GAR.diff $(PKG_ROOT)/var/smoothwall/mods-available/GAR/usr/bin
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/usr/bin; patch < GAR.diff

CONFIGURE = yes
configure: download
	@echo; echo "configure/prepare smoothd"
	mkdir -v smoothd
	cp -v ../smoothd/smoothd-0.0/*.h smoothd
	cp -v ../smoothd/smoothd-0.0/*.cpp smoothd
	cp -v ../smoothd/smoothd-0.0/*.hpp smoothd
	cp -v ../smoothd/smoothd-0.0/default smoothd
	cp -v $(PKG_ROOT)/var/smoothwall/mods-available/GAR/src/sysGAR.cpp smoothd
	cp -v Makefile.GAR smoothd/Makefile

COMPILE = yes
compile: configure
	@echo; echo; echo "compile smoothd/sysGAR.so"
	(IPTABLES_VER=$(IPTABLES_VER) make $(JOBS) -C smoothd)

INSTALL = yes
install: compile
	@echo; echo "install our sysGAR.so, install.sh, install-gar.pl && stopsquid"
	install -v -m 0644 settings $(PKG_ROOT)/var/smoothwall/mods-available/GAR
	install -v -m 0755 install.sh $(PKG_ROOT)/var/smoothwall/mods-available/GAR
	install -v -m 0755 uninstall.sh $(PKG_ROOT)/var/smoothwall/mods-available/GAR
	install -v -m 0755 install-gar.pl $(PKG_ROOT)/var/smoothwall/mods-available/GAR
	install -v -m 0755 -D stopsquid $(PKG_ROOT)/var/smoothwall/mods-available/GAR/usr/bin/smoothwall/stopsquid
	install -v smoothd/sysGAR.so $(PKG_ROOT)/var/smoothwall/mods-available/GAR/usr/lib/smoothd/sysGAR.so.$(mTUPLE)

	@echo; echo "chown && chmod on httpd"
	# via  GAR_permissions_list
	# not sure if backups is needed
	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/backup
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR; chown -v nobody:nobody backup
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR; chown -v nobody:nobody config
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR; chown -v nobody:nobody settings

	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR; chown -v -R nobody:nobody httpd

	# GAR.conf
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; cp -v GAR.conf GAR.conf.orig
	sed -e 's/^IgnoreSIDs.*$$/IgnoreSIDs /' -i $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc/GAR.conf
	sed -e 's/^IgnoreGIDs.*$$/IgnoreGIDs /' -i $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc/GAR.conf
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; chown -v nobody:nobody GAR.conf

	# GAR.ignore
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; mv -v GAR.ignore GAR.ignore.orig
	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc/GAR.ignore
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; chown -v nobody:nobody GAR.ignore

	# GAR.target
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; mv -v GAR.target GAR.target.orig
	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc/GAR.target
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; chown -v nobody:nobody GAR.target

	# gartool.conf
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; mv -v gartool.conf gartool.conf.orig
	#touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc/gartool.conf
	echo "include /var/smoothwall/mods/GAR/etc/tor_routers.conf" > $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc/gartool.conf
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; chown -v nobody:nobody gartool.conf
	#cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; chown -v nobody:nobody guardian-orig.conf

	# tor_routers.conf
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; mv -v tor_routers.conf tor_routers.conf.orig
	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc/tor_routers.conf
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/etc; chown -v nobody:nobody tor_routers.conf

	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/usr/lib/smoothwall/services; chown -v nobody:nobody GAR
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/db; chown -v nobody:nobody GARipblock
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/db; chown -v nobody:nobody unblock

	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log/{GAR.log,snortstats.err,snortstats.log}
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log; chown -v nobody:nobody GAR.log
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log; chown -v nobody:nobody snortstats.err
	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log; chown -v nobody:nobody snortstats.log

#	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log/{GAR.log.1.gz,GAR.log.2.gz,GAR.log.3.gz}
#	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log/{GAR.log.4.gz,GAR.log.5.gz,GAR.log.6.gz}
#	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log/{GAR.log.7.gz,GAR.log.8.gz}
#	cd $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log; chown -v nobody:nobody GAR.log.*.gz
#	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log/{snortstats.err.1.gz,snortstats.err.2.gz}
#	touch $(PKG_ROOT)/var/smoothwall/mods-available/GAR/var/log/{snortstats.err.3.gz,snortstats.err.4.gz}

CLEAN = yes
clean:
ifndef BUILD_PHASE
	@echo -n " $(PACKAGE)"
	@rm -rf smoothd
else
	@echo " $(PACKAGE)"
	@echo; echo "clean"
	rm -rf smoothd
	rm -rf $(PKG_ROOT)
	rm -vf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
