# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile

VERSION_DEFINES = -DPRODUCT_NAME="\"$(PRODUCT_NAME) $(PRODUCT_VERSION)\"" -DPRODUCT_EXTRA="\"$(PRODUCT_EXTRA)\"" -DPRODUCT_ARCH="\"$(mARCH)\""
VERSION_DEFINES += -DTITLE='"Smoothwall $(PRODUCT_NAME) $(PRODUCT_VERSION)-$(REVISION)$(PRODUCT_EXTRA)-$(mARCH)"'

CC=gcc 

LD=gcc
LDFLAGS=-g -L../libsmooth
LIBS=-lnewt -lslang -ldl -lsmooth

COMPILE=$(CC) -c $(VERSION_DEFINES) $(INCLUDE) $(CFLAGS)

LINK=$(LD) $(LIBRARY) $(LDFLAGS)

all : programs

programs : setup

clean :
	-rm -f *.o setup core

######

OBJS=main.o hostname.o passwords.o networking.o misc.o webproxy.o \
	keymap.o restore.o isdn.o adsl.o dhcp.o defaults.o timezone.o

setup: $(OBJS)
	$(LINK) $(OBJS) -o $@ $(LIBS)

%.o : %.c
	$(COMPILE) $< -o $@
		
main.o : main.c
adsl.o : adsl.c
console.o : console.c
defaults.o : defaults.c
dhcp.o : dhcp.c
hardware.o : hardware.c
hostname.o : hostname.c
isdn.o : isdn.c
keymap.o : keymap.c
misc.o : misc.c
networking.o : networking.c
passwords.o : passwords.c
resetadmin.o : resetadmin.c
restore.o : restore.c
setup.o : setup.c
timezone.o : timezone.c
webproxy.o : webproxy.c
