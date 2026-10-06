from flask import Flask
from app.config.config import Config
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.dashboard import dashboard_bp
from app.routes.zones import zones_bp
from app.routes.records import records_bp
from app.routes.sentinel import sentinel_bp
from flask_login import LoginManager
from app.models.models import User, db
from app.i18n import init_i18n, t

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'auth.flash.login_required'
    login_manager.login_message_category = 'info'
    login_manager.localize_callback = t

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    init_i18n(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(zones_bp, url_prefix='/dashboard/zones')
    app.register_blueprint(records_bp, url_prefix='/dashboard')
    app.register_blueprint(sentinel_bp, url_prefix='/dashboard/sentinel')

    return app
