# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = isdn4k-utils
VERSION = 3.27_20151118
EXTENSION = .tar.xz

#BASE_URL = ftp://ftp.isdn4linux.de/pub/isdn4linux/CVS-Snapshots/
BASE_URL = http://pkgs.fedoraproject.org/repo/pkgs/isdn4k-utils/isdn4k-utils-3.27_20151118.tar.xz/8b4733559b1c4de3d7716af4dbbbb354

CONFIGURE = yes

configure: patch
	@cp -avR config $(DIR)/.config
	sed -i -e 's=test -f $$ac_dir/$$ac_word;=test -f "$$ac_dir/$$ac_word";=' $(DIR)/FAQ/configure
	@make -C $(DIR) subconfig
	sed -e 's/\(\$$(MAKE) -C $$$$i all\)/CFLAGS="$(CFLAGS)" \1/' $(DIR)/Makefile
	sed -i -e 's/\(\$$(MAKE) -C $$$$i all\)/CFLAGS="$(CFLAGS)" \1/' $(DIR)/Makefile
	# Avoid too much complexity, so do this here
	# But don't do it because it apparently hasn't been needed for 3.1
	# mkdir -p $(PKG_ROOT)/dev

include ../Makefile.rules
