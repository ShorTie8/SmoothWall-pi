/* SmoothWall libsmooth.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * (c) Danish Translation Team:
 * Jacob Anderson
 * Karina Anderson 
 *
 * filename: danish
 * Contains danish strings. */
 
#include "libsmooth.h"

char *danish_tr[] = {

/**********/
/* COMMON */
/**********/

/* TR_OK */
"Ok",
/* TR_CANCEL */
"Annuler",
/* TR_INSTALLATION_CANCELED */
"Installation annuleret.",
/* TR_HELPLINE */
"          <Tab>/<Alt-Tab> mellem elementerne   |  <Mellemrum> v�lger",
/* TR_QUIT */
"Afbryd",
/* TR_DISABLED */
"Sl�et Fra",
/* TR_ENABLED */
"Sl�et Til",
/* TR_UNSET */
"Ikke Sat",
/* TR_UNABLE_TO_OPEN_SETTINGS_FILE */
"Kan ikke �bne indstillingsfilen",
/* TR_DONE */
"Udf�rt",
/* TR_PROBE_FAILED */
"Auto detektering mislykkedes.",

/*************/
/* LIBSMOOTH */
/*************/

/* main.c  */

/* netstuff.c */
/* TR_IP_ADDRESS_PROMPT */
"IP adresse:",
/* TR_NETWORK_ADDRESS_PROMPT */
"Netv�rks adresse:",
/* TR_NETMASK_PROMPT */
"Netv�rks maske:",
/* TR_ENTER_IP_ADDRESS_INFO */
"Indtast IP adresse information",
/* TR_INVALID_FIELDS */
"De f�lgende felter er ugyldige:\n\n",
/* TR_IP_ADDRESS_CR */
"IP adresse\n",
/* TR_NETWORK_ADDRESS_CR */
"Netv�rks adresse\n",
/* TR_NETWORK_MASK_CR */
"Netv�rks maske\n",
/* TR_INTERFACE (%s is interface name) */
"%s interface",
/* TR_ENTER_THE_IP_ADDRESS_INFORMATION (%s is interface name) */
"Indtast IP adresse information for %s interfacet.",
/* TR_LOOKING_FOR_NIC (%s is a nic name) */
"Leder efter: %s",
/* TR_FOUND_NIC (%s is a nic name) */
"Smoothwall har fundet f�lgende NIC'er p� din maskine: %s",
/* TR_MODULE_NAME_CANNOT_BE_BLANK */
"Modul navn kan ikke v�re blankt.",
/* TR_STATIC */
"Statisk",
/* TR_DHCP_HOSTNAME */
"DHCP V�rtsnavn:",
/* TR_DHCP_HOSTNAME_CR */
"DHCP V�rtsnavn\n",

/* misc.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_HOSTNAMECONF */
"Kan ikke skrive til /var/smoothwall/main/hostname.conf",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS */
"Kan ikke skrive til /etc/hosts.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_DENY */
"Kan ikke skrive til /etc/hosts.deny.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_ALLOW */
"Kan ikke skrive til /etc/hosts.allow.",
/* TR_UNABLE_TO_SET_HOSTNAME */
"Ude af stand til at s�tte v�rtsnavn.",

/***********/
/* INSTALL */
/***********/
/* TR_WELCOME */
"Velkommen til Smoothwall installationsprogrammet. Bes�g vores " \
"hjemmeside p� http://www.smoothwall.org.  Ved at v�lge Annuler " \
"p� de f�lgende sk�rmbilleder kan du reboote (genstarte) computeren.",
/* TR_NO_IDE_HARDDISK */
"Der bliv IKKE fundet nogen IDE harddisk.",
/* TR_SELECT_INSTALLATION_MEDIA */
"V�lg installations medie",
/* TR_SELECT_INSTALLATION_MEDIA_LONG */
"Smoothwall kan installed fra flere kilder.  Det nemmeste er at bruge " \
"maskinens CDROM drev. Hvis computer ikke har et CDROM drev, kan du " \
"installere via en anden maskine p� et LAN som har installationsfilerne " \
"tilg�ngelige via HTTP. I dette tilf�lde vil en netv�rks driver diskette v�re " \
"n�dvendig.",
/* TR_NO_IDE_CDROM */
"Ingen IDE cdrom fundet.",
/* TR_INSERT_CDROM */
"Inds�t venligst Smoothwall CD i CDROM drevet.",
/* TR_INSERT_FLOPPY */
"Inds�t venligst Smoothwall driver disketten i floppy drevet.",
/* TR_PREPARE_HARDDISK */
"Installations programmet vil nu forberede IDE harddisken p� %s. " \
"F�rst vil disken blive partitioneret, derefter vil partitionerne f� lagt et " \
"filsystem p�.",
/* TR_PARTITIONING_DISK */
"Partitionerer disk...",
/* TR_UNABLE_TO_PARTITION */
"Ikke i stand til at partitionere disken.",
/*s TR_MAKING_SWAPSPACE */
"Laver swap plads...",
/* TR_UNABLE_TO_MAKE_SWAPSPACE */
"Ikke i stand til at lave swap plads.",
/* TR_MAKING_ROOT_FILESYSTEM */
"Laver root (rod) filsystem...",
/* TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM */
"Ikke i stand til at lave root filsystem.",
/* TR_MOUNTING_ROOT_FILESYSTEM */
"Mounter root filsystemet...",
/* TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM */
"Ikke i stand til at mounte root filsystemet.",
/* TR_MAKING_BOOT_FILESYSTEM */
"Laver boot filsystemet...",
/* TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM */
"Ikke i stand til at lave boot filsystemet.",
/* TR_MOUNTING_BOOT_FILESYSTEM */
"Mounter boot filsystemet...",
/* TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM */
"Ikke i stand til at mounte boot filsystemet.",
/* TR_MAKING_LOG_FILESYSTEM */
"Laver lognings filsystemet...",
/* TR_UNABLE_TO_MAKE_LOG_FILESYSTEM */
"Ikke i stand til at lave lognings filsystemet.",
/* TR_MOUNTING_LOG_FILESYSTEM */
"Mounter lognings filsystemet...",
/* TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM */
"Ikke i stand til at mounte lognings filsystemet.",
/* TR_MOUNTING_SWAP_PARTITION */
"Mounter swap partitionen...",
/* TR_UNABLE_TO_MOUNT_SWAP_PARTITION */
"Ikke i stand til at mounte swap partitionen.",
/* TR_NETWORK_SETUP_FAILED */
"Fejl i netv�rksops�tningen.",
/* TR_NO_TARBALL_DOWNLOADED */
"Ingen tarball er downloadet.",
/* TR_INSTALLING_FILES */
"Installerer filer...",
/* TR_UNABLE_TO_INSTALL_FILES */
"Ikke i stand til at installere filer.",
/* TR_UNABLE_TO_REMOVE_TEMP_FILES */
"Ikke i stand til at fjerne midlertidige downloadede filer.",
/* TR_ERROR_WRITING_CONFIG */
"Fejl under skrivning af konfigurations informationer.",
/* TR_INSTALLING_LILO */
"Installerer LILO...",
/* TR_UNABLE_TO_INSTALL_LILO */
"Ikke i stand til at installere LILO.",
/* TR_UNABLE_TO_UNMOUNT_HARDDISK */
"Ikke i stand til at unmounte harddisken.",
/* TR_UNABLE_TO_UNMOUNT_CDROM */
"Ikke i stand til at unmounte CDROM/floppydisk.",
/* TR_UNABLE_TO_EJECT_CDROM */
"Ikke i stand til at skubbe cd skuffen ud.",
/* TR_CONGRATULATIONS */
"Tillykke!",
/* TR_CONGRATULATIONS_LONG */
"Smoothwall blev succesfuldt installeret. Fjern venligst alle floppy disketter eller " \
"CDROMer i computeren. Ops�tningsprogrammet vil nu k�re der hvor du kan konfigurere din ISDN, " \
" netv�rks kort, og system kodeord. Efter at ops�tningsprogrammet er fuldf�rt, " \
"skal du i din web browsers adresse felt skrive http://smoothwall:81 eller " \
"https://smoothwall:445 (eller hvad du nu har kaldt din Smoothwall), og konfigurere " \
"opkalds netv�rk (hvis n�dvendigt) og fjern-adgang. Husk at s�tte " \
"et kodeord til Smoothwall 'opkalds' bruger, hvis du �nsker at det skal v�re muligt for ikke Smoothwall " \
"'admin' brugere at kontrollere opkaldsforbindelsen.",
/* TR_PRESS_OK_TO_REBOOT */
"Tryk Ok for at genstarte.",
/* TR_ERROR */
"Fejl",
/* TR_CALCULATING_MODULE_DEPENDANCIES */
"Udregner modul afh�ngigheder...",
/* TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES */
"Ikke i stand til at udrege modul afh�ngigheder.",

/* cdrom.c */
/* TR_SELECT_CDROM_TYPE */
"V�lg CDROM type",
/* TR_SELECT_CDROM_TYPE_LONG */
"Ingen IDE CDROM blev fundet p� denne maskine.  V�lg venligst hvilket " \
"af de f�lgende drivere du �nsker at bruge s� Smoothwall kan f� adgang til CDROMen.",
/* TR_SUGGEST_IO (%x is an IO number) */
"(foresl� %x)",
/* TR_SUGGEST_IRQ (%d is an IRQ number) */
"(foresl� %d)",
/* TR_CONFIGURE_THE_CDROM */
"Konfigurer CDROMen ved at v�lge den passende IO adresse og/eller IRQ.",
/* TR_INVALID_IO (note extra space) */
"Detaljerne indtastet for IO porten er ugyldige. ",
/* TR_INVALID_IRQ */
"Indtastede IRQ detaljer er ugyldige.",

/* config.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_SETTINGS */
"Ikke i stand til at skrive til /var/smoothwall/main/settings.",
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_ETHERNET_SETTINGS */
"Ikke i stand til at skrive til /var/smoothwall/ethernet/settings.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK */
"Ikke i stand til at skabe symlink /dev/harddisk.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1 */
"Ikke i stand til skabe symlink /dev/harddisk1.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2 */
"Ikke i stand til at skabe symlink /dev/harddisk2.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3 */
"Ikke i stand til at skabe symlink /dev/harddisk3.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4 */
"Ikke i stand til at skabe symlink /dev/harddisk4.",

/* net.c */
/* TR_DOWNLOADING */
"Downloader...",
/* TR_FAILED_TO_DOWNLOAD */
"Fejl opstod under downloadning.",
/* TR_ENTER_URL */
"Indtast URL'en til Smoothwall tar.gz filen. " \
"ADVARSEL: DNS ikke tilg�ngelig!  Dette skulle ende med filen 'smoothwall.tgz'.",

/* nic.c */
/* TR_CONFIGURE_NETWORKING */
"Konfigurer netv�rket",
/* TR_CONFIGURE_NETWORKING_LONG */
"Du skal nu konfigurere netv�rket ved f�rst at indl�se den korrekte driver til" \
"den GR�NNE gr�nseflade (interface). Du kan g�re dette enten ved auto-check for et" \
"netv�rkskort, eller ved at v�lge den korrekte driver fra en liste. Bem�rk, at hvis" \
"du har mere end et netv�rkskort installeret, kan du konfigurere de andre senere" \
"i installationen. Bem�rk ogs�, at hvis du har mere end et kort som er af samme " \
"type som det GR�NNE og hvis hvert kort kr�ver specielle modul parametre, " \
"b�r du indtaste disse parametre for alle kort af denne type, "  \
"s� alle kort bliver aktive n�r du konfigurerer det GR�NNE interface.",
/* TR_INTERFACE_FAILED_TO_COME_UP */
"Interfacet (gr�nsefladen) kunne ikke startes.",
/* TR_ENTER_NETWORK_DRIVER */
"Kunne ikke finde et netv�rkskort automatisk. Indtast driveren og " \
"yderligere parametre for netv�rkskortet.",

/*********/
/* SETUP */
/*********/

/* main.c */
/* TR_HOSTNAME */
"V�rtsnavn",
/* TR_NETWORKING */
"Netv�rket",
/* TR_DHCP_SERVER_CONFIGURATION */
"DHCP server konfiguration",
/* TR_ISDN_CONFIGURATION */
"ISDN Konfiguration",
/* TR_ROOT_PASSWORD */
"\'root\' kodeord",
/* TR_SETUP_PASSWORD */
"\'setup\' kodeord",
/* TR_ADMIN_PASSWORD */
"Admin kodeord",
/* TR_SECTION_MENU */
"Sektions menu",
/* TR_SELECT_THE_ITEM */
"V�lg den enhed du �nsker at konfigurere.",
/* TR_SETUP_FINISHED */
"Ops�tingen er fuldf�rt.  Tryk Ok for at genstarte.",
/* TR_SETUP_NOT_COMPLETE */
"Den f�rste ops�ting blev ikke helt fuldf�rt.  Du m� sikre at Ops�tingen bliver " \
"fuldst�ndig k�rt igennem ved at k�re Ops�tningen igen i shell'en.",

/* passwords.c */
/* TR_ENTER_ROOT_PASSWORD */
"Indtast 'root' bruger kodeordet. Log p� som denne bruger for at f� kommandolinie adgang.",
/* TR_SETTING_ROOT_PASSWORD */
"Indstiller 'root' kodeordet....",
/* TR_PROBLEM_SETTING_ROOT_PASSWORD */
"Problem med at indstille 'root' kodeordet.",
/* TR_ENTER_SETUP_PASSWORD */
"Indstast 'setup' bruger kodeordet. Log p� som denne bruger for at f� adgang til ops�tnings " \
"programmet.",
/* TR_SETTING_SETUP_PASSWORD */
"Indstiller 'setup' kodeordet....",
/* TR_PROBLEM_SETTING_SETUP_PASSWORD */
"Problem med at indstille 'setup' kodeord.",
/* TR_ENTER_ADMIN_PASSWORD */
"Indtast Smoothwall admin kodeord.  Det er denne bruger der bruges " \
"til at logge p� Smoothwalls web administration sider.",
/* TR_SETTING_ADMIN_PASSWORD */
"Indstiller Smoothwall admin kodeordet....",
/* TR_PROBLEM_SETTING_ADMIN_PASSWORD */
"Problem med at indstille Smoothwalls admin kodeord.",
/* TR_PASSWORD_PROMPT */
"Kodeord:",
/* TR_AGAIN_PROMPT */
"Igen:",
/* TR_PASSWORD_CANNOT_BE_BLANK */
"Kodeord kan ikke v�re blankt.",
/* TR_PASSWORDS_DO_NOT_MATCH */
"De indtastede kodeord er ikke ens.",

/* hostname.c */
/* TR_ENTER_HOSTNAME */
"Indtast maskinens v�rtsnavn.",
/* TR_HOSTNAME_CANNOT_BE_EMPTY */
"V�rtsnavns feltet kan ikke v�re tomt.",
/* TR_HOSTNAME_CANNOT_CONTAIN_SPACES */
"V�rtsnavn kan ikke indeholde mellemrum.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTNAME */
"Kan ikke skrive til /etc/hostname",

/* isdn.c */
/* TR_GERMAN_1TR6 */
"Tysk 1TR6",
/* TR_EURO_EDSS1 */
"Euro (EDSS1)",
/* TR_LEASED_LINE */
"Lejet linie",
/* TR_US_NI1 */
"US NI1",
/* TR_PROTOCOL_COUNTRY */
"Protokol/Land",
/* TR_ISDN_CARD */
"ISDN kort",
/* TR_MSN_CONFIGURATION */
"Lokalt telefon nummer (MSN/EAZ)",
/* TR_SET_ADDITIONAL_MODULE_PARAMETERS */
"Ops�t yderligere modul parametre",
/* TR_RED_IN_USE */
"ISDN (eller anden extern forbindelse) er i �jeblikket i brug.  Du kan ikke " \
"koconfigurere ISDN, mens det R�DE interface er aktivt.",
/* TR_ISDN_CONFIGURATION_MENU */
"ISDN konfigurations menu",
/* TR_ISDN_STATUS */
"ISDN er i �jeblikket %s.\n\n" \
"   Protokol: %s\n" \
"   Kort: %s\n" \
"   Lokalt telefon nummer: %s\n\n" \
"V�lg den endhed du �nsker at omkonfigurere, eller v�lg at bruge de nuv�rende indstillinger.",
/* TR_ISDN_NOT_YET_CONFIGURED */
"ISDN er ikke konfigureret endnu. V�lg det emne som du vil konfigurere.",
/* TR_ENABLE_ISDN */
"Sl� ISDN til",
/* TR_DISABLE_ISDN */
"Sl� ISDN fra",
/* TR_INITIALISING_ISDN */
"Initialiserer ISDN...",
/* TR_UNABLE_TO_INITIALISE_ISDN */
"Ude af stand til at initialisere ISDN.",
/* TR_ISDN_NOT_SETUP */
"ISDN ikke opsat. Nogle emner er ikke blevet valgt.",
/* TR_ISDN_PROTOCOL_SELECTION */
"ISDN protokol valg",
/* TR_CHOOSE_THE_ISDN_PROTOCOL */
"V�lg den ISDN protokol du vil have.",
/* TR_AUTODETECT */
"* AUTO-FIND *",
/* TR_ISDN_CARD_SELECTION */
"ISDN kard valg",
/* TR_CHOOSE_THE_ISDN_CARD_INSTALLED */
"V�lg det ISDN kort som er installeret i denne computer.",
/* TR_CHECKING_FOR */
"Unders�ger: %s",
/* TR_ISDN_CARD_NOT_DETECTED */
"ISDN kort ikke detekteret. Du kan v�re n�dt til at specificere yderligere " \
"modul parametre, hvis kortet er et ISA kort eller kr�ver specielle indstillinger.",
/* TR_DETECTED */
"Fandt et: %s",
/* TR_UNABLE_TO_FIND_AN_ISDN_CARD */
"ISDN kort ikke finde. Du kan v�re n�dt til at specificere yderligere " \
"modul parametre, hvis kortet er et ISA kort eller kr�ver specielle indstillinger.",
/* TR_ENTER_THE_LOCAL_MSN */
"Indtast det lokale telefon nummer (MSN/EAZ).",
/* TR_PHONENUMBER_CANNOT_BE_EMPTY */
"Telefonnummer kan ikke v�re tomt.",
/* TR_ENTER_ADDITIONAL_MODULE_PARAMS */
"Nogle ISDN kort (is�r ISA modeller) kr�ver yderligere modul " \
"parametre for at indstille IRQ og IO adresse information. Hvis du har et s�dant " \
"ISDN kort, indtast disse extra parametre her. For eksampel: " \
"\"io=0x280 irq=9\". De vil blive brugt under kort detektering.",

/* networking.c */
/* TR_PUSHING_NETWORK_DOWN */
"Skubber netv�rk ned...",
/* TR_PULLING_NETWORK_UP */
"Tr�kker netv�rk op...",
/* TR_NETWORK_CONFIGURATION_TYPE */
"Netv�rks konfigurationstype",
/* TR_DRIVERS_AND_CARD_ASSIGNMENTS */
"Driver og kort tildelinger",
/* TR_ADDRESS_SETTINGS */
"Adresse indstillinger",
/* TR_DNS_AND_GATEWAY_SETTINGS */
"DNS og Gateway indstillinger",
/* TR_RESTART_REQUIRED */
"\n\nN�r konfigurationen er fuldf�rt, vil en genstart af netv�rket v�re n�dvendig.",
/* TR_CURRENT_CONFIG (first %s is type, second is restart message (or not) */
"Nuv�rende konfiguration: %s%s",
/* TR_NETWORK_CONFIGURATION_MENU */
"Netv�rks konfigurations menu",
/* TR_NETWORK_CONFIGURATION_TYPE_LONG */
"V�lg en netv�rks konfiguration til Smoothwall.  De f�lgende " \
"konfigurations typer viser de interfaces (gr�nseflader) som har ethernet tilsluttet. " \
"Hvis du �ndrer denne indstilling, vil det v�re n�dvendigt at genstarte netv�rket, og du " \
"vil v�re n�dt til at genkonfigurere netv�rksdriver tildelingerne.",
/* TR_PUSHING_NON_LOCAL_NETWORK_DOWN */
"Skubber ikke lokalt netv�rk ned...",
/* TR_YOUR_CONFIGURATION_IS_SINGLE_GREEN_ALREADY_HAS_DRIVER */
"Din konfiguration er indstillet til et enligt GR�NT interface, " \
"som allerede har en driver tildelt.",
/* TR_CONFIGURE_NETWORK_DRIVERS */
"Konfigurer netv�rk drivere, og hvilket interface hvert kort er " \
"tildelt til.  Den nuv�rende konfiguration er som f�lger:\n\n",
/* TR_DO_YOU_WISH_TO_CHANGE_THESE_SETTINGS */
"\n �nsker du at �ndre disse indstillinger?",
/* TR_UNCLAIMED_DRIVER */
"Der er et ikke tildelt ethernet kort af typen:\n%s\n\n" \
"Du kan tildele det til:",
/* TR_CARD_ASSIGNMENT */
"Kort tildeling",
/* TR_PROBE */
"Fors�g at finde ",
/* TR_SELECT */
"V�lg",
/* TR_NO_UNALLOCATED_CARDS */
"Ingen utildelte kort tilbage, " \
"der er brug for flere. Du bliver n�dt til at s�ge efter flere kort, eller " \
"V�lge at v�lge en driver fra listen.",
/* TR_UNABLE_TO_FIND_ANY_ADDITIONAL_DRIVERS */
"Ikke i stand til at finde yderligere drivere.",
/* TR_ALL_CARDS_SUCCESSFULLY_ALLOCATED */
"Alle kort er successfuldt allokeret.",
/* TR_NOT_ENOUGH_CARDS_WERE_ALLOCATED */
"For f� kort blev allokeret.",
/* TR_MANUAL */
"* MANUEL *",
/* TR_SELECT_NETWORK_DRIVER */
"V�lg netv�rks driver",
/* TR_SELECT_NETWORK_DRIVER_LONG */
"V�lg netv�rks driveren for det kort, som er installeret i denne maskine. " \
"Hvis du v�lger MANUEL, vil du f� mulighed for at indtaste " \
"driverens modul navn og parametre for de drivere som har " \
"specielle krav, s�som ISA kort.",
/* TR_UNABLE_TO_LOAD_DRIVER_MODULE */
"Ikke i stand til at indl�se driver modulet.",
/* TR_THIS_DRIVER_MODULE_IS_ALREADY_LOADED */
"Dette driver module er allerede indl�st.",
/* TR_MODULE_PARAMETERS */
"Indtast modul navn og parametre for den driver du eftersp�rger.",
/* TR_LOADING_MODULE */
"Indl�ser modul...",
/* TR_WARNING */
"ADVARSEL",
/* TR_WARNING_LONG */
"Hvis du �ndrer denne IP adresse, og du er logget ind via fjern-adgang, " \
"vil din forbindelse til Smoothwall maskinen blive afbrudt, og du vil " \
"skulle etablere forbindelse igen p� den nye IP. Dette er en risikofyldt operation, som kun " \
"b�r pr�ves, hvis du har fysisk adgang til Smoothwall maskinen, hvis noget " \
"skulle g� galt.",
/* TR_SINGLE_GREEN */
"Din konfiguration er opsat til et enkelt GR�NT interface.",
/* TR_SELECT_THE_INTERFACE_YOU_WISH_TO_RECONFIGURE */
"V�lg det interface du vil genkonfigurere.",
/* TR_DNS_GATEWAY_WITH_GREEN */
"Din konfiguration bruger ikke en ethernet adapter til " \
"dets R�DE interface.  DNS og Gateway information for opkaldsbrugere " \
"bliver konfigureret automatisk n�r der foretages opkald.",
/* TR_PRIMARY_DNS */
"Prim�r DNS:",
/* TR_SECONDARY_DNS */
"Sekund�r DNS:",
/* TR_DEFAULT_GATEWAY */
"Standard Gateway:",
/* TR_DNS_AND_GATEWAY_SETTINGS_LONG */
"Indtast DNS og gateway information.  Disse indstilliner bliver kun brugt hvis DHCP " \
"er sl�et fra p� det R�DE interface.",
/* TR_PRIMARY_DNS_CR */
"Prim�r DNS\n",
/* TR_SECONDARY_DNS_CR */
"Sekund�r DNS\n",
/* TR_DEFAULT_GATEWAY_CR */
"Standard Gateway\n",
/* TR_SECONDARY_WITHOUT_PRIMARY_DNS */
"Sekund�r DNS angivet uden at der er en Prim�r DNS",
/* TR_UNKNOWN */
"UKENDT",
/* TR_NO_ORANGE_INTERFACE */
"Intet ORANGE interface tildelt.",
/* TR_MISSING_ORANGE_IP */
"Manglende IP information for det ORANGE interface.",
/* TR_NO_RED_INTERFACE */
"Intet R�DT interface tildelt.",
/* TR_MISSING_RED_IP */
"Manglende IP information for det R�DE interface.",

/* dhcp.c */
/* TR_START_ADDRESS */
"Start adresse:",
/* TR_END_ADDRESS */
"Slut adresse:",
/* TR_DEFAULT_LEASE */
"Standard lease tid(min):",
/* TR_MAX_LEASE */
"Max lease tid(min):",
/* TR_DOMAIN_NAME_SUFFIX */
"Dom�ne navns suffix:",
/* TR_CONFIGURE_DHCP */
"Konfigurer DHCP serveren, ved at indtaste ops�tnings information.",
/* TR_START_ADDRESS_CR */
"Start adresse\n",
/* TR_END_ADDRESS_CR */
"Slut adresse\n",
/* TR_DEFAULT_LEASE_CR */
"Standard lease tid\n",
/* TR_MAX_LEASE_CR */
"Max lease tid\n",
/* TR_DOMAIN_NAME_SUFFIX_CR */
"Dom�ne navns suffix\n",

/* keymap.c */
/* TR_KEYBOARD_MAPPING */
"Tegns�t",
/* TR_KEYBOARD_MAPPING_LONG */
"V�lg den type tastatur du bruger fra nedenst�ende liste.",

/* timezone.c */
/* TR_TIMEZONE */
"Tidszone",
/* TR_TIMEZONE_LONG */
"V�lg den tidszone du er i fra nedenst�ende liste.",

/* usbadsl.c */
/* TR_USB_CONTROLLER */
"V�lg USB controlleren",
/* TR_USBADSL_STATUS */
"USB ADSL er i �jblikket: %s\n" \
"   Controller: %s\n\n" \
"V�lg det du vil genkonfigurere, eller v�lg at bruge nuv�rende indstillinger.",
/* TR_USBADSL_CONFIGURATION */
"USB ADSL konfiguration",
/* TR_ENABLE_USBADSL */
"Sl� USB ADSL til",
/* TR_DISABLE_USBADSL */
"Sl� USB ADSL fra",
/* TR_INITIALISING_USBADSL */
"Initialisirer USB ADSL.",
/* TR_UNABLE_TO_INITIALISE_USBADSL */
"Ikke i stand til at initialisere USB ADSL",
/* TR_USBADSL_NOT_SETUP */
"USB ADSL ikke sat op.",
/* TR_USB_CONTROLLER_SELECTION */
"USB controller valg",
/* TR_CHOOSE_THE_USB_CONTROLLER_INSTALLED */
"V�lg den USB controller som er installeret p� Smoothwall maskinen.",
/* TR_USB_CONTROLLER_NOT_DETECTED */
"USB controller ikke detekteret.",
/* TR_UNABLE_TO_FIND_A_USB_CONTROLLER */
"Ikke i stand til at finde en USB controller.",
/* TR_STARTING_UP_USBADSL */
"Starter USB ADSL op..."

};
