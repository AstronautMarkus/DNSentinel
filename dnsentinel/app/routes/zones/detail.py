from . import zones_bp
from flask import render_template
from flask_login import login_required, current_user
from app.models.models import Zone

@zones_bp.route('/cloudflare/<zone_id>', methods=['GET'])
@login_required
def zone_detail(zone_id):
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    return render_template('zones/detail.html', zone=zone)