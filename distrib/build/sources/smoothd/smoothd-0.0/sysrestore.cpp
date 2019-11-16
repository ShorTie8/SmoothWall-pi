/* Simple Settings Restore Module for the SmoothWall SUIDaemon            */
/* For setting the system time                                            */
/* (c) 2007 SmoothWall Ltd                                                */
/* ---------------------------------------------------------------------- */
/* Original Author  : Lawrence Manning                                    */
/* Translated to C++: M. W. Houston                                       */

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
#include "ipbatch.h"
#include "setuid.h"

extern "C" {
	int load(std::vector<CommandFunctionPair> & );
	int restore_settings(std::vector<std::string> & parameters, std::string & response);
}

int load(std::vector<CommandFunctionPair> & pairs)
{
	/* CommandFunctionPair name("command", "function"); */
	CommandFunctionPair restore_settings_function("restoresettings", "restore_settings", 0, 0);
	
	pairs.push_back(restore_settings_function);

	return (0);
}

int restore_settings(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;

	std::vector<std::string> cmd;
	std::string::size_type n;
	
	cmd.push_back("/etc/rc.d/restorescript");

	error = simplesecuresystemvector(cmd);

	if (error)
		response = "restore settings failed";
	else
		response = "Simple settings restored; reboot the system now.";

EXIT:
	return error;
}
