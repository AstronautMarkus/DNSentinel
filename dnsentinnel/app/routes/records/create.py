from . import records_bp
from flask import render_template, jsonify, request
from flask_login import login_required
from app.models.models import Zone, Record
from flask_login import current_user
import requests

@records_bp.route('/<zone_id>/records/create', methods=['GET'])
@login_required
def create_record(zone_id):
    return render_template('records/create.html', zone_id=zone_id)

@records_bp.route('/<zone_id>/records/cloudflare', methods=['GET'])
@login_required
def get_cloudflare_records(zone_id):
    
    zone = Zone.query.filter_by(zone_id=zone_id).first()

    print(f"Retrieved zone: {zone}")
    if zone:
        print(f"Using API token: {zone.api_token}")

    if not zone or not zone.api_token:
        return jsonify({'error': 'Zone not found or API token missing'}), 404

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?per_page=100"
    headers = {
        "Authorization": f"Bearer {zone.api_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

