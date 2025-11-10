from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    zones = db.relationship("Zone", back_populates="user")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

class Zone(db.Model):
    __tablename__ = 'zones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    status = db.Column(db.String(50), nullable=True)
    paused = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(50), nullable=True)
    development_mode = db.Column(db.Boolean, default=False)
    name_servers = db.Column(db.JSON, nullable=True)
    original_name_servers = db.Column(db.JSON, nullable=True)
    original_registrar = db.Column(db.String(255), nullable=True)
    original_dnshost = db.Column(db.String(255), nullable=True)
    modified_on = db.Column(db.DateTime, nullable=True)
    created_on = db.Column(db.DateTime, nullable=True)
    zone_id = db.Column(db.String(255), nullable=False)
    api_token = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", back_populates="zones")
    records = db.relationship("Record", back_populates="zone")

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zone_id_fk = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    record_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    proxied = db.Column(db.Boolean, default=False)
    proxiable = db.Column(db.Boolean, default=True)
    ttl = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    content = db.Column(db.String(255), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, nullable=True)
    modified_on = db.Column(db.DateTime, nullable=True)
    settings = db.Column(db.JSON, nullable=True)
    tags = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    zone = db.relationship("Zone", back_populates="records")
    updates = db.relationship("Update", back_populates="record")

class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id_fk = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
    old_ip = db.Column(db.String(45), nullable=True)
    new_ip = db.Column(db.String(45), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    record = db.relationship("Record", back_populates="updates")
