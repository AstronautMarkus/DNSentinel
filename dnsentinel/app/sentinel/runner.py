"""
The background loop that runs the sentinel on schedule.

Every SENTINEL_TICK_SECONDS the runner renews a lease in `sentinel_lock`
and runs the check for each user whose next run is due. The lease makes
sure a single process does the work even when several run the app (the
dev server plus `python sentinel.py`, or several gunicorn workers): the
others wait, and take over if the holder stops renewing it.
"""
import atexit
import logging
import os
import socket
import threading
import uuid
from datetime import timedelta

from sqlalchemy.exc import IntegrityError

from app.models.models import db, utcnow, Record, SentinelLock, SentinelSettings, Zone
from app.services.ip import detect_public_ips
from .engine import run_check

log = logging.getLogger('dnsentinel.sentinel')

LEASE_ID = 1


def configure_logging():
    if log.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s [sentinel] %(levelname)s %(message)s'))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False


def acquire_lease(owner, ttl):
    """Take or renew the lease. True if `owner` holds it now."""
    now = utcnow()
    lease = db.session.get(SentinelLock, LEASE_ID, with_for_update=True)
    if lease is None:
        db.session.add(SentinelLock(id=LEASE_ID, owner=owner, heartbeat_at=now))
        try:
            db.session.commit()
            return True
        except IntegrityError:  # another process created it first
            db.session.rollback()
            return False

    held_by_other = lease.owner != owner and lease.heartbeat_at and now - lease.heartbeat_at < ttl
    if held_by_other:
        db.session.rollback()  # release the row lock
        return False
    lease.owner, lease.heartbeat_at = owner, now
    db.session.commit()
    return True


def release_lease(owner):
    lease = db.session.get(SentinelLock, LEASE_ID)
    if lease and lease.owner == owner:
        lease.owner, lease.heartbeat_at = None, None
        db.session.commit()


def lease_heartbeat():
    """When the running sentinel last checked in, or None if none ever did."""
    lease = db.session.get(SentinelLock, LEASE_ID)
    return lease.heartbeat_at if lease and lease.owner else None


def run_due_checks(force=False, renew=None):
    """
    One scheduler tick: run every enabled user whose check is due (all of
    them with `force`). `renew` is called between users and returns False
    if the lease was lost. Returns the list of (user_id, CheckResult).
    """
    now = utcnow()
    user_ids = [uid for (uid,) in (db.session.query(Zone.user_id).join(Record)
                                   .filter(Record.auto_update.is_(True)).distinct())]
    due = []
    for user_id in user_ids:
        settings = SentinelSettings.for_user(user_id)
        if settings.enabled and (force or settings.next_run_at is None or settings.next_run_at <= now):
            due.append(settings)
    if not due:
        return []

    # One fresh lookup, shared by every user on automatic detection.
    detected = detect_public_ips(max_age=0) if any(s.ip_mode == 'auto' for s in due) else None
    results = []
    for settings in due:
        if renew and not renew():
            break
        try:
            result = run_check(settings, detected)
        except Exception:
            db.session.rollback()
            log.exception('Check failed for user %s', settings.user_id)
            continue
        results.append((settings.user_id, result))
        log.info('user %s: %s checked, %s updated, %s failed, %s skipped (IPv4 %s, IPv6 %s)%s',
                 settings.user_id, result.checked, result.updated, result.failed, result.skipped,
                 result.ipv4 or '-', result.ipv6 or '-',
                 f' — {result.message}' if result.message else '')
    return results


class SentinelRunner:
    def __init__(self, app, tick_seconds=None):
        self.app = app
        self.tick = tick_seconds or app.config['SENTINEL_TICK_SECONDS']
        self.owner = f'{socket.gethostname()}:{os.getpid()}:{uuid.uuid4().hex[:8]}'
        self._stop = threading.Event()
        self._thread = None

    @property
    def lease_ttl(self):
        return timedelta(seconds=self.tick * 3)

    def run_once(self, force=False):
        """One tick. Returns the results, or None if another process holds the lease."""
        with self.app.app_context():
            renew = lambda: acquire_lease(self.owner, self.lease_ttl)
            if not renew():
                return None
            return run_due_checks(force=force, renew=renew)

    def release(self):
        """Hand the lease back, so another process can take over right away."""
        with self.app.app_context():
            release_lease(self.owner)

    def run_forever(self):
        log.info('Sentinel started (%s), checking every %ss', self.owner, self.tick)
        while not self._stop.is_set():
            try:
                self.run_once()
            except Exception:
                log.exception('Sentinel tick failed')
            self._stop.wait(self.tick)
        try:
            self.release()
        except Exception:
            log.exception('Could not release the sentinel lease')
        log.info('Sentinel stopped')

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self.run_forever, name='dnsentinel-sentinel', daemon=True)
        self._thread.start()
        # Hand the lease back on a clean exit, so a restarted process takes over at once.
        atexit.register(self.stop, 5)

    def stop(self, timeout=None):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout)
