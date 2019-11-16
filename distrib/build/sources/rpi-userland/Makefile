# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2018
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = rpi-userland
VERSION = master
DIR = userland-master
COMPILE_DIR = $(DIR)-compile

DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo
	if [ ! -f $(DOWNLOADS_DIR)/rpi-userland-master.tar.gz ]; then \
	  wget -c -N https://github.com/raspberrypi/userland/archive/master.tar.gz -O $(DOWNLOADS_DIR)/rpi-userland-master.tar.gz ; \
	else \
	  echo "Got it" ; \
	fi; \

PATCH = yes
patch: $(DIR)/
	@echo; echo; echo "patch"
	cp -v $(DIR)/makefiles/cmake/vmcs.cmake $(DIR)/makefiles/cmake/vmcs.cmake.orig
	cd $(DIR); patch -p1 < ../disable-hello_pi.patch
	#cd $(DIR); patch -p1 < ../usr-fix.patch

CONFIGURE = yes
configure: patch
	@echo; echo; echo "configure"; echo
	mkdir $(COMPILE_DIR)
ifeq ($(mTUPLE), pi4-64)
	cd $(COMPILE_DIR); cmake -DARM64=ON -DCMAKE_BUILD_TYPE=release -DCMAKE_INSTALL_PREFIX=/usr -DVMCS_INSTALL_PREFIX=/usr ../$(DIR)
else
	cd $(COMPILE_DIR); cmake -DCMAKE_BUILD_TYPE=release -DCMAKE_INSTALL_PREFIX=/usr -DVMCS_INSTALL_PREFIX=/usr ../$(DIR)
endif
 
include ../Makefile.rules
