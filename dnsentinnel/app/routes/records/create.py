from . import records_bp
from flask import render_template, jsonify, request
from flask_login import login_required
from app.models.models import db, Zone, Record
from flask_login import current_user
import requests
from datetime import datetime


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

@records_bp.route('/<zone_id>/records/import', methods=['POST'])
@login_required
def import_record(zone_id):
    zone = Zone.query.filter_by(zone_id=zone_id).first()
    if not zone:
        return jsonify({'error': 'Zone not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    existing_record = Record.query.filter_by(zone_id_fk=zone.id, name=data.get('name')).first()
    if existing_record:
        return jsonify({'error': 'A record with this name already exists in the zone'}), 409

    try:
        record = Record(
            zone_id_fk=zone.id,
            record_id=data.get('id'),
            name=data.get('name'),
            type=data.get('type'),
            proxied=data.get('proxied', False),
            proxiable=data.get('proxiable', True),
            ttl=data.get('ttl', 1),
            active=True,
            content=data.get('content'),
            comment=data.get('comment'),
            created_on=datetime.fromisoformat(data['created_on'].replace('Z', '+00:00')) if data.get('created_on') else None,
            modified_on=datetime.fromisoformat(data['modified_on'].replace('Z', '+00:00')) if data.get('modified_on') else None,
            settings=data.get('settings'),
            tags=data.get('tags'),
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({'success': True, 'id': record.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

