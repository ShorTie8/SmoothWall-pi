/* SmoothWall setup program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * filename: main.c
 * Contains main entry point, and misc functions. */

#include "setup.h"

FILE *flog = NULL;
char *logname;

char **ctr = NULL;

int automode = 0;
int usbfail = 0;
int rebootrequired = 0;
int performedrestore = 0;

extern char *english_tr[];

int main(int argc, char *argv[])
{
	int choice;
	char *sections[14]; /* need to fill this out AFTER knowing lang */
	int rc;
	struct keyvalue *kv;
	char selectedshortlang[STRING_SIZE] = "en";
	int autook = 0;
	int doreboot = 0;
	struct stat statbuf;
	
	memset(&statbuf, 0, sizeof(struct stat));
			
	/* Log file/terminal stuff. */
	if (argc >= 2)
		logname = argv[1];	
	else
		logname = strdup("/root/setup.log");

	if (!(flog = fopen(logname, "w+")))
	{
		printf("Couldn't open log terminal\n");
		return 1;
	}
	
	/* Engage auto operation (run through 'normal' selections automatically) */
	if (argc >= 3)
	{
		if (strlen(argv[2]) == 12 && strncmp(argv[2], "firstInstall", 12) == 0)
		{
			/* This execution only follows the installer; outgoing rules are cleared */
			automode = 1;
		}
		else if (strlen(argv[2]) == 15 && strncmp(argv[2], "networkingOnly", 15) == 0)
		{
			/* This execution only runs during bootup when the NICs have changed */
			automode = 2;
		}
		else
		{
			/* All other values mean generic auto mode during normal operation */
			automode = 3;
		}
	}
	
	fprintf(flog, "Setup program started.\n");

	kv = initkeyvalues();
	if (!(readkeyvalues(kv, CONFIG_ROOT "main/settings")))
	{
		printf("Smoothwall is not properly installed.\n");
		return 1;
	}
	findkey(kv, "LANGUAGE", selectedshortlang);
	
	ctr = english_tr; 
	
	newtInit();
	newtCls();

	newtDrawRootText(0, 0, TITLE " -- http://smoothwall.org/");
	newtPushHelpLine(ctr[TR_HELPLINE]);		

	if (automode == 0)
	{
		/* Admin selects each menu item individually */
		sections[0] = ctr[TR_RESTORE_CONFIGURATION];
		sections[1] = ctr[TR_KEYBOARD_MAPPING];
		sections[2] = ctr[TR_TIMEZONE];
		sections[3] = ctr[TR_HOSTNAME];
		sections[4] = ctr[TR_WEB_PROXY];
		sections[5] = ctr[TR_DEFAULT_SECURITY_LEVEL];
		sections[6] = ctr[TR_ISDN_CONFIGURATION];
		sections[7] = ctr[TR_ADSL_CONFIGURATION];
		sections[8] = ctr[TR_NETWORKING];	
		sections[9] = ctr[TR_DHCP_SERVER_CONFIGURATION],
		sections[10] = ctr[TR_ROOT_PASSWORD];
		sections[11] = ctr[TR_SETUP_PASSWORD];
		sections[12] = ctr[TR_ADMIN_PASSWORD];
		sections[13] = NULL;	
	
		usbfail = 1;
		if (!stat("/proc/bus/usb/devices", &statbuf))
			usbfail = 0;
			
		if (usbfail)
			fprintf(flog, "USB HCI not detected.\n");
		else
			fprintf(flog, "USB HCI detected.\n");		
			
		choice = 0;
		for (;;)
		{
			rc = newtWinMenu(ctr[TR_SECTION_MENU],
				ctr[TR_SELECT_THE_ITEM], 50, 5, 5, 8,
				sections, &choice, ctr[TR_OK], ctr[TR_QUIT], NULL);
			
			if (rc == 2)
				break;
			
			switch (choice)
			{
				case 0:
					handlerestore();
					break;

				case 1:
					handlekeymap();
					break;
				
				case 2:
					handletimezone();
					break;
				
				case 3:
					handlehostname();
					break;

				case 4:
					handlewebproxy();
					break;
					
				case 5:
					handledefaults();
					break;

				case 6:
					handleisdn();
					break;

				case 7:
					handleadsl();
					break;
				
				case 8:
					handlenetworking();
					break;
					
				case 9:
					handledhcp();
					break;
									
				case 10:
					handlerootpassword();
					break;

				case 11:
					handlesetuppassword();
					break;
					
				case 12:
					handleadminpassword();
					break;
		
				default:
					break;
			}
		}
	}
	else if (automode == 2)
	{
		/* Admin specified networkingOnly as the third arg */
		/* This happens when the NIC change and rc.sysint runs setup */
		handlenetworking();
		autook = 2;
	}
	else
	{
		/* automode is 1 (firstInstall) or 3 (generic) */
		usbfail = 1;
				
		if (newtWinChoice(ctr[TR_RESTORE_CONFIGURATION], ctr[TR_NO], ctr[TR_YES],
			ctr[TR_RESTORE_LONG]) != 1)
		{
			if (!(handlerestore()))
				goto EXIT;
		}
	
		if (!(handlekeymap()))
			goto EXIT;
		if (!(handletimezone()))
			goto EXIT;
		if (!(handlehostname()))
			goto EXIT;
		if (!(handledefaults()))
			goto EXIT;
		if (!(handlenetworking()))
			goto EXIT;

		if (!performedrestore)
		{
			choice = 0;
			
			for (;;)
			{		
				sections[0] = ctr[TR_WEB_PROXY];
				sections[1] = ctr[TR_ISDN_CONFIGURATION];
				sections[2] = ctr[TR_ADSL_CONFIGURATION];
				sections[3] = ctr[TR_DHCP_SERVER_CONFIGURATION],
				sections[4] = NULL;	
	
				rc = newtWinMenu(ctr[TR_SECTION_MENU],
					ctr[TR_SELECT_THE_ITEM], 50, 5, 5, 8,
					sections, &choice, ctr[TR_OK], ctr[TR_FINISHED], NULL);
				
				if (rc == 2)
					break;
				
				switch (choice)
				{
					case 0:
						handlewebproxy();
						break;
						
					case 1:
						handleisdn();
						break;
	
					case 2:
						handleadsl();
						break;
											
					case 3:
						handledhcp();
						break;
	
					default:
						break;
				}
			}
		}	

		if (!(handleadminpassword()))
			goto EXIT;
		if (!(handlerootpassword()))
			goto EXIT;
	
		autook = 1;
	}

EXIT:	
	if (automode == 1 || automode == 3)
	{
		if (autook)
			newtWinMessage("", ctr[TR_OK], ctr[TR_SETUP_FINISHED]);
		else
			newtWinMessage(ctr[TR_WARNING], ctr[TR_OK], ctr[TR_SETUP_NOT_COMPLETE]);
	}
	else if (automode == 2)
	{
		if (autook == 2)
		{
			fprintf(flog, "Setup program ended.\n");
			fflush(flog);
			fclose(flog);
			newtFinished();
			return 0;
		}
		else
		{
			return -1;
		}
	}
	else
	{
		if (rebootrequired)
		{
			if (newtWinChoice("", ctr[TR_YES], ctr[TR_NO],
				ctr[TR_DO_YOU_WANT_TO_REBOOT]) != 2)
			{
				doreboot = 1;
			}
		} 
	}

	fprintf(flog, "Setup program ended.\n");
	fflush(flog);
	fclose(flog);
		
	newtFinished();

 	if (doreboot)
		system("/sbin/shutdown -r now");

	return 0;
}

