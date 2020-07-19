/* SysSshd Module for the SmoothWall SUIDaemon                           */
/* Contains functions relating to starting/restarting sshd                  */
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
#include <sstream>
#include <cstdio>
#include <fcntl.h>
#include <syslog.h>
#include <signal.h>

#include "module.h"
#include "ipbatch.h"
#include "setuid.h"

extern "C" {
	int load(std::vector<CommandFunctionPair> & );
	int restart_sshd(std::vector<std::string> & parameters, std::string & response);
	int start_sshd(std::vector<std::string> & parameters, std::string & response);
	int stop_sshd(std::vector<std::string> & parameters, std::string & response);
}

int load(std::vector<CommandFunctionPair> & pairs)
{
	/* CommandFunctionPair name("command", "function"); */
	CommandFunctionPair restart_sshd_function("sshdrestart", "restart_sshd", 0, 0);
	CommandFunctionPair start_sshd_function("sshdstart", "start_sshd", 0, 0);
	CommandFunctionPair stop_sshd_function("sshdstop", "stop_sshd", 0, 0);

	pairs.push_back(restart_sshd_function);
	pairs.push_back(start_sshd_function);
	pairs.push_back(stop_sshd_function);

	return 0;
}

int restart_sshd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	
	error = stop_sshd(parameters, response);
	
	if (!error)
	{
		error = start_sshd(parameters, response);
		if (!error)
		{
			response = "Remote Access restarted.";
			return (0);
		}
	}
	
	if (error)
	{
		response += "\nRemote Access restart failed.";
		std::cerr << "Remote access restart errors:\n" << response << "\n";
	}
	
	return error;
}

int stop_sshd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;

	killprocess("/var/run/sshd.pid");
	usleep(100000);
	response = "Sshd Process Terminated";

	return (0);
}


int start_sshd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
        std::vector<std::string>ipbfilter;

	ConfigVAR settings("/var/smoothwall/remote/settings");
	ConfigVAR ethernetsettings("/var/smoothwall/ethernet/settings");
	
	// Remove existing allows, if any
        ipbfilter.push_back("/sbin/iptables -t filter -F restrict_remote");

	// Insert allows as needed, and start the daemon
	// GREEN, as it's configured
	if (settings["ENABLE_SSH_GREEN"] == "on")
	{
        	ipbfilter.push_back("/sbin/iptables -t filter -A restrict_remote -i " + ethernetsettings["GREEN_DEV"] + " -p tcp -m tcp --dport 222 -j RETURN");
	}
	if (settings["ENABLE_HTTP_GREEN"] == "on")
	{
        	ipbfilter.push_back("/sbin/iptables -t filter -A restrict_remote -i " + ethernetsettings["GREEN_DEV"] + " -p tcp -m tcp --dport 81 -j RETURN");
	}
	if (settings["ENABLE_HTTPS_GREEN"] == "on")
	{
        	ipbfilter.push_back("/sbin/iptables -t filter -A restrict_remote -i " + ethernetsettings["GREEN_DEV"] + " -p tcp -m tcp --dport 441 -j RETURN");
	}

	// PURPLE, as it's configured
	if (ethernetsettings["PURPLE_DEV"] != ""
	 && settings["ENABLE_SSH_PURPLE"] == "on")
	{
        	ipbfilter.push_back("/sbin/iptables -t filter -A restrict_remote -i " + ethernetsettings["PURPLE_DEV"] + " -p tcp -m tcp --dport 222 -j RETURN");
	}
	if (settings["ENABLE_HTTP_PURPLE"] == "on")
	{
        	ipbfilter.push_back("/sbin/iptables -t filter -A restrict_remote -i " + ethernetsettings["PURPLE_DEV"] + " -p tcp -m tcp --dport 81 -j RETURN");
	}
	if (settings["ENABLE_HTTPS_PURPLE"] == "on")
	{
        	ipbfilter.push_back("/sbin/iptables -t filter -A restrict_remote -i " + ethernetsettings["PURPLE_DEV"] + " -p tcp -m tcp --dport 441 -j RETURN");
	}

	// Close with the default REJECT
        ipbfilter.push_back("/sbin/iptables -t filter -A restrict_remote -j LOG --log-prefix \"Denied-by-filter:rstr_rem \"");
        ipbfilter.push_back("/sbin/iptables -t filter -A restrict_remote -j REJECT --reject-with icmp-port-unreachable");

	// Debug
        //for (int i = 0; i < ipbfilter.size(); i++) {
	//	std::cerr << "sysssh debug ipbfilter" << ipbfilter[i] << "\n";
        //}

	// And set up iptables
	error = ipbatch(ipbfilter);
	if (error)
	{
		response += "\nCan't prepare chain restrict_remote.";
		return (error);
	}

	// Restart daemon if needed
	if (settings["ENABLE_SSH_GREEN"] == "on"
	 || settings["ENABLE_SSH_PURPLE"] == "on")
	{
		// Start SSH daemon
		error = simplesecuresysteml("/usr/sbin/sshd", NULL);
		if (error)
		{
			response += "\nCan't start sshd";
		}
	}

	return (error);
}
