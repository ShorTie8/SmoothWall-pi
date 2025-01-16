# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

CC=gcc

COMPILE = $(CC) $(CFLAGS)

DEFUNCT_PROGS = setdmzholes setportfw setoutbound setxtaccess restartdhcp restartsnort \
	restartsquid smoothiedeath smoothierebirth alcateladslfw \
	ipsecctrl  restartdnsproxy restartssh \
	setadvnet setipblock restartupnp restartntpd updown

PROGS = installpackage

all : $(PROGS)

clean : 
	-rm -f $(PROGS) *.o core

######

% : %.c
	$(COMPILE) $< -o $@
