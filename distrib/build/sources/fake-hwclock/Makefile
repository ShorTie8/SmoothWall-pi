# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.


# https://git.einval.com/cgi-bin/gitweb.cgi?p=fake-hwclock.git

include ../Makefile.conf

PACKAGE = fake-hwclock
VERSION = 0.11
EXTENSION = .tar.gz
BASE_FHC = http://http.debian.net/debian/pool/main/f/fake-hwclock
TAR_FHC = fake-hwclock_$(VERSION).tar.gz


DOWNLOAD = yes
download:
	$(DL_CMD) $(BASE_FHC)/$(TAR_FHC)

INSTALL = yes
install: download
	tar xf $(DOWNLOADS_DIR)/$(PACKAGE)_$(VERSION).tar.gz

	mkdir -p $(PKG_ROOT)
	mkdir -vp $(PKG_ROOT)/{etc,sbin}
	install -m 0755 git/fake-hwclock $(PKG_ROOT)/sbin
	mkdir -vp $(PKG_ROOT)/etc/cron.hourly
	install -m 0755 git/debian/fake-hwclock.cron.hourly $(PKG_ROOT)/etc/cron.hourly/fake-hwclock
	echo "`date -u '+%Y-%m-%d %H:%M:%S'`" > $(PKG_ROOT)/etc/fake-hwclock.data
# EnvironmentFile=-/etc/default/fake-hwclock
	mkdir -vp $(PKG_ROOT)/etc/default
	install -m 0644 git/etc/default/fake-hwclock $(PKG_ROOT)/etc/default

# make -C installroot

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf git
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz


include ../Makefile.rules
