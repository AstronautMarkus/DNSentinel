from . import records_bp
from flask import jsonify, request
from flask_login import login_required
from app.models.models import db, Zone, Record
from datetime import datetime

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

@records_bp.route('/<zone_id>/records/check_existing', methods=['POST'])
@login_required
def check_existing_records(zone_id):
    """
    Receive: { "record_ids": [ ... ] }
    Return: { "existing": [ { "record_id": ..., "name": ... }, ... ] }
    """
    zone = Zone.query.filter_by(zone_id=zone_id).first()
    if not zone:
        return jsonify({'error': 'Zone not found'}), 404

    data = request.get_json()
    record_ids = data.get('record_ids', [])
    if not isinstance(record_ids, list):
        return jsonify({'error': 'Invalid record_ids'}), 400

    existing = Record.query.filter(
        Record.zone_id_fk == zone.id,
        Record.record_id.in_(record_ids)
    ).all()

    result = [{"record_id": r.record_id, "name": r.name} for r in existing]
    return jsonify({"existing": result})


@records_bp.route('/<zone_id>/records/import_bulk', methods=['POST'])
@login_required
def import_bulk_records(zone_id):
    """
    Receive: {
        "records": [ {...}, ... ],
        "action": "replace" | "ignore" | "cancel"
    }
    """
    zone = Zone.query.filter_by(zone_id=zone_id).first()
    if not zone:
        return jsonify({'error': 'Zone not found'}), 404

    data = request.get_json()
    records = data.get('records', [])
    action = data.get('action', 'ignore')

    if action == 'cancel':
        return jsonify({'cancelled': True}), 200

    record_ids = [r.get('id') for r in records if r.get('id')]
    existing_records = Record.query.filter(
        Record.zone_id_fk == zone.id,
        Record.record_id.in_(record_ids)
    ).all()
    existing_map = {r.record_id: r for r in existing_records}

    added, updated, skipped = [], [], []

    for rec in records:
        rec_id = rec.get('id')
        if rec_id in existing_map:
            if action == 'replace':
                # Update existing record
                record = existing_map[rec_id]
                record.name = rec.get('name')
                record.type = rec.get('type')
                record.proxied = rec.get('proxied', False)
                record.proxiable = rec.get('proxiable', True)
                record.ttl = rec.get('ttl', 1)
                record.active = True
                record.content = rec.get('content')
                record.comment = rec.get('comment')
                record.created_on = datetime.fromisoformat(rec['created_on'].replace('Z', '+00:00')) if rec.get('created_on') else None
                record.modified_on = datetime.fromisoformat(rec['modified_on'].replace('Z', '+00:00')) if rec.get('modified_on') else None
                record.settings = rec.get('settings')
                record.tags = rec.get('tags')
                updated.append(rec_id)
            elif action == 'ignore':
                skipped.append(rec_id)
                continue
        else:
            # Add new record
            record = Record(
                zone_id_fk=zone.id,
                record_id=rec.get('id'),
                name=rec.get('name'),
                type=rec.get('type'),
                proxied=rec.get('proxied', False),
                proxiable=rec.get('proxiable', True),
                ttl=rec.get('ttl', 1),
                active=True,
                content=rec.get('content'),
                comment=rec.get('comment'),
                created_on=datetime.fromisoformat(rec['created_on'].replace('Z', '+00:00')) if rec.get('created_on') else None,
                modified_on=datetime.fromisoformat(rec['modified_on'].replace('Z', '+00:00')) if rec.get('modified_on') else None,
                settings=rec.get('settings'),
                tags=rec.get('tags'),
            )
            db.session.add(record)
            added.append(rec_id)
    try:
        db.session.commit()
        return jsonify({
            'added': added,
            'updated': updated,
            'skipped': skipped
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

