# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = Python
<<<<<<< HEAD
MAX_VERSION = 3
MIN_VERSION = 11
VERSION = $(MAX_VERSION).$(MIN_VERSION).14
=======
VERSION = 3.11.14
>>>>>>> af3cfd7d4c327fc40902c0039f4504490d766118
EXTENSION = .tar.xz
BASE_URL = http://www.python.org/ftp/python/$(VERSION)

# Tool Chain Build Stage 3 Python 3
#
ifeq ($(BUILD_PHASE), Stage_3)

PATCH = yes
patch: $(DIR)/
	cd $(DIR); sed -i '/def add_multiarch_paths/a \        return' setup.py

CONFIG_OPTS = --prefix=$(TOOLS_DIR)

<<<<<<< HEAD
INSTALL = yes
install: compile
	@make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	# Remove precompiled pycache at toolchain and tests
	@(cd $(TOOLS_DIR)/lib/python3.$(MIN_VERSION) && \
		find . | grep -E "(/__pycache__|/test/)" | xargs rm -rf)

=======
>>>>>>> af3cfd7d4c327fc40902c0039f4504490d766118
endif

# Final Build Python 3
#
ifeq ($(BUILD_PHASE), Final)
CONFIG_OPTS += \
		--enable-shared \
		--with-system-ffi \
		--with-system-gdbm \
		--with-system-expat \
		--with-ensurepip=yes \
		ax_cv_c_float_words_bigendian=no

COMPILE = yes
compile: configure
	@find $(DIR) -type d -exec chmod o=rx {} \;
	@find $(DIR) -type f -exec chmod o=r {} \;
	@chmod -R o+rw $(DIR)
	@make ${JOBS} -C $(DIR)

endif

include ../Makefile.rules
