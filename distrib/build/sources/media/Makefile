# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions
include ../Makefile

PACKAGE = media
VERSION = N/A

TAR_OPTIONS = 

# Two dirs down, one cross each.
ifeq ($(BUILD_OUT), crumbs/build-progress.out)
  MEDIA_BUILD_OUT := ../../$(BUILD_OUT)
else
  MEDIA_BUILD_OUT := $(BUILD_OUT)
endif

# Make it easy to switch between the two
export UDEV = eudev
export UDEVunused = udev

# Document these pkgs, don't install.
# Some of these are retirees.
TOOLCHAIN_PKGS = expect
OTHER_PKGS = updates jam $(UDEVunused) udev-config cnxadsl \
	     libart_lgpl procps procinfo dev86 openswan

TARGET_DIR = /build/target

ADV_PKGS = gdbm GeoIP Python libmnl openldap gperf attr \
	   subversion ntop iperf
KVM_PKGS = samba

INST_PKGS = glibc libsmooth+setup libgcc freetype libpng libdnet \
	    daq libnet libnetfilter_queue libnfnetlink attr libcap-ng LuaJIT \
	    libnetfilter_acct libnetfilter_conntrack libnetfilter_cthelper \
	    libnetfilter_cttimeout libnetfilter_log libnftnl libnl \
	    libcap fontconfig glib cairo libffi readline libpcap sqlite-autoconf \
	    libosip2 pango zlib slang pixman libxml2 libusb-compat libusb \
	    libevent nspr nss unbound c_icap c_icap_modules curl \
	    kmod gmp mpfr mpc popt yaml perl-mods rsync \
	    newt binutils coreutils iana-etc mktemp file findutils gawk \
	    ncurses vim less sed flex gettext inetutils iputils \
	    whois perl bash bc bzip2 kbd e2fsprogs grep gzip module-init-tools \
	    procinfo-ng procps-ng psmisc shadow sysklogd logrotate sysvinit tar \
	    util-linux joe wget iptables ipset ipbatch pciutils usbutils \
	    linux openssl openssh httpd smoothd squid squidclamav freefont \
	    strace rrdtool cron tcpdump dnsmasq ntp openntpd hdparm hddtemp \
	    iproute2 gd expat ethtool listtables inotify-tools \
	    beep2 pcre trafficstats iftop setuids ppp isdn4k-utils rp-pppoe \
	    ibod dhcpcd eciadsl-synch_bin eciadsl-usermode dhcp snort \
	    oinkmaster libreswan wireless_tools wpa_supplicant imspector diffutils clamav \
	    p3scan siproxd which miniupnpd ez-ipupdate noip cdrtools \
	    suricata smartmontools at dosfstools grub linux-atm \
	    mtools nano reiserfsprogs parted xtables-addons cpio dialog \
	    $(UDEV) lm_sensors xz pcmciautils qemu sysfsutils db squidGuard \
	    apcupsd cacert-bundle setkerneltz fping \
	    kernel-drivers \
	    coretree $(ADV_PKGS) device-ids

# Leave kernel-drivers out for now.
#	    kernel-drivers \

# INST_PKGS notes.
# cacert-bundle should be installed after openssl.
# kernel-drivers *MUST* be installed after linux. Its drivers replace their
#   counterparts in linux.
# linux-backports *may* override drivers in kernel-drivers; keep an eye pealed.
# 'coretree' *MUST* be third-last.
# If the 'advanced' mechanism is added, ADV_PKGS must be second-last; they'll
#   override what's in coretree.
# 'device-ids' *MUST* be last in order to overwrite any existing version of usb.ids
#   and pci.ids in usr/share.

DEV_PKGS = kernel-headers patch make autoconf automake bison dejagnu gcc \
	   gdb tcl m4 neon git screen lynx groff man man-pages \
	   klibc pkg-config sudo texinfo busybox \
	   libtool nasm acpica zip

NOT_DRIVERS = #drivers/video

cdrom:
	mkdir cdrom
	echo "      runtimeroot" >>$(MEDIA_BUILD_OUT)
	make -C runtimeroot KERNEL_TYPE=$(KERNEL_TYPE) 
	echo "      installroot" >>$(MEDIA_BUILD_OUT)
	make -C installroot KERNEL_TYPE=$(KERNEL_TYPE) 
	echo "      cdromboot" >>$(MEDIA_BUILD_OUT)
	make -C cdromboot KERNEL_TYPE=$(KERNEL_TYPE) 

cdrom/smoothwall.tgz:
	echo "      prepare cdrom tree" >>$(MEDIA_BUILD_OUT)
	mkdir -p distrib distrib/sys distrib-dev distrib-doc/usr/share/

ifeq ($(BITS_64), yes)
	cd distrib; [ -e lib64 ] || ln -s lib lib64
	cd distrib-dev; [ -e lib64 ] || ln -s lib lib64
	mkdir -p distrib/usr; cd distrib/usr; [ -e lib64 ] || ln -s lib lib64
	mkdir -p distrib-dev/usr; cd distrib-dev/usr; [ -e lib64 ] || ln -s lib lib64
endif
	
	install -D runtimerootimage.gz distrib/boot/initrd-$(K_SWE_VERSION).gz
	
	echo "        unpack dev packages" >>$(MEDIA_BUILD_OUT)
	echo "Unpacking dev packages:"
	(for I in $(DEV_PKGS); do \
	    if [ ! -e $(TARGET_DIR)/smoothwall-$$I.tar.gz ]; then \
	      make -C ../$$I clean all; retCode=$$?; \
	      if [ $$retCode -ne 0 ]; then \
	        echo "$$I FAILED"; \
	        exit $$retCode; \
	      fi; \
	    fi; \
	    echo -n "    $$I"; \
	    TAR_OPTIONS= tar -zxf $(TARGET_DIR)/smoothwall-$$I.tar.gz -C distrib-dev || (echo; exit 69); \
	    echo; \
	  done; \
	);
	
	@echo "        copy dev shared libs to distrib" >>$(MEDIA_BUILD_OUT)
	@echo "Copying dev shared libs to distrib:"
	(cd distrib-dev; \
	  find . -name \*.so\* -print | cpio -pd ../distrib \
	)
	
	@echo "        unpack main packages" >>$(MEDIA_BUILD_OUT)
	@echo "Unpacking main packages:"
	(for I in $(INST_PKGS); do \
	    if [ ! -e $(TARGET_DIR)/smoothwall-$$I.tar.gz ]; then \
	      make -C ../$$I clean all; retCode=$$?; \
	      if [ $$retCode -ne 0 ]; then \
	        echo "$$I FAILED"; \
	        exit $$retCode; \
	      fi; \
	    fi; \
	    echo -n "    $$I"; \
	    TAR_OPTIONS= tar xf $(TARGET_DIR)/smoothwall-$$I.tar.gz -C distrib || (echo; exit 68); \
	    echo; \
	  done; \
	);
# Move usr/include/python2.7 *back*!
	@echo "        move includes to distrib-dev" >>$(MEDIA_BUILD_OUT)
	@echo "Moving includes to distrib-dev:"
	if [ -d distrib/usr/include ]; then \
	  mkdir -p distrib-dev/usr/include; \
	  cp -a distrib/usr/include distrib-dev/usr/; \
	  rm -rf distrib/usr/include/*; \
	  mv distrib-dev/usr/include/python2.7 distrib/usr/include; fi
	
	@echo "        move static libs to distrib-dev" >>$(MEDIA_BUILD_OUT)
	@echo "Moving static libs to distrib-dev:"
	cd distrib; find . -name \*.a -o -name \*.la | while read a; do \
	  mkdir -p ../distrib-dev/`dirname $$a`; \
	  mv $$a ../distrib-dev/$$a; \
	done
	
	@echo "        move docs to distrib-doc" >>$(MEDIA_BUILD_OUT)
	@echo "Moving docs to distrib-doc:"
	for I in man info share/man share/info share/doc share/gtk-doc \
	      share/ntop/html share/slsh/help examples; do \
	  if [ -d distrib/usr/$$I ]; then \
	    mkdir -p distrib-doc/usr/$$I; \
	    mv distrib/usr/$$I/* distrib-doc/usr/$$I/; fi; \
	done
	
	@echo "        delete FB devices" >>$(MEDIA_BUILD_OUT)
	@for i in distrib/lib/modules/*; do \
	    (cd $$i/kernel; rm -rf $(NOT_DRIVERS)); \
	  done
	@echo "        strip symbols" >>$(MEDIA_BUILD_OUT)
	/build/toolcrib/striptree distrib
	/build/toolcrib/striptree distrib-dev
	/build/toolcrib/striptree distrib-doc
	
	@echo -e "\nProduct info:"
	@( \
	echo "  PRODUCT='$(PRODUCT_NAME)'"; \
	echo "  VERSION='$(PRODUCT_VERSION)'"; \
	echo "  EXTRA='$(PRODUCT_EXTRA)'"; \
	echo "  REVISION='$(REVISION)'"; \
	echo "  UI_VERSION='$(UI_VERSION)'"; \
	echo "  ARCH='$(mTUPLE)'"; \
	) | sed -u -e 's/^/  /'
	
	@mkdir -p distrib/var/smoothwall/main
	@( \
	  echo "PRODUCT='$(PRODUCT_NAME)'" ; \
	  echo "VERSION='$(PRODUCT_VERSION)'" ; \
	  echo "EXTRA='$(PRODUCT_EXTRA)'"; \
	  echo "REVISION='$(REVISION)'" ; \
	  echo "UI_VERSION='$(UI_VERSION)'" ; \
	  echo "ARCH='$(mTUPLE)'" ; \
	) > distrib/var/smoothwall/main/productdata
	
	@chown nobody:nobody distrib/var/smoothwall/main/productdata
	
	@echo "        secure tree ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nSecuring tree ..."
	@( \
	  mkdir -p distrib/tmp; \
	  /build/toolcrib/securetree distrib; \
	  /build/toolcrib/securetree distrib-dev; \
	  /build/toolcrib/securetree distrib-doc; \
	  chmod u+s distrib/usr/bin/ping{,6}; \
	  chmod u+s distrib/usr/bin/traceroute; \
	  chmod u+s distrib/usr/sbin/listtables; \
	  chown root:nobody distrib/usr/bin/setuids/*; \
	  chmod 4750 distrib/usr/bin/setuids/*; \
	  chmod 1777 distrib/tmp; \
	) | sed -u -e 's/^/  /'
	
	@echo "        convert to shadow passwords ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nConverting to shadow passwords ..."
	@( \
	/usr/bin/chroot distrib /usr/sbin/pwconv; \
	/usr/bin/chroot distrib /usr/sbin/grpconv; \
	) | sed -u -e 's/^/  /'
	
	@echo "        update library cache ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nUpdating library cache ..."
	@( \
	/sbin/ldconfig -r distrib; \
	) | sed -u -e 's/^/  /'
	
	@echo "        tidy ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nTidying ..."
	@#rm -f distrib/etc/resolv.conf
	@find distrib -name .gitignore -exec rm -f {} \;
	@rm -f distrib/etc/ipsec.conf distrib/etc/ipsec.secrets
	@ln -s /var/smoothwall/vpn/ipsec.conf distrib/etc/ipsec.conf
	@ln -s /var/smoothwall/vpn/ipsec.secrets distrib/etc/ipsec.secrets
	@ln -sf /usr/bin/hostname distrib/bin/hostname
	@cd distrib; chown -R root:root usr/share/ntop usr/etc/ntop
	@cd distrib/etc; mkdir -p apcupsd/scripts && chown root:root apcupsd/scripts && chmod 755 apcupsd/scripts
	@cd distrib/etc; chmod 644 logrotate.{base,conf,d/*}
	@cd distrib-doc; chown -R root:root .
	@cd distrib/bin; ln -s /usr/bin/gzip gzip
	
	@echo "      copy to Dev ..." >>$(MEDIA_BUILD_OUT)
	@mkdir cdrom-dev
	@cd cdrom; cp -aR . ../cdrom-dev/
	
	@echo "      copy to OffRoad ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nCopying to OffRoad ..."
	@mkdir -p offroad
	@cd cdrom; cp -av . ../offroad
	@for i in main other; do sed -i \
	     -e '/Install Smoothwall/,+4d' \
	     -e '/Convert ISO/,+9d' \
	     -e '$d' \
	     offroad/boot/grub/$${i}.conf; done
	
	@echo "      build final tarballs ..." >>$(MEDIA_BUILD_OUT)
	@echo "        main ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nBuilding smoothwall.tgz, stand by ..."
	@tar -zcf cdrom/smoothwall.tgz -C distrib .
	@echo -n `tar tvf cdrom/smoothwall.tgz |wc -l` > cdrom/smoothwall.tgz.filecount
	@cp -a cdrom/smoothwall.tgz* cdrom-dev/
	
	@echo "        dev ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nBuilding smoothdev.tgz, stand by ..."
	@tar -zcf cdrom-dev/smoothdev.tgz -C distrib-dev .
	
	@echo "        doc ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nBuilding smoothdoc.tgz, stand by ..."
	@tar -zcf cdrom-dev/smoothdoc.tgz -C distrib-doc .
	
	@( \
	  src_tgz=../../../../smoothsrc.tar.gz; \
	  if [ -e "$src_tgz" ]; then \
	    echo -e "\nCopying smoothsrc.tgz, stand by ..."; \
	    cp $src_tgz  cdrom-dev/smoothsrc.tgz; \
	  fi \
	)

extracontent: cdrom
	cp -avR extracontent/* cdrom
	(for I in README.txt README.html; do \
		cat templates/$$I | \
			sed "s@\%PRODUCT_NAME\%@$(PRODUCT_NAME)@g" | \
			sed "s@\%BASENAME\%@$(BASENAME)@g" \
		> cdrom/$$I; \
	done);
	find cdrom -name .git -exec rm -rf {} \;

all: cdrom cdrom/smoothwall.tgz extracontent
	@echo "      assemble full ISO ..." >>$(MEDIA_BUILD_OUT)
	@( \
	  RELEASE="$(BASENAME)$(PRODUCT_EXTRA)-$(mTUPLE)"; \
	  ISONAME=$(TARGET_DIR)/isos/$${RELEASE}.iso; \
	  /sbin/mkisofs -o $${ISONAME} \
	    -b boot/grub/stage2_eltorito -J -R \
	    -no-emul-boot -boot-load-size 4 -boot-info-table \
	    -V $(BASENAME) --publisher "Smoothwall Express" cdrom; \
	  echo -e "$${ISONAME} assembly complete\n\n"; \
	)
	@echo "      assemble dev ISO ..." >>$(MEDIA_BUILD_OUT)
	@( \
	  RELEASE="$(BASENAME)$(PRODUCT_EXTRA)-$(mTUPLE)"; \
	  ISONAME=$(TARGET_DIR)/isos/$${RELEASE}-dev.iso; \
	  /sbin/mkisofs -o $${ISONAME} \
	    -b boot/grub/stage2_eltorito -J -R \
	    -no-emul-boot -boot-load-size 4 -boot-info-table \
	    -V $(BASENAME) --publisher "Smoothwall Express (Dev.)" cdrom-dev; \
	  echo -e "$${ISONAME} assembly complete\n\n"; \
	)
	@echo "      assemble offRoad ISO ..." >>$(MEDIA_BUILD_OUT)
	@( \
	  RELEASE="$(BASENAME)$(PRODUCT_EXTRA)-$(mTUPLE)"; \
	  ISONAME=$(TARGET_DIR)/isos/$${RELEASE}-offroad.iso; \
	  /sbin/mkisofs -o $${ISONAME} \
	    -b boot/grub/stage2_eltorito -J -R \
	    -no-emul-boot -boot-load-size 4 -boot-info-table \
	    -V $(BASENAME) --publisher "Smoothwall Express (OffRoad)" offroad; \
	  echo -e "$${ISONAME} assembly complete\n\n"; \
	)

clean:
	@echo -n " $(PACKAGE)"
	@rm -f Media.mediaISO.built
	@rm -f *.img
	@rm -rf cdrom cdrom-dev offroad distrib distrib-dev distrib-doc klibc temp
	@make --no-print-directory -C cdromboot clean >/dev/null 2>&1
	@make --no-print-directory -C installroot clean >/dev/null 2>&1
	@make --no-print-directory -C runtimeroot clean >/dev/null 2>&1
	
download:
	@true
