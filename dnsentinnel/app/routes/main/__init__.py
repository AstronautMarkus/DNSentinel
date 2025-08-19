from flask import Blueprint

main_bp = Blueprint('main', __name__)

from .index import add_index_route

add_index_route(main_bp)

