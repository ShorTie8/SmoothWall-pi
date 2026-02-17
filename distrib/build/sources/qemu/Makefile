# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = qemu
VERSION = 10.2.1
EXTENSION = .tar.xz
BASE_URL = https://download.qemu.org

# Verbose build
export V=1

ifeq ($(mTUPLE),x86_64)
CONFIG_OPTS = --target-list=x86_64-softmmu
else ifeq ($(mTUPLE),$(filter $(mTUPLE),pi0w rpi5))
CONFIG_OPTS = --target-list=arm-softmmu
else ifeq ($(mTUPLE),i586)
CONFIG_OPTS = --target-list=i386-softmmu
else
echo "UnSSupported mTUPLE $(mTUPLE)"
exit 46
endif

include ../Makefile.rules

