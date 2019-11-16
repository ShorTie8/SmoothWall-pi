/* SmoothWall install program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * filename: main.c
 * Contains main entry point, and misc functions. */

#include <unistd.h>
#include "install.h"

#define CDROM_INSTALL 0
#define URL_INSTALL 1

#define TRIM_DISK_SIZE 60000

FILE *flog = NULL;
char *logname;

char **ctr;

extern char *english_tr[];

static int partitiondisk(char *diskdevnode);

int main(int argc, char *argv[])
{
	char fmtpartdevnode[STRING_SIZE];
	struct blockdevice hd, cdrom;	/* Params for CDROM and HD */
	int cdmounted;			/* Loop flag for inserting a cd. */ 
	int rc;
	char commandstring[STRING_SIZE];
	int installtype = CDROM_INSTALL; 
	char *insertmessage, *insertdevnode;
	char tarballfilename[STRING_SIZE];
	char shortlangname[10];
	char tarballFileCountStr[21];
	int allok = 0;
	int tarballFileCount = 40000;
	struct keyvalue *ethernetkv = initkeyvalues();
	FILE *handle;
	FILE *Fpartitions, *openShut;
	int maximum_free, current_free, partStart;
	int log_partition, boot_partition, root_partition, swap_partition;
	struct keyvalue *hwprofilekv = initkeyvalues();
	FILE *hkernelcmdline;
	char kernelcmdline[STRING_SIZE];
	int ramsize;
	int trimbigdisk = 0;
	int partitionsizes[5];
	int c = 0;

	setenv("TERM", "linux", 0);

	sethostname("smoothwall", 10);

	memset(&hd, 0, sizeof(struct blockdevice));
	memset(&cdrom, 0, sizeof(struct blockdevice));
	memset(fmtpartdevnode, 0, STRING_SIZE);
	memset(kernelcmdline, 0, STRING_SIZE);
	memset(partitionsizes, 0, 5 * sizeof(int));

	/* Log file/terminal stuff. */
	if (argc >= 2)
	{		
		if (!(flog = fopen(argv[1], "w+")))
			return 0;
	}
	else
		return 0;
	
	logname = argv[1];
	
	fprintf(flog, "Install program started.\n");

	if (!(hkernelcmdline = fopen("/proc/cmdline", "r")))
		return 0;
	fgets(kernelcmdline, STRING_SIZE, hkernelcmdline);
	fclose(hkernelcmdline);
	
	if (strstr(kernelcmdline, "trimbigdisk"))
		trimbigdisk = 1;

	newtInit();
	newtCls();

	ctr = english_tr;
	strcpy(shortlangname, "en");

	newtDrawRootText(0, 0, TITLE " -- http://smoothwall.org/");
	newtPushHelpLine(ctr[TR_HELPLINE]);

	newtWinMessage(ctr[TR_BASIC], ctr[TR_OK], ctr[TR_WELCOME]);
	
	/* Get device letter for the IDE HD.  This has to succeed. */
	if (!(findharddiskorcdrom(&hd, DISK_HD)))
	{
		errorbox(ctr[TR_NO_HARDDISK]);
		goto EXIT;
	}

	if (!(findharddiskorcdrom(&cdrom, DISK_CDROM)))
	{
		errorbox(ctr[TR_NO_CDROM]);
		goto EXIT;
	}
	else
		installtype = CDROM_INSTALL;
	
	if (installtype == CDROM_INSTALL)
	{
		insertmessage = ctr[TR_INSERT_CDROM];
		insertdevnode = cdrom.devnode;

		/* Try to mount /cdrom in a loop. */
		cdmounted = 0;
		snprintf(commandstring, STRING_SIZE, "/bin/mount %s /cdrom -o ro", insertdevnode);
		while (!cdmounted)
		{
			if (!(mysystem(commandstring))) {
				cdmounted = 1;
			} else {
				rc = newtWinChoice(ctr[TR_BASIC], ctr[TR_OK], ctr[TR_CANCEL], insertmessage);
				if (rc != 1)
				{
					errorbox(ctr[TR_INSTALLATION_CANCELED]);
					goto EXIT;
				}
			}
		}
	}

	// Prepare the udev rules, including the persistent HD rules.
	snprintf(commandstring,
		 STRING_SIZE,
		 "/bin/installer/prepudevrules %s", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_PREPARING_DRIVER_RULES]))
	{
		errorbox(ctr[TR_UNABLE_TO_PREPARE_DRIVER_RULES]);
		goto EXIT;
	}

	rc = newtWinChoice(ctr[TR_BASIC], ctr[TR_OK], ctr[TR_CANCEL],
		ctr[TR_PREPARE_HARDDISK], hd.devnode);
	if (rc != 1)
		goto EXIT;

	rc = newtWinChoice(ctr[TR_PREPARE_HARDDISK_WARNING], ctr[TR_OK], ctr[TR_CANCEL],
		ctr[TR_PREPARE_HARDDISK_WARNING_LONG]);
	if (rc != 1)
		goto EXIT;

	/* If this fails, ramsize will be set to 0.  We can still cope though as this
	 * figure is only used as a guide to setting the swap size. */
	ramsize = gettotalmemory();
	fprintf(flog, "%d MiB RAM detected.\n", ramsize);

	// 2013/02/18 - Neal Murphy
	//   It's time to adjust partition sizes; hard drives have become immense in
	// 13 years. The boot partition grows to 200MiB. Swap is limited to at least
	// 256MiB and up to 1/8 of the total disk space; if you have 16GiB RAM, you
	// *surely* don't need 16GiB swap. Logs probably shouldn't grow larger than
	// 20GiB unless you are logging all packets on a saturated gigE link. The root
	// FS can have the rest of the disk.
	//   SWE3 has grown in size. It can be made to install on a 1GB drive, but
	// that's rather tight. 2GiB is OK for a plain, simple firewall. 16GiB is
	// probably more than most systems will need. Building SWE3.1 now requires
	// around 12GiB disk.

	/* Partition, mkswp, mkfs. */
	/* before partitioning, first determine the sizes of each
	 * partition.  In order to do that we need to know the size of
	 * the disk. */
	maximum_free = getdisksize(hd.devnode);
	
	if (trimbigdisk)
		maximum_free = maximum_free > TRIM_DISK_SIZE ? TRIM_DISK_SIZE : maximum_free;

	fprintf(flog, "%d MiB disk space (Trimming: %d)\n", maximum_free, trimbigdisk);
	
	boot_partition = 200; /* in MiB */

	// '-4' for 1 MiB at each end and 2MiB bios_grub partition (for Grub2 someday).
	current_free = maximum_free - boot_partition - 4;

	// Swap size should never need to be larger than 1/8 of the disk. It could probably
	// be fixed at 512MiB.
	if (ramsize > maximum_free/8)
		swap_partition = maximum_free/8 > 1024 ? 1024 : maximum_free/8;
	else
		swap_partition = ramsize < 256 ? 256 : ramsize; /* in MiB */
	current_free -= swap_partition;
	
	// Set log partition to 1/3 free, but crowbar between 20MiB and 20000MiB.
	log_partition = (current_free / 3) > 20 ? current_free / 3 : 20;
	if (log_partition > 20000) { log_partition = 20000; }
	current_free -= log_partition;

	root_partition = current_free;
	fprintf(flog, "boot = %d, swap = %d, log = %d, root = %d\n",
		boot_partition, swap_partition, log_partition, root_partition);

	// To make the partitions
	Fpartitions = fopen("/tmp/partitions", "w");
	fprintf(Fpartitions, "unit MiB\n");
	fprintf(Fpartitions, "select %s\n", hd.devnode);
	fprintf(Fpartitions, "mklabel gpt\n");
	partStart = 3;
	fprintf(Fpartitions, "mkpart boot ext4 %d %d\n", partStart, partStart+boot_partition);
	fprintf(Fpartitions, "name 1 \"/boot\"\n");
	fprintf(Fpartitions, "toggle 1 boot\n");
	partStart += boot_partition;
	fprintf(Fpartitions, "mkpart swap linux-swap %d %d\n", partStart, partStart+swap_partition);
	fprintf(Fpartitions, "name 2 swap\n");
	partStart += swap_partition;
	fprintf(Fpartitions, "mkpart log ext4 %d %d\n", partStart, partStart+log_partition);
	fprintf(Fpartitions, "name 3 \"/var/log\"\n");
	partStart += log_partition;
	fprintf(Fpartitions, "mkpart root ext4 %d %d\n", partStart, partStart+root_partition);
	fprintf(Fpartitions, "name 4 \"/\"\n");
	// Someday, these will be added to handle UEFI
	//fprintf(Fpartitions, "mkpart bios_grub 1 2\n");
	//fprintf(Fpartitions, "name 5 \"bios_grub\"\n");
	fprintf(Fpartitions, "print\n");
	fprintf(Fpartitions, "quit\n");
	fclose (Fpartitions);

	if (partitiondisk(hd.devnode))
	{
		errorbox(ctr[TR_UNABLE_TO_PARTITION]);
		goto EXIT;
	}

	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -L boot -t ext4 -FFj %s1", hd.devnode);	
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_BOOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mkswap -L linux-swap %s2", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_SWAPSPACE]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_SWAPSPACE]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -L log -t ext4 -FFj %s3", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_LOG_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_LOG_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -L root -t ext4 -FFj %s4", hd.devnode);	
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_ROOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM]);
		goto EXIT;
	}
	/* Mount harddisk. */
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s4 /harddisk", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_ROOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM]);
		goto EXIT;
	}

	// Ensure the mount points exist and have limited access
	mkdir("/harddisk/boot", S_IRWXU|S_IRGRP|S_IXGRP|S_IRUSR|S_IXUSR);
	mkdir("/harddisk/var", S_IRWXU|S_IRGRP|S_IXGRP|S_IRUSR|S_IXUSR);
	mkdir("/harddisk/var/log", S_IRWXU|S_IRGRP|S_IXGRP|S_IRUSR|S_IXUSR);
	
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s1 /harddisk/boot", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_BOOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/swapon %s2", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_SWAP_PARTITION]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_SWAP_PARTITION]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s3 /harddisk/var/log", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_LOG_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM]);
		goto EXIT;
	}

	if (installtype == URL_INSTALL)
	{
		/* Network driver and params. */
		if (!(networkmenu(ethernetkv)))
		{
			errorbox(ctr[TR_NETWORK_SETUP_FAILED]);
			goto EXIT;
		}
	}

	/* Either use tarball from cdrom or download. */
	if (installtype == CDROM_INSTALL)
	{
		strncpy(tarballfilename, "/cdrom/smoothwall.tgz", STRING_SIZE);
		// Get the tarball's file count
		openShut = fopen("/cdrom/smoothwall.tgz.filecount", "r");
		fscanf(openShut, "%20s", tarballFileCountStr);
		fclose(openShut);
		tarballFileCount = strtol(tarballFileCountStr, NULL, 10);
	}
	else
	{
		if (!(downloadtarball()))
		{
			errorbox(ctr[TR_NO_TARBALL_DOWNLOADED]);
			goto EXIT;
		}
		strncpy(tarballfilename, "/harddisk/smoothwall.tgz", STRING_SIZE);
	}
	
	/* unpack... */
	snprintf(commandstring, STRING_SIZE, 
		"/bin/tar -C /harddisk -zxvf %s",
		tarballfilename);
	if (runcommandwithprogress(45, 4, ctr[TR_BASIC], commandstring, tarballFileCount,
		ctr[TR_INSTALLING_FILES]))
	{
		errorbox(ctr[TR_UNABLE_TO_INSTALL_FILES]);
		goto EXIT;
	}
	
	/* Remove temp tarball if we downloaded. */
	if (installtype == URL_INSTALL)
	{
		if (unlink("/harddisk/smoothwall.tgz"))
		{
			errorbox(ctr[TR_UNABLE_TO_REMOVE_TEMP_FILES]);
			goto EXIT;
		}
	}

	// Ensure the udev rules dir exists
	mkdir("/harddisk/etc", S_IRWXU|S_IRGRP|S_IXGRP|S_IRUSR|S_IXUSR);
	mkdir("/harddisk/etc/udev", S_IRWXU|S_IRGRP|S_IXGRP|S_IRUSR|S_IXUSR);
	mkdir("/harddisk/etc/udev/rules.d", S_IRWXU|S_IRGRP|S_IXGRP|S_IRUSR|S_IXUSR);
	// Copy the persistent rules from rootfs to HD
	mysystem("/bin/cp /etc/udev/rules.d/*Smoothwall* /harddisk/etc/udev/rules.d");

	// Create the new system's fstab
	if (runcommandwithstatus("/harddisk/usr/bin/installer/writefstab", ctr[TR_SETTING_UP_FSTAB]))
	{
		errorbox(ctr[TR_UNABLE_TO_SETUP_FSTAB]);
		goto EXIT;
	}

	// Save the hardware profile
	replacekeyvalue(hwprofilekv, "STORAGE_DEVNODE", hd.devnode);
	replacekeyvalue(hwprofilekv, "CDROM_DEVNODE", cdrom.devnode);
	replacekeyvalue(hwprofilekv, "FS", "ext4");
	writekeyvalues(hwprofilekv, "/harddisk/" CONFIG_ROOT "/main/hwprofile");

	// Set the default timezone
	openShut = fopen("/harddisk/" CONFIG_ROOT "/time/settings", "w");
	fprintf(openShut, "TIMEZONE=UTC\n");
	fclose(openShut);

	// Prepare module dependencies
	if (runcommandwithstatus("/bin/chroot /harddisk /sbin/depmod -a",
		ctr[TR_CALCULATING_MODULE_DEPENDENCIES]))
	{
		errorbox(ctr[TR_UNABLE_TO_CALCULATE_MODULE_DEPENDENCIES]);
		goto EXIT;
	}

	if (!(writeconfigs(&hd, ethernetkv, shortlangname)))
	{
		errorbox(ctr[TR_ERROR_WRITING_CONFIG]);
		goto EXIT;
	}
	
	if (runcommandwithstatus("/harddisk/usr/bin/installer/adjustinitrd", ctr[TR_ADJUSTING_INITRAMFS]))
	{
		errorbox(ctr[TR_UNABLE_TO_ADJUST_INITRAMFS]);
		goto EXIT;
	}

	// Write the grub config, bind-mount sys stuff, install grub
	if (runcommandwithstatus("/harddisk/usr/bin/installer/writegrubconf", ctr[TR_PREPARING_BOOTLOADER]))
	{
		errorbox(ctr[TR_UNABLE_TO_PREPARE_BOOTLOADER]);
		goto EXIT;
	}
	mysystem("/sbin/mount --rbind /proc /harddisk/proc");
	mysystem("/sbin/mount --rbind /sys /harddisk/sys");
	mysystem("/sbin/mount --rbind /dev /harddisk/dev");

	if (runcommandwithstatus("/harddisk/usr/bin/installer/installgrub",
		ctr[TR_INSTALLING_BOOTLOADER]))
	{
		errorbox(ctr[TR_UNABLE_TO_INSTALL_BOOTLOADER]);
		goto EXIT;
	}
	
	if (installtype == CDROM_INSTALL)
	{
		if (mysystem("/sbin/umount /cdrom"))
		{
			errorbox(ctr[TR_UNABLE_TO_UNMOUNT_CDROM]);
			goto EXIT;
		}

		if (!(ejectcdrom(cdrom.devnode)))
		{
			errorbox(ctr[TR_UNABLE_TO_EJECT_CDROM]);
			//goto EXIT; // This shouldn't fail the install.
		}
	}

	if (touchfile("/harddisk/var/smoothwall/patches/available"))
	{
		errorbox("Unable to touch patch list file.");
		goto EXIT;
	}		

	newtWinMessage(ctr[TR_CONGRATULATIONS], ctr[TR_OK],
		ctr[TR_CONGRATULATIONS_LONG]);
		
	allok = 1;
				
EXIT:
	fprintf(flog, "Install program ended.\n");	
	fflush(flog);
	fclose(flog);

	if (!(allok))
		newtWinMessage(ctr[TR_BASIC], ctr[TR_OK], ctr[TR_PRESS_OK_TO_REBOOT]);	
	
	newtFinished();
	
	freekeyvalues(ethernetkv);

	if (allok)
	{
		if (system("/bin/chroot /harddisk /usr/sbin/setup /dev/tty2 firstInstall"))
			printf("Unable to run setup.\n");
	}
	
	return 0;
}

static int partitiondisk(char *diskdevnode)
{
	int c = 0;
	int start = 1; int end = 0;
	char commandstring[STRING_SIZE];
	
	// Be sure the partition table is cleared.
	memset(commandstring, 0, STRING_SIZE);
	snprintf(commandstring, STRING_SIZE, "/bin/dd if=/dev/zero of=%s bs=1024 count=1", diskdevnode);
	mysystem(commandstring);
	usleep(500000);
	memset(commandstring, 0, STRING_SIZE);
	snprintf(commandstring, STRING_SIZE, "/bin/echo \"change\" > /sys/block/%s/uevent", diskdevnode+5);
	mysystem(commandstring);
	
	// Wait for udev to handle the deleted partitions, if any
	memset(commandstring, 0, STRING_SIZE);
	snprintf(commandstring, STRING_SIZE, "/sbin/udevadm settle");
	mysystem(commandstring);

	// Now partition in one swell foop.
	memset(commandstring, 0, STRING_SIZE);
	snprintf(commandstring, STRING_SIZE, "/usr/sbin/parted %s </tmp/partitions", diskdevnode);
	if (runcommandwithstatus(commandstring, ctr[TR_PARTITIONING_DISK]))
	{
		return 1;
	}
	usleep(500000);
	
	// Wait for udev to handle the new partitions
	memset(commandstring, 0, STRING_SIZE);
	snprintf(commandstring, STRING_SIZE, "/bin/echo \"change\" > /sys/block/%s/uevent", diskdevnode+5);
	mysystem(commandstring);
	memset(commandstring, 0, STRING_SIZE);
	snprintf(commandstring, STRING_SIZE, "/sbin/udevadm settle");
	mysystem(commandstring);
	
	return 0;
}
