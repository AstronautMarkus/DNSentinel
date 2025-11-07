from flask import render_template
from app.routes.dashboard import dashboard_bp
import requests
import socket


@dashboard_bp.route('/dashboard/home')
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

    return render_template('dashboard/home.html', isp_ip=isp_ip, ethernet_ip=ethernet_ip)