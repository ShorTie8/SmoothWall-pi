# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
# (c) ShorTie 2016
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions
include ../Makefile

PACKAGE = media-sdcard
VERSION = N/A

TAR_OPTIONS = 
RELEASE = $(BASENAME)$(PRODUCT_EXTRA)-$(mTUPLE)
ZIPNAME = $(TARGET_DIR)/isos/$(RELEASE).zip
DEVZIPNAME = $(TARGET_DIR)/isos/$(RELEASE)-dev.zip

# Two dirs down, one cross each.
ifeq ($(BUILD_OUT), crumbs/build-progress.out)
  export MEDIA_BUILD_OUT := ../../$(BUILD_OUT)
else
  export MEDIA_BUILD_OUT := $(BUILD_OUT)
endif

# Document these pkgs, don't install.
# Some of these are retirees.
TOOLCHAIN_PKGS = expect

# eudev is used now
OTHER_PKGS = updates jam udev udev-config cnxadsl \
	     libart_lgpl procps procinfo dev86 openswan eciadsl-synch_bin eciadsl-usermode

TARGET_DIR = /build/target

ADV_PKGS = gdbm GeoIP Python libmnl openldap gperf attr \
	   subversion ntop iperf
KVM_PKGS = samba

# use this to include mTUPLE specifics
ifeq ($(mTUPLE),$(filter $(mTUPLE),i586 i686 x86_64))
  export GRUB = grub
  #export GRUB = grub2 kernel-drivers cdrtools libelf
else ifeq ($(mTUPLE),$(filter $(mTUPLE),pi0w rpi2 rpi3 pi3-64 rpi4 pi4-64))
  export GRUB = fake-hwclock rpi-firmware i2c-tools rng-tools
  RPI_PKGS = rpi-userland
  #ADV_PKGS +=
else ifeq ($(mTUPLE),ODROID-XU3)
  export GRUB = u-boot
endif

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
	    ibod dhcpcd dhcp snort \
	    oinkmaster libreswan wireless_tools wpa_supplicant imspector diffutils clamav \
	    p3scan siproxd which miniupnpd ez-ipupdate noip \
	    smartmontools at dosfstools linux-atm \
	    mtools nano reiserfsprogs parted xtables-addons cpio dialog \
	    eudev lm_sensors xz pcmciautils qemu sysfsutils db squidGuard \
	    apcupsd cacert-bundle setkerneltz fping \
	    kernel-drivers \
	    linux-firmware acl libelf bridge-utils $(RPI_PKGS) \
	    iw libgcrypt libgpg-error crda hostapd M2Crypto wireless-regdb \
	    coretree $(GRUB) $(ADV_PKGS) device-ids FFC

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
	   pkg-config sudo texinfo busybox \
	   libtool nasm acpica zip

NOT_DRIVERS = drivers/video

cdrom:
	@echo -e "\n\ncdrom"
#	exit 42
	mkdir cdrom
	echo "      installroot" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\ninstallroot"
	make -C installroot KERNEL_TYPE=$(KERNEL_TYPE) 
	install -D installrootimage.gz cdrom-dev1/installrootimage.gz
#	exit 42

	echo "      runtimeroot" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nruntimeroot" 
	make -C runtimeroot KERNEL_TYPE=$(KERNEL_TYPE)
#	install -D runtimerootimage.gz cdrom-dev/initrd-$(K_SWE_VERSION).gz
#	exit 42
	@echo; echo

ifeq ($(mTUPLE),$(mARCH))
	echo "      cdromboot" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\ncdromboot"
	make -C cdromboot KERNEL_TYPE=$(KERNEL_TYPE)
	mkdir -vp distrib/boot/grub
	cp -v cdromboot/backdrop.xpm.gz distrib/boot/grub
	cp -v cdromboot/express_boot_protect.xpm.gz distrib/boot/grub
endif

cdrom/smoothwall.tgz:
	echo "      prepare tree" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nprepare tree"
	mkdir -vp distrib distrib/sys distrib-dev distrib-doc/usr/share/

ifeq ($(BITS_64), yes)
	@echo -e "\n\nBITS_64"
	cd distrib; [ -e lib64 ] || ln -s lib lib64
	cd distrib-dev; [ -e lib64 ] || ln -s lib lib64
	mkdir -p distrib/usr; cd distrib/usr; [ -e lib64 ] || ln -s lib lib64
	mkdir -p distrib-dev/usr; cd distrib-dev/usr; [ -e lib64 ] || ln -s lib lib64
endif
	
	@echo -e "\n\ninstall -D runtimerootimage.gz"
	install -D runtimerootimage.gz distrib/boot/initrd-$(K_SWE_VERSION).gz
	install -D installrootimage.gz cdrom-dev/installrootimage.gz
	
	echo "        unpack dev packages" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nUnpacking dev packages"
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
	@echo -e "\n\nCopying dev shared libs to distrib"
	(cd distrib-dev; \
	  find . -name \*.so\* -print | cpio -pd ../distrib \
	)
	
	@echo "        unpack main packages" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nUnpacking main packages"
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
	@echo -e "\n\nMoving includes to distrib-dev"
	if [ -d distrib/usr/include ]; then \
	  mkdir -p distrib-dev/usr/include; \
	  cp -a distrib/usr/include distrib-dev/usr/; \
	  rm -rf distrib/usr/include/*; \
	  mv distrib-dev/usr/include/python2.7 distrib/usr/include; fi
	
	@echo "        move static libs to distrib-dev" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nMoving static libs to distrib-dev:"
	cd distrib; find . -name \*.a -o -name \*.la | while read a; do \
	  mkdir -p ../distrib-dev/`dirname $$a`; \
	  mv $$a ../distrib-dev/$$a; \
	done
	
	@echo "        move docs to distrib-doc" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nMoving docs to distrib-doc"
	for I in man info share/man share/info share/doc share/gtk-doc \
	      share/ntop/html share/slsh/help examples; do \
	  if [ -d distrib/usr/$$I ]; then \
	    mkdir -p distrib-doc/usr/$$I; \
	    mv distrib/usr/$$I/* distrib-doc/usr/$$I/; fi; \
	done
	
	@echo "        delete FB devices" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\ndelete FB devices"
	@for i in distrib/lib/modules/*; do \
	    (cd $$i/kernel; rm -rf $(NOT_DRIVERS)); \
	  done
	@echo "        strip symbols" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nstrip symbols"
	/build/toolcrib/striptree distrib
	@echo -e "\n\nstrip symbols -dev"
	/build/toolcrib/striptree distrib-dev
	@echo -e "\n\nstrip symbols -doc"
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

	(if [ -a ../../swe-u10-arm-patch.tar.xz ] ; then \
      cp -v ../../swe-u10-arm-patch.tar.xz distrib/boot/ ; \
	fi);

# fake-hwclock adjustment
ifeq ($(mTUPLE),$(filter $(mTUPLE),pi0w rpi2 rpi3 pi3-64 rpi4 pi4-64))
	@echo "        setting fake-harware clock" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nsetting fake-harware clock"; echo
	echo "`date -u '+%Y-%m-%d %H:%M:%S'`" > distrib/etc/fake-hwclock.data
else ifeq ($(mTUPLE),xu4)
	@echo "        Copy boot.ini" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nCopy boot.ini's"; echo
	cp -av boot.ini.xu4 distrib/boot/boot.ini
# maybe
	echo Smoothie distrib/etc/httpd/conf/httpd.conf

	# xu4 does not make a 70-persistent-net.rules for the 8153 nic
	sed -i '/compareMACs/s/^/# /g' distrib/etc/rc.d/rc.sysinit
	grep -r 'compareMACs' distrib/etc/rc.d/rc.sysinit

	@echo "        Making uInitrd" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nMaking uInitrd"; echo
	cd distrib/boot; mkimage -A arm -O linux -T ramdisk -C gzip -a 0x0 -e 0x0 -n uInitrd -d initrd-$(K_SWE_VERSION).gz uInitrd
endif

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
#	@mkdir cdrom-dev
	@cd cdrom; cp -avR . ../cdrom-dev/
	@cd distrib/boot; cp -avR . ../../cdrom-dev/

ifeq ($(mTUPLE),$(mARCH))
	@echo "      copy to OffRoad ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nCopying to OffRoad ..."
	@mkdir -p offroad
	@cd cdrom; cp -av . ../offroad
	@for i in main other; do sed -i \
	     -e '/Install Smoothwall/,+4d' \
	     -e '/Convert ISO/,+9d' \
	     -e '$d' \
	     offroad/boot/grub/$${i}.conf; done
endif
	
	@echo "      build final tarballs ..." >>$(MEDIA_BUILD_OUT)
	@echo "        main ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\nBuilding smoothwall.tgz, stand by ..."
	@tar -zcf cdrom/smoothwall.tgz -C distrib .
	@echo -n `tar tvf cdrom/smoothwall.tgz |wc -l` > cdrom/smoothwall.tgz.filecount
	@cp -a cdrom/smoothwall.tgz* cdrom-dev/
	@echo -e "\n\nCreate md5sum"
	(cd cdrom; md5sum smoothwall.tgz > smoothwall.tgz.md5sum)
	cp -v cdrom/smoothwall.tgz.md5sum cdrom-dev/

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

extracontent: cdrom/smoothwall.tgz
	@echo "      extracontent ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nextracontent"
ifeq ($(mTUPLE),$(mARCH))
	cp -avR ../media/extracontent/* cdrom
else
	cp -avR ../media/extracontent/docs cdrom-dev
	cp -av ../media/extracontent/smoothwall.ico cdrom-dev
endif
	(for I in README.txt README.html; do \
		cat ../media/templates/$$I | \
			sed "s@\%PRODUCT_NAME\%@$(PRODUCT_NAME)@g" | \
			sed "s@\%BASENAME\%@$(BASENAME)@g" \
		> cdrom/$$I; \
	done);
	find cdrom -name .git -exec rm -rf {} \;
ifeq ($(mARCH),arm)
	cp -av cdrom/README* cdrom-dev
endif
	cp -av ../wpa_supplicant/wpa_supplicant.conf.sample cdrom
	cp -av ../wpa_supplicant/wpa_supplicant.conf.sample cdrom-dev

all: clean cdrom cdrom/smoothwall.tgz extracontent
#all: cdrom cdrom/smoothwall.tgz
	@echo -e "\n\nall\n\n"
ifeq ($(mTUPLE),$(mARCH))
	@echo "      assemble full ISO ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nassemble full ISO ..."
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
	@echo -e "\n\nassemble dev ISO ..."
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
	@echo -e "\n\nassemble offRoad ISO ..."
	@( \
	  RELEASE="$(BASENAME)$(PRODUCT_EXTRA)-$(mTUPLE)"; \
	  ISONAME=$(TARGET_DIR)/isos/$${RELEASE}-offroad.iso; \
	  /sbin/mkisofs -o $${ISONAME} \
	    -b boot/grub/stage2_eltorito -J -R \
	    -no-emul-boot -boot-load-size 4 -boot-info-table \
	    -V $(BASENAME) --publisher "Smoothwall Express (OffRoad)" offroad; \
	  echo -e "$${ISONAME} assembly complete\n\n"; \
	)
else ifeq ($(mTUPLE),$(filter $(mTUPLE),pi0w rpi2 rpi3 pi3-64 rpi4 pi4-64))
	#cp -v cdrom/cmdline.txt.install cdrom/cmdline.txt
	#cp -v cdrom/config.txt.install cdrom/config.txt
	cp -v cdrom-dev/cmdline.txt.install cdrom-dev/cmdline.txt
	cp -v cdrom-dev/config.txt.install cdrom-dev/config.txt

	@echo "      Create $(mTUPLE) zip ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nCreate $(mTUPLE) zip ..."
	cd cdrom-dev; zip -x smoothdev.tgz -r $(ZIPNAME) *
	#cd cdrom-dev; TAR_OPTIONS= tar -cjSf ../SmoothWall-$(mTUPLE).tar.bz2 * --exclude=smoothdev.tgz
	@echo "      Create $(mTUPLE) dev zip ..." >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nCreate $(mTUPLE) dev zip ..."
	#cd cdrom-dev; zip -r $(DEVZIPNAME) *

	@echo "        $(ZIPNAME) assembly complete" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\$(ZIPNAME) assembly complete"
	@echo -e "$(ZIPNAME) assembly complete\n\n"



else
	@echo; echo "Might need to adjust"
	exit 42
endif

clean:
ifndef BUILD_PHASE
	@echo -n " $(PACKAGE)"
	@rm -f Media.mediaISO.built
	@rm -f *.img
	@rm -rf cdrom cdrom-dev offroad distrib distrib-dev distrib-doc klibc temp
	@make --no-print-directory -C cdromboot clean >/dev/null 2>&1
	@make --no-print-directory -C installroot clean >/dev/null 2>&1
	@make --no-print-directory -C runtimeroot clean >/dev/null 2>&1
else
	@echo "$(PACKAGE)"
	@echo; echo "clean"
	pwd
	#rm -vf Media.mediaISO.built
	#rm -vf Media.mediaISO.out
	rm -vf *.gz
	rm -vf *.img
	rm -vf $(TARGET_DIR)/isos/*.zip
	rm -rf cdrom cdrom-dev offroad distrib distrib-dev distrib-doc klibc temp
	make --no-print-directory -C cdromboot clean
	make --no-print-directory -C runtimeroot clean
	make --no-print-directory -C installroot clean
	#exit 42
endif	
	
download:
	@true
