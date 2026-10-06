# DNSentinel
Autonomous Cloudflare DNS manager with dashboard and automated updates.

Connect a Cloudflare zone, manage its DNS records, and turn on **auto-update** for the
A/AAAA records that should follow your home connection. The **IP sentinel** checks every
few minutes and points them at your current public IP whenever your ISP changes it.

## Setup

```bash
cd dnsentinel
cp .env.example .env            # MySQL credentials, SECRET_KEY, sentinel options
pip install -r requirements.txt
python app/scripts/init_db.py   # creates tables; run it again after every update
python main.py                  # http://localhost:5010
```

`init_db.py` only adds what's missing (tables, columns), so it's safe to run on a database
that already has data. `--reset` / `--fresh` drop everything.

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

The sentinel runs inside the web app by default. To run it on its own (e.g. as a service,
with the dashboard stopped):

```bash
python sentinel.py          # loop forever (systemd, launchd, Docker…)
python sentinel.py --once   # one check for every enabled user, then exit (cron)
```

Running both is safe: a lease in the database makes sure only one process does the work.
Set `SENTINEL_EMBEDDED=false` if you prefer the web app never to run it.
