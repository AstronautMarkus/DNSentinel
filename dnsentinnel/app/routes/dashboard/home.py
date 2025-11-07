from flask import render_template
from app.routes.dashboard import dashboard_bp

@dashboard_bp.route('/dashboard/home')
def home():
    return render_template('dashboard/home.html')