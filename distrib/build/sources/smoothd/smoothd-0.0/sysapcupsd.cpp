/* Apcupsd Module for the SmoothWall SUIDaemon                            */
/* Contains functions relating to the management of the apcupsd           */
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
#include <fcntl.h>
#include <syslog.h>
#include <signal.h>

#include "module.h"
#include "ipbatch.h"
#include "setuid.h"

extern "C" {
   int load(std::vector<CommandFunctionPair> & );

   int restart_apcupsd(std::vector<std::string> & parameters, std::string & response);
   int   start_apcupsd(std::vector<std::string> & parameters, std::string & response);
   int    stop_apcupsd(std::vector<std::string> & parameters, std::string & response);
   int   write_apcupsd(std::vector<std::string> & parameters, std::string & response);
}

int load(std::vector<CommandFunctionPair> & pairs) {
   /* CommandFunctionPair name("command", "function"); */
   CommandFunctionPair restart_apcupsd_function( "apcupsdrestart", "restart_apcupsd", 0, 0 );
   CommandFunctionPair   start_apcupsd_function( "apcupsdstart",     "start_apcupsd", 0, 0 );
   CommandFunctionPair    stop_apcupsd_function( "apcupsdstop",       "stop_apcupsd", 0, 0 );
   CommandFunctionPair   write_apcupsd_function( "apcupsdwrite",     "write_apcupsd", 0, 0 );

   pairs.push_back( restart_apcupsd_function );
   pairs.push_back(   start_apcupsd_function );
   pairs.push_back(    stop_apcupsd_function );
   pairs.push_back(   write_apcupsd_function );

   return 0;
}

int restart_apcupsd(std::vector<std::string> & parameters, std::string & response) {
   int error = 0;
   
   error += stop_apcupsd( parameters, response );

   if ( !error )
      error += start_apcupsd( parameters, response );
   
   if ( !error )
      response = "APCupsd restart successful";

   return error;
}
   

int stop_apcupsd(std::vector<std::string> & parameters, std::string & response) {

   killprocess("/var/run/apcupsd.pid");
   sleep(2);
   response = "APCupsd process terminated";
   unlink("/var/run/apcupsd.pid");

   return 0;
}
   
int start_apcupsd(std::vector<std::string> & parameters, std::string & response) {
   int error = 0;

   ConfigVAR settings("/var/smoothwall/apcupsd/settings");
   if (settings["ENABLE"] == "on")
      {
      error = simplesecuresysteml("/sbin/apcupsd", NULL);

      response = "APCupsd process started";

      if (error) {
         response = "APCupsd Start Failed!";
      } else {
         response = "APCupsd Start Successful";
      }
   }
   return error;
}

int write_apcupsd(std::vector<std::string> & parameters, std::string & response) {
   int error = 0;

      {
      error = simplesecuresysteml("/usr/bin/smoothwall/writeapcupsdconf.pl", NULL);

      if (error) {
         response = "apcupsd.conf write FAILED!";
      } else {
         response = "apcupsd.conf written";
      }
   }
   return error;
}
