# Keep 'make clean' tidy.

PACKAGE = extras
VERSION = N/A
all:
	bin/bind-test -m
	(chroot ../../..) || bin/bind-test -u
	bin/bind-test -u

clean:
	@true

print-version:
	@echo "$(PACKAGE) $(VERSION)"

