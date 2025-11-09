from flask import Flask
from app.config.config import Config
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.dashboard import dashboard_bp
from flask_login import LoginManager
from app.models.models import User, db

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    return app
