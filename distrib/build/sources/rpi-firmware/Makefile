# SmoothWall Build system.
#
# (c) ShorTie 2016
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = rpi-firmware
#VERSION = a154f2136850dba827cf4bc40794854376902cbd
#VERSION = 08262019
#GIT_COMMIT = 7163480fff007dc98978899b556dcf06f8a462c8

#VERSION = 10282019
#GIT_COMMIT = 4ee44af381d55bc2221cf80c1433842a48ed09e1

VERSION = 11062019
GIT_COMMIT = 00daf85ffa373ecce7836df7543c6ebe4cf43639

FILES = LICENCE.broadcom bootcode.bin \
		fixup.dat fixup4.dat start.elf start4.elf

DOWNLOAD = yes
download:
	@echo; echo; echo "download"; echo; echo -n "rpi-firmware $(VERSION) "
	@if [ -a $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz.done ]; then \
		echo "got it already"; \
	else \
		echo; echo; echo "Creating $(PACKAGE)-$(VERSION).tar.gz"; echo; \
		(mkdir -vp $(DIR)/lib/firmware/brcm; \
		echo; echo; echo "downloading"; echo; \
		(cd $(DIR)/lib/firmware/brcm; \
			wget  https://github.com/RPi-Distro/firmware-nonfree/raw/master/brcm/brcmfmac43430-sdio.bin; \
			wget  https://raw.githubusercontent.com/RPi-Distro/firmware-nonfree/master/brcm/brcmfmac43430-sdio.txt; \
			wget  https://github.com/RPi-Distro/firmware-nonfree/raw/master/brcm/brcmfmac43455-sdio.bin; \
			wget  https://github.com/RPi-Distro/firmware-nonfree/raw/master/brcm/brcmfmac43455-sdio.clm_blob; \
			wget  https://raw.githubusercontent.com/RPi-Distro/firmware-nonfree/master/brcm/brcmfmac43455-sdio.txt)); \
		echo; echo; echo "boot"; echo; \
		(mkdir -vp $(DIR)/boot; \
		(cd $(DIR)/boot; \
			for FILE in $(FILES); do \
				wget https://raw.githubusercontent.com/RPi-Distro/firmware/debian/boot/$$FILE --no-check-certificate; \
			done;)); \
		echo; echo; echo "config.txt -n- cmdline.txt"; echo; \
		(cd $(DIR)/boot; \
			wget https://raw.githubusercontent.com/RPi-Distro/pi-gen/9cffa42a3514cd2a4d0aa648a6e52860ae86e1b5/stage1/00-boot-files/files/config.txt; \
			wget https://raw.githubusercontent.com/RPi-Distro/pi-gen/9cffa42a3514cd2a4d0aa648a6e52860ae86e1b5/stage1/00-boot-files/files/cmdline.txt; \
			sed -e 's@ROOTDEV@/dev/mmcblk0p4@' cmdline.txt); \
		tar -zcvf $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz $(DIR); \
		touch $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz.done; \
	fi

	@echo; echo -n "rpi-eeprom download "
	@if [ ! -f $(DOWNLOADS_DIR)/rpi-eeprom-master.tar.gz ]; then \
		echo "downloading"; echo; \
		wget -c -N https://github.com/raspberrypi/rpi-eeprom/archive/master.tar.gz -O $(DOWNLOADS_DIR)/rpi-eeprom-master.tar.gz ; \
		touch $(DOWNLOADS_DIR)/rpi-eeprom-master.tar.gz.done; \
	else \
		echo "got it already"; echo; \
	fi


INSTALL = yes
install: download
	@echo; echo; echo "install"; echo
	tar -xf $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz

	@echo; mkdir -vp $(PKG_ROOT)/{boot,lib/firmware/brcm}; echo
	install -m 0644 $(DIR)/boot/LICENCE.broadcom $(PKG_ROOT)/boot/LICENCE.broadcom
ifeq ($(mTUPLE),$(filter $(mTUPLE),pi0w rpi2 rpi3 pi3-64))
	install -m 0644 $(DIR)/boot/bootcode.bin $(PKG_ROOT)/boot/bootcode.bin
	install -m 0644 $(DIR)/boot/fixup.dat    $(PKG_ROOT)/boot/fixup.dat
	install -m 0644 $(DIR)/boot/start.elf    $(PKG_ROOT)/boot/start.elf
	install -m 0644 $(DIR)/lib/firmware/brcm/brcmfmac43430-sdio.bin $(PKG_ROOT)/lib/firmware/brcm/brcmfmac43430-sdio.bin
	install -m 0644 $(DIR)/lib/firmware/brcm/brcmfmac43430-sdio.txt $(PKG_ROOT)/lib/firmware/brcm/brcmfmac43430-sdio.txt
else ifeq ($(mTUPLE),$(filter $(mTUPLE),rpi4 pi4-64))
	install -m 0644 $(DIR)/boot/fixup4.dat   $(PKG_ROOT)/boot/fixup4.dat
	install -m 0644 $(DIR)/boot/start4.elf   $(PKG_ROOT)/boot/start4.elf
	install -m 0644 $(DIR)/lib/firmware/brcm/brcmfmac43455-sdio.bin $(PKG_ROOT)/lib/firmware/brcm/brcmfmac43455-sdio.bin
	install -m 0644 $(DIR)/lib/firmware/brcm/brcmfmac43455-sdio.clm_blob $(PKG_ROOT)/lib/firmware/brcm/brcmfmac43455-sdio.clm_blob
	install -m 0644 $(DIR)/lib/firmware/brcm/brcmfmac43455-sdio.txt $(PKG_ROOT)/lib/firmware/brcm/brcmfmac43455-sdio.txt
	@echo; echo; echo "rpi-eeprom install"; echo
	mkdir -vp $(PKG_ROOT)/usr/sbin/rpi-eeprom; echo
	cd $(DIR); tar -xf $(DOWNLOADS_DIR)/rpi-eeprom-master.tar.gz
	cp -vR $(DIR)/rpi-eeprom-master/* $(PKG_ROOT)/usr/sbin/rpi-eeprom
else
	$(info Unsupported pi)
	$(error FAIL)
endif

	@echo; echo; echo "cmdline && config's"; echo
	install -m 0644 cmdline.txt.install $(PKG_ROOT)/boot/cmdline.txt.install
	install -m 0644 config.txt.install $(PKG_ROOT)/boot/config.txt.install
	sed -i $(PKG_ROOT)/boot/config.txt.install -e "s/UNAME/$(KERNEL_VER)/"

	@echo
	install -m 0644 cmdline.txt.normal $(PKG_ROOT)/boot/cmdline.txt.normal
	install -m 0644 config.txt.normal $(PKG_ROOT)/boot/config.txt.normal
	sed -i $(PKG_ROOT)/boot/config.txt.normal -e "s/UNAME/$(KERNEL_VER)/"

	@echo
	install -m 0644 $(DIR)/boot/cmdline.txt $(PKG_ROOT)/boot/cmdline.txt.foundation
	install -m 0644 $(DIR)/boot/config.txt $(PKG_ROOT)/boot/config.txt.foundation

ifeq ($(mTUPLE),$(filter $(mTUPLE),pi3-64 pi4-64))
	echo "arm_64bit=1" >> $(PKG_ROOT)/boot/config.txt.install
	echo "arm_64bit=1" >> $(PKG_ROOT)/boot/config.txt.normal
	echo "arm_64bit=1" >> $(PKG_ROOT)/boot/config.txt.foundation
endif

ifeq ($(mTUPLE),$(filter $(mTUPLE),rpi3 pi3-64 rpi4 pi4-64))
	echo "dtparam=random=on" >> $(PKG_ROOT)/boot/config.txt.install
	echo "dtparam=random=on" >> $(PKG_ROOT)/boot/config.txt.normal
endif

include ../Makefile.rules
