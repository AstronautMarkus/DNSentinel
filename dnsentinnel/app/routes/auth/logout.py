from flask import redirect, url_for, flash
from flask_login import logout_user, current_user
from app.routes.auth import auth_bp

@auth_bp.route('/logout')
def logout():
    user_name = current_user.name if current_user.is_authenticated else "user"
    logout_user()
    flash(f'See you, {user_name}! You have been logged out. We\'ll continue working in the background to keep your addresses updated!', 'info')
    return redirect(url_for('auth.login'))
