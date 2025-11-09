from . import zones_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ...models.models import db, Zone

@zones_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_zone():
    if request.method == 'POST':
        name = request.form.get('name')
        zone_id = request.form.get('zone_id')
        api_token = request.form.get('api_token')

        if not name or not zone_id or not api_token:
            flash('All fields are required.', 'danger')
            return render_template('zones/create.html')

        if Zone.query.filter_by(name=name).first():
            flash('A zone with that name already exists.', 'warning')
            return render_template('zones/create.html')

        if Zone.query.filter_by(zone_id=zone_id, user_id=current_user.id).first():
            flash('You already have a zone registered with that Zone ID.', 'warning')
            return render_template('zones/create.html')

        new_zone = Zone(
            name=name,
            zone_id=zone_id,
            api_token=api_token,
            user_id=current_user.id
        )
        db.session.add(new_zone)
        db.session.commit()
        flash('Zone created successfully.', 'success')
        return redirect(url_for('dashboard.home'))

    return render_template('zones/create.html')