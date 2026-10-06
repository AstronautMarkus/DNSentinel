from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

# Record types the sentinel can keep pointed at a dynamic IP.
DYNAMIC_RECORD_TYPES = ('A', 'AAAA')


def utcnow():
    """Naive UTC timestamp: every DateTime column here stores UTC without tzinfo."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def parse_cloudflare_datetime(value):
    """Cloudflare timestamps ('2025-10-06T12:00:00.123Z') as naive UTC, or None."""
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    zones = db.relationship("Zone", back_populates="user", cascade="all, delete-orphan")
    sentinel = db.relationship("SentinelSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")

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
    created_at = db.Column(db.DateTime, default=utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", back_populates="zones")
    records = db.relationship("Record", back_populates="zone", cascade="all, delete-orphan")

    def update_from_cloudflare(self, data):
        """Mirror a Cloudflare zone (the API's `result` object) onto this row."""
        self.name = data.get('name') or self.name
        self.status = data.get('status')
        self.paused = bool(data.get('paused', False))
        self.type = data.get('type')
        self.development_mode = bool(data.get('development_mode', 0))
        self.name_servers = data.get('name_servers')
        self.original_name_servers = data.get('original_name_servers')
        self.original_registrar = data.get('original_registrar')
        self.original_dnshost = data.get('original_dnshost')
        self.modified_on = parse_cloudflare_datetime(data.get('modified_on'))
        self.created_on = parse_cloudflare_datetime(data.get('created_on'))

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
    # False once the record is no longer found in Cloudflare (sync or sentinel).
    active = db.Column(db.Boolean, default=True)
    # TXT records (DKIM keys…) go well past 255 characters.
    content = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, nullable=True)
    modified_on = db.Column(db.DateTime, nullable=True)
    settings = db.Column(db.JSON, nullable=True)
    tags = db.Column(db.JSON, nullable=True)
    # Kept pointed at the user's public IP by the sentinel (A / AAAA only).
    auto_update = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())

    created_at = db.Column(db.DateTime, default=utcnow)
    zone = db.relationship("Zone", back_populates="records")
    updates = db.relationship("Update", back_populates="record", cascade="all, delete-orphan")

    @property
    def supports_auto_update(self):
        return self.type in DYNAMIC_RECORD_TYPES

    def update_from_cloudflare(self, data):
        """Mirror a Cloudflare DNS record (the API's `result` object) onto this row."""
        self.record_id = data.get('id') or self.record_id
        self.name = data.get('name')
        self.type = data.get('type')
        self.content = data.get('content')
        self.proxied = bool(data.get('proxied', False))
        self.proxiable = bool(data.get('proxiable', True))
        self.ttl = data.get('ttl', 1)
        self.priority = data.get('priority')
        self.comment = data.get('comment')
        self.settings = data.get('settings')
        self.tags = data.get('tags')
        self.created_on = parse_cloudflare_datetime(data.get('created_on'))
        self.modified_on = parse_cloudflare_datetime(data.get('modified_on'))
        self.active = True
        if not self.supports_auto_update:
            self.auto_update = False

class Update(db.Model):
    """One sentinel change to a record: an IP update, or a failed attempt."""
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id_fk = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
    old_ip = db.Column(db.String(45), nullable=True)
    new_ip = db.Column(db.String(45), nullable=True)
    # 'updated' | 'failed'
    status = db.Column(db.String(20), nullable=False)
    # Failure reason: an i18n key (sentinel.reason.*) or Cloudflare's own message.
    response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=utcnow)

    record = db.relationship("Record", back_populates="updates")

class SentinelSettings(db.Model):
    """Per-user sentinel configuration, plus the outcome of its last run."""
    __tablename__ = 'sentinel_settings'

    IP_MODES = ('auto', 'manual')
    INTERVALS = (1, 2, 5, 10, 15, 30, 60)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    enabled = db.Column(db.Boolean, nullable=False, default=True, server_default=db.true())
    interval_minutes = db.Column(db.Integer, nullable=False, default=5, server_default='5')
    # 'auto': the public IP the ISP gives us, detected online. 'manual': the IPs below.
    ip_mode = db.Column(db.String(10), nullable=False, default='auto', server_default='auto')
    manual_ipv4 = db.Column(db.String(45), nullable=True)
    manual_ipv6 = db.Column(db.String(45), nullable=True)

    # IPs the records were pointed at on the last run.
    current_ipv4 = db.Column(db.String(45), nullable=True)
    current_ipv6 = db.Column(db.String(45), nullable=True)
    last_run_at = db.Column(db.DateTime, nullable=True)
    next_run_at = db.Column(db.DateTime, nullable=True)
    # 'ok' | 'error'
    last_status = db.Column(db.String(20), nullable=True)
    # An i18n key (sentinel.reason.*) or Cloudflare's own message.
    last_message = db.Column(db.Text, nullable=True)
    # {'checked': n, 'updated': n, 'failed': n, 'skipped': n}
    last_summary = db.Column(db.JSON, nullable=True)

    user = db.relationship("User", back_populates="sentinel")

    @classmethod
    def for_user(cls, user_id):
        """The user's settings, created with the defaults on first use."""
        settings = cls.query.filter_by(user_id=user_id).first()
        if settings is None:
            settings = cls(user_id=user_id, enabled=True, interval_minutes=5, ip_mode='auto')
            db.session.add(settings)
            db.session.commit()
        return settings

class SentinelLock(db.Model):
    """
    Single-row lease electing the process that runs the sentinel, so several
    processes (dev server, gunicorn workers, `python sentinel.py`) never
    update the same records at once. See app/sentinel/runner.py.
    """
    __tablename__ = 'sentinel_lock'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    owner = db.Column(db.String(128), nullable=True)
    heartbeat_at = db.Column(db.DateTime, nullable=True)
