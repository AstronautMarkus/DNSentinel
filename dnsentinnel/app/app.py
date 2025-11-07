from flask import Flask

from app.config.config import Config
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['engine'] = Config.engine
    app.config['SessionLocal'] = Config.SessionLocal
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    
    return app
