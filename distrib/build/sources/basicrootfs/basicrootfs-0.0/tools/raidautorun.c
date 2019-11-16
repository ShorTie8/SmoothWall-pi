/* Copyright 2005-2010 SmoothWall Ltd
 *
 * SmoothWall helper program - raidautorun.
 *
 * filename: raidautorun.c
 * Starts the raid device on /dev/md0, as needed by the initrd. */

#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>
#define MD_MAJOR 9
#include <linux/raid/md_u.h>

int main(int argc, char *argv[])
{
	/* /dev/md0 must exist. */
	int fd = open("/dev/md0", O_RDWR, 0);
	
	if (!fd)
	{
		perror("Failed to open /dev/md0");
		return 1;
	}
	
	if (ioctl(fd, RAID_AUTORUN, 0))
	{
		perror("Couldn't start RAID");
		return 1;
	}
	
	close(fd);

	printf("RAID started\n");
	
	return 0;
}
