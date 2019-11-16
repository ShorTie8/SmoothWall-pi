/* SmoothWall libsmooth.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * -= Swedish translation team =-
 * Fredrik Johansson	<frejo@home.se>
 * Francis j. Morris	<franman@visto.com>
 * Thomas Persson	<thomas.persson@mbox2.swipnet.se> 
 * Torulf Wiberg" 	<torulf@dcab.se> 
 * Oden Eriksson	<oden.eriksson@kvikkjokk.net> 
 * Hans Laakso		<Hans.Laakso@evoxrifa.com>
 *
 * filename: swedish.c
 * Contains swedish strings. */

#include "libsmooth.h"

char *swedish_tr[] = {

/**********/
/* COMMON */
/**********/

/* TR_OK */
"Ok",
/* TR_CANCEL */
"�ngra",
/* TR_INSTALLATION_CANCELED */
"Installation avbruten.",
/* TR_HELPLINE */
"            <Tab>/<Alt-Tab> mellan elements   |  <Mellanslag> v�ljer",
/* TR_QUIT */
"L�mna",
/* TR_DISABLED */
"Avaktiverad",
/* TR_ENABLED */
"Aktiverad",
/* TR_UNSET */
"UNSET",
/* TR_UNABLE_TO_OPEN_SETTINGS_FILE */
"Kan inte �ppna inst�llnings filen",
/* TR_DONE */
"Done",
/* TR_PROBE_FAILED */
"Auto detecting misslyckades.",

/*************/
/* LIBSMOOTH */
/*************/

/* main.c  */

/* netstuff.c */
/* TR_IP_ADDRESS_PROMPT */
"IP-address:",
/* TR_NETWORK_ADDRESS_PROMPT */
"N�tverksaddress:",
/* TR_NETMASK_PROMPT */
"N�tmask:",
/* TR_ENTER_IP_ADDRESS_INFO */
"Ange IP-addressinformation",
/* TR_INVALID_FIELDS */
"F�ljande f�lt �r felaktiga:\n\n",
/* TR_IP_ADDRESS_CR */
"IP-address\n",
/* TR_NETWORK_ADDRESS_CR */
"N�tverksaddress\n",
/* TR_NETWORK_MASK_CR */
"N�tmask\n",
/* TR_INTERFACE (%s is interface name) */
"%s n�tverksgr�nssnitt",
/* TR_ENTER_THE_IP_ADDRESS_INFORMATION (%s is interface name) */
"Fyll i IP-address information f�r varje %s n�tverksgr�nssnitt.",
/* TR_LOOKING_FOR_NIC (%s is a nic name) */
"S�ker efter: %s",
/* TR_FOUND_NIC (%s is a nic name) */
"Smoothwall har hittat f�jande N�tverkskort i din maskin: %s",
/* TR_MODULE_NAME_CANNOT_BE_BLANK */
"Modulnamnet kan inte vara blankt.",
/* TR_STATIC */
"Statisk",
/* TR_DHCP_HOSTNAME */
"DHCP-v�rdnamn:",
/* TR_DHCP_HOSTNAME_CR */
"DHCP-v�rdnamn\n",

/* misc.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_HOSTNAMECONF */
"Kan inte skriva till /var/smoothwall/main/hostname.conf",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS */
"Kan inte skriva till /etc/hosts.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_DENY */
"Kan inte skriva till /etc/hosts.deny.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_ALLOW */
"Kan inte skriva till /etc/hosts.allow.",
/* TR_UNABLE_TO_SET_HOSTNAME */
"Kan inte st�lla in v�rdnamn.",

/***********/
/* INSTALL */
/***********/
/* TR_WELCOME */
"W�lkommen till Smoothwall installationsprogram. Bes�k g�rna v�r " \
"hemsida p� http://www.smoothwall.org. Om du v�ljer Avbryt p� n�gon " \
"av f�ljande f�nster kommer datorn att startas om.",
/* TR_NO_IDE_HARDDISK */
"Ingen IDE-h�rddisk hittad.",
/* TR_SELECT_INSTALLATION_MEDIA */
"V�lj installations media",
/* TR_SELECT_INSTALLATION_MEDIA_LONG */
"Smoothwall kan installeras fr�n olika media.   Enklast �r att " \
"anv�nda Datorns CDROM l�sare. Om datorn inte har detta, kan du alltid " \
"installera via en annan Dator p� ditt lokala N�tverk d�r installations filerna " \
"finns via HTTP. I detta fall beh�ver du Smoothwall driver diskett.",
/* TR_NO_IDE_CDROM */
"Ingen IDE-cdrom hittad.",
/* TR_INSERT_CDROM */
"Stoppa in Smoothwall CD:n i CDROM l�saren.",
/* TR_INSERT_FLOPPY */
"Stoppa in Smoothwall driver diskett i diskettl�saren.",
/* TR_PREPARE_HARDDISK */
"Installationsprogramet kommer nu att preparera din IDE h�rddisk p� %s. " \
"F�rst kommer disken att bli partitionerad, s� att installationsprogrammet " \
"kan kopiera filerna till h�rddisken.",
/* TR_PARTITIONING_DISK */
"Skapar partition p� h�rddisken...",
/* TR_UNABLE_TO_PARTITION */
"Kan inte skapa partition p� h�rddisken.",
/* TR_MAKING_SWAPSPACE */
"Skapar swaputrymme...",
/* TR_UNABLE_TO_MAKE_SWAPSPACE */
"Kan inte skapa swaputrymme.",
/* TR_MAKING_ROOT_FILESYSTEM */
"Skapar root filsystem...",
/* TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM */
"Kan inte skapa rootfilsystem.",
/* TR_MOUNTING_ROOT_FILESYSTEM */
"Monterar rootfilsystem...",
/* TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM */
"Kan inte montera rootfilsystem.",
/* TR_MAKING_BOOT_FILESYSTEM */
"Skapar bootfilsystem...",
/* TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM */
"Kan inte skapa bootfilsystem.",
/* TR_MOUNTING_BOOT_FILESYSTEM */
"Monterar bootfilsystem...",
/* TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM */
"Kan inte montera bootfilsystem.",
/* TR_MAKING_LOG_FILESYSTEM */
"Skapar loggfiler...",
/* TR_UNABLE_TO_MAKE_LOG_FILESYSTEM */
"Kan inte skapa loggfilsystemet.",
/* TR_MOUNTING_LOG_FILESYSTEM */
"Monterar loggfilsystemet...",
/* TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM */
"Kan inte montera loggfilsystemet.",
/* TR_MOUNTING_SWAP_PARTITION */
"Monterar swappartitionen...",
/* TR_UNABLE_TO_MOUNT_SWAP_PARTITION */
"Kan inte montera swappartitionen.",
/* TR_NETWORK_SETUP_FAILED */
"N�tverksinst�llningarna �r inte godk�nda.",
/* TR_NO_TARBALL_DOWNLOADED */
"Ingen tarball nerladdad.",
/* TR_INSTALLING_FILES */
"Installerar filer...",
/* TR_UNABLE_TO_INSTALL_FILES */
"Kan inte installera filer.",
/* TR_UNABLE_TO_REMOVE_TEMP_FILES */
"Kan inte ta bort tempor�ra TEMP-filer.",
/* TR_ERROR_WRITING_CONFIG */
"Fel vid skrivning till konfigurationsinformation.",
/* TR_INSTALLING_LILO */
"Installarerar LILO...",
/* TR_UNABLE_TO_INSTALL_LILO */
"Kan inte installarera LILO.",
/* TR_UNABLE_TO_UNMOUNT_HARDDISK */
"Kan inte montera h�rddisk.",
/* TR_UNABLE_TO_UNMOUNT_CDROM */
"Kan inte avmontera CDROM/floppydisk.",
/* TR_UNABLE_TO_EJECT_CDROM */
"Kan inte mata ut CD.",
/* TR_CONGRATULATIONS */
"Grattis!",
/* TR_CONGRATULATIONS_LONG */
"Smoothwall har lyckats med installationen. Ta bort ev floppydisketter eller " \
"CD-skivor ur datorn. Konfigurationsprogrammet kommer att forts�tta att konfigurera ISDN, " \
"n�tverkskort och system l�senord. N�r installationen �r " \
"klar skall du peka din webl�sare p� http://smoothwall:81 eller " \
"https://smoothwall:445 (dvs det namnet du gav Smoothwall), d�r kan du st�lla in " \
"modem uppkoppling (om s� beh�vs) fj�rraccess. Kom ih�g att st�lla in " \
"l�senord f�r Smoothwall modemuppkopplingsanv�ndare, om du vill f�rhindra att icke Smoothwall " \
"'admin' anv�ndare ska kunna ta kontroll �ver l�nken.",
/* TR_PRESS_OK_TO_REBOOT */
"Tryck Ok f�r att starta om.",
/* TR_ERROR */
"Fel",
/* TR_CALCULATING_MODULE_DEPENDANCIES */
"Kalkylerar modul beroenden...",
/* TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES */
"Kan inte kalkylera modul beroenden.",

/* cdrom.c */
/* TR_SELECT_CDROM_TYPE */
"V�lj CDROM-model",
/* TR_SELECT_CDROM_TYPE_LONG */
"Ingen IDE CDROM hittad i Datorn.   V�lj vilken av " \
"f�ljande drivrutiner du vill anv�nda s� Smoothwall kan anv�nda CD l�saren.",
/* TR_SUGGEST_IO (%x is an IO number) */
"(letar %x)",
/* TR_SUGGEST_IRQ (%d is an IRQ number) */
"(letar %d)",
/* TR_CONFIGURE_THE_CDROM */
"St�ll in CD-l�saren med att v�lja r�tt IO address och/eller IRQ.",
/* TR_INVALID_IO (note extra space) */
"Felaktigt v�rde p� IO-port!!. ",
/* TR_INVALID_IRQ */
"Felaktigt v�rde p� IRQ!!.",

/* config.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_SETTINGS */
"Kan inte skriva /var/smoothwall/main/settings.",
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_ETHERNET_SETTINGS */
"Kan inte skriva /var/smoothwall/ethernet/settings.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK */
"Kan inte skapa symlink /dev/harddisk.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1 */
"Kan inte skapa symlink /dev/harddisk1.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2 */
"Kan inte skapa symlink /dev/harddisk2.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3 */
"Kan inte skapa symlink /dev/harddisk3.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4 */
"Kan inte skapa symlink /dev/harddisk4.",

/* net.c */
/* TR_DOWNLOADING */
"Laddar ned...",
/* TR_FAILED_TO_DOWNLOAD */
"fel vid nerladdning.",
/* TR_ENTER_URL */
"Skriv URL till Smoothwall tar.gz filen. " \
"VARNING: DNS �r inte tillg�nlig!  URL:n ska alltid sluta med 'smoothwall.tgz'.",

/* nic.c */
/* TR_CONFIGURE_NETWORKING */
"N�tverksinst�llning",
/* TR_CONFIGURE_NETWORKING_LONG */
"Du skall nu st�lla in n�tverket med att f�rst ladda r�tt drivrutin f�r " \
"GR�NT n�tverkskort. Du kan g�ra detta genom att antingen l�ta systemet leta upp" \
"n�tverkskortet, eller s� v�ljer du sj�lv r�tt drivrutin fr�n en lista. Notera att om du har " \
"mera �n ett n�tverkskort installerat, s� kan du alltid konfigurera dessa " \
"senare i installationen. Notera ochs� att om du har flera n�tverkskort " \
"med samma model som GR�NT s� kr�vs speciella" \
"parameterar, du m�ste alltid �ndra alla parameterar f�r n�tverkskortet s� att "  \
"alla n�tverkskort kan aktiveras n�r du st�ller in GR�NA sidan.",
/* TR_INTERFACE_FAILED_TO_COME_UP */
"N�tverket kan inte initieras.",
/* TR_ENTER_NETWORK_DRIVER */
"Hittar inte n�tverkskort automatiskt st�ll in r�tt drivrutin och " \
"anv�nd specifika parameterar f�r n�tverkskort.",

/*********/
/* SETUP */
/*********/

/* main.c */
/* TR_HOSTNAME */
"Datornamn",
/* TR_NETWORKING */
"N�tverk",
/* TR_DHCP_SERVER_CONFIGURATION */
"DHCP-server inst�llningar",
/* TR_ISDN_CONFIGURATION */
"ISDN-inst�llningar",
/* TR_ROOT_PASSWORD */
"\'root\' l�senord",
/* TR_SETUP_l�senord */
"\'setup\' password",
/* TR_ADMIN_PASSWORD */
"Admin l�senord",
/* TR_SECTION_MENU */
"Huvudmeny",
/* TR_SELECT_THE_ITEM */
"V�lj vad du vill konfigurera.",
/* TR_SETUP_FINISHED */
"Konfigureringen �r f�rdig.  Tryck p� Ok f�r omstart.",
/* TR_SETUP_NOT_COMPLETE */
"Installationen slutf�rdes inte korrekt.  Du m�ste f�rs�kra dig om att installationen blev " \
"korrekt slutf�rd. K�r setup igen via fj�rrkonsol.",

/* passwords.c */
/* TR_ENTER_ROOT_PASSWORD */
"V�lj ett'root' l�senord. Du kan logga in som denna anv�ndare f�r access via kommandotolk.",
/* TR_SETTING_ROOT_PASSWORD */
"Sparar  'root' l�senord....",
/* TR_PROBLEM_SETTING_ROOT_PASSWORD */
"Kan inte spara 'root' l�senord.",
/* TR_ENTER_SETUP_PASSWORD */
"Skriv in 'setup' anv�ndarens l�senord. Logga in som denna anv�ndare f�r att komma " \
"till konfigureringsprogrammet programmet.",
/* TR_SETTING_SETUP_PASSWORD */
"Sparar 'setup' l�senord....",
/* TR_PROBLEM_SETTING_SETUP_PASSWORD */
"Kan inte spara 'setup' l�senord.",
/* TR_ENTER_ADMIN_PASSWORD */
"Skriv in Smoothwall administrat�r l�senord.Denna anv�ndare �r till f�r " \
"inlogging som Smoothwalls webbadministrat�r.",
/* TR_SETTING_ADMIN_PASSWORD */
"Sparar Smoothwalls administrat�rl�senord....",
/* TR_PROBLEM_SETTING_ADMIN_PASSWORD */
"Kan inte spara Smoothwall administrat�r l�senord.",
/* TR_PASSWORD_PROMPT */
"l�senord:",
/* TR_AGAIN_PROMPT */
"Igen:",
/* TR_PASSWORD_CANNOT_BE_BLANK */
"L�senordet kan inte vara tomt.",
/* TR_PASSWORDS_DO_NOT_MATCH */
"L�senorden matchar inte varandra.",

/* hostname.c */
/* TR_ENTER_HOSTNAME */
"Skriv in datornamn.",
/* TR_HOSTNAME_CANNOT_BE_EMPTY */
"Datornamn kan inte vara tomt.",
/* TR_HOSTNAME_CANNOT_CONTAIN_SPACES */
"Datornamn f�r inte inneh�lla blanksteg.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTNAME */
"Kan inte skriva datornamn till /etc/hostname",

/* isdn.c */
/* TR_GERMAN_1TR6 */
"German 1TR6",
/* TR_EURO_EDSS1 */
"Euro (EDSS1)",
/* TR_LEASED_LINE */
"Leased line",
/* TR_US_NI1 */
"US NI1",
/* TR_PROTOCOL_COUNTRY */
"Protokoll/Land",
/* TR_ISDN_CARD */
"ISDN-kort",
/* TR_MSN_CONFIGURATION */
"Eget telefonnummer (MSN/EAZ)",
/* TR_SET_ADDITIONAL_MODULE_PARAMETERS */
"S�tt specifika modulparameterar",
/* TR_RED_IN_USE */
"ISDN (eller annan externt koppling) anv�nds.  Du kan inte " \
"konfigurera ISDN n�r det R�DA n�tet �r aktivt.",
/* TR_ISDN_CONFIGURATION_MENU */
"ISDN-inst�llningar",
/* TR_ISDN_STATUS */
"ISDN Status %s.\n\n" \
"   Protocol: %s\n" \
"   Kort: %s\n" \
"   Lokalt telenummer: %s\n\n" \
"V�lj vilket du vill omkonfigurera , eller v�lj nuvarande inst�llningar.",
/* TR_ISDN_NOT_YET_CONFIGURED */
"ISDN har inte blivit konfigurerat. V�lj vilket du vill konfigurera.",
/* TR_ENABLE_ISDN */
"Aktiverar ISDN",
/* TR_DISABLE_ISDN */
"Deaktiverar ISDN",
/* TR_INITIALISING_ISDN */
"Initierar ISDN...",
/* TR_UNABLE_TO_INITIALISE_ISDN */
"Kan inte initiera ISDN.",
/* TR_ISDN_NOT_SETUP */
"ISDN setup kan ej spara. Vissa f�lt ej markerade.",
/* TR_ISDN_PROTOCOL_SELECTION */
"ISDN protocol selection",
/* TR_CHOOSE_THE_ISDN_PROTOCOL */
"V�lj vilket ISDN-protokoll du beh�ver.",
/* TR_AUTODETECT */
"* Automatisk *",
/* TR_ISDN_CARD_SELECTION */
"ISDN card selection",
/* TR_CHOOSE_THE_ISDN_CARD_INSTALLED */
"V�lj vilket ISDN-kort du har.",
/* TR_CHECKING_FOR */
"S�ker efter: %s",
/* TR_ISDN_CARD_NOT_DETECTED */
"ISDN-kort ej hittat. Du beh�ver v�lja drivrutin manuellt " \
"Om det �r ett kort med en ISA-buss beh�ver du v�lja IO-adress IRQ .",
/* TR_DETECTED */
"Funnet : %s",
/* TR_UNABLE_TO_FIND_AN_ISDN_CARD */
"Kan inte hitta n�got ISDN-kort i denna dator. Du m�ste v�lja r�tt drivrutin " \
"Om det �r ett kort med en ISA-buss beh�ver du manuellt v�lja IO-adress IRQ " \
"specifika inst�llningar.",
/* TR_ENTER_THE_LOCAL_MSN */
"Skriv in ditt lokala telefonnummer (MSN/EAZ).",
/* TR_PHONENUMBER_CANNOT_BE_EMPTY */
"Telefonnummer kan inte vara blankt.",
/* TR_ENTER_ADDITIONAL_MODULE_PARAMS */
"Vissa ISDN-kort (speciellt ISA-kort) m�ste du manuellt v�lja " \
"specifika parameterar f�r IRQ och IO-adress." \
"skriv dessa extra parameterar h�r. Till exempel: " \
"\"io=0x280 irq=9\". Dessa kommer att anv�ndas f�r hitta ditt ISDN-kort.",

/* networking.c */
/* TR_PUSHING_NETWORK_DOWN */
"Deaktiverar n�tverket...",
/* TR_PULLING_NETWORK_UP */
"Aktiverar n�tverket...",
/* TR_NETWORK_CONFIGURATION_TYPE */
"N�tverkskonfigurationstyp",
/* TR_DRIVERS_AND_CARD_ASSIGNMENTS */
"Drivrutin och kortinst�llningar",
/* TR_ADDRESS_SETTINGS */
"Adressinst�llningar",
/* TR_DNS_AND_GATEWAY_SETTINGS */
"DNS och Gateway-inst�llningar",
/* TR_RESTART_REQUIRED */
"\n\n N�r konfigurationen �r klar, kommer n�tverket att starta om.",
/* TR_CURRENT_CONFIG (first %s is type, second is restart message (or not) */
"Nuvarande konfiguration: %s%s",
/* TR_NETWORK_CONFIGURATION_MENU */
"N�tverkskonfiguration",
/* TR_NETWORK_CONFIGURATION_TYPE_LONG */
"V�lj vilken n�tverkskonfiguration f�r Smoothwall.  F�ljande " \
"visar vilket n�tverksgr�nssnitt som �r tilldelad till respektive n�tverkskort. " \
"Om du �ndrar denna inst�llning, kommer n�tverket att starta om," \
"d� m�ste du tilldela om n�tverksgr�nssnitt till respektive n�tverkskort.",
/* TR_PUSHING_NON_LOCAL_NETWORK_DOWN */
"Deaktiverar lokalt n�tverk...",
/* TR_YOUR_CONFIGURATION_IS_SINGLE_GREEN_ALREADY_HAS_DRIVER */
"Din konfiguration �r inst�lld f�r enkelt GR�NT n�tverksgr�nssnitt, " \
"som redan har en drivrutin tilldelad.",
/* TR_CONFIGURE_NETWORK_DRIVERS */
"Tilldela n�tverksdrivutiner, till vilket n�tverksgr�nssnitt f�r varje n�tverkskort " \
"du vill tilldela.  Nuvarande konfiguration :\n\n",
/* TR_DO_YOU_WISH_TO_CHANGE_THESE_SETTINGS */
"\nDo vill du �ndra dessa inst�llningar?",
/* TR_UNCLAIMED_DRIVER */
"Det finns ej tilldelade n�tverkskort av typen:\n%s\n\n" \
"Du kan tilldelad detta till:",
/* TR_CARD_ASSIGNMENT */
"N�tverkskorttilldelning",
/* TR_PROBE */
"Unders�ker",
/* TR_SELECT */
"V�lj",
/* TR_NO_UNALLOCATED_CARDS */
"Inga ej tilldelade n�tverkskort kvar, " \
"fler beh�vs. Du kan l�ta systemet s�ka efter flera n�tverkskort, eller " \
"v�lj manuellt en drivrutin fr�n listan.",
/* TR_UNABLE_TO_FIND_ANY_ADDITIONAL_DRIVERS */
"Hittar inte l�mplig drivrutin.",
/* TR_ALL_CARDS_SUCCESSFULLY_ALLOCATED */
"Alla n�tverkskort hittade .",
/* TR_NOT_ENOUGH_CARDS_WERE_ALLOCATED */
"Inte tillr�ckligt med n�tverkskort hittade.",
/* TR_MANUAL */
"* MANUELLT *",
/* TR_SELECT_NETWORK_DRIVER */
"V�lj n�tverksdrivrutin",
/* TR_SELECT_NETWORK_DRIVER_LONG */
"V�lj drivrutin f�r n�tverkskortet du har i datorn. " \
"Om du v�ljer MANUELLT, har du m�jlighet att v�lja " \
"drivrutin f�r ditt n�tverkskort,samt specifika parametrar " \
" typ IO-adress IRQ.",
/* TR_UNABLE_TO_LOAD_DRIVER_MODULE */
"Kan inte ladda drivrutin.",
/* TR_THIS_DRIVER_MODULE_IS_ALREADY_LOADED */
"Denna drivrutin �r redan laddad.",
/* TR_MODULE_PARAMETERS */
"Skriv in modul(drivrutin) namnet och specifika parametrar f�r din drivrutin beh�ver.",
/* TR_LOADING_MODULE */
"Ladda modulen...",
/* TR_WARNING */
"WARNING",
/* TR_WARNING_LONG */
"Om du �ndrar denna IP-adress, och �r inloggad via fj�rrkonsolen, " \
"s� kommer du att tappa kontakten till Smoothwall, " \
"du m�ste du �ter igen ta kontakt med nya IP-adressen.Detta kan vara en riskabel �tg�rd om n�got g�r fel, " \
"Man b�r g�ra detta enbart om fysiskt befinner sig vid datorn.",
/* TR_SINGLE_GREEN */
"Din konfiguration �r inst�lld f�r enkelt GR�NT n�tverksgr�nssnitt.",
/* TR_SELECT_THE_INTERFACE_YOU_WISH_TO_RECONFIGURE */
"V�lj vilket n�tverksgr�nssnitt du vill omkonfigurera.",
/* TR_DNS_GATEWAY_WITH_GREEN */
"Din konfiguration kan inte dra nytta av n�tverkskortet f�r " \
"sitt R�DA gr�nssnitt. DNS och Gateway-information f�r uppringda anv�ndare " \
"konfigureras automatiskt vid uppringning.",
/* TR_PRIMARY_DNS */
"Prim�r DNS:",
/* TR_SECONDARY_DNS */
"Sekund�r DNS:",
/* TR_DEFAULT_GATEWAY */
"Standard Gateway (IP):",
/* TR_DNS_AND_GATEWAY_SETTINGS_LONG */
"Skriv DNS och standardgateway. Dessa inst�llningar beh�vs om DHCP " \
"�r avaktiverad p� det R�DA n�tverksgr�nssnittet.",
/* TR_PRIMARY_DNS_CR */
"Prim�r DNS\n",
/* TR_SECONDARY_DNS_CR */
"Sekund�r DNS\n",
/* TR_DEFAULT_GATEWAY_CR */
"Standard Gateway\n",
/* TR_SECONDARY_WITHOUT_PRIMARY_DNS */
"Sekund�r DNS specificerad utan Prim�r DNS",
/* TR_UNKNOWN */
"Ok�nt",
/* TR_NO_ORANGE_INTERFACE */
"Inget ORANGE n�tverksgr�nssnitt tilldelat.",
/* TR_MISSING_ORANGE_IP */
"Ingen IP-information p� ORANGE n�tverksgr�nssnitt.",
/* TR_NO_RED_INTERFACE */
"Inget R�TT n�tverksgr�nssnitt tilldelat.",
/* TR_MISSING_RED_IP */
"Ingen IP-information p� R�TT n�tverksgr�nssnitt.",

/* dhcp.c */
/* TR_START_ADDRESS */
"Startadress:",
/* TR_END_ADDRESS */
"Slutadress:",
/* TR_DEFAULT_LEASE */
"Standardleasetid (mins):",
/* TR_MAX_LEASE */
"Max leasetid (mins):",
/* TR_DOMAIN_NAME_SUFFIX */
"Dom�n:",
/* TR_CONFIGURE_DHCP */
"Konfigurera DHCP-server genom att skriva in parameterinformation.",
/* TR_START_ADDRESS_CR */
"Startadress\n",
/* TR_END_ADDRESS_CR */
"Slutadress\n",
/* TR_DEFAULT_LEASE_CR */
"Standardleasetid\n",
/* TR_MAX_LEASE_CR */
"Max leasetid\n",
/* TR_DOMAIN_NAME_SUFFIX_CR */
"Dom�n \n",

/* keymap.c */
/* TR_KEYBOARD_MAPPING */
"Tangentbord",
/* TR_KEYBOARD_MAPPING_LONG */
"V�lj vilket tangentbord du anv�nder fr�n listan nedan.",

/* timezone.c */
/* TR_TIMEZONE */
"Tidszon",
/* TR_TIMEZONE_LONG */
"V�lj vilken tidszon du befinner dig i fr�n listan nedan.",

/* usbadsl.c */
/* TR_USB_CONTROLLER */
"V�lj vilken USB kontroller",
/* TR_USBADSL_STATUS */
"USB ADSL �r f�ljande: %s\n" \
"   kontroller: %s\n\n" \
"V�lj vilken du vill omkonfigurera, eller v�lj nuvarande inst�llningar.",
/* TR_USBADSL_CONFIGURATION */
"USB ADSL konfiguration",
/* TR_ENABLE_USBADSL */
"Aktivera USB ADSL",
/* TR_DISABLE_USBADSL */
"Avaktivera USB ADSL",
/* TR_INITIALISING_USBADSL */
"Initierar USB ADSL.",
/* TR_UNABLE_TO_INITIALISE_USBADSL */
"Kan inte initiera USB ADSL",
/* TR_USBADSL_NOT_SETUP */
"USB ADSL inte konfigurerat.",
/* TR_USB_CONTROLLER_SELECTION */
"USB kontroller val",
/* TR_CHOOSE_THE_USB_CONTROLLER_INSTALLED */
"V�lj vilken USB kontroller som �r installarerad i din Smoothwall-dator.",
/* TR_USB_CONTROLLER_NOT_DETECTED */
"USB kontroller inte hittad.",
/* TR_UNABLE_TO_FIND_A_USB_CONTROLLER */
"Hittar inte n�gon USB kontroller.",
/* TR_STARTING_UP_USBADSL */
"Startar upp USB ADSL..."

};
