from flask import redirect,url_for
from flask_login import current_user
from app.i18n import render_localized_template

def add_index_route(main_bp):
    @main_bp.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.home'))
        return render_localized_template('index.html')
