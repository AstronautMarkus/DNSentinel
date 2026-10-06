from . import zones_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, Zone
import requests
from datetime import datetime
from app.i18n import t

@zones_bp.route('/cloudflare/create', methods=['GET', 'POST'])
@login_required
def create_zone():
    if request.method == 'POST':
        zone_id = request.form.get('zone_id')
        api_token = request.form.get('api_token')

        if not zone_id or not api_token:
            flash(t('zones.flash.missing_fields'), 'danger')
            return render_template('zones/create.html')

        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        try:
            resp = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            flash(t('zones.connection_error', error=str(e)), 'danger')
            return render_template('zones/create.html')

        if resp.status_code != 200:
            flash(t('zones.flash.invalid_credentials'), 'danger')
            return render_template('zones/create.html')

        data = resp.json().get('result', {})
        name = data.get('name')
        if not name:
            flash(t('zones.flash.no_name'), 'danger')
            return render_template('zones/create.html')

        if Zone.query.filter_by(name=name).first():
            flash(t('zones.flash.name_exists'), 'warning')
            return render_template('zones/create.html')
        if Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first():
            flash(t('zones.flash.id_exists'), 'warning')
            return render_template('zones/create.html')

        new_zone = Zone(
            name=name,
            status=data.get('status'),
            paused=data.get('paused', False),
            type=data.get('type'),
            development_mode=bool(data.get('development_mode', 0)),
            name_servers=data.get('name_servers'),
            original_name_servers=data.get('original_name_servers'),
            original_registrar=data.get('original_registrar'),
            original_dnshost=data.get('original_dnshost'),
            modified_on=datetime.fromisoformat(data['modified_on'].replace('Z', '+00:00')) if data.get('modified_on') else None,
            created_on=datetime.fromisoformat(data['created_on'].replace('Z', '+00:00')) if data.get('created_on') else None,
            zone_id=zone_id,
            api_token=api_token,
            user_id=current_user.id
        )
        db.session.add(new_zone)
        db.session.commit()
        flash(t('zones.flash.created'), 'success')
        return redirect(url_for('dashboard.home'))

    return render_template('zones/create.html')