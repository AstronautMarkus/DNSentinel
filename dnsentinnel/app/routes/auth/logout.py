from flask import redirect, url_for, flash, session
from app.routes.auth import auth_bp

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out. See you next time!', 'info')
    return redirect(url_for('auth.login'))
