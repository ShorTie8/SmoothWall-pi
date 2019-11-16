/* SmoothWall libsmooth.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * (c) Spanish Translation Team
 * Luis Ludovico
 * Bruno Maderni
 * Jaime Herrera
 * Juan Moncayo
 * Yonathan Sabbah
 * Marco van Beek
 * Ra|l Martmnez Peris 
 *
 * filename: spanish.c
 * Contains spanish strings. */

#include "libsmooth.h"

char *spanish_tr[] = {

/**********/
/* COMMON */
/**********/

/* TR_OK */
"Ok",
/* TR_CANCEL */
"Cancelar",
/* TR_INSTALLATION_CANCELED */
"Instalaci�n cancelada.",
/* TR_HELPLINE */
"           <Tab>/<Alt-Tab> entre elementos   |  <Space> seleccionar",
/* TR_QUIT */
"Salir",
/* TR_DISABLED */
"Deshabilitado",
/* TR_ENABLED */
"Habilitado",
/* TR_UNSET */
"Sin predefinir",
/* TR_UNABLE_TO_OPEN_SETTINGS_FILE */
"No se puede abrir el archivo de configuraci�n.",
/* TR_DONE */
"Listo",
/* TR_PROBE_FAILED */
"La detecci�n automatica ha fallado.",

/*************/
/* LIBSMOOTH */
/*************/

/* main.c  */

/* netstuff.c */
/* TR_IP_ADDRESS_PROMPT */
"Direcci�n IP:",
/* TR_NETWORK_ADDRESS_PROMPT */
"Direcci�n de RED:",
/* TR_NETMASK_PROMPT */
"Mascara de RED:",
/* TR_ENTER_IP_ADDRESS_INFO */
"Inserte la informaci�n de IP",
/* TR_INVALID_FIELDS */
"Los siguiente campos son invalidos\n\n",
/* TR_IP_ADDRESS_CR */
"Direcci�n de IP\n",
/* TR_NETWORK_ADDRESS_CR */
"Direcci�n de RED\n",
/* TR_NETWORK_MASK_CR */
"Mascara de RED\n",
/* TR_INTERFACE (%s is interface name) */
"%s interface",
/* TR_ENTER_THE_IP_ADDRESS_INFORMATION (%s is interface name) */
"Inserte la direcci�n IP para la interfaz %s .",
/* TR_LOOKING_FOR_NIC (%s is a nic name) */
"Buscando el siguiente adaptador: %s",
/* TR_FOUND_NIC (%s is a nic name) */
"Smoothwall ha detectado la siguiente interfaz de red: %s",
/* TR_MODULE_NAME_CANNOT_BE_BLANK */
"El nombre de m�dulo no puede estar vacio.",
/* TR_STATIC */
"Estatica",
/* TR_DHCP_HOSTNAME */
"Nombre del DHCP:",
/* TR_DHCP_HOSTNAME_CR */
"Nombre del DHCP\n",

/* misc.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_HOSTNAMECONF */
"Imposible escribir /var/smoothwall/main/hostname.conf",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS */
"Imposible escribir /etc/hosts.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_DENY */
"Imposible escribir /etc/hosts.deny.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_ALLOW */
"No es posible escribir /etc/hosts.allow.",
/* TR_UNABLE_TO_SET_HOSTNAME */
"No es posible configurar el nombre de host.",

/***********/
/* INSTALL */
/***********/
/* TR_WELCOME */
"Bienvenido al programa de instalaci�n de Smoothwall. Por favor visite nuestra " \
"p�gina en http://www.smoothwall.org. Seleccionando Cancelar en cualquiera " \
"de las siguientes pantallas reiniciar� la computadora.",
/* TR_NO_IDE_HARDDISK */
"Disco r�gido IDE no encontrado.",
/* TR_SELECT_INSTALLATION_MEDIA */
"Seleccione el medio de instalaci�n",
/* TR_SELECT_INSTALLATION_MEDIA_LONG */
"Smoothwall puede ser instalado desde m�ltiples fuentes. La mas simple es " \
"usar el CDROM de la m�quina. Si la computadora no tiene CDROM, puede " \
"instalarse a trav�s de otra m�quina en la LAN que tenga los archivos de instalaci�n " \
"disponibles via HTTP. En este caso el diskette con los controladores de red ser�n " \
"requeridos.",
/* TR_NO_IDE_CDROM */
"IDE cdrom no encontrado.",
/* TR_INSERT_CDROM */
"Por favor inserte el CD de Smoothwall en el CDROM.",
/* TR_INSERT_FLOPPY */
"Por favor inserte el diskette del controlador de Smootwall en la disketera.",
/* TR_PREPARE_HARDDISK */
"El programa de instalaci�n preparar� ahora el disco r�gido IDE en %s. " \
"Primero el disco ser� particionado y luego las particiones tendr�n " \
"un sistema de archivos puestos en ellas.",
/* TR_PARTITIONING_DISK */
"Particionando el disco...",
/* TR_UNABLE_TO_PARTITION */
"No es posible particionar el disco.",
/* TR_MAKING_SWAPSPACE */
"Creando espacio SWAP...",
/* TR_UNABLE_TO_MAKE_SWAPSPACE */
"Imposible crear espacio SWAP.",
/* TR_MAKING_ROOT_FILESYSTEM */
"Creando sistema de archivos ra�z...",
/* TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM */
"No es posible crear el sistema de archivos ra�z.",
/* TR_MOUNTING_ROOT_FILESYSTEM */
"Montando sistema de archivos ra�z...",
/* TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM */
"No es posible montar el sistema de archivos ra�z.",
/* TR_MAKING_BOOT_FILESYSTEM */
"Creando sistema de archivos de booteo...",
/* TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM */
"No es posible crear el sistema de archivos de booteo.",
/* TR_MOUNTING_BOOT_FILESYSTEM */
"Montando sistemas de archivo de booteo...",
/* TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM */
"No es posbile montar el sistema de archivos de booteo.",
/* TR_MAKING_LOG_FILESYSTEM */
"Creando sistema de archivos log...",
/* TR_UNABLE_TO_MAKE_LOG_FILESYSTEM */
"No es posible crear el sistema de archivos log.",
/* TR_MOUNTING_LOG_FILESYSTEM */
"Montando el sistema de archivos log...",
/* TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM */
"No es posible montar el sistema de archivos log.",
/* TR_MOUNTING_SWAP_PARTITION */
"Montando partici�n SWAP...",
/* TR_UNABLE_TO_MOUNT_SWAP_PARTITION */
"No es posible montar la partici�n SWAP.",
/* TR_NETWORK_SETUP_FAILED */
"Fall� la configuraci�n de Red.",
/* TR_NO_TARBALL_DOWNLOADED */
"Ning�n tarball descargado.",
/* TR_INSTALLING_FILES */
"Instalando archivos...",
/* TR_UNABLE_TO_INSTALL_FILES */
"No es posible instalar archivos.",
/* TR_UNABLE_TO_REMOVE_TEMP_FILES */
"No es posible remover los archivos temporales descargados.",
/* TR_ERROR_WRITING_CONFIG */
"Error escribiendo informaci�n de configuraci�n.",
/* TR_INSTALLING_LILO */
"Instalando LILO...",
/* TR_UNABLE_TO_INSTALL_LILO */
"No es posible instalar LILO.",
/* TR_UNABLE_TO_UNMOUNT_HARDDISK */
"No es posible desmontar el disco r�gido.",
/* TR_UNABLE_TO_UNMOUNT_CDROM */
"No es posible desmontar el CDROM/diskette.",
/* TR_UNABLE_TO_EJECT_CDROM */
"No es posible expulsar el CDROM.",
/* TR_CONGRATULATIONS */
"Felicitaciones!",
/* TR_CONGRATULATIONS_LONG */
"La instalaci�n de Smoothwall se ha realizado con �xito. Retire por favor cualquier" \
"disquette o CD-ROM del ordenador. El programa de Configuraci�n le guiar�" \
"a continuaci�n a trav�s de distintas opciones donde usted podr�" \
"configurar sus dispositivos RDSI, tarjetas de red, as� como las" \
"contrase�as del sistema. Una vez terminada la configuraci�n, deber� escribir " \
"en su navegador de internet la direcci�n http://smoothwall:81 o " \
"https://smoothwall:445 (o cambiando Smoothwall por el nombre con que lo haya " \
"personalizado), a continuaci�n deber� configurar la conexi�n telef�nica" \
"(si es necesario) y el acceso remoto. No se olvide poner las contrase�as" \
"para SmootWall del usuario 'dial', si no puede conectar a Smoothwall" \
"el usuario 'admin' est� capacitado para corregir cualquier error de configuraci�n.",
/* TR_PRESS_OK_TO_REBOOT */
"Pulse Ok para reiniciar el ordenador.",
/* TR_ERROR */
"Error",
/* TR_CALCULATING_MODULE_DEPENDANCIES */
"Calculando las dependencias de los m�dulos...",
/* TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES */
"Incapaz de calcular las dependencias de los m�dulos.",

/* cdrom.c */
/* TR_SELECT_CDROM_TYPE */
"Seleccione el tipo de CD-ROM",
/* TR_SELECT_CDROM_TYPE_LONG */
"No se ha detectado una unidad CD-ROM IDE en este ordenador. Por favor, seleccione " \
"uno de los siguientes controladores que desee Smoothwall utilice para controlar el CD-ROM.",
/* TR_SUGGEST_IO (%x is an IO number) */
"(recomendamos %x)",
/* TR_SUGGEST_IRQ (%d is an IRQ number) */
"(recomendamos %d)",
/* TR_CONFIGURE_THE_CDROM */
"Configure el CD-ROM seleccionando direcci�n IO y/o la IRQ apropiada.",
/* TR_INVALID_IO (note extra space) */
"El puerto IO que ha introducido no es v�lido. ",
/* TR_INVALID_IRQ */
"La IRQ que ha introducido no es v�lida.",

/* config.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_SETTINGS */
"Incapaz de escribir /var/smoothwall/main/settings.",
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_ETHERNET_SETTINGS */
"Incapaz de escribir /var/smoothwall/ethernet/settings.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK */
"Incapaz de crear un enlace a /dev/harddisk.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1 */
"Incapaz de crear un enlace a /dev/harddisk1.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2 */
"Incapaz de crear un enlace a /dev/harddisk2.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3 */
"Incapaz de crear un enlace a /dev/harddisk3.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4 */
"Incapaz de crear un enlace a /dev/harddisk4.",

/* net.c */
/* TR_DOWNLOADING */
"Descargando...",
/* TR_FAILED_TO_DOWNLOAD */
"Fallo al descargar el archivo de la red.",
/* TR_ENTER_URL */
"Introduzca la URL del archivo 'tar.gz' de Smoothwall. " \
"�ATENCION: DNS no disponible! Se debe terminar con el fichero 'smoothwall.tgz'.",

/* nic.c */
/* TR_CONFIGURE_NETWORKING */
"Configurando la red",
/* TR_CONFIGURE_NETWORKING_LONG */
"Debe configurar primero la red GREEN cargando el controlador apropiado. " \
"Debe seleccionar el controlar a trav�s de la auto-detecci�n de la tarjeta de red" \
"o eligiendo el controlador correcto de la lista. D�se cuenta que si tiene varias " \
"tarjetas de red instaladas, deber� configurarlas todas posteriormente a la instalaci�n." \
"N�tese tambi�n que si tiene m�s de una tarjeta del mismo tipo que la GREEN y " \
"dicha tarjeta requiere par�metros especiales de configuraci�n, deber� introducir" \
"todos los par�metros en todas las tarjetas del mismo tipo para que todas las tarjetas"  \
"se puedan utilizar cuando haya configurado la interfaz GREEN.",
/* TR_INTERFACE_FAILED_TO_COME_UP */
"Ha sido imposible inicilizar la interfaz.",
/* TR_ENTER_NETWORK_DRIVER */
"Ha fallado la detecci�n autom�tica de la tarjeta de red." \
"Introduce el controlador y los par�metros opcionales de la tarjeta de red.",

/*********/
/* SETUP */
/*********/

/* main.c */
/* TR_HOSTNAME */
"Nombre del servidor",
/* TR_NETWORKING */
"Red",
/* TR_DHCP_SERVER_CONFIGURATION */
"Configuraci�n del servidor DHCP",
/* TR_ISDN_CONFIGURATION */
"Configuraci�n RSDI",
/* TR_ROOT_PASSWORD */
"Contrase�a del usuario \'root\'",
/* TR_SETUP_PASSWORD */
"Contrase�a del usuario \'setup\'",
/* TR_ADMIN_PASSWORD */
"Contrase�a del usuario Admin",
/* TR_SECTION_MENU */
"Men� de la secci�n",
/* TR_SELECT_THE_ITEM */
"Seleccione el item que desea configurar.",
/* TR_SETUP_FINISHED */
"La instalaci�n esta completa. Presione Aceptar para reinciar.",
/* TR_SETUP_NOT_COMPLETE */
"La instalaci�n inicial no se completo en su totalidad. Debe asegurarse que la instalaci�n es" \
"correctamente finalizada ejecutando el comando setup nuevamente desde el Shell.",

/* passwords.c */
/* TR_ENTER_ROOT_PASSWORD */
"Ingrese la contrase�a del usuario 'root'. Ingrese con este usuario para acceder a la linea de comandos.",
/* TR_SETTING_ROOT_PASSWORD */
"Configurando la contrase�a para 'root'...",
/* TR_PROBLEM_SETTING_ROOT_PASSWORD */
"Hubo problemas mientras se configuraba la contrase�a para 'root'.",
/* TR_ENTER_SETUP_PASSWORD */
"Ingrese la contrase�a del usuario 'setup'. Ingrese con este usuario para acceder al programa de " \
"configuraci�n.",
/* TR_SETTING_SETUP_PASSWORD */
"Configurando la contrase�a para 'setup'...",
/* TR_PROBLEM_SETTING_SETUP_PASSWORD */
"Hubo problemas mientras se configuraba la contrase�a para 'setup'.",
/* TR_ENTER_ADMIN_PASSWORD */
"Ingrese la contrase�a del usuario admin de Smoothwall. Este es el usuario para utilizar " \
"las p�ginas web de administraci�n de Smoothwall.",
/* TR_SETTING_ADMIN_PASSWORD */
"Configurando la contrase�a del usuario admin de Smoothwall ...",
/* TR_PROBLEM_SETTING_ADMIN_PASSWORD */
"Hubo problemas mientras se configuraba la contrase�a para admin.",
/* TR_PASSWORD_PROMPT */
"Contrase�a:",
/* TR_AGAIN_PROMPT */
"Nuevamente:",
/* TR_PASSWORD_CANNOT_BE_BLANK */
"La contrase�a no pude quedar vacia.",
/* TR_PASSWORDS_DO_NOT_MATCH */
"Las contrase�as no coinciden.",

/* hostname.c */
/* TR_ENTER_HOSTNAME */
"Ingrese el nombre del ordenador.",
/* TR_HOSTNAME_CANNOT_BE_EMPTY */
"El nombre del ordenador no puede dejarse vacio.",
/* TR_HOSTNAME_CANNOT_CONTAIN_SPACES */
"El nombre del ordenador no puede contener espacios.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTNAME */
"Incapaz de grabar en /etc/hostname",

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
"Protocolo/Pa�s",
/* TR_ISDN_CARD */
"Tarjeta RSDI",
/* TR_MSN_CONFIGURATION */
"N�mero telef�nico local (MSN/EAZ)",
/* TR_SET_ADDITIONAL_MODULE_PARAMETERS */
"Configurar par�metros adicionales",
/* TR_RED_IN_USE */
"RSDI (o otra conexi�n externa) estan actualmente en uso. No puede " \
"configurar RSDI mientras la interfaz RED este activa.",
/* TR_ISDN_CONFIGURATION_MENU */
"Menu de configuraci�n ISDN",
/* TR_ISDN_STATUS */
"RSDI es actualmente %s.\n\n" \
"   Protocolo: %s\n" \
"   Placa: %s\n" \
"   N�mero telef�nico local: %s\n\n" \
"Seleccione el item que desea reconfigurar, o eliga de utilizar la configuraci�n actual.",
/* TR_ISDN_NOT_YET_CONFIGURED */
"RSDI aun no ha sido configurado. Seleccione el item que desea configurar.",
/* TR_ENABLE_ISDN */
"Activar RSDI",
/* TR_DISABLE_ISDN */
"Desactivar RSDI",
/* TR_INITIALISING_ISDN */
"Inicializando RSDI...",
/* TR_UNABLE_TO_INITIALISE_ISDN */
"Incapaz de inicializar RSDI.",
/* TR_ISDN_NOT_SETUP */
"RSDI no esta configurado. Algnos items pueden no haber sido seleccionados aun.",
/* TR_ISDN_PROTOCOL_SELECTION */
"Selecci�n de protocolo RSDI",
/* TR_CHOOSE_THE_ISDN_PROTOCOL */
"Seleccione el protocolo RSDI requerido",
/* TR_AUTODETECT */
"* AUTODETECci�n *",
/* TR_ISDN_CARD_SELECTION */
"Selecci�n de tarjeta RSDI",
/* TR_CHOOSE_THE_ISDN_CARD_INSTALLED */
"Seleccione la tarjeta RSDI instalada en este ordenador.",
/* TR_CHECKING_FOR */
"Controlando por: %s",
/* TR_ISDN_CARD_NOT_DETECTED */
"No se detecto una tarjeta RSDI. Deber� especificar par�metros de m�dulos adicionales " \
"si la tarjeta es tipo ISA o si requiere par�metros especiales.",
/* TR_DETECTED */
"Detectada como: %s",
/* TR_UNABLE_TO_FIND_AN_ISDN_CARD */
"Incapaz de encontrar un placa RSDI en este ordenador. Deber� especificar par�metros " \
"de m�dulos adicionales si la tarjeta es tipo ISA o si requiere de par�metros " \
"especiales.",
/* TR_ENTER_THE_LOCAL_MSN */
"Ingrese el n�mero telef�nico local (MSN/EAZ).",
/* TR_PHONENUMBER_CANNOT_BE_EMPTY */
"El n�mero telef�nico no puede quedar vacio.",
/* TR_ENTER_ADDITIONAL_MODULE_PARAMS */
"Algunas tarjetas RSDI(especialmente las tipo ISA) pueden requerir par�metros de m�dulo " \
"adicionales para configurar el IRQ e informaci�n de direcci�n de IO. Si tiene una tarjeta " \
"RSDI como estas, ingrese estos par�metros adicionales aqu�. Por ejemplo: " \
"\"io=0x280 irq=9\". Ser�n utilizados durante la detecci�n de la tarjeta.",

/* networking.c */
/* TR_PUSHING_NETWORK_DOWN */
"Bajando servicios de red...",
/* TR_PULLING_NETWORK_UP */
"Subiendo servicios de red...",
/* TR_NETWORK_CONFIGURATION_TYPE */
"Tipo de configuraci�n de red",
/* TR_DRIVERS_AND_CARD_ASSIGNMENTS */
"Asignaci�n de adaptadores de red y controladores",
/* TR_ADDRESS_SETTINGS */
"Configuraci�n de direcciones",
/* TR_DNS_AND_GATEWAY_SETTINGS */
"Configuraci�n de compuerta y DNS",
/* TR_RESTART_REQUIRED */
"\n\nCuando se complete la configuraci�n, ser� necesario reiniciar los servicios de red.",
/* TR_CURRENT_CONFIG (first %s is type, second is restart message (or not) */
"Configuraci�n actual: %s%s",
/* TR_NETWORK_CONFIGURATION_MENU */
"Menu de configuraci�n de red",
/* TR_NETWORK_CONFIGURATION_TYPE_LONG */
"Seleccione la configuraci�n de red para Smoothwall. Los siguientes " \
"tipos de configuraci�n muestran las interfases que tienen ethernet adosadas. " \
"Si cambia esta configuraci�n, los servicios de red ser�n reiniciados y " \
"deber� reconfigurar la asignaci�n de adaptadores/controladores de red.",
/* TR_PUSHING_NON_LOCAL_NETWORK_DOWN */
"Bajando servicios de red que no fueran de red local...",
/* TR_YOUR_CONFIGURATION_IS_SINGLE_GREEN_ALREADY_HAS_DRIVER */
"Su configuraci�n fue programada para un solo adaptador de red GREEN, " \
"el cual ya tiene un driver asignado.",
/* TR_CONFIGURE_NETWORK_DRIVERS */
"Configure los controladores de red, y que interfaz tiene cada uno" \
"asignado tambien. La configuraci�n actual es la siguiente:\n\n",
/* TR_DO_YOU_WISH_TO_CHANGE_THESE_SETTINGS */
"\n�Desea cambiar esta configuraci�n?",
/* TR_UNCLAIMED_DRIVER */
"Existe una tarjeta ethernet no asignada del tipo:\n%s\n\n" \
"Puede asignar esta a:",
/* TR_CARD_ASSIGNMENT */
"Asignar Tarjeta",
/* TR_PROBE */
"Probar",
/* TR_SELECT */
"Seleccionar",
/* TR_NO_UNALLOCATED_CARDS */
"No quedan placas sin asignar, " \
"pero se requieten adicionales. Puede autodetectar en busca de otras placas, o " \
"seleccionar un controlador de los disponibles en la lista.",
/* TR_UNABLE_TO_FIND_ANY_ADDITIONAL_DRIVERS */
"Imposibilitado de encontrar nuevos controladores.",
/* TR_ALL_CARDS_SUCCESSFULLY_ALLOCATED */
"Todas las tarjetas fueron correctamente asignadas.",
/* TR_NOT_ENOUGH_CARDS_WERE_ALLOCATED */
"No hay mas tarjetas para asignar.",
/* TR_MANUAL */
"* MANUAL *",
/* TR_SELECT_NETWORK_DRIVER */
"Seleccione un controlador",
/* TR_SELECT_NETWORK_DRIVER_LONG */
"Seleccione el controlador par la tarjeta instalada en este ordenador. " \
"Si selecciono MANUAL, tendr� la oportunidad de ingresar" \
"el nombre del m�dulo y los par�metros para los controladores que " \
"requieran par�metros especiales, como ser la tarjetas tipo ISA.",
/* TR_UNABLE_TO_LOAD_DRIVER_MODULE */
"Inposibilitado de cargar el m�dulo del controlador.",
/* TR_THIS_DRIVER_MODULE_IS_ALREADY_LOADED */
"El m�dulo controlador ya se encuentra carfado.",
/* TR_MODULE_PARAMETERS */
"Ingrese el nombre del m�dulo y los par�metros que requiera el controlador.",
/* TR_LOADING_MODULE */
"Cargando m�dulo...",
/* TR_WARNING */
"PELIGRO",
/* TR_WARNING_LONG */
"Si cambia la direcci�n IP, y se encuentra conectado en forma remota, " \
"perder� su conexi�n con la m�quina Smoothwall, y tendra que reconectar " \
"con la nueva direcci�n IP . Esta es una operaci�n riesgosa y solo debe" \
"realizarse si tiene acceso f�sico a la m�quina por si algo malo " \
"sucediera.",
/* TR_SINGLE_GREEN */
"Su configuraci�n es para una unica interfaz de red GREEN.",
/* TR_SELECT_THE_INTERFACE_YOU_WISH_TO_RECONFIGURE */
"Seleccione la interfaz que dese reconfigurar.",
/* TR_DNS_GATEWAY_WITH_GREEN */
"Su configuraci�n no utiliza una adapator de red ethernet para la interfaz " \
"RED. La informaci�n de DNS de compuerta predeterminada para usuarios de " \
"acceso telefonico es configurada automaticamente en el momento de discar.",
/* TR_PRIMARY_DNS */
"DNS primario:",
/* TR_SECONDARY_DNS */
"DNS secundario:",
/* TR_DEFAULT_GATEWAY */
"Compuerta predeterminada:",
/* TR_DNS_AND_GATEWAY_SETTINGS_LONG */
"Ingrese informaci�n de compuerta predeterminda y DNS. Esta informaci�n solo ser� utilizada si DHCP  " \
"se encontrara desactivado en la interfaz RED.",
/* TR_PRIMARY_DNS_CR */
"DNS primario\n",
/* TR_SECONDARY_DNS_CR */
"DNS secundario\n",
/* TR_DEFAULT_GATEWAY_CR */
"Compuerta predeterminada\n",
/* TR_SECONDARY_WITHOUT_PRIMARY_DNS */
"Configuro un DNS secundario sin haber especificado el primario",
/* TR_UNKNOWN */
"DESCONOCIDO",
/* TR_NO_ORANGE_INTERFACE */
"No se asigno interfaz ORANGE.",
/* TR_MISSING_ORANGE_IP */
"Falta informaci�n IP en la interfaz ORANGE.",
/* TR_NO_RED_INTERFACE */
"No se asigno interfaz RED.",
/* TR_MISSING_RED_IP */
"Falta informaci�n IP en la interfaz RED.",

/* dhcp.c */
/* TR_START_ADDRESS */
"Primera direcci�n:",
/* TR_END_ADDRESS */
"Ultima direcci�n:",
/* TR_DEFAULT_LEASE */
"Tiempo de arriendo:",
/* TR_MAX_LEASE */
"M�ximo tiempo de arriendo:",
/* TR_DOMAIN_NAME_SUFFIX */
"Prefijo de dominio:",
/* TR_CONFIGURE_DHCP */
"Configure el servicio DHCP completando la siguiente informaci�n de configuraci�n.",
/* TR_START_ADDRESS_CR */
"Primera direcci�n\n",
/* TR_END_ADDRESS_CR */
"Ultima direcci�n\n",
/* TR_DEFAULT_LEASE_CR */
"Tiempo de arriendo\n",
/* TR_MAX_LEASE_CR */
"M�ximo tiempo de arriendo\n",
/* TR_DOMAIN_NAME_SUFFIX_CR */
"Prefijo de dominio\n",

/* keymap.c */
/* TR_KEYBOARD_MAPPING */
"Distribuci�n del teclado",
/* TR_KEYBOARD_MAPPING_LONG */
"Elija el tipo de teclado que est� usando seg�n la siguiente lista.",

/* timezone.c */
/* TR_TIMEZONE */
"Zona horaria",
/* TR_TIMEZONE_LONG */
"Elija su zona horaria donde se encuentre seg�n la siguiente lista.",

/* usbadsl.c */
/* TR_USB_CONTROLLER */
"Seleccione el controlador USB",
/* TR_USBADSL_STATUS */
"USB ADSL es actualmente: %s\n" \
"   Controlador: %s\n\n" \
"Seleccione el item que desea configurar, o elija la configuraci�n actual.",
/* TR_USBADSL_CONFIGURATION */
"Configuraci�n USB ADSL",
/* TR_ENABLE_USBADSL */
"Activar USB ADSL",
/* TR_DISABLE_USBADSL */
"Desactivar USB ADSL",
/* TR_INITIALISING_USBADSL */
"Inicializando USB ADSL.",
/* TR_UNABLE_TO_INITIALISE_USBADSL */
"Imposibilitado de inicializar USB ADSL",
/* TR_USBADSL_NOT_SETUP */
"No fue configurado USB ADSL",
/* TR_USB_CONTROLLER_SELECTION */
"Selecci�n de controlador USB",
/* TR_CHOOSE_THE_USB_CONTROLLER_INSTALLED */
"Seleccione el controlador USB instalado en su m�quina Smoothwall.",
/* TR_USB_CONTROLLER_NOT_DETECTED */
"Controlador USB no pudo ser detectado.",
/* TR_UNABLE_TO_FIND_A_USB_CONTROLLER */
"Inposibilitado de encontrar un controlador USB.",
/* TR_STARTING_UP_USBADSL */
"Inciando servicios de USB ADSL..."

};
