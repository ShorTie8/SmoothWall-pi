# When a new kernel is installed, xtables-addons must also be installed so that
#   /lib/modules/X/extra/ is installed and available.

# Put kernel-drivers and linux-firmware at the end before coretree to ensure
#   that they override those files in linux when linux is updated.

UPDATE_PACKAGES = \
		  LuaJIT \
		  c_icap \
		  c_icap_modules \
		  clamav \
		  cron \
		  device-ids \
		  ipbatch \
		  iproute2 \
		  ipset \
		  iptables \
		  libreswan \
		  libusb \
		  libusb-compat \
		  linux \
		  listtables \
		  miniupnpd \
		  neon \
		  openssh \
		  openssl \
		  ppp \
		  smoothd \
		  snort \
		  squid \
		  squidclamav \
		  suricata \
		  unbound \
		  xtables-addons \
		  kernel-drivers \
		  linux-firmware \
		  coretree


UPDATE_ID = 010
UPDATE_NAME = Update10

CLAMAV = yes
KERNEL = yes
EXTRA_UPDATE_FILES = tzdata2018g.tar.gz
$(shell cp ../../../downloads/$(EXTRA_UPDATE_FILES) . 2>/dev/null)

include ../Makefile.update
