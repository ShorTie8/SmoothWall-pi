# Copyright 2004-2010 SmoothWall Ltd

include ../../Makefile.versions
include ../../Makefile.conf

BASIC_ROOT_FS = basicrootfs

WORKING_DIR = /build/sources/basicrootfs/basicrootfs-0.0/tmp

CORETREE_DIR = /build/sources/coretree/distrib/
BB_DIR = /build/buildroot/busybox/
GLIBC_DIR = /build/buildroot/glibc/

all: clean
	make -C tools

	mkdir tmp

	(cd tmp && \
	mkdir bin cdrom dev etc harddisk lib proc sys tmp usr && \
	ln -s bin sbin && \
	cp -dvR --parents /usr/share/terminfo/l/linux . && \
	cp -dvR $(GLIBC_DIR)/usr/share/zoneinfo/UTC etc/localtime && \
	cp -dvR $(GLIBC_DIR)/lib/ld-*.so $(GLIBC_DIR)/lib/ld-*.so.* $(GLIBC_DIR)/lib/libc-*.so $(GLIBC_DIR)/lib/libc.so.* \
		$(GLIBC_DIR)/lib/libdl-* $(GLIBC_DIR)/lib/libdl.* \
		$(GLIBC_DIR)/lib/libm-* $(GLIBC_DIR)/lib/libm.* \
		$(GLIBC_DIR)/lib/libpthread-*.so $(GLIBC_DIR)/lib/libpthread.so.* \
		$(GLIBC_DIR)/lib/libnss_files* $(GLIBC_DIR)/lib/libnss_compat* lib && \
	cp -dvR $(CORETREE_DIR)/etc/nsswitch.conf etc && \
	cp -dvR $(CORETREE_DIR)/sbin/hotplug sbin/hotplug.dormant && \
	cp -avR $(BB_DIR)/opt/busybox/bin/* bin && \
	cp -dvR ../tools/iowrap ../tools/raidautorun bin && \
	cp -dvR ../etc/* etc && \
	touch etc/ld.so.conf && \
	mknod dev/console c 5 1 && \
	mknod dev/null c 1 3 && \
	mknod dev/md0 b 9 0 && \
	for TTY in 1 2 3 4 5 6; do mknod dev/tty$$TTY c 4 $$TTY; done && \
	tar zcvf dev.tar.gz dev && \
	/sbin/ldconfig -r . \
	)
	(cd tmp && \
	for PACKAGE in udev mdadm module-init-tools; do \
		tar zxvf /build/target/smoothwall-$$PACKAGE.tar.gz ; \
	done && \
	rm -rfv usr/share/locale && \
	rm -rfv sbin/insmod.static)

	/build/striptree tmp

ifdef BITS_64
	(cd tmp; ln -s lib lib64)
	(cd tmp/usr; ln -s lib lib64)
endif

	(cd tmp && \
	find . -print | cpio -H newc -ov | bzip2 > ../basicrootfs.bz2 \
	)

clean:
	@make -C tools clean
	@rm -rf $(BASIC_ROOT_FS) tmp/
	@rm -f $(BASIC_ROOT_FS).bz2
