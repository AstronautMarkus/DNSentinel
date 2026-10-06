from . import sentinel_bp
from datetime import timedelta
from flask import render_template, current_app
from flask_login import login_required, current_user
from app.models.models import utcnow, Record, SentinelSettings, Update, Zone
from app.sentinel import lease_heartbeat, target_ips, watched_records
from app.services.ip import detect_public_ips, same_ip


def render_overview(settings, form=None, errors=None, status=200):
    """The sentinel page; `form`/`errors` re-render a rejected settings form."""
    detected = detect_public_ips()
    target_ipv4, target_ipv6 = target_ips(settings, detected)
    records = watched_records(current_user.id)
    for record in records:
        target = target_ipv4 if record.type == 'A' else target_ipv6
        record.target_ip = target
        record.in_sync = bool(target) and same_ip(record.content, target)

    history = (Update.query.join(Record).join(Zone)
               .filter(Zone.user_id == current_user.id)
               .order_by(Update.timestamp.desc(), Update.id.desc())
               .limit(50).all())

    heartbeat = lease_heartbeat()
    lease_ttl = timedelta(seconds=current_app.config['SENTINEL_TICK_SECONDS'] * 3)
    daemon_online = bool(heartbeat) and utcnow() - heartbeat < lease_ttl

    form = form or {
        'enabled': settings.enabled,
        'interval_minutes': settings.interval_minutes,
        'ip_mode': settings.ip_mode,
        'manual_ipv4': settings.manual_ipv4 or '',
        'manual_ipv6': settings.manual_ipv6 or '',
    }
    return render_template('sentinel/index.html', settings=settings, form=form, errors=errors or {},
                           detected=detected, target_ipv4=target_ipv4, target_ipv6=target_ipv6,
                           records=records, history=history, daemon_online=daemon_online,
                           heartbeat=heartbeat, intervals=SentinelSettings.INTERVALS), status


@sentinel_bp.route('', methods=['GET'])
@login_required
def overview():
    return render_overview(SentinelSettings.for_user(current_user.id))
