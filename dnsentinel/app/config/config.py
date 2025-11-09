import os
from dotenv import load_dotenv

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dnsentinnel-default-secret-key')
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env'))
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = os.getenv('MYSQL_PORT')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False