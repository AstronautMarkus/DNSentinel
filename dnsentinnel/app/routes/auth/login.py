from flask import render_template, request, redirect, url_for, flash, current_app, session
from app.models.models import User
from app.routes.auth import auth_bp
from werkzeug.security import check_password_hash
from flask_login import login_user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    email = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Login successful. Welcome, {user.name}!', 'success')
            return redirect(url_for('dashboard.home'))
        else:
            flash('Email or password is incorrect. Please try again.', 'danger')
            return render_template('login.html', email=email)
    return render_template('login.html', email=email)
