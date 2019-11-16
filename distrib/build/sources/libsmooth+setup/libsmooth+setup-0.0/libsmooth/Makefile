# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile
include ../../../Makefile.versions

CC = gcc 

LD = ld
LDFLAGS = -i

COMPILE = $(CC) -c $(INCLUDE) $(CFLAGS)

LINK = $(LD) $(LIBRARY) $(LDFLAGS)

all : libsmooth.so libsmooth.o 

clean :
	-rm -f *.o libsmooth.so core langs.h

langs.h :
	-cp -f langs.h.temp langs.h
	-cat english.c | ./makelangs.pl >> langs.h

######

OBJS = english.o varval.o main.o netstuff.o

libsmooth.so: $(OBJS)
	$(CC)  -fPIC -Wall -shared -Wl,-soname,$@ -o $@ $(OBJS) $(LIBS)

libsmooth.o: $(OBJS)
	$(LINK) $(OBJS) -o $@ $(LIBS)

%.o : %.c
	$(COMPILE) \
	  -D TITLE='"Smoothwall $(PRODUCT_NAME) $(PRODUCT_VERSION)-$(REVISION)$(PRODUCT_EXTRA)-$(mARCH)"' \
	  $< -o $@
		
english.o : langs.h english.c
#german.o : langs.h german.c
#dutch.o : langs.h dutch.c
#danish.o : langs.h danish.c

varval.o : langs.h varval.c
main.o : langs.h main.c
netstuff.o : langs.h netstuff.c


