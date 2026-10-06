from . import records_bp
from flask import jsonify, request
from flask_login import login_required, current_user
from app.models.models import db, Zone, Record
from app.i18n import t

@records_bp.route('/<zone_id>/records/import', methods=['POST'])
@login_required
def import_record(zone_id):
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first()
    if not zone:
        return jsonify({'error': t('records.api.zone_not_found')}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': t('records.api.invalid_json')}), 400

    # Several records can share a name (A + AAAA + TXT…); the Cloudflare ID is what's unique.
    existing_record = Record.query.filter_by(zone_id_fk=zone.id, record_id=data.get('id')).first()
    if existing_record:
        return jsonify({'error': t('records.api.already_imported')}), 409

    try:
        record = Record(zone_id_fk=zone.id)
        record.update_from_cloudflare(data)
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
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first()
    if not zone:
        return jsonify({'error': t('records.api.zone_not_found')}), 404

    data = request.get_json()
    record_ids = data.get('record_ids', [])
    if not isinstance(record_ids, list):
        return jsonify({'error': t('records.api.invalid_ids')}), 400

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
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first()
    if not zone:
        return jsonify({'error': t('records.api.zone_not_found')}), 404

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
                existing_map[rec_id].update_from_cloudflare(rec)
                updated.append(rec_id)
            else:
                skipped.append(rec_id)
        else:
            record = Record(zone_id_fk=zone.id)
            record.update_from_cloudflare(rec)
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

