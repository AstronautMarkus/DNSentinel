# DNSentinel
Autonomous Cloudflare DNS manager with dashboard and automated updates.

Connect a Cloudflare zone, manage its DNS records, and turn on **auto-update** for the
A/AAAA records that should follow your home connection. The **IP sentinel** checks every
few minutes and points them at your current public IP whenever your ISP changes it.

## Install (Linux, systemd)

You need Python 3.10+ (with `venv`), MySQL or MariaDB, systemd, and a reverse proxy for
HTTPS (nginx, Caddy…).

1. Create an empty database and a user for it:

   ```sql
   CREATE DATABASE dnsentinel CHARACTER SET utf8mb4;
   CREATE USER 'dnsentinel'@'localhost' IDENTIFIED BY 'a-strong-password';
   GRANT ALL PRIVILEGES ON dnsentinel.* TO 'dnsentinel'@'localhost';
   ```

2. Clone DNSentinel and run the deploy script as root:

   ```bash
   sudo git clone https://github.com/AstronautMarkus/DNSentinel.git /opt/DNSentinel
   sudo /opt/DNSentinel/deploy/install.sh
   ```

   It creates a `dnsentinel` system user, a virtualenv and two services,
   `dnsentinel-web` (the dashboard, on `127.0.0.1:5010`) and `dnsentinel-sentinel`
   (the IP sentinel), and prints an **install token**. `BIND`, `WORKERS` and
   `SERVICE_USER` change the defaults: `sudo BIND=127.0.0.1:8080 deploy/install.sh`.

3. Point your reverse proxy at `127.0.0.1:5010`, open the site and finish the installer:
   the token, the database and your account. There is no sign-up page, so nobody else can
   create an account, and without the token nobody else can install it either. Install
   over HTTPS and the session cookies are marked secure.

To update: `cd /opt/DNSentinel && sudo git pull && sudo deploy/install.sh`. It upgrades
the database and restarts both services. Logs: `journalctl -u dnsentinel-web -u dnsentinel-sentinel`.

## Settings

The installer saves them encrypted in `dnsentinel/config/config.json.enc`, with the key
in `dnsentinel/config/secret.key`. Back up both. Manage them as the service user:

```bash
cd /opt/DNSentinel/dnsentinel
sudo -u dnsentinel .venv/bin/python manage.py config show
sudo -u dnsentinel .venv/bin/python manage.py config edit    # in $EDITOR, saved encrypted again
sudo systemctl restart dnsentinel-web dnsentinel-sentinel    # apply the changes
```

| Key | |
|-----|---|
| `database` | `host`, `port`, `name`, `user`, `password` |
| `secret_key` | Signs the session cookies. Changing it signs everyone out. |
| `secure_cookies` | Send cookies over HTTPS only. On when installed over HTTPS. |
| `sentinel.embedded` | Also run the sentinel inside the web app (off: the service runs it). |
| `sentinel.tick_seconds` | How often the sentinel looks for users whose check is due. |

Accounts are added, or their password reset, from the command line:

```bash
sudo -u dnsentinel .venv/bin/python manage.py user someone@example.com
```

## Development

```bash
cd dnsentinel
pip install -r requirements.txt
python manage.py install-token   # then open http://localhost:5010 and use it
python main.py                   # dashboard (and installer) on port 5010
python sentinel.py               # the IP sentinel, in another terminal
python -m unittest discover tests
```

After pulling changes, `python app/scripts/init_db.py` adds the new tables and columns
(the deploy script does it for you). It never drops data; `--reset` / `--fresh` drop
everything.

## Cloudflare API token

In Cloudflare, go to **My Profile → API Tokens → Create Token** and give it, for the zone
you want to manage:

- **Zone → Zone → Read**
- **Zone → DNS → Edit**

Add the zone in DNSentinel with its Zone ID (on the zone's Overview page) and the token.
DNSentinel checks both permissions before saving it, and **Test connection** / **Replace
token** on the zone page check it again later.

## IP sentinel

1. Open a zone's DNS records and turn on **Auto-update** for A and AAAA records
   (or create a new record with it on and leave the address empty).
2. In **IP sentinel**, choose the IP to use: your ISP's public IP, detected online on every
   check, or a fixed one. Only public addresses are accepted (no LAN or CG-NAT ranges).
3. Pick the frequency (1–60 minutes). On every check the sentinel compares each record *in
   Cloudflare* with your IP and updates the ones that differ, so a record edited by hand in
   the Cloudflare dashboard is put back too. Changes and failures show up in **Activity**.

The `dnsentinel-sentinel` service runs it. To run it by hand:

```bash
python sentinel.py          # loop forever
python sentinel.py --once   # one check for every enabled user, then exit (cron)
```

Set `sentinel.embedded` to `true` to also run it inside the web app. Running both is safe:
a lease in the database makes sure only one process does the work.
