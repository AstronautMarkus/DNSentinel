from flask import Blueprint, render_template
from app.middleware.checkIsUserAuth import check_is_user_auth

base_bp = Blueprint('main', __name__)

@base_bp.route('/')
@check_is_user_auth
def index():
    return render_template('index.html')