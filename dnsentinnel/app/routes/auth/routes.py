from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from app.models.user import User
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

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
            return redirect(url_for('main.index'))
        else:
            flash('Email or password is incorrect', 'danger')
        session_db.close()
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Session closed', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        SessionLocal = current_app.config['SessionLocal']
        session_db = SessionLocal()
        if session_db.query(User).filter_by(email=email).first():
            flash('Email is already registered', 'warning')
            session_db.close()
            return redirect(url_for('auth.register'))
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        session_db.add(new_user)
        session_db.commit()
        session_db.close()
        flash('User registered successfully', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')