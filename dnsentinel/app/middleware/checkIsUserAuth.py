from flask import session, redirect, url_for, flash, request
from functools import wraps

def check_is_user_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path != '/':
                flash('You must log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
