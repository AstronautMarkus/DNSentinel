from flask import render_template, request, redirect, url_for, flash, current_app, session
from app.models.user import User
from werkzeug.security import check_password_hash

def add_login_route(auth_bp):
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            SessionLocal = current_app.config['SessionLocal']
            session_db = SessionLocal()
            user = session_db.query(User).filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_name'] = user.name
                flash('Login successful', 'success')
                session_db.close()
                return redirect(url_for('dashboard.home'))
            else:
                flash('Email or password is incorrect', 'danger')
            session_db.close()
        return render_template('login.html')
