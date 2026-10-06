from . import zones_bp
from .validate import check_credentials
from flask import request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, Zone
from app.i18n import t


@zones_bp.route('/cloudflare/<zone_id>/check', methods=['POST'])
@login_required
def check_zone(zone_id):
    """Re-check the stored token against Cloudflare and refresh the zone details."""
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    data, error = check_credentials(zone.zone_id, zone.api_token)
    if error:
        return jsonify({'ok': False, 'msg': error}), 400
    zone.update_from_cloudflare(data)
    db.session.commit()
    return jsonify({'ok': True, 'msg': t('zones.api.still_valid')})


@zones_bp.route('/cloudflare/<zone_id>/token', methods=['POST'])
@login_required
def replace_zone_token(zone_id):
    """Swap the zone's API token for a new one, once Cloudflare accepts it."""
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    api_token = ((request.get_json(silent=True) or {}).get('api_token') or '').strip()
    data, error = check_credentials(zone.zone_id, api_token)
    if error:
        return jsonify({'ok': False, 'msg': error}), 400
    zone.api_token = api_token
    zone.update_from_cloudflare(data)
    db.session.commit()
    return jsonify({'ok': True, 'msg': t('zones.api.token_replaced')})


@zones_bp.route('/cloudflare/<zone_id>/delete', methods=['POST'])
@login_required
def delete_zone(zone_id):
    """Remove the zone, its records and their history from DNSentinel. Cloudflare is untouched."""
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    name = zone.name
    db.session.delete(zone)
    db.session.commit()
    flash(t('zones.flash.deleted', zone=name), 'success')
    return redirect(url_for('zones.list_zones'))
