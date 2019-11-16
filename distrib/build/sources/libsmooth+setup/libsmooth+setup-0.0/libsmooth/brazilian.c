/* SmoothWall libsmooth.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * Brazillian Portuguese Translation Team:
 * Gilberto Gaudencio
 * Uelinton B. dos Santos
 *
 * filename: brazillain.c
 * Contains brazillian strings. */

#include "libsmooth.h"

char *brazilian_tr[] = {

/**********/
/* COMMON */
/**********/

/* TR_OK */
"Ok",
/* TR_CANCEL */
"Cancelar",
/* TR_INSTALLATION_CANCELED */
"Instala��o cancelada.",
/* TR_HELPLINE */
"              <Tab>/<Alt-Tab> movimentar   |  <Espa�o> selecionar",
/* TR_QUIT */
"Sair",
/* TR_DISABLED */
"Desativado",
/* TR_ENABLED */
"Ativado",
/* TR_UNSET */
"N�o especificado",
/* TR_UNABLE_TO_OPEN_SETTINGS_FILE */
"N�o foi poss�vel abrir arquivo de configura��o",
/* TR_DONE */
"Feito",
/* TR_PROBE_FAILED */
"A auto-detec��o falhou.",

/*************/
/* LIBSMOOTH */
/*************/

/* main.c  */

/* netstuff.c */
/* TR_IP_ADDRESS_PROMPT */
"Endere�o IP:",
/* TR_NETWORK_ADDRESS_PROMPT */
"Endere�o de rede:",
/* TR_NETMASK_PROMPT */
"M�scara de rede:",
/* TR_ENTER_IP_ADDRESS_INFO */
"Introduza informa��es sobre o endere�o IP",
/* TR_INVALID_FIELDS */
"Os seguintes campos n�o s�o v�lidos:\n\n",
/* TR_IP_ADDRESS_CR */
"Endere�o IP\n",
/* TR_NETWORK_ADDRESS_CR */
"Endere�o de rede\n",
/* TR_NETWORK_MASK_CR */
"M�scara de rede\n",
/* TR_INTERFACE (%s is interface name) */
"Interface %s",
/* TR_ENTER_THE_IP_ADDRESS_INFORMATION (%s is interface name) */
"Introduza informa��es sobre o endere�o IP da interface %s.",
/* TR_LOOKING_FOR_NIC (%s is a nic name) */
"Procurando: %s",
/* TR_FOUND_NIC (%s is a nic name) */
"Smoothwall detectou o seguinte NIC nesta m�quina: %s",
/* TR_MODULE_NAME_CANNOT_BE_BLANK */
"O nome do m�dulo n�o pode ser nulo.",
/* TR_STATIC */
"Est�tico",
/* TR_DHCP_HOSTNAME */
"Nome do servidor DHCP:",
/* TR_DHCP_HOSTNAME_CR */
"Nome do servidor DHCP\n",

/* misc.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_HOSTNAMECONF */
"Imposs�vel salvar /var/smoothwall/main/hostname.conf",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS */
"Imposs�vel salvar /etc/hosts.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_DENY */
"Imposs�vel salvar /etc/hosts.deny.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTS_ALLOW */
"Imposs�vel salvar /etc/hosts.allow.",
/* TR_UNABLE_TO_SET_HOSTNAME */
"Imposs�vel salvar nome do servidor.",

/***********/
/* INSTALL */
/***********/
/* TR_WELCOME */
"Seja bem vindo ao programa de instala��o SmootWall. Por favor " \
"visite a nossa p�gina em http://www.smoothwall.org. Selecionar " \
"Cancelar em qualquer das telas seguintes reiniciar� o computador.",

/* TR_NO_IDE_HARDDISK */
"Nenhum disco r�gido IDE encontrado.",
/* TR_SELECT_INSTALLATION_MEDIA */
"Selecione o modo de instala��o",
/* TR_SELECT_INSTALLATION_MEDIA_LONG */
"Smoothwall pode ser instalado de diversas formas. A mais simples � usar " \
"o leitor de CDROM do computador. Caso n�o seja poss�vel, pode-se tamb�m "\
"instalar atrav�s de outro computador em rede que tenha os arquivos de "\
"instala��o dispon�veis via HTTP. Neste caso ser� necess�rio o disquete "\
"com os controladores de rede.",
/* TR_NO_IDE_CDROM */
"Nenhum CDROM IDE encontrado.",
/* TR_INSERT_CDROM */
"Por favor insira o CD Smoothwall.",
/* TR_INSERT_FLOPPY */
"Por favor insira o disquete de controladores Smoothwall.",
/* TR_PREPARE_HARDDISK */
"O programa de instala��o ir� agora preparar o disco r�gido IDE %s. " \
"Primeiro ser�o criadas parti��es no disco, e depois cada parti��o ser� " \
"formatada.",
/* TR_PARTITIONING_DISK */
"Criando parti��es no disco...",
/* TR_UNABLE_TO_PARTITION */
"Imposs�vel criar parti��es no disco.",
/* TR_MAKING_SWAPSPACE */
"Criando espa�o de swap...",
/* TR_UNABLE_TO_MAKE_SWAPSPACE */
"Imposs�vel criar espa�o de swap.",
/* TR_MAKING_ROOT_FILESYSTEM */
"Criando sistema de arquivos root...",
/* TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM */
"Imposs�vel criar sistema de arquivos root.",
/* TR_MOUNTING_ROOT_FILESYSTEM */
"Montando sistema de arquivos root...",
/* TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM */
"Imposs�vel montar sistema de arquivos root.",
/* TR_MAKING_BOOT_FILESYSTEM */
"Criando sistema de arquivos boot...",
/* TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM */
"Imposs�vel criar sistema de arquivos boot.",
/* TR_MOUNTING_BOOT_FILESYSTEM */
"Montando boot...",
/* TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM */
"Imposs�vel montar sistema de arquivos boot.",
/* TR_MAKING_LOG_FILESYSTEM */
"Criando sistema de arquivos log...",
/* TR_UNABLE_TO_MAKE_LOG_FILESYSTEM */
"Imposs�vel criar sistema de arquivos log.",
/* TR_MOUNTING_LOG_FILESYSTEM */
"Montando sistema de arquivos log...",
/* TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM */
"Imposs�vel montar sistema de arquivos log.",
/* TR_MOUNTING_SWAP_PARTITION */
"Montando sistema de arquivos swap...",
/* TR_UNABLE_TO_MOUNT_SWAP_PARTITION */
"Imposs�vel montar sistema de arquivos swap.",
/* TR_NETWORK_SETUP_FAILED */
"A configura��o da rede falhou.",
/* TR_NO_TARBALL_DOWNLOADED */
"Nenhum arquivo tarball transferido.",
/* TR_INSTALLING_FILES */
"Instalando arquivos...",
/* TR_UNABLE_TO_INSTALL_FILES */
"Imposs�vel instalar arquivos.",
/* TR_UNABLE_TO_REMOVE_TEMP_FILES */
"Imposs�vel remover arquivos tempor�rios.",
/* TR_ERROR_WRITING_CONFIG */
"Erro ao salvar arquivo de configura��o.",
/* TR_INSTALLING_LILO */
"Instalando LILO...",
/* TR_UNABLE_TO_INSTALL_LILO */
"Imposs�vel instalar LILO.",
/* TR_UNABLE_TO_UNMOUNT_HARDDISK */
"Imposs�vel desmontar disco r�gido.",
/* TR_UNABLE_TO_UNMOUNT_CDROM */
"Imposs�vel desmontar CDROM/disquete.",
/* TR_UNABLE_TO_EJECT_CDROM */
"Imposs�vel ejetar CDROM.",
/* TR_CONGRATULATIONS */
"Parab�ns!",
/* TR_CONGRATULATIONS_LONG */
"Smoothwall foi instalado com sucesso. Por favor remova quaisquer disquetes " \
"ou CD-ROMs do computador. Em seguida ser� poss�vel configurar a conex�o ISDN, " \
"interfaces de rede, e senhas do sistema. Ap�s ter terminado a " \
"configura��o, dever� apontar o seu browser a http://smoothwall:81 ou " \
"https://smoothwall:445 (assumindo que smoothwall � o nome deste sistema) e " \
"configurar o modem (se necess�rio) e o acesso remoto. Lembre-se de ativar " \
"a senha para o usu�rio 'dial' caso queira permitir que outros " \
"usu�rios al�m do 'admin' controlem a conex�o.",

/* TR_PRESS_OK_TO_REBOOT */
"Pressione Ok para reiniciar.",
/* TR_ERROR */
"Erro",
/* TR_CALCULATING_MODULE_DEPENDANCIES */
"Calculando depend�ncias dos m�dulos...",
/* TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES */
"Imposs�vel calcular depend�ncias dos m�dulos.",

/* cdrom.c */
/* TR_SELECT_CDROM_TYPE */
"Selecione o tipo de CDROM",
/* TR_SELECT_CDROM_TYPE_LONG */
"Nenhum CDROM IDE foi detectado nesta m�quina. Por favor qual dos seguintes " \
"controladores deseja utilizar para que Smoothwall tenha acesso ao CDROM.",
/* TR_SUGGEST_IO (%x is an IO number) */
"(sugere %x)",
/* TR_SUGGEST_IRQ (%d is an IRQ number) */
"(sugere %d)",
/* TR_CONFIGURE_THE_CDROM */
"Configure o CDROM escolhendo o endere�o IO e/ou IRQ apropriados.",
/* TR_INVALID_IO (note extra space) */
"Os detalhes da porta IO introduzidos n�o s�o v�lidos. ",
/* TR_INVALID_IRQ */
"Os detalhes do IRQ introduzidos n�o s�o v�lidos.",

/* config.c */
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_MAIN_SETTINGS */
"Imposs�vel salvar /var/smoothwall/main/settings.",
/* TR_UNABLE_TO_WRITE_VAR_SMOOTHWALL_ETHERNET_SETTINGS */
"Imposs�vel salvar /var/smoothwall/ethernet/settings.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK */
"Imposs�vel criar liga��o simb�lica /dev/harddisk.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1 */
"Imposs�vel criar liga��o simb�lica /dev/harddisk1.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2 */
"Imposs�vel criar liga��o simb�lica /dev/harddisk2.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3 */
"Imposs�vel criar liga��o simb�lica /dev/harddisk3.",
/* TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4 */
"Imposs�vel criar liga��o simb�lica /dev/harddisk4.",

/* net.c */
/* TR_DOWNLOADING */
"Transferindo...",
/* TR_FAILED_TO_DOWNLOAD */
"A transfer�ncia falhou.",
/* TR_ENTER_URL */
"Digite o URL completo para o arquivo tar.gz Smoothwall. " \
"AVISO: DNS indispon�vel! O URL deve terminar com o arquivo 'smoothwall.tgz'.",

/* nic.c */
/* TR_CONFIGURE_NETWORKING */
"Configura��o da rede",
/* TR_CONFIGURE_NETWORKING_LONG */
"Pode agora configurar a rede, carregando primeiro o controlador correto para " \
"a interface VERDE. Pode faz�-lo usando a auto-detec��o da interface de rede " \
"ou escolhendo o controlador adequado de uma lista. Note que se possui interfaces " \
"de rede adicionais, poder� configur�-las posteriormente durante a instala��o. " \
"Note tamb�m que se possui interfaces adicionais do mesmo tipo da interface VERDE, " \
"e se cada uma necessitar de par�metros especiais, deve especific�-los todos de " \
"de forma a que todas as interfaces se tornem ativas ao configurar a interface VERDE.",

/* TR_INTERFACE_FAILED_TO_COME_UP */
"A interface falhou ao inicializar.",
/* TR_ENTER_NETWORK_DRIVER */
"A detec��o autom�tica falhou. Especifique o controlador e " \
"os par�metros opcionais para a interface de rede.",

/*********/
/* SETUP */
/*********/

/* main.c */
/* TR_HOSTNAME */
"Nome do servidor",
/* TR_NETWORKING */
"Rede",
/* TR_DHCP_SERVER_CONFIGURATION */
"Configura��o do servidor DHCP",
/* TR_ISDN_CONFIGURATION */
"Configura��o ISDN",
/* TR_ROOT_PASSWORD */
"Senha de \'root\'",
/* TR_SETUP_PASSWORD */
"Senha de \'setup\'",
/* TR_ADMIN_PASSWORD */
"Senha de admin",
/* TR_SECTION_MENU */
"Men� de se��es",
/* TR_SELECT_THE_ITEM */
"Selecione o item que deseja configurar.",
/* TR_SETUP_FINISHED */
"Configura��o completa.  Pressione Ok para reiniciar.",
/* TR_SETUP_NOT_COMPLETE */
"A configura��o inicial n�o foi terminada com sucesso. Assegure-se que esta " \
"tenha sido completada devidamente antes de tentar executar o programa setup " \
"na linha de comando.",

/* passwords.c */
/* TR_ENTER_ROOT_PASSWORD */
"Digite a senha para o usu�rio 'root'. Este � o usu�rio que " \
"tem acesso � linha de comando.",
/* TR_SETTING_ROOT_PASSWORD */
"Atualizando a senha do usu�rio 'root'...",
/* TR_PROBLEM_SETTING_ROOT_PASSWORD */
"Erro ao atualizar a senha do usu�rio 'root'.",
/* TR_ENTER_SETUP_PASSWORD */
"Digite a senha para o usu�rio 'setup'. Este � o usu�rio que " \
"tem acesso ao programa setup.",
/* TR_SETTING_SETUP_PASSWORD */
"Atualizando a senha do usu�rio 'setup'...",
/* TR_PROBLEM_SETTING_SETUP_PASSWORD */
"Erro ao atualizar a senha do usuario 'setup'.",
/* TR_ENTER_ADMIN_PASSWORD */
"Digite a senha para o usu�rio 'admin'. Este � o usu�rio que " \
"tem acesso � administra��o Smoothwall via web.",
/* TR_SETTING_ADMIN_PASSWORD */
"Atualizando a senha do usu�rio 'admin'...",
/* TR_PROBLEM_SETTING_ADMIN_PASSWORD */
"Erro ao atualizar a senha do usu�rio 'admin'.",
/* TR_PASSWORD_PROMPT */
"Senha:",
/* TR_AGAIN_PROMPT */
"Confirma��o:",
/* TR_PASSWORD_CANNOT_BE_BLANK */
"A senha n�o pode ser nula.",
/* TR_PASSWORDS_DO_NOT_MATCH */
"As senhas n�o coincidem.",

/* hostname.c */
/* TR_ENTER_HOSTNAME */
"Atribua um nome a este computador.",
/* TR_HOSTNAME_CANNOT_BE_EMPTY */
"O nome do servidor n�o pode ser nulo.",
/* TR_HOSTNAME_CANNOT_CONTAIN_SPACES */
"O nome do servidor n�o pode conter espa�os.",
/* TR_UNABLE_TO_WRITE_ETC_HOSTNAME */
"Imposs�vel gravar /etc/hostname",

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
"Adaptador ISDN",
/* TR_MSN_CONFIGURATION */
"N� de telefone local (MSN/EAZ)",
/* TR_SET_ADDITIONAL_MODULE_PARAMETERS */
"Especifique par�metros adicionais",
/* TR_RED_IN_USE */
"A linha ISDN (ou outra conex�o externa) j� est� sendo utilizada.  N�o � poss�vel " \
"configurar a linha ISDN enquanto a interface VERMELHA estiver ativa.",
/* TR_ISDN_CONFIGURATION_MENU */
"Men� de configura��o ISDN",
/* TR_ISDN_STATUS */
"A linha ISDN est� %s.\n\n" \
"   Protocolo: %s\n" \
"   Interface: %s\n" \
"   N� de telefone local: %s\n\n" \
"Selecione o item que deseja reconfigurar, ou utilize a configura��o atual.",
/* TR_ISDN_NOT_YET_CONFIGURED */
"A linha ISDN ainda n�o foi configurada. Selecione o item que deseja configurar.",
/* TR_ENABLE_ISDN */
"Ativar ISDN",
/* TR_DISABLE_ISDN */
"Desativar ISDN",
/* TR_INITIALISING_ISDN */
"Inicializando ISDN...",
/* TR_UNABLE_TO_INITIALISE_ISDN */
"Imposs�vel inicializar ISDN.",
/* TR_ISDN_NOT_SETUP */
"a linha ISDN ainda n�o foi configurada. Alguns items ainda n�o foram selecionados.",
/* TR_ISDN_PROTOCOL_SELECTION */
"Sele��o de protocolo ISDN",
/* TR_CHOOSE_THE_ISDN_PROTOCOL */
"Escolha o protocolo adequado.",
/* TR_AUTODETECT */
"* AUTO-DETEC��O *",
/* TR_ISDN_CARD_SELECTION */
"Sele��o do adaptador ISDN",
/* TR_CHOOSE_THE_ISDN_CARD_INSTALLED */
"Escolha o adaptador ISDN instalado neste computador.",
/* TR_CHECKING_FOR */
"Procurando: %s",
/* TR_ISDN_CARD_NOT_DETECTED */
"Adaptador ISDN n�o detectado. Pode ser necess�rio especificar par�metros " \
"adicionais se o tipo do adaptador for ISA ou caso tenha requerimentos especiais.",
/* TR_DETECTED */
"Detectado: %s",
/* TR_UNABLE_TO_FIND_AN_ISDN_CARD */
"Adaptador ISDN n�o detectado. Pode ser necess�rio especificar par�metros " \
"adicionais se o tipo do adaptador for ISA ou caso tenha requerimentos especiais.",
/* TR_ENTER_THE_LOCAL_MSN */
"Digite o n� de telefone local (MSN/EAZ).",
/* TR_PHONENUMBER_CANNOT_BE_EMPTY */
"O n� de telefone n�o pode ser nulo.",
/* TR_ENTER_ADDITIONAL_MODULE_PARAMS */
"Alguns adaptadores (especialmente os ISA) podem requerer par�metros adicionais " \
"para especificar o IRQ e o endere�o IO. Se possui um destes adaptadores, digite " \
"esses par�metros aqui. Por exemplo: " \
"\"io=0x280 irq=9\". Estes ser�o usados durante a detec��o.",

/* networking.c */
/* TR_PUSHING_NETWORK_DOWN */
"Desativando a rede...",
/* TR_PULLING_NETWORK_UP */
"Ativando a rede...",
/* TR_NETWORK_CONFIGURATION_TYPE */
"Tipo de configura��o da rede",
/* TR_DRIVERS_AND_CARD_ASSIGNMENTS */
"Controladores e atribui��o de adaptadores",
/* TR_ADDRESS_SETTINGS */
"Endere�os",
/* TR_DNS_AND_GATEWAY_SETTINGS */
"DNS e Gateway",
/* TR_RESTART_REQUIRED */
"\n\nAo completar a configura��o, a rede deve ser reinicializada.",
/* TR_CURRENT_CONFIG (first %s is type, second is restart message (or not) */
"Configura��o atual: %s%s",
/* TR_NETWORK_CONFIGURATION_MENU */
"Men� de configura��o da rede",
/* TR_NETWORK_CONFIGURATION_TYPE_LONG */
"Selecione a configura��o de rede para o Smoothwall. Os seguintes tipos " \
"de configura��o listam as interfaces que possuem conex�o ethernet. " \
"Se alterar esta configura��o, ser� necess�rio reinicializar a rede, e ter� " \
"de reconfigurar a atribui��o de controladores de rede.",
/* TR_PUSHING_NON_LOCAL_NETWORK_DOWN */
"Desativando a rede n�o-local...",
/* TR_YOUR_CONFIGURATION_IS_SINGLE_GREEN_ALREADY_HAS_DRIVER */
"A configura��o atual especifica uma �nica interface VERDE, " \
"a qual j� possui um controlador associado.",
/* TR_CONFIGURE_NETWORK_DRIVERS */
"Configure os controladores de rede, e as interfaces a que cada " \
"adaptador est� associado. A configura��o atual � a seguinte:\n\n",
/* TR_DO_YOU_WISH_TO_CHANGE_THESE_SETTINGS */
"\nPretende alterar estes par�metros?",
/* TR_UNCLAIMED_DRIVER */
"Existe um adaptador ethernet livre do tipo:\n%s\n\n" \
"Pode atribu�-lo a:",
/* TR_CARD_ASSIGNMENT */
"Atribui��o de adaptadores",
/* TR_PROBE */
"Auto-detec��o",
/* TR_SELECT */
"Sele��o",
/* TR_NO_UNALLOCATED_CARDS */
"N�o existem adaptadores de rede livres, " \
"mas s�o necess�rios mais adaptadores. Pode optar por auto-detectar ou " \
"por escolher um controlador da lista.",
/* TR_UNABLE_TO_FIND_ANY_ADDITIONAL_DRIVERS */
"N�o foi possivel encontrar controladores adicionais.",
/* TR_ALL_CARDS_SUCCESSFULLY_ALLOCATED */
"Todos os adaptadores foram atribuidos com sucesso.",
/* TR_NOT_ENOUGH_CARDS_WERE_ALLOCATED */
"N�o foram atribuidos adaptadores suficientes.",
/* TR_MANUAL */
"* MANUAL *",
/* TR_SELECT_NETWORK_DRIVER */
"Selecionar controlador de rede",
/* TR_SELECT_NETWORK_DRIVER_LONG */
"Selecione o controlador de rede para o adaptador instalado neste " \
"computador. Se selecionar MANUAL, ter� a oportunidade de especificar " \
"o nome do m�dulo controlador e eventuais par�metros para controladores " \
"que tenham requisitos especiais, como por exemplo adaptadores ISA.",
/* TR_UNABLE_TO_LOAD_DRIVER_MODULE */
"Imposs�vel carregar o m�dulo controlador.",
/* TR_THIS_DRIVER_MODULE_IS_ALREADY_LOADED */
"Este m�dulo controlador j� est� carregado.",
/* TR_MODULE_PARAMETERS */
"Digite o nome do m�dulo controlador e os respectivos par�metros",
/* TR_LOADING_MODULE */
"Carregando m�dulo...",
/* TR_WARNING */
"AVISO",
/* TR_WARNING_LONG */
"Se alterar este endere�o IP enquanto estiver ligado remotamente, " \
"a sua conex�o ao computador Smoothwall ser� interompida, e ter� de " \
"voltar a conectar-se atrav�s do novo endere�o IP. Trata-se de um procedimento " \
"arriscado, e s� deve ser tentado caso tenha acesso f�sico � m�quina, para " \
"o caso de algo correr mal.",
/* TR_SINGLE_GREEN */
"O sistema est� configurado para uma �nica interface VERDE.",
/* TR_SELECT_THE_INTERFACE_YOU_WISH_TO_RECONFIGURE */
"Selecione a interface que pretende reconfigurar.",
/* TR_DNS_GATEWAY_WITH_GREEN */
"A configura��o atual n�o utiliza um adaptador ethernet associado � " \
"interface VERMELHA. As informa��es relativas a DNS e gateway para " \
"usu�rios de conex�es telef�nicas ser�o configuradas automaticamente " \
"ao efetuar a conex�o.",
/* TR_PRIMARY_DNS */
"DNS prim�rio:",
/* TR_SECONDARY_DNS */
"DNS secund�rio:",
/* TR_DEFAULT_GATEWAY */
"Gateway:",
/* TR_DNS_AND_GATEWAY_SETTINGS_LONG */
"Digite as informa��es relativas a DNS e gateway. Estas informa��es ser�o " \
"usadas apenas se o DHCP estiver desligado na interface VERMELHA.",
/* TR_PRIMARY_DNS_CR */
"DNS prim�rio\n",
/* TR_SECONDARY_DNS_CR */
"DNS secund�rio\n",
/* TR_DEFAULT_GATEWAY_CR */
"Gateway\n",
/* TR_SECONDARY_WITHOUT_PRIMARY_DNS */
"DNS secund�rio especificado sem o respectivo DNS prim�rio",
/* TR_UNKNOWN */
"DESCONHECIDO",
/* TR_NO_ORANGE_INTERFACE */
"Nenhuma interface LARANJA configurada.",
/* TR_MISSING_ORANGE_IP */
"Faltam as informa��es sobre o endere�o IP da interface LARANJA.",
/* TR_NO_RED_INTERFACE */
"Nenhuma interface VERMELHA configurada.",
/* TR_MISSING_RED_IP */
"Faltam as informa��es sobre o endere�o IP da interface VERMELHA.",

/* dhcp.c */
/* TR_START_ADDRESS */
"Endere�o inicial:",
/* TR_END_ADDRESS */
"Endere�o final:",
/* TR_DEFAULT_LEASE */
"Aluguel por defeito (mins):",
/* TR_MAX_LEASE */
"Aluguel m�ximo (mins):",
/* TR_DOMAIN_NAME_SUFFIX */
"Nome do dom�nio (sufixo):",
/* TR_CONFIGURE_DHCP */
"Configure o servidor DHCP digitando a informa��o dos seus par�metros.",
/* TR_START_ADDRESS_CR */
"Endere�o inicial\n",
/* TR_END_ADDRESS_CR */
"Endere�o final\n",
/* TR_DEFAULT_LEASE_CR */
"Tempo de aluguel por defeito\n",
/* TR_MAX_LEASE_CR */
"Tempo de aluguel m�ximo\n",
/* TR_DOMAIN_NAME_SUFFIX_CR */
"Nome de dom�nio (sufixo)\n",

/* keymap.c */
/* TR_KEYBOARD_MAPPING */
"Mapas de teclado",
/* TR_KEYBOARD_MAPPING_LONG */
"Escolha o seu tipo de teclado na lista abaixo.",

/* timezone.c */
/* TR_TIMEZONE */
"Fuso hor�rio",
/* TR_TIMEZONE_LONG */
"Escolha o seu fuso hor�rio na lista abaixo.",

/* usbadsl.c */
/* TR_USB_CONTROLLER */
"Escolha o controlador USB",
/* TR_USBADSL_STATUS */
"USB ADSL est� atualmente: %s\n" \
"   Controlador: %s\n\n" \
"Selecione o item que pretende reconfigurar, ou use a configura��o actual.",
/* TR_USBADSL_CONFIGURATION */
"Configura��o USB ADSL",
/* TR_ENABLE_USBADSL */
"Ativar USB ADSL",
/* TR_DISABLE_USBADSL */
"Desativar USB ADSL",
/* TR_INITIALISING_USBADSL */
"Inicializando USB ADSL.",
/* TR_UNABLE_TO_INITIALISE_USBADSL */
"Imposs�vel inicializar USB ADSL",
/* TR_USBADSL_NOT_SETUP */
"USB ADSL n�o configurado.",
/* TR_USB_CONTROLLER_SELECTION */
"Sele��o de controlador USB",
/* TR_CHOOSE_THE_USB_CONTROLLER_INSTALLED */
"Escolha o controlador USB instalado na m�quina Smoothwall.",
/* TR_USB_CONTROLLER_NOT_DETECTED */
"Controlador USB n�o detectado.",
/* TR_UNABLE_TO_FIND_A_USB_CONTROLLER */
"N�o foi poss�vel encontrar um controlador USB..",
/* TR_STARTING_UP_USBADSL */
"Ativando USB ADSL..."

};
