                        Smoothwall Express Build System
                        ===============================
                        fest3er-swe3.1-update10 ++ p4-64

Basic's of Build Process
------------------------
  cd SmoothWall-pi/distrib/build
  make predownload
  make build
  make media

Install zip file is in target/isos

OVERVIEW
--------

The build process consists of 3 main steps:

  1. Construct a temporary "tools" environment using the hosts toolchain.  A
     symlink in the host (/tools) ensures that all programs, when a "make
     install" is done on them, end up in the temporary tree and not in the
     host system.  This symlink is created automatically.  The build process
     automatically archives the toolchain and the crumbs directory (see below)
     so that this step can be skipped if desired.

  2. Compile all packages that will end up in the final installation
     smoothwall.tgz, plus any programs and libraries that are required to
     compile those programs.  This stage is done using the temporary tools
     environment and is chrooted into the working build environment.  Before
     building the "core" packages, such as the kernel etc, the build toolchain
     that will be used in the final build is compiled up with the /tools
     toolchain, thus the /tools structure is no longer needed.  Packages that
     are compiled and installed are placed into the build environment (i.e.
     under distrib/).  Also, each compiled package is tarred up into a tarball
     that is used in step 3.

  3. Create the last few tools needed to create the final bootable ISO (such
     as mkisofs, and grub).  Then build the smoothwall.tgz, by untarring the
     packages compiled in step 2 into a new directory.  Smoothwall specific
     files are added from the "coretree" package.  Finally build the bootdisk
     images and the ISO itself.

An optional fourth step is to prepare a bootable flash drive to install
without an optical drive.  This process copies the contents of the ISO to the
flash, make a miniscule adjustment to grub.conf, then installs grub to make
the flash bootable.  It should work just as well on an external rotating drive,
but this has not been tested.



LAYOUT
------

Smoothwall Express can be built in any directory on any file system that has
about 16GiB free space.  We'll use "/home/express" in the following examples.

Change directory to /home/express.

This directory can be used to hold documentation and other files that won't be
used in the build environment itself.  This README file is one example.

The main working directory is distrib/.  Once an initial build has been
completed, this directory can be chrooted into and it will be possible to work
on the tree, add new packages, etc.  chroot is used to build the final phase.

Change directory to distrib/.

Directory tools/ contains the temporary (toolchain) build environment.  Even
after a completed build, you should leave this directory alone; it will be
needed if you rebuild the final phase (step 2, above).  Note that it is valid
to archive tools/ and build/crumbs (see below) and to restore them if you wish
to skip building the toolchain (step 1, above).

Change directory to build./

build/ is where the "action" is.  This directory contains the build top level
makefile and directories buildroot, crumbs, downloads, sources, target, and
toolcrib.

build/Makefile is the top level makefile.  This controls the entire build
process.  Run 'make' to see basic build instructions.

build/buildroot is where each compiled package's files and directories are
assembled in a faux root directory so that their tarballs (archives) can be
unpacked directly to the target root dir.

build/crumbs contains a number of 'bread crumbs' and log files related to the
build system itself.  For the most part, the 'bread crumbs' are empty files
that the build system uses to keep track of where it is in the build process.
The crumbs allow the build process to be re-entrant while also ensuring that
each package is always built from scratch.

build/downloads contains all of the downloaded source tarballs as well as a
flag file for each tarball to indicate that the tarball doesn't need to be
fetched.

build/target contains all of the final compiled/assembled package tarballs
that will be used to prepare the installation media.  build/target/isos
contains the ISO 9660 images that users will download, burn to CD/DVD, and
install to load their own Smoothwall Express firewalls.

build/toolcrib contains all of the top-level scripts used to check, prepare,
compile, build and assemble the system.  It contains scripts that install the
necessary packages on a standard GNU/Linux distribution so that it can build
Smoothwall Express.  There is a script used to build the three phases of the
toolchain and a script used to build the final phase of the system.  There are
a number of scripts used to adjust the toolchain during the build process and
to verify its correct operation.  There is a script that contains some handy
tools to monitor the build process and to rebuild packages in the final phase.

build/sources is the real heart of the build process.  Each directory is a
package, including some smoothwall-specific ones, like libsmooth+setup for the
setup program, setuids for the little C 'set UID root' programs, etc.  Each dir
contains a Makefile that must have specific targets, such "download".  The
clever part is it is possible to use ready made targets, by including the
Makefile.rules in the directory above.  This has targets for configuring,
compiling, installing and creating the package archive.  For GNU-compliant,
./configure compatible packages, it is possible to make a makefile to build
the package in only a few lines, including the download URL.  See the
sources/sed/Makefile for a good example.

Two packages are worth extra attention: coretree is a package that builds a
tarfile tree of all the extra files needed by smoothie, such as CGIs etc.  It
does this by copying them out of sources/coretree/tree into a temp dir, before
tarring up the temp dir.  So if you want to add static files to the distrib,
add them to this tree.  Symlinks and permissions are not directly set in this
tree - they are created and set in media/Makefile, scripted fashion.

Finally, build/sources/media is where the INITRAMFSes and ISOs are assembled.
Three ISOs are prepared.
  1. OffRoad Explorer; it contains the kernel and initramfs and grub--just
     enough so you can boot to a shell prompt and explore your hardware to
     see if it is supported.  It is small (around 32MiB) so you'll waste less
     of your scarce time just to see if Smoothwall will even boot on your
     hardware.
  2. Standard firewall runtime; it contains no development programs or docs.
  3. Development firewall runtime; everything needed to build Smoothwall
     Express is included.

The final ISOs are stored in the build/target/iso directory.



THE TOOLCRIB
------------

The toolcrib contains nearly all of the scripts and utilities used to build
Smoothwall.  In alphabetical order, they are:

as_chroot - enable the build system to perform specific operations as root
     (the super user) in a change-root (chroot) jail.  This allows the user to
     execute the build as a non-root user, thus reducing the chance the build
     system will damage the host system.

distrib_root - a one-liner that returns the absolute path of the distrib dir's
     parent.  This is part of what enables the system to be built almost
     anywhere in the host's filesystem(s).

dlverify - this script is used to perform that actual download of each
     package's source tarballs.  It defaults to looking in the Smoothwall
     Express project's archive for them, but will fall back to the upstream
     insternet sources as needed.  There are provisions to use different
     internet and local collections.  There are a few options available to
     control other aspects of its operation.  Please read the script for all
     the details.

     [From the original SWE3.0 README: "Download and verify".  This is a little
     helper script that wraps wget.  The purpose of the wrapper is two-fold: to
     stop wget being called on a completed download, thus causing unnecessary
     network traffic, and also to verify a completed download by MD5.  The
     arguments are: <directory> <url> [md5].  Directory is usually the standard
     d/l area.  The MD5 can be left off, in which case no download check is
     done.  To cope with partial downloads, once a d/l has completed, an
     additional touch file will be created with the same name as the download
     file, plus ".done".  Only if this file is present will the download be
     skipped over.  Note that the Makefile.conf (in sources) defines DL_CMD for
     you, and it includes the download destination dir.  So to do a download
     from within a makefile, you should usually just do: $(DL_CMD) http://...
     This script also has the ability to use a local mirror.  The URL root for
     the mirror is set at the top of the script.  To create a local mirror for
     yourself, after doing a full build, copy the files in build/download
     (except the .done files) into your mirror.]

environment - contains only the bash function 'set_build_environment'.  This
     function ensures that each phase of the build gets the precise
     environment it needs in order to build its bits correctly.

final_tc_adjustment - this performs the final adjustments to the toolchain
     after glibc is built during the final phase.  It also contains a provision
     to unwind (reverse) the adjustment in case the adjustment fails; it's
     also used to re-prepare the build tree so that the final phase can be
     rebuilt.

final_tc_check - this performs a number of sanity checks on the toolchain
     after gcc has been built during the final phase.  This ensures that the
     build process stops if the toolchain has not been properly built.

functions - it contains a number of low- and mid-level functions used during
     the build process.  These functions run adjustments, package builds and
     toolchain build phases; they check results for sanity and also determine
     how many CPUs/cores are available for the build.

handy_tools - contains a few very handy commandline tools: gitstat (find what
     you've changed), monbuild (monitor the progress of a package's build),
     monloop (monbuild in a convenient loop) and redo (rebuild specific final
     phase packages without dealing with the trail of breadcrumbs).

host_check.sh - checks the host environment for all of the requisite tools
     needed to build.  This is done first; if the right stuff isn't found, the
     build fails immediately.

host_debian_inst, host_gentoo_inst - these scripts install any missing
     requisite packages on the respective host systems.  They should ensure
     that host_check.sh never fails.

make_final - this script is run in a chroot jail as root.  It handles building
     the entire final phase of the build.

make_flash - converts the assembled ISO onto a USB thumb drive and makes it
     bootable.

make_media - assembles the install, development and offroad ISOs.

make_toolchain - builds the toolchain needed to build the final phase.

prep_final_env - prepares the environment for script prepare_final_tree.

securetree - turns off user and group 'sticky' bits on all files and dirs in
     the specified dir.

striptree - strips symbol tables &cet.  from programs, libraries and modules.

tc_check - checks the sanity of the toolchain after each build phase to ensure
     that a faulty build process doesn't traipse down the road to Perdition.



USING THE BUILD SCRIPTS
-----------------------

When building on a standard GNU/Linux distribution, it is recommended that you
build as a non-root user; the build system uses su and/or sudo to become root
when it needs to.  This minimizes the chance that a programming mistake will
wipe out or even subtley alter your host system.

The build tree may be installed anywhere on the host system; the script
'distrib_root' finds the path.  The build system ensures that the /tools
symlink points to the right place before proceeding with the build.  Be aware
that since there can be only *one* /tools symlink, you can execute exactly
*one* build at any given time.

The build system ensures that a reasonable /etc/resolv.conf exists in the
final phase chroot jail.  This allows requisite network operations to succeed.

Enter "make" (with no rule) to display helpful information related to running
the build system.  There are also several help rules that display more in-depth
information on some advanced features of the build system.

To start the build, enter "make build".  Note that some packages now insist on
using HTTPS when fetching their source tarballs.  As of 11/2013, the wget built
for the toolchain still doesn't handle not checking HTTPS security
certificates.  Therefore, it is best to run 'make predownload' to pre-fetch all
the source tarballs before starting the build.



RESTARTING THE BUILD
--------------------

The build is (nearly) completely re-entrant.  You may interrupt it at almost
any point; the next time you build, it will pick up at the beginning of the
step when it was interrupted.



TESTED HOST ENVIRONMENTS
------------------------

Smoothwall Express 3.1
Debian Wheezy
Debian Squeeze
Gentoo

Generally, the build should work on any Linux that is capable of building GCC
4.7.2, binutils 2.22 and glibc 2.14.1.

As of 2013/03/15, there have been problems building on systems using GCC 4.6
and GLIBC 3.15-3.17.



THANKS TO
---------

Linux From Scratch (www.linuxfromscratch.org); their LFS books were invaluable
     on the journey enhancing the build system and modernizing the source
     packages.



CREDITS
-------

Lawrence Manning (smoothwall@aslak.net) - Initial implementation.
Neal Murphy (neal.p.murphy@alum.wpi.edu) - SMP, re-entrance and bread crumbs,
     general modernization, 2009-2013.



COPYRIGHT AND LICENCE
---------------------

The Smoothwall build system and associated scripts are (c) Smoothwall Ltd,
2005 and licenced under the GNU GPL v2.

Murphy's enhancements are © Neal P. Murphy and fully licensed under the GNU
GPL v2.

ShorTie's enhancements are © Jeffrey R. Blanner and fully licensed under the
GNU GPL v2.
