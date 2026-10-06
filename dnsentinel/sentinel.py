"""
Run the DNSentinel IP sentinel on its own, without the web dashboard.

    python sentinel.py           # loop forever (systemd, launchd, Docker…)
    python sentinel.py --once    # check every enabled user now, then exit (cron)

The web app (main.py) also runs the sentinel in a background thread unless
SENTINEL_EMBEDDED=false; a database lease keeps the two from doubling up.
"""
import argparse
import signal
import sys

from app import create_app
from app.sentinel import SentinelRunner, configure_logging


def main():
    parser = argparse.ArgumentParser(description='Keep Cloudflare DNS records pointed at your public IP.')
    parser.add_argument('--once', action='store_true', help='run one check for every enabled user and exit')
    args = parser.parse_args()

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
