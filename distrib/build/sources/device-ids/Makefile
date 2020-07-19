# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

# This should always download the latest versions.

# This is also a quick hack. There's gotta be a better way to do this.

include ../Makefile.conf

PACKAGE = device-ids
VERSION = 0.0

PCI_URL = http://pci-ids.ucw.cz/v2.2/
PCI_FILE = pci.ids.bz2
USB_URL = http://www.linux-usb.org/
USB_FILE = usb.ids.bz2
OUI_URL = http://standards-oui.ieee.org/oui/
OUI_FILE = oui.txt

# Force fetching from upstream origin every time.
export MIRROR_UNO =
export MIRROR_DOS =

DOWNLOAD = yes

# For a download every time.
download:
	@rm -f ../../downloads/oui.txt* ../../downloads/pci.ids* ../../downloads/usb.ids*
	@$(DL_CMD) $(PCI_URL)$(PCI_FILE)
	@$(DL_CMD) $(USB_URL)$(USB_FILE)
	@$(DL_CMD) $(OUI_URL)$(OUI_FILE)


PREPARE = yes
$(DIR)/: download
	mkdir $(DIR) && \
	  cd $(DIR) && \
	  bunzip2 < ../../../downloads/$(PCI_FILE) > pci.ids && \
	  bunzip2 < ../../../downloads/$(USB_FILE) > usb.ids && \
	  ../../../toolcrib/filter-oui -v

INSTALL = yes
install: $(DIR)/
	mkdir -p $(PKG_ROOT)/usr/share $(PKG_ROOT)/usr/lib/smoothwall
	cd $(DIR) &&  \
	  cp *.ids oui.txt $(PKG_ROOT)/usr/share && \
	  cp oui_vendor.pm $(PKG_ROOT)/usr/lib/smoothwall

include ../Makefile.rules
