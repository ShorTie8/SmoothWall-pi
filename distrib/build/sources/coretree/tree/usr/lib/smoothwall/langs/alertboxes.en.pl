# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

%baseabouttext = (

'index.cgi'		=> '
Welcome to Smoothwall ' . $displayVersion . '<br>
This is your gateway to configuring and administering your Smoothwall
firewall.  Further information on your Smoothwall Express is available from <a href=\'http://www.smoothwall.org/\'
 title=\'www.smoothwall.org - external link\'>our website</a>.
',

'credits.cgi' 		=> 'Smoothwall Express' . $tr{'version'} . ' ' . $displayVersion . ' ' . $webuirevision,
'status.cgi' 		=> 'Active service status of your Smoothie.',
'advstatus.cgi' 	=> 'Pertinent information about your Smoothie, current configuration and resource usage.',
'graphs.cgi' 		=> 'Statistical graphical and numeric data based upon traffic usage across your Smoothwall\'s network interfaces.',
'proxy.cgi' 		=> 'Configure and enable your Smoothwall\'s integrated caching web proxy service.',
'dhcp.cgi' 		=> 'Configure and enable your Smoothwall\'s DHCP service, to automatically allocate LAN IP addresses to your network clients.',
'ddns.cgi' 		=> 'Especially suited when your ISP assigs you a different IP address every time you connect, you can configure your Smoothwall to manage and update your dynamic DNS names from several popular services.',
'ids.cgi' 		=> 'Enable the Snort IDS service to detect potential security breach attempts from outside your network.  Note that Snort <strong>does not</strong> prevent these attempts &mdash; your port forwarding and access rules are used to allow and deny inbound access from the outside.<br>Snort is no longer shipped with any rules. In order to fetch rules you need to visit <a href="http://www.snort.org" onclick="window.open(this.href); return false">www.snort.org</a> and register for an Oink code',
'remote.cgi' 		=> 'Enable Secure Shell access to your Smoothwall, and restrict access based upon referral URL to ignore external links to your Smoothwall.',
'portfw.cgi' 		=> 'Add multiple static IPs to existing interfaces and forward ports and protocols from any interface to any interface.',
'xtaccess.cgi' 		=> 'Allow access to admin services running on the Smoothwall to external hosts.',
'dmzholes.cgi' 		=> 'Enable access from a host on your ORANGE or PURPLE networks to a port on a host on your GREEN network.',
'pppsetup.cgi' 		=> 'Configure username, password and other details for up to five PPP, PPPoA or PPPoE connections.',
'vpnmain.cgi' 		=> 'Control and manage your VPN connections.',
'vpnconfig.dat' 	=> 'Create connections to other Smoothwalls or IPSec-compliant hosts which have static IP addresses.',
'log.dat' 		=> 'Check activity logs for services operating on your Smoothwall, such as DHCP, IPSec, updates and core kernel activity',
'proxylog.dat' 		=> 'Check logs for the web proxy service.',
'firewalllog.dat'	=> 'Check logs for attempted access to your network from outside hosts.  Connections listed here <strong>have</strong> been blocked.',
'ids.dat' 		=> 'Check logs for potentially malicious attempted access to your network from outside hosts.  Connections listed here <strong>have not necessarily</strong> been blocked &mdash; use the Firewall Log Viewer to confirm blocked access.',
'ipinfo.cgi' 		=> 'Perform a \'whois\' lookup on an ip address or domain name.',
'iptools.cgi' 		=> 'Perform \'ping\' and \'traceroute\' network diagnostics.',
'shell.cgi' 		=> 'Connect to your Smoothwall using a Java SSH applet (requires SSH to be <a href="/cgi-bin/remote.cgi">enabled</a>).',
'updates.cgi' 		=> 'See the latest updates and fixes available for your Smoothwall, and an installation history of updates previously applied.',
'modem.cgi' 		=> 'Apply specific AT string settings for your PSTN modem or ISDN TA.',
'changepw.cgi' 		=> 'Change passwords for the \'admin\' and \'dial\' management interface users.  This does not affect access by SSH.',
'shutdown.cgi' 		=> 'Shutdown or restart your Smoothwall &mdash; restarts are sometimes mandated by update installation.',
'time.cgi' 		=> 'Change timezone, manually set the time and date, configure time syncronisation and enable the time server.<br /><i>The time daemon runs and serves clients only when </i>Automatic<i> is selected.<br />Read the Time feature help page for these details.</i>',
'advnet.cgi' 		=> 'Configure ICMP settings and other advanced features.',
'outbound.cgi'		=> 'Configure interfaces to have outbound traffic blocked, except on specific rules.',
'ipblock.cgi' 		=> 'Add blocking rules to prevent access from specified IP addresses or networks.',
'backup.img' 		=> 'Use this page to create a backup floppy disk or floppy disk image file.',
'backup.cgi' 		=> 'Monitor PnP or manual backup progress. Configure USB/eSATA/Firewire or other hot-plug drive for PnP backups.',
'im.cgi'		=> 'Configure the IM logging proxy.',
'outgoing.cgi' 		=> 'Add rules to control local machine\'s access to external services and set time frames for them.',
'traffic.cgi'		=> 'Configure Linux Traffic Control (QoS) for your network.',
'sipproxy.cgi'		=> 'Configure the SIP proxy service. It can be used to transparently or non-transparently proxy SIP calls to and from the GREEN network.',
'interfaces.cgi'	=> 'Configure the network interface IP addresses, as well as DNS and gateway settings.',
'hosts.cgi'		=> 'Add static DNS entries to Smoothwall\'s inbuilt DNS server.',
'timedaccess.cgi'	=> 'Configure timed access rules to prevent or allow internal machines network access at certain times of the day.',
'p3scan.cgi'		=> 'Configure the POP3 anti-virus proxy. This proxy will remove viruses from emails that are retrieved through using the POP3 protocol.<br>ClamAV does not ship with rules; before you use the POP3 proxy the first time, you must run <i>freshclam</i> on the console, in an SSH session, or by clicking the Update button below.</i>',
'pop3log.dat'		=> 'Check log for the POP3 Anti-Virus service.',
'imviewer.cgi'		=> 'View logged IM conversations in realtime.',
'preferences.cgi'	=> 'Configure the Smoothwall Express User Interface.',
'bandwidthbars.cgi'	=> 'Shows realtime network bandwidth usage bars.',
'trafficmonitor.cgi'	=> 'Shows realtime network bandwidth usage graphs.',
'register.cgi'		=> 'Shows information about your Smoothwall Express system.',
'smoothinfo.cgi'        => 'Use this page to generate a report about your Smoothwall Express 3.1. This will provide a base for forum support requests.',
'urlfilter.cgi'		=> 'Block unwanted content with the URL filter for the web proxy service.',
'urlfilter.dat'		=> 'Check logs for attempted access from clients to domains and URLs that have been blocked by the URL filter.',
'apcupsd.cgi'           => 'Configure the interaction between Smoothwall Express and the UPS that powers it. Configure notifications.<br />Allow slave systems to connect to the daemon to monitor the UPS.',

);

