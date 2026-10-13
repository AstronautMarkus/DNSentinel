"""
DNSentinel's settings, Nextcloud style: no .env, the web installer (/install)
writes them once to config/config.json.enc, encrypted with config/secret.key.
Edit them later with `python manage.py config edit`.

    {
      "secret_key": "...",
      "database": {"host": "localhost", "port": 3306, "name": "dnsentinel", "user": "...", "password": "..."},
      "secure_cookies": true,                            # installed over HTTPS
      "sentinel": {"embedded": false, "tick_seconds": 30}
    }

The installer only runs with a token from `python manage.py install-token`,
so nobody else can claim a fresh deployment.
"""
import hashlib
import hmac
import json
import os
import secrets
import tempfile

from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy.engine import URL

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
CONFIG_FILE = 'config.json.enc'
KEY_FILE = 'secret.key'
TOKEN_FILE = 'install.token'


def _path(name):
    return os.path.join(CONFIG_DIR, name)


def _read(name):
    with open(_path(name), 'rb') as f:
        return f.read()


def _write(name, data):
    """Atomic write, readable only by the user running DNSentinel."""
    os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=CONFIG_DIR)  # created 0600
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
    os.replace(tmp, _path(name))


def is_installed():
    return os.path.exists(_path(CONFIG_FILE))


def load_settings():
    if not is_installed():
        raise RuntimeError(f'DNSentinel is not installed: {_path(CONFIG_FILE)} is missing. Open the web installer first.')
    try:
        return json.loads(Fernet(_read(KEY_FILE)).decrypt(_read(CONFIG_FILE)))
    except InvalidToken:
        raise RuntimeError(f'{_path(CONFIG_FILE)} cannot be decrypted with {_path(KEY_FILE)}.') from None


def save_settings(settings):
    if not os.path.exists(_path(KEY_FILE)):
        _write(KEY_FILE, Fernet.generate_key())
    _write(CONFIG_FILE, Fernet(_read(KEY_FILE)).encrypt(json.dumps(settings, indent=2).encode()))


def database_url(database):
    return URL.create(
        'mysql+pymysql',
        username=database['user'],
        password=database['password'],
        host=database['host'],
        port=int(database['port']),
        database=database['name'],
    ).render_as_string(hide_password=False)


def flask_config(settings):
    sentinel = settings.get('sentinel', {})
    secure = bool(settings.get('secure_cookies', False))
    return {
        'SECRET_KEY': settings['secret_key'],
        'SQLALCHEMY_DATABASE_URI': database_url(settings['database']),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        # The sentinel thread keeps connections open for days; drop the ones MySQL timed out.
        'SQLALCHEMY_ENGINE_OPTIONS': {'pool_pre_ping': True, 'pool_recycle': 3600},
        'SESSION_COOKIE_SAMESITE': 'Lax',
        'SESSION_COOKIE_SECURE': secure,
        'REMEMBER_COOKIE_SECURE': secure,
        # Run the IP sentinel inside the web process (see app/sentinel/); the
        # dnsentinel-sentinel service runs it on its own instead.
        'SENTINEL_EMBEDDED': bool(sentinel.get('embedded', False)),
        # How often the sentinel looks for users whose check is due.
        'SENTINEL_TICK_SECONDS': int(sentinel.get('tick_seconds', 30)),
    }


# ── Install token ──
# Only its hash is stored; the installer deletes it once DNSentinel is installed.

def _digest(token):
    return hashlib.sha256(token.encode()).hexdigest()


def new_install_token():
    token = secrets.token_urlsafe(24)
    _write(TOKEN_FILE, _digest(token).encode())
    return token


def has_install_token():
    return os.path.exists(_path(TOKEN_FILE))


def check_install_token(token):
    try:
        expected = _read(TOKEN_FILE).decode().strip()
    except FileNotFoundError:
        return False
    return hmac.compare_digest(_digest(token), expected)


def clear_install_token():
    try:
        os.remove(_path(TOKEN_FILE))
    except FileNotFoundError:
        pass
