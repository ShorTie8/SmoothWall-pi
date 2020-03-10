/* SysXtAccess Module for the SmoothWall SUIDaemon                              */
/* Contains functions relating to external Access                               */
/* (c) 2007 SmoothWall Ltd                                                      */
/* ============================================================================ */
/* Original Author  : Daniel Goscomb                                            */
/* Translated to C++: M. W. Houston                                             */
/*                                                                              */
/* include the usual headers.  iostream gives access to stderr (cerr)           */
/* module.h includes vectors and strings which are important                    */
/* ============================================================================ */
/* Modifications for Full Firewall Control by Stanford Prescott MD              */
/* ============================================================================ */
/* Combined sysportfw.cpp into this module for Full Firewall Control because    */
/* some changes will be needed here, to support FFC.                            */
/*                                          09/04/25         --Steven L Pittman */
/* **************************************************************************** */
/*         Comments for sysportfw.cpp                                           */
/* ============================================================================ */
/* include the usual headers.  iostream gives access to stderr (cerr)           */
/* module.h includes vectors and strings which are important                    */
/*============================================================================= */
/* No original author listed --  Assume that Drew S DuPont and                  */
/*                                                       Toby Long Leather      */
/*  contributed to  02/24/2008 - Stanford Prescott MD                           */
/*  collection of routines to manipulate IPTables for                           */
/*  multiple IP interfaces and Full Firewall Control                            */
/*============================================================================= */
/* Modifications:  Steven L Pittman                     08/05/18          --slp */
/*  Heavy modifications to streamline routines and reduce bulk                  */
/*  hopefully making the code easier to read.                                   */
/* ============================================================================ */
/* Modifications to improve speed and avoid the problems associated with        */
/* calls to ipbatch hanging when either there is too much execution time        */
/* or a counter overflows (the source of neither has been found)          --slp */
/* ============================================================================ */
/* Modifications to search in the vector and not add any duplicates to the      */
/* iptables rules                                          08/06/06       --slp */
/* ============================================================================ */
/* Modifications to reestablish bouncing operations  IPTables would report      */
/* negated inputs, but will not use them in mangle  having the input in         */
/* mangle where MARK is established prevented it frome being used in nat        */
/* for any interpretation  The net result is that we now have a rule for each   */
/* internal interface with a unique mark and a rule for each mark for NAT --slp */
/* ============================================================================ */
/* Modifications to support masking outbounds to alias IPs.  Red interface      */
/* detection was reworked, and source IP was added to the DNAT rules for        */
/* differentiation.  We now throw an error if the DNAT is not logical.          */
/*                                                        08/06/16        --slp */
/* ============================================================================ */
/* Modification to SNAT for Aliases to accept individually in portfw_post       */
/*                                                       08/06/23         --slp */
/* ============================================================================ */
/* Modification to use MARK vice CONNMARK because of a conflict with QoS        */
/* Modifications to jump the proxies                                            */
/*                                                       08/06/25         --slp */
/* ============================================================================ */
/* Modification to portfwf to include the destination interface                 */
/* Modifications to test protocol before assuming it is a port forward          */
/*                                                        08/07/12        --slp */
/* ============================================================================ */
/* Modifications add "FFC Log:" information to the smoothd log for errors and   */
/* successes                                              08/09/01        --slp */
/* ============================================================================ */
/* Added source interface to the DNAT entry Added error check for non-matched   */
/* input interface/cop-out to default IP from /local-ip on forwards             */
/*                                                        08/09/16        --slp */
/* ============================================================================ */
/* Added check to alias settings to determine if the alias is enabled.          */
/* Changed the CONNMARK to use the upper twelve bits only, and share with       */
/* another CONNMARK user, if it is aware of and uses a mask to not disturb our  */
/* CONNMARKs. We continue to use MARKs without mask because of stock conflicts  */
/* Added code to allow negation of the source IP or MAC.  Added code to limit   */
/* source IPs on each of the three possible interfaces to their supposed        */
/* subnets, to avoid anal race conditions.  Removed portfw_b and portfw_pre     */
/* chains from legacy FFC, and use stock chains.  Set return values to zero     */
/* to make "response" a readable value by the caller.  Added a new chain,       */
/* portfwfi, for the INPUT chain, to block possible proxy bypasses of FFC       */
/* rules.  Added code to sysxtaccess.cpp  (Could not do alisup/dn internally.)  */
/*                                                        09/05/09        --slp */
/* ============================================================================ */
/* Changed the bouncing SNAT to only be applied to packets that are coming in   */
/* and going out of the same interface.  Bumped the version to 3.1.4 to avoid   */
/* confusion, since this is for SW 3.  Slight modification to the log prefix    */
/* for the subnet limiting rules.                                               */
/*                                                        09/09/05        --slp */
/* ============================================================================ */
/* Fix a logic issue for the portfwi rules. version 3.1.5                       */
/* target logic return for ACCEPT                         09/11/14        --slp */
/* ============================================================================ */
/* Fix a logic issue for the portfwi rules. version 3.1.6                       */
/* dport was not included in portfwi                      09/12/07        --slp */
/* ============================================================================ */
/* Fix a logic issue for the portfwi rules. version 3.1.8                       */
/* portfwi rules are generated for no output interface (Any) for discrete       */
/* control of the proxies                                 10/03/16        --slp */
/* ============================================================================ */
/* Changed all error responses to have the first word in the response to be     */
/* "Abort".  Moved the subnet check rule generator to a subfunction.  Changed   */
/* ifaliasup to create an up to date list of HOME_NET for snort (also correct   */
/* long standing error for DNS_SERVERS, meant to be local DNS servers) in       */
/* /var/smoothwall/portfw/snort.var                                             */
/* a few other syntax changes.     Version 3.2.0          10/03/31        --slp */
/* ============================================================================ */
/* Error in External Access.       Version 3.2.1          10/06/02        --slp */
/* ============================================================================ */
/* Allow DHCP to bypass the subnet checks. Version 3.2.2  10/06/25        --slp */
/* ============================================================================ */
/* ifaliasup check and update aliases      Version 3.3.0  10/08/18        --slp */
/* ============================================================================ */
/* add source IP to mask for VPN issue     Version 3.3.1  10/12/03        --slp */
/* ============================================================================ */
/* Add a check to avoid deleting non-existant rules in jmpsquid                 */
/* discontinue use of deprecated negation  Version 3.3.2  10/12/03        --slp */
/* ============================================================================ */
/* Rewrite of sysiptables.cpp to combine incoming outgoing and                  */
/* internal functions into one UI and config file. This required                */
/* the addition of the logic from the TOFC mod. Also added new timing,          */
/* IP Range and multiple port groupings using xtables modules.                  */
/* This version is for SWE 3.1              Version 3.4.1 13/03/15        --stp */
/* ============================================================================ */
/* Minor changes for formatting, added call to ifaliasdn in ifaliasup           */
/*                                          Version 3.4.1 13/07/07        --slp */
/* ============================================================================ */

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <algorithm>
#include <vector>

#include "module.h"
#include "ipbatch.h"
#include "setuid.h"

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <glob.h>
#include <syslog.h>
#include <signal.h>
#include <unistd.h>

#define LETTERS "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#define NUMBERS "0123456789"
#define HEX "0123456789abcdefgABCDEFG"
#define MAC_HEX ":" HEX
#define LETTERS_NUMBERS LETTERS NUMBERS
#define MULTI_PORTS "0123456789:-"
#define IP_RANGE IP_NUMBERS "-"
#define INTERFACE "ethipbondrwlau" NUMBERS
#define INTERFACE_ALIAS ":" INTERFACE

extern "C"
{
 int load(std::vector<CommandFunctionPair> & );

// Setup dummy calls to the stock functions
 int set_incoming(std::vector<std::string> & parameters, std::string       & response);
 int set_outgoing(std::vector<std::string> & parameters, std::string       & response);
 int set_internal(std::vector<std::string> & parameters, std::string       & response);

 int set_xtaccess(std::vector<std::string> & parameters, std::string       & response);
 int set_portfw(std::vector<std::string>   & parameters, std::string       & response);
 int ifaliasup(std::vector<std::string>    & parameters, std::string       & response);
 int ifaliasdown(std::vector<std::string>  & parameters, std::string       & response);
 int get_alias(std::vector<std::string>    & parameters);
 int rmdupes(std::vector<std::string>      & parameters, const std::string & newparm);
 int errrpt(const std::string              & parameter);
 int snet2cidr(const std::string           & parameters);
 int readether(std::vector<std::string>    & parameters, std::string       & target);
 int chkaliases(std::vector<std::string>   & parameters);
 int wrtaliases(std::string                & response);
 int wrtdefaults(std::string               & response);
 int genrpt(std::string                    & response);
 bool chkproxy();
 bool proxymod();
}

std::map<std::string, std::vector<std::string>, eqstr> portlist;

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int load_portlist()
{
 /* open the portlist file for reading */

 glob_t globbuf;

 memset(&globbuf, 0, sizeof(glob_t));

 glob("/var/smoothwall/knownports/*", GLOB_DOOFFS, NULL, &globbuf);

 for (size_t i = 0; i < globbuf.gl_pathc; i++)
 {
  std::ifstream input(globbuf.gl_pathv[i]);
  char buffer[2048];

  /* determine the filename */
  char *section = globbuf.gl_pathv[i] + strlen("/var/smoothwall/knownports/");
		
  if (!input) continue;

  while (input)
  {
   if (!input.getline(buffer, sizeof(buffer)))
    break;
	
   if (strlen(buffer) > 0)
   {
    char *name = buffer;
    char *value = strstr(name, ",");	

    if (value && *value)
    {
     *value = '\0';
     value++; 
    } 
    else
     value = name;

     std::vector<std::string> & vect = portlist[section];
     vect.push_back(value);
   }
  }
  input.close();
 }

 return 0;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int load(std::vector<CommandFunctionPair> & pairs)
{
 /*
 CommandFunctionPair name("command" for external smoothcom call,
          "function" internal name of the function,
          int user that is switched to during execution,
          int group that is switched to during execution,
          int version will supersede earlier .so versions);
 */

 int version = 311;

 CommandFunctionPair set_incoming_function ("setxtaccess","set_incoming",0,0,version);
 CommandFunctionPair set_outgoing_function ("setxtaccess","set_outgoing",0,0,version);
 CommandFunctionPair set_internal_function ("setxtaccess","set_internal",0,0,version);

 CommandFunctionPair set_xtaccess_function ("setxtaccess","set_xtaccess",0,0,version);
 CommandFunctionPair set_portfw_function   ("setportfw",    "set_portfw",0,0,version);
 CommandFunctionPair ifalias_down_function ("ifaliasdown", "ifaliasdown",0,0,version);
 CommandFunctionPair ifalias_up_function   ("ifaliasup",     "ifaliasup",0,0,version);
 CommandFunctionPair wrt_defaults_function ("wrtdefaults", "wrtdefaults",0,0,version);
 CommandFunctionPair gen_rpt_function      ("genrpt", "genrpt",0,0,version);

 pairs.push_back(set_incoming_function);
 pairs.push_back(set_outgoing_function);
 pairs.push_back(set_internal_function);

 pairs.push_back(set_xtaccess_function);
 pairs.push_back(set_portfw_function);
 pairs.push_back(ifalias_down_function);
 pairs.push_back(ifalias_up_function);
 pairs.push_back(wrt_defaults_function);
 pairs.push_back(gen_rpt_function);

 return 0;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int set_xtaccess(std::vector<std::string> & parameters, std::string & response)
{
 std::string ifacefile    = "/var/smoothwall/red/iface";
 std::string cmdprefix    = "/var/smoothwall/mods/fullfirewall";
 std::string configfile   = cmdprefix + "/xtaccess/config";
 std::string aliasfile    = cmdprefix + "/portfw/aliases";

 ConfigSTR ifacef(ifacefile);
 ConfigCSV config(configfile);
 ConfigCSV aliases(aliasfile);

 std::vector<std::string> ipb;
 std::string red_ip            = "";
 std::string iface             = ifacef.str();
 std::string destination       = "";
 std::string dport_out         = "";
 int error                     = 0;

 // preset the response to a success, changed only on error, always return zero

 response = "External Access Rules set";

 if (ifacef.str() == "")
 {
  response = "Abort, could not open red local interface file (" + ifacefile + ")";
  return errrpt (response);
 }
 if (iface.find_first_not_of(INTERFACE) != std::string::npos)
 {
  response = "Abort, bad interface: " + iface;
  return errrpt (response);
 }

 rmdupes(ipb, "iptables -t filter -F xtaccess");
 rmdupes(ipb, "iptables -t nat -F portfw_pre");

 //=============================================================================>
 // Any destination IP that is local and not forwarded goes to us through INPUT

 for (int line = config.first(); line == 0; line = config.next())
 {
  const std::string & alias    = config[0];
  const std::string & protocol = config[1];
  const std::string & remip    = config[2];
  const std::string & locport  = config[3];
  const std::string & enabled  = config[4];

  if (protocol.find_first_not_of(NUMBERS) != std::string::npos)
  {
   response = "Abort, bad protocol: " + protocol;
   return errrpt (response);
  }
  if (remip.find_first_not_of(IP_NUMBERS) != std::string::npos)
  {
   response = "Abort, bad remote IP: " + remip;
   return errrpt (response);
  }
  if (locport.find_first_not_of(NUMBERS_COLON) != std::string::npos)
  {
   response = "Abort, bad port: " + locport;
   return errrpt (response);
  }
  dport_out = "";
  if (locport !=  "0" && locport !=  "") dport_out = " --dport " + locport;

  red_ip = "";
  for (int aline = aliases.first(); aline == 0; aline = aliases.next())

  // we need to find the alias IP of the red interface
  {
   const std::string & f_ifalias = aliases[1];
   const std::string & f_ipaddress = aliases[3];

   if (alias == f_ifalias)
   {
    red_ip = f_ipaddress;
    break;
   }
  }
  if (red_ip == "")
  {
   response = "Abort, could not find an alias match in (" + configfile + ") with (" +
    aliasfile + ") for an IP in the XTAccess rule";
   return errrpt(response);
  }
  destination = " -d " + red_ip;

  //============================================================================>
  // This only creates the rules if they are present and enabled, the alias
  // may be disabled which would make the rule ineffective since the IP would
  // not be present in "ip addr"

  if (enabled == "on")
  {
   rmdupes(ipb, "iptables -t filter -A xtaccess -i " + iface + " -d " + red_ip + 
    " -p " + protocol + dport_out + " -s " + remip + " -j ACCEPT");
  }
 }

 error = ipbatch(ipb);

 if (error) response = "Abort in XtAccess while transferring rules to IPTables, via ipbatch.";

 return errrpt (response);
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int set_portfw(std::vector<std::string> & parameters, std::string & response)
{
 int error = 0;
 std::string::size_type n;
 std::string::size_type p;
 std::vector<std::string>ipb;

 std::string localipfile = "/var/smoothwall/red/local-ipaddress";
 std::string ifacefile = "/var/smoothwall/red/iface";
 std::string cmdprefix = "/var/smoothwall/mods/fullfirewall";
 std::string configfile = cmdprefix + "/portfw/config";
 std::string aliasfile = cmdprefix + "/portfw/aliases";
 std::string sncheckfile = cmdprefix + "/portfw/subcheck";
// std::string upnpfile = "/var/smoothwall/advnet/settings";
 std::string ifile;

 ConfigSTR   localip(localipfile);
 ConfigSTR   red_iface(ifacefile);
 ConfigCSV   fwdconf(configfile);
 ConfigCSV   aliases(aliasfile);
 ConfigVAR   subnetcheck(sncheckfile);
 ConfigVAR   settings("/var/smoothwall/mods/fullfirewall/portfw/settings");
 ConfigVAR   netsettings("/var/smoothwall/ethernet/settings");
 ConfigVAR   squidsettings("/var/smoothwall/proxy/settings");
 ConfigVAR   squidmodsettings("/var/smoothwall/mods/proxy/settings");

 std::string greencheck  = settings["GREEN"];
 std::string purplecheck = settings["PURPLE"];
 std::string orangecheck = settings["ORANGE"];

 // preset the response to a success, changed only on error, always return zero

 response = "Port forwarding rules set";

 if (localip.str() == "")
 {
  response = "Abort, could not open red local IP file (" + localipfile + ")";
  return errrpt (response);
 }
 if (localip.str().find_first_not_of(IP_NUMBERS) != std::string::npos)
 {
  response = "Abort, bad local IP: " + localip.str();
  return errrpt (response);
 }
 if (red_iface.str() == "")
 {
  response = "Abort, could not open red interface file (" + ifacefile + ")";
  return errrpt (response);
 }
 if (red_iface.str().find_first_not_of(INTERFACE) != std::string::npos)
 {
  response = "Abort, bad red interface specifier: " + red_iface.str();
  return errrpt (response);
 }
 std::string red_if      = red_iface.str();
 std::string fwdest_out  = "";
 std::string dest_out    = "";
 std::string ifc_in_out  = "";
 std::string ifc_out_out = "";
 std::string fwdportdest = "";
 std::string srcipmac_in = "";
 std::string srcipmac_out= "";
 std::string dport_out   = "";
 std::string fwdport_out = "";
 std::string dnat_out    = "";
 std::string in_dest     = "";
 bool bounce_type        = false;
 bool forwarding         = false;
 bool translating        = false;
 bool negated_source     = false;
 std::string temp_source = "";
 std::string internal_if = "";
 std::string conn_green  = "0xD0000000";
 std::string conn_purple = "0xE0000000";
 std::string conn_orange = "0xF0000000";
 std::string green_if    = "";
 std::string green_ifip  = "";
 std::string orange_if   = "";
 std::string orange_ifip = "";
 std::string purple_if   = "";
 std::string purple_ifip = "";

 unsigned int x;
 unsigned int y;
 unsigned int z;

 /*
 The mark_mask value can only be used if we switch to CONNMARK tracking
 std::string mark_mask   = "0xFFF00000/";
 //=============================================================================>
 // We use the upper three nybbles of the available CMARK sequence numbers for
 // identifying the CMARKs associated with Full Firewall Control.  Any other
 // applications using CMARKs must be aware of this, always using a CMARK mask
 // that is not greater than 0x000FFFFF.  Available only if we use CONNMARK
 //=============================================================================>
 */
 rmdupes (ipb, "iptables -t filter -F portfwf");  // filtering rules  (moved stk)
 rmdupes (ipb, "iptables -t nat -F portfw");      // DNAT forwarding        (stk)
 rmdupes (ipb, "iptables -t mangle -F portfwb");  // MARK bounce & OMask    (stk)
 rmdupes (ipb, "iptables -t nat -F portfw_post"); // SNAT bounce & OMask    (add)
 rmdupes (ipb, "iptables -t filter -F portfwi");  // filter rules for INPUT (add)
 rmdupes (ipb, "iptables -t filter -F subnetchk");// filter rules FOR/INPUT (add)

 std::string chainfwd2Int = "iptables -A tofcfwd2Int";
 std::string chainfwd2Ext = "iptables -A tofcfwd2Ext";
 std::string chainproxy = "iptables -A tofcproxy";

 rmdupes(ipb, "iptables -F tofcfwd2Ext");
 rmdupes(ipb, "iptables -F tofcfwd2Int");
 rmdupes(ipb, "iptables -F tofcproxy");
 rmdupes(ipb, "iptables -F tofcblock");

 rmdupes(ipb, "iptables -F dmzholes");

 // ============================================================================>
 // we allow masking outbound to a red alias by having an association in
 // the alias file between a single internal IP and the alias interface
 // ============================================================================>
 // Here we find the internal interfaces for possible bouncing and create the
 // rules for masking outbounds to alias interfaces as we read the alias file

 unsigned int mark_seq = 0x800;

 for (int line = aliases.first(); line == 0; line = aliases.next())
 {
  char conn_mark[15] = "";

  const std::string & f_ifcolor   = aliases[0];
  const std::string & f_ifalias   = aliases[1];
  const std::string & f_realif    = aliases[2];
  const std::string & f_ipaddress = aliases[3];
  const std::string & f_addmask   = aliases[4];
  const std::string & f_enabled   = aliases[7];
  const std::string & f_mask2add  = aliases[9];
  std::string scprefixf = "iptables -t filter -A";
  std::string sclogpre = " -j LOG --log-prefix \"..FFC..not.";
  std::string sclogpost = ".subnet.. \"";
  std::string sclogrej = " -j REJECT";

  //  Allow DHCP to bypass subnet checking
  rmdupes (ipb, scprefixf + " subnetchk -p udp --dport 67 -j RETURN");
  //  And allow multicast addresses to bypass subnet checking
  rmdupes (ipb, scprefixf + " subnetchk -p igmp -d 224.0.0.0/4 -j RETURN");
  rmdupes (ipb, scprefixf + " portfwi -j subnetchk");
  rmdupes (ipb, scprefixf + " portfwf -j subnetchk");

  //============================================================================>
  //  log and reject any packets with a source that is not in the correct
  //  subnet for the interface that received them
  //===>>  To disable:  set "(GREEN|PURPLE|ORANGE)=off" in the portfw settings file

  if (f_ifcolor == "GREEN")
  {
   green_if = f_realif;
   green_ifip = f_ipaddress;
   if (greencheck != "off")
   {
    char cidr[5] = "";
    sprintf((char*) cidr, "/%d", snet2cidr(f_addmask));

    std::string scpostfixl = (" -i " + green_if + " ! -s " + green_ifip + cidr +
     sclogpre + f_ifcolor + sclogpost);
    std::string scpostfixr = (" -i " + green_if + " ! -s " + green_ifip + cidr +
     sclogrej);

    rmdupes (ipb, scprefixf + " subnetchk" + scpostfixl);
    rmdupes (ipb, scprefixf + " subnetchk" + scpostfixr);
   }
  }
  if (f_ifcolor == "ORANGE")
  {
   orange_if = f_realif;
   orange_ifip = f_ipaddress;
   if (orangecheck != "off")
   {
    char cidr[5] = "";
    sprintf((char*) cidr, "/%d", snet2cidr(f_addmask));

    std::string scpostfixl = (" -i " + orange_if + " ! -s " + orange_ifip + cidr +
     sclogpre + f_ifcolor + sclogpost);
    std::string scpostfixr = (" -i " + orange_if + " ! -s " + orange_ifip + cidr +
     sclogrej);

    rmdupes (ipb, scprefixf + " subnetchk" + scpostfixl);
    rmdupes (ipb, scprefixf + " subnetchk" + scpostfixr);
   }
  }
  if (f_ifcolor == "PURPLE")
  {
   purple_if = f_realif;
   purple_ifip = f_ipaddress;
   if (purplecheck != "off")
   {
    char cidr[5] = "";
    sprintf((char*) cidr, "/%d", snet2cidr(f_addmask));

    std::string scpostfixl = (" -i " + purple_if + " ! -s " + purple_ifip + cidr +
     sclogpre + f_ifcolor + sclogpost);
    std::string scpostfixr = (" -i " + purple_if + " ! -s " + purple_ifip + cidr +
     sclogrej);

    rmdupes (ipb, scprefixf + " subnetchk" + scpostfixl);
    rmdupes (ipb, scprefixf + " subnetchk" + scpostfixr);
   }
  }
  if (f_mask2add != "" && f_mask2add.find_first_of("/") == std::string::npos &&
   f_ifalias.find_first_of(":") != std::string::npos && f_enabled == "on")

  //============================================================================>
  // Make sure we have an alias interface and a single IP to mask
  {
   sprintf((char*) conn_mark, "%#010x", (++mark_seq) * 0x100000);
   conn_mark[10] = 0;

   rmdupes (ipb, "iptables -t mangle -A portfwb -s " + f_mask2add +
    " -j MARK --set-mark " + conn_mark);

   rmdupes (ipb, "iptables -t nat -A portfw_post -o " + red_if + " -s " + f_mask2add +
    " -m mark --mark " + conn_mark + " -j SNAT --to-source " + f_ipaddress);
  }
  if (mark_seq > 0x8FF)
  {
   response = "Abort, more than 255 aliases not supported, reduce alias count.";
   return errrpt (response);
  }
  if (error)
  {
   response = "Abort in alias file for " + f_ifalias + " interface.";
   return errrpt (response);
  }
 }//     <<== End of reading "aliasfile"

 //=============================================================================>
 // This is to clean up any previously entered jumps around the proxies, then
 // we set the jumps around the proxies for any outbound masking to an alias

 std::string proxy_jmph = "iptables -t nat ";
 std::string proxy_jmpt = " -m mark --mark 0x80000000/0x80000000 -j RETURN";

 // the match mark mask does not correctly mask for some reason
 // the position of flag and mask might be reversed

 if (chkproxy())
 {
  rmdupes (ipb, proxy_jmph + "-D jmpim" + proxy_jmpt);
  rmdupes (ipb, proxy_jmph + "-D jmpp3scan" + proxy_jmpt);
  rmdupes (ipb, proxy_jmph + "-D jmpsip" + proxy_jmpt);
  rmdupes (ipb, proxy_jmph + "-D jmpsquid" + proxy_jmpt);
 }

 if (mark_seq > 0x800)
 {
  rmdupes (ipb, proxy_jmph + "-I jmpim" + proxy_jmpt);
  rmdupes (ipb, proxy_jmph + "-I jmpp3scan" + proxy_jmpt);
  rmdupes (ipb, proxy_jmph + "-I jmpsip" + proxy_jmpt);
  rmdupes (ipb, proxy_jmph + "-I jmpsquid" + proxy_jmpt);
 }

 // Prepare multiports from service names
 load_portlist();

 //=============================================================================>
 // Read the rules, in sequence from "configfile" and build

 for (int line = fwdconf.first(); line == 0; line = fwdconf.next())
 {
  const std::string & f_input   = fwdconf[1];
  const std::string & f_source  = fwdconf[2];
  const std::string & f_dport   = fwdconf[3];
  const std::string & f_output  = fwdconf[4];
  const std::string & f_fwdest  = fwdconf[5];
  const std::string & f_fwdport = fwdconf[6];
  const std::string & f_proto   = fwdconf[7];
  const std::string & f_action  = fwdconf[8];
  const std::string & f_enabled = fwdconf[9];
  const std::string & f_timed   = fwdconf[10];
  const std::string & setproxy  = fwdconf[11];

  std::string daysow = "";
  std::string time_str = "";
  std::string tmpdays = "";
  std::string tmpports = "";
  std::string proxyports = "";
  std::vector<std::string> full_time_str;
  std::vector<std::string> protos;
  std::vector<std::string> protos_tr;
  std::vector<std::string> tgt_out;
  std::vector<std::string> action_out;

  std::string aliasif    = "";

  // Determine if input interface is an alias
  if (f_input.find(":") != std::string::npos) 
  {
   aliasif = "true";
  }

  if (f_input.find_first_not_of(INTERFACE) != std::string::npos &&
   (f_input.find_first_not_of(INTERFACE_ALIAS) != std::string::npos) &&
    f_input != "any")
  {
   response = "Abort, bad input interface: (" + f_input + ") rule number " + fwdconf[0];
   return errrpt (response);
  }
  if (f_output.find_first_not_of(INTERFACE) != std::string::npos &&
   (f_output.find_first_not_of(INTERFACE_ALIAS) != std::string::npos) &&
    f_output != "any")
  {
   response = "Abort, bad output interface: " + f_output + " rule number " + fwdconf[0];
   return errrpt (response);
  }

  // First operation is to remove negation, if present

  negated_source = false;
  if ((p = f_source.find_first_of("! ")) != std::string::npos &&
   (n = f_source.find_first_not_of("! ")) != std::string::npos)
  {
     negated_source = true;
     temp_source = f_source;
     temp_source = temp_source.erase(p, n - p);
  }
  else temp_source = f_source;

  if (f_fwdport.find_first_not_of(NUMBERS_COLON) != std::string::npos)
  {
   response = "Abort, bad new destination port: (" + f_fwdport +
    ") rule number " + fwdconf[0];
   return errrpt (response);
  }
  if (f_action != "REJECT" && f_action != "RETURN" && f_action != "ACCEPT" &&
   f_action  != "DROP" && f_action != "LOG" && f_action != "LOG&ACCEPT" && 
    f_action != "LOG&REJECT" && f_action != "LOG&DROP")
  {
   response = "Abort, bad action: (" + f_action + ") rule number " + fwdconf[0];
   return errrpt (response);
  }

  //<==========================================================================>
  //                            *Ports*

   if (f_dport != "N/A")
   {            
    if ((n = f_dport.find_first_not_of(MULTI_PORTS)) == std::string::npos)
    {
     tmpports = f_dport;

     // replace all hyphens with commas
     std::replace(tmpports.begin(), tmpports.end(), '-', ','); 

     dport_out = " -m multiport --ports " + tmpports;
    }
    else
    { 
     // it's an entry from the application or service(s) menu (mapped port) 
               
     if (portlist[f_dport.c_str()].size() > 0)
     {                  
      std::string nport = "";
      std::vector<std::string> & vect = portlist[f_dport.c_str()];
      unsigned int i = 0;
      while (i < vect.size())
      {
       if (strlen ( nport.c_str() ) > 0) nport += ",";
       nport += vect[i++].c_str();
      }
      dport_out = " -m multiport --ports " + nport;
     }
    }
   }
   else dport_out = "";  // if f_dport == N/A then empty dport_out
   //<<==== End of determing initial destination port

   //=================================================================================
   //                             *Protocols*

   // Ports determined above get loaded into the protocols vector for later output in rules
   if ( f_proto == "6" || f_proto == "TCP&UDP" ) 
   {
    if ( ( f_input == red_if || aliasif == "true" ) && f_fwdport == "0" ) // Incoming rule no port translation
    {
     protos.push_back(" -p 6 " + dport_out);
     protos_tr.push_back(" -p 6 " + dport_out);
    }
    else
     if ( ( f_input == red_if || aliasif == "true" ) && f_fwdport != "0" ) // Redirecting (translating) a port
     {
      protos.push_back(" -p 6  --dport " + f_fwdport);
      protos_tr.push_back(" -p 6 " + dport_out);
     }
     else protos.push_back(" -p 6 " + dport_out);
   }
      
   if ( f_proto == "17" || f_proto == "TCP&UDP" ) 
   {
    if ( ( f_input == red_if || aliasif == "true" ) && f_fwdport == "0" ) // Incoming rule no port translation
    {
     protos.push_back(" -p 17 " + dport_out);
     protos_tr.push_back(" -p 17 " + dport_out);
    }
    else
     if ( ( f_input == red_if || aliasif == "true" ) && f_fwdport != "0" ) // Redirecting (translating) a port
     {
      protos.push_back(" -p 17  --dport " + f_fwdport);
      protos_tr.push_back(" -p 17 " + dport_out);
     }
     else protos.push_back(" -p 17 " + dport_out);
   }
                    
   // IPSEC
   if ( f_proto == "IPSec" || f_proto == "VPNs" )
   {
    protos.push_back(" -p 50 ");
    protos.push_back(" -p 51 ");
    protos.push_back(" -p 17 -m multiport --ports 500,4500 ");
   }
          
   // OpenVPN
   if ( f_proto == "OpenVPN" || f_proto == "VPNs" )
   {
    protos.push_back(" -p 6 -m multiport --ports 1194,1195 ");
    protos.push_back(" -p 17 -m multiport --ports 1194,1195 ");
   }

   // PPTP
   if ( f_proto == "PPTP" || f_proto == "VPNs" )
   {
    protos.push_back(" -p 6 -m multiport --ports 1723 ");
    protos.push_back(" -p 47 ");
   }
          
   // ICMP
   if ( f_proto == "1" )
   {
    protos.push_back(" -p 1 ");
   }

   // Any (actually all) protocols
   if ( f_proto == "all" )
   {
    protos.push_back("");
   }

   // Protocol entry not recognized
   if ( protos.size() == 0)
   {
    response = "Abort, protocol entry not recognized (" + f_proto + ") in rule number " + fwdconf[0];
    return errrpt (response);
   }

   //<=============================================================================
   //                       *Source IP or MAC or IP Range*

   // Used for defining an external Source IP or network
   srcipmac_out = "";
   srcipmac_in = ""; // for returning traffic from outgoing rule
   if (temp_source.find_first_not_of(IP_NUMBERS) == std::string::npos)
   {
    srcipmac_out = " -s " + temp_source;
    srcipmac_in = " -d " + temp_source;

    // must be a space between "!" and the descriptor
    if (negated_source) srcipmac_out = " ! " + srcipmac_out;
   }
   else
    if (temp_source.find_first_not_of(IP_RANGE) == std::string::npos)
    {
     if (negated_source)
     {
      srcipmac_out = " ! --src-range " + temp_source;
      srcipmac_in = " ! --dst-range " + temp_source;
     }
     else
     {
      srcipmac_out = " --src-range " + temp_source;
      srcipmac_in = " --dst-range " + temp_source;
     }
     srcipmac_out = " -m iprange" + srcipmac_out;
     srcipmac_in = " -m iprange" + srcipmac_in;
    }
   else
    if (temp_source.find_first_not_of(MAC_HEX) == std::string::npos)
    {
     if (negated_source)
     {
      srcipmac_out = " ! --mac-source " + temp_source;
      srcipmac_in = "";
     }
     else
     {
      srcipmac_out = " --mac-source " + temp_source;
      srcipmac_in = "";
     }
     srcipmac_out = " -m mac " + srcipmac_out;
     srcipmac_in = "";
    }
   else
    if (temp_source == "0.0.0.0/0")
    {
     srcipmac_out = "";
     srcipmac_in = "";
    }
   else
    {
     response = "Abort, bad source IP or MAC: (" + f_source + ") rule number " + fwdconf[0];
     return errrpt (response);
    }
   //<<==== End source IP/MAC

   //<============================================================================>
   //                           *Destination IP*
   std::string dstipmac_in = "";
   std::string dstipmac_out = "";
   if ((n = f_fwdest.find_first_not_of(IP_NUMBERS)) == std::string::npos)
   {
    dstipmac_in = " -s " + f_fwdest;
    dstipmac_out = " -d " + f_fwdest;
   }
   else
    if ((n = f_fwdest.find_first_not_of(MAC_HEX)) == std::string::npos)
    {
     dstipmac_out = " -m mac --mac-source " + f_fwdest;
    }
   else
    if ((n = f_fwdest.find_first_not_of(IP_RANGE)) == std::string::npos)
    {
     dstipmac_in = " -m iprange --src-range " + f_fwdest;
     dstipmac_out = " -m iprange --dst-range " + f_fwdest;
    }
   else
    if (f_fwdest == "0.0.0.0/0")
    {
     dstipmac_in = "";
     dstipmac_out = "";
    }
   else
   {
    response = "Abort, bad destination IP (" + f_fwdest + ") in rule number " + fwdconf[0];
    return errrpt (response);
   }

   //<========================================================================>
   //                             *Action Handling*

   if ( f_action == "LOG" ) tgt_out.push_back(" -j LOG --log-prefix \"Allowed-by-filter:incoming \"");
   if ( f_action == "ACCEPT" )
   { 
    tgt_out.push_back(" -j ACCEPT");
    action_out.push_back(" -j RETURN");
   }
   if ( f_action == "REJECT" ) tgt_out.push_back(" -j REJECT");
   if ( f_action == "DROP" ) tgt_out.push_back(" -j DROP");

   if ( f_action == "LOG&ACCEPT" ) 
   {
     tgt_out.push_back(" -j LOG --log-prefix \"Allowed-by-filter:incoming \"");
     tgt_out.push_back(" -j ACCEPT");

     action_out.push_back(" -j LOG --log-prefix \"Allowed-by-filter:incoming \"");
     action_out.push_back(" -j RETURN");
   }

   if ( f_action == "LOG&DROP" ) 
   {
     tgt_out.push_back(" -j LOG --log-prefix \"Denied-by-filter:incoming \"");
     tgt_out.push_back(" -j DROP");
   }

   if ( f_action == "LOG&REJECT" ) 
   {
     tgt_out.push_back(" -j LOG --log-prefix \"Denied-by-filter:incoming \"");
     tgt_out.push_back(" -j REJECT");
   }

   //<==============================================================================>
   //                              *Time Frames*
   unsigned int myx = 14;
   if (f_timed == "on")
   {
    while (fwdconf[myx+2] != "")
    {
     const std::string & daysofweek = fwdconf[myx++];
     const std::string & timestart = fwdconf[myx++];
     const std::string & timestop = fwdconf[myx++];
                
     if (daysofweek != "")
     {
      tmpdays = daysofweek;
      std::replace( tmpdays.begin(), tmpdays.end(), ' ', ','); //<<===== replace all spaces with commas
      daysow = " --weekdays " + tmpdays;
     }
     else
     {
      daysow = "";
     }
     time_str = " --timestart " + timestart + " --timestop " + timestop;
     full_time_str.push_back(" -m time --kerneltz " + daysow + time_str);
    }
   }
   else
   {
    full_time_str.push_back(" ");
   } //<<===== End of building time strings for inclusion with incoming rules

//<============================================================================>
//                             *Incoming rules section*

if (f_input == red_if || aliasif == "true")
{
  if (f_enabled == "on")
  {
   // ==========================================================================>
   // we allow red bouncing by specifying that it comes from * interface
   // because bouncing requires that DNAT and SNAT be done on the packets
   // specifying an interface on bounces is not possible, the source is the
   // destination for bounces, if the source must be limited on bounces,
   // use an IP limitation
   // ==========================================================================>
   // Here we create the source strings, or leave null if unused

   forwarding = false;
   in_dest = "";
   if (f_input.find(red_if) != std::string::npos)
   {
    if (f_proto == "1" || f_proto == "6" || f_proto == "17" ||
     f_proto == "47" || f_proto == "50" || f_proto == "51" || f_proto == "TCP&UDP")
    {
     forwarding = true;

     // ICMP:1 TCP:6 UDP:17 GRE:47 ESP:50 AH:51   <---Forwarded protocols

     in_dest = localip.str();

     // default IP for the actual red interface, changed only for aliases
     // If it is an alias

     if (f_input.find(":") != std::string::npos)
     {
      for (int line = aliases.first(); line == 0; line = aliases.next())

      // forwarding from the red interface we need to find the IP
      {
       const std::string & f_ifalias = aliases[1];
       const std::string & f_ipaddress = aliases[3];

       if ((f_input == f_ifalias  && aliases[7] == "on"))
        in_dest = f_ipaddress;
      }
     }
     if (in_dest.find_first_not_of(IP_NUMBERS) != std::string::npos &&
      in_dest.find_first_of("/") != std::string::npos)
     {
      response = "Abort, could not find match for interface (" + f_input +
       ") and IP (" + in_dest +
        ") to construct a forwarding rule in rule number " + fwdconf[0];
      return errrpt (response);
     }
    }  //  <<== End of protocols from Red IF 
   }  //  <<== End of Red IF IP address

   ifc_in_out = "";
   if (f_input != "any" && ! forwarding)

   // If it is not "any" and not being forwarded set the input interface
   {
    ifc_in_out = f_input;

    // If it is an alias interface, truncate the string starting with the colon

    if ((n = ifc_in_out.find_first_of(":")) != std::string::npos)
     ifc_in_out.erase(n, 4);

    ifc_in_out = " -i " + ifc_in_out;
   }
   ifc_out_out = "";
   if (f_output != "any" && f_output != "")
   {
    ifc_out_out = f_output;

    if ((n = ifc_out_out.find_first_of(":")) != std::string::npos)
     ifc_out_out.erase(n, 4);

    ifc_out_out = " -o " + ifc_out_out;
   }

   dest_out = "";
   if (in_dest != "") dest_out = " -d " + in_dest;

   translating = false;
   fwdport_out = "";
   fwdportdest = "";
   if (f_fwdport !=  "0" && f_fwdport !=  "")
   {
    translating = true;
    //fwdport_out = " --dport " + f_fwdport;
    fwdportdest = f_fwdport;

    if ((n = fwdportdest.find_first_of(":")) != std::string::npos)
     fwdportdest.replace(n, 1, "-");

    fwdportdest = ":" + fwdportdest;
   } //<<==== End of determining redirecting to another port incoming

   //if (! translating && dport_out != "") fwdport_out = dport_out;

   fwdest_out = "";
   dnat_out = "";
   if (translating || forwarding)
   {
    if (f_fwdest != "0.0.0.0/0" &&
      f_fwdest.find_first_of("/") == std::string::npos &&
        f_fwdest.find_first_of("-") == std::string::npos)

    // an IP is being forwarded, but we must have a destination IP to
    // forward to for DNAT to be sensible
    {
     fwdest_out = " -d " + f_fwdest;
     dnat_out = " -j DNAT --to-destination " + f_fwdest + fwdportdest;
    }
    // If we expected to build a DNAT rule and failed, the IP is not singular

    if (dnat_out == "")
    {
     response = "Abort, bad new destination IP (" + f_fwdest +
      "), must be single IP in rule number " + fwdconf[0];
     return errrpt (response);
    }

    // translation requires the same IP in the DNAT initial destination

    if (! forwarding) dest_out = fwdest_out;
   }
   
   // if we aren't going to DNAT we still need some information in portfwf

   //if (! translating && dport_out != "") fwdport_out = dport_out;

   if (dnat_out == "" && f_fwdest != "") fwdest_out = dstipmac_out;

   // ==========================================================================>
   // Here we get down to the business of creating the rules from the strings

   x = 0;
   while ( x < protos.size() ) //<<==== This is to handle if both TCP&UDP are selected
   {                           //       two rules, one for each, if so
    z = 0;        //<<==== This is the counter for multiple time strings
    while ( z < full_time_str.size() ) // attached to one rule. One rule for each time string
    {
     y = 0;
     while ( y < tgt_out.size() )
     {
      if (forwarding || translating) rmdupes (ipb, "iptables -t nat -A portfw " +
       ifc_in_out + protos_tr[x] + srcipmac_out + dest_out + full_time_str[z] + dnat_out);

      rmdupes (ipb, "iptables -t filter -A portfwf -m state --state NEW" + ifc_in_out +
       ifc_out_out + protos[x] + srcipmac_out + fwdest_out + full_time_str[z] + tgt_out[y]);

      // In the INPUT chain we should not ACCEPT since EXTACCESS should be the
      // source for that type of rule, and only process rules that are not
      // forwarding or translating rules, meaning no specific output interface

      // Note: If the destination interface is specified then we don't create
      // a rule.  This allows the proxies to bypass a block rule for outbounds
      // which may be blocked by an additional specific rule with the Any
      // interface specified.  Another option explored was to skip only ACCEPT
      // rules, but that has limited usability as well.

      if (ifc_out_out == "")
      {
       if (f_action == "ACCEPT" || f_action == "LOG&ACCEPT")
       {
        rmdupes (ipb, "iptables -t filter -A portfwi -m state --state NEW" +
         ifc_in_out + protos[x] + srcipmac_out + full_time_str[z] + action_out[y]);
       }
       else
       {
        rmdupes (ipb, "iptables -t filter -A portfwi -m state --state NEW" +
         ifc_in_out + protos[x] + srcipmac_out + full_time_str[z] + tgt_out[y]);
       }
      }
      y++;
     }
     z++;
    }
    x++;
   }

   // ==========================================================================>
   // Here we create rules for bouncing if the input interface is null and
   // there has been a DNAT for the red interface, we skip translating DNAT

   if (forwarding)
   {
    std::string forward_pre = "iptables -t mangle -A portfwb -i ";
    std::string forward_post = " -j MARK --set-mark ";

    if (green_if  != "") rmdupes (ipb, forward_pre + green_if  + dest_out +
     forward_post +  conn_green);

    if (purple_if != "") rmdupes (ipb, forward_pre + purple_if + dest_out +
     forward_post + conn_purple);

    if (orange_if != "") rmdupes (ipb, forward_pre + orange_if + dest_out +
     forward_post + conn_orange);

    bounce_type = true;
   }

  }//   <<==== End of enabled
}//    <<==== End of incoming rules

//<============================================================================>
//                             *Outgoing rules section*

if ( f_input != red_if && f_output == red_if )
{
   std::string input_dev  = "";
   std::string output_dev  = "";

   // Verify zone colors
   if (f_input == "" || f_dport == "" || f_enabled == "")
    continue;   
    /* Skip lines with these values empty */

   if (f_input == green_if)
   {
    // GREEN is always configured
    input_dev = " -i " + green_if;
    output_dev = " -o " + green_if;
   }
   if (f_input == orange_if)
   {
    if (orange_if == "" ) continue;  // skip if ORANGE is not configured
    input_dev = " -i " + orange_if;
    output_dev = " -o " + orange_if;
   }
   if (f_input == purple_if)
   {     
    if (purple_if == "" ) continue;  // skip if PURPLE is not configured
    input_dev = " -i " + purple_if;
    output_dev = " -o " + purple_if;
   }
   if ( input_dev == "" )
   {
    response = "Abort, source interface not recognized (" + f_input + ") in rule number " + fwdconf[0];
    return errrpt (response);
   }
                                                       
   if (f_enabled == "on")
   {
    std::string action2 = "";

                        /* ===========Action============= */

    if ( f_action == "ACCEPT" || f_action == "LOG&ACCEPT")
    {
/*     if (upnpfile["ENABLE_UPNP" == "on"])
     { 
      action2 = " -j MINIUPNPD";
     }
     else
     {
*/
      action2 = " -j ACCEPT";
     //}
    }
    else
    {
     action2 = " -j tofcblock";
    }

                       /* ===Deal with squid web proxy === */

    // If port 80 is blocked, block the web proxy in the INPUT chain
    if (setproxy == "on")
    {
     if (action2 == " -j tofcblock")
     {
      if (proxymod())
      {
       if (squidmodsettings["ENABLE"] == "on" || squidmodsettings["ENABLE_PURPLE"] == "on")
       {
        proxyports = " -p 6 -m multiport --ports 800 ";
       }
      }
      else
      {
       if (squidsettings["ENABLE"] == "on" || squidsettings["ENABLE_PURPLE"] == "on")
       {
        proxyports = " -p 6 -m multiport --ports 800 ";
       }
      }
     }
    }

    //==========================================================================>
                         /* =========Output========= */
    x = 0;
    while ( x < protos.size() )
    {
     z = 0;
     while ( z < full_time_str.size() )
     {
      std::string localProtos = protos[x];
      size_t portsFound;

      /* Replace --ports with --sports or --ports, respectively */
      /* Then handle the command */
      portsFound = localProtos.find("--ports");
      if (portsFound != std::string::npos) localProtos.replace(portsFound, 2, "--s");

      rmdupes(ipb, chainfwd2Int + localProtos + output_dev + srcipmac_in + dstipmac_in 
         + full_time_str[z] + " -m state --state RELATED,ESTABLISHED " + action2);

      portsFound = localProtos.find("--sports");
      if (portsFound != std::string::npos) localProtos.replace(portsFound, 3, "--d");

      rmdupes(ipb, chainfwd2Ext + localProtos + input_dev + srcipmac_out + dstipmac_out +
       full_time_str[z] + " -m state --state NEW,RELATED,ESTABLISHED " + action2);

      /* Proxy stuff should look at --dports, so no change needed                   */
      /* If a "proxyable" port is blocked, block the proxy's port in INPUT as well. */
      /* But only if the proxy is enabled                                           */

      if ( proxyports != "" )
      {
       rmdupes(ipb, chainproxy + proxyports + input_dev + srcipmac_out +
        srcipmac_in + full_time_str[z] + action2);
      }
      z++;
     }
     x++;
    }
   } // <<==== End of enabled
  } // <<==== End of outgoing rules

  //<============================================================================>
  //                            *Internal pinholes (dmzholes)*

  if (f_input != red_if && aliasif == "" && f_output != red_if)
  {
   if (f_enabled == "on")
   {
    x = 0;
    while ( x < protos.size() )
    {
     z = 0;
     while ( z < full_time_str.size() )
     {
      y = 0;
      while ( y < tgt_out.size() )
      {
       if ((f_input == green_if && (f_output == purple_if || f_output == orange_if)) || (f_input == purple_if && f_output == orange_if))
       {
        rmdupes(ipb, "iptables -A dmzholes -m state --state NEW " + protos[x] 
          + srcipmac_out + dstipmac_out + full_time_str[z] + " -j REJECT");
       }
       if ((f_input == orange_if && (f_output == purple_if || f_output == green_if)) || (f_input == purple_if && f_output == green_if))
       {
        rmdupes(ipb, "iptables -A dmzholes -m state --state NEW " + protos[x] 
          + srcipmac_out + dstipmac_out + full_time_str[z] + " -j ACCEPT");
       }
       y++;
      }
      z++;
     }
     x++;
    }
   }
  }// <<==== End of dmz internal pinholes
 }// <<==== End of reading portfw/config file

 //=============================================================================>
 // The rules have been created, now we need to allow bounces, if we are doing
 // any portforwarding that allows bouncing

 if (bounce_type)
 {
  // We only need to SNAT those packets that came in the same interface that
  // they are going out on to ensure the return path is through the interface

  std::string pfw_post_pre = "iptables -t nat -A portfw_post -m mark --mark ";
  std::string pfw_post_post = " -j SNAT --to-source ";

  if (green_if != "")
   rmdupes (ipb, pfw_post_pre + conn_green  + " -o " + green_if  + pfw_post_post +
    green_ifip);

  if (purple_if != "")
   rmdupes (ipb, pfw_post_pre + conn_purple + " -o " + purple_if + pfw_post_post +
    purple_ifip);

  if (orange_if != "")
   rmdupes (ipb, pfw_post_pre + conn_orange + " -o " + orange_if + pfw_post_post +
    orange_ifip);
 }

 // <<==== Begin setting up tofcblock drop table
 // Log then reject packets for table tofcblock
   
 std::string log_prefix = " -j LOG --log-prefix \"Denied-by-filter:outgoing \"";
 std::string rulehead = "iptables -A tofcblock -i ";
 std::string relestab = " -m state --state ESTABLISHED,RELATED";
     
 rmdupes(ipb, chainfwd2Ext + " -j tofcblock");
 rmdupes(ipb, chainfwd2Int + " -j tofcblock");
 rmdupes(ipb, "iptables -A tofcblock" + log_prefix);
 rmdupes(ipb, "iptables -A tofcblock -p tcp" + relestab + " -j REJECT --reject-with tcp-reset");
 rmdupes(ipb, "iptables -A tofcblock -j REJECT --reject-with icmp-admin-prohibited");

 rmdupes(ipb, "iptables -A dmzholes -j ACCEPT");

 //=============================================================================>
 // Pass the built up vector of strings to ipbatch to build IPTables entries

 error = ipbatch(ipb);

 if (error) response = "Abort while flushing rules to IPTables, via ipbatch.";

 return errrpt (response);
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int rmdupes( std::vector<std::string> & argv, const std::string & argc)
{
 unsigned int i = 0;
 int err = 0;

 while ( i < argv.size() )
 {
  if ( argc == argv[ i++ ] ) return err;
 }
 argv.push_back(argc);
 return err;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int errrpt(std::vector<std::string> & logdata)
{
  int err = 0, z = 0;

  for (std::vector<std::string>::iterator i = logdata.begin();
       i != logdata.end();
       i++)
  {
    syslog(LOG_INFO, "-- FFC Log:  %s", (*i).c_str());
  }

 return err;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int errrpt(const std::string & logdata)
{
 int err = 0;

 syslog(LOG_INFO, "-- FFC Log:  %s", logdata.c_str());

 return err;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int snet2cidr(const std::string & argc)
{
 int rval       = 0;
 int count      = 0;
 int counter    = 0;
 int data       = 0;
 char largc[16] = "";
 char * ref     = largc;
 bool done      = false;

 strncpy((char*) largc, argc.c_str(), 15);

 // copy 15 characters (xxx.xxx.xxx.xxx) break them at the periods, and
 // select the possible binary values of netmask converting to the CIDR

 for (counter = 0, ref = strtok((char*) largc, "."); (!done) &&
  ref != NULL; ref = strtok(NULL, "."))
 {
  data = safeatoi (ref);

  // Let's check for some odd numbers to get things correct
  // If we get a value that is greater than 255 we are in deep doo-doo

  if (data > 255) return -1;  // A return of -1 should alert the caller

  if (data > 248 && data < 252) data = 248;
  if (data > 240 && data < 248) data = 240;
  if (data > 224 && data < 240) data = 224;
  if (data > 192 && data < 224) data = 192;
  if (data > 128 && data < 192) data = 128;

  switch (data)
  {
   case 255: count+= 8; break;  // 11111111  Get the next nybble
   case 254: count++;           // 11111110  Anything less than 255
   case 253:                    // 11111101  will be the last nybble
   case 252: count++;           // 11111100  
   case 248: count++;           // 111110XX  These are all handled by
   case 240: count++;           // 11110XXX  the IF statements above
   case 224: count++;           // 1110XXXX
   case 192: count++;           // 110XXXXX
   case 128: count++;           // 10XXXXXX
   default: done = true;        // 0XXXXXXX
  }
  if ( ++counter > 3) done = true;
 }
 rval = count;

 return rval;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int wrtaliases(std::string & response)
{
 int error = 0;
 unsigned int i = 0;
 std::string cmdprefix = "/var/smoothwall/mods/fullfirewall";
 std::string varfile   = cmdprefix + "/portfw/aliases";
 std::vector<std::string> argv;
 FILE * varhandle;

 error = chkaliases(argv);

 if (!(varhandle = fopen(varfile.c_str(), "w")))
 {
  response = "Abort, could not create or open (" + varfile + ") file";
  return errrpt(response);
 }
 while ( i < argv.size() )
 {
  fputs((char*) argv[i++].c_str(), varhandle);
 }
 fclose(varhandle);

 error += simplesecuresysteml("/bin/chown","nobody:nobody",varfile.c_str(),NULL);

 response = "Successfully updated aliases file.";
 if (error) response = "Abort while attempting to update aliases file.";

 return errrpt(response);
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int wrtdefaults(std::string & response)
{
 int error = 0;
 unsigned int i = 0;
 unsigned int x = 0;

 std::string cmdprefix   = "/var/smoothwall/mods/fullfirewall";
 std::string configfile  = cmdprefix + "/portfw/config";
 std::string defaultfile = cmdprefix + "/portfw/defaults";
 std::string etherfile   = "/var/smoothwall/ethernet/settings";
 std::string redfile     = "/var/smoothwall/red/iface";

 ConfigSTR rediface(redfile);
 ConfigVAR ether(etherfile);
 ConfigCSV defaultvars(defaultfile);

 std::string gdev    = ether["GREEN_DEV"];
 std::string pdev    = ether["PURPLE_DEV"];
 std::string buildit = "";
 std::vector<std::string> argd;

 FILE * varhandle;

 if (!(varhandle = fopen(configfile.c_str(), "w")))
 {
  response = "Abort, could not create or open (" + configfile + ") file";
  return errrpt(response);
 }

 for (int line = defaultvars.first(); line == 0; line = defaultvars.next())
 {
  x++;
  std::ostringstream ostr;       //output string stream
  ostr << x;                     //convert integer to a string
  std::string cnt = ostr.str();  //cnt is the counter for the rule order number in config

  buildit  = cnt + ",";
  buildit += gdev + ",";
  buildit += defaultvars[2] + ",";
  buildit += defaultvars[3] + ",";
  buildit += rediface.str() + ",";
  buildit += defaultvars[5] + ",";
  buildit += defaultvars[6] + ",";
  buildit += defaultvars[7] + ",";
  buildit += "ACCEPT,on,off,,\n";

  argd.push_back(buildit);
 }
 if (pdev != "")
 {
  for (int line = defaultvars.first(); line == 0; line = defaultvars.next())
  {
   x++;
   std::ostringstream ostr;      //output string stream
   ostr << x;                    //convert integer to a string
   std::string cnt = ostr.str(); //cnt is the counter for the rule order number in config

   buildit  = cnt + ",";
   buildit += pdev + ",";
   buildit += defaultvars[2] + ",";
   buildit += defaultvars[3] + ",";
   buildit += rediface.str() + ",";
   buildit += defaultvars[5] + ",";
   buildit += defaultvars[6] + ",";
   buildit += defaultvars[7] + ",";
   buildit += "ACCEPT,on,off,,\n";

   argd.push_back(buildit);
  }
 }
 while (i < argd.size())
 {
  fputs((char*) argd[i++].c_str(), varhandle);
 }
 fclose(varhandle);
 error += simplesecuresysteml("/bin/chown","nobody:nobody",configfile.c_str(),NULL);

 response = "Successfully updated default outgoing rules in config file.";
 if (error) response = "Abort while attempting to update config with outgoing rules.";

 return errrpt(response);
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int chkaliases(std::vector<std::string> & argv)
{
 std::string cmdprefix = "/var/smoothwall/mods/fullfirewall";
 std::string aliasfile = cmdprefix + "/portfw/aliases";
 std::string args      = "RED";
 int error             = 0;
 ConfigCSV aliases(aliasfile);

 error += readether(argv, args);
 args   = "GREEN";
 error += readether(argv, args);
 args   = "ORANGE";
 error += readether(argv, args);
 args   = "PURPLE";
 error += readether(argv, args);
 
 for (int line = aliases.first(); line == 0; line = aliases.next())
 {
  if (aliases[0].find_first_of(":") != std::string::npos)
  {
   std::string larg;

   // Stepping through the array with an index might be simpler and quicker, 
   // but explicits allow us to replace selected values easily in the future
   
   larg  = aliases[0] + ",";
   larg += aliases[1] + ",";
   larg += aliases[2] + ",";
   larg += aliases[3] + ",";
   larg += aliases[4] + ",";
   larg += aliases[5] + ",";
   larg += aliases[6] + ",";
   larg += aliases[7] + ",";
   larg += aliases[8] + ",";
   larg += aliases[9] + "\n";
   argv.push_back(larg);
  }
 }
 return 0;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int readether(std::vector<std::string> & argv, std::string & args)
{
 std::string localipfile    = "/var/smoothwall/red/local-ipaddress";
 std::string redfile        = "/var/smoothwall/red/iface";
 std::string etherfile      = "/var/smoothwall/ethernet/settings";
 std::string buildit        = "";
 char between[32]           = "";

 ConfigVAR   ether(etherfile);
 ConfigSTR   localip(localipfile);
 ConfigSTR   rediface(redfile);

 buildit += args + ",";
 if (args == "RED")
 {
  buildit += rediface.str() + ",";
  buildit += rediface.str() + ",";
  buildit += localip.str() + ",";
 }
 else
 {
  sprintf((char *)between, "%s%s", args.c_str(), "_DEV");
  if (ether[(const char *) between] == "") return 0;
  buildit += ether[(const char *) between] + ",";
  buildit += ether[(const char *) between] + ",";
  sprintf((char *)between, "%s%s", args.c_str(), "_ADDRESS");
  buildit += ether[(const char *) between] + ",";
 }
 sprintf((char *)between, "%s%s", args.c_str(), "_NETMASK");
 buildit += ether[(const char *) between] + ",";
 sprintf((char *)between, "%s%s", args.c_str(), "_BROADCAST");
 buildit += ether[(const char *) between] + ",";
 buildit += "on,on,,\n";
 argv.push_back(buildit);

return 0;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int ifaliasdown(std::vector<std::string> & parameters, std::string & response)
{
 std::vector<std::string> argc;
 int error = 0;
 unsigned int i = 0;

 response = "Taking alias interfaces down";
 error = errrpt(response);

 std::string cmdprefix = "/var/smoothwall/mods/fullfirewall";
 std::string aliasfile = cmdprefix + "/portfw/aliases";

 ConfigCSV   aliases(aliasfile);

 for (int line = aliases.first(); line == 0; line = aliases.next())
 {
  const std::string & f_ifalias  = aliases[1];
  const std::string & f_realif   = aliases[2];
  const std::string & f_ip       = aliases[3];
  const std::string & f_net      = aliases[4];
  const std::string & f_enabled  = aliases[7];

  if (f_ifalias.find_first_of(":") != std::string::npos)
  {
   char f_ipcidr[30]     = "";
   char * ipcidrptr      = f_ipcidr;
   sprintf(ipcidrptr, "%s/%d", f_ip.c_str(), snet2cidr(f_net));

   error += simplesecuresysteml("/usr/sbin/ip","addr","delete","dev",f_realif.c_str(),ipcidrptr,NULL);
  }
 }

 response = "Successfully brought down alias interfaces.";

 if (error) response = "Abort while bringing down alias interfaces";

 return errrpt(response);
}

int get_alias(std::vector<std::string> &argc)
{
 int error = 0;

 std::vector<std::string> argv;
 std::string cmdprefix = "/var/smoothwall/mods/fullfirewall";
 std::string aliasfile = cmdprefix + "/portfw/aliases";

 ConfigCSV   aliases(aliasfile);
 ConfigVAR   netsettings("/var/smoothwall/ethernet/settings");

 for (int line = aliases.first(); line == 0; line = aliases.next())
 {
  const std::string & f_ifalias  = aliases[1];
  const std::string & f_realif   = aliases[2];
  const std::string & f_ip       = aliases[3];
  const std::string & f_net      = aliases[4];
  const std::string & f_enabled  = aliases[7];

  if (f_ifalias.find_first_of(":") != std::string::npos && f_enabled == "on")
  {
   char f_ipcidr[30]     = "";
   char * ipcidrptr      = f_ipcidr;
   sprintf(ipcidrptr, "%s/%d", f_ip.c_str(), snet2cidr(f_net));
   argc.push_back(f_realif + ipcidrptr);
  }
 }
 return error;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int ifaliasup(std::vector<std::string> & parameters, std::string & response)
{
 int error = 0;

 error = wrtaliases (response);
 if (error) return errrpt(response);

 error = ifaliasdown (parameters, response);
 if (error) return errrpt (response);

 std::vector<std::string> argv;

 std::string cmdprefix = "/var/smoothwall/mods/fullfirewall";
 std::string varfile     = "/etc/snort/vars";
 std::string localipfile = "/var/smoothwall/red/local-ipaddress";
 std::string aliasfile   = cmdprefix + "/portfw/aliases";
 ConfigCSV   aliases(aliasfile);
 ConfigSTR   localip(localipfile);
 std::string::size_type n;
 char home_net[5000] = "";
 char * hnptr = home_net;
 FILE * varhandle;

 if (localip.str() == "")
 {
  response = "Abort, could not open red local IP file (" + localipfile + ")";
  return errrpt (response);
 }
 if (localip.str().find_first_not_of(IP_NUMBERS) != std::string::npos)
 {
  response = "Abort, bad local IP: " + localip.str();
  return errrpt (response);
 }
 std::string homenet = "var HOME_NET [" + localip.str();

 response = "Bringing alias interfaces up";
 error = errrpt(response);
 hnptr += sprintf(hnptr, "%s,", homenet.c_str());

 for (int line = aliases.first(); line == 0; line = aliases.next())
 {
  std::string f_color   = aliases[0];
  std::string f_ifalias = aliases[1];
  std::string f_realif  = aliases[2];
  std::string f_ip      = aliases[3];
  std::string f_net     = aliases[4];
  std::string f_bcst    = aliases[5];

  if ((n = f_ifalias.find_first_of(":")) != std::string::npos && aliases[7] == "on")
  {
   // Add the alias to HOME_NET if it is enabled and we have room (with
   // 255 aliases maximum should be less than 4878 plus 28 chars at finish)

   if ((n = f_color.find("RED")) != std::string::npos)
    hnptr += sprintf(hnptr, "%s,", f_ip.c_str());


   errrpt("bringing up alias (" + f_ifalias + ")");

   char f_ipcidr[30]     = "";
   char * ipcidrptr      = f_ipcidr;
   sprintf(ipcidrptr, "%s/%d", f_ip.c_str(), snet2cidr(f_net)); 

   error += simplesecuresysteml("/usr/sbin/ip","addr","add","dev",f_realif.c_str(),ipcidrptr,NULL);
  }
 }
 // backup one space to overwrite the trailing comma

 hnptr += sprintf(--hnptr, "]\n");

 if (!(varhandle = fopen(varfile.c_str(), "w")))
 {
  response = "Abort, could not create or open (" + varfile + ") file";
  return errrpt(response);
 }
 fputs((char*) home_net, varhandle);
 fclose(varhandle);

 //errrpt("NOTE:  snort should be restarted manually to update its HOME_NET value");
 //errrpt("NOTE:  /etc/snort.conf can be further customized for each scenario");

 response = "Successfully brought up alias interfaces.";
 if (error) response = "Abort while bringing up alias interfaces";

 return errrpt(response);
}

///#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
bool chkproxy()
{
 unsigned int i = 0;
 std::vector<std::string> argv;
 std::vector<std::string> args;
 std::vector<std::string> argc;
 std::string              chkst;

 args.push_back("iptables -t nat -nvL jmpsquid");

 argv = simplesecurepopenvector(args, argc);

 while (i < argv.size())
 {
  chkst = argv[i++];
  if (chkst.find_first_of("MARK match 0x80000000/0x80000000") != std::string::npos)
  {
   return true;
  }
 }
 return false;
}

///#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
bool proxymod() {
    std::string file = "/var/smoothwall/mods/proxy/settings";
    struct stat buffer;
    return (stat(file.c_str(), &buffer) == 0);
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int genrpt(std::string & response)
{
 int error = 0;

 error = simplesecuresysteml("/var/smoothwall/mods/fullfirewall/ffc-diags.pl", NULL);

 response = "Successfully generated diagnostic report.";
 if (error) response = "Abort while attempting to generate diagnostic report.";

 return errrpt(response);
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int setincoming(std::string & response)
{
 return 0;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int setoutgoing(std::string & response)
{
 return 0;
}

//#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@>
int setinternal(std::string & response)
{
 return 0;
}