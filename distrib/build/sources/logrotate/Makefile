# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = logrotate
VERSION = 3.22.0
TARBALL = $(VERSION)
BASE_URL = https://github.com/logrotate/logrotate/archive/refs/tags

PATCH = yes
patch: $(DIR)/
	@echo; echo "Patch";echo
	@cd $(DIR); ./autogen.sh
	
include ../Makefile.rules
