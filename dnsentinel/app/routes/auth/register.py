from flask import render_template, request, redirect, url_for, flash
from app.models.models import User, db
from werkzeug.security import generate_password_hash
from app.routes.auth import auth_bp
from app.i18n import t

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash(t('auth.flash.email_taken'), 'warning')
            return redirect(url_for('auth.register'))
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(t('auth.flash.registered'), 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')
