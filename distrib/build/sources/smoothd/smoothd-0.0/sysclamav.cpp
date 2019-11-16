/* SysIM Module for the SmoothWall SUIDaemon                              */
/* Contains functions relating to the management of the P3Scan            */
/* (c) 2005 SmoothWall Ltd                                                */
/* ---------------------------------------------------------------------- */
/* Original Author : D.K.Taylor                                           */

/* include the usual headers.  iostream gives access to stderr (cerr)     */
/* module.h includes vectors and strings which are important              */
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <fcntl.h>
#include <syslog.h>
#include <signal.h>

#include "module.h"
#include "ipbatch.h"
#include "setuid.h"

extern "C" {
	int load(std::vector<CommandFunctionPair> & );

	int restart_clamav(std::vector<std::string> & parameters, std::string & response);
	int   start_clamav(std::vector<std::string> & parameters, std::string & response);
	int    stop_clamav(std::vector<std::string> & parameters, std::string & response);
	int      freshclam(std::vector<std::string> & parameters, std::string & response);
}

int load(std::vector<CommandFunctionPair> & pairs)
{
	/* CommandFunctionPair name("command", "function"); */
	CommandFunctionPair restart_clamav_function("clamavrestart",  "restart_clamav", 0, 0);
	CommandFunctionPair   start_clamav_function("clamavstart",      "start_clamav", 0, 0);
	CommandFunctionPair    stop_clamav_function("clamavstop",        "stop_clamav", 0, 0);
	CommandFunctionPair      freshclam_function("clamavfreshclam",     "freshclam", 0, 0);

	pairs.push_back(restart_clamav_function);
	pairs.push_back(  start_clamav_function);
	pairs.push_back(   stop_clamav_function);
	pairs.push_back(     freshclam_function);

	return 0;
}

int restart_clamav(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;

	error += stop_clamav(parameters, response);
	if (error)
	{
		response = "Restart: " + response;
		return error;
	}

	error = start_clamav(parameters, response);
	response = "Restart: " + response;

	// Not needing ClamAV is still success
	if (error == 1) error = 0;

	return error;
}


int stop_clamav(std::vector<std::string> & parameters, std::string & response)
{	
	response = "ClamAV Daemon Stopped";

	return (killunknownprocess("clamd"));
}

int start_clamav(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	int needed;
	std::ostringstream num2str;

	needed = simplesecuresysteml("/bin/egrep", "-i", "=on$", "/var/smoothwall/clamav/settings", NULL);

	// If the execve() fails, it returns -1, which turns into 255 by the
	//   time it gets here.
	if (needed == 255)
	{
		fprintf(stderr, "ClamAV Start Failed: /bin/egrep not found\n");
		response = "ClamAV Start Failed: /bin/egrep not found!";
		return (-1);
	}

	else if (needed == 2)
	{
		fprintf(stderr, "ClamAV Start Failed: egrep failed\n");
		response = "ClamAV Start Failed: egrep failed!";
		return (-1);
	}

	else if (needed == 1)
	{
		response = "ClamAV not needed";
		return needed;
	}

	else if (needed == 0)
	{
		error = simplesecuresysteml("/usr/sbin/clamd", "--config-file=/usr/lib/smoothwall/clamd.conf", NULL);

		if (error)
			response = "ClamAV Daemon Failed! Check /var/log/smoothderror; run freshclam.";
		else
			response = "ClamAV Daemon Started";
		return error;
	}
	else {
		num2str << needed;
		response = "ClamAV Not Started: grep returned " + num2str.str();
		return needed;
	}
}

int freshclam(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	int needed;
	std::ostringstream num2str;

	error = simplesecuresysteml("/usr/bin/freshclam", NULL);
fprintf(stderr, "freshclam return code %d\n", error);

	// If the execve() fails, it returns -1, which turns into 255 by the
	//   time it gets here.
	if (error == 255)
	{
		fprintf(stderr, "Freshclam Failed: /usr/bin/freshclam not found\n");
		response = "Freshclam Failed: /usr/bin/freshclam not found!";
		return (-1);
	}
	else if (error == 0)
	{
		response = "ClamAV Virus Database Updated";
		return (0);
	}
	else if (error == 1)
	{
		response = "ClamAV Virus Database Already Up-To-Date";
		return (0);
	}
	else
	{
		fprintf(stderr, "ClamAV Virus Database Update Failed: return code %d\n", error);
		num2str << error;
		response = "ClamAV Virus Database Update Failed: return code " + num2str.str() + "!";
		return (-1);
	}

}
