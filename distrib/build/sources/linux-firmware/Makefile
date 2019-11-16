# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = linux-firmware
VERSION = 20181026

EXTENSION = .tar.gz

export pkgName = $(PACKAGE)
export gitURL = git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
export gitCommitID = 1baa34868b2c
export gitBranch = $(VERSION)

PREPARE = yes
$(DIR)/:
	true

COMPILE = yes
compile:
	true

INSTALL = yes
install: download
	rm -rf $(PKG_ROOT)
	mkdir -p $(PKG_ROOT)/lib/firmware
	tar xvf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	../../toolcrib/findfirmware | sort | uniq > needed-firmware.list
	set -x; cd $(PACKAGE)-$(VERSION); cat ../needed-firmware.list | while read fw; do \
	  if [ -f "$$fw" ]; then \
	    echo "$$fw" >> ../found-firmware.list; \
	  else \
	    echo "$$fw" >> ../notfound.list; \
	  fi; \
	done
	sort found-firmware.list | uniq > firmware.list
	tar cf culled.tar -C $(PACKAGE)-$(VERSION) -T firmware.list
	tar xvf culled.tar -C $(PKG_ROOT)/lib/firmware
	chown -R root:root $(PKG_ROOT)/lib/firmware
	find $(PKG_ROOT)/lib/firmware -type f -exec chmod 444 {} \;
	find $(PKG_ROOT)/lib/firmware -type d -exec chmod 555 {} \;

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(PACKAGE)-$(VERSION) {needed-,found-,}firmware.list culled.tar notfound.list
	@rm -rf $(PKG_ROOT)

include ../Makefile.rules
