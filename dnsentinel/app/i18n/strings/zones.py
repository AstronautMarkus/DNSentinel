"""Cloudflare zones: list, create (+ credential validation API) and detail."""

STRINGS = {
    # ── List ──
    'zones.list.title': {'en': 'Cloudflare DNS Zones', 'es': 'Zonas DNS de Cloudflare'},
    'zones.list.subtitle': {'en': 'Cloudflare zones connected to DNSentinel.', 'es': 'Zonas de Cloudflare conectadas a DNSentinel.'},
    'zones.list.added': {'en': 'Added zones', 'es': 'Zonas agregadas'},
    'zones.list.empty_text': {
        'en': 'Connect a Cloudflare zone with its Zone ID and an API token to start managing its DNS records.',
        'es': 'Conecta una zona de Cloudflare con su ID de zona y un token de API para empezar a gestionar sus registros DNS.',
    },

    # ── Create ──
    'zones.create.title': {'en': 'Add a Zone', 'es': 'Agregar una zona'},
    'zones.create.heading': {'en': 'Add Cloudflare DNS zone', 'es': 'Agregar zona DNS de Cloudflare'},
    'zones.create.subtitle': {
        'en': 'Fill out the form below to add a Cloudflare DNS zone in DNSentinel.',
        'es': 'Completa el formulario para agregar una zona DNS de Cloudflare a DNSentinel.',
    },
    'zones.create.credentials': {'en': 'Zone credentials', 'es': 'Credenciales de la zona'},
    'zones.create.zone_id_hint': {
        'en': "The zone identifier shown on the zone's Overview page in Cloudflare.",
        'es': 'El identificador que aparece en la página de Información general de la zona en Cloudflare.',
    },
    'zones.create.token_hint': {
        'en': 'Credentials are validated against Cloudflare before the zone is created.',
        'es': 'Las credenciales se validan con Cloudflare antes de crear la zona.',
    },
    'zones.create.validate': {'en': 'Validate credentials', 'es': 'Validar credenciales'},
    'zones.create.submit': {'en': 'Create zone', 'es': 'Crear zona'},
    'zones.create.help_title': {'en': 'Where to find these', 'es': 'Dónde encontrarlos'},
    'zones.create.help_zone_id': {
        'en': 'In the Cloudflare dashboard, open your domain. The Zone ID is in the API section of the Overview page.',
        'es': 'En el panel de Cloudflare, abre tu dominio. El ID de zona está en la sección API de la página de Información general.',
    },
    'zones.create.help_token': {
        'en': 'Go to My Profile → API Tokens and create a token for this zone with the Zone → Zone → Read '
              'and Zone → DNS → Edit permissions.',
        'es': 'Ve a Mi perfil → Tokens de API y crea un token para esta zona con los permisos Zona → Zona → Leer '
              'y Zona → DNS → Editar.',
    },
    'zones.create.help_validate_title': {'en': 'Validate, then create', 'es': 'Valida y luego crea'},
    'zones.create.help_validate': {
        'en': 'DNSentinel checks the credentials with Cloudflare before the zone can be created.',
        'es': 'DNSentinel comprueba las credenciales con Cloudflare antes de permitir crear la zona.',
    },

    # ── Detail ──
    'zones.detail.title': {'en': '{zone} · Zone Detail', 'es': '{zone} · Detalle de zona'},
    'zones.detail.subtitle': {'en': 'Cloudflare DNS zone detail.', 'es': 'Detalle de la zona DNS de Cloudflare.'},
    'zones.detail.back': {'en': 'Back to zones', 'es': 'Volver a zonas'},
    'zones.detail.info': {'en': 'Zone information', 'es': 'Información de la zona'},
    'zones.detail.paused': {'en': 'Paused', 'es': 'Pausada'},
    'zones.detail.dev_mode': {'en': 'Development mode', 'es': 'Modo de desarrollo'},
    'zones.detail.registrar': {'en': 'Registrar', 'es': 'Registrador'},
    'zones.detail.dns_host': {'en': 'DNS host', 'es': 'Host DNS'},
    'zones.detail.name_servers': {'en': 'Name servers', 'es': 'Servidores de nombres'},
    'zones.detail.cf_name_servers': {'en': 'Cloudflare name servers', 'es': 'Servidores de nombres de Cloudflare'},
    'zones.detail.original_name_servers': {'en': 'Original name servers', 'es': 'Servidores de nombres originales'},
    'zones.detail.credentials': {'en': 'Credentials', 'es': 'Credenciales'},
    'zones.detail.replace_token': {'en': 'Replace token', 'es': 'Reemplazar token'},
    'zones.detail.check': {'en': 'Test connection', 'es': 'Probar conexión'},
    'zones.detail.danger_zone': {'en': 'Remove zone', 'es': 'Quitar zona'},
    'zones.detail.delete_text': {
        'en': 'Removes the zone, its imported records and their history from DNSentinel. Nothing changes in Cloudflare.',
        'es': 'Quita la zona, sus registros importados y su historial de DNSentinel. En Cloudflare no cambia nada.',
    },
    'zones.detail.delete_title': {'en': 'Remove zone?', 'es': '¿Quitar la zona?'},
    'zones.detail.delete_confirm': {
        'en': '{zone} and all its imported records will be removed from DNSentinel. Your DNS in Cloudflare stays as it is.',
        'es': '{zone} y todos sus registros importados se quitarán de DNSentinel. Tu DNS en Cloudflare queda igual.',
    },
    'zones.detail.delete': {'en': 'Remove zone', 'es': 'Quitar zona'},

    # Cloudflare zone `status` / `type` values; unknown values fall back to the raw value.
    'zones.status.active': {'en': 'Active', 'es': 'Activa'},
    'zones.status.pending': {'en': 'Pending', 'es': 'Pendiente'},
    'zones.status.initializing': {'en': 'Initializing', 'es': 'Inicializando'},
    'zones.status.moved': {'en': 'Moved', 'es': 'Movida'},
    'zones.status.deleted': {'en': 'Deleted', 'es': 'Eliminada'},
    'zones.status.deactivated': {'en': 'Deactivated', 'es': 'Desactivada'},
    'zones.type.full': {'en': 'Full', 'es': 'Completa'},
    'zones.type.partial': {'en': 'Partial', 'es': 'Parcial'},
    'zones.type.secondary': {'en': 'Secondary', 'es': 'Secundaria'},

    # ── Flash messages (create) ──
    'zones.flash.missing_fields': {
        'en': 'Both Zone ID and API Token are required.',
        'es': 'El ID de zona y el token de API son obligatorios.',
    },
    'zones.flash.no_name': {
        'en': 'Could not retrieve zone name from Cloudflare.',
        'es': 'No se pudo obtener el nombre de la zona desde Cloudflare.',
    },
    'zones.flash.name_exists': {'en': 'A zone with that name already exists.', 'es': 'Ya existe una zona con ese nombre.'},
    'zones.flash.id_exists': {
        'en': 'You already have a zone registered with that Zone ID.',
        'es': 'Ya tienes una zona registrada con ese ID de zona.',
    },
    'zones.flash.created': {'en': 'Zone created successfully.', 'es': 'Zona creada correctamente.'},
    'zones.flash.deleted': {
        'en': 'Zone {zone} removed from DNSentinel. Nothing was changed in Cloudflare.',
        'es': 'Zona {zone} quitada de DNSentinel. No se cambió nada en Cloudflare.',
    },

    # ── Validation API (create form) ──
    'zones.connection_error': {'en': 'Connection error with Cloudflare: {error}', 'es': 'Error de conexión con Cloudflare: {error}'},
    'zones.api.missing_data': {'en': 'Missing data. Please complete all fields.', 'es': 'Faltan datos. Completa todos los campos.'},
    'zones.api.valid': {
        'en': 'Zone and token are valid! You can continue with the creation.',
        'es': '¡La zona y el token son válidos! Puedes continuar con la creación.',
    },
    'zones.api.forbidden': {
        'en': 'The token is valid, but does not have permission to access this zone. Check the permissions in Cloudflare.',
        'es': 'El token es válido, pero no tiene permiso para acceder a esta zona. Revisa los permisos en Cloudflare.',
    },
    'zones.api.not_found': {
        'en': 'The Zone ID does not exist or is not accessible with this token. Please check that the Zone ID is correct.',
        'es': 'El ID de zona no existe o no es accesible con este token. Comprueba que el ID de zona sea correcto.',
    },
    'zones.api.unauthorized': {
        'en': 'The token is invalid or expired. Generate a new token in Cloudflare.',
        'es': 'El token no es válido o expiró. Genera un token nuevo en Cloudflare.',
    },
    'zones.api.no_dns_permission': {
        'en': 'The token can read the zone but not its DNS records. Give it the Zone → DNS → Edit permission.',
        'es': 'El token puede leer la zona pero no sus registros DNS. Dale el permiso Zona → DNS → Editar.',
    },
    'zones.api.still_valid': {
        'en': 'The token still works. Zone details were refreshed from Cloudflare.',
        'es': 'El token sigue funcionando. Los datos de la zona se actualizaron desde Cloudflare.',
    },
    'zones.api.token_replaced': {
        'en': 'Token replaced. DNSentinel uses it from now on.',
        'es': 'Token reemplazado. DNSentinel lo usará a partir de ahora.',
    },
    'zones.api.unexpected': {'en': 'Unexpected error: {status}', 'es': 'Error inesperado: {status}'},
}
