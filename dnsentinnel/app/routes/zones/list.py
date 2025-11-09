from . import zones_bp
from flask import render_template
from flask_login import login_required, current_user
from ...models.models import Zone

@zones_bp.route('/cloudflare', methods=['GET'])
@login_required
def list_zones():
    user_zones = Zone.query.filter_by(user_id=current_user.id).all()
    return render_template('zones/list.html', user_zones=user_zones)