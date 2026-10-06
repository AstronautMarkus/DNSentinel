from flask import redirect, url_for, flash
from flask_login import logout_user, current_user
from app.routes.auth import auth_bp
from app.i18n import t

@auth_bp.route('/logout')
def logout():
    user_name = current_user.name if current_user.is_authenticated else t('auth.flash.default_user')
    logout_user()
    flash(t('auth.flash.logged_out', name=user_name), 'info')
    return redirect(url_for('auth.login'))
