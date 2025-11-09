from . import zones_bp
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from ...models.models import db, Zone
import requests

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

@zones_bp.route('/validate', methods=['POST'])
def validate_zone():
    data = request.json
    zone_id = data.get('zone_id')
    api_token = data.get('api_token')
    if not zone_id or not api_token:
        return jsonify({'ok': False, 'msg': 'Missing data. Please complete all fields.'}), 400

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Connection error with Cloudflare: {str(e)}'}), 500

    if resp.status_code == 200:
        return jsonify({'ok': True, 'msg': 'Zone and token are valid! You can continue with the creation.'})
    elif resp.status_code == 403:
        return jsonify({'ok': False, 'msg': 'The token is valid, but does not have permission to access this zone. Check the permissions in Cloudflare.'})
    elif resp.status_code == 404:
        return jsonify({'ok': False, 'msg': 'The Zone ID does not exist or is not accessible with this token. Please check that the Zone ID is correct.'})
    elif resp.status_code == 401:
        return jsonify({'ok': False, 'msg': 'The token is invalid or expired. Generate a new token in Cloudflare.'})
    else:
        return jsonify({'ok': False, 'msg': f'Unexpected error: {resp.status_code}'}), 400