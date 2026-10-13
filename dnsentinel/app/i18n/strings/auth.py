"""Sign in and logout."""

STRINGS = {
    'auth.email': {'en': 'Email', 'es': 'Correo electrónico'},
    'auth.password': {'en': 'Password', 'es': 'Contraseña'},
    'auth.name_placeholder': {'en': 'John Doe', 'es': 'Juan Pérez'},
    'auth.email_placeholder': {'en': 'john@example.com', 'es': 'juan@example.com'},

    # ── Login ──
    'auth.login.subtitle': {'en': 'Sign in to your DNSentinel account.', 'es': 'Inicia sesión en tu cuenta de DNSentinel.'},

    # ── Flash messages ──
    'auth.flash.login_success': {
        'en': 'Login successful. Welcome, {name}!',
        'es': 'Sesión iniciada. ¡Te damos la bienvenida, {name}!',
    },
    'auth.flash.login_required': {'en': 'Please sign in to continue.', 'es': 'Inicia sesión para continuar.'},
    'auth.flash.login_failed': {
        'en': 'Email or password is incorrect. Please try again.',
        'es': 'El correo o la contraseña son incorrectos. Inténtalo de nuevo.',
    },
    'auth.flash.logged_out': {
        'en': "See you, {name}! You have been logged out. We'll continue working in the background to keep your addresses updated!",
        'es': '¡Hasta pronto, {name}! Cerraste sesión. ¡Seguiremos trabajando en segundo plano para mantener tus direcciones actualizadas!',
    },
    'auth.flash.default_user': {'en': 'user', 'es': 'usuario'},
}
