from . import records_bp

from flask import render_template
from flask_login import login_required
from app.models.models import Zone, Record

@records_bp.route('/<zone_id>/records/<record_id>', methods=['GET'])
@login_required
def detail_record(zone_id, record_id):
    zone = Zone.query.filter_by(zone_id=zone_id).first()
    record = None
    if zone:
        record = Record.query.filter_by(record_id=record_id, zone_id_fk=zone.id).first()
    return render_template('records/detail.html', zone_id=zone_id, record=record)