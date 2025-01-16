# When a new kernel is installed, xtables-addons must also be installed so that
#   /lib/modules/X/extra/ is installed and available.

# Put kernel-drivers and linux-firmware at the end before coretree to ensure
#   that they override those files in linux when linux is updated.

UPDATE_PACKAGES = \
		  curl \
		  daq \
		  device-ids \
		  dhcpcd \
		  dnsmasq \
		  ipbatch \
		  ipset \
		  iptables \
		  kernel-drivers \
		  libmnl \
		  libnftnl \
		  libreswan \
		  linux \
		  miniupnpd \
		  ncurses \
		  nspr \
		  nss \
		  openssh \
		  ppp \
		  smoothd \
		  snort \
		  squidclamav \
		  suricata \
		  trafficstats \
		  usb-modeswitch \
		  xtables-addons \
		  linux-firmware \
		  coretree


UPDATE_ID = 012
UPDATE_NAME = Update12

KERNEL = yes

EXTRA_UPDATE_FILES = tzdata2024a.tar.gz
$(shell cp ../../../downloads/$(EXTRA_UPDATE_FILES) . 2>/dev/null)

include ../Makefile.update
