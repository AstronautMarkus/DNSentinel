"""DNS records: list (+ import API), detail, create/edit form and record actions."""

STRINGS = {
    'records.proxy_status': {'en': 'Proxy status', 'es': 'Estado del proxy'},
    'records.ttl_auto': {'en': 'Auto', 'es': 'Automático'},
    'records.ttl_minutes': {
        'en': {'one': '{count} minute', 'other': '{count} minutes'},
        'es': {'one': '{count} minuto', 'other': '{count} minutos'},
    },
    'records.ttl_hours': {
        'en': {'one': '{count} hour', 'other': '{count} hours'},
        'es': {'one': '{count} hora', 'other': '{count} horas'},
    },
    'records.ttl_days': {
        'en': {'one': '{count} day', 'other': '{count} days'},
        'es': {'one': '{count} día', 'other': '{count} días'},
    },
    'records.auto_update': {'en': 'Auto-update', 'es': 'Actualización automática'},
    'records.auto_update_hint': {
        'en': 'Keep this record pointed at your public IP',
        'es': 'Mantener este registro apuntando a tu IP pública',
    },
    'records.auto_update_for': {'en': 'Auto-update {name}', 'es': 'Actualización automática de {name}'},
    'records.missing': {'en': 'Not in Cloudflare', 'es': 'No está en Cloudflare'},
    'records.missing_hint': {'en': 'This record was deleted in Cloudflare.', 'es': 'Este registro se eliminó en Cloudflare.'},

    # ── List ──
    'records.list.title': {'en': 'DNS Records', 'es': 'Registros DNS'},
    'records.list.subtitle_html': {
        'en': 'DNS record list from the <strong>{zone}</strong> zone.',
        'es': 'Lista de registros DNS de la zona <strong>{zone}</strong>.',
    },
    'records.list.back': {'en': 'Back to zone', 'es': 'Volver a la zona'},
    'records.list.import': {'en': 'Import records', 'es': 'Importar registros'},
    'records.list.add': {'en': 'Add record', 'es': 'Agregar registro'},
    'records.list.sync': {'en': 'Sync', 'es': 'Sincronizar'},
    'records.list.sync_hint': {'en': 'Refresh these records from Cloudflare', 'es': 'Actualizar estos registros desde Cloudflare'},
    'records.list.sentinel_paused': {
        'en': "The sentinel is paused, so auto-update records aren't being updated.",
        'es': 'El centinela está en pausa, así que los registros con actualización automática no se están actualizando.',
    },
    'records.list.sentinel_settings': {'en': 'Sentinel settings', 'es': 'Configuración del centinela'},
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
        'en': 'Add a record, or import the ones already in Cloudflare, to start managing them with DNSentinel.',
        'es': 'Agrega un registro, o importa los que ya están en Cloudflare, para empezar a gestionarlos con DNSentinel.',
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
    'records.detail.missing_alert': {
        'en': 'This record no longer exists in Cloudflare. Delete it here, or sync the zone if it was restored.',
        'es': 'Este registro ya no existe en Cloudflare. Elimínalo aquí, o sincroniza la zona si se restauró.',
    },
    'records.detail.not_editable': {
        'en': '{type} records are edited in the Cloudflare dashboard. Here you can view or remove them.',
        'es': 'Los registros {type} se editan en el panel de Cloudflare. Aquí puedes verlos o quitarlos.',
    },
    'records.detail.auto_update_desc': {
        'en': 'The sentinel keeps this record pointed at your public IP.',
        'es': 'El centinela mantiene este registro apuntando a tu IP pública.',
    },
    'records.detail.no_history': {
        'en': "The sentinel hasn't changed this record yet.",
        'es': 'El centinela todavía no ha cambiado este registro.',
    },

    # ── Create / edit form ──
    'records.form.new_title': {'en': 'Add record', 'es': 'Agregar registro'},
    'records.form.edit_title': {'en': 'Edit record', 'es': 'Editar registro'},
    'records.form.new_heading': {'en': 'Add DNS record', 'es': 'Agregar registro DNS'},
    'records.form.edit_heading': {'en': 'Edit DNS record', 'es': 'Editar registro DNS'},
    'records.form.subtitle_html': {
        'en': 'Changes are saved to Cloudflare for <strong>{zone}</strong> right away.',
        'es': 'Los cambios se guardan al instante en Cloudflare para <strong>{zone}</strong>.',
    },
    'records.form.card_title': {'en': 'DNS record', 'es': 'Registro DNS'},
    'records.form.type_locked': {
        'en': "The type can't be changed once the record exists.",
        'es': 'El tipo no se puede cambiar una vez creado el registro.',
    },
    'records.form.ttl_proxied': {
        'en': 'Proxied records always use Auto TTL.',
        'es': 'Los registros con proxy siempre usan TTL automático.',
    },
    'records.form.name_hint': {
        'en': 'Use @ for the root domain (the zone itself).',
        'es': 'Usa @ para el dominio raíz (la zona misma).',
    },
    'records.form.use_my_ip': {'en': 'Use my IP', 'es': 'Usar mi IP'},
    'records.form.content_auto_hint': {
        'en': 'Leave it empty to use your current public IP. The sentinel keeps it updated.',
        'es': 'Déjalo vacío para usar tu IP pública actual. El centinela lo mantiene actualizado.',
    },
    'records.form.content_a': {'en': 'IPv4 address', 'es': 'Dirección IPv4'},
    'records.form.content_aaaa': {'en': 'IPv6 address', 'es': 'Dirección IPv6'},
    'records.form.content_cname': {'en': 'Target', 'es': 'Destino'},
    'records.form.content_txt': {'en': 'Content', 'es': 'Contenido'},
    'records.form.content_mx': {'en': 'Mail server', 'es': 'Servidor de correo'},
    'records.form.content_ns': {'en': 'Nameserver', 'es': 'Servidor de nombres'},
    'records.form.priority': {'en': 'Priority', 'es': 'Prioridad'},
    'records.form.priority_hint': {
        'en': 'Lower values are tried first (0–65535).',
        'es': 'Los valores más bajos se usan primero (0–65535).',
    },
    'records.form.proxied': {'en': 'Proxied through Cloudflare', 'es': 'Con proxy de Cloudflare'},
    'records.form.proxied_hint': {
        'en': 'Cloudflare serves the traffic and hides your IP. Turn it off for SSH, games and other non-web services.',
        'es': 'Cloudflare atiende el tráfico y oculta tu IP. Desactívalo para SSH, juegos y otros servicios que no son web.',
    },
    'records.form.auto_update': {'en': 'Auto-update with my public IP', 'es': 'Actualizar automáticamente con mi IP pública'},
    'records.form.auto_update_hint': {
        'en': 'The sentinel points this record at your public IP and updates it whenever the IP changes.',
        'es': 'El centinela apunta este registro a tu IP pública y lo actualiza cada vez que la IP cambia.',
    },
    'records.form.optional': {'en': 'optional', 'es': 'opcional'},
    'records.form.save': {'en': 'Save changes', 'es': 'Guardar cambios'},
    'records.form.create': {'en': 'Create record', 'es': 'Crear registro'},
    'records.form.help_title': {'en': 'Good to know', 'es': 'Conviene saber'},
    'records.form.help_cloudflare_title': {'en': 'Saved in Cloudflare', 'es': 'Se guarda en Cloudflare'},
    'records.form.help_cloudflare': {
        'en': 'DNSentinel creates and edits the record through the Cloudflare API, so the change is live within seconds.',
        'es': 'DNSentinel crea y edita el registro con la API de Cloudflare, así que el cambio se aplica en segundos.',
    },
    'records.form.help_auto_update': {
        'en': 'For A and AAAA records. Turn it on for every name that should follow your home IP.',
        'es': 'Para registros A y AAAA. Actívalo en cada nombre que deba seguir a la IP de tu casa.',
    },
    'records.form.help_proxied': {
        'en': 'The orange cloud. Available for A, AAAA and CNAME records.',
        'es': 'La nube naranja. Disponible para registros A, AAAA y CNAME.',
    },

    # Field errors (app/services/records.py)
    'records.form.error.type': {'en': 'Choose one of the supported record types.', 'es': 'Elige uno de los tipos de registro admitidos.'},
    'records.form.error.required': {'en': 'This field is required.', 'es': 'Este campo es obligatorio.'},
    'records.form.error.name': {
        'en': 'Enter a valid name: letters, digits, hyphens and dots, or @.',
        'es': 'Ingresa un nombre válido: letras, números, guiones y puntos, o @.',
    },
    'records.form.error.no_current_ip': {
        'en': "There's no public IP available to fill in. Enter the address yourself.",
        'es': 'No hay una IP pública disponible para completar. Ingresa la dirección tú mismo.',
    },
    'records.form.error.ipv4': {
        'en': 'Enter a valid IPv4 address, like 203.0.113.10.',
        'es': 'Ingresa una dirección IPv4 válida, como 203.0.113.10.',
    },
    'records.form.error.ipv6': {
        'en': 'Enter a valid IPv6 address, like 2001:db8::10.',
        'es': 'Ingresa una dirección IPv6 válida, como 2001:db8::10.',
    },
    'records.form.error.hostname': {
        'en': 'Enter a valid hostname, like mail.example.com.',
        'es': 'Ingresa un nombre de host válido, como mail.example.com.',
    },
    'records.form.error.too_long': {'en': 'This value is too long.', 'es': 'Este valor es demasiado largo.'},
    'records.form.error.priority': {
        'en': 'Enter a number between 0 and 65535.',
        'es': 'Ingresa un número entre 0 y 65535.',
    },

    # ── Flash messages ──
    'records.flash.invalid_form': {'en': 'Check the highlighted fields.', 'es': 'Revisa los campos marcados.'},
    'records.flash.unreachable': {
        'en': "Couldn't reach Cloudflare. Check the internet connection and try again.",
        'es': 'No se pudo conectar con Cloudflare. Revisa la conexión a Internet e inténtalo de nuevo.',
    },
    'records.flash.forbidden': {
        'en': 'Cloudflare rejected the API token. It needs the Zone → DNS → Edit permission for this zone.',
        'es': 'Cloudflare rechazó el token de API. Necesita el permiso Zona → DNS → Editar para esta zona.',
    },
    'records.flash.cloudflare_error': {'en': 'Cloudflare returned an error: {error}', 'es': 'Cloudflare devolvió un error: {error}'},
    'records.flash.created': {'en': 'Record {name} created in Cloudflare.', 'es': 'Registro {name} creado en Cloudflare.'},
    'records.flash.updated': {'en': 'Record {name} updated in Cloudflare.', 'es': 'Registro {name} actualizado en Cloudflare.'},
    'records.flash.not_editable': {
        'en': '{type} records can only be edited in the Cloudflare dashboard.',
        'es': 'Los registros {type} solo se pueden editar en el panel de Cloudflare.',
    },
    'records.flash.missing_in_cloudflare': {
        'en': 'This record no longer exists in Cloudflare.',
        'es': 'Este registro ya no existe en Cloudflare.',
    },
    'records.flash.deleted': {'en': 'Record {name} deleted from Cloudflare.', 'es': 'Registro {name} eliminado de Cloudflare.'},
    'records.flash.untracked': {
        'en': 'DNSentinel stopped tracking {name}. It is still live in Cloudflare.',
        'es': 'DNSentinel dejó de seguir {name}. Sigue activo en Cloudflare.',
    },
    'records.flash.synced': {
        'en': 'Synced with Cloudflare: {refreshed} refreshed, {missing} no longer in Cloudflare, {not_imported} not imported yet.',
        'es': 'Sincronizado con Cloudflare: {refreshed} actualizados, {missing} ya no están en Cloudflare, {not_imported} sin importar.',
    },

    # ── Import API (shown in the import dialogs) ──
    'records.api.zone_not_found': {'en': 'Zone not found', 'es': 'Zona no encontrada'},
    'records.api.zone_or_token_missing': {
        'en': 'Zone not found or API token missing',
        'es': 'Zona no encontrada o falta el token de API',
    },
    'records.api.invalid_json': {'en': 'Invalid JSON', 'es': 'JSON no válido'},
    'records.api.already_imported': {'en': 'This record is already imported', 'es': 'Este registro ya está importado'},
    'records.api.auto_update_unsupported': {
        'en': 'Only A and AAAA records can be updated automatically.',
        'es': 'Solo los registros A y AAAA se pueden actualizar automáticamente.',
    },
    'records.api.auto_update_on': {
        'en': 'The sentinel now keeps {name} pointed at your IP.',
        'es': 'El centinela ahora mantiene {name} apuntando a tu IP.',
    },
    'records.api.auto_update_on_paused': {
        'en': '{name} will follow your IP once the sentinel is resumed.',
        'es': '{name} seguirá a tu IP cuando se reanude el centinela.',
    },
    'records.api.auto_update_off': {
        'en': '{name} is no longer updated automatically.',
        'es': '{name} ya no se actualiza automáticamente.',
    },
    'records.api.invalid_ids': {'en': 'Invalid record_ids', 'es': 'record_ids no válido'},
}
