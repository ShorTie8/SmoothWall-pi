/* SmoothWall libsmooth.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * (c) Finnish Translation Team:
 * Jussi Siponen
 * Pasi Parkkinen
 *
 * filename: finnish.c
 * Contains finnish strings. */

#include "libsmooth.h"

char *finnish_tr[] = {

/**********/
/* COMMON */
/**********/

/* TR_OK */
"Ok",
/* TR_CANCEL */
"Peruuta",
/* TR_INSTALLATION_CANCELED */
"Asennus keskeytetty.",
/* TR_HELPLINE */
"        <Tab>/<Alt-Tab> elementtien v�lill�   |  <V�lily�nti> valitsee",
/* TR_QUIT */
"Poistu",
/* TR_DISABLED */
"Ei k�yt�ss�",
/* TR_ENABLED */
"K�yt�ss�",
/* TR_UNSET */
"EI ASETETTU",
/* TR_UNABLE_TO_OPEN_SETTINGS_FILE */
"Asetustiedostoa ei voi avata",
/* TR_DONE */
"Valmis",
/* TR_PROBE_FAILED */
"Automaattinen tunnistus ep�onnistui.",

/*************/
/* LIBSMOOTH */
/*************/

/* main.c  */

/* netstuff.c */
/* TR_IP_ADDRESS_PROMPT */
"IP-osoite:",
/* TR_NETWORK_ADDRESS_PROMPT */
"Verkko-osoite:",
/* TR_NETMASK_PROMPT */
"Aliverkon peite:",
/* TR_ENTER_IP_ADDRESS_INFO */
"Anna IP-osoite -asetukset",
/* TR_INVALID_FIELDS */
"N�iden kenttien arvot eiv�t kelpaa:\n\n",
/* TR_IP_ADDRESS_CR */
"IP-osoite\n",
/* TR_NETWORK_ADDRESS_CR */
"Verkko-osoite\n",
/* TR_NETWORK_MASK_CR */
"Aliverkon peite\n",
/* TR_INTERFACE (%s is interface name) */
"%s verkkoliit�nt�",
/* TR_ENTER_THE_IP_ADDRESS_INFORMATION (%s is interface name) */
"Anna IP-asetukset verkkoliit�nn�lle %s.",
/* TR_LOOKING_FOR_NIC (%s is a nic name) */
"Etsin: %s",
/* TR_FOUND_NIC (%s is a nic name) */
"Smoothwall on l�yt�nyt verkkosovittimen: %s",
/* TR_MODULE_NAME_CANNOT_BE_BLANK */
"Moduulin nimi on annettava.",
/* TR_STATIC */
"Kiinte�",
/* TR_DHCP_HOSTNAME */
"DHCP-palvelin:",
/* TR_DHCP_HOSTNAME_CR */
"DHCP-palvelin\n",

/* misc.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_HOSTNAMECONF */
"Tiedostoa /var/smoothwall/main/hostname.conf ei voida kirjoittaa.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS */
"Tiedostoa /etc/hosts ei voida kirjoittaa.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_DENY */
"Tiedostoa /etc/hosts.deny ei voida kirjoittaa.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_ALLOW */
"Tiedostoa /etc/hosts.allow ei voida kirjoittaa.",
/* TR_UNABLE_TO_SET_HOSTNAME */
"Is�nt�nime� ei voida asettaa.",

/***********/
/* INSTALL */
/***********/
/* TR_WELCOME */
"Tervetuloa Smoothwall asennusohjelmaan. Pyyd�mme k�ym��n kotisivuillamme " \
"osoitteessa http://www.smoothwall.org. Jos valitset Peruuta " \
"seuraavilla n�yt�ill�, tietokone k�ynnistet��n uudelleen.",
/* TR_NO_IDE_HARDDISK */
"Yht��n IDE kiintolevy� ei l�ytynyt.",
/* TR_SELECT_INSTALLATION_MEDIA */
"Valitse asennusmedia",
/* TR_SELECT_INSTALLATION_MEDIA_LONG */
"Smoothwall voidaan asentaa useista eri l�hteist�.  Helpointa on " \
"k�ytt�� tietokoneen CDROM-asemaa. Jos tietokoneessa ei ole CDROM-asemaa, voit " \
"asentaa toiselta verkossa olevalta tietokoneelta, jolta asennustiedostot " \
"noudetaan HTTP-protokollalla. T�ss� tapauksessa tarvitset verkkosovittimen " \
"laiteohjainlevykkeen.",
/* TR_NO_IDE_CDROM */
"Yht��n IDE CDROM-asemaa ei l�ytynyt.",
/* TR_INSERT_CDROM */
"Laita Smoothwall CD CDROM-asemaan.",
/* TR_INSERT_FLOPPY */
"Laita Smoothwall laiteohjainlevyke levykeasemaan.",
/* TR_PREPARE_HARDDISK */
"Asennusohjelma valmistelee IDE kiintolevyn %s. " \
"Aluksi levy osioidaan ja sitten osioille luodaan " \
"tiedostoj�rjestelm�t.",
/* TR_PARTITIONING_DISK */
"Osioidaan levy�...",
/* TR_UNABLE_TO_PARTITION */
"Levyn osiointi ep�onnistui.",
/* TR_MAKING_SWAPSPACE */
"Luodaan swap-osiota...",
/* TR_UNABLE_TO_MAKE_SWAPSPACE */
"Swap-osion luominen ep�onnistui.",
/* TR_MAKING_ROOT_FILESYSTEM */
"Luodaan root-tiedostoj�rjestelm�...",
/* TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM */
"root-tiedostoj�rjestelm�n luominen ep�onnistui.",
/* TR_MOUNTING_ROOT_FILESYSTEM */
"Liit�n root-tiedostoj�rjestelm�n...",
/* TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM */
"root-tiedostoj�rjestelm�n liitt�minen ep�onnistui.",
/* TR_MAKING_BOOT_FILESYSTEM */
"Luodaan boot-tiedostoj�rjestelm�...",
/* TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM */
"boot-tiedostoj�rjestelm�n luominen ep�onnistui.",
/* TR_MOUNTING_BOOT_FILESYSTEM */
"Liit�n boot-tiedostoj�rjestelm�n...",
/* TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM */
"boot-tiedostoj�rjestelm�n liitt�minen ep�onnistui.",
/* TR_MAKING_LOG_FILESYSTEM */
"Luodaan log-tiedostoj�rjestelm�...",
/* TR_UNABLE_TO_MAKE_LOG_FILESYSTEM */
"log-tiedostoj�rjestelm�n luominen ep�onnistui.",
/* TR_MOUNTING_LOG_FILESYSTEM */
"Liit�n log-tiedostoj�rjestelm�n...",
/* TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM */
"log-tiedostoj�rjestelm�n liitt�minen ep�onnistui.",
/* TR_MOUNTING_SWAP_PARTITION */
"Liit�n swap-osion...",
/* TR_UNABLE_TO_MOUNT_SWAP_PARTITION */
"swap-osion liitt�minen ep�onnistui.",
/* TR_NETWORK_SETUP_FAILED */
"Verkkoasennus ep�onnistui.",
/* TR_NO_TARBALL_DOWNLOADED */
"Tar-pakettia ei ladattu.",
/* TR_INSTALLING_FILES */
"Kopioidaan tiedostoja...",
/* TR_UNABLE_TO_INSTALL_FILES */
"Tiedostojen kopiointi ep�onnistui.",
/* TR_UNABLE_TO_REMOVE_TEMP_FILES */
"V�liaikaistiedostojen poistaminen ep�onnistui.",
/* TR_ERROR_WRITING_CONFIG */
"Asetustietojen kirjoittaminen ep�onnistui.",
/* TR_INSTALLING_LILO */
"Asennetaan LILO...",
/* TR_UNABLE_TO_INSTALL_LILO */
"LILOn asennus ep�onnistui.",
/* TR_UNABLE_TO_UNMOUNT_HARDDISK */
"Kiintolevyn irroittaminen ep�onnistui.",
/* TR_UNABLE_TO_UNMOUNT_CDROM */
"CDROM/levykkeen irroittaminen ep�onnistui.",
/* TR_UNABLE_TO_EJECT_CDROM */
"CDROM-levyn poistaminen ep�onnistui.",
/* TR_CONGRATULATIONS */
"Onneksi olkoon!",
/* TR_CONGRATULATIONS_LONG */
"Smoothwall on nyt asennettu. Poista levykkeet ja " \
"CDROM:t asemista. Vuorossa on nyt asetusten tekeminen (ISDN, " \
"verkkosovittimet ja salasanat). Kun asennus on valmis, k�y hallintasivuilla " \
"osoitteessa http://smoothwall:81 tai https://smoothwall:445 " \
"(korvaa 'smoothwall' asennuksessa k�ytt�m�ll�si is�nt�nimell�), " \
"jos sinun tarvitsee luoda puhelinverkkoyhteyden asetukset. Muista antaa " \
"Smoothwallin 'dial'-k�ytt�j�lle salasana, jos tahdot muidenkin kuin " \
"p��k�ytt�j�n voivan avata ja sulkea yhteyden.",
/* TR_PRESS_OK_TO_REBOOT */
"Paina OK k�ynnist��ksesi tietokoneen uudelleen.",
/* TR_ERROR */
"Virhe",
/* TR_CALCULATING_MODULE_DEPENDANCIES */
"Tarkistetaan moduulien riippuvuussuhteet...",
/* TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES */
"Riippuvuussuhteiden tarkistus ep�onnistui.",

/* cdrom.c */
/* TR_SELECT_CDROM_TYPE */
"Valitse CDROMin tyyppi",
/* TR_SELECT_CDROM_TYPE_LONG */
"Yht��n IDE CDROM-asenaa ei l�ytynyt.  Valitse, mit� n�ist� laiteohjaimista " \
"haluat Smoothwallin k�ytt�v�n CDROM-aseman ohjaamiseen.",
/* TR_SUGGEST_IO (%x is an IO number) */
"(ehdotus %x)",
/* TR_SUGGEST_IRQ (%d is an IRQ number) */
"(ehdotus %d)",
/* TR_CONFIGURE_THE_CDROM */
"Valitse CDROMin k�ytt�m� IO-osoite ja/tai IRQ (keskeytys).",
/* TR_INVALID_IO (note extra space) */
"IO-osoite ei kelpaa. ",
/* TR_INVALID_IRQ */
"IRQ ei kelpaa.",

/* config.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_SETTINGS */
"Tiedostoa /var/smoothwall/main/settings ei voida kirjoittaa.",
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_ETHERNET_SETTINGS */
"Tiedostoa /var/smoothwall/ethernet/settings ei voida kirjoittaa.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK */
"Symbolista linkki� /dev/harddisk ei voida luoda.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1 */
"Symbolista linkki� /dev/harddisk1 ei voida luoda.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2 */
"Symbolista linkki� /dev/harddisk2 ei voida luoda.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3 */
"Symbolista linkki� /dev/harddisk3 ei voida luoda.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4 */
"Symbolista linkki� /dev/harddisk4 ei voida luoda.",

/* net.c */
/* TR_DOWNLOADING */
"Lataan...",
/* TR_FAILED_TO_DOWNLOAD */
"Lataus ep�onnistui.",
/* TR_ENTER_URL */
"Anna Smoothwall tar.gz-tiedoston URL. " \
"VAROITUS: DNS ei ole k�ytett�viss�. Osoitteen tulee p��tty� " \
"tiedostonimeen 'smoothwall.tgz'.",

/* nic.c */
/* TR_CONFIGURE_NETWORKING */
"Verkkoasetukset",
/* TR_CONFIGURE_NETWORKING_LONG */
"Aloita verkkoasetusten teko lataamalla oikea laiteohjain GREEN-verkkoliit�nn�lle. "  \
"Asennus voi tunnustella sovittimia puolestasi tai voit valita ohjaimen listasta. "  \
"Huomaa ett� jos koneessa on useita verkkosovittimia, tapahtuu loppujen sovitinten "  \
"k�ytt�notto my�hemmin. Ota my�s huomioon, ett� jos koneessa on muita "  \
"GREEN-liit�nn�n sovittimen kanssa samantyyppisi� sovittimia ja annat niiden "  \
"laiteohjaimille lis�asetuksia, on n�iden lis�asetusten oltava sellaisia ett� "  \
"kaikki n�m� sovittimet voivat k�ynnisty� samanaikaisesti GREEN-liit�nn�n "  \
"kanssa.",
/* TR_INTERFACE_FAILED_TO_COME_UP */
"Verkkoliit�nn�n k�ynnistys ep�onnistui.",
/* TR_ENTER_NETWORK_DRIVER */
"Verkkosovittimen tunnistus ep�onnistui. Anna oikea laiteohjain " \
"ja mahdolliset lis�asetukset verkkosovittimelle.",

/*********/
/* SETUP */
/*********/

/* main.c */
/* TR_HOSTNAME */
"Is�nt�nimi",
/* TR_NETWORKING */
"Verkkoasetukset",
/* TR_DHCP_SERVER_CONFIGURATION */
"DHCP-palvelimen asetukset",
/* TR_ISDN_CONFIGURATION */
"ISDN-asetukset",
/* TR_ROOT_PASSWORD */
"\'root\' salasana",
/* TR_SETUP_PASSWORD */
"\'setup\' salasana",
/* TR_ADMIN_PASSWORD */
"P��k�ytt�j�n salasana",
/* TR_SECTION_MENU */
"Valikko",
/* TR_SELECT_THE_ITEM */
"Valitse kohde, jonka asetuksia haluat muuttaa.",
/* TR_SETUP_FINISHED */
"Asennus valmis. Paina OK k�ynnist��ksesi tietokoneen uudelleen.",
/* TR_SETUP_NOT_COMPLETE */
"Asennusta ei suoritettu loppuun. Suorita komento setup komentorivilt� " \
"varmistaaksesi asennuksen onnistumisen.",

/* passwords.c */
/* TR_ENTER_ROOT_PASSWORD */
"Anna k�ytt�j�n 'root' salasana. K�yt� t�t� tunnusta komentojen " \
"suorittamiseen komentorivilt�.",
/* TR_SETTING_ROOT_PASSWORD */
"Asetaan k�ytt�j�n 'root' salasana...",
/* TR_PROBLEM_SETTING_ROOT_PASSWORD */
"K�ytt�j�n 'root' salasanan asettaminen ep�onnistui.",
/* TR_ENTER_SETUP_PASSWORD */
"Anna k�ytt�j�n 'setup' salasana. K�yt� t�t� tunnusta " \
"asennusohjelman suorittamiseen.",
/* TR_SETTING_SETUP_PASSWORD */
"Asetaan k�ytt�j�n 'setup' salasana...",
/* TR_PROBLEM_SETTING_SETUP_PASSWORD */
"K�ytt�j�n 'setup' salasanan asettaminen ep�onnistui.",
/* TR_ENTER_ADMIN_PASSWORD */
"Anna Smoothwall p��k�ytt�j�n salasana. K�yt� t�t� tunnusta " \
"Smoothwallin web-hallintaan kirjautumiseen.",
/* TR_SETTING_ADMIN_PASSWORD */
"Asetetaan Smoothwall p��k�ytt�j�n salasana...",
/* TR_PROBLEM_SETTING_ADMIN_PASSWORD */
"Smoothwall p��k�ytt�j�n salasanan asettaminen ep�onnistui.",
/* TR_PASSWORD_PROMPT */
"Salasana:",
/* TR_AGAIN_PROMPT */
"Salasana uudestaan:",
/* TR_PASSWORD_CANNOT_BE_BLANK */
"Salasana ei voi olla tyhj�.",
/* TR_PASSWORDS_DO_NOT_MATCH */
"Salasanat eiv�t t�sm��.",

/* hostname.c */
/* TR_ENTER_HOSTNAME */
"Anna koneen is�nt�nimi.",
/* TR_HOSTNAME_CANNOT_BE_EMPTY */
"Is�nt�nimi ei voi olla tyhj�.",
/* TR_HOSTNAME_CANNOT_CONTAIN_SPACES */
"Is�nt�nimess� ei voi olla v�lily�ntej�.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTNAME */
"Tiedostoa /etc/hostname ei voida kirjoittaa.",

/* isdn.c */
/* TR_GERMAN_1TR6 */
"Saksalainen 1TR6",
/* TR_EURO_EDSS1 */
"Euro (EDSS1)",
/* TR_LEASED_LINE */
"Kiinte� linja",
/* TR_US_NI1 */
"US NI1",
/* TR_PROTOCOL_COUNTRY */
"Protokolla/Maa",
/* TR_ISDN_CARD */
"ISDN-sovitin",
/* TR_MSN_CONFIGURATION */
"Oma puhelinnumero (MSN/EAZ)",
/* TR_SET_ADDITIONAL_MODULE_PARAMETERS */
"Moduulin lis�asetukset",
/* TR_RED_IN_USE */
"ISDN (tai muu ulkoinen yhteys) on k�yt�ss�. Et voi muuttaa " \
"ISDN-asetuksia, kun RED-verkkoliit�nt� on aktiivinen.",
/* TR_ISDN_CONFIGURATION_MENU */
"ISDN-asetukset",
/* TR_ISDN_STATUS */
"ISDN k�ytt�� %s.\n\n" \
"   Protokolla: %s\n" \
"   Sovitin: %s\n" \
"   Oma puhelinnumero: %s\n\n" \
"Valitse asetus, jonka haluat muuttaa tai hyv�ksy nykyiset asetukset.",
/* TR_ISDN_NOT_YET_CONFIGURED */
"ISDN-asetukset ep�t�ydelliset. Valitse asetus, jonka haluat muuttaa.",
/* TR_ENABLE_ISDN */
"Ota ISDN k�ytt��n",
/* TR_DISABLE_ISDN */
"Poista ISDN k�yt�st�",
/* TR_INITIALISING_ISDN */
"Alustetaan ISDN...",
/* TR_UNABLE_TO_INITIALISE_ISDN */
"ISDN alustus ep�onnistui.",
/* TR_ISDN_NOT_SETUP */
"ISDN-asennus ei ole valmis. Joitain asetuksia ei ole annettu.",
/* TR_ISDN_PROTOCOL_SELECTION */
"ISDN-protokollan valinta",
/* TR_CHOOSE_THE_ISDN_PROTOCOL */
"Valitse k�ytetty ISDN-protokolla.",
/* TR_AUTODETECT */
"* TUNNISTA AUTOMAATTISESTI *",
/* TR_ISDN_CARD_SELECTION */
"ISDN-sovittimen valinta",
/* TR_CHOOSE_THE_ISDN_CARD_INSTALLED */
"Valitse k�ytt�m�si ISDN-sovitin.",
/* TR_CHECKING_FOR */
"Etsit��n: %s",
/* TR_ISDN_CARD_NOT_DETECTED */
"Yht��n ISDN-sovitinta ei l�ytynyt. Moduuli saattaa vaatia lis�asetuksia " \
"jos sovitin on ISA-liit�nt�inen tai sovitin muuten vaatii niit�.",
/* TR_DETECTED */
"L�ydettin sovitin: %s",
/* TR_UNABLE_TO_FIND_AN_ISDN_CARD */
"Yht��n ISDN-sovitinta ei l�ytynyt. Moduuli saattaa vaatia lis�asetuksia " \
"jos sovitin on ISA-liit�nt�inen tai sovitin muuten vaatii niit�.",
/* TR_ENTER_THE_LOCAL_MSN */
"Anna oma puhelinnumero (MSN/EAZ).",
/* TR_PHONENUMBER_CANNOT_BE_EMPTY */
"Puhelinnumero ei voi olla tyhj�.",
/* TR_ENTER_ADDITIONAL_MODULE_PARAMS */
"Jotkin ISDN-sovittimet (varsinkin ISA-liit�nt�iset) saattavat vaatia " \
"lis�asetuksia IRQ ja IO-osoitteen osalta. Jos sinulla on " \
"t�llainen ISDN-sovitin, anna lis�asetukset t�h�n. Esimerkiksi: " \
"\"io=0x280 irq=9\". Lis�asetuksia k�ytet��n sovittimen tunnistuksessa.",

/* networking.c */
/* TR_PUSHING_NETWORK_DOWN */
"Sammutetaan verkko-ohjelmisto...",
/* TR_PULLING_NETWORK_UP */
"K�ynnistet��n verkko-ohjelmisto...",
/* TR_NETWORK_CONFIGURATION_TYPE */
"Verkkoasetuksen tyyppi",
/* TR_DRIVERS_AND_CARD_ASSIGNMENTS */
"Laiteohjaimet ja verkkosovittimet",
/* TR_ADDRESS_SETTINGS */
"Osoitteet",
/* TR_DNS_AND_GATEWAY_SETTINGS */
"DNS ja yhdysk�yt�v�",
/* TR_RESTART_REQUIRED */
"\n\nKun asetukset on tehty, verkko-ohjelmisto on k�ynnistett�v� uudelleen.",
/* TR_CURRENT_CONFIG (first %s is type, second is restart message (or not) */
"Nykyinen asetus: %s%s",
/* TR_NETWORK_CONFIGURATION_MENU */
"Verkkoasetukset",
/* TR_NETWORK_CONFIGURATION_TYPE_LONG */
"Valitse Smoothwallin k�ytt�m� verkkoasetus. Valitse listasta, " \
"miss� verkkoliit�nn�iss� k�ytet��n ethernet-sovittimia. " \
"Valinnan muuttaminen vaatii verkko-ohjelmiston uudelleenk�ynnistyksen " \
"ja nollaa tehdyt laiteohjainvalinnat.",
/* TR_PUSHING_NON_LOCAL_NETWORK_DOWN */
"Sammutetaan ulkoinen verkko...",
/* TR_YOUR_CONFIGURATION_IS_SINGLE_GREEN_ALREADY_HAS_DRIVER */
"T�m� asetus k�ytt�� yht� GREEN-liit�nt��, " \
"jolle on jo laiteohjain.",
/* TR_CONFIGURE_NETWORK_DRIVERS */
"Valitse laiteohjaimet ja kohdista verkkosovittimet " \
"eri liit�nn�ille.  Nykyiset asetukset:\n\n",
/* TR_DO_YOU_WISH_TO_CHANGE_THESE_SETTINGS */
"\nHaluatko muuttaa n�it� asetuksia?",
/* TR_UNCLAIMED_DRIVER */
"L�ytyi kohdistamaton ethernet-sovitin:\n%s\n\n" \
"Voit kohdistaa sen:",
/* TR_CARD_ASSIGNMENT */
"Liit�nn�n kohdistus",
/* TR_PROBE */
"Tunnustele",
/* TR_SELECT */
"Valitse",
/* TR_NO_UNALLOCATED_CARDS */
"Kohdistamattomia sovittimia ei l�ytynyt, " \
"niit� tarvitaan enemm�n. Voit tunnustella verkkosovittimia tai " \
"valita laiteohjaimen listasta.",
/* TR_UNABLE_TO_FIND_ANY_ADDITIONAL_DRIVERS */
"Uusia verkkosovittimia ei l�ytynyt.",
/* TR_ALL_CARDS_SUCCESSFULLY_ALLOCATED */
"Kaikki verkkosovittimet kohdistettu.",
/* TR_NOT_ENOUGH_CARDS_WERE_ALLOCATED */
"Liian v�h�n kohdistettuja verkkosovittimia.",
/* TR_MANUAL */
"* K�SIN *",
/* TR_SELECT_NETWORK_DRIVER */
"Valitse laiteohjain",
/* TR_SELECT_NETWORK_DRIVER_LONG */
"Valitse verkkosovittimen k�ytt�m� laiteohjain. " \
"Valita K�SIN mahdollistaa laitohjainmoduulin nimen ja lis�asetusten " \
"sy�tt�misen. T�m� voi olla tarpeen joidenkin sovittimien laiteohjainten " \
"kanssa (jotkin ISA-liit�nt�iset sovittimet).",
/* TR_UNABLE_TO_LOAD_DRIVER_MODULE */
"Laiteohjaimen lataus ep�onnistui.",
/* TR_THIS_DRIVER_MODULE_IS_ALREADY_LOADED */
"Laiteohjain on jo ladattu.",
/* TR_MODULE_PARAMETERS */
"Anna moduulin nimi ja tarvittaessa lis�asetukset.",
/* TR_LOADING_MODULE */
"Lataan moduulia...",
/* TR_WARNING */
"VAROITUS",
/* TR_WARNING_LONG */
"Jos muutat t�m�n IP-osoitteen ja olet et�yhteydess� koneeseen, " \
"yhteys katkeaa ja joudut ottamaan uudestaan yhteytt� uuteen IP-osoitteeseen. " \
"T�m� on vaarallinen toimenpide ja sit� tulisi yritt�� vain jos " \
"p��set mahdollisessa virhetilanteessa kirjautumaan Smoothwall-koneen " \
"omalle konsolille.",
/* TR_SINGLE_GREEN */
"T�m� asetus k�ytt�� yht� GREEN-liit�nt��.",
/* TR_SELECT_THE_INTERFACE_YOU_WISH_TO_RECONFIGURE */
"Valitse liit�nt�, jonka asetuksia haluat muuttaa.",
/* TR_DNS_GATEWAY_WITH_GREEN */
"T�m� kokoonpano ei k�yt� ethernet-sovitinta RED-verkkoliit�nn�ss�. " \
"DNS- ja Oletusyhdysk�yt�v� -asetukset tehd��n automaattisesti " \
"yhteytt� luotaessa.",
/* TR_PRIMARY_DNS */
"Ensisijainen DNS:",
/* TR_SECONDARY_DNS */
"Toissijainen DNS:",
/* TR_DEFAULT_GATEWAY */
"Oletusyhdysk�yt�v�:",
/* TR_DNS_AND_GATEWAY_SETTINGS_LONG */
"Anna DNS- ja oletusyhdysk�yt�v�-asetukset. N�it� asetuksia k�ytet��n vain, " \
"jos RED-liit�nt� ei k�yt� DHCPt�.",
/* TR_PRIMARY_DNS_CR */
"Ensisijainen DNS\n",
/* TR_SECONDARY_DNS_CR */
"Toissijainen DNS\n",
/* TR_DEFAULT_GATEWAY_CR */
"Oletusyhdysk�yt�v�\n",
/* TR_SECONDARY_WITHOUT_PRIMARY_DNS */
"Toissijainen DNS annettu, mutta ensisijainen DNS puuttuu",
/* TR_UNKNOWN */
"TUNTEMATON",
/* TR_NO_ORANGE_INTERFACE */
"ORANGE-liit�nt�� ei ole annettu.",
/* TR_MISSING_ORANGE_IP */
"ORANGE-liit�nn�n IP-asetuksia ei ole annettu.",
/* TR_NO_RED_INTERFACE */
"RED-liit�nt�� ei ole annettu.",
/* TR_MISSING_RED_IP */
"RED-liit�nn�n IP-asetuksia ei ole annettu.",

/* dhcp.c */
/* TR_START_ADDRESS */
"Ensimm�inen osoite:",
/* TR_END_ADDRESS */
"Viimeinen osoite:",
/* TR_DEFAULT_LEASE */
"Istunnon oletuskestoaika:",
/* TR_MAX_LEASE */
"Istunnon kestoaika enint��n:",
/* TR_DOMAIN_NAME_SUFFIX */
"Toimialueen tunnus:",
/* TR_CONFIGURE_DHCP */
"Anna DHCP-palvelimen asetukset.",
/* TR_START_ADDRESS_CR */
"Ensimm�inen osoite\n",
/* TR_END_ADDRESS_CR */
"Viimeinen osoite\n",
/* TR_DEFAULT_LEASE_CR */
"Oletusistunto\n",
/* TR_MAX_LEASE_CR */
"Istunto enint��n\n",
/* TR_DOMAIN_NAME_SUFFIX_CR */
"Toimialueen tunnus\n",

/* keymap.c */
/* TR_KEYBOARD_MAPPING */
"N�pp�imist�kartta",
/* TR_KEYBOARD_MAPPING_LONG */
"Valitse k�ytt�m�si n�pp�imist� alla olevasta listasta.",

/* timezone.c */
/* TR_TIMEZONE */
"Aikavy�hyke",
/* TR_TIMEZONE_LONG */
"Valitse aikavy�hyke alla olevasta listasta.",

/* usbadsl.c */
/* TR_USB_CONTROLLER */
"Valitse USB-ohjain",
/* TR_USBADSL_STATUS */
"USB ADSL k�ytt��: %s\n" \
"   Ohjain: %s\n\n" \
"Valitse asetus, jonka haluat muuttaa tai hyv�ksy nykyiset asetukset.",
/* TR_USBADSL_CONFIGURATION */
"USB ADSL-asetukset",
/* TR_ENABLE_USBADSL */
"Ota USB ADSL k�ytt��n",
/* TR_DISABLE_USBADSL */
"Poista USB ADSL k�yt�st�",
/* TR_INITIALISING_USBADSL */
"Alustetaan USB ADSL.",
/* TR_UNABLE_TO_INITIALISE_USBADSL */
"USB ADSL alustus ep�onnistui",
/* TR_USBADSL_NOT_SETUP */
"USB ADSL asetuksia ei ole annettu.",
/* TR_USB_CONTROLLER_SELECTION */
"Valitse USB-ohjain",
/* TR_CHOOSE_THE_USB_CONTROLLER_INSTALLED */
"Valitse k�ytett�v� USB-ohjain.",
/* TR_USB_CONTROLLER_NOT_DETECTED */
"USB-ohjainta ei l�ytynyt.",
/* TR_UNABLE_TO_FIND_A_USB_CONTROLLER */
"USB-ohjainta ei l�ytynyt.",
/* TR_STARTING_UP_USBADSL */
"K�ynnist�n USB ADSL..."

};
