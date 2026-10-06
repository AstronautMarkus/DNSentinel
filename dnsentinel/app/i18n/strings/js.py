"""
Strings used from JavaScript. Every `js.*` key is embedded in each page as
JSON (base/partials/head.html) and read with `t(key, vars)` from
static/js/app.js. Templates can use them with t() too, so text shared
between the server-rendered markup and a script lives in one place.
"""

STRINGS = {
    # ── Shared behaviour (static/js/app.js) ──
    'js.common.ok': {'en': 'OK', 'es': 'Aceptar'},
    'js.common.cancel': {'en': 'Cancel', 'es': 'Cancelar'},
    'js.common.confirm': {'en': 'Confirm', 'es': 'Confirmar'},
    'js.common.are_you_sure': {'en': 'Are you sure?', 'es': '¿Seguro que quieres continuar?'},
    'js.common.error': {'en': 'Error', 'es': 'Error'},
    'js.common.unexpected_error': {'en': 'Unexpected error', 'es': 'Error inesperado'},
    'js.common.show_token': {'en': 'Show token', 'es': 'Mostrar token'},
    'js.common.hide_token': {'en': 'Hide token', 'es': 'Ocultar token'},
    'js.layout.show_navigation': {'en': 'Show navigation', 'es': 'Mostrar navegación'},
    'js.layout.hide_navigation': {'en': 'Hide navigation', 'es': 'Ocultar navegación'},

    # ── Zone credential validation (zones/create.html) ──
    'js.zones.validating': {'en': 'Validating...', 'es': 'Validando...'},
    'js.zones.validating_text': {'en': 'Checking credentials with Cloudflare', 'es': 'Comprobando las credenciales con Cloudflare'},
    'js.zones.validated': {'en': 'Validated!', 'es': '¡Validado!'},
    'js.zones.validation_error': {'en': 'Validation Error', 'es': 'Error de validación'},
    'js.zones.validation_failed': {
        'en': 'Could not validate. Please try again or check your connection.',
        'es': 'No se pudo validar. Inténtalo de nuevo o revisa tu conexión.',
    },
    'js.zones.validate_first': {'en': 'Please validate credentials first', 'es': 'Primero valida las credenciales'},

    # ── Record import dialogs (records/list.html) ──
    'js.records.fetching': {'en': 'Fetching Cloudflare records...', 'es': 'Obteniendo registros de Cloudflare...'},
    'js.records.fetch_failed': {'en': 'Failed to fetch records', 'es': 'No se pudieron obtener los registros'},
    'js.records.none_found': {'en': 'No records found', 'es': 'No se encontraron registros'},
    'js.records.select_one': {'en': 'Select a record to import', 'es': 'Selecciona un registro para importar'},
    'js.records.not_found': {'en': 'Record not found', 'es': 'Registro no encontrado'},
    'js.records.confirm_single': {'en': 'Import this record?', 'es': '¿Importar este registro?'},
    'js.records.import': {'en': 'Import', 'es': 'Importar'},
    'js.records.importing': {'en': 'Importing...', 'es': 'Importando...'},
    'js.records.importing_all': {'en': 'Importing records...', 'es': 'Importando registros...'},
    'js.records.import_failed': {'en': 'Failed to import', 'es': 'No se pudo importar'},
    'js.records.imported': {'en': 'Imported!', 'es': '¡Importado!'},
    'js.records.check_failed': {'en': 'Failed to check existing records', 'es': 'No se pudieron comprobar los registros existentes'},
    'js.records.exist_title': {'en': 'Some records already exist', 'es': 'Algunos registros ya existen'},
    'js.records.exist_intro': {'en': 'The following records already exist:', 'es': 'Los siguientes registros ya existen:'},
    'js.records.exist_question': {'en': 'What do you want to do?', 'es': '¿Qué quieres hacer?'},
    'js.records.replace': {'en': 'Replace', 'es': 'Reemplazar'},
    'js.records.ignore': {'en': 'Ignore', 'es': 'Ignorar'},
    'js.records.confirm_all': {'en': 'Import all records?', 'es': '¿Importar todos los registros?'},
    # {count} picks the plural form; {n} is the (bold) number shown.
    'js.records.confirm_all_text': {
        'en': {'one': 'You are about to import {n} record.', 'other': 'You are about to import {n} records.'},
        'es': {'one': 'Estás a punto de importar {n} registro.', 'other': 'Estás a punto de importar {n} registros.'},
    },
    'js.records.action': {'en': 'Action:', 'es': 'Acción:'},
    'js.records.import_finished': {'en': 'Import finished', 'es': 'Importación finalizada'},
    'js.records.added': {'en': 'Added:', 'es': 'Agregados:'},
    'js.records.updated': {'en': 'Updated:', 'es': 'Actualizados:'},
    'js.records.skipped': {'en': 'Skipped:', 'es': 'Omitidos:'},

    # ── Alerts chart (dashboard/home.html) ──
    'js.dashboard.series': {'en': 'Alerts', 'es': 'Alertas'},
    'js.dashboard.alerts': {
        'en': {'one': '{count} alert', 'other': '{count} alerts'},
        'es': {'one': '{count} alerta', 'other': '{count} alertas'},
    },
    'js.dashboard.total': {'en': 'Total: {value}', 'es': 'Total: {value}'},
    'js.dashboard.peak': {'en': 'Peak: {value} on {day}', 'es': 'Máximo: {value} el {day}'},

    # ── Landing walkthrough (static/js/ip-demo.js, index.html) ──
    'js.demo.pause': {'en': 'Pause', 'es': 'Pausar'},
    'js.demo.play': {'en': 'Play', 'es': 'Reproducir'},
    'js.demo.status_online': {'en': 'All sites online', 'es': 'Todos los sitios en línea'},
    'js.demo.status_changed': {'en': 'IP changed', 'es': 'La IP cambió'},
    'js.demo.status_down': {'en': 'Sites down', 'es': 'Sitios caídos'},
    'js.demo.status_fixing': {'en': 'Updating DNS', 'es': 'Actualizando DNS'},
    'js.demo.dns_ok': {'en': 'Records match your IP', 'es': 'Los registros coinciden con tu IP'},
    'js.demo.dns_stale': {'en': 'Records still point to {ip}', 'es': 'Los registros aún apuntan a {ip}'},
    'js.demo.dns_updated': {'en': 'Updated by DNSentinel', 'es': 'Actualizado por DNSentinel'},
    'js.demo.site_online': {'en': 'Online', 'es': 'En línea'},
    'js.demo.site_down': {'en': 'Down', 'es': 'Caído'},
    'js.demo.agent_off': {'en': 'Not running', 'es': 'Detenido'},
    'js.demo.looking_up': {'en': 'Looking up {domain}…', 'es': 'Buscando {domain}…'},
    'js.demo.connecting': {'en': 'Connecting to {ip}…', 'es': 'Conectando con {ip}…'},
    'js.demo.nobody_at': {'en': 'Nobody at {ip}', 'es': 'Nadie en {ip}'},
    'js.demo.new_ip': {'en': 'New IP detected: {ip}', 'es': 'Nueva IP detectada: {ip}'},
    'js.demo.updating': {'en': 'Updating Cloudflare records…', 'es': 'Actualizando registros de Cloudflare…'},
    'js.demo.updated': {'en': 'Cloudflare records updated', 'es': 'Registros de Cloudflare actualizados'},
}
