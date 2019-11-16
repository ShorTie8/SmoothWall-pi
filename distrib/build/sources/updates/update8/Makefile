# Non-obvious dependency notes:
#   iproute TC libs depend on libxtables (iptables)
#   c_icap_modules libclamav_mod depends on libclamav (clamav)
# Such dependent pkgs *MUST* be updated when the upper pkg is updated
# Script .../updates/checklibs should find missing libs on updated test smoothies

UPDATE_PACKAGES = \
		  linux \
		  iptables \
		  ipset \
		  xtables-addons \
		  iproute2 \
		  c_icap_modules \
		  c_icap \
		  openswan \
		  ipbatch \
		  listtables \
		  trafficstats \
		  linux-firmware \
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
		  libsmooth+setup \
		  nspr \
		  nss \
		  openssl \
		  unbound \
		  apcupsd \
		  bc \
		  cacert-bundle \
		  dhcpcd \
		  e2fsprogs \
		  eudev \
		  file \
		  findutils \
		  fping \
		  gawk \
		  grep \
		  isdn4k-utils \
		  openssh \
		  pcmciautils \
		  qemu \
		  smoothd \
		  snort \
		  squid \
		  squidclamav \
		  strace \
		  suricata \
		  sysklogd \
		  util-linux \
		  xz \
		  coretree


UPDATE_ID = 008
UPDATE_NAME = Update8

CLAMAV = yes
KERNEL = yes

EXTRA_UPDATE_FILES = remove-old-files

include ../Makefile.update
