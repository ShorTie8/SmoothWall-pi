# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
#
# (c) Spanish Translation Team
# Luis Ludovico
# Bruno Maderni
# Jaime Herrera
# Juan Moncayo
# Yonathan Sabbah
# Marco van Beek
# Ra|l Martmnez Peris

%basetr = (

%basetr,

# common
'invalid input' => 'Dato incorrecto',
'save' => 'Grabar', # button
'refresh' => 'Refrescar', # button
'restore' => 'Recuperar', # button
'error messages' => 'Mensajes de error:',
'back' => 'VOLVER',
'help' => 'Ayuda',
'primary dns' => 'DNS primario:',
'secondary dns' => 'DNS secundario:',
'invalid primary dns' => 'DNS primario inv�lido .',
'invalid secondary dns' => 'DNS secundario inv�lido.',
'dhcp server' => 'Server DHCP',
'username' => 'Nombre de usuario:',
'password' => 'Contrase�a:',
'enabled' => 'Activo:',
'this field may be blank' => 'Este campo puede quedar vacio.',
'these fields may be blank' => 'Estos campos pueden quedar vacios.',

# header.pl
'sshome' => 'home',
'ssstatus' => 'estado',
'sstraffic graphs' => 'gr�fica de tr�fico',
'ssppp settings' => 'configuraci�n ppp',
'ssmodem' => 'modem',
'ssusb adsl firmware upload' => 'actualizaci�n de fimrware usb adsl',
'ssssh' => 'ssh',
'sspasswords' => 'contrase�as',
'ssweb proxy' => 'proxy de web',
'ssdhcp' => 'dhcp',
'ssport forwarding' => 'reenvio de puertos',
'ssexternal service access' => 'acceso externo a los servicios',
'ssdmz pinholes' => 'dmz pinholes',
'ssdynamic dns' => 'dns dinamico',
'ssids' => 'sistema de detecci�n de intrusos',
'sscontrol' => 'control',
'ssconnections' => 'conecciones',
'ssother' => 'otros',
'ssfirewall' => 'cortafuegos',
'ssshutdown' => 'apagar',
'ssshell' => 'shell',
'ssupdates' => 'actualizaciones',
'sshelp' => 'ayuda',
'sscredits' => 'creditos',
'ssip info' => 'Informci�n IP',
'powered by' => 'powered by',
'alt home' => 'Home', # alt
'alt information' => 'Informaci�n', # alt
'alt dialup' => 'Discado', # alt
'alt remote access' => 'Acceso remoto', # alt
'alt services' => 'Servicios', # alt
'alt ids' => 'Sistema de detecci�n de intrusos', # alt
'alt vpn' => 'Redes privadas virtuales', # alt
'alt logs' => 'Registros', #alt 
'alt shutdown' => 'Apagar', # alt
'alt shell' => 'Shell', # alt
'alt updates' => 'Actualizaciones', # alt

# changepw.cgi
'admin user password has been changed' => 'La contrase�a del usuario admin ha sido cambiada.',
'dial user password has been changed' => 'La contrase�a del usuario user ha sido cambiada.',
'password cant be blank' => 'La contrase�a no puede dejarse vacia.',
'passwords do not match' => 'La contrase�as ingresadas no conciden.',
'change passwords' => 'Cambiar las contrase�as',
'administrator user password' => 'Contrase�a del usuario Admin:',
'dial user password' => 'Contrase�a del usuario Dial:',
'again' => 'Nuevamente:',
'passwords must be at least 6 characters in length' => 'las contrase�as deben tener al menos 6 caracteres', 
'password contains illegal characters' => 'La contrase�a contiene caracteres ilegales.',

# credits.cgi
'credits' => 'Cr�ditos',
'version' => 'Versi�n: ',
'sponsors' => 'Patrocinadores',
'links' => 'Enlaces',
'smoothwall homepage' => 'P�gina de Smoothwall',
'translation teams' => 'equipos de la traducci�n',

# dhcp.cgi
'invalid start address' => 'Direcci�n inicial no v�lida.',
'invalid end address' => 'Direcci�n final no v�lida.',
'cannot specify secondary dns without specifying primary' => 'No se puede especificar un DNS secundario sin especificar el primario.',
'invalid default lease time' => 'Tiempo de asignaci�n por defecto no v�lido.',
'invalid max lease time' => 'Tiempo m�x de asignaci�n no v�lido.',
'dhcp server enabled' => 'Servidor DHCP habilitado.  Reiniciando.',
'dhcp server disabled' => 'Servidor DHCP deshabilitado.  Detenido.',
'dhcp configuration' => 'Configuraci�n DHCP',
'start address' => 'Direcci�n inicial:',
'end address' => 'Direcci�n final:',
'default lease time' => 'Tiempo de asignaci�n por defecto (mins):',
'max lease time' => 'M�x tiempo de asignaci�n (mins):',
'domain name suffix' => 'Sufijo del nombre de dominio:',

# proxy.cgi
'web proxy configuration' => 'Configuraci�n del Web proxy',
'web proxyc' => 'Web proxy:',
'cache size' => 'Tama�o de Cach�(MB):',
'invalid cache size' => 'Tama�o del cach� no valido.',
'remote proxy' => 'Proxy remoto:',
'invalid maximum object size' => 'Tama�o m�ximo de objeto no v�lido.',
'invalid minimum object size' => 'Tama�o m�nimo de objeto no v�lido.',
'invalid maximum outgoing size' => 'Tama�o m�ximo de salida no v�lido.',
'invalid maximum incoming size' => 'Tama�o m�ximo de entrada no v�lido.',
'transparent' => 'Transparente:',
'max size' => 'Tama�o m�ximo de objeto (KB):',
'min size' => 'Tama�o m�nimo de objeto (KB):',
'max outgoing size' => 'Tama�o m�ximo de salida (KB):',
'max incoming size' => 'Tama�o m�ximo de entrada (KB):',

# common to logs cgis
'january' => 'Enero',
'february' => 'Febrero',
'march' => 'Marzo',
'april' => 'Abril',
'may' => 'Mayo',
'june' => 'Junio',
'july' => 'Julio',
'august' => 'Agosto',
'september' => 'Septiembre',
'october' => 'Octubre',
'november' => 'Noviembre',
'december' => 'Diciembre',
'month' => 'Mes:',
'day' => 'D�a:',
'update' => 'Actualizar', # button
'export' => 'Exportar', # button
'older' => 'Anterior',
'newer' => 'Siguiente',
'settingsc' => 'Configuraciones:',

# logs.cgi/firewalllog.dat
'firewall log' => 'Registro del firewall',
'firewall log2' => 'Registro del firewall:',
'date' => 'D�a:',
'time' => 'Hora',
'action' => 'Acci�n',
'chain' => 'Cadena',
'iface' => 'Interfaz',
'protocol' => 'Protocolo',
'source' => 'Fuente',
'src port' => 'Puerto origen',
'destination' => 'Destino',
'dst port' => 'Puerto Destino',
'unknown' => 'DESCONOCIDO',
'lookup' => 'Consulta',

# logs.cgi/log.dat
'log viewer' => 'Visor de registros',
'section' => 'Secci�n:',
'kernel' => 'Kernel',
'loginlogout' => 'Apertura/cierre de sesiones',
'update transcript' => 'Actualizar transcripciones',
'log' => 'Registro:',

# logs.cgi/proxylog.dat
'proxy log viewer' => 'Visualizaci�n del registro del Proxy',
'bad ignore filter' => 'Ignorar filtro err�neo:',
'caps all' => 'TODO',
'ignore filterc' => 'Ignorar filtro:',
'enable ignore filterc' => 'Activar ignorar filtro:',
'source ip' => 'Origen IP',
'website' => 'Sitio World Wide Web',

# logs.cgi/ids.dat
'ids log viewer' => 'Visor del registro IDS',
'datec' => 'Fecha:',
'namec' => 'Nombre:',
'priorityc' => 'Prioridad:',
'typec' => 'Tipo:',
'ipinfoc' => 'Informaci�n de IP:',
'referencesc' => 'Referencias:',
'none found' => 'no se encuentran datos',

# index.cgi
'main page' => 'P�gina principal',
'dial' => 'Marcar', # button
'hangup' => 'Colgar', # button
'current profile' => 'Perfil actual:',
'connected' => 'Conectado',
'dialing' => 'Marcando...',
'modem idle' => 'M�dem inactivo',
'isdn idle' => 'RDSI inactiva',
'profile has errors' => 'El perfil tiene errores',
'modem settings have errors' => 'La configuraci�n del m�odem tiene errores',
'user pages' => 'P�ginas del usuario',
'mstatus information' => 'Informaci�n&nbsp;de&nbsp;situaci�n',
'mnetwork traffic graphs' => 'Gr�ficas&nbsp;de&nbsp;tr�fico&nbsp;en&nbsp;la&nbsp;red',
'administrator pages' => 'P�ginas del administrador',
'mppp setup' => 'Configuraci�n&nbsp;de&nbsp;PPP&nbsp;(Protocolo de Punto a Punto)',
'mmodem configuration' => 'Configuraci�n del m�dem',
'mchange passwords' => 'Cambio de contrase�as',
'mremote access' => 'Acceso remoto',
'mdhcp configuration' => 'Configuraci�n&nbsp;de&nbsp;DHCP',
'mproxy configuration' => 'Configuraci�n&nbsp;del&nbsp;proxy',
'mport forwarding configuration' => 'Configuraci�n del puerto de reenv�o',
'mshutdown control' => 'Control de apagado',
'mlog viewer' => 'Visor de registros',
'mfirewall log viewer' => 'Visor de registros del cortafuegos',
'msecure shell' => 'Consola de mandatos Segura (SSH - Secure Shell)',
'modem dod waiting' => 'M�dem a la espera para marcar bajo demanda',
'isdn dod waiting' => 'RDSI a la espera para marcar bajo demanda',
'pppoe idle' => 'PPPOE inactiva',
'usbadsl idle' => 'Conexi�n ADSL por USB inactiva',
'pppoe dod waiting' => 'PPPOE a la espera para marcar bajo demanda',
'there are updates' => 'Hay actualizaciones disponibles para su sistema. Por favor, visite la secci�n "Actualizaciones" para m�s informaci�n.',
'updates is old1' => 'Su archivo de actualizaci�n ',
'updates is old2' => 'd�as desfasado. Le recomendamos actualice su sistema visitando la p�ginas "Actualizaciones".',

# pppsetup.cgi
'unable to alter profiles while red is active' => 'Inahbilitado de modificar el perfil mientras la interfaz RED este activa.', 
'profile name not given' => 'No se ha dado nombre al perfil.',
'telephone not set' => 'Tel�fono no configurado.',
'bad characters in the telephone number field' => 'Car�cteres err�neos en el campo del n�mero de tel�fono',
'username not set' => 'Usuario no establecido.',
'spaces not allowed in the username field' => 'No se permiten espacios para el nombre de usuario.',
'password not set' => 'Contrase�a no establecida.',
'spaces not allowed in the password field' => 'No se permiten espacios para la contrase�a de usuario.',
'idle timeout not set' => 'Tiempo m�ximo de inactividad no establecido.',
'only digits allowed in the idle timeout' => 'S�lo se permiten n�meros en el campo del tiempo m�ximo de inactividad.',
'bad characters in script field' => 'Caracteres no v�lidos en el campo del gui�n',
'max retries not set' => 'N�mero m�ximo de reintentos no establecido.',
'only digits allowed in max retries field' => 'S�lo se permiten n�meros en el campo del m�ximo n�mero de reintentos.',
'profile saved' => 'Perfil guardado: ',
'select' => 'Seleccionar', # button
'profile made current' => 'Perfil seleccionado actualmente: ',
'the selected profile is empty' => 'El perfil seleccionado est� vac�o.',
'delete' => 'Borrar', # button
'profile deleted' => 'Perfil borrado: ',
'empty' => 'Vac�o',
'unnamed' => 'An�nimo',
'ppp setup' => 'Configuraci�n de PPP',
'profiles' => 'Perfiles:',
'profile name' => 'Nombre del perfil:',
'telephony' => 'Tel�fono:',
'interface' => 'Interfaz:',
'modem on com1' => 'M�dem en COM1',
'modem on com2' => 'M�dem en COM2',
'modem on com3' => 'M�dem en COM3',
'modem on com4' => 'M�dem en COM4',
'isdn tty' => 'RDSI (ISDN) a TTY',
'isdn1' => 'RDSI (ISDN) sencillo',
'isdn2' => 'RDSI (ISDN) dual',
'computer to modem rate' => 'Velocidad del puerto del ordenador al m�dem:',
'number' => 'N�mero:',
'modem speaker on' => 'Altavoz del m�dem encendido:',
'dialing mode' => 'Modo de marcado:',
'tone' => 'Tono',
'pulse' => 'Pulso',
'maximum retries' => 'N�mero m�ximo de reintentos:',
'idle timeout' => 'Tiempo m�ximo de inactividad (en minutos; 0 para deshabilitar):',
'persistent connection' => 'Conexi�n constante (vuelve a conectar en caso de desconexi�n):',
'authentication' => 'Autentificaci�n:',
'method' => 'M�todo:',
'pap or chap' => 'PAP o CHAP',
'standard login script' => 'Gui�n de conexi�n',
'demon login script' => 'Gui�n demonio de conexi�n ',
'other login script' => 'Otro gui�n de conexi�n',
'script name' => 'Nombre del gui�n:',
'type' => 'Tipo:',
'manual' => 'Manual',
'automatic' => 'Autom�tico',
'dod' => 'Marcado bajo demanda:',
'dod for dns' => 'Marcado bajo demanda para DNS:',
'connect on smoothwall restart' => 'Conectar al reiniciar Smoothwall:',
'pppoe settings' => 'Configuraci�n adicional de PPPoE:',
'usb adsl settings' => 'Configuraci�n adicional USB ADSL:',
'service name' => 'Nombre del servicio:',
'concentrator name' => 'Nombre del concentrador:',
'vpi number' => 'N�mero de VPI:',
'vci number' => 'N�mero de VCI:',
'firmwarec' => 'Microc�digo del dispositivo:',
'firmware present' => 'Microc�digo del dispositivo disponible',
'firmware not present' => 'Microc�digo del dispositivo <B>NO</B> disponible',
'upload usb adsl firmware' => 'Cargar microc�digo de USB ADSL',
'dial on demand for this interface is not supported' => 'Discado bajo demanda no esta soportado para esta interfaz.',
'no usb adsl firmware' => 'No hay firmware usb adsl',

# remote.cgi
'ssh is enabled' => 'SSH activo. Reiniciando',
'ssh is disabled' => 'SSH inactivo. Desconectando',
'remote access' => 'Acceso remoto',
'remote access2' => 'Acceso remoto:',

# shutdown.cgi
'shutting down smoothwall' => 'Apagando Smoothwall',
'shutdown control' => 'Funciones de apagado',
'shutdown' => 'Apagar', # button
'shutdown2' => 'Apagar:',
'shutting down' => 'Apagando',
'smoothwall has now shutdown' => 'Smoothwall se ha apagado correctamente',
'rebooting smoothwall' => 'Reiniciando Smoothwall', 
'reboot' => 'Reinciar', # button 
'rebooting' => 'Reiniciando', 
'smoothwall has now rebooted' => 'Smoothwall esta siendo reinciado ahora.', 

# status.cgi
'web server' => 'Servidor de Web',
'cron server' => 'Servidor de CRON',
'dns proxy server' => 'Servidor de DNS proxy',
'logging server' => 'Servidor de registro',
'kernel logging server' => 'Servidor de registro del N�cleo (SSH)',
'secure shell server' => 'Consola segura del servidor',
'vpn' => 'VPN',
'web proxy' => 'Web proxy',
'intrusion detection system' => 'Sistema de detecci�n de intrusos',
'status information' => 'Informe de situaci�n',
'services' => 'Servicios:',
'memory' => 'Memoria:',
'uptime and users' => 'Tiempo en marcha de las operaciones y usuarios:',
'interfaces' => 'Interfaces:',
'disk usage' => 'Cantidad de disco usado:',
'loaded modules' => 'M�dulos cargados:',
'kernel version' => 'Versi�n del N�cleo:',
'stopped' => 'PARADO',
'running' => 'EN MARCHA',
'swapped' => 'INTERCAMBIADO',

# portfw.cgi and dmzhole.cgi and xtaccess.cgi
'source port numbers' => 'Puerto de origen debe ser un n�mero.',
'source is bad' => 'Direcci�n IP o de red invalida.',
'destination ip bad' => 'Direcci�n IP de destino invalida',
'destination port numbers' => 'Puerto de destino debe ser un n�mero.',
'unable to open file' => 'Incapaz de abrir el archivo',
'source port in use' => 'Puerto de destino en uso:',
'forwarding rule added' => 'Regla de reenvio agregada; reiniciando reenvio',
'forwarding rule removed' => 'Regla de reenvio eliminada; reiniciando reenvio',
'external access rule added' => 'Regla de acceso externa agregada; reiniciando control de acceso',
'external access rule removed' =>' Regla de acceso externa eliminada; reiniciando control de acceso',
'dmz pinhole rule added' => 'Regla DMZ pinhole agregada; reiniciando DMZ pinhole',
'dmz pinhole rule removed' => 'Regla DMZ pinhole eliminada; reiniciando DMZ pinhole',
'port forwarding configuration' => 'Configuraci�n de reenvio de puertos',
'dmz pinhole configuration' => 'Configuraci�n DMZ pinhole',
'external access configuration' => 'Configuraci�n de acceso externo',
'add a new rule' => 'Agregar un nueva regla:',
'sourcec' => 'IP de origen, o red (vacio para "TODAS"):',
'source ipc' => 'IP de origen:',
'source portc' => 'Puerto de origen:',
'destination ipc' => 'IP de destino:',
'destination portc' => 'Puerto de destino:',
'current rules' => 'Reglas actuales:',
'source ip' => 'IP de origen',
'source port' => 'Puerto de origen',
'destination ip' => 'IP de destino',
'destination port' => 'Puerto de destino',
'add' => 'Agregar', # button
'remove' => 'Eliminar', # button
'edit' => 'Editart', # button
'enabledtitle' => 'Activo',
'nothing selected' => 'Nada seleccionado',
'you can only select one item to edit' => 'Debe seleccionar solo un item para editar',
'mark' => 'Seleccionar',
'all' => 'TODOS',

# ddns.cgi
'dynamic dns' => 'DNS din�mico',
'add a host' => 'Agregar un ordenador:',
'servicec' => 'Servicio:',
'behind a proxy' => 'Detras de un proxy:',
'enable wildcards' => 'Activar comodines:',
'hostnamec' => 'Nombre de Ordenador:',
'domainc' => 'Dominio:',
'current hosts' => 'Ordenadores actuales:',
'service' => 'Servicioe',
'hostname' => 'Nombre de ordenador',
'domain' => 'Dominio',
'proxy' => 'Proxy',
'wildcards' => 'Comodines',
'hostname not set' => 'Nombre de ordenador no configurado.',
'domain not set' => 'Dominio no configurado.',
'invalid hostname' => 'Nombre de ordenador inv�lido.',
'invalid domain name' => 'Nombre de dominio inv�lido.',
'hostname and domain already in use' => 'Nombre de ordenador y dominio ya se encuentran en uso.',
'ddns hostname added' => 'Nombre de ordenador agregado al DNS din�mico',
'ddns hostname removed' => 'Nombre de ordenador eliminado del DNS din�mico',
'force update' => 'Forzar actualizaci�n',

# ipinfo.cgi
'ip info' => 'Informaci�n de direcci�n IP',
'lookup failed' => 'Fallo la busqueda invertida',

# shell.cgi
'secure shellc' => 'Shell seguro:',

# modem.cgi
'restore defaults' => 'Valores predeterminados', # button
'timeout must be a number' => 'Timeout debe ser un n�mero.',
'modem configuration' => 'Configuraci�n del Modem',
'modem configurationc' => 'Configuraci�n del Modem:',
'init string' => 'Inicializaci�n:',
'hangup string' => 'Cortar:',
'speaker on' => 'Activar parlante:',
'speaker off' => 'Descativar parlante:',
'tone dial' => 'Discado por tono:',
'pulse dial' => 'Discado por pulso:',
'connect timeout' => 'Tiempo para establecer conexi�n:',
'send cr' => 'ISP requiere Retorno de Carro:',

# vpnmain.cgi
'restart' => 'Reiniciar',
'stop' => 'Detener',
'vpn configuration main' => 'Configuraci�n de VPN - Principal',
'main' => 'Principal',
'connections' => 'Connecciones',
'global settingsc' => 'Configuraci�n general:',
'local vpn ip' => 'IP local de VPN:',
'if blank the currently configured ethernet red address will be used' => 'Si es vacio, se utilizara la configuraci�n actual de la Zona Ethernet RED.',
'manual control and status' => 'Control manual y estado:',
'connection name' => 'Nombre',
'connection status' => 'Estado',
'capsclosed' => 'CERRADO',
'capsdisabled' => 'INACTIVO',
'capsopen' => 'ABIERTO',

# vpn.cgi/vpnconfig.dat
'name must only contain characters' => 'El nombre debe contener s�lo caracteres.',
'left ip is invalid' => 'IP izquierdo inv�lido.',
'left next hop ip is invalid' => 'El pr�ximo salto de la izquierda tiene IP inv�lido.',
'left subnet is invalid' => 'La subred izquierda es inv�lida.',
'right ip is invalid' => 'El IP derecho es inv�lido.',
'right next hop ip is invalid' => 'El pr�ximo salto de la derecha tiene IP inv�lido.',
'right subnet is invalid' => 'La subred derecha es inv�lida.',
'vpn configuration connections' => 'Configuraci�n de VPN - Conexiones',
'add a new connection' => 'Agregar una nueva conexi�n:',
'namec' => 'Nombre:',
'leftc' => 'Izquierda:',
'left next hopc' => 'Pr�ximo salto de la izquierda:',
'left subnetc' => 'Subred izquierda:',
'rightc' => 'Derecha:',
'right next hopc' => 'Pr�ximo salto de la derecha:',
'right subnetc' => 'Subred derecha:',
'secretc' => 'Secreto:',
'current connections' => 'Conexiones actuales:',
'markc' => 'Marca:',
'import and export' => 'Importar y Exportar:',
'import' => 'Importar', # button

# graphs.cgi
'network traffic graphs' => 'Gr�ficos de tr�fico en la red',
'network traffic graphsc' => 'Gr�ficos de tr�fico en la red:',
'no graphs available' => 'No hay gr�ficos disponibles.',
'no information available' => 'No hay informaci�n disponible.',

# usbadsl.cgi
'usb adsl setup' => 'Configuraci�n de ADSL por USB',
'usb adsl help' => 'Para utilizar el m�dem USB debe debe cargar el firmware en su computador Smoothwall. Por favor descargue el tarball desde Alcatel y despu�s cargue el archivo <B>mgmt.o</B> usando el formulario de abajo.',
'upload' => 'Cargar', # button
'upload successfull' => 'Carga exitosa.',
'could not create file' => 'No se pudo crear el archivo.',
'mgmt upload' => 'Cargar controlador para ADSL por USB:',
'upload filec' => 'Cargar archivo:',

# updates.cgi
'updates' => 'Actualizaciones',
'could not open available updates file' => 'No se pudo abrir el archivo de actualizaciones disponibles.',
'could not download the available updates list' => 'No se pudo descargar la lista de actulizaciones disponibles.',
'could not create directory' => 'No se pudo crear directorio.',
'could not open updatefile for writing' => 'No se pudo abrir para escritura el archivo de actualizaci�n.',
'this is not an authorised update' => 'Esta no es una actualizaci�n autorizada, o su lista de parches es antigua.',
'this is not a valid archive' => 'Este no el un archivo v�lido.',
'could not open update information file' => 'No se pudo abrir el archivo de informaci�n para actualizaci�n. La actualizaci�n esta corrupta.',
'this update is already installed' => 'Esta actualizaci�n ya se encuentra instalada.',
'package failed to install' => 'Fall&oacute la instalaci&oacuten del paquete.',
'update installed but' => 'Actualilizaci�n instalada pero la base de datos de paquetes instalados no pudo ser actualizada',
'refresh update list' => 'Refrescar lista de actualizaciones', # button
'installed updates' => 'Actualizaciones instaladas:',
'id' => 'ID',
'title' => 'T�tulo',
'description' => 'Descripci�n',
'released' => 'Liberado',
'installed' => 'Instalado',
'could not open installed updates file' => 'No pudo ser abierto el archivo de actualizaciones',
'available updates' => 'Actualizaciones disponibles:',
'there are updates available' => 'Hay actualizaciones para su sistema. Es muy importante que las instale tan pronto como le sea posible.',
'info' => 'Informaci�n',
'all updates installed' => 'Todas las actualizaciones instaladas',
'install new update' => 'Instalar actualizaci�n:',
'to install an update' => 'Para instalar una actualizaci�n por favor cargue abajo el archivo .tar.gz:',
'upload update file' => 'Cargar archivo de actualizaci�n:',
'could not download latest patch list' => 'No se pudo descargar la �ltima lista de parches (no conectado).',
'could not connect to smoothwall org' => 'No se pudo conectar con smoothwall.org',
'successfully refreshed updates list' => 'La lista de actualizaciones fue actualizada exitosamente.',
'the following update was successfully installedc' => 'La siguiente actualizaci�n fue instalada exitosamente:',

# ids.cgi
'snort is enabled' => 'SNORT est� habilitado',
'snort is disabled' => 'SNORT est� deshabilitado',
'intrusion detection system2' => 'Sistema de Detecci�n de Intrusiones:',

);
