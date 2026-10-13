"""The web installer (first run)."""

STRINGS = {
    'install.title': {'en': 'Install DNSentinel', 'es': 'Instalar DNSentinel'},
    'install.subtitle': {
        'en': 'Connect the database and create the account you will sign in with.',
        'es': 'Conecta la base de datos y crea la cuenta con la que iniciarás sesión.',
    },
    'install.no_token_title': {'en': 'Create an install token first', 'es': 'Primero crea un token de instalación'},
    'install.no_token_html': {
        'en': 'On the server, run <code>python manage.py install-token</code> in the DNSentinel folder, then reload this page.',
        'es': 'En el servidor, ejecuta <code>python manage.py install-token</code> en la carpeta de DNSentinel y recarga esta página.',
    },
    'install.token': {'en': 'Install token', 'es': 'Token de instalación'},
    'install.token_hint_html': {
        'en': 'Printed by <code>python manage.py install-token</code> on the server.',
        'es': 'Lo muestra <code>python manage.py install-token</code> en el servidor.',
    },

    # ── Database ──
    'install.database': {'en': 'MySQL database', 'es': 'Base de datos MySQL'},
    'install.db_host': {'en': 'Host', 'es': 'Host'},
    'install.db_port': {'en': 'Port', 'es': 'Puerto'},
    'install.db_name': {'en': 'Database name', 'es': 'Nombre de la base de datos'},
    'install.db_user': {'en': 'User', 'es': 'Usuario'},
    'install.db_hint': {
        'en': 'The database must already exist. DNSentinel creates its tables.',
        'es': 'La base de datos debe existir. DNSentinel crea sus tablas.',
    },

    # ── Account ──
    'install.account': {'en': 'Your account', 'es': 'Tu cuenta'},
    'install.password_hint': {'en': 'At least {min} characters.', 'es': 'Al menos {min} caracteres.'},
    'install.submit': {'en': 'Install', 'es': 'Instalar'},

    # ── Errors ──
    'install.error.token': {'en': 'The install token is not valid.', 'es': 'El token de instalación no es válido.'},
    'install.error.required': {'en': 'Fill in every required field.', 'es': 'Completa todos los campos obligatorios.'},
    'install.error.port': {'en': 'The database port must be a number.', 'es': 'El puerto de la base de datos debe ser un número.'},
    'install.error.password': {
        'en': 'Your password needs at least {min} characters.',
        'es': 'Tu contraseña necesita al menos {min} caracteres.',
    },
    'install.error.database': {
        'en': 'Could not set up the database: {detail}',
        'es': 'No se pudo preparar la base de datos: {detail}',
    },
}
