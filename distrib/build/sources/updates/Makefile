# Keep 'make clean' tidy.

PACKAGE = updates
VERSION = N/A

clean:
	@echo -n " updates"
	@for i in update[1-9]*; do if [ -d $$i ]; then (cd $$i; make clean);  fi; done

print-version:
	@echo "$(PACKAGE) $(VERSION)"
