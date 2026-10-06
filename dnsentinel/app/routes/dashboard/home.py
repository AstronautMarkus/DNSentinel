from flask import render_template
from app.routes.dashboard import dashboard_bp
import socket
from datetime import timedelta
from sqlalchemy import func
from flask_login import current_user, login_required
from app.models.models import db, utcnow, Zone, Record, SentinelSettings, Update
from app.services.ip import detect_public_ips
from app.i18n import t

CHART_DAYS = 7


@dashboard_bp.route('/home')
@login_required
def home():
    
    isp_ip = detect_public_ips().ipv4 or t('dashboard.no_internet')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ethernet_ip = s.getsockname()[0]
    except Exception:
        ethernet_ip = "127.0.0.1"
        
    finally:
        s.close()

    user_zones = Zone.query.filter_by(user_id=current_user.id).order_by(Zone.id.desc()).all()
    record_counts = dict(
        db.session.query(Record.zone_id_fk, func.count(Record.id))
        .join(Zone).filter(Zone.user_id == current_user.id)
        .group_by(Record.zone_id_fk).all()
    )
    watched_count = (Record.query.join(Zone)
                     .filter(Zone.user_id == current_user.id, Record.auto_update.is_(True)).count())

    # Sentinel activity per day (UTC), oldest first, for the stats and the chart.
    today = utcnow().date()
    days = [today - timedelta(days=offset) for offset in range(CHART_DAYS - 1, -1, -1)]
    since = utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=CHART_DAYS - 1)
    events = (db.session.query(Update.timestamp, Update.status)
              .join(Record).join(Zone)
              .filter(Zone.user_id == current_user.id, Update.timestamp >= since).all())
    updates_per_day = {day: 0 for day in days}
    failures = 0
    for timestamp, status in events:
        if status == 'updated':
            updates_per_day[timestamp.date()] = updates_per_day.get(timestamp.date(), 0) + 1
        else:
            failures += 1

    return render_template('dashboard/home.html', isp_ip=isp_ip, ethernet_ip=ethernet_ip,
                           user_zones=user_zones[:3], zone_count=len(user_zones), record_counts=record_counts,
                           watched_count=watched_count, sentinel=SentinelSettings.for_user(current_user.id),
                           chart_days=[day.isoformat() for day in days],
                           chart_values=[updates_per_day[day] for day in days],
                           update_count=sum(updates_per_day.values()), failure_count=failures)
