from flask import Blueprint

sentinel_bp = Blueprint('sentinel', __name__)

from . import overview, settings, check
