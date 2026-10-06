from . import sentinel_bp
from flask import jsonify, request
from flask_login import login_required, current_user
from app.models.models import SentinelSettings
from app.sentinel import run_check, target_ips
from app.services.ip import detect_public_ips
from app.i18n import t


@sentinel_bp.route('/check', methods=['POST'])
@login_required
def check_now():
    """Run the sentinel for the signed-in user right away, with a fresh IP lookup."""
    settings = SentinelSettings.for_user(current_user.id)
    detected = detect_public_ips(max_age=0) if settings.ip_mode == 'auto' else None
    result = run_check(settings, detected)
    return jsonify({
        'ok': result.status == 'ok',
        'summary': result.summary(),
        'ipv4': result.ipv4,
        'ipv6': result.ipv6,
        'msg': t(result.message, default=result.message) if result.message else None,
    })


@sentinel_bp.route('/ip', methods=['GET'])
@login_required
def current_ip():
    """
    The IPs the user's records should point at (per their sentinel settings),
    plus what was detected online. ?refresh=1 skips the detection cache.
    """
    settings = SentinelSettings.for_user(current_user.id)
    detected = detect_public_ips(max_age=0 if request.args.get('refresh') else 60)
    ipv4, ipv6 = target_ips(settings, detected)
    return jsonify({
        'mode': settings.ip_mode,
        'ipv4': ipv4,
        'ipv6': ipv6,
        'detected': {
            'ipv4': detected.ipv4,
            'ipv6': detected.ipv6,
            'ipv4_source': detected.ipv4_source,
            'ipv6_source': detected.ipv6_source,
        },
    })
