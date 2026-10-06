"""
The sentinel pass for one user: work out the IPs their records should point
at, compare them with what Cloudflare actually serves, and patch whatever
drifted. Used by the background runner (runner.py) and by "Check now".

Comparing against Cloudflare (not the local copy) means a record edited by
hand in the Cloudflare dashboard is put back on the next pass as well.
"""
from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta

from app.models.models import db, utcnow, Record, Update, Zone
from app.services.cloudflare import CloudflareClient, CloudflareError
from app.services.ip import detect_public_ips, same_ip


@dataclass
class CheckResult:
    ipv4: str | None = None
    ipv6: str | None = None
    checked: int = 0
    updated: int = 0
    failed: int = 0
    # Records whose IP family has no address (e.g. AAAA without IPv6).
    skipped: int = 0
    # Why the whole pass could not run, or the last record failure.
    message: str | None = None
    fatal: bool = False

    @property
    def status(self):
        return 'error' if self.fatal or self.failed else 'ok'

    def summary(self):
        return {'checked': self.checked, 'updated': self.updated, 'failed': self.failed, 'skipped': self.skipped}


def target_ips(settings, detected=None):
    """(ipv4, ipv6) the user's records should point at; None for a family without one."""
    if settings.ip_mode == 'manual':
        return settings.manual_ipv4 or None, settings.manual_ipv6 or None
    detected = detected or detect_public_ips()
    return detected.ipv4, detected.ipv6


def watched_records(user_id):
    return (Record.query.join(Zone)
            .filter(Zone.user_id == user_id, Record.auto_update.is_(True))
            .order_by(Zone.name, Record.name, Record.type)
            .all())


def run_check(settings, detected=None):
    """Run one pass for `settings.user_id`, record the outcome on `settings` and commit."""
    result = CheckResult()
    result.ipv4, result.ipv6 = target_ips(settings, detected)

    if not (result.ipv4 or result.ipv6):
        # Never touch records when we don't know where they should point.
        result.fatal = True
        result.message = 'sentinel.reason.no_ip' if settings.ip_mode == 'auto' else 'sentinel.reason.no_manual_ip'
    else:
        by_zone = defaultdict(list)
        for record in watched_records(settings.user_id):
            by_zone[record.zone].append(record)
        for zone, records in by_zone.items():
            _check_zone(zone, records, result)

    now = utcnow()
    settings.last_run_at = now
    settings.next_run_at = now + timedelta(minutes=settings.interval_minutes)
    settings.current_ipv4, settings.current_ipv6 = result.ipv4, result.ipv6
    settings.last_status = result.status
    settings.last_message = result.message
    settings.last_summary = result.summary()
    db.session.commit()
    return result


def _check_zone(zone, records, result):
    client = CloudflareClient(zone.api_token)
    try:
        # One list call per record type instead of one GET per record.
        remote = {}
        for rtype in sorted({record.type for record in records}):
            remote.update({r['id']: r for r in client.list_dns_records(zone.zone_id, type=rtype)})
    except CloudflareError as err:
        for record in records:
            result.checked += 1
            _log_failure(record, record.content, None, _reason(err), result)
        return

    for record in records:
        result.checked += 1
        target = result.ipv4 if record.type == 'A' else result.ipv6
        if not target:
            result.skipped += 1
            continue

        current = remote.get(record.record_id)
        if current is None:
            record.active = False
            _log_failure(record, record.content, target, 'sentinel.reason.record_missing', result)
            continue

        if same_ip(current.get('content'), target):
            record.update_from_cloudflare(current)
            continue

        try:
            updated = client.update_dns_record(zone.zone_id, record.record_id, {'content': target})
        except CloudflareError as err:
            record.update_from_cloudflare(current)
            _log_failure(record, current.get('content'), target, _reason(err), result)
            continue

        record.update_from_cloudflare(updated)
        db.session.add(Update(record=record, old_ip=current.get('content'), new_ip=target, status='updated'))
        result.updated += 1


def _reason(err):
    if err.status is None:
        return 'sentinel.reason.unreachable'
    if err.is_auth_error:
        return 'sentinel.reason.forbidden'
    return str(err)


def _log_failure(record, old_ip, new_ip, reason, result):
    result.failed += 1
    result.message = reason
    # A broken token fails every few minutes; log it once, not on every pass.
    last = (Update.query.filter_by(record_id_fk=record.id)
            .order_by(Update.timestamp.desc(), Update.id.desc()).first()) if record.id else None
    if last and last.status == 'failed' and last.response == reason:
        return
    db.session.add(Update(record=record, old_ip=old_ip, new_ip=new_ip, status='failed', response=reason))
