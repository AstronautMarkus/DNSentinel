from . import records_bp
from .form import cloudflare_error_message
from flask import jsonify
from flask_login import login_required, current_user
from app.models.models import Zone
from app.services.cloudflare import CloudflareClient, CloudflareError
from app.i18n import t

@records_bp.route('/<zone_id>/records/cloudflare', methods=['GET'])
@login_required
def get_cloudflare_records(zone_id):
    
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first()

    if not zone or not zone.api_token:
        return jsonify({'error': t('records.api.zone_or_token_missing')}), 404

    try:
        records = CloudflareClient(zone.api_token).list_dns_records(zone.zone_id)
    except CloudflareError as err:
        return jsonify({'error': cloudflare_error_message(err)}), 502
    return jsonify({'result': records})
