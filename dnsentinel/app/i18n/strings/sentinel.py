"""IP sentinel: overview page, settings, and the reasons it logs for failed updates."""

STRINGS = {
    'sentinel.title': {'en': 'IP sentinel', 'es': 'Centinela de IP'},
    'sentinel.subtitle': {
        'en': 'Keeps your auto-update records pointed at your public IP, checking them on a schedule.',
        'es': 'Mantiene tus registros con actualización automática apuntando a tu IP pública, revisándolos periódicamente.',
    },
    'sentinel.status.active': {'en': 'Active', 'es': 'Activo'},
    'sentinel.status.paused': {'en': 'Paused', 'es': 'En pausa'},
    'sentinel.status.attention': {'en': 'Needs attention', 'es': 'Requiere atención'},
    'sentinel.check_now': {'en': 'Check now', 'es': 'Comprobar ahora'},
    'sentinel.check_now_disabled': {
        'en': 'Turn on auto-update on a record first',
        'es': 'Primero activa la actualización automática en algún registro',
    },
    'sentinel.offline_title': {'en': "The sentinel process isn't running", 'es': 'El proceso del centinela no está en ejecución'},
    'sentinel.offline_text_html': {
        'en': 'Records are only updated while it runs. It starts with the web app (<code>python main.py</code>), '
              'or on its own with <code>python sentinel.py</code>.',
        'es': 'Los registros solo se actualizan mientras se ejecuta. Arranca junto con la web (<code>python main.py</code>) '
              'o por separado con <code>python sentinel.py</code>.',
    },
    'sentinel.last_error': {'en': 'The last check had problems', 'es': 'La última comprobación tuvo problemas'},

    # ── Stats ──
    'sentinel.stat.process': {'en': 'Process', 'es': 'Proceso'},
    'sentinel.stat.online': {'en': 'Running', 'es': 'En ejecución'},
    'sentinel.stat.offline': {'en': 'Stopped', 'es': 'Detenido'},
    'sentinel.stat.heartbeat': {'en': 'Last seen', 'es': 'Visto por última vez'},
    'sentinel.stat.never_seen': {'en': 'Never started', 'es': 'Nunca se inició'},
    'sentinel.stat.last_check': {'en': 'Last check', 'es': 'Última comprobación'},
    'sentinel.stat.summary': {'en': '{updated} updated · {failed} failed', 'es': '{updated} actualizados · {failed} con error'},
    'sentinel.stat.not_run': {'en': 'Not run yet', 'es': 'Aún no se ha ejecutado'},
    'sentinel.stat.next_check': {'en': 'Next check', 'es': 'Próxima comprobación'},
    'sentinel.stat.soon': {'en': 'Within a minute', 'es': 'En menos de un minuto'},
    'sentinel.stat.watched': {'en': 'Watched records', 'es': 'Registros vigilados'},
    'sentinel.stat.watched_meta': {'en': 'A and AAAA with auto-update', 'es': 'A y AAAA con actualización automática'},

    # ── Target IPs ──
    'sentinel.target_ips': {'en': 'Target IP addresses', 'es': 'Direcciones IP de destino'},
    'sentinel.target_for': {'en': '{family} for {type} records', 'es': '{family} para registros {type}'},
    'sentinel.no_address': {'en': 'Not available', 'es': 'No disponible'},
    'sentinel.source_manual': {'en': 'Set manually', 'es': 'Fijada manualmente'},
    'sentinel.source_detected': {'en': 'Detected via {source}', 'es': 'Detectada con {source}'},
    'sentinel.source_none': {'en': 'No public {family} detected', 'es': 'No se detectó una {family} pública'},
    'sentinel.copy_ip': {'en': 'Copy {family}', 'es': 'Copiar {family}'},

    # ── Settings ──
    'sentinel.settings.title': {'en': 'Settings', 'es': 'Configuración'},
    'sentinel.settings.enabled': {'en': 'Sentinel enabled', 'es': 'Centinela activado'},
    'sentinel.settings.enabled_hint': {
        'en': 'When off, records keep whatever IP they have now.',
        'es': 'Si está desactivado, los registros conservan la IP que tengan ahora.',
    },
    'sentinel.settings.interval': {'en': 'Frequency', 'es': 'Frecuencia'},
    'sentinel.settings.every': {
        'en': {'one': 'Every minute', 'other': 'Every {count} minutes'},
        'es': {'one': 'Cada minuto', 'other': 'Cada {count} minutos'},
    },
    'sentinel.settings.ip_source': {'en': 'IP address to use', 'es': 'Dirección IP a usar'},
    'sentinel.settings.auto': {'en': "My ISP's public IP", 'es': 'La IP pública de mi ISP'},
    'sentinel.settings.auto_desc': {
        'en': 'Detected online on every check, so records follow your IP when the ISP changes it.',
        'es': 'Se detecta en línea en cada comprobación, así los registros siguen a tu IP cuando el ISP la cambia.',
    },
    'sentinel.settings.manual': {'en': 'A fixed IP', 'es': 'Una IP fija'},
    'sentinel.settings.manual_desc': {
        'en': 'Records always point at the addresses you enter below.',
        'es': 'Los registros siempre apuntan a las direcciones que indiques abajo.',
    },
    'sentinel.settings.detected_now': {'en': 'Detected right now:', 'es': 'Detectada ahora:'},
    'sentinel.settings.detect_again': {'en': 'Detect again', 'es': 'Detectar de nuevo'},
    'sentinel.settings.manual_ip': {'en': '{family} address', 'es': 'Dirección {family}'},
    'sentinel.settings.use_detected': {'en': 'Use detected', 'es': 'Usar la detectada'},
    'sentinel.settings.manual_hint': {
        'en': 'Public addresses only. Leave one empty to skip that family: no IPv6 means AAAA records are left alone.',
        'es': 'Solo direcciones públicas. Deja una vacía para omitir esa familia: sin IPv6, los registros AAAA no se tocan.',
    },
    'sentinel.settings.save': {'en': 'Save settings', 'es': 'Guardar configuración'},
    'sentinel.settings.error.interval': {
        'en': 'Choose one of the listed frequencies.',
        'es': 'Elige una de las frecuencias de la lista.',
    },

    # Reasons an IP is rejected (app/services/ip.py InvalidIP.reason).
    'sentinel.ip_error.invalid': {'en': 'This is not a valid IP address.', 'es': 'Esta no es una dirección IP válida.'},
    'sentinel.ip_error.wrong_family': {
        'en': 'This address belongs to the other IP family.',
        'es': 'Esta dirección pertenece a la otra familia de IP.',
    },
    'sentinel.ip_error.not_public': {
        'en': 'This is a private or reserved address (LAN, CG-NAT…). Use the public IP your ISP gives you.',
        'es': 'Es una dirección privada o reservada (LAN, CG-NAT…). Usa la IP pública que te asigna tu ISP.',
    },
    'sentinel.ip_error.required': {'en': 'Enter at least one IP address.', 'es': 'Ingresa al menos una dirección IP.'},

    'sentinel.flash.saved': {
        'en': 'Sentinel settings saved. They apply on the next check.',
        'es': 'Configuración del centinela guardada. Se aplica en la próxima comprobación.',
    },
    'sentinel.flash.invalid': {'en': 'Check the highlighted fields.', 'es': 'Revisa los campos marcados.'},

    # ── Help ──
    'sentinel.help.title': {'en': 'How it works', 'es': 'Cómo funciona'},
    'sentinel.help.watch_title': {'en': 'Pick the records', 'es': 'Elige los registros'},
    'sentinel.help.watch': {
        'en': 'Turn on auto-update on the A and AAAA records that should follow your IP.',
        'es': 'Activa la actualización automática en los registros A y AAAA que deben seguir a tu IP.',
    },
    'sentinel.help.source_title': {'en': 'Choose the IP', 'es': 'Elige la IP'},
    'sentinel.help.source': {
        'en': 'Use the public IP your ISP assigns, detected automatically, or a fixed one.',
        'es': 'Usa la IP pública que asigna tu ISP, detectada automáticamente, o una fija.',
    },
    'sentinel.help.loop_title': {'en': 'It keeps watch', 'es': 'Se queda vigilando'},
    'sentinel.help.loop': {
        'en': 'On every check it compares each record in Cloudflare with your IP and updates the ones that differ, '
              'including records edited by hand in Cloudflare.',
        'es': 'En cada comprobación compara cada registro en Cloudflare con tu IP y actualiza los que no coinciden, '
              'incluso los que se editaron a mano en Cloudflare.',
    },
    'sentinel.help.service_title': {'en': 'Run it as a service', 'es': 'Ejecútalo como servicio'},
    'sentinel.help.service_html': {
        'en': 'To keep it running without the dashboard, run <code>python sentinel.py</code> with systemd, launchd or Docker.',
        'es': 'Para que siga funcionando sin el panel, ejecuta <code>python sentinel.py</code> con systemd, launchd o Docker.',
    },

    # ── Watched records ──
    'sentinel.records.title': {'en': 'Watched records', 'es': 'Registros vigilados'},
    'sentinel.records.zone': {'en': 'Zone', 'es': 'Zona'},
    'sentinel.records.current': {'en': 'Current IP', 'es': 'IP actual'},
    'sentinel.records.target': {'en': 'Target IP', 'es': 'IP de destino'},
    'sentinel.records.no_ip': {'en': 'No IP', 'es': 'Sin IP'},
    'sentinel.records.in_sync': {'en': 'In sync', 'es': 'Sincronizado'},
    'sentinel.records.pending': {'en': 'Update pending', 'es': 'Actualización pendiente'},
    'sentinel.records.empty_title': {'en': 'No watched records', 'es': 'No hay registros vigilados'},
    'sentinel.records.empty_text': {
        'en': "Open a zone's DNS records and turn on auto-update for the A or AAAA records that should follow your IP.",
        'es': 'Abre los registros DNS de una zona y activa la actualización automática en los registros A o AAAA que deben seguir a tu IP.',
    },

    # ── Activity ──
    'sentinel.history.title': {'en': 'Activity', 'es': 'Actividad'},
    'sentinel.history.desc': {
        'en': 'IP changes and failed attempts, newest first.',
        'es': 'Cambios de IP e intentos fallidos, los más recientes primero.',
    },
    'sentinel.history.when': {'en': 'When', 'es': 'Cuándo'},
    'sentinel.history.change': {'en': 'Change', 'es': 'Cambio'},
    'sentinel.history.updated': {'en': 'Updated', 'es': 'Actualizado'},
    'sentinel.history.failed': {'en': 'Failed', 'es': 'Falló'},
    'sentinel.history.empty_title': {'en': 'No activity yet', 'es': 'Aún no hay actividad'},
    'sentinel.history.empty_text': {
        'en': 'Changes made by the sentinel will show up here.',
        'es': 'Aquí aparecerán los cambios que haga el centinela.',
    },

    # Failure reasons stored by app/sentinel/engine.py (Update.response, last_message).
    'sentinel.reason.no_ip': {
        'en': "Couldn't detect your public IP, so records were left as they were.",
        'es': 'No se pudo detectar tu IP pública, así que los registros se dejaron como estaban.',
    },
    'sentinel.reason.no_manual_ip': {
        'en': 'No fixed IP is set, so records were left as they were.',
        'es': 'No hay una IP fija configurada, así que los registros se dejaron como estaban.',
    },
    'sentinel.reason.record_missing': {
        'en': 'The record no longer exists in Cloudflare.',
        'es': 'El registro ya no existe en Cloudflare.',
    },
    'sentinel.reason.unreachable': {'en': "Couldn't reach Cloudflare.", 'es': 'No se pudo conectar con Cloudflare.'},
    'sentinel.reason.forbidden': {
        'en': 'Cloudflare rejected the API token (it needs the Zone → DNS → Edit permission).',
        'es': 'Cloudflare rechazó el token de API (necesita el permiso Zona → DNS → Editar).',
    },
}
