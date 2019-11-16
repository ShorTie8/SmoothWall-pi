/* SmoothWall libsmooth.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * filename: hungarian.c
 * Contains hungarain strings. */

#include "libsmooth.h"

char *hungarian_tr[] = {

/**********/
/* COMMON */
/**********/

/* TR_OK */
"Ok",
/* TR_CANCEL */
"Megszakit�s",
/* TR_INSTALLATION_CANCELED */
"A telepit�s megszakadt",
/* TR_HELPLINE */
"                 <Tab>/<Alt-Tab> mozg�s   |  <Space> kiv�laszt�s",
/* TR_QUIT */
"Kil�p�s",
/* TR_DISABLED */
"Tiltva",
/* TR_ENABLED */
"Enged�lyezve",
/* TR_UNSET */
"NINCS BE�LLITVA",
/* TR_UNABLE_TO_OPEN_SETTINGS_FILE */
"Nem lehet megnyitni a be�llit�sokat tartalmaz� f�jlt",
/* TR_DONE */
"K�sz",
/* TR_PROBE_FAILED */
"Az automatikus felismer�s sikertelen",

/*************/
/* LIBSMOOTH */
/***** ********/

/* main.c  */

/* netstuff.c */
/* TR_IP_ADDRESS_PROMPT */
"IP cim:",
/* TR_NETWORK_ADDRESS_PROMPT */
"H�l�zati cim:",
/* TR_NETMASK_PROMPT */
"H�lozati maszk:",
/* TR_ENTER_IP_ADDRESS_INFO */
"K�rem az IP cim inform�ciokat",
/* TR_INVALID_FIELDS */
"A k�vetkez� mez�k �rv�nytelenek:\n\n",
/* TR_IP_ADDRESS_CR */
"IP cim\n",
/* TR_NETWORK_ADDRESS_CR */
"H�l�zati cim\n",
/* TR_NETWORK_MASK_CR */
"H�l�zati maszk mask\n",
/* TR_INTERFACE (%s is interface name) */
"%s interface",
/* TR_ENTER_THE_IP_ADDRESS_INFORMATION (%s is interface name) */
"K�rem az IP cim inform�ci�kat a  %s interface sz�m�ra.",
/* TR_LOOKING_FOR_NIC (%s is a nic name) */
"Keresem: %s",
/* TR_FOUND_NIC (%s is a nic name) */
"A Smoothwall a k�vetkez� k�rty�t ismerte fel a g�pben: %s",
/* TR_MODULE_NAME_CANNOT_BE_BLANK */
"A moduln�v nem lehet �res.",
/* TR_STATIC */
"Statikus",
/* TR_DHCP_HOSTNAME */
"DHCP Hostn�v:",
/* TR_DHCP_HOSTNAME_CR */
"DHCP Hostn�v\n",

/* misc.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_HOSTNAMECONF */
"Nem lehet irni a /var/smoothwall/main/hostname.conf",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS */
"Nem lehet irni /etc/hosts.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_DENY */
"nem lehet irni /etc/hosts.deny.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_ALLOW */
"Nem lehet irni  /etc/hosts.allow.",
/* TR_UNABLE_TO_SET_HOSTNAME */
"Nem lehet be�llitani a hostnevet.",

/***********/
/* INSTALL */
/***********/
/* TR_WELCOME */
"K�sz�nti a Smoothwall install�l� program. K�rj�k l�togassa meg " \
"honlapunkat a  http://www.smoothwall.org cimen.  A Megszakit kiv�laszt�s�val " \
"ujraindul a sz�mit�g�p.",
/* TR_NO_IDE_HARDDISK */
"Nem tal�ltam IDE hard discet.",
/* TR_SELECT_INSTALLATION_MEDIA */
"V�lasszon telepit�si mediumot",
/* TR_SELECT_INSTALLATION_MEDIA_LONG */
"A Smoothwall t�bbf�le forr�sb�l install�lhat�. A legegyszer�bb ha " \
"CDROM drive-rol telepitjuk. Ha nincs ilyen�nk akkor " \
"h�lozaton kereszt�l is telepithetjuk egy masik gepr�l,melyen az install�l� f�jlok  " \
"el�rhet�k HTTP-n kereszt�l. Ebben az esetben sz�ks�g van a h�l�zati driverek " \
"lemez�re.",
/* TR_NO_IDE_CDROM */
"Nem tal�ltam IDE CD-Rom-ot.",
/* TR_INSERT_CDROM */
"K�rem helyezze be a Smoothwall CD-t a meghajtoba.",
/* TR_INSERT_FLOPPY */
"K�rem helyezze a Smoothwall driver disket a floppy drive-ba.",
/* TR_PREPARE_HARDDISK */
"Az install�l� program el�k�sziti a hard disket  %s. " \
"El�sz�r a lemez particion�l�s t�rt�nik meg," \
"majd f�jlrendszer ker�l r�juk.",
/* TR_PARTITIONING_DISK */
"Perticion�lom a lemezt...",
/* TR_UNABLE_TO_PARTITION */
"Nem lehet particion�lni a lemezt.",
/* TR_MAKING_SWAPSPACE */
"A swap elk�szit�se...",
/* TR_UNABLE_TO_MAKE_SWAPSPACE */
"Nem lehet elk�sziteni a swap ter�letet.",
/* TR_MAKING_ROOT_FILESYSTEM */
"A root f�jlrendszer kialakit�sa...",
/* TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM */
"Nem lehet kialakitani a root f�jlrendszert.",
/* TR_MOUNTING_ROOT_FILESYSTEM */
"A root f�jlrendszer mountol�sa...",
/* TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM */
"Nem lehet mountolni a root f�jlrendszert.",
/* TR_MAKING_BOOT_FILESYSTEM */
"A boot f�jlrendszer kialakit�sa...",
/* TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM */
"Nem lehet kialakitani a boot f�jlredszert.",
/* TR_MOUNTING_BOOT_FILESYSTEM */
"A boot f�jlredszer mountol�sa...",
/* TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM */
"Mem lehet mountolni a boot f�jlrendszert.",
/* TR_MAKING_LOG_FILESYSTEM */
"A log f�jlrendszer kailakit�sa...",
/* TR_UNABLE_TO_MAKE_LOG_FILESYSTEM */
"Nem lehet kialakitani a log f�jlrendszert.",
/* TR_MOUNTING_LOG_FILESYSTEM */
"A log f�jlrendszer mountol�sa...",
/* TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM */
"Nem lehet mountolni a log f�jlrendszert.",
/* TR_MOUNTING_SWAP_PARTITION */
"A swap particio mountol�sa...",
/* TR_UNABLE_TO_MOUNT_SWAP_PARTITION */
"Nem lehet mountolni a swap particiot.",
/* TR_NETWORK_SETUP_FAILED */
"A h�lozat be�llit�sa nem siker�lt.",
/* TR_NO_TARBALL_DOWNLOADED */
"Nincs let�lthet� tar f�jl.",
/* TR_INSTALLING_FILES */
"F�jlok telepit�se...",
/* TR_UNABLE_TO_INSTALL_FILES */
"Nem lehet a f�jlokat telepiteni.",
/* TR_UNABLE_TO_REMOVE_TEMP_FILES */
"Nem lehet elt�volitani az ideiglenesen let�lt�tt f�jlokat.",
/* TR_ERROR_WRITING_CONFIG */
"Huiba a konfigur�ci�s f�jl ir�sakor.",
/* TR_INSTALLING_LILO */
" A LILO install�l�sa...",
/* TR_UNABLE_TO_INSTALL_LILO */
"Nem lehet a LILO-t install�lni.",
/* TR_UNABLE_TO_UNMOUNT_HARDDISK */
"Nem lehet unmountolni a harddisket.",
/* TR_UNABLE_TO_UNMOUNT_CDROM */
"Nem lehet unmountolni a CDROM-ot vagy a floppyt.",
/* TR_UNABLE_TO_EJECT_CDROM */
"Nem lehet kiadni a CDROM.",
/* TR_CONGRATULATIONS */
"Gratul�lunk!",
/* TR_CONGRATULATIONS_LONG */
"A Smoothwall szerencs�sen install�l�dott. K�rj�k vegye ki a floppy lemezt vagy a " \
"Cd lemezt a sz�mit�g�pb�l. A Setup program fog elindulni, amellyel be�llithatjuk az ISDN-t," \
" a h�l�zati k�rty�kat �s a rendszer jelszavait. Miut�n a Setup program" \
"befejez�d�tt, a web b�ng�sz�dbe ird a k�vetkez�ket:  http://smoothwall:81 vagy " \
"https://smoothwall:445 (vagy ami a Smoothwall g�p hostneve), �s �llitsd be  " \
"a t�rcs�z� hozz�f�r�st(ha sz�ks�ges) �s a t�voli hozz�f�r�st. Ne felejtsd el be�llitani " \
"a 'dial' felhaszn�l� jelszav�t, ha nem a Smoothwall " \
"'admin' felhaszn�l�i vez�rlik a t�rcs�z�st.",
/* TR_PRESS_OK_TO_REBOOT */
"Nyomj Ok-t az ujraindit�shoz.",
/* TR_ERROR */
"Hiba",
/* TR_CALCULATING_MODULE_DEPENDANCIES */
"A mudulf�gg�s�gek kisz�mit�sa...",
/* TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES */
"Nem lehet a modulf�gg�s�geket kisz�mitani.",

/* cdrom.c */
/* TR_SELECT_CDROM_TYPE */
"V�lassz CDROM tipust",
/* TR_SELECT_CDROM_TYPE_LONG */
"Nincs IDE CDROM a rendszerben. V�laszd ki a k�vetkez�k k�z�l " \
"a megfelel�t, hogy a Smoothwall hozz� tudjon f�rni.",
/* TR_SUGGEST_IO (%x is an IO number) */
"(javasolt %x)",
/* TR_SUGGEST_IRQ (%d is an IRQ number) */
"(javasolt %d)",
/* TR_CONFIGURE_THE_CDROM */
"�llitsd be a CDROM-ot a megfelel� IO cimmel , �s/vagy IRQ-val.",
/* TR_INVALID_IO (note extra space) */
"Az IO port �rv�nytelen. ",
/* TR_INVALID_IRQ */
"Az IRQ �rv�nytelen.",

/* config.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_SETTINGS */
"Nem lehet irni /var/smoothwall/main/settings.",
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_ETHERNET_SETTINGS */
"Nem lehet irni  /var/smoothwall/ethernet/settings.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK */
"Nem lehet szimlinket k�sziteni /dev/harddisk.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1 */
"Nem lehet szimlinket k�sziteni /dev/harddisk1.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2 */
"Nem lehet szimlinket k�sziteni /dev/harddisk2.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3 */
"Nem lehet szimlinket k�sziteni /dev/harddisk3.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4 */
"Unable to create symlink /dev/harddisk4.",

/* net.c */
/* TR_DOWNLOADING */
"Let�lt�s...",
/* TR_FAILED_TO_DOWNLOAD */
"A let�lt�s nem siker�lt.",
/* TR_ENTER_URL */
"Ird be a Smoothwall tar.gz f�jl el�r�si hely�t. " \
"FIGYELEM: DNS nem hozz�f�rhet�!  'smoothwall.tgz'-vel kell v�gz�dni a cimnek.",

/* nic.c */
/* TR_CONFIGURE_NETWORKING */
"A h�lozat be�llit�sa",
/* TR_CONFIGURE_NETWORKING_LONG */
"Most konfigur�lnod kell a h�lozatot, el�sz�r a megfelel� meghajt�t kell bet�lteni a " \
"GREEN interf�sz sz�m�ra. Megteheted ezt a h�lozati k�rtya automatikus felismer�s�vel " \
"vagy a megfelel� driver list�bol valo kiv�laszt�s�val. Ha t�bb mind egy k�rty�d van " \
"a k�s�bbiekben lesz lehet�s�ged, hogy a t�bbit is konfigur�ld" \
" Tov�bb� megjegyezz�k, ha t�bb k�rty�d van, amely " \
"azonos tipusu mint a GREEN interf�sz akkkor mindegyik k�rty�nak speci�lis " \
"param�terekre van sz�ks�ge, minden ilyen tipusu k�rty�nak meg kell adni a param�tereket "  \
"igy minden k�rtya aktiv�l�dik amikor a GREEN interf�szt be�llitod.",
/* TR_INTERFACE_FAILED_TO_COME_UP */
"Az interf�sz nem aktiv.",
/* TR_ENTER_NETWORK_DRIVER */
"Nem siker�lt a h�l�zati k�rtya automatikus felismer�se. Ird be a driver �s  " \
"param�tereket a h�l�zati k�rtya sz�m�ra.",

/*********/
/* SETUP */
/*********/

/* main.c */
/* TR_HOSTNAME */
"Hostn�v",
/* TR_NETWORKING */
"H�l�zat",
/* TR_DHCP_SERVER_CONFIGURATION */
"DHCP szerver konfiguraci�",
/* TR_ISDN_CONFIGURATION */
"ISDN konfigur�ci�",
/* TR_ROOT_PASSWORD */
"\'root\' jelsz�",
/* TR_SETUP_PASSWORD */
"\'setup\' jelsz�",
/* TR_ADMIN_PASSWORD */
"Admin jelsz�",
/* TR_SECTION_MENU */
"Section menu",
/* TR_SELECT_THE_ITEM */
"V�laszd ki mit szeretn�l be�llitani.",
/* TR_SETUP_FINISHED */
"A Setup k�sz.  Nyomj Ok -t az ujraindul�shoz .",
/* TR_SETUP_NOT_COMPLETE */
"Az alap be�llit�s nincs teljesen befejezve. Bizonyosodj meg r�la, hogy a Setup program " \
"norm�lisan befejez�d�tt. Futtasd �jra a setup-ot a shellb�l.",

/* passwords.c */
/* TR_ENTER_ROOT_PASSWORD */
"Ird be a 'root' felhaszn�l� jelszav�t. Jelentkezz be ezzel a felhaszn�l�val a parancssori hozz�f�r�shez.",
/* TR_SETTING_ROOT_PASSWORD */
"Be�llitom a 'root' jelsz�t....",
/* TR_PROBLEM_SETTING_ROOT_PASSWORD */
"Probl�ma a 'root' jelsz� be�llit�s�val",
/* TR_ENTER_SETUP_PASSWORD */
"Ird be a 'setup' felhaszn�l� jelszav�t. Jelentkezz be ezzel a felhaszn�l�val hogy lefuttasd a setup " \
"programot.",
/* TR_SETTING_SETUP_PASSWORD */
"Be�llitom a  'setup' jelsz�t....",
/* TR_PROBLEM_SETTING_SETUP_PASSWORD */
"Probl�ma a 'setup' jelsz� be�llit�s�val",
/* TR_ENTER_ADMIN_PASSWORD */
"Ird be a Smoothwall admin jelszav�t.  Ezt a felhaszn�l�t haszn�ljuk " \
"a Smoothwall web adminisztr�ci�s lapjaira t�rt�n� bejelentkez�shez.",
/* TR_SETTING_ADMIN_PASSWORD */
"Be�llitom a Smoothwall admin jelsz�t....",
/* TR_PROBLEM_SETTING_ADMIN_PASSWORD */
"Probl�ma a  Smoothwall admin jelsz� be�llit�s�val.",
/* TR_PASSWORD_PROMPT */
"Jelsz�:",
/* TR_AGAIN_PROMPT */
"Ism�t:",
/* TR_PASSWORD_CANNOT_BE_BLANK */
"A jelsz� nem lehet �res.",
/* TR_PASSWORDS_DO_NOT_MATCH */
"A jelszavak nem egyeznek.",

/* hostname.c */
/* TR_ENTER_HOSTNAME */
"Ird be a g�p hostnev�t.",
/* TR_HOSTNAME_CANNOT_BE_EMPTY */
"A hostn�v nem lehet �res.",
/* TR_HOSTNAME_CANNOT_CONTAIN_SPACES */
"A hostn�v nem tartalmazhat sz�k�z�ket.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTNAME */
"Nem lehet irni /etc/hostname",

/* isdn.c */
/* TR_GERMAN_1TR6 */
"German 1TR6",
/* TR_EURO_EDSS1 */
"Euro (EDSS1)",
/* TR_LEASED_LINE */
"B�relt vonal",
/* TR_US_NI1 */
"US NI1",
/* TR_PROTOCOL_COUNTRY */
"Protocol/orsz�g",
/* TR_ISDN_CARD */
"ISDN k�rtya",
/* TR_MSN_CONFIGURATION */
"Saj�t telefonsz�m (MSN/EAZ)",
/* TR_SET_ADDITIONAL_MODULE_PARAMETERS */
"Tov�bbi modul param�terek be�llit�sa",
/* TR_RED_IN_USE */
"Az ISDN (vagy egy m�sik k�ls� kapcsolat) haszn�latban van.  Nem tudod " \
"konfigur�lni az ISDN-t amig a RED interf�sz aktiv.",
/* TR_ISDN_CONFIGURATION_MENU */
"ISDN configur�ci�s menu",
/* TR_ISDN_STATUS */
"ISDN jelenlegi %s.\n\n" \
"   Protokoll: %s\n" \
"   K�rtya: %s\n" \
"   Helyi telefonsz�m: %s\n\n" \
"V�laszd ki, minek a be�llit�s�t akarod megv�ltoztatni, vagy v�laszd a jelenlegi be�llit�st .",
/* TR_ISDN_NOT_YET_CONFIGURED */
"Az ISDN m�g nincs konfigur�lva. V�laszd ki mit szeretn�l be�llitani.",
/* TR_ENABLE_ISDN */
"ISDN enged�lyez�se",
/* TR_DISABLE_ISDN */
"ISDN tilt�s",
/* TR_INITIALISING_ISDN */
"ISDN inicializ�l�s...",
/* TR_UNABLE_TO_INITIALISE_ISDN */
"Nem lehet inicializ�lni az ISDN-t.",
/* TR_ISDN_NOT_SETUP */
"Az ISDN nincs be�llitva. N�h�ny dolog m�g nincs kiv�lasztva.",
/* TR_ISDN_PROTOCOL_SELECTION */
"ISDN protokoll kiv�laszt�s",
/* TR_CHOOSE_THE_ISDN_PROTOCOL */
"V�laszd ki a sz�ks�ges ISDN protokollt.",
/* TR_AUTODETECT */
"* AUTODETECT *",
/* TR_ISDN_CARD_SELECTION */
"ISDN k�rtya kiv�laszt�s",
/* TR_CHOOSE_THE_ISDN_CARD_INSTALLED */
"V�laszd ki a megfelel� ISDN k�rty�t.",
/* TR_CHECKING_FOR */
"Kipr�b�lom: %s",
/* TR_ISDN_CARD_NOT_DETECTED */
"Nem tal�ltam ISDN k�rty�t. Lehet hogy sz�ks�g van tov�bbi modul param�terek megad�s�ra" \
"ha a k�rtya ISA tipus� vagy speci�lis k�vetelm�nyei vannak.",
/* TR_DETECTED */
"Tal�ltam : %s",
/* TR_UNABLE_TO_FIND_AN_ISDN_CARD */
"Nem tal�ltam ISDN k�rty�t a g�pben. Lehet hogy sz�ks�g van tov�bbi modul param�terek megad�s�ra " \
"ha a k�rtya ISA tipus� vagy speci�lis k�vetelm�nyei" \
"vannak.",
/* TR_ENTER_THE_LOCAL_MSN */
"K�rem a saj�t telefonsz�mod (MSN/EAZ).",
/* TR_PHONENUMBER_CANNOT_BE_EMPTY */
"A telefonsz�m mez� nem lehet �res.",
/* TR_ENTER_ADDITIONAL_MODULE_PARAMS */
"N�h�ny ISDN k�rtya (k�l�n�sen az ISA k�rty�k) tov�bbi modul param�tereket " \
"ig�nyel az IRQ �s az IO cim be�llit�s�shoz. Ha ilyened van " \
"ird be a megfelel� param�tereket. P�ld�ul: " \
"\"io=0x280 irq=9\". Ezeket az inform�ci�k lesznek felhaszn�lva a k�rtya felismer�sn�l.",

/* networking.c */ 
/* TR_PUSHING_NETWORK_DOWN */
"H�l�zat deaktv�l�s...",
/* TR_PULLING_NETWORK_UP */
"H�l�zat aktiv�l�s...",
/* TR_NETWORK_CONFIGURATION_TYPE */
"A h�l�zati konfigur�ci� tipusa",
/* TR_DRIVERS_AND_CARD_ASSIGNMENTS */
"Meghajt�program �s k�rtya hozz�rendel�sek",
/* TR_ADDRESS_SETTINGS */
"Cim be�llit�sok",
/* TR_DNS_AND_GATEWAY_SETTINGS */
"DNS �s  Gateway be�llit�sok",
/* TR_RESTART_REQUIRED */
"\n\nHa k�sz a konfigur�ci�, a h�l�zat �jraindit�sa sz�ks�ges.",
/* TR_CURRENT_CONFIG (first %s is type, second is restart message (or not) */
"Jelenlegi be�llit�s: %s%s",
/* TR_NETWORK_CONFIGURATION_MENU */
"H�l�zati be�llit�sok menuje",
/* TR_NETWORK_CONFIGURATION_TYPE_LONG */
"V�laszd ki a h�l�zati konfigur�ci�t a Smoothwall r�sz�re.  A k�vetkez� " \
"konfigur�ci� tipusok azok, amelyekhez ethernet van csatlakoztatva" \
"Ha megv�ltoztatod ezt a be�llit�st, akkor sz�ks�ges a h�l�zat �jraindit�sa, " \
"�s �t kell konfigur�lni a h�l�zati k�rtya drivereket is.",
/* TR_PUSHING_NON_LOCAL_NETWORK_DOWN */
"Lel�v�m a helyi h�l�zatot...",
/* TR_YOUR_CONFIGURATION_IS_SINGLE_GREEN_ALREADY_HAS_DRIVER */
"A konfigur�ci� egy GREEN interf�szre van �llitva, " \
"amelyhez m�r van driver hozz�rendelve.",
/* TR_CONFIGURE_NETWORK_DRIVERS */
"Configure network drivers, and which interface each card " \
"is assigned to.  The current configuration is as follows:\n\n",
/* TR_DO_YOU_WISH_TO_CHANGE_THESE_SETTINGS */
"\nMeg akarod v�ltoztatni ezeket a be�llit�sokat ?",
/* TR_UNCLAIMED_DRIVER */
"There is an unclaimed ethernet card of type:\n%s\n\n" \
"Ehhez tudod hozz�rendelni:",
/* TR_CARD_ASSIGNMENT */
"K�rtya hozz�rendel�s",
/* TR_PROBE */
"Felismer�s",
/* TR_SELECT */
"Kiv�laszt�s",
/* TR_NO_UNALLOCATED_CARDS */
"Nem maradt kiv�lasztatlan k�rtya, " \
"pedig sz�ks�ges lenne. Automatikusan megkerestetheted a sz�ks�ges k�rty�kat,vagy " \
"v�lassz drivert a list�b�l.",
/* TR_UNABLE_TO_FIND_ANY_ADDITIONAL_DRIVERS */
"Nem lehet tov�bbi drivereket tal�lni.",
/* TR_ALL_CARDS_SUCCESSFULLY_ALLOCATED */
"Minden k�rtya sikeresen hozz�rendelve.",
/* TR_NOT_ENOUGH_CARDS_WERE_ALLOCATED */
"Nincs elegend� k�rtya hozz�rendelve.",
/* TR_MANUAL */
"* MANUALIS *",
/* TR_SELECT_NETWORK_DRIVER */
"V�lassz h�l�zati drivert",
/* TR_SELECT_NETWORK_DRIVER_LONG */
"V�laszd ki az install�lt k�rty�nak megfelel� drivert. " \
"ha a MANUALIS-t v�lasztod , akkor lehet�s�g edlesz megadni " \
"a driver modul nev�t �s a param�tereket. " \
"(K�l�n�sen ISA k�rty�k eset�ben lehet sz�ks�ges)",
/* TR_UNABLE_TO_LOAD_DRIVER_MODULE */
"Nem lehet bet�lteni a driver modult.",
/* TR_THIS_DRIVER_MODULE_IS_ALREADY_LOADED */
"A driver modul m�r be van t�ltve.",
/* TR_MODULE_PARAMETERS */
"Ird be a modul nev�t , �s az �ltala ig�nyelt param�tereket.",
/* TR_LOADING_MODULE */
"A modul bet�lt�se...",
/* TR_WARNING */
"WARNING",
/* TR_WARNING_LONG */
"Ha megv�ltoztatod ezt az IP cimet, �s t�volr�l jelentkezt�l be, " \
"a kapcsolat a  Smoothwall g�ppel meg fog szakadni, �s �jra kell " \
"csatlakoznod ezen az �j IP cimen. Ez egy vesz�lyes m�velet, " \
"�s csak akkor pr�b�ld meg, ha fizikailag is hozz�f�rsz a g�phez, " \
"ha net�n valami m�gsem siker�lne.g.",
/* TR_SINGLE_GREEN */
"A konfigur�ci�d GREEN interf�szre van �llitva.",
/* TR_SELECT_THE_INTERFACE_YOU_WISH_TO_RECONFIGURE */
"V�laszd ki az interf�szt amit �t akarsz konfigur�lni.",
/* TR_DNS_GATEWAY_WITH_GREEN */
"A konfigur�ci�d nem haszn�l ethernet k�rty�t " \
" RED interf�sz sz�m�ra. A DNS �s a  Gateway inform�ci�k a dialup felhaszn�l�k " \
"sz�m�ra automatikusan konfigur�l�dnak a t�rcs�z�skor.",
/* TR_PRIMARY_DNS */
"Els�dleges DNS:",
/* TR_SECONDARY_DNS */
"M�sodlagos DNS:",
/* TR_DEFAULT_GATEWAY */
"Default Gateway:",
/* TR_DNS_AND_GATEWAY_SETTINGS_LONG */
"K�rem a DNS �s a gateway inform�ci�kat. Ezek a be�llit�sok csak akkor haszn�latosakha a DHCP " \
"tiltva van a RED interf�szen.",
/* TR_PRIMARY_DNS_CR */
"Els�dleges DNS\n",
/* TR_SECONDARY_DNS_CR */
"M�sodlagos DNS\n",
/* TR_DEFAULT_GATEWAY_CR */
"Default Gateway\n",
/* TR_SECONDARY_WITHOUT_PRIMARY_DNS */
"M�sodlagos DNS van megadva Els�dleges DNS n�lk�l",
/* TR_UNKNOWN */
"ISMERETLEN",
/* TR_NO_ORANGE_INTERFACE */
"Nincs ORANGE interf�sz hozz�rendelve.",
/* TR_MISSING_ORANGE_IP */
"Hi�nyz� IP inform�ci� az ORANGE interf�sz sz�m�ra.",
/* TR_NO_RED_INTERFACE */
"Nincs RED interf�sz hozz�rendelve.",
/* TR_MISSING_RED_IP */
"Hi�nyz� IP inform�ci� a RED interf�sz sz�m�ra.",

/* dhcp.c */
/* TR_START_ADDRESS */
"Kezd�cim:",
/* TR_END_ADDRESS */
"V�gcim:",
/* TR_DEFAULT_LEASE */
"Alap�rtelmezett b�rlet (perc):",
/* TR_MAX_LEASE */
"Max b�rlet (perc):",
/* TR_DOMAIN_NAME_SUFFIX */
"Domain n�v ut�tag:",
/* TR_CONFIGURE_DHCP */
"A DHCP server be�llit�sa.",
/* TR_START_ADDRESS_CR */
"Kezd�cim\n",
/* TR_END_ADDRESS_CR */
"V�gcim\n",
/* TR_DEFAULT_LEASE_CR */
"Alap�rtelmezett b�rlet\n",
/* TR_MAX_LEASE_CR */
"Max b�rlet\n",
/* TR_DOMAIN_NAME_SUFFIX_CR */
"Domain n�v ut�tag\n",

/* keymap.c */
/* TR_KEYBOARD_MAPPING */
"Billenty�zet kezel�s",
/* TR_KEYBOARD_MAPPING_LONG */
"V�laszd ki a billenty�zet tipus�t az al�bbi list�b�l.",

/* timezone.c */
/* TR_TIMEZONE */
"Id�zona",
/* TR_TIMEZONE_LONG */
"V�laszd ki a megfelel� id�zon�t az al�bbi list�b�l.",

/* usbadsl.c */
/* TR_USB_CONTROLLER */
"V�laszd ki az  USB vez�rl�t",
/* TR_USBADSL_STATUS */
"USB ADSL jelenleg: %s\n" \
"   Vez�rl�: %s\n\n" \
"V�laszd ki azt a t�telt amit konfigur�lni szerten�z, vagy v�laszd a jelenlegi be�llit�sokat.",
/* TR_USBADSL_CONFIGURATION */
"USB ADSL konfigur�ci�",
/* TR_ENABLE_USBADSL */
"USB ADSL enged�lyez�s",
/* TR_DISABLE_USBADSL */
"USB ADSL tilt�s",
/* TR_INITIALISING_USBADSL */
"USB ADSL inicializ�l�s.",
/* TR_UNABLE_TO_INITIALISE_USBADSL */
"Nem lehet inicializ�lni az USB ADSL-t",
/* TR_USBADSL_NOT_SETUP */
"A USB ADSL nincs be�llitva.",
/* TR_USB_CONTROLLER_SELECTION */
"USB controller kiv�laszt�s",
/* TR_CHOOSE_THE_USB_CONTROLLER_INSTALLED */
"V�laszd ki az instll�lt USB controller.",
/* TR_USB_CONTROLLER_NOT_DETECTED */
"Nem tal�ltam USB controllert.",
/* TR_UNABLE_TO_FIND_A_USB_CONTROLLER */
"Nem tal�ltam USB kontrollert.",
/* TR_STARTING_UP_USBADSL */
"Az  USB ADS indit�saL..."

};
