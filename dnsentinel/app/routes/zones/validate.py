from . import zones_bp
from flask import request, jsonify
from flask_login import login_required
from app.i18n import t
from app.services.cloudflare import CloudflareClient, CloudflareError, is_cloudflare_id


def credentials_error(err):
    """User-facing message for a CloudflareError raised while checking credentials."""
    if err.status is None:
        return t('zones.connection_error', error=str(err))
    if err.is_not_found:
        return t('zones.api.not_found')
    if err.status == 403:
        return t('zones.api.forbidden')
    if err.is_auth_error:
        return t('zones.api.unauthorized')
    return t('zones.api.unexpected', status=f'{err.status} – {err}')


def check_credentials(zone_id, api_token):
    """
    Check a Zone ID + API token against Cloudflare: the token must be able
    to read the zone and its DNS records. Returns (zone, None) with the
    zone's API `result` when valid, or (None, user-facing message).
    """
    if not zone_id or not api_token:
        return None, t('zones.api.missing_data')
    if not is_cloudflare_id(zone_id):
        return None, t('zones.api.not_found')

    client = CloudflareClient(api_token)
    try:
        zone = client.get_zone(zone_id)
    except CloudflareError as err:
        return None, credentials_error(err)
    try:
        client.dns_records_page(zone_id, per_page=5)
    except CloudflareError as err:
        return None, t('zones.api.no_dns_permission') if err.is_auth_error else credentials_error(err)
    return zone, None


@zones_bp.route('/cloudflare/validate', methods=['POST'])
@login_required
def validate_zone():
    data = request.get_json(silent=True) or {}
    zone_id = (data.get('zone_id') or '').strip().lower()
    api_token = (data.get('api_token') or '').strip()

    zone, error = check_credentials(zone_id, api_token)
    if error:
        return jsonify({'ok': False, 'msg': error}), 400
    return jsonify({'ok': True, 'msg': t('zones.api.valid'), 'name': zone.get('name')})
