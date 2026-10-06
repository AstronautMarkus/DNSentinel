"""Dashboard home."""

STRINGS = {
    'dashboard.welcome': {'en': 'Welcome back, {name}', 'es': 'Hola de nuevo, {name}'},
    'dashboard.subtitle': {'en': 'Your DNS and IP status at a glance.', 'es': 'El estado de tu DNS y tu IP de un vistazo.'},
    'dashboard.view_zones': {'en': 'View zones', 'es': 'Ver zonas'},

    # ── IP cards ──
    'dashboard.network_addresses': {'en': 'Network addresses', 'es': 'Direcciones de red'},
    'dashboard.public_ip': {'en': 'Public IP address (ISP)', 'es': 'Dirección IP pública (ISP)'},
    'dashboard.local_ip': {'en': 'Local IP address (Ethernet)', 'es': 'Dirección IP local (Ethernet)'},
    'dashboard.copy_public_ip': {'en': 'Copy public IP', 'es': 'Copiar IP pública'},
    'dashboard.copy_local_ip': {'en': 'Copy local IP', 'es': 'Copiar IP local'},
    'dashboard.no_internet': {'en': 'Not connected to Internet', 'es': 'Sin conexión a Internet'},

    # ── Stats ──
    'dashboard.summary': {'en': 'Summary', 'es': 'Resumen'},
    'dashboard.zones': {'en': 'Zones', 'es': 'Zonas'},
    'dashboard.watched': {'en': 'Watched records', 'es': 'Registros vigilados'},
    'dashboard.updates': {'en': 'IP updates', 'es': 'Actualizaciones de IP'},
    'dashboard.failures': {'en': 'Failed updates', 'es': 'Actualizaciones fallidas'},
    'dashboard.last_7_days': {'en': 'Last 7 days', 'es': 'Últimos 7 días'},

    # ── Zones card ──
    'dashboard.cf_zones': {'en': 'Cloudflare DNS zones', 'es': 'Zonas DNS de Cloudflare'},
    'dashboard.records': {'en': 'Records', 'es': 'Registros'},
    'dashboard.empty_text': {
        'en': 'Connect a Cloudflare zone to start keeping its DNS records in sync.',
        'es': 'Conecta una zona de Cloudflare para empezar a mantener sincronizados sus registros DNS.',
    },

    # ── Updates chart ──
    'dashboard.updates_week': {'en': 'IP updates this week', 'es': 'Actualizaciones de IP de esta semana'},
    'dashboard.updates_desc': {
        'en': 'Records updated by the sentinel per day (UTC), last 7 days',
        'es': 'Registros actualizados por el centinela por día (UTC), últimos 7 días',
    },
    'dashboard.chart_label': {
        'en': 'Line chart of IP updates per day this week',
        'es': 'Gráfico de líneas de actualizaciones de IP por día de esta semana',
    },
}
