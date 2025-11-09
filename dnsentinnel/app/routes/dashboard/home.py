from flask import render_template, flash
from app.routes.dashboard import dashboard_bp
import requests
import socket
from flask_login import current_user, login_required
from app.models.models import Zone


@dashboard_bp.route('/dashboard/home')
@login_required
def home():
    
    try:
        isp_ip = requests.get('https://api.ipify.org').text
    except:
        isp_ip = "Not connected to Internet"

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ethernet_ip = s.getsockname()[0]
    except Exception:
        ethernet_ip = "127.0.0.1"
        
    finally:
        s.close()

    user_zones = Zone.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard/home.html', isp_ip=isp_ip, ethernet_ip=ethernet_ip, user_zones=user_zones)