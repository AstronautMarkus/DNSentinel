"""
The web installer: database credentials and the first account, guarded by
the token from `python manage.py install-token`. Settings are saved only
once the database is ready, so a failed attempt can simply be retried.
"""
import secrets

from flask import Blueprint, redirect, render_template, request
from sqlalchemy.exc import SQLAlchemyError

from app.config.config import check_install_token, clear_install_token, has_install_token, save_settings
from app.i18n import t
from app.models.models import User, db
from app.models.schema import upgrade_schema

install_bp = Blueprint('install', __name__)

TEXT_FIELDS = ('token', 'db_host', 'db_port', 'db_name', 'db_user', 'name', 'email')
DEFAULTS = {'db_host': 'localhost', 'db_port': '3306', 'db_name': 'dnsentinel'}


@install_bp.route('/install', methods=['GET', 'POST'])
def install():
    if not has_install_token():
        return render_template('install.html', no_token=True)

    form = {field: request.form.get(field, DEFAULTS.get(field, '')).strip() for field in TEXT_FIELDS}
    error = None
    if request.method == 'POST':
        error = run_install(form, request.form.get('db_password', ''), request.form.get('password', ''))
        if error is None:
            return redirect(request.script_root + '/auth/login')
    return render_template('install.html', form=form, error=error, min_password=User.MIN_PASSWORD_LENGTH)


def run_install(form, db_password, password):
    """Install DNSentinel. Returns an error message, or None once it is installed."""
    if not check_install_token(form['token']):
        return t('install.error.token')
    if not all(form.values()) or not password:
        return t('install.error.required')
    if not form['db_port'].isdigit():
        return t('install.error.port')
    if len(password) < User.MIN_PASSWORD_LENGTH:
        return t('install.error.password', min=User.MIN_PASSWORD_LENGTH)

    settings = {
        'secret_key': secrets.token_hex(32),
        'database': {
            'host': form['db_host'],
            'port': int(form['db_port']),
            'name': form['db_name'],
            'user': form['db_user'],
            'password': db_password,
        },
        'secure_cookies': request.is_secure,
        'sentinel': {'embedded': False, 'tick_seconds': 30},
    }

    from app import create_app  # app/__init__.py imports this blueprint
    app = create_app(settings)
    try:
        with app.app_context():
            upgrade_schema(db)
            User.save_account(form['name'], form['email'], password)
            db.engine.dispose()
    except SQLAlchemyError as exc:
        return t('install.error.database', detail=str(getattr(exc, 'orig', None) or exc))

    save_settings(settings)
    clear_install_token()
    return None
