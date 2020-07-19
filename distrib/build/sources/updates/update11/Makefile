# When a new kernel is installed, xtables-addons must also be installed so that
#   /lib/modules/X/extra/ is installed and available.

# Put kernel-drivers and linux-firmware at the end before coretree to ensure
#   that they override those files in linux when linux is updated.

UPDATE_PACKAGES = \
		  bc \
		  bison \
		  cacert-bundle \
		  c_icap_modules \
		  clamav \
		  curl \
		  daq \
		  device-ids \
		  dhcpcd \
		  gmp \
		  grub \
		  inetutils \
		  iproute2 \
		  libreswan \
		  linux \
		  miniupnpd \
		  ntp \
		  openssh \
		  openssl \
		  smoothd \
		  snort \
		  sqlite-autoconf \
		  squid \
		  suricata \
		  unbound \
		  util-linux \
		  xtables-addons \
		  kernel-drivers \
		  linux-firmware \
		  coretree


UPDATE_ID = 011
UPDATE_NAME = Update11

CLAMAV = yes
KERNEL = yes
EXTRA_UPDATE_FILES = tzdata2019c.tar.gz
$(shell cp ../../../downloads/$(EXTRA_UPDATE_FILES) . 2>/dev/null)

include ../Makefile.update
