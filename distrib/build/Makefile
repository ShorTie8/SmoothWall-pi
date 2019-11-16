# SmoothWall Build system.
#
# Parts (c) SmoothWall Ltd 2005
# Parts (c) Neal P. Murphy 2009-2012
#
# This code is distributed under the terms of the GPL v2.
#
# Top level Makefile for SmoothWall Build system.

# A few notes:
#   - This build system is re-entrant and uses multiple CPUs (when available).
#   - The toolchain is built and installed as the starting user. Root is
#     invoked as needed, such as to adjust the host's /tool symlink.
#   - The final stage and the ISO are built as user root in the chroot jail;
#     thus root owns all files created in the final phase.
#   - The flash drive is prepared as user root. The drive is determined using
#     inotifywait; it's plug-n-play.
#
#   - This build system is far more robust than the original. If you
#     build as a non-root user, there is almost no chance of damaging
#     your host system.
#   - If a package build fails, a minor tweak will almost always let it
#     proceed without trouble.
#   - If one of the 'adjusting' steps fails, it will back out its
#     adjustments so you can try again.
#
#   - After completing the full build, you can rebuild bits and pieces by
#     using the 'redo' function ala 'redo daq snort'.

export SHELL = bash +h

include sources/Makefile
include sources/Makefile.flags-arch

export SRC_TGZ = ../../smoothsrc-$(mARCH).tar.gz

ifndef ktype
export ktype = 
export KERNEL_TYPE=
else
export KERNEL_TYPE=-$(ktype)
endif

ifneq ($(no_be), 1)
$(shell rm -f crumbs/build_environment)
$(shell make -f toolcrib/Makefile.build_environment prep_env >crumbs/redirectstdio.out 2>&1)
endif

# Default target, display help
#
default:
	@echo
	@echo "When building on a host GNU/Linux distrib, build as a non-root user. The"
	@echo "system will become root as needed via 'sudo'."
	@echo
	@echo "The build system is very robust, and very unlikely to hose your host"
	@echo "system. But you must still know what you are doing!"
	@echo
	@echo "Useful commands:"
	@echo "  . toolcrib/handy_utils"
	@echo "  make predownload"
	@echo "  make build"
	@echo "  make media"
	@echo
	@echo "To build 32-bit on an x86_64 GNU/Linux distro:"
	@echo "  linux32"
	@echo "  make build"
	@echo "This is the only method known to produce consistent results."
	@echo
	@echo "Useful targets:"
	@echo "  savesources       Make a tarball of the sources used to build."
	@echo
	@echo "  clean             Clean all but downloads to build from scratch."
	@echo "  predownload       Download sourcecode packages in advance."
	@echo "  toolchain         Build the toolchain and archive it for re-use."
	@echo "  build             Build everything or continue building from an error"
	@echo "                    or an interruption."
	@echo "  media             Make ISOs."
	@echo "  reprep-final      Prepare to rebuild final stage *only*."
	@echo "  package           Clean, archive sources, pre-fetch tarballs, build,"
	@echo "                    and make media with matching source tarball."
	@echo "  print-versions    Create crumbs/packageVersions.html to ease finding"
	@echo "                    newer versions of upstream packages."
	@echo
	@echo "Help:"
	@echo "  help-arch         How to select a different 32-bit ARCH"
	@echo "  help-dl           How to customize 'make predownload'"
	@echo "  help-utils        Handy build utilities"
	@echo "  help-env          Display environment used during the build"
	@echo
	@echo "Please view Makefile for other targets."
	@echo

help-arch:
	@echo
	@echo "Choose a different 32-bit ARCH"
	@echo "  ARCH32=i586 make build"
	@echo "  ARCH32=i686 make build"
	@echo

help-dl:
	@echo
	@echo "Predownload/download helpers"
	@echo "  Options to control downloads:"
	@echo "    CONTINUE_DL=    if you have a slow conection, this will continue"
	@echo "                    a previous, interrupted download instead of creating"
	@echo "                    tarball.[1-n]"
	@echo "    NO_CHECK_CERT=  do not check the veracity of SSL certs"
	@echo "    PASV=           use 'passive' FTP"
	@echo "    MIRROR_UNO=hostA and/or MIRROR_DOS=hostB"
	@echo "                    use hostA and/or hostB as sources for source packages."
	@echo "                    hostA defaults to \"\", and hostB defaults to"
	@echo "                    \"downloads.smoothwall.org/buildmirror/\". This helps when you"
	@echo "                    have a local web site containing the source tarballs"
	@echo "                    or want to verify the URLs in the pkg makefiles."
	@echo "  Example showing all four options:"
	@echo "    CONTINUE_DL= NO_CHECK_CERT= PASV= MIRROR_UNO=downloads \\"
	@echo "      MIRROR_DOS=\"\" make build"
	@echo "    Continue a previously started DL, don't check SSL certs, use FTP's"
	@echo "    PASSIVE facility, use the local 'downloads' web host, and do not"
	@echo "    use the smoothwall downloads mirror (skip right to internet sources)."
	@echo

help-env:
	@echo
	@echo "This is the basic environment used during the build:"
	@sed -e 's/^/  /' crumbs/build_environment
	@echo

help-utils:
	@echo
	@echo "There are useful functions in .../build/toolcrib/handy_utils:"
	@echo "  - monbuild: monitor the progress of a package's build"
	@echo "  - monloop: monbuild in a shell-like loop"
	@echo "  - redo: rebuild one or more packages in the final build stage"
	@echo "To use them: '. toolcrib/handy_utils' or source the file"
	@echo "in your ~/.bashrc so they're always ready."
	@echo


# Host check
#
crumbs/host.checked:
	@bash toolcrib/host_check.sh
	@touch crumbs/host.checked

# build preparation
#
crumbs/tc_prep.built:
	@+env -i toolcrib/make_toolchain PREP
	@touch crumbs/tc_prep.built

# build stage 1
#
crumbs/tc_stage_1.built: crumbs/tc_prep.built
	@+$(ARCHset) env -i toolcrib/make_toolchain 1
	@+$(ARCHset) env -i toolcrib/tc_check 1
	@#exit 101
	@rm -f dummy.c a.out
	@touch crumbs/tc_stage_1.built

# build stage 2
#
crumbs/tc_stage_2.built: crumbs/tc_stage_1.built
	@+$(ARCHset) env -i toolcrib/make_toolchain 2
	@+$(ARCHset) env -i toolcrib/tc_check 2
	@rm -f dummy.c a.out
	@#exit 102
	@touch crumbs/tc_stage_2.built

# build stage 3
#
crumbs/tc_stage_3.built: crumbs/tc_stage_2.built
	@+$(ARCHset) env -i toolcrib/make_toolchain 3
	@#exit 103
	@touch crumbs/tc_stage_3.built

# make the toolchain only
crumbs/toolchain.built: crumbs/host.checked crumbs/tc_stage_3.built
	@mkdir -pv target
	@sudo su -c "chown --reference . target"
	@tar cfJ target/smoothwall-toolchain-$(mARCH)$(PRODUCT_EXTRA).tar.xz ../tools crumbs
	@touch crumbs/toolchain.built

toolchain: crumbs/toolchain.built

# prepare final build environment
#
crumbs/Final.prep.built: crumbs/toolchain.built
	@(tput smso; echo -e "\nPreparing Final Build tree"; tput rmso) \
	    <$(BUILD_IN) >>$(BUILD_OUT) 2>&1
	+@$(ARCHset) toolcrib/as_chroot \
	    "/build/toolcrib/prepare_final_tree >crumbs/Final-prep.out 2>&1"
	@touch crumbs/Final.prep.built

# must have resolv.conf in chroot jail
#
crumbs/resolv.conf:
	@if [ -f /etc/resolv.conf ]; then cp /etc/resolv.conf ./crumbs/; fi
	@if [ -f /etc/resolv.conf.dnsmasq ]; then cp /etc/resolv.conf.dnsmasq ./crumbs/resolv.conf; fi

# build all software
#
crumbs/Final.built: crumbs/resolv.conf crumbs/Final.prep.built
	@(tput smso; echo -e "\nFinal Build"; tput rmso) \
	    <$(BUILD_IN) >>$(BUILD_OUT) 2>&1
	+@$(ARCHset) toolcrib/as_chroot "/build/toolcrib/make_final"
	@touch crumbs/Final.built

build: crumbs/host.checked crumbs/Final.built

rebuild:
	+@for i in clean predownload build; do \
	    $(MAKE) $$i; \
	done

# prepare the installation media
#
media: crumbs/Final.built
	+@(echo -e "\nMaking ISO images with linux$(KERNEL_TYPE)..."; sleep 1; \
	    $(ARCHset) toolcrib/as_chroot "/build/toolcrib/make_media") \
	    <$(BUILD_IN) >>$(BUILD_OUT) 2>&1

# prepare the specified update; the Final phase must have been built first.
#
update: crumbs/Final.built
	@if [ -z "$(UPDATE)" ]; then echo "Example: UPDATE=1 make update"; exit 234; fi;
	@echo -e "\nPreparing update '$(UPDATE)'..."
	+@ $(ARCHset) toolcrib/as_chroot "/build/toolcrib/make_update $(UPDATE)"

# prepare a bootable flash image
#
RELEASE = $(BASENAME)$(PRODUCT_EXTRA)-$(mTUPLE)
mediaflashimg: 
	@echo -e "\nMaking FLASH image..."; sleep 1
	@$(ARCHset) sudo su -c "RELEASE=$(RELEASE) toolcrib/make_flashimg"


# prepare a bootable flash drive
#
mediaflash: 
	@echo -e "\nMaking FLASH content..."; sleep 1
	@+sudo su -c "toolcrib/make_flash"

# after a successful build, this will do everything including a tarball of the
# sources and a tarball of the built toolchain.
#
package:
	+for i in clean savesources predownload build media; do \
	    $(MAKE) $$i; \
	done

# Get tossed in the pokey with the proper environment
#
chroot:
	@env -i /tools/bin/bash --rcfile crumbs/build_environment --noprofile toolcrib/as_chroot

# Pre-fetch source tarballs from internet
#
predownload:
	@echo -e "\nPre-downloading source tarballs..." \
	  <$(BUILD_IN) >>$(BUILD_OUT) 2>&1; sleep 1
	@( \
	  export BUILD_PHASE="PreDownload"; \
	  . toolcrib/environment; \
	  set_build_environment; \
	  cd sources; \
	  for I in `find . -maxdepth 3 -mindepth 1 -type d | sort`; do \
	    if [ "$$I" != "\./\.git" ]; then \
	      if echo $$I | egrep "^./nss/nss-[^/]*/nss" >/dev/null 2>&1; then \
	        continue; \
	      elif echo $$I | egrep "^./mtools/mtools-4.0.15/scripts" >/dev/null 2>&1; then \
	        continue; \
	      elif echo $$I | egrep "^./cdrtools" >/dev/null 2>&1; then \
	        NW="GMAKE_NOWARN=true "; \
	      else \
	        unset NW; \
	      fi; \
	      $(MAKE) $$NW -C $$I -n download >/dev/null 2>/dev/null; \
	      if [ $$? -eq 0 ]; then \
	        echo -n " `basename $$I`"; \
	        $(MAKE) --no-print-directory -C $$I download; \
	        if [ $$? -ne 0 ]; then \
	          echo -e "\n$$I predownload failed.\n"; \
	          exit 1; \
	        fi \
	      else \
		if [ $$I == "./daq" -o $$I == "./snort" ]; then \
		  echo -e "\ntoolcrib/get-snort-ver.sh could not get current $${I/.\//} version or URL" >&2; \
		  exit 1; \
		fi \
	      fi \
	    fi; \
	  done \
	) <$(BUILD_IN) >>$(BUILD_OUT) 2>&1; \
	echo

# Save a copy of the build directory, sans downloads, for future replication
#
savesources:
	@echo -e "\nArchiving sources..." \
	  <$(BUILD_IN) >>$(BUILD_OUT) 2>&1; sleep 1
	@tar cfz $(SRC_TGZ) -C .. --exclude build/downloads . \
	  <$(BUILD_IN) >>$(BUILD_OUT) 2>&1

packageinfos.html:
	@+if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(MAKE) packageinfos.html"; \
	else \
	  rm -rf /tmp/downloads; mkdir /tmp/downloads; \
	  echo "<ul>" >/tmp/packageinfo.html; \
	  (cd sources; for I in `find -maxdepth 1 -mindepth 1 -type d`; do \
		if [ "$$I" != "CVS" ]; then \
			ROOT=$$PWD/../.. $(MAKE) --no-print-directory -C $$I packageinfo.html; \
		fi \
	  done); \
	fi
	-$(MAKE) -C sources/modules packageinfos.html
	@echo "</ul>" >>/tmp/packageinfo.html

# Print all package version/source info
#
print-versions:
	@cd sources; \
	for I in */; do \
	  echo -n "$$I " >&2; pushd $$I >/dev/null 2>&1; make --no-print-directory print-version || echo "$$I||print-version failed||" ; popd >/dev/null 2>&1; \
	done | (echo "<html><body><table>" ; while read PKG VER BASE_URL ; do \
	  echo "<tr><td style='text-align:right'>$${PKG}</td><td>$$VER</td><td>$$BASE_URL</td></tr>"; \
	done | sort -f; echo "</table></body></html>") > ../crumbs/packageVersions.html

# Prepare to rebuild the final stage
reprep-final:
	@+$(ARCHset) toolcrib/as_chroot "/build/toolcrib/make_final --unwind"
	@+if [ `id -u` -eq 0 ]; then CMD="bash"; else CMD="sudo su"; fi; \
	   $$CMD -c "no_be=1 $(MAKE) clean-distrib clean-final-crumbs clean-media-crumbs clean-buildroot clean-target"

# Clean the entire directory back to pristine plus downloaded tarballs
clean:
	@if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(ARCHset) $(MAKE) clean"; \
	else \
	  no_be=1 $(MAKE) --no-print-directory clean-distrib; \
	  no_be=1 $(MAKE) --no-print-directory clean-buildroot; \
	  no_be=1 $(MAKE) --no-print-directory clean-target; \
	  no_be=1 $(ARCHset) $(MAKE) --no-print-directory clean-sources; \
	  no_be=1 $(MAKE) --no-print-directory clean-tools; \
	  no_be=1 $(MAKE) --no-print-directory clean-crumbs; \
	  rm -f $(SRC_TGZ); \
	  rm -f nohup.out; \
	fi

# Empty the buildroot directory
#
clean-buildroot:
	@+if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(MAKE) --no-print-directory clean-buildroot"; \
	else \
	  tput smso; echo "cleaning buildroot"; tput rmso; \
	  rm -rf buildroot/*; \
	fi

# Delete the ISOs and the package tarballs
#
clean-target:
	@+if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(MAKE) --no-print-directory clean-target"; \
	else \
	  tput smso; echo "cleaning target"; tput rmso; \
	  rm -rf target/*; \
	fi

# Clean the sources dir to 'pristine'
# NOTE: if you've bumped versions, the old version build dirs won't be removed
#   because the buid system is now blind to them.
#
clean-sources:
	@+if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(ARCHset) $(MAKE) --no-print-directory clean-sources"; \
	else \
	  tput smso; echo -n "cleaning sources"; tput rmso; \
	  (cd sources; for I in `find -maxdepth 1 -mindepth 1 -type d | sort`; do \
	     if [ "$$I" != "CVS" ]; then \
	       export BUILDDIR=`pwd`; $(ARCHset) $(MAKE) --no-print-directory -C $$I clean; \
	     fi \
	  done); \
	  echo; \
	fi
	@+sudo su -c "cd sources; find . -name wget-log -exec rm -f {} \;"
	@+sudo su -c "cd sources; find . -name wget-log.[0-9]\* -exec rm -f {} \;"

# Delete the toolchain
#
clean-tools:
	@+if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(MAKE) --no-print-directory clean-tools"; \
	else \
	  tput smso; echo "cleaning tools"; tput rmso; \
	  rm -rf ../tools/*; \
	fi

# Delete the packages installed for the chroot environment
#
clean-distrib:
	@+if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(MAKE) --no-print-directory clean-distrib"; \
	else \
	  tput smso; echo "cleaning distrib"; tput rmso; \
	  cd ..; rm -rf `ls -C1 . | egrep -v "build|tools"` ; \
	  echo "Only build and tools should print:"; \
	  ls -dC * | sed -e 's/^/  /'; \
	fi

# Vacuum up the trail of bread crumbs
#
clean-crumbs: clean-prep-crumbs clean-stage1-crumbs clean-stage2-crumbs clean-stage3-crumbs clean-final-crumbs clean-media-crumbs
	@rm -f crumbs/*

clean-prep-crumbs:
	@tput smso; echo "cleaning prep crumbs"; tput rmso
	@rm -f crumbs/host.checked crumbs/tc_prep.built crumbs/tc-Stage_PREP.debug

clean-stage1-crumbs:
	@tput smso; echo "cleaning stage1 crumbs"; tput rmso
	@rm -f sources/*/Stage_1*.{out,built} crumbs/*tage_1*

clean-stage2-crumbs:
	@tput smso; echo "cleaning stage2 crumbs"; tput rmso
	@rm -f sources/*/Stage_2*.{out,built} crumbs/*tage_2*

clean-stage3-crumbs:
	@tput smso; echo "cleaning stage3 crumbs"; tput rmso
	@rm -f sources/*/Stage_3*.{out,built} crumbs/*tage_3*

clean-final-crumbs:
	@+if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(MAKE) clean-final-crumbs"; \
	else \
	  tput smso; echo "cleaning final crumbs"; tput rmso; \
	  rm -f sources/*/Final*.{out,built} crumbs/Final* crumbs/resolv.conf; \
	fi

clean-media-crumbs:
	@+if [ `id -u` -ne 0 ]; then \
	  sudo su -c "no_be=1 $(MAKE) clean-media-crumbs"; \
	else \
	  tput smso; echo "cleaning media crumbs"; tput rmso; \
	  rm -f sources/*/Media*.{out,built} crumbs/Media*; \
	fi
