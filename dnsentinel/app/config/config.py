import os
from dotenv import load_dotenv

def _env_bool(name, default):
    value = os.getenv(name)
    return default if value is None else value.strip().lower() in ('1', 'true', 'yes', 'on')

class Config:
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env'))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dnsentinel-default-secret-key')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = os.getenv('MYSQL_PORT')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    # DATABASE_URL overrides the MySQL settings (e.g. sqlite:///dnsentinel.db).
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # The sentinel thread keeps connections open for days; drop the ones MySQL timed out.
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True, 'pool_recycle': 3600}
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Run the IP sentinel inside the web process (see app/sentinel/).
    SENTINEL_EMBEDDED = _env_bool('SENTINEL_EMBEDDED', True)
    # How often the sentinel looks for users whose check is due.
    SENTINEL_TICK_SECONDS = int(os.getenv('SENTINEL_TICK_SECONDS', '30'))
