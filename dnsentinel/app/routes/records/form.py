from . import records_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, Zone, Record, SentinelSettings
from app.services.cloudflare import CloudflareClient, CloudflareError
from app.services.records import EDITABLE_TYPES, TTL_CHOICES, form_values, parse_record_form
from app.sentinel import target_ips
from app.i18n import t


def cloudflare_error_message(err):
    """User-facing message for a CloudflareError raised by a record operation."""
    if err.status is None:
        return t('records.flash.unreachable')
    if err.is_auth_error:
        return t('records.flash.forbidden')
    return t('records.flash.cloudflare_error', error=str(err))


def _current_ips():
    return target_ips(SentinelSettings.for_user(current_user.id))


def _render_form(zone, values, errors, record=None, status=200):
    return render_template('records/form.html', zone=zone, zone_id=zone.zone_id, record=record,
                           values=values, errors=errors, record_types=EDITABLE_TYPES,
                           ttl_choices=TTL_CHOICES), status


@records_bp.route('/<zone_id>/records/new', methods=['GET', 'POST'])
@login_required
def create_record(zone_id):
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()

    if request.method == 'GET':
        values = form_values()
        if request.args.get('type') in EDITABLE_TYPES:
            values['type'] = request.args['type']
        return _render_form(zone, values, {})

    values, payload, errors = parse_record_form(request.form, zone.name, current_ips=_current_ips)
    if errors:
        flash(t('records.flash.invalid_form'), 'danger')
        return _render_form(zone, values, errors, status=400)

    try:
        data = CloudflareClient(zone.api_token).create_dns_record(zone.zone_id, payload)
    except CloudflareError as err:
        flash(cloudflare_error_message(err), 'danger')
        return _render_form(zone, values, errors, status=400)

    record = Record(zone=zone, auto_update=values['auto_update'])
    record.update_from_cloudflare(data)
    db.session.add(record)
    db.session.commit()
    flash(t('records.flash.created', name=record.name), 'success')
    return redirect(url_for('records.detail_record', zone_id=zone.zone_id, record_id=record.record_id))


@records_bp.route('/<zone_id>/records/<record_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_record(zone_id, record_id):
    zone = Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first_or_404()
    record = Record.query.filter_by(record_id=record_id, zone_id_fk=zone.id).first_or_404()
    detail_url = url_for('records.detail_record', zone_id=zone.zone_id, record_id=record.record_id)

    if record.type not in EDITABLE_TYPES:
        flash(t('records.flash.not_editable', type=record.type), 'warning')
        return redirect(detail_url)

    if request.method == 'GET':
        return _render_form(zone, form_values(record, zone.name), {}, record)

    values, payload, errors = parse_record_form(request.form, zone.name, record_type=record.type,
                                                current_ips=_current_ips)
    if errors:
        flash(t('records.flash.invalid_form'), 'danger')
        return _render_form(zone, values, errors, record, status=400)

    try:
        data = CloudflareClient(zone.api_token).update_dns_record(zone.zone_id, record.record_id, payload)
    except CloudflareError as err:
        message = t('records.flash.missing_in_cloudflare') if err.is_not_found else cloudflare_error_message(err)
        flash(message, 'danger')
        return _render_form(zone, values, errors, record, status=400)

    record.auto_update = values['auto_update']
    record.update_from_cloudflare(data)
    db.session.commit()
    flash(t('records.flash.updated', name=record.name), 'success')
    return redirect(detail_url)
