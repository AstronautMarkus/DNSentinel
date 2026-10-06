from flask import Blueprint

records_bp = Blueprint('records', __name__)

from . import form, list, cloudflare, import_record, detail, manage