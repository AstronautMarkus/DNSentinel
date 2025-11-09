from . import zones_bp
from flask import request, jsonify
import requests

@zones_bp.route('/validate', methods=['POST'])
def validate_zone():
    data = request.json
    zone_id = data.get('zone_id')
    api_token = data.get('api_token')
    if not zone_id or not api_token:
        return jsonify({'ok': False, 'msg': 'Missing data. Please complete all fields.'}), 400

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Connection error with Cloudflare: {str(e)}'}), 500

    if resp.status_code == 200:
        return jsonify({'ok': True, 'msg': 'Zone and token are valid! You can continue with the creation.'})
    elif resp.status_code == 403:
        return jsonify({'ok': False, 'msg': 'The token is valid, but does not have permission to access this zone. Check the permissions in Cloudflare.'})
    elif resp.status_code == 404:
        return jsonify({'ok': False, 'msg': 'The Zone ID does not exist or is not accessible with this token. Please check that the Zone ID is correct.'})
    elif resp.status_code == 401:
        return jsonify({'ok': False, 'msg': 'The token is invalid or expired. Generate a new token in Cloudflare.'})
    else:
        return jsonify({'ok': False, 'msg': f'Unexpected error: {resp.status_code}'}), 400