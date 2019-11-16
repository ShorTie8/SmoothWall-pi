# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = inotify-tools
VERSION = 3.20.1

TARBALL = $(VERSION)

#DIR = $(PACKAGE)-$(VERSION)


#BASE_URL = https://github.com/rvoicilas/inotify-tools/archive/3.20.1.tar.gz/inotify-tools-3.20.1.tar.gz
BASE_URL = https://github.com/rvoicilas/inotify-tools/archive

PATCH = yes
patch: $(DIR)/
	@echo; echo; echo "patch"
	# 
	cd $(DIR); autoreconf -vif


include ../Makefile.rules
