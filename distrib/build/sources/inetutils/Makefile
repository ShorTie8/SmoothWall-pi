# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = inetutils
#VERSION = 1.9.4
VERSION = 2.7
#ReConfigure = yes
BASE_URL = https://ftp.gnu.org/gnu/inetutils

CONFIG_OPTS += \
		--bindir=/usr/bin    \
		--localstatedir=/var \
		--disable-logger     \
		--disable-whois      \
		--disable-rcp        \
		--disable-rexec      \
		--disable-rlogin     \
		--disable-rsh        \
		--disable-servers

PATCH = yes
patch: $(DIR)/
	#cd $(DIR); sed -i 's@<sys/types.h>@<sys/types.h>\n#include <stdlib.h>@' \
	#    libicmp/icmp_timestamp.c
	##	First, make the package build with gcc-14.1 or later:
	cd $(DIR); sed -i 's/def HAVE_TERMCAP_TGETENT/ 1/' telnet/telnet.c
include ../Makefile.rules
