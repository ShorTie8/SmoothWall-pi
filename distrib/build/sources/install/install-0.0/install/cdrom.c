/* SmoothWall install program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * filename: cdrom.c
 * CDROM menu. Get "misc" driver name etc. */

#include <errno.h>
#include "install.h"

extern FILE *flog;
extern char *logname;

extern char **ctr;

/* Ejects the CDROM.  returns 0 for failure, 1 for success. */
int ejectcdrom(char *dev)
{
	int fd;
	char msgstring[STRING_SIZE];

	if ((fd = open(dev, O_RDONLY|O_NONBLOCK)) == -1)
		return 0;
	
	/* At some point, the kernel/umount stopped unlocking the drive, which
	 * affects the eject ioctl as well as the physical button. */
	if (ioctl(fd, CDROM_LOCKDOOR, 0) == -1)
	{
		close(fd);
		snprintf(msgstring, STRING_SIZE, "Cannot unlock CD drive: errno=%d\n", errno);
		fprintf(flog, msgstring);
		return 0;
	}
	
	// Now eject
	if (ioctl(fd, CDROMEJECT) == -1)
	{
		close(fd);
		snprintf(msgstring, STRING_SIZE, "Cannot eject CD drive: errno=%d\n", errno);
		fprintf(flog, msgstring);
		return 0;
	}
	close(fd);
	
	return 1;
}	
