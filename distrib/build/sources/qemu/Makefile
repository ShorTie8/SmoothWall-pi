# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = qemu
VERSION = 2.12.1

BASE_URL = http://wiki.qemu-project.org/download
EXTENSION = .tar.bz2

# Verbose build
export V=1

ifeq ($(mTUPLE),x86_64)
CONFIG_OPTS = --target-list=x86_64-softmmu
else ifeq ($(mTUPLE),$(filter $(mTUPLE),pi0w rpi2 rpi3 rpi4 xu4))
CONFIG_OPTS = --target-list=arm-softmmu
else
CONFIG_OPTS = --target-list=i386-softmmu
endif

include ../Makefile.rules

