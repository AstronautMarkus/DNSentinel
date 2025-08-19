from flask import redirect, url_for, flash, session

def add_logout_route(auth_bp):
    @auth_bp.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out. See you next time!', 'info')
        return redirect(url_for('auth.login'))
