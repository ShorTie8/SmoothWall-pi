# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = nano
VER_MAG = 8
VER_MIN = 7
VERSION = $(VER_MAG).$(VER_MIN)
EXTENSION = .tar.xz
BASE_URL = https://www.nano-editor.org/dist/v$(VER_MAG)

#ReConfigure = yes
PRE_CONFIGURE = LIBS=-ltinfo

#CFLAGS += -std=gnu17

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) prefix=$(PKG_ROOT)$(PKG_DIR) install

include ../Makefile.rules
