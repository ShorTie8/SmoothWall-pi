include ../Makefile.conf

PACKAGE = siproxd
#VERSION = 0.8.3
#BASE_URL = http://downloads.sourceforge.net/project/siproxd/$(PACKAGE)/$(VERSION)

#### or github
## you need full commitID for DIR to work
VERSION = 0.8.4.git
gitCommitID = 0bb5dd4aac9f5578db664d82f67091bc83c3780d
BASE_URL = https://github.com/hb9xar/siproxd/archive/$(gitCommitID)
DIR = $(PACKAGE)-$(gitCommitID)


PATCH_FILE1 = siproxd_pidfilechange.patch
PATCH_FILE2 = ltdl.patch

PREPARE = yes
$(DIR)/: download
	@echo; echo "PrePare"
	tar -xf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)
	cd $(DIR); ./autogen.sh

include ../Makefile.rules
