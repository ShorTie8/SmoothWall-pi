include ../Makefile.conf
include ../Makefile.versions

PACKAGE = basicrootfs
VERSION = 0.0

compile:
	$(MAKE) -C $(DIR)

install: compile
	mkdir -p $(PKG_ROOT)
	install -D $(DIR)/basicrootfs.bz2 $(PKG_ROOT)/usr/lib/installer/basicrootfs.bz2

all: install
	tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) .

clean:
	@echo -n " $(PACKAGE)"
	@$(MAKE) -C $(DIR) clean
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

download:
	@true
