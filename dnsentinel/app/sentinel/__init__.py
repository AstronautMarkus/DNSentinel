"""
The IP sentinel: keeps every auto-update A/AAAA record pointed at the
user's public IP. engine.py does one pass, runner.py schedules them.
"""
from .engine import run_check, target_ips, watched_records
from .runner import SentinelRunner, configure_logging, lease_heartbeat


def start_sentinel(app):
    """Run the sentinel in a background thread of this process, unless SENTINEL_EMBEDDED is off."""
    if not app.config['SENTINEL_EMBEDDED']:
        return None
    runner = app.extensions.get('dnsentinel.sentinel')
    if runner is None:
        configure_logging()
        runner = app.extensions['dnsentinel.sentinel'] = SentinelRunner(app)
    runner.start()
    return runner
