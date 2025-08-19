from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import Config
from app.models.user import User, Base
from app.routes.auth.routes import auth_bp as auth_views
from app.routes.base.routes import base_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(base_bp)
    app.register_blueprint(auth_views)

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.config['engine'] = engine
    app.config['SessionLocal'] = SessionLocal
    return app
