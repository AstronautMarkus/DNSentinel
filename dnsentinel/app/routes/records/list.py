from . import records_bp

from flask import render_template
from flask_login import login_required
from app.models.models import Zone, Record

@records_bp.route('/<zone_id>/records', methods=['GET'])
@login_required
def list_records(zone_id):
    zone = Zone.query.filter_by(zone_id=zone_id).first()
    records = []
    if zone:
        records = Record.query.filter_by(zone_id_fk=zone.id).all()
    return render_template('records/list.html', records=records, zone=zone)