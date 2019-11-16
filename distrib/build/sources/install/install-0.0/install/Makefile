# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile

VERSION_DEFINES = -DPRODUCT_NAME="\"$(PRODUCT_NAME) $(PRODUCT_VERSION)\"" -DPRODUCT_EXTRA="\"$(PRODUCT_EXTRA)\"" -DPRODUCT_ARCH="\"$(mARCH)\""

CFLAGS += -DTITLE='"Smoothwall $(PRODUCT_NAME) $(PRODUCT_VERSION)-$(REVISION)$(PRODUCT_EXTRA)-$(mARCH)"'
CXXFLAGS += -DTITLE='"Smoothwall $(PRODUCT_NAME) $(PRODUCT_VERSION)-$(REVISION)$(PRODUCT_EXTRA)-$(mARCH)"'

CC=gcc 

LD=gcc
LDFLAGS=-g 
LIBS=-lnewt -lslang

COMPILE=$(CC) -c $(EXTRA_DEFINES) $(VERSION_DEFINES) $(CAP_DEFINES) $(INCLUDE) $(CFLAGS)

LINK=$(LD) $(LIBRARY) $(LDFLAGS)

all : programs 

programs : clean install

clean :
	@rm -f *.o install core

######

OBJS=main.o storagedevice.o disks.o cdrom.o nic.o net.o config.o /usr/lib/libsmooth.o

install: $(OBJS)
	$(LINK) $(OBJS) -o $@ $(LIBS)

%.o : %.c
	$(COMPILE) $< -o $@
		
main.o : main.c
storagedevice.o : storagedevice.c
disks.o : disks.c
cdrom.o : cdrom.c
nic.o : nic.c
net.o : net.c
config.o : config.c
