# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = vim
MAJ = 7
MIN = 3
VERSION = $(MAJ).$(MIN)

BASE_URL = ftp://ftp.vim.org/pub/vim/unix/
EXTENSION = .tar.bz2

DIR = $(PACKAGE)$(MAJ)$(MIN)

CONFIG_OPTS += --prefix=${PKG_DIR} --with-tlib=tinfo

INSTALL = yes

install: compile
	mkdir -p $(PKG_ROOT)
	+cd $(DIR); \
	  $(MAKE) DESTDIR=$(PKG_ROOT) install; \
	  install runtime/vimrc_example.vim $(PKG_ROOT)$(PKG_DIR)/share/vim/vimrc; \
	  sed -i -e 's/mouse=a/mouse=/' $(PKG_ROOT)$(PKG_DIR)/share/vim/vimrc
	cd $(PKG_ROOT)/usr/bin; ln -s vim vi;
	cd $(PKG_ROOT)/usr/share/man; \
	  find . -name vim.1 -print | while read a; do \
	    ln -sv `basename $$a` `dirname $$a`/vi.1; \
	  done
	cd $(PKG_ROOT)/usr/share; \
	  mkdir doc; \
	  cd doc; \
	  ln -sv ../vim/vim73/doc vim-$(MAJ).$(MIN)


include ../Makefile.rules
