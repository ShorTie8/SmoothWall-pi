/* SmoothWall install program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 * 
 * filename: config.c
 * Write the config and get password stuff. */

#include <pwd.h>

#include "install.h"

extern FILE *flog;
extern char *logname;

extern char **ctr;

/* called to write out all config files using the keyvalue interface. */
int writeconfigs(struct blockdevice *hd, struct keyvalue *ethernetkv, char *lang)
{
	char devnode[STRING_SIZE];
	int ignore;
	struct keyvalue *kv = initkeyvalues();
	struct passwd *pwd;
	
	/* Write out the network settings we got from a few mins ago. */
	writekeyvalues(ethernetkv, "/harddisk" CONFIG_ROOT "ethernet/settings");
	
	/* default stuff for main/settings. */
	replacekeyvalue(kv, "LANGUAGE", lang);
	replacekeyvalue(kv, "HOSTNAME", "smoothwall");
	writekeyvalues(kv, "/harddisk" CONFIG_ROOT "main/settings");
	freekeyvalues(kv);
	if (pwd = getpwnam("nobody"))
	{
		/* Has to work, so ignore return vals */
		ignore = chmod ("/harddisk" CONFIG_ROOT "main/settings", S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH);
		ignore = chown ("/harddisk" CONFIG_ROOT "main/settings", pwd->pw_uid, pwd->pw_gid);
	}

	return 1;
}
