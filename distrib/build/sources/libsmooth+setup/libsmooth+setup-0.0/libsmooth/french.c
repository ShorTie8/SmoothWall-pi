/* SmoothWall libsmooth.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * (c) French Translation Team:
 * David Boileau
 * Thierry Charbonnel
 * Frederic Gonnet   
 * Francois Thomas
 * Fabien Illide
 * Christopher Heger 
 * Manu El Poulpe     
 * Frederic Legrain   
 * Roger De Riemaecker
 * Eric Vaneberck
 * Ismail Simoes
 * Denis Renard
 * Pierre
 * Andre Joanisse 
 * Xavier de Gelis
 * Nicolas Micheli
 * Hughes Devaux
 * John S. Gage
 * Jeff   
 * nicolas
 * Ikos
 * C�dric Th�venet
 * Veronique Marie Hammonds
 *
 * filename: french.c
 * Contains french strings. */

#include "libsmooth.h"

char *french_tr[] = {

/**********/
/* COMMON */
/**********/

/* TR_OK */
"Ok",
/* TR_CANCEL */
"Annuler",
/* TR_INSTALLATION_CANCELED */
"L'installation a �t� annul�e.",
/* TR_HELPLINE */
"              <Tab>/<Alt-Tab> entre champs   |  <Space> s�lectionner",
/* TR_QUIT */
"Quitter",
/* TR_DISABLED */
"D�sactiver",
/* TR_ENABLED */
"Activer",
/* TR_UNSET */
"INACTIF",
/* TR_UNABLE_TO_OPEN_SETTINGS_FILE */
"Le fichier de configuration ne peut pas �tre ouVERTEEEE",
/* TR_DONE */
"Terminer",
/* TR_PROBE_FAILED */
"La d�tection automatique a �chou�.",

/*************/
/* LIBSMOOTH */
/*************/

/* main.c  */

/* netstuff.c */
/* TR_IP_ADDRESS_PROMPT */
"Adresse IP:",
/* TR_NETWORK_ADDRESS_PROMPT */
"Adresse r�seau:",
/* TR_NETMASK_PROMPT */
"Masque de r�seau:",
/* TR_ENTER_IP_ADDRESS_INFO */
"Inscrivez l'information de l'adresse IP",
/* TR_INVALID_FIELDS */
"Les champs qui suivent ne sont pas valables:\n\n",
/* TR_IP_ADDRESS_CR */
"Adresse IP\n",
/* TR_NETWORK_ADDRESS_CR */
"Adresse r�seau\n",
/* TR_NETWORK_MASK_CR */
"Masque de r�seau\n",
/* TR_INTERFACE (%s is interface name) */
"%s interface",
/* TR_ENTER_THE_IP_ADDRESS_INFORMATION (%s is interface name) */
"Inscrivez l'information de l'adresse IP pour l'interface %s.",
/* TR_LOOKING_FOR_NIC (%s is a nic name) */
"Recherche: %s",
/* TR_FOUND_NIC (%s is a nic name) */
"Smoothwall a d�tect� l'interface r�seau dans votre machine: %s",
/* TR_MODULE_NAME_CANNOT_BE_BLANK */
"Le nom du module ne peut pas �tre vide.",
/* TR_STATIC */
"Statique",
/* TR_DHCP_HOSTNAME */
"Nom d'h�te DHCP:",
/* TR_DHCP_HOSTNAME_CR */
"Nom d'h�te DHCP\n",

/* misc.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_HOSTNAMECONF */
"Il n'est pas possible d'�crire /var/smoothwall/main/hostname.conf",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS */
"Il n'est pas possible d'�crire /etc/hosts.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_DENY */
"Il n'est pas possible d'�crire /etc/hosts.deny.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_ALLOW */
"Il n'est pas possible d'�crire /etc/hosts.allow.",
/* TR_UNABLE_TO_SET_HOSTNAME */
"Il n'est pas possible de cr�er le nom d'h�te.",

/***********/
/* INSTALL */
/***********/
/* TR_WELCOME */
"Bienvenue au programme d'installation de Smoothwall.  Venez voir " \
"notre page d'accueil � http://www.smoothwall.org.  Si vous annulez " \
"l'un des �crans qui suivent l'ordinateur red�marrera.",
/* TR_NO_IDE_HARDDISK */
"Aucun disque dur IDE.",
/* TR_SELECT_INSTALLATION_MEDIA */
"Choisir une source d'installation",
/* TR_SELECT_INSTALLATION_MEDIA_LONG */
"L'installation smoothwall peut se faire de plusieurs sources.  La m�thode " \
"la plus simple est d'utiliser le lecteur CDROM de l'ordinateur.  Si " \
"l'ordinateur ne poss�de pas de lecteur CDROM, une installation est " \
"encore possible si une autre machine, qui est connect�e au r�seau, " \
"offre les fichiers par HTTP.  Dans ce cas la disquette avec les " \
"pilotes (drivers) des cartes r�seaux est requise.",
/* TR_NO_IDE_CDROM */
"Aucun CDROM IDE.",
/* TR_INSERT_CDROM */
"Placer le CD de Smoothwall dans le lecteur CDROM.",
/* TR_INSERT_FLOPPY */
"Ins�rer la disquette des pilotes (drivers) de Smoothwall dans le lecteur.",
/* TR_PREPARE_HARDDISK */
"Le programme d'installation va maintenant pr�parer le disque dur IDE " \
"de %s. Le disque sera partitionn�, et un syst�me de gestion " \
"de fichiers cr�� sur chaque partition.",
/* TR_PARTITIONING_DISK */
"Le partitionnement du disque est commenc�...",
/* TR_UNABLE_TO_PARTITION */
"Il n'est pas possible de partitionner le disque dur.",
/* TR_MAKING_SWAPSPACE */
"Cr�ation du fichier d'�change...",
/* TR_UNABLE_TO_MAKE_SWAPSPACE */
"Il n'est pas possible de cr�er le fichier d'�change.",
/* TR_MAKING_ROOT_FILESYSTEM */
"Cr�ation du r�pertoire racine...",
/* TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM */
"Il n'est pas possible de cr�er le r�pertoire racine.",
/* TR_MOUNTING_ROOT_FILESYSTEM */
"Montage du r�pertoire racine...",
/* TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM */
"Il n'est pas possible de monter le r�pertoire racine.",
/* TR_MAKING_BOOT_FILESYSTEM */
"Cr�ation du r�pertoire boot...",
/* TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM */
"Il n'est pas possible de cr�er le r�pertoire boot.",
/* TR_MOUNTING_BOOT_FILESYSTEM */
"Montage du r�pertoire boot...",
/* TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM */
"Il n'est pas possible de monter le r�pertoire boot.",
/* TR_MAKING_LOG_FILESYSTEM */
"Cr�ation du r�pertoire log...",
/* TR_UNABLE_TO_MAKE_LOG_FILESYSTEM */
"Il n'est pas possible de cr�er le r�pertoire log.",
/* TR_MOUNTING_LOG_FILESYSTEM */
"Montage du r�pertoire log...",
/* TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM */
"Il n'est pas possible de monter le r�pertoire log.",
/* TR_MOUNTING_SWAP_PARTITION */
"Montage du fichier d'�change...",
/* TR_UNABLE_TO_MOUNT_SWAP_PARTITION */
"Il n'est pas possible de monter le fichier d'�change...",
/* TR_NETWORK_SETUP_FAILED */
"Le param�trage du r�seau a �chou�.",
/* TR_NO_TARBALL_DOWNLOADED */
"Aucune archive tar � t�l�charger.",
/* TR_INSTALLING_FILES */
"Installation des fichiers...",
/* TR_UNABLE_TO_INSTALL_FILES */
"Il n'est pas possible d'installer les fichiers.",
/* TR_UNABLE_TO_REMOVE_TEMP_FILES */
"Il n'est pas possible d'enlever les fichiers temporaires qui ont �t� t�l�charg�s.",
/* TR_ERROR_WRITING_CONFIG */
"Erreur en �crivant les donn�es de configuration.",
/* TR_INSTALLING_LILO */
"Installation de LILO...",
/* TR_UNABLE_TO_INSTALL_LILO */
"Il n'est pas possible d'installer LILO.",
/* TR_UNABLE_TO_UNMOUNT_HARDDISK */
"Il n'est pas possible de d�monter le disque dur.",
/* TR_UNABLE_TO_UNMOUNT_CDROM */
"Il n'est pas possible de d�monter le lecteur CDROM/disquette.",
/* TR_UNABLE_TO_EJECT_CDROM */
"Il n'est pas possible d'expulser le CDROM.",
/* TR_CONGRATULATIONS */
"F�licitations!",
/* TR_CONGRATULATIONS_LONG */
"L'installation de Smoothwall a r�ussit. Retirez le CDROM et la disquette " \
"de l'ordinateur.  La configuration du syst�me va maintenant commencer. " \
"Vous aurez la possibilit� de faire la configuration de vos p�riph�riques RNIS et r�seaux " \
"ainsi que de choisir les mots de passe du syst�me. Une fois que la " \
"configuration sera termin�e, connectez-vous � l'adresse suivante: " \
"http://(adresse IP Smoothwall ou nom):81 ou https://(adresse IP Smoothwall ou nom):445 " \
"et il est sugg�r� que vous configuriez la connexion � internet" \
"(si vous en avez besoin) et l'acc�s � distance.  N'oubliez pas " \
"de sp�cifier un mot de passe pour l'utilisateur 'dial' si vous voulez " \
"que les utilisateurs de Smoothwall non 'admin' puissent avoir contr�le de la ligne.",
/* TR_PRESS_OK_TO_REBOOT */
"Pressez OK pour red�marrer l'ordinateur.",
/* TR_ERROR */
"Erreur",
/* TR_CALCULATING_MODULE_DEPENDANCIES */
"Calcul des d�pendances de module...",
/* TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES */
"Il n'est pas possible de calculer les d�pendances de module.",

/* cdrom.c */
/* TR_SELECT_CDROM_TYPE */
"S�lectionnez un type de CDROM",
/* TR_SELECT_CDROM_TYPE_LONG */
"Un lecteur de CDROM IDE n'a �t� pas trouv� dans l'ordinateur. " \
"S�lectionnez les pilotes suivants que Smoothwall utilisera pour acc�der " \
"au lecteur CDROM.",
/* TR_SUGGEST_IO (%x is an IO number) */
"(suggestion %x)",
/* TR_SUGGEST_IRQ (%d is an IRQ number) */
"(suggestion %d)",
/* TR_CONFIGURE_THE_CDROM */
"Configurez le lecteur  CDROM en choisissant une adresse IO et/ou un IRQ",
/* TR_INVALID_IO (note extra space) */
"Les param�tres pour l'adresse IO ne sont pas valables. ",
/* TR_INVALID_IRQ */
"Les param�tres pour l'IRQ ne sont pas valables.",

/* config.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_SETTINGS */
"Il n'est pas possible d'�crire /var/smoothwall/main/settings.",
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_ETHERNET_SETTINGS */
"Il n'est pas possible d'�crire /var/smoothwall/ethernet/settings.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK */
"Il n'est pas possible de cr�er le lien symbolique /dev/harddisk.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1 */
"Il n'est pas possible de cr�er le lien symbolique /dev/harddisk1.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2 */
"Il n'est pas possible de cr�er le lien symbolique /dev/harddisk2.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3 */
"Il n'est pas possible de cr�er le lien symbolique /dev/harddisk3.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4 */
"Il n'est pas possible de cr�er le lien symbolique /dev/harddisk4.",

/* net.c */
/* TR_DOWNLOADING */
"En cours de t�l�chargement...",
/* TR_FAILED_TO_DOWNLOAD */
"Le t�l�chargement a �chou�.",
/* TR_ENTER_URL */
"Inscrivez l'URL du fichier tar.gz de Smoothwall. " \
"AVERTEEEEISSEMENT: Le DNS n'est pas disponible!  Ceci devrait terminer avec " \
"le fichier 'smoothwall.tgz'.",

/* nic.c */
/* TR_CONFIGURE_NETWORKING */
"Configuration du r�seau",
/* TR_CONFIGURE_NETWORKING_LONG */
"Vous pouvez maintenant configurer les p�riph�riques du r�seau en chargeant " \
"le bon pilote pour l'interface VERTE. Vous avez le choix d'utiliser la " \
"m�thode automatique pour trouver votre carte r�seau, ou de choisir " \
"le bon pilote de la liste.  Notez que si vous avez plus d'une carte r�seau " \
"install�e, vous aurez la chance de configurer les autres plus tard. " \
"C'est aussi tr�s important de noter que si vous avez plus d'une carte " \
"r�seau du m�me type que la carte VERTE, et que chaque carte a besoin de " \
"param�tres sp�ciaux pour le module, vous devrez inscrire les param�tres " \
"pour toutes les cartes de ce type pour qu'elles deviennent toutes actives " \
"quand vous configurerez l'interface VERTE.",
/* TR_INTERFACE_FAILED_TO_COME_UP */
"Le montage de l'interface a �chou�.",
/* TR_ENTER_NETWORK_DRIVER */
"La d�tection automatique de la carte r�seau a �chou�.  Inscrivez le pilote " \
"et les param�tres optionnels pour la carte r�seau.",

/*********/
/* SETUP */
/*********/

/* main.c */
/* TR_HOSTNAME */
"Nom d'h�te",
/* TR_NETWORKING */
"R�seau",
/* TR_DHCP_SERVER_CONFIGURATION */
"Configuration du serveur DHCP",
/* TR_ISDN_CONFIGURATION */
"Configuration RNIS",
/* TR_ROOT_PASSWORD */
"Mot de passe \'root\'",
/* TR_SETUP_PASSWORD */
"Mot de passe \'setup\'",
/* TR_ADMIN_PASSWORD */
"Mot de passe \'admin\'",
/* TR_SECTION_MENU */
"Section menu",
/* TR_SELECT_THE_ITEM */
"Choisissez l'�l�ment que vous voulez configurez.",
/* TR_SETUP_FINISHED */
"Le param�trage est complet.  Pressez OK pour red�marrer l'ordinateur.",
/* TR_SETUP_NOT_COMPLETE */
"L'initialisation n'est pas enti�rement compl�te. Pri�re de vous assurer que "\
"la configuration soit compl�te en red�marrant la configuration depuis le "\
"shell.",

/* passwords.c */
/* TR_ENTER_ROOT_PASSWORD */
"Inscrivez le mot de passe pour l'utilisateur 'root'. Seulement " \
"l'utilisateur 'root' peut acc�der � la ligne de commande.",
/* TR_SETTING_ROOT_PASSWORD */
"Sauvegarde du mot de passe pour 'root'....",
/* TR_PROBLEM_SETTING_ROOT_PASSWORD */
"Il n'est pas possible d'�crire le mot de passe pour 'root'.",
/* TR_ENTER_SETUP_PASSWORD */
"Inscrivez le mot de passe pour l'utilisateur 'setup'. Seulement " \
"l'utilisateur 'setup' peut acc�der au programme de configuration.",
/* TR_SETTING_SETUP_PASSWORD */
"Sauvegarde du mot de passe pour 'setup'....",
/* TR_PROBLEM_SETTING_SETUP_PASSWORD */
"Il n'est pas possible d'�crire le mot de passe pour 'setup'.",
/* TR_ENTER_ADMIN_PASSWORD */
"Inscrivez le mot de passe pour l'administrateur de Smoothwall. " \
"Seulement l'utilisateur 'admin' peut acc�der aux pages webs d'administration.",
/* TR_SETTING_ADMIN_PASSWORD */
"Sauvegarde du mot de passe pour administrateur....",
/* TR_PROBLEM_SETTING_ADMIN_PASSWORD */
"Il n'est pas possible d'�crire le mot de passe pour l'administrateur.",
/* TR_PASSWORD_PROMPT */
"Mot de passe:",
/* TR_AGAIN_PROMPT */
"Encore:",
/* TR_PASSWORD_CANNOT_BE_BLANK */
"Le mot de passe ne peut pas �tre vide.",
/* TR_PASSWORDS_DO_NOT_MATCH */
"Les mots de passe ne sont pas identiques.",

/* hostname.c */
/* TR_ENTER_HOSTNAME */
"Inscrivez le nom d'h�te de la machine.",
/* TR_HOSTNAME_CANNOT_BE_EMPTY */
"Le nom d'h�te ne peut pas �tre vide.",
/* TR_HOSTNAME_CANNOT_CONTAIN_SPACES */
"Le nom d'h�te ne peut pas contenir d'espace.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTNAME */
"Il n'est pas possible d'�crire /etc/hostname",

/* isdn.c */
/* TR_GERMAN_1TR6 */
"Allemand 1TR6",
/* TR_EURO_EDSS1 */
"Euro (EDSS1)",
/* TR_LEASED_LINE */
"Ligne lou�e",
/* TR_US_NI1 */
"�-U NI1",
/* TR_PROTOCOL_COUNTRY */
"Protocole/Pays",
/* TR_ISDN_CARD */
"Carte RNIS",
/* TR_MSN_CONFIGURATION */
"Num�ro d'acc�s local (MSN/EAZ)",
/* TR_SET_ADDITIONAL_MODULE_PARAMETERS */
"Paramm�tres additionnels du module",
/* TR_RED_IN_USE */
"Le RNIS (ou une autre connexion externe) est occup�.  Vous ne pouvez pas " \
"configurer RNIS pendant que l'interface ROUGE est active.",
/* TR_ISDN_CONFIGURATION_MENU */
"Menu de configuration RNIS",
/* TR_ISDN_STATUS */
"Le RNIS actuel %s.\n\n" \
"   Protocole: %s\n" \
"   Carte: %s\n" \
"   Num�ro d'acc�s locale: %s\n\n" \
"S�lectionnez l'�l�ment que vous voulez changer, ou utilisez cette configuration.",
/* TR_ISDN_NOT_YET_CONFIGURED */
"Le RNIS n'est pas configur�. S�lectionnez l'�l�ment que vous voulez configurer.",
/* TR_ENABLE_ISDN */
"Activer RNIS",
/* TR_DISABLE_ISDN */
"D�sactiver RNIS",
/* TR_INITIALISING_ISDN */
"Initialisation du RNIS...",
/* TR_UNABLE_TO_INITIALISE_ISDN */
"Il n'est pas possible d'initialiser RNIS.",
/* TR_ISDN_NOT_SETUP */
"Le RNIS n'est pas configur�.  Certains �l�ments n'ont pas �t� s�lectionn�s.",
/* TR_ISDN_PROTOCOL_SELECTION */
"Protocole RNIS",
/* TR_CHOOSE_THE_ISDN_PROTOCOL */
"S�lectionnez le protocole requis pour RNIS.",
/* TR_AUTODETECT */
"* DETECTION AUTOMATIQUE *",
/* TR_ISDN_CARD_SELECTION */
"Carte RNIS",
/* TR_CHOOSE_THE_ISDN_CARD_INSTALLED */
"S�lectionnez la carte RNIS install�e dans cet ordinateur.",
/* TR_CHECKING_FOR */
"Cherche: %s",
/* TR_ISDN_CARD_NOT_DETECTED */
"La d�tection automatique de la carte RNIS a �chou�e. Il est possible " \
"que vous deviez sp�cifier des param�tres additionnels pour le module " \
"si la carte est de type ISA ou doit �tre trait�e d'une mani�re sp�ciale.",
/* TR_DETECTED */
"D�tecter: %s",
/* TR_UNABLE_TO_FIND_AN_ISDN_CARD */
"Une carte RNIS n'a pas �t� trouv�e dans cet ordinateur.  Il est possible " \
"que vous devez sp�cifier des param�tres additionnels pour le module " \
"si la carte est de type ISA ou doit �tre trait�e d'une mani�re sp�ciale.",
/* TR_ENTER_THE_LOCAL_MSN */
"Inscrivez le num�ro d'acc�s local (MSN/EAZ).",
/* TR_PHONENUMBER_CANNOT_BE_EMPTY */
"Le num�ro d'acc�s local ne peut pas �tre vide.",
/* TR_ENTER_ADDITIONAL_MODULE_PARAMS */
"Certaines cartes RNIS (particuli�rement les cartes de type ISA) requi�rent " \
"des param�tres additionnels pour indiquer au module le bon IRQ ou l'adresse " \
"IO. Si vous poss�dez une de ces carte, inscrivez les param�tres additionnels"\
"ici.  Par exemple: \"io=0x280 irq=9\".  Les param�tres vont �tres utilis�s " \
"pendant que la carte est d�tect�e.",

/* networking.c */
/* TR_PUSHING_NETWORK_DOWN */
"Le r�seau s'arr�te",
/* TR_PULLING_NETWORK_UP */
"Le r�seau red�marre...",
/* TR_NETWORK_CONFIGURATION_TYPE */
"Type de configuration du r�seau",
/* TR_DRIVERS_AND_CARD_ASSIGNMENTS */
"Sp�cification de la carte et du pilote",
/* TR_ADDRESS_SETTINGS */
"Sp�cification des adresses",
/* TR_DNS_AND_GATEWAY_SETTINGS */
"Sp�cification du DNS et des passerelles",
/* TR_RESTART_REQUIRED */
"\n\nUne fois la configuration termin�e, le r�seau devra �tre relanc�.",
/* TR_CURRENT_CONFIG (first %s is type, second is restart message (or not) */
"Configuration actuelle: %s%s",
/* TR_NETWORK_CONFIGURATION_MENU */
"Menu de configuration du r�seau",
/* TR_NETWORK_CONFIGURATION_TYPE_LONG */
"S�lectionnez le configuration du r�seau pour Smoothwall.  Les configurations " \
"qui suivent indiquent les interfaces qui sont reli�es � l'ethernet. " \
"Si vous changez cet �l�ment le r�seau devra �tre relanc�, et " \
"vous serez forc� de reconfigurer les pilotes du r�seau.",
/* TR_PUSHING_NON_LOCAL_NETWORK_DOWN */
"Le r�seau non local s'arr�te...",
/* TR_YOUR_CONFIGURATION_IS_SINGLE_GREEN_ALREADY_HAS_DRIVER */
"Votre configuration est faite pour un seul interface VERTE, avec un pilote " \
"d�j� sp�cifi�.",
/* TR_CONFIGURE_NETWORK_DRIVERS */
"Configurez les pilotes du r�seau, et indiquer quelles interfaces sont " \
"attribu�es � quels pilotes. Voici la configuration actuelle:\n\n",
/* TR_DO_YOU_WISH_TO_CHANGE_THESE_SETTINGS */
"\nVoulez-vous changer les param�tres?",
/* TR_UNCLAIMED_DRIVER */
"Il y a une carte ethernet non attribu�e de type:\n%s\n\n" \
"Vous pouvez l'attribuer �:",
/* TR_CARD_ASSIGNMENT */
"Attribution des cartes",
/* TR_PROBE */
"Sonde",
/* TR_SELECT */
"S�lectionnez",
/* TR_NO_UNALLOCATED_CARDS */
"L'attribution des cartes ne peut pas �tre faite, car il ne reste plus " \
"de cartes. Vous pouvez utiliser la m�thode de d�tection automatique, ou " \
"s�lectionner un pilote de la liste.",
/* TR_UNABLE_TO_FIND_ANY_ADDITIONAL_DRIVERS */
"Aucun pilote additionnel n'a �t� trouv�.",
/* TR_ALL_CARDS_SUCCESSFULLY_ALLOCATED */
"Toutes les cartes ont �t� attribu�es avec succ�s.",
/* TR_NOT_ENOUGH_CARDS_WERE_ALLOCATED */
"Il n'y avait pas assez de cartes pour finir l'attribution.",
/* TR_MANUAL */
"* MANUEL *",
/* TR_SELECT_NETWORK_DRIVER */
"S�lectionnez un pilote de r�seau",
/* TR_SELECT_NETWORK_DRIVER_LONG */
"S�lectionnez le pilote pour la carte de r�seau install�s dans cette machine. " \
"Si vous choisi MANUEL, vous aurez la possibilit� d'inscrire le nom du module " \
"et les param�tres pour les cartes sp�ciales comme celles de type ISA.",
/* TR_UNABLE_TO_LOAD_DRIVER_MODULE */
"Il n'est pas possible de charger le pilote.",
/* TR_THIS_DRIVER_MODULE_IS_ALREADY_LOADED */
"Le pilote est d�j� charg�.",
/* TR_MODULE_PARAMETERS */
"Inscrivez le nom du module et les param�tres qui sont requis pour le pilote." ,
/* TR_LOADING_MODULE */
"Le module se charge...",
/* TR_WARNING */
"AVERTEEEEISSEMENT",
/* TR_WARNING_LONG */
"Si vous changez l'adresse IP, et que vous �tes logu� par acc�s � distance, " \
"la connexion � la machine Smoothwall sera interrompue et vous aurez besoin " \
"de vous reconnecter avec la nouvelle adresse IP.  Ceci est une op�ration qui " \
"est tr�s risqu�e et qui devrait seulement �tre essay�e si vous avez " \
"directement acc�s a la machine pour r�gler les probl�mes �ventuels.",
/* TR_SINGLE_GREEN */
"Votre configuration est pr�par�e pour un interface VERTE simple.",
/* TR_SELECT_THE_INTERFACE_YOU_WISH_TO_RECONFIGURE */
"S�lectionnez l'interface que vous d�sirez reconfigurer.",
/* TR_DNS_GATEWAY_WITH_GREEN */
"Votre configuration n'utilise pas un p�riph�rique ethernet pour " \
"l'interface ROUGE. Les param�tres pour le DNS et la passerelle sont " \
"configur�s automatiquement pour les utilisateurs avec acc�s r�seau quand " \
"la connexion est �tablie.",
/* TR_PRIMARY_DNS */
"DNS primaire:",
/* TR_SECONDARY_DNS */
"DNS secondaire:",
/* TR_DEFAULT_GATEWAY */
"Passerelle:",
/* TR_DNS_AND_GATEWAY_SETTINGS_LONG */
"Inscrivez l'information du DNS et de la passerelle. Ces param�tres seront " \
"seulement utilis�s si le DHCP est d�sactiv� � partir de l'interface ROUGE.",
/* TR_PRIMARY_DNS_CR */
"DNS primaire\n",
/* TR_SECONDARY_DNS_CR */
"DNS secondaire\n",
/* TR_DEFAULT_GATEWAY_CR */
"Passerelle\n",
/* TR_SECONDARY_WITHOUT_PRIMARY_DNS */
"Le DNS secondaire ne peut pas �tre sp�cifi� sans un DNS primaire",
/* TR_UNKNOWN */
"INCONNU",
/* TR_NO_ORANGE_INTERFACE */
"Aucune interface ORANGE n'a �t� allou�e.",
/* TR_MISSING_ORANGE_IP */
"L'information IP pour l'interface ORANGE n'est pas compl�te.",
/* TR_NO_RED_INTERFACE */
"Aucune interface ROUGE n'a �t� allou�e.",
/* TR_MISSING_RED_IP */
"L'information IP pour l'interface ROUGE n'est pas compl�te.",

/* dhcp.c */
/* TR_START_ADDRESS */
"Adresse de d�part:",
/* TR_END_ADDRESS */
"Adresse de fin:",
/* TR_DEFAULT_LEASE */
"Temps de pr�t par d�faut (mins):",
/* TR_MAX_LEASE */
"Temps de pr�t maximum (mins):",
/* TR_DOMAIN_NAME_SUFFIX */
"Suffixe de nom de domaine:",
/* TR_CONFIGURE_DHCP */
"Configurez le serveur DHCP en entrant l'information de configuration.",
/* TR_START_ADDRESS_CR */
"Adresse de d�part\n",
/* TR_END_ADDRESS_CR */
"Adresse de fin\n",
/* TR_DEFAULT_LEASE_CR */
"Temps de pr�t par d�faut\n",
/* TR_MAX_LEASE_CR */
"Temps de pr�t maximum\n",
/* TR_DOMAIN_NAME_SUFFIX_CR */
"Suffixe de nom de domaine\n",

/* keymap.c */
/* TR_KEYBOARD_MAPPING */
"Type de clavier",
/* TR_KEYBOARD_MAPPING_LONG */
"Choisissez le type de clavier que vous utilisez dans la liste ci-dessous.",

/* timezone.c */
/* TR_TIMEZONE */
"Fuseau horaire",
/* TR_TIMEZONE_LONG */
"Choisissez le fuseau horaire dans lequel voue �tes dans la liste ci-dessous.",

/* usbadsl.c */
/* TR_USB_CONTROLLER */
"Selectionnez le contr�leur USB",
/* TR_USBADSL_STATUS */
"L'ADSL USB est actuellement: %s\n" \
"   Contr�leur: %s\n\n" \
"Selectionez ce que vous voulez reconfigurer, ou choisissez d'utiliser les "\
"param�tres courants.",
/* TR_USBADSL_CONFIGURATION */
"Configuration de l'USB ADSL ",
/* TR_ENABLE_USBADSL */
"Activer l'USB ADSL",
/* TR_DISABLE_USBADSL */
"D�sactiver l'USB ADSL",
/* TR_INITIALISING_USBADSL */
"Initialisation de l'USB ADSL.",
/* TR_UNABLE_TO_INITIALISE_USBADSL */
"Impossible d'initialiser l'USB ADSL",
/* TR_USBADSL_NOT_SETUP */
"USB ADSL non configur�.",
/* TR_USB_CONTROLLER_SELECTION */
"S�lection du contr�leur USB",
/* TR_CHOOSE_THE_USB_CONTROLLER_INSTALLED */
"Choisissez le contr�leur USB install� sur la machine Smoothwall .",
/* TR_USB_CONTROLLER_NOT_DETECTED */
"Contr�leur USB non d�tect�.",
/* TR_UNABLE_TO_FIND_A_USB_CONTROLLER */
"Impossible de trouver un contr�leur USB.",
/* TR_STARTING_UP_USBADSL */
"D�marrage de l'USB ADSL..."

};
