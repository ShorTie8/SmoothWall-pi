# SmoothWall Build system.
#
# (c) ShorTie 2019
#
# This code is distributed under the terms of the GPL v2.

# https://www.ccsinfo.com/forum/viewtopic.php?t=50256

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = wiringPi
VERSION = 2.46
#VERSION = 2.52

#commit	8d188fa0e00bb8c6ff6eddd07bf92857e9bd533a

DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo
	if [ -a $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz.done ]; then \
		echo; echo; echo "got it already"; echo; \
	else \
		echo; echo; echo "downloading"; echo; \
		git clone git://git.drogon.net/wiringPi wiringPi-$(VERSION); \
		tar -zcvf $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz $(DIR); \
		touch $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz.done; \
	fi

PATCH = yes
patch: $(DIR)/
	@true

COMPILE = yes
compile: patch
	@echo; echo; echo "compile WiringPi Library"; echo
	make $(JOBS) PREFIX= -C $(DIR)/wiringPi
	@echo; echo "install"; echo
	make PREFIX= -C $(DIR)/wiringPi install
	@echo; echo; echo "compile WiringPi Devices Library"; echo
	make PREFIX= $(JOBS) -C $(DIR)/devLib
	@echo; echo "install"; echo
	make PREFIX= -C $(DIR)/devLib install
	@echo; echo; echo "compile GPIO Utility"; echo
	make PREFIX= $(JOBS) -C $(DIR)/gpio

INSTALL = yes
install: compile
	@echo; echo; echo "Install"; echo
	mkdir -vp $(PKG_ROOT)/{lib,bin}
	@echo; echo; echo "install wiringPi"; echo
	make PREFIX= -C $(DIR)/wiringPi DESTDIR=$(PKG_ROOT) install
	@echo; echo "install devLib"; echo
	make PREFIX= -C $(DIR)/devLib DESTDIR=$(PKG_ROOT) install
	@echo; echo "install gpio"; echo
	make PREFIX= -C $(DIR)/gpio DESTDIR=$(PKG_ROOT) install
	
include ../Makefile.rules
