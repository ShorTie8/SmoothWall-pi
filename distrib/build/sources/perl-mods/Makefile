# Smoothwall Build System
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.
#
# Written by: Charlie Heselton
#
# Makefile for all needed perl modules
#

include ../Makefile.conf

PACKAGE = perl-mods
VERSION = 0.0

# List of all mods to be built. Add here, then add dir and makefile in
#   version dir below. IO-Socket-SSL seems to depend on Net-SSLeay; both
#   are moved to the end of the list.
export PERL_MODS = \
	    App-Control \
	    Authen-NTLM \
	    Authen-SASL \
	    Config-Patch \
	    Date-Calc \
	    FCGI \
	    CGI-Fast \
	    GD \
	    GDTextUtil \
	    GDGraph \
	    HTML-Parser \
	    HTML-Tagset \
	    Log-Log4perl \
	    Net-CIDR \
	    Net-Netmask \
	    Net-SMTPS \
	    Net-SMTP-SSL \
	    NetAddr-IP \
	    RRD-Simple \
	    Set-IntSpan \
	    URI \
	    libnet \
	    libwww-perl \
	    local-lib \
	    Net-SSLeay \
	    IO-Socket-SSL \
	    XML-Parser \
	    XML-Simple

DOWNLOAD = yes
download:
	@+$(MAKE) -C $(PACKAGE)-$(VERSION) download

COMPILE = yes
compile: download
	@+$(MAKE) $(JOBS) -C $(COMPILE_DIR)

INSTALL = yes
install: compile
	@true

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@+$(MAKE) --no-print-directory -C $(COMPILE_DIR) clean >/dev/null 2>&1
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
