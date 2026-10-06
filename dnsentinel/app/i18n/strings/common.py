"""Shared UI chrome: layouts, navigation, macros and labels used across pages."""

STRINGS = {
    # ── Generic labels ──
    'common.name': {'en': 'Name', 'es': 'Nombre'},
    'common.type': {'en': 'Type', 'es': 'Tipo'},
    'common.status': {'en': 'Status', 'es': 'Estado'},
    'common.content': {'en': 'Content', 'es': 'Contenido'},
    'common.created': {'en': 'Created', 'es': 'Creado'},
    'common.modified': {'en': 'Modified', 'es': 'Modificado'},
    'common.created_on': {'en': 'Created on', 'es': 'Creado el'},
    'common.modified_on': {'en': 'Modified on', 'es': 'Modificado el'},
    'common.added_to_dnsentinel': {'en': 'Added to DNSentinel', 'es': 'Agregado a DNSentinel'},
    'common.actions': {'en': 'Actions', 'es': 'Acciones'},
    'common.details': {'en': 'Details', 'es': 'Detalles'},
    'common.cancel': {'en': 'Cancel', 'es': 'Cancelar'},
    'common.view_all': {'en': 'View all', 'es': 'Ver todo'},
    'common.zone_id': {'en': 'Zone ID', 'es': 'ID de zona'},
    'common.api_token': {'en': 'API token', 'es': 'Token de API'},
    'common.copy_zone_id': {'en': 'Copy zone ID', 'es': 'Copiar ID de zona'},
    'common.dns_zones': {'en': 'DNS zones', 'es': 'Zonas DNS'},
    'common.dns_records': {'en': 'DNS records', 'es': 'Registros DNS'},
    'common.add_zone': {'en': 'Add zone', 'es': 'Agregar zona'},
    'common.no_zones': {'en': 'No zones yet', 'es': 'Aún no hay zonas'},
    'common.sign_in': {'en': 'Sign in', 'es': 'Iniciar sesión'},
    'common.create_account': {'en': 'Create account', 'es': 'Crear cuenta'},

    # ── Navigation (headers, sidebar, footers) ──
    'nav.main': {'en': 'Main navigation', 'es': 'Navegación principal'},
    'nav.sidebar': {'en': 'Sidebar', 'es': 'Barra lateral'},
    'nav.footer': {'en': 'Footer', 'es': 'Pie de página'},
    'nav.breadcrumb': {'en': 'Breadcrumb', 'es': 'Ruta de navegación'},
    'nav.section_general': {'en': 'General', 'es': 'General'},
    'nav.dashboard': {'en': 'Dashboard', 'es': 'Panel'},
    'nav.go_to_dashboard': {'en': 'Go to dashboard', 'es': 'Ir al panel'},

    # ── Layout ──
    'layout.dynamic_ip_manager': {'en': 'Dynamic IP manager', 'es': 'Gestor de IP dinámica'},
    'layout.tagline': {
        'en': 'Autonomous Cloudflare DNS manager that keeps your records in sync with your dynamic IP address.',
        'es': 'Gestor autónomo de DNS en Cloudflare que mantiene tus registros sincronizados con tu dirección IP dinámica.',
    },
    'layout.rights_reserved': {'en': 'All rights reserved.', 'es': 'Todos los derechos reservados.'},
    'layout.created_by': {'en': 'Created by', 'es': 'Creado por'},
    'layout.dismiss_notification': {'en': 'Dismiss notification', 'es': 'Cerrar notificación'},
    'layout.logout': {'en': 'Log out', 'es': 'Cerrar sesión'},
    'layout.logout_confirm_title': {'en': 'Log out?', 'es': '¿Cerrar sesión?'},
    'layout.logout_confirm_text': {
        'en': "You'll be signed out of DNSentinel. Your DNS records will keep updating in the background.",
        'es': 'Se cerrará tu sesión en DNSentinel. Tus registros DNS seguirán actualizándose en segundo plano.',
    },

    # ── Macros (base/partials/macros.html) ──
    'ui.copy': {'en': 'Copy', 'es': 'Copiar'},
    'ui.copy_token': {'en': 'Copy token', 'es': 'Copiar token'},
    'ui.yes': {'en': 'Yes', 'es': 'Sí'},
    'ui.no': {'en': 'No', 'es': 'No'},
    'ui.on': {'en': 'On', 'es': 'Activado'},
    'ui.off': {'en': 'Off', 'es': 'Desactivado'},
    'ui.proxied': {'en': 'Proxied', 'es': 'Con proxy'},
    'ui.dns_only': {'en': 'DNS only', 'es': 'Solo DNS'},
    'ui.active': {'en': 'Active', 'es': 'Activo'},
    'ui.inactive': {'en': 'Inactive', 'es': 'Inactivo'},
}
