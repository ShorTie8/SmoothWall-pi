/* SysUpnpd Module for the SmoothWall SUIDaemon                           */
/* Contains functions relating to starting/restarting upnpd                  */
/* (c) 2007 SmoothWall Ltd                                                */
/* ----------------------------------------------------------------------  */
/* Original Author  : Lawrence Manning                                     */
/* Translated to C++: M. W. Houston                                        */

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
	int load(std::vector<CommandFunctionPair> &  );
	int restart_upnpd(std::vector<std::string> & parameters, std::string & response );
	int start_upnpd(std::vector<std::string> & parameters, std::string & response );
	int stop_upnpd(std::vector<std::string> & parameters, std::string & response );
	int write_upnpd(std::vector<std::string> & parameters, std::string & response );
}

int load(std::vector<CommandFunctionPair> & pairs )
{
	/* CommandFunctionPair name("command", "function" ); */
	CommandFunctionPair restart_upnpd_function("upnpdrestart", "restart_upnpd", 0, 0);
	CommandFunctionPair start_upnpd_function("upnpdstart", "start_upnpd", 0, 0);
	CommandFunctionPair stop_upnpd_function("upnpdstop", "stop_upnpd", 0, 0);
	CommandFunctionPair write_upnpd_function("upnpdwrite", "write_upnpd", 0, 0);

	pairs.push_back(restart_upnpd_function);
	pairs.push_back(start_upnpd_function);
	pairs.push_back(stop_upnpd_function);
	pairs.push_back(write_upnpd_function);

	return 0;
}

int restart_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	
	error += stop_upnpd(parameters, response);
	
	if (!error)
		error += start_upnpd(parameters, response);
	
	if (!error)
		response = "Upnpd Restart Successful";
	
	return error;
}

int stop_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	
	killprocess("/var/run/miniupnpd.pid");

	response = "Miniupnpd process terminated";

	return error;
}

int start_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;

	ConfigVAR settings("/var/smoothwall/advnet/settings");

	// Do nothing if not enabled
	if (settings["ENABLE_UPNP"] != "on")
	{
		return error;
	}

	// If RED is not active, UPnP won't work anyway
	ConfigSTR iface("/var/smoothwall/red/iface");
	if (iface.str() == "")
	{
		return error;
	}

	// We're here; run it

	ConfigSTR uuid("/etc/miniupnpd.uuid");
	std::vector<std::string> args;
	ConfigVAR netsettings("/var/smoothwall/ethernet/settings");
	ConfigVAR ownershipsettings("/var/smoothwall/main/ownership");
	ConfigVAR productdatasettings("/var/smoothwall/main/productdata");

	// Write the config
	args.push_back("/usr/bin/smoothwall/writeupnp");
	error = simplesecuresystemvector(args);
	if (error)
	{
		response = "Can't write miniupnpd.conf; won't start daemon";
		return error;
	}
	args.clear();

	// Start the daemon
	args.push_back("/usr/sbin/miniupnpd");
	args.push_back("-f");
	args.push_back("/etc/miniupnpd.conf");

	error = simplesecuresystemvector(args);
	if (error)
		response = "Can't start miniupnpd";
	else
		response = "Miniupnpd start successful";
	return error;
}

int write_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	std::vector<std::string> args;

	// Write the config
	args.push_back("/usr/bin/smoothwall/writeupnp");
	error = simplesecuresystemvector(args);
	if (error)
	{
		response = "Can't write miniupnpd.conf";
	}
	return error;
}
