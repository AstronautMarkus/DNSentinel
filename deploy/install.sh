#!/usr/bin/env bash
# Installs (or updates) DNSentinel as two systemd services on Linux:
#   dnsentinel-web       the dashboard (gunicorn on $BIND, put an HTTPS reverse proxy in front)
#   dnsentinel-sentinel  the IP sentinel
#
# Needs python3 (3.10+, with venv), a MySQL/MariaDB server and systemd. Run as root:
#   sudo deploy/install.sh
# Run it again after `git pull` to update: it upgrades the database and restarts both services.
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../dnsentinel" && pwd)"
SERVICE_USER="${SERVICE_USER:-dnsentinel}"
BIND="${BIND:-127.0.0.1:5010}"
WORKERS="${WORKERS:-2}"
PYTHON="$APP_DIR/.venv/bin/python"

die() { echo "Error: $*" >&2; exit 1; }
as_service() { runuser -u "$SERVICE_USER" -- "$@"; }

[[ $EUID -eq 0 ]] || die "run it as root: sudo $0"
command -v systemctl >/dev/null || die "systemd is required."
command -v python3 >/dev/null || die "python3 is required."
command -v mysql >/dev/null || command -v mariadb >/dev/null \
    || echo "Note: no MySQL client here. Fine if the database runs on another host."

cd "$APP_DIR"
id -u "$SERVICE_USER" >/dev/null 2>&1 \
    || useradd --system --home-dir "$APP_DIR" --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER"
as_service test -r "$APP_DIR/main.py" \
    || die "$SERVICE_USER cannot read $APP_DIR. Clone DNSentinel somewhere like /opt/DNSentinel."

echo "Installing Python packages..."
[[ -x "$PYTHON" ]] || python3 -m venv .venv || die "could not create the virtualenv (Debian/Ubuntu: apt install python3-venv)."
"$PYTHON" -m pip install --quiet --upgrade pip
"$PYTHON" -m pip install --quiet -r requirements.txt

# Settings, their key and the install token live here, readable only by the service.
install -d -m 700 -o "$SERVICE_USER" -g "$SERVICE_USER" config

write_unit() {  # name, description, ExecStart, extra [Service] lines
    cat > "/etc/systemd/system/$1.service" <<EOF
[Unit]
Description=$2
After=network-online.target mysql.service mariadb.service
Wants=network-online.target

[Service]
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$APP_DIR
ExecStart=$3
Environment=PYTHONUNBUFFERED=1
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
$4

[Install]
WantedBy=multi-user.target
EOF
}

write_unit dnsentinel-web "DNSentinel web dashboard" \
    "$APP_DIR/.venv/bin/gunicorn --workers $WORKERS --bind $BIND --access-logfile - main:app" \
    "ReadWritePaths=$APP_DIR/config"  # the web installer writes the settings
write_unit dnsentinel-sentinel "DNSentinel IP sentinel" "$PYTHON sentinel.py" ""

systemctl daemon-reload
systemctl enable --quiet dnsentinel-web dnsentinel-sentinel

if [[ -f config/config.json.enc ]]; then
    as_service "$PYTHON" app/scripts/init_db.py
    systemctl restart dnsentinel-web dnsentinel-sentinel
    echo "DNSentinel updated and restarted."
else
    systemctl restart dnsentinel-web dnsentinel-sentinel
    echo
    as_service "$PYTHON" manage.py install-token
    echo
    echo "DNSentinel is listening on $BIND. Point your HTTPS reverse proxy at it, open the site"
    echo "and finish the installer with the token above."
fi
