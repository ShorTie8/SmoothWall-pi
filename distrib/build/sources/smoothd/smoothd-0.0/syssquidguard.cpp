/* Syssquidguard Module for the SmoothWall SUIDaemon                           */
/* (c) 2007 SmoothWall Ltd                                                */
/* ----------------------------------------------------------------------  */
/* Original Author  : Lawrence Manning                                     */
/* Portions (c) Stanford Prescott                                        */

/* include the usual headers.  iostream gives access to stderr (cerr)     */
/* module.h includes vectors and strings which are important              */
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <fcntl.h>
#include <syslog.h>
#include <signal.h>

#include "module.h"
#include "setuid.h"

extern "C" {
	int load( std::vector<CommandFunctionPair> &  );
	int sg_prebuild(std::vector<std::string> & parameters, std::string & response);
	int errrpt(const std::string & parameter);
	int sg_autoupdate(std::vector<std::string> & parameters, std::string & response);
}

int load( std::vector<CommandFunctionPair> & pairs )
{
	/* CommandFunctionPair name( "command", "function" ); */
	CommandFunctionPair sg_prebuild_function("sgprebuild", "sg_prebuild", 0, 0);
	CommandFunctionPair sg_autoupdate_function("sgautoupdate", "sg_autoupdate", 0, 0);

	pairs.push_back(sg_prebuild_function);
	pairs.push_back(sg_autoupdate_function);

	return 0;
}

int sg_prebuild(std::vector<std::string> & parameters, std::string & response)
{
   int error = 0;
   response = "squidGuard: updating blacklists.";
   error = simplesecuresysteml("/usr/bin/smoothwall/prebuild.pl", NULL);

   if (!error)
     response = "squidGuard: blacklists updated.";
   else
     response = "squidGuard: unable to update blacklists!";
	
   return errrpt (response);
}

int sg_autoupdate(std::vector<std::string> & parameters, std::string & response)
{
   int error = 0;

   ConfigVAR settings("/var/smoothwall/urlfilter/autoupdate/autoupdate.conf");

   std::string updpath = "/usr/bin/smoothwall/sgbl-autoupdate";
   std::string url = "";

   FILE *exists;
   FILE *updfile;

   // No need to check for existence; '-f' says to feign success if it isn't there.
   // unlink() would be more efficient, but that doesn't matter in this case.
   error = simplesecuresysteml("/bin/rm", "-f", "/etc/cron.daily/sgbl-autoupdate", NULL);
   error = simplesecuresysteml("/bin/rm", "-f", "/etc/cron.weekly/sgbl-autoupdate", NULL);
   error = simplesecuresysteml("/bin/rm", "-f", "/etc/cron.monthly/sgbl-autoupdate", NULL);

   if ( settings["ENABLE_AUTOUPDATE"] == "on" )
   {
     // Check/vet the value; only these three can be used.
     if ((settings["UPDATE_SCHEDULE"] == "daily") ||
        (settings["UPDATE_SCHEDULE"] == "weekly") ||
        (settings["UPDATE_SCHEDULE"] == "monthly"))
     {
       // Prep the link name and make a symlink.
       std::string tmpFileName = "/etc/cron." + settings["UPDATE_SCHEDULE"] + "/sgbl-autoupdate";
       error = simplesecuresysteml("/bin/ln", "-s", updpath.c_str(), tmpFileName.c_str(), NULL);
     }
   }

   if (!error)
     response = "squidGuard: Success setting up autoupdate.";
   else
     response = "squidGuard: Unable to setup autoupdate.";
	
  return errrpt (response);
}

int errrpt(const std::string & logdata)
{
 int err = 0;

 syslog(LOG_INFO, "squidGuard:  %s", logdata.c_str());

 return err;
}
