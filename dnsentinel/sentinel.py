"""
Run the DNSentinel IP sentinel on its own, without the web dashboard.

    python sentinel.py           # loop forever (the dnsentinel-sentinel service)
    python sentinel.py --once    # check every enabled user now, then exit (cron)

The web app (main.py) can also run it in a background thread when the
config's sentinel.embedded is true; a database lease keeps the two from
doubling up.
"""
import argparse
import signal
import sys
import time

from app import create_app
from app.config.config import is_installed
from app.sentinel import SentinelRunner, configure_logging


def main():
    parser = argparse.ArgumentParser(description='Keep Cloudflare DNS records pointed at your public IP.')
    parser.add_argument('--once', action='store_true', help='run one check for every enabled user and exit')
    args = parser.parse_args()

    if not is_installed():
        if args.once:
            print('DNSentinel is not installed yet: open the web installer first.')
            return 1
        # The service starts with the web one, before anyone has gone through the installer.
        print('DNSentinel is not installed yet; waiting for the web installer...', flush=True)
        while not is_installed():
            time.sleep(10)

    configure_logging()
    runner = SentinelRunner(create_app())

    if args.once:
        results = runner.run_once(force=True)
        runner.release()
        if results is None:
            print('Another process holds the sentinel lease; nothing was checked.')
            return 1
        if not results:
            print('No enabled user has auto-update records.')
        return 1 if any(result.status == 'error' for _, result in results) else 0

    # Stop between ticks, so the lease is handed back before exiting.
    for signum in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signum, lambda *_: runner.stop())
    runner.run_forever()
    return 0


if __name__ == '__main__':
    sys.exit(main())
