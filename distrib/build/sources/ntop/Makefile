# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ntop
VERSION = 5.0.1

BASE_URL = http://iweb.dl.sourceforge.net/project/ntop/$(PACKAGE)/Stable/

CONFIG_OPTS += --prefix=/usr --with-ssl --with-ossl-root=/usr --with-ossl-lib=/usr/lib --with-ossl-include=/usr/include

CONFIGURE = yes

configure: $(DIR)/
	@echo; echo "configure"
	cd $(DIR); patch -p1 < ../configure.in.patch
ifeq ($(mARCH), arm64)
	for i in $$(find $(DIR) -name config.guess -o -name config.sub); do \
		cp -vf ../glibc/glibc-*/scripts/$$(basename $${i}) $${i}; \
	done
endif

	@( \
	  cd $(DIR); \
	  sed -i -e 's/svn co/svn --non-interactive --trust-server-cert co/' autogen.sh; \
	  sed -i -e 's=https://svn.ntop.org=https://ntop.org=' autogen.sh; \
	  ./autogen.sh; \
	  autoreconf -f -i; \
	  ./configure $(CONFIG_OPTS); \
	)
	  #./autogen.sh --noconfig; \

include ../Makefile.rules

# This goes before the first 'sed' line above 
# Stopped working after the release of 5.0.1
#sed -i -e 's/svn co/svn --non-interactive --trust-server-cert co/' autogen.sh; \
