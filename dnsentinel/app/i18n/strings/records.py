"""DNS records: list (+ import API) and detail."""

STRINGS = {
    'records.proxy_status': {'en': 'Proxy status', 'es': 'Estado del proxy'},
    'records.ttl_auto': {'en': 'Auto', 'es': 'Automático'},

    # ── List ──
    'records.list.title': {'en': 'DNS Records', 'es': 'Registros DNS'},
    'records.list.subtitle_html': {
        'en': 'DNS record list from the <strong>{zone}</strong> zone.',
        'es': 'Lista de registros DNS de la zona <strong>{zone}</strong>.',
    },
    'records.list.back': {'en': 'Back to zone', 'es': 'Volver a la zona'},
    'records.list.import': {'en': 'Import records', 'es': 'Importar registros'},
    'records.list.single': {'en': 'Single record', 'es': 'Registro individual'},
    'records.list.single_desc': {'en': 'Pick one record from Cloudflare', 'es': 'Elige un registro de Cloudflare'},
    'records.list.full': {'en': 'Full list', 'es': 'Lista completa'},
    'records.list.full_desc': {'en': 'Import every record in the zone', 'es': 'Importa todos los registros de la zona'},
    'records.list.imported': {'en': 'Imported records', 'es': 'Registros importados'},
    'records.list.view': {'en': 'View', 'es': 'Ver'},
    'records.list.view_record': {'en': 'View {name}', 'es': 'Ver {name}'},
    'records.list.edit': {'en': 'Edit', 'es': 'Editar'},
    'records.list.edit_record': {'en': 'Edit {name}', 'es': 'Editar {name}'},
    'records.list.delete': {'en': 'Delete', 'es': 'Eliminar'},
    'records.list.delete_record': {'en': 'Delete {name}', 'es': 'Eliminar {name}'},
    'records.list.empty_title': {'en': 'No records available', 'es': 'No hay registros disponibles'},
    'records.list.empty_text': {
        'en': 'Import records from Cloudflare to start managing them with DNSentinel.',
        'es': 'Importa registros desde Cloudflare para empezar a gestionarlos con DNSentinel.',
    },

    # ── Detail ──
    'records.detail.title': {'en': 'Record Detail', 'es': 'Detalle del registro'},
    'records.detail.not_found': {'en': 'Not found', 'es': 'No encontrado'},
    'records.detail.heading': {'en': 'DNS record detail', 'es': 'Detalle del registro DNS'},
    'records.detail.subtitle': {'en': 'DNS record detail.', 'es': 'Detalle del registro DNS.'},
    'records.detail.back': {'en': 'Back to records', 'es': 'Volver a registros'},
    'records.detail.record': {'en': 'Record', 'es': 'Registro'},
    'records.detail.proxiable': {'en': 'Proxiable', 'es': 'Admite proxy'},
    'records.detail.comment': {'en': 'Comment', 'es': 'Comentario'},
    'records.detail.no_comment': {'en': 'No comment.', 'es': 'Sin comentario.'},
    'records.detail.settings_tags': {'en': 'Settings & tags', 'es': 'Configuración y etiquetas'},
    'records.detail.settings': {'en': 'Settings', 'es': 'Configuración'},
    'records.detail.tags': {'en': 'Tags', 'es': 'Etiquetas'},
    'records.detail.identifiers': {'en': 'Identifiers', 'es': 'Identificadores'},
    'records.detail.record_id': {'en': 'Record ID', 'es': 'ID del registro'},
    'records.detail.copy_record_id': {'en': 'Copy record ID', 'es': 'Copiar ID del registro'},
    'records.detail.zone_id_fk': {'en': 'Zone ID FK', 'es': 'FK de la zona'},
    'records.detail.record_not_found': {'en': 'Record not found.', 'es': 'Registro no encontrado.'},

    # ── Import API (shown in the import dialogs) ──
    'records.api.zone_not_found': {'en': 'Zone not found', 'es': 'Zona no encontrada'},
    'records.api.zone_or_token_missing': {
        'en': 'Zone not found or API token missing',
        'es': 'Zona no encontrada o falta el token de API',
    },
    'records.api.invalid_json': {'en': 'Invalid JSON', 'es': 'JSON no válido'},
    'records.api.name_exists': {
        'en': 'A record with this name already exists in the zone',
        'es': 'Ya existe un registro con este nombre en la zona',
    },
    'records.api.invalid_ids': {'en': 'Invalid record_ids', 'es': 'record_ids no válido'},
}
