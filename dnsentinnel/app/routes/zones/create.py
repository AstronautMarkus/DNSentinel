from . import zones_bp
from flask import render_template, request

@zones_bp.route('/create', methods=['GET', 'POST'])
def create_zone():
    if request.method == 'POST':
        pass
    return render_template('zones/create.html')