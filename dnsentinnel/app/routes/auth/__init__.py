from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from .login import add_login_route
from .logout import add_logout_route
from .register import add_register_route

add_login_route(auth_bp)
add_logout_route(auth_bp)
add_register_route(auth_bp)
