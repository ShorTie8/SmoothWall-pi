# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

ifeq ($(mARCH),$(filter $(mARCH),arm arm64))
include ../Makefile.kernel.rpi
else
include ../Makefile.kernel
endif

VERSION = $(KERNEL_VER)
