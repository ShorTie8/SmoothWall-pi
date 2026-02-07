# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = iftop
#VERSION = 1.0pre4
#BASE_URL = https://pdw.ex-parrot.com/iftop/download

VERSION = 0.17
BASE_URL = https://pdw.ex-parrot.com/iftop/download/iftop-0.17.tar.gz

CFLAGS += -std=gnu17
PRE_CONFIGURE = LIBS=-ltinfo

#ifeq ($(mARCH), aarch64)
ReConfigure = yes
#endif

include ../Makefile.rules
