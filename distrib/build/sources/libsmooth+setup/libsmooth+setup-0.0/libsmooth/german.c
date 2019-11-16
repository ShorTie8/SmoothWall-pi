/* SmoothWall libsmooth.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * (c) German Translation Team:
 * Lukas Frey
 * Dirk Bergner
 * Ralf Stahlmann  
 * Sven Hummel
 * Boris Friedrichs
 * Sebastian Ahrens
 * Martin Schluter
 * Andrej Huschka
 * Ingo Bradtka
 * Georg Lorenz   
 * Jens Kruse    
 * Marcel Gsteiger
 * Dirk Siedle   
 * Arne Matzke
 * Dirk Schwilski 
 * Joerg Dulz   
 * Alexis Lawrence
 * Robert Krauss
 * Erkan Sapmaz
 * Detlef Braas 
 * Egino
 * Thomas Sempach
 * Heiko Rittelmeier
 * Florian Moesch
 * Gunther B�hm 
 *
 * filename: german.c
 * Contains german strings. */

#include "libsmooth.h"

/* char *english_tr[] = { Muss dies auch ersetzt werden ?? */

char *german_tr[] = {

/**********/
/* COMMON */
/**********/

/* TR_OK */
"Ok",
/* TR_CANCEL */
"Abbrechen",
/* TR_INSTALLATION_CANCELED */
"Installation abgebrochen.",
/* TR_HELPLINE */
"   mit <Tab>/<Alt-Tab> zwischen den Feldern umschalten | <Leertaste> w�hlt aus",
/* TR_QUIT */
"Verlassen",
/* TR_DISABLED */
"Ausgeschaltet",
/* TR_ENABLED */
"Eingeschaltet",
/* TR_UNSET */
"Nicht gesetzt",
/* TR_UNABLE_TO_OPEN_SETTINGS_FILE */
"Konfigurationsdatei nicht zu �ffnen",
/* TR_DONE */
"Erledigt",
/* TR_PROBE_FAILED */
"Automatische Erkennung missgl�ckt.",

/*************/
/* LIBSMOOTH */
/*************/

/* main.c  */

/* netstuff.c */
/* TR_IP_ADDRESS_PROMPT */
"IP-Adresse:",
/* TR_NETWORK_ADDRESS_PROMPT */
"Netzwerk Adresse:",
/* TR_NETMASK_PROMPT */
"Netzwerk Maske:",
/* TR_ENTER_IP_ADDRESS_INFO */
"Eingabe der IP-Adresse",
/* TR_INVALID_FIELDS */
"Die folgenden Felder sind ung�ltig:\n\n",
/* TR_IP_ADDRESS_CR */
"IP-Adresse\n",
/* TR_NETWORK_ADDRESS_CR */
"Netzwerk Adresse\n",
/* TR_NETWORK_MASK_CR */
"Netzwerk Maske\n",
/* TR_INTERFACE (%s is interface name) */
"%s Schnittstelle",
/* TR_ENTER_THE_IP_ADDRESS_INFORMATION (%s is interface name) */
"Eingabe der IP-Adresse f�r die %s-Schnittstelle.",
/* TR_LOOKING_FOR_NIC (%s is a nic name) */
"Suche nach: %s",
/* TR_FOUND_NIC (%s is a nic name) */
"Smoothwall hat folgende Netzwerkkarte gefunden: %s",
/* TR_MODULE_NAME_CANNOT_BE_BLANK */
"Modulname muss eingetragen sein.",
/* TR_STATIC */
"Statisch",
/* TR_DHCP_HOSTNAME */
"DHCP Hostname:",
/* TR_DHCP_HOSTNAME_CR */
"DHCP Hostname\n",

/* misc.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_HOSTNAMECONF */
"Kann die Datei /var/smoothwall/main/hostname.conf nicht schreiben.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS */
"Kann die Datei /etc/hosts nicht schreiben.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_DENY */
"Kann die Datei /etc/hosts.deny nicht schreiben.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_ALLOW */
"Kann die Datei /etc/hosts.allow nicht schreiben.",
/* TR_UNABLE_TO_SET_HOSTNAME */
"Kann den Hostnamen nicht festlegen.",

/***********/
/* INSTALL */
/***********/
/* TR_WELCOME */
"Willkommen beim Smoothwall-Installationsprogramm. Besuchen Sie unsere Homepage " \
"http://www.smoothwall.org.  W�hlen Sie Abbruch in den nachfolgenden Bildschirmdialogen, " \
"um den Computer neu zu starten.",
/* TR_NO_IDE_HARDDISK */
"Keine IDE-Festplatte gefunden.",
/* TR_SELECT_INSTALLATION_MEDIA */
"Bitte w�hlen Sie das Installationsmedium",
/* TR_SELECT_INSTALLATION_MEDIA_LONG */
"Sie k�nnen Smoothwall ab verschiedenen Quellen installieren. Am einfachsten " \
"verwenden Sie das lokale CD-ROM Laufwerk. Fehlt dieses, k�nnen Sie von einer anderen " \
"Arbeitsstation im Netzwerk installieren, welche die Installationsdateien via HTTP " \
"zug�nglich macht. In diesem Fall ben�tigen Sie die " \
" Netzwerk-Treiberdiskette.",
/* TR_NO_IDE_CDROM */
"Kein IDE CD-ROM gefunden.",
/* TR_INSERT_CDROM */
"Bitte legen Sie die Smoothwall CD in das CD-ROM Laufwerk ein.",
/* TR_INSERT_FLOPPY */
"Bitte legen Sie die Smoothwall Treiberdiskette in das Diskettenlaufwerk ein.",
/* TR_PREPARE_HARDDISK */
"Nun wird die IDE-Festplatte auf %s vorbereitet. " \
"Zun�chst wird die Festplatte partitioniert, danach wird ein Dateisystem " \
"aufgebracht.",
/* TR_PARTITIONING_DISK */
"Festplatte wird partitioniert...",
/* TR_UNABLE_TO_PARTITION */
"Festplatte kann nicht partitioniert werden.",
/* TR_MAKING_SWAPSPACE */
"Einrichtung von Festplattenspeicher f�r die Auslagerung (swap space)...",
/* TR_UNABLE_TO_MAKE_SWAPSPACE */
"Festplattenspeicher f�r die Auslagerung (swap space) kann nicht eingerichtet werden.",
/* TR_MAKING_ROOT_FILESYSTEM */
"Erstellen des root-Filesystems...",
/* TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM */
"root-Filesystem kann nicht erstellt werden.",
/* TR_MOUNTING_ROOT_FILESYSTEM */
"Mounten des root-Filesystems...",
/* TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM */
"root-Filesystem kann nicht gemounted werden.",
/* TR_MAKING_BOOT_FILESYSTEM */
"Erstellen des boot-Filesystems...",
/* TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM */
"boot-Filesystem kann nicht erstellt werden.",
/* TR_MOUNTING_BOOT_FILESYSTEM */
"Mounten des boot-Filesystems...",
/* TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM */
"boot-Filesystem kann nicht gemounted werden.",
/* TR_MAKING_LOG_FILESYSTEM */
"Erstellen des log-Filesystems...",
/* TR_UNABLE_TO_MAKE_LOG_FILESYSTEM */
"log-Filesystem kann nicht erstellt werden.",
/* TR_MOUNTING_LOG_FILESYSTEM */
"Mounten des log-Filesystems...",
/* TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM */
"log-Filesystem kann nicht gemounted werden.",
/* TR_MOUNTING_SWAP_PARTITION */
"Mounten der swap-Partition...",
/* TR_UNABLE_TO_MOUNT_SWAP_PARTITION */
"swap-Partition kann nicht gemounted werden.",
/* TR_NETWORK_SETUP_FAILED */
"Netzwerksetup misslungen.",
/* TR_NO_TARBALL_DOWNLOADED */
"Kein tarball heruntergeladen.",
/* TR_INSTALLING_FILES */
"Dateien werden installiert...",
/* TR_UNABLE_TO_INSTALL_FILES */
"Dateien k�nnen nicht installiert werden.",
/* TR_UNABLE_TO_REMOVE_TEMP_FILES */
"Tempor�re heruntergeladene Datenen k�nnen nicht entfernt werden.",
/* TR_ERROR_WRITING_CONFIG */
"Fehler beim Schreiben der Konfigurationsinformationen.",
/* TR_INSTALLING_LILO */
"LILO wird installiert...",
/* TR_UNABLE_TO_INSTALL_LILO */
"LILO kann nicht installiert werden.",
/* TR_UNABLE_TO_UNMOUNT_HARDDISK */
"Fehler bei unmount der Festplatte.",
/* TR_UNABLE_TO_UNMOUNT_CDROM */
"Fehler bei unmount von CDROM/Floppy Disk.",
/* TR_UNABLE_TO_EJECT_CDROM */
"Fehler beim Auswurf der CD-ROM.",
/* TR_CONGRATULATIONS */
"Gratuliere!",
/* TR_CONGRATULATIONS_LONG */
"Sie haben nun Smoothwall erfolgreich installiert. Bitte entfernen Sie allf�llige Disketten oder " \
"CD-ROMs in den Laufwerken. Nun wird Setup gestartet, was Ihnen die Konfigurierung von ISDN, " \
"Netzwerkanschl�ssen und Systempassw�rtern erm�glichen wird. Nach Abschluss des Setup starten Sie bitte " \
"einen Webbrowser und �ffnen die Seite http://smoothwall:81 resp. https://smoothwall:445. " \
"Geben Sie dabei anstelle von \'smoothwall\' die IP-Adresse oder den von Ihnen gew�hlten Namen ein. Konfigurieren Sie danach " \
"die W�hlverbindungen (sofern gew�nscht) und den Fernzugriff. Wenn ein Nicht-Administrator (admin) die W�hlverbindungen " \
"zu bedienen hat, m�ssen Sie f�r den Benutzer \'dial\' ein Passwort definieren. Andernfalls bleibt ihm der Zugriff " \
"zur Steuerung der W�hlverbindungen verwehrt.",
/* TR_PRESS_OK_TO_REBOOT */
"Dr�cken Sie OK, um neu zu starten.",
/* TR_ERROR */
"Fehler",
/* TR_CALCULATING_MODULE_DEPENDANCIES */
"Bestimmen der Modulabh�ngigkeiten...",
/* TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES */
"Modulabh�ngigkeiten k�nnen nicht bestimmt werden.",

/* cdrom.c */
/* TR_SELECT_CDROM_TYPE */
"Typ des CD-ROM waehlen",
/* TR_SELECT_CDROM_TYPE_LONG */
"In Ihrem Rechner konnte kein IDE CD-ROM-Laufwerk gefunden werden.  Bitte " \
"waehlen Sie, welchen der folgenden Treiber Sie verwenden wollen, damit "\
"Smoothwall auf das Laufwerk zugreifen kann.",
/* TR_SUGGEST_IO (%x is an IO number) */
"(Vorschlag: %x)",
/* TR_SUGGEST_IRQ (%d is an IRQ number) */
"(Vorschlag %d)",
/* TR_CONFIGURE_THE_CDROM */
"Konfigurieren Sie das CD-ROM durch Angabe der I/O-Adresse und/oder des IRQ.",
/* TR_INVALID_IO (note extra space) */
"Die eingegebenen Daten ueber den I/O-Port sind ungueltig. ",
/* TR_INVALID_IRQ */
"Die eingegebenen Daten ueber den IRQ sind ungueltig.",

/* config.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_SETTINGS */
"Konnte /var/smoothwall/main/settings nicht erstellen.",
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_ETHERNET_SETTINGS */
"Konnte /var/smoothwall/ethernet/settings nicht erstellen.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK */
"Konnte den Link /dev/harddisk nicht erstellen.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1 */
"Konnte den Link /dev/harddisk1 nicht erstellen.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2 */
"Konnte den Link /dev/harddisk2 nicht erstellen.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3 */
"Konnte den Link /dev/harddisk3 nicht erstellen.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4 */
"Konnte den Link /dev/harddisk4 nicht erstellen.",

/* net.c */
/* TR_DOWNLOADING */
"Lade herunter...",
/* TR_FAILED_TO_DOWNLOAD */
"Download fehlgeschlagen.",
/* TR_ENTER_URL */
"Geben Sie die URL des Smoothwall .tar.gz-Archivs ein. " \
"WARNUNG: DNS nicht verfuegbar. Dies sollte mit der Datei 'smoothwall.tgz' enden.",

/* nic.c */
/* TR_CONFIGURE_NETWORKING */
"Netzwerk konfigurieren",
/* TR_CONFIGURE_NETWORKING_LONG */
"Sie sollten jetzt das Netzwerk konfigurieren, indem Sie zuerst den richtigen Treiber " \
"fuer die GRUENE Netzwerkkarte laden. Sie koennen dies entweder durch eine automatische "\
"Suche oder durch Auswahl des passenden Treibers aus der Liste machen."\
"Bitte beachten: Sollten Sie mehr als eine Netzwerkkarte in Ihrem Rechner "\
"installiert haben, so koennen Sie die anderen Karten spaeter im Installationsverlauf "\
"konfigurieren. Bitte beachten Sie weiter: Sollten Sie mehr als eine Netzwerkkarte "\
"des gleichen Typs wie die GRUENE installiert haben und jede Karte spezielle "\
"Modulparameter benoetigen, so sollten Sie die Parameter fuer alle Karten dieses "\
"Typs so eingeben, dass alle Karten aktiv werden koennen wenn Sie die GRUENE "\
"Karte konfigurieren. ",
/* TR_INTERFACE_FAILED_TO_COME_UP */
"Das Interface konnte nicht gestartet werden.",
/* TR_ENTER_NETWORK_DRIVER */
"Die automatische Suche nach einer Netzwerkkarte schlug fehl. Bitter geben Sie "\
"den Treiber und benoetigte optionale Parameter fuer Ihre Netzwerkkarte an.",

/*********/
/* SETUP */
/*********/

/* main.c */
/* TR_HOSTNAME */
"Rechnername",
/* TR_NETWORKING */
"Netzwerk",
/* TR_DHCP_SERVER_CONFIGURATION */
"DHCP-Server-Konfiguration",
/* TR_ISDN_CONFIGURATION */
"ISDN-Konfiguration",
/* TR_ROOT_PASSWORD */
"\'root\' Passwort",
/* TR_SETUP_PASSWORD */
"\'setup\' Passwort",
/* TR_ADMIN_PASSWORD */
"Admin Passwort",
/* TR_SECTION_MENU */
"Abschnittsmenu",
/* TR_SELECT_THE_ITEM */
"Waehlen Sie den Eintrag, den Sie konfigurieren wollen.",
/* TR_SETUP_FINISHED */
"Setup ist vollstaendig. Waehlen Sie OK um neu zu starten.",
/* TR_SETUP_NOT_COMPLETE */
"Die Installation war nicht vollstaendig. Sie muessen sicherstellen, dass das "\
"Setup komplett abgeschlossen wurde, indem Sie das Setup-Programm erneut von "\
"der Shell aus aufrufen.",

/* passwords.c */
/* TR_ENTER_ROOT_PASSWORD */
"Bitte geben Sie das Passwort des Benutzers 'root' ein. Melden Sie sich als "\
"'root' an um auf die Kommandozeile zuzugreifen.",
/* TR_SETTING_ROOT_PASSWORD */
"Setze das Passwort fuer 'root'....",
/* TR_PROBLEM_SETTING_ROOT_PASSWORD */
"Probleme beim Setzen des Passworts fuer 'root'.",
/* TR_ENTER_SETUP_PASSWORD */
"Geben Sie das Passwort des Benutzers 'setup' ein. Melden Sie sich als 'setup' "\
"an um auf das Setup-Programm zuzugreifen.",
/* TR_SETTING_SETUP_PASSWORD */
"Setze das Passwort fuer 'setup'....",
/* TR_PROBLEM_SETTING_SETUP_PASSWORD */
"Probleme beim Setzen des Passworts fuer 'setup'.",
/* TR_ENTER_ADMIN_PASSWORD */
"Bitte geben Sie das Passwort fuer den Smoothwall-Admin ein. Der Benutzer 'admin' "\
"ist fuer die Administration der Smoothwall ueber die Weboberflaeche vorgesehen.",
/* TR_SETTING_ADMIN_PASSWORD */
"Setze das Passwort fuer 'admin'....",
/* TR_PROBLEM_SETTING_ADMIN_PASSWORD */
"Probleme beim Setzen des Passworts fuer 'admin'.",
/* TR_PASSWORD_PROMPT */
"Passwort:",
/* TR_AGAIN_PROMPT */
"Wiederholung:",
/* TR_PASSWORD_CANNOT_BE_BLANK */
"Das Passwort darf nicht leer sein.",
/* TR_PASSWORDS_DO_NOT_MATCH */
"Die beiden Passwoerter stimmen nicht ueberein.",

/* hostname.c */
/* TR_ENTER_HOSTNAME */
"Geben Sie den Rechnernamen ein.",
/* TR_HOSTNAME_CANNOT_BE_EMPTY */
"Der Rechnername darf nicht leer sein.",
/* TR_HOSTNAME_CANNOT_CONTAIN_SPACES */
"Der Rechnername darf keine Leerzeichen enthalten.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTNAME */
"Konnte /etc/hostname nicht schreiben.",

/* isdn.c */
/* TR_GERMAN_1TR6 */
"1TR6 (Deutschland)",
/* TR_EURO_EDSS1 */
"Euro ISDN (EDSS1)",
/* TR_LEASED_LINE */
"Mietleitung (Leased line)",
/* TR_US_NI1 */
"US NI1",
/* TR_PROTOCOL_COUNTRY */
"Protokoll/Land",
/* TR_ISDN_CARD */
"ISDN - Karte",
/* TR_MSN_CONFIGURATION */
"lokale Telefonnummer (MSN/EAZ)",
/* TR_SET_ADDITIONAL_MODULE_PARAMETERS */
"zus�tzliche Modulparameter",
/* TR_RED_IN_USE */
"ISDN (oder eine andere externe Verbindung) wird zur Zeit benutzt.  Um ISDN konfigurieren zu k�nnen, " \
"darf die Schnittstelle ROT nicht aktiv sein.",
/* TR_ISDN_CONFIGURATION_MENU */
"ISDN Konfigurationsmen�",
/* TR_ISDN_STATUS */
"ISDN ist zur Zeit %s.\n\n" \
"   Protokoll: %s\n" \
"   Karte: %s\n" \
"   Lokale Telefonnummer: %s\n\n" \
"Bitte w�hlen Sie aus, was Sie neu konfigurieren m�chten oder �bernehmen Sie die aktuellen Einstellungen.",
/* TR_ISDN_NOT_YET_CONFIGURED */
"ISDN wurde noch nicht konfiguriert. Bitte w�hlen Sie die zu konfigurierenden Elemente aus.",
/* TR_ENABLE_ISDN */
"ISDN aktivieren",
/* TR_DISABLE_ISDN */
"ISDN deaktivieren",
/* TR_INITIALISING_ISDN */
"ISDN wird initialisiert...",
/* TR_UNABLE_TO_INITIALISE_ISDN */
"ISDN kann nicht initialisiert werden.",
/* TR_ISDN_NOT_SETUP */
"ISDN wurde nicht eingerichtet. Ein Teil der Einstellungen fehlt.",
/* TR_ISDN_PROTOCOL_SELECTION */
"ISDN Protokollauswahl",
/* TR_CHOOSE_THE_ISDN_PROTOCOL */
"Bitte w�hlen Sie Ihr zutreffendes ISDN-Protokoll aus.",
/* TR_AUTODETECT */
"* Selbsterkennung (AUTODETECT) *",
/* TR_ISDN_CARD_SELECTION */
"Auswahl der ISDN-Karte",
/* TR_CHOOSE_THE_ISDN_CARD_INSTALLED */
"Bitte geben Sie an, welcher Typ ISDN-Karte in diesem Computer installiert ist.",
/* TR_CHECKING_FOR */
"�berpr�fe Kartentyp: %s",
/* TR_ISDN_CARD_NOT_DETECTED */
"ISDN-Karte konnte nicht erkannt werden. Unter Umst�nden m�ssen Sie zus�tzliche Modulparameter angeben, " \
"z.B. bei einer ISA-Karte oder bei speziellen Erfordernissen der Karte.",
/* TR_DETECTED */
"Erkannter Kartentyp: %s",
/* TR_UNABLE_TO_FIND_AN_ISDN_CARD */
"In diesem Computer konnte keine ISDN-Karte erkannt werden. Unter Umst�nden m�ssen Sie zus�tzliche " \
"Modulparamter angeben, z.B. bei einer ISA-Karte oder bei speziellen Erfordernissen " \
"der Karte.",
/* TR_ENTER_THE_LOCAL_MSN */
"Bitte geben Sie die lokale Telefonnummer ein (MSN/EAZ).",
/* TR_PHONENUMBER_CANNOT_BE_EMPTY */
"Telefonnummereingabe ist obligatorisch.",
/* TR_ENTER_ADDITIONAL_MODULE_PARAMS */
"Ein Teil der ISDN-Karten (besonders ISA-Karten) erfordert unter Umst�nden zus�tzliche " \
"Modulparameter f�r Interrupt (IRQ) und Ein-/Ausgabeadressen (IO addresses). Falls eine solche Karte in diesem Sytem " \
"installiert ist, geben Sie diese zus�tzlichen Parameter bitte hier ein, z.B.: " \
"\"io=0x280 irq=9\". Diese Angaben werden anschliessend f�r die Kartenerkennung benutzt.",

/* networking.c */
/* TR_PUSHING_NETWORK_DOWN */
"Fahre das Netzwerk herunter...",
/* TR_PULLING_NETWORK_UP */
"Starte das Netzwerk...",
/* TR_NETWORK_CONFIGURATION_TYPE */
"Art der Netzwerkkonfiguration",
/* TR_DRIVERS_AND_CARD_ASSIGNMENTS */
"Treiber und Kartenzuordnung",
/* TR_ADDRESS_SETTINGS */
"Adresseinstellungen",
/* TR_DNS_AND_GATEWAY_SETTINGS */
"DNS- und Gatewayeinstellungen",
/* TR_RESTART_REQUIRED */
"\n\nNach Abschluss der Konfiguration muss das Netzwerk neu gestartet werden.",
/* TR_CURRENT_CONFIG (first %s is type, second is restart message (or not) */
"Aktuelle Konfiguration: %s%s",
/* TR_NETWORK_CONFIGURATION_MENU */
"Netzwerkkonfiguration",
/* TR_NETWORK_CONFIGURATION_TYPE_LONG */
"Waehlen Sie die Netzwerkkonfiguration von Smoothwall.  Die folgenden " \
"Konfigurationsarten zeigen die Schnittstellen, die eine Ethernetverbindung haben. " \
"Falls Sie diese Einstellung aendern, so wird ein Neustart des Netzwerks erforderlich  " \
"und Sie muessen die Treiberzuordnung rekonfigurieren.",
/* TR_PUSHING_NON_LOCAL_NETWORK_DOWN */
"Fahre das nicht-lokale Netzwerk herunter...",
/* TR_YOUR_CONFIGURATION_IS_SINGLE_GREEN_ALREADY_HAS_DRIVER */
"Ihre Konfiguration wurde fuer eine einzelne GRUENE Schnittstelle eingerichtet, " \
"der schon ein Treiber zugewiesen wurde.",
/* TR_CONFIGURE_NETWORK_DRIVERS */
"Konfigurieren Sie die Netzwerktreiber und welcher Schnittstelle welche Karte " \
"zugewiesen ist. Die aktuelle Konfiguration ist folgende:\n\n",
/* TR_DO_YOU_WISH_TO_CHANGE_THESE_SETTINGS */
"\nWollen Sie diese Einstellungen aendern?",
/* TR_UNCLAIMED_DRIVER */
"Es gibt eine nicht zugewiesene Netzwerkkarte des Typs:\n%s\n\n" \
"Sie koennen diese zuweisen an:",
/* TR_CARD_ASSIGNMENT */
"Kartenzuweisung",
/* TR_PROBE */
"Test",
/* TR_SELECT */
"Waehlen",
/* TR_NO_UNALLOCATED_CARDS */
"Keine nicht zugewiesene Karte mehr vorhanden, es werden noch mehr benoetigt. " \
"Sie koennen automatisch nach weiteren Karten suchen lassen oder aus der Liste " \
"einen Treiber waehlen.",
/* TR_UNABLE_TO_FIND_ANY_ADDITIONAL_DRIVERS */
"Es konnten keine weiteren Treiber gefunden werden.",
/* TR_ALL_CARDS_SUCCESSFULLY_ALLOCATED */
"Alle Netzwerkkarten wurden erfolgreich zugewiesen.",
/* TR_NOT_ENOUGH_CARDS_WERE_ALLOCATED */
"Es wurden nicht genuegend Netzwerkkarten zugewiesen.",
/* TR_MANUAL */
"* MANUELL *",
/* TR_SELECT_NETWORK_DRIVER */
"Netzwerktreiber auswaehlen",
/* TR_SELECT_NETWORK_DRIVER_LONG */
"Waehlen Sie den Netzwerktreiber fuer die in diesem Rechner installierte Netzwerkkarte. " \
"Falls Sie MANUELL waehlen, so koennen Sie den Namen des Treibermoduls und " \
"zusaetzliche erforderliche Parameter fuer den Treiber angeben, " \
"wie es zum Beispiel bei manchen ISA-Karten notwendig ist.",
/* TR_UNABLE_TO_LOAD_DRIVER_MODULE */
"Treibermodul konnte nicht geladen werden.",
/* TR_THIS_DRIVER_MODULE_IS_ALREADY_LOADED */
"Dieses Treibermodul ist bereits geladen.",
/* TR_MODULE_PARAMETERS */
"Geben Sie den Namen des Moduls und spezielle Parameter fuer den von Ihnen " \
"benoetigten Treiber an.",
/* TR_LOADING_MODULE */
"Modul wird geladen...",
/* TR_WARNING */
"WARNUNG",
/* TR_WARNING_LONG */
"Falls Sie diese IP-Adresse aendern, und Sie mittels einer Remote-Sitzung zugreifen, " \
"so wird Ihre Verbindung zur Smoothwall getrennt und Sie muessen sich erneut zur  " \
"neuen IP-Adresse verbinden. Diese Aktion ist riskant und Sie sollten dies nur tun " \
"wenn Sie physikalischen Zugriff auf den Rechner haben um Massnahmen ergreifen zu  " \
"koennen falls etwas nicht ordnungsgemaess funktioniert.",
/* TR_SINGLE_GREEN */
"Ihre Konfiguration wurde fuer eine einzelne gruene Netzwerkkarte eingerichtet.",
/* TR_SELECT_THE_INTERFACE_YOU_WISH_TO_RECONFIGURE */
"Waehlen Sie die Schnittstelle, die Sie neu konfigurieren wollen.",
/* TR_DNS_GATEWAY_WITH_GREEN */
"Ihre Konfiguration verwendet keine Netzwerkkarte fuer die ROTE Schnittstelle. " \
"DNS- und Gatewayeinstellungen werden automatisch bei der Einwahl vorgenommen.",
/* TR_PRIMARY_DNS */
"Erster DNS:",
/* TR_SECONDARY_DNS */
"Zweiter DNS:",
/* TR_DEFAULT_GATEWAY */
"Standardgateway:",
/* TR_DNS_AND_GATEWAY_SETTINGS_LONG */
"Bitte geben Sie die DNS- und Gatewayinformationen an. Diese Einstellungen " \
"werden nur verwendet, falls DHCP an der ROTEN Schnittstelle deaktiviert wurde.",
/* TR_PRIMARY_DNS_CR */
"Erster DNS\n",
/* TR_SECONDARY_DNS_CR */
"Zweiter DNS\n",
/* TR_DEFAULT_GATEWAY_CR */
"Standardgateway\n",
/* TR_SECONDARY_WITHOUT_PRIMARY_DNS */
"Es wurde ein Sekundaerer DNS ohne Angabe eines Primaeren DNS definiert",
/* TR_UNKNOWN */
"UNBEKANNT",
/* TR_NO_ORANGE_INTERFACE */
"Keine ORANGE Schnittstelle zugewiesen.",
/* TR_MISSING_ORANGE_IP */
"Fehlende IP-Informationen bei der ORANGENEN Schnittstelle.",
/* TR_NO_RED_INTERFACE */
"Keine ROTE Schnittstelle zugewiesen.",
/* TR_MISSING_RED_IP */
"Fehlende IP-Informationen bei der ROTEN Schnittstelle.",

/* dhcp.c */
/* TR_START_ADDRESS */
"Start address:",
/* TR_END_ADDRESS */
"End address:",
/* TR_DEFAULT_LEASE */
"Default lease (mins):",
/* TR_MAX_LEASE */
"Max lease (mins):",
/* TR_DOMAIN_NAME_SUFFIX */
"Domain name suffix:",
/* TR_CONFIGURE_DHCP */
"Configure the DHCP server by entering the settings information.",
/* TR_START_ADDRESS_CR */
"Start address\n",
/* TR_END_ADDRESS_CR */
"End address\n",
/* TR_DEFAULT_LEASE_CR */
"Default lease time\n",
/* TR_MAX_LEASE_CR */
"Max lease time\n",
/* TR_DOMAIN_NAME_SUFFIX_CR */
"Domain name suffix\n",

/* keymap.c */
/* TR_KEYBOARD_MAPPING */
"Keyboard mapping",
/* TR_KEYBOARD_MAPPING_LONG */
"Choose the type of keyboard you are using from the list below.",

/* timezone.c */
/* TR_TIMEZONE */
"Timezone",
/* TR_TIMEZONE_LONG */
"Choose the timezone you are in from the list below.",

/* usbadsl.c */
/* TR_USB_CONTROLLER */
"Select the USB controller",
/* TR_USBADSL_STATUS */
"USB ADSL is currently: %s\n" \
"   Controller: %s\n\n" \
"Select the item you wish to reconfigure, or choose to use the current settings.",
/* TR_USBADSL_CONFIGURATION */
"USB ADSL configuration",
/* TR_ENABLE_USBADSL */
"Enable USB ADSL",
/* TR_DISABLE_USBADSL */
"Disable USB ADSL",
/* TR_INITIALISING_USBADSL */
"Initialising USB ADSL.",
/* TR_UNABLE_TO_INITIALISE_USBADSL */
"Unable to initialise USB ADSL",
/* TR_USBADSL_NOT_SETUP */
"USB ADSL not setup.",
/* TR_USB_CONTROLLER_SELECTION */
"USB controller selection",
/* TR_CHOOSE_THE_USB_CONTROLLER_INSTALLED */
"Choose the USB controller installed in the Smoothwall machine.",
/* TR_USB_CONTROLLER_NOT_DETECTED */
"USB controller not detected.",
/* TR_UNABLE_TO_FIND_A_USB_CONTROLLER */
"Unable to find a USB controller.",
/* TR_STARTING_UP_USBADSL */
"Starting up USB ADSL..."

};
