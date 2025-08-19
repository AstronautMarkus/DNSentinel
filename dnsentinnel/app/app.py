from flask import Flask
from app.routes.base.routes import base_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(base_bp)
    return app
