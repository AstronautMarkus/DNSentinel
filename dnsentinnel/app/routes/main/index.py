from flask import render_template,redirect,url_for
from flask_login import current_user

def add_index_route(main_bp):
    @main_bp.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.home'))
        return render_template('index.html')
