from . import records_bp

from flask import render_template
from flask_login import login_required, current_user
from app.models.models import Zone, Record, SentinelSettings
from app.services.records import EDITABLE_TYPES

@records_bp.route('/<zone_id>/records', methods=['GET'])
@login_required
def list_records(zone_id):
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    records = Record.query.filter_by(zone_id_fk=zone.id).order_by(Record.name, Record.type).all()
    return render_template('records/list.html', records=records, zone=zone, zone_id=zone_id,
                           editable_types=EDITABLE_TYPES, sentinel=SentinelSettings.for_user(current_user.id))
