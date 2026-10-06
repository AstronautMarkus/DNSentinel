from . import zones_bp
from flask import request, jsonify
from flask_login import login_required
import requests
from app.i18n import t

@zones_bp.route('/cloudflare/validate', methods=['POST'])
@login_required
def validate_zone():
    data = request.json
    zone_id = data.get('zone_id')
    api_token = data.get('api_token')
    if not zone_id or not api_token:
        return jsonify({'ok': False, 'msg': t('zones.api.missing_data')}), 400

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return jsonify({'ok': False, 'msg': t('zones.connection_error', error=str(e))}), 500

    if resp.status_code == 200:
        return jsonify({'ok': True, 'msg': t('zones.api.valid')})
    elif resp.status_code == 403:
        return jsonify({'ok': False, 'msg': t('zones.api.forbidden')})
    elif resp.status_code == 404:
        return jsonify({'ok': False, 'msg': t('zones.api.not_found')})
    elif resp.status_code == 401:
        return jsonify({'ok': False, 'msg': t('zones.api.unauthorized')})
    else:
        return jsonify({'ok': False, 'msg': t('zones.api.unexpected', status=resp.status_code)}), 400