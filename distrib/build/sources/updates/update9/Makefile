# When a new kernel is installed, xtables-addons must also be installed so that
#   /lib/modules/X/extra/ is installed and available.

# Put kernel-drivers and linux-firmware at the end before coretree to ensure
#   that they override those files in linux when linux is updated.

UPDATE_PACKAGES = \
		  apcupsd \
		  at \
		  bc \
		  binutils \
		  bison \
		  c_icap \
		  c_icap_modules \
		  cacert-bundle \
		  clamav \
		  cpio \
		  curl \
		  device-ids \
		  dhcpcd \
		  dnsmasq \
		  e2fsprogs \
		  eudev \
		  file \
		  findutils \
		  fping \
		  gawk \
		  glibc \
		  grep \
		  httpd \
		  ipbatch \
		  iproute2 \
		  ipset \
		  iptables \
		  isdn4k-utils \
		  kmod \
		  libevent \
		  libmnl \
		  libnetfilter_acct \
		  libnetfilter_conntrack \
		  libnetfilter_cthelper \
		  libnetfilter_cttimeout \
		  libnetfilter_log \
		  libnetfilter_queue \
		  libnfnetlink \
		  libnftnl \
		  libnl \
		  libosip2 \
		  libreswan \
		  libsmooth+setup \
		  linux \
		  listtables \
		  lm_sensors \
		  nspr \
		  nss \
		  openssh \
		  openssl \
		  patch \
		  pcmciautils \
		  perl-mods \
		  procps-ng \
		  siproxd \
		  smoothd \
		  snort \
		  squid \
		  squidclamav \
		  strace \
		  suricata \
		  sysklogd \
		  trafficstats \
		  unbound \
		  util-linux \
		  wget \
		  wireless_tools \
		  wpa_supplicant \
		  xtables-addons \
		  xz \
		  kernel-drivers \
		  linux-firmware \
		  coretree


UPDATE_ID = 009
UPDATE_NAME = Update9

CLAMAV = yes
KERNEL = yes
EXTRA_UPDATE_FILES = tzdata2018c.tar.gz
$(shell cp ../../../downloads/$(EXTRA_UPDATE_FILES) . 2>/dev/null)

include ../Makefile.update
