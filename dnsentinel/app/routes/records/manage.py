from . import records_bp
from .form import cloudflare_error_message
from flask import request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, Zone, Record, SentinelSettings
from app.services.cloudflare import CloudflareClient, CloudflareError
from app.i18n import t


@records_bp.route('/<zone_id>/records/<record_id>/delete', methods=['POST'])
@login_required
def delete_record(zone_id, record_id):
    """
    mode=cloudflare: delete the record in Cloudflare, then in DNSentinel.
    mode=local: only stop tracking it; Cloudflare keeps serving it.
    """
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    record = Record.query.filter_by(record_id=record_id, zone_id_fk=zone.id).first_or_404()
    mode = 'local' if request.form.get('mode') == 'local' else 'cloudflare'
    name = record.name

    if mode == 'cloudflare':
        try:
            CloudflareClient(zone.api_token).delete_dns_record(zone.zone_id, record.record_id)
        except CloudflareError as err:
            # Already gone from Cloudflare: forgetting it locally is all that's left.
            if not err.is_not_found:
                flash(cloudflare_error_message(err), 'danger')
                return redirect(url_for('records.detail_record', zone_id=zone.zone_id, record_id=record.record_id))

    db.session.delete(record)
    db.session.commit()
    flash(t('records.flash.deleted' if mode == 'cloudflare' else 'records.flash.untracked', name=name), 'success')
    return redirect(url_for('records.list_records', zone_id=zone.zone_id))


@records_bp.route('/<zone_id>/records/<record_id>/auto_update', methods=['POST'])
@login_required
def toggle_auto_update(zone_id, record_id):
    """Turn sentinel IP tracking on or off for one record. Body: {"enabled": bool}."""
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    record = Record.query.filter_by(record_id=record_id, zone_id_fk=zone.id).first_or_404()
    enabled = bool((request.get_json(silent=True) or {}).get('enabled'))

    if enabled and not record.supports_auto_update:
        return jsonify({'ok': False, 'msg': t('records.api.auto_update_unsupported')}), 400

    record.auto_update = enabled
    settings = SentinelSettings.for_user(current_user.id)
    if enabled:
        settings.next_run_at = None  # check on the sentinel's next tick
    db.session.commit()

    if not enabled:
        msg = t('records.api.auto_update_off', name=record.name)
    elif settings.enabled:
        msg = t('records.api.auto_update_on', name=record.name)
    else:
        msg = t('records.api.auto_update_on_paused', name=record.name)
    return jsonify({'ok': True, 'enabled': enabled, 'sentinel_enabled': settings.enabled, 'msg': msg})


@records_bp.route('/<zone_id>/records/sync', methods=['POST'])
@login_required
def sync_records(zone_id):
    """Refresh every imported record from Cloudflare, and flag the ones deleted there."""
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    try:
        remote = {r['id']: r for r in CloudflareClient(zone.api_token).list_dns_records(zone.zone_id)}
    except CloudflareError as err:
        flash(cloudflare_error_message(err), 'danger')
        return redirect(url_for('records.list_records', zone_id=zone.zone_id))

    refreshed = missing = 0
    for record in zone.records:
        data = remote.get(record.record_id)
        if data:
            record.update_from_cloudflare(data)
            refreshed += 1
        else:
            record.active = False
            record.auto_update = False
            missing += 1
    db.session.commit()

    flash(t('records.flash.synced', refreshed=refreshed, missing=missing,
            not_imported=len(remote) - refreshed), 'warning' if missing else 'success')
    return redirect(url_for('records.list_records', zone_id=zone.zone_id))
