from flask import render_template, request, redirect, url_for, flash, current_app, session
from app.models.user import User
from app.routes.auth import auth_bp
from werkzeug.security import check_password_hash

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    email = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        SessionLocal = current_app.config['SessionLocal']
        session_db = SessionLocal()
        user = session_db.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash(f'Login successful. Welcome, {user.name}!', 'success')
            session_db.close()
            return redirect(url_for('dashboard.home'))
        else:
            flash('Email or password is incorrect. Please try again.', 'danger')
            session_db.close()
            return render_template('login.html', email=email)
    return render_template('login.html', email=email)
