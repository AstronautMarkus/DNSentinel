from flask import render_template, request, redirect, url_for, flash, current_app
from app.models.user import User
from werkzeug.security import generate_password_hash
from app.routes.auth import auth_bp

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
