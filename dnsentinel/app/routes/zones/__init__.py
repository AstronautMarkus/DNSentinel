from flask import Blueprint

zones_bp = Blueprint('zones', __name__)

from . import create, validate, list