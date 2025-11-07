from flask import redirect, url_for, flash, session
from app.routes.auth import auth_bp

@auth_bp.route('/logout')
def logout():
    user_name = session['user_name']
    session.clear()
    flash(f'See you, {user_name}! You have been logged out. We\'ll continue working in the background to keep your addresses updated!', 'info')
    return redirect(url_for('auth.login'))
