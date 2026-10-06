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
    'dashboard.alerts': {'en': 'Alerts', 'es': 'Alertas'},
    'dashboard.updates': {'en': 'Updates', 'es': 'Actualizaciones'},
    'dashboard.users': {'en': 'Users', 'es': 'Usuarios'},

    # ── Zones card ──
    'dashboard.cf_zones': {'en': 'Cloudflare DNS zones', 'es': 'Zonas DNS de Cloudflare'},
    'dashboard.records': {'en': 'Records', 'es': 'Registros'},
    'dashboard.empty_text': {
        'en': 'Connect a Cloudflare zone to start keeping its DNS records in sync.',
        'es': 'Conecta una zona de Cloudflare para empezar a mantener sincronizados sus registros DNS.',
    },

    # ── Alerts chart ──
    'dashboard.alerts_week': {'en': 'Alerts this week', 'es': 'Alertas de esta semana'},
    'dashboard.alerts_desc': {'en': 'Daily alert count, last 7 days', 'es': 'Alertas por día, últimos 7 días'},
    'dashboard.chart_label': {
        'en': 'Line chart of alerts per day this week',
        'es': 'Gráfico de líneas de alertas por día de esta semana',
    },
}
