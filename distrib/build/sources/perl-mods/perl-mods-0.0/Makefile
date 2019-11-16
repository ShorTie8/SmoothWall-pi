# SmoothWall Build System
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

all:
	@+for i in $(PERL_MODS); do \
	  make -C $$i install || exit 1; \
	done

download:
	@+for i in $(PERL_MODS); do \
	  echo -n " $$i"; \
	  make -C $$i download || exit 1; \
	done

clean:
	@+for i in $(PERL_MODS); do \
	  make --no-print-directory -C $$i clean; \
	done >/dev/null 2>&1
