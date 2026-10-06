from . import sentinel_bp
from .overview import render_overview
from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, SentinelSettings
from app.services.ip import InvalidIP, parse_public_ip
from app.i18n import t


@sentinel_bp.route('/settings', methods=['POST'])
@login_required
def save_settings():
    settings = SentinelSettings.for_user(current_user.id)
    form = {
        'enabled': request.form.get('enabled') == 'on',
        'interval_minutes': request.form.get('interval_minutes', type=int),
        'ip_mode': request.form.get('ip_mode'),
        'manual_ipv4': (request.form.get('manual_ipv4') or '').strip(),
        'manual_ipv6': (request.form.get('manual_ipv6') or '').strip(),
    }
    errors = {}

    if form['interval_minutes'] not in SentinelSettings.INTERVALS:
        errors['interval_minutes'] = 'sentinel.settings.error.interval'
    if form['ip_mode'] not in SentinelSettings.IP_MODES:
        form['ip_mode'] = 'auto'

    # Manual IPs are validated even in automatic mode, so whatever is stored is usable.
    for field, version in (('manual_ipv4', 4), ('manual_ipv6', 6)):
        if form[field]:
            try:
                form[field] = parse_public_ip(form[field], version)
            except InvalidIP as err:
                errors[field] = f'sentinel.ip_error.{err.reason}'
    if form['ip_mode'] == 'manual' and not (form['manual_ipv4'] or form['manual_ipv6']):
        errors['manual_ipv4'] = 'sentinel.ip_error.required'

    if errors:
        flash(t('sentinel.flash.invalid'), 'danger')
        return render_overview(settings, form, errors, status=400)

    settings.enabled = form['enabled']
    settings.interval_minutes = form['interval_minutes']
    settings.ip_mode = form['ip_mode']
    settings.manual_ipv4 = form['manual_ipv4'] or None
    settings.manual_ipv6 = form['manual_ipv6'] or None
    settings.next_run_at = None  # apply the new settings on the next tick
    db.session.commit()
    flash(t('sentinel.flash.saved'), 'success')
    return redirect(url_for('sentinel.overview'))
