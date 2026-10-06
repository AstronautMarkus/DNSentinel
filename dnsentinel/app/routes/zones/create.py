from . import zones_bp
from .validate import check_credentials
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, Zone
from app.i18n import t

@zones_bp.route('/cloudflare/create', methods=['GET', 'POST'])
@login_required
def create_zone():
    if request.method == 'POST':
        zone_id = (request.form.get('zone_id') or '').strip().lower()
        api_token = (request.form.get('api_token') or '').strip()

        if not zone_id or not api_token:
            flash(t('zones.flash.missing_fields'), 'danger')
            return render_template('zones/create.html')

        data, error = check_credentials(zone_id, api_token)
        if error:
            flash(error, 'danger')
            return render_template('zones/create.html')

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

        new_zone = Zone(zone_id=zone_id, api_token=api_token, user_id=current_user.id)
        new_zone.update_from_cloudflare(data)
        db.session.add(new_zone)
        db.session.commit()
        flash(t('zones.flash.created'), 'success')
        return redirect(url_for('zones.zone_detail', zone_id=zone_id))

    return render_template('zones/create.html')
