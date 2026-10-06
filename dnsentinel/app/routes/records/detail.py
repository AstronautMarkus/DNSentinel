from . import records_bp

from flask import render_template
from flask_login import login_required, current_user
from app.models.models import Zone, Record, Update
from app.services.records import EDITABLE_TYPES

@records_bp.route('/<zone_id>/records/<record_id>', methods=['GET'])
@login_required
def detail_record(zone_id, record_id):
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    record = Record.query.filter_by(record_id=record_id, zone_id_fk=zone.id).first()
    history = (Update.query.filter_by(record_id_fk=record.id)
               .order_by(Update.timestamp.desc(), Update.id.desc()).limit(20).all()) if record else []
    return render_template('records/detail.html', zone=zone, zone_id=zone_id, record=record,
                           history=history, editable=bool(record) and record.type in EDITABLE_TYPES)
