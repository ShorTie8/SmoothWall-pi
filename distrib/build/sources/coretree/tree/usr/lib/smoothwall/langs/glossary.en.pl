# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

%baseglossary = (

%baseglossary,

	'De-Militarized Zone'  => "<strong>De-Militarized Zone</strong> A common term for a logically isolated network used to house machines which expose services to the internet (such as HTTP or mail servers) and are therefore isolated from the locally protected networks.",
	'DMZ'  => "<strong>De-Militarized Zone</strong> A common term for a logically isolated network used to house machines which expose services to the internet (such as HTTP or mail servers) and are therefore isolated from the locally protected networks.",
	'ORANGE' => "<strong>ORANGE</strong> The name usually given for the interface on a Smoothwall system which provides the De-Militarized Zone.",
	'GREEN' => "<strong>GREEN</strong> The local network usually reserved for desktop machines and servers. It can access all the other internal networks.",
	'PURPLE' => "<strong>PURPLE</strong> An optional additional network intended to be used for wireless laptops and other devices. Machines on PURPLE can access ORANGE but not GREEN.",
	'PPP' => "<strong>Point to Point Protocol</strong> A protocol used for connecting to an ISP over a serial-like conection, such a analogue modem or ADSL.",
	'ADSL' => "<strong>Asymmetric Digital Subscriber Line</strong> A mechanism for connecting to the Internet at broadband speeds over conventional copper phone lines.",
	'ISDN' => "<strong>Integrated Standards Digital Network</strong> A moderate-speed (64Kbit/sec usually) method for connecting to the Internet.",
	'Port' => "<strong>Port</strong> Each Internet service, such HTTP or SMTP, is assigned a unique number which identifies the service. Also a general name for a connector on a PC, such a serial port.",
	'IP' => "<strong>Internet Protocol (address)</strong> Each host on an IP network is assigned a numerical address in the form 1.2.3.4. These addresses can either be external (on the wider Internet) or local (on the local network).",
	'TCP' => "<strong>Transmission Control Protocol</strong> A network protocol that guarantees reliable and in-order delivery of data between Internet hosts",
	'UDP' => "<strong>User Datagram Protocol</strong> A network protocol that provides a connection-less data exchange. Delivery of data is not guaranteed.",
	'MSN' => "<strong>Microsoft Messenger</strong> A program for talking to your mates and sending them pictures, videos and the like.",
	'IRC' => "<strong>Internet Relay Chat</strong> A realtime communications network and protocol developed in 1988. The first widespread Internet chat system.",
	'VOIP' => "<strong>Voice over Internet Protocol</strong> A catch-all term for any protocol or program that provides voice and/or data calls over the public Internet. VOIP calls are effectivly free, but can suffer from quality problems.",
	'SYN cookie' => "<strong>SYN cookie</strong> A mechanism for avoiding Denial of Service attacks.",
	'UPnP' => "<strong>Universal Plug n Play</strong> A collection of mechanisms and protocols for automating network setup, and other tasks. In Smoothwall UPnP support is used to allow programs such as MSN to work better when connecting through a NATed Internet connection.",
	'Traceroute' => "<strong>Traceroute</strong> A program that can be used to determine the path a packet will take on its way to an Inernet host.",
	'Ping' => "<strong>Ping</strong> A program for determining whether a machine is up and running, and also for measuring the time it takes to reach it.",
	'SSH' => "<strong>Secure Shell</strong> A program that can be used to gain command-line access to another machine, with the ability to encrypt the session. It also has strong authentication.",
	'HTTP' => "<strong>Hyper-Text Transfer Protocol</strong> The protcol used to transfer webpages and simular content between webservers and browsers.",
	'HTTPS' => "<strong>Hyper-Text Transfer Protcol (Secure)</strong> An extention to HTTP to provide security in the form of encryption and identification.",
	'FTP' => "<strong>File Transfer Protocol</strong> An antiquated protocol for use in file transfer between Internet hosts. It provides little in the way of authentication and encryption.",
	'POP3' => "<strong>Post Office Protocol 3</strong> A simple protocol used in the downloading of Emails between a server and a client. Extensions exist for secure authentication and encryption.",
	'NAT' => "<strong>Network Address Translation</strong> Any form of IP address munging, but in a Smoothwall context it is the mechanism by which an internal host on GREEN or any other interface accesses the Internet with only a single real external IP address.",
	'NTP' => "<strong>Network Time Protocol</strong> A protocol for telling machines, accurately, what the time is on a network. It is used both on the Internet and on LANs.",
	'VNC' => "<strong>Virtual Network Computing</strong> A set of programs, that allows the remote access of another computer\\'s desktop. Available for all major Operating Systems.",
	'SSL' => "<strong>Secure Sockets Layer</strong> A layering protocol that can be used to add encryption and authentication to a lower-level protocol, such as POP3 or HTTP.",
	'TLS' => "<strong>Transport Layer Security</strong> A layering protocol that can be used to add encryption and authentication to a lower-level protocol, such as POP3 or HTTP.",
	'ClamAV' => "<strong>Clam AntiVirus</strong> An open source (GPL) anti-virus toolkit, designed especially for e-mail scanning on mail gateways.",
	'DNS' => "<strong>Domain Name System</strong> A protocol and service for the resolution of human-understandable names, such as www.smoothwall.org, to IP addresses, and vica-versa.",
	'DHCP' => "<strong>Dynamic Host Configuration Protocol</strong> A protocol and service for automatically configuring machines on a network. DHCP typically furnishes hosts with an IP address, DNS settings, and gateway information.",
	'PCI' => "<strong>Peripheral Component Interconnect</strong> A standard for attaching peripheral devices inside of a PC. Replaces the older ISA and VESA standards.",
	'Linux' => "<strong>Linux</strong> An Open Source Operating System originally written by Linus Torvalds.",
	'ITSP' => "<strong>Internet Telephony Service Provider</strong> An ITSP offers an Internet data service for making telephone calls using VoIP (Voice over IP) technology.",
	'MAC' => "<strong>Media Access Control (address) </strong> The hardware address of a network device, typically a NIC, which is hardcoded into the device\\'s firmware.",
	'LAN' => "<strong>Local Area Network</strong> A small computer network, usually confined to a single building.",
	'URL' => "<strong>Uniform Resource Locator</strong> A sequence of characters representing the location of a resource on the Internet, such a webpage.",
	'ICMP' => "<strong>Internet Control Message Protocol</strong> A core Internet protocol which, when used together with TCP and UDP, is used to indicate error conditions and the like. It is also used for \\'pinging\\' hosts to check for availability.",
	'RED' => "<strong>RED</strong> The external (Internet) connected interface and network.",
	'ISP' => "<strong>Internet Service Provider</strong> A company or other party that provides Internet access.",
	'Setup program' => "<strong>Setup</strong> Smoothwall\\'s commandline (console) program used for performing low-level configuration tasks such as configuring network interfaces and setting user passwords.",
	'JavaScript' => "<strong>JavaScript</strong> A programming language built into most web browsers enabling dynamic content and realtime input validation, amongst other things.",
	'USB' => "<strong>Universal Serial Bus</strong> A serial bus standard for interfacing devices such as cameras, printers and modems to computers.",
	'Java' => "<strong>Java</strong> A platform-independent programming language and engine for running such programs.",
	'IGMP' => "<strong>Internet Group Management Protocol</strong> This is a communications protocol used to manage the membership of Internet Protocol multicast groups. It should generally be ignored unless a machine is part of such a group.",
	'Isochronous' => "Things that happen at regular intervals, such as the packets of an active VoIP channel.",
	'UPS' => 'Uninterruptable Power Supply.',
);

1;
