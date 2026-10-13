"""
WSGI entry point: `gunicorn main:app` (the dnsentinel-web service), or
`python main.py` for the development server.

Serves the web installer until DNSentinel is installed, then the app itself,
without a restart: every worker switches on its next request.
"""
import os
import threading

from app import create_app, create_installer
from app.config.config import is_installed
from app.sentinel import start_sentinel


class DNSentinel:
    def __init__(self):
        self.app = None
        self.installer = None
        self.lock = threading.Lock()

    def current(self):
        if self.app is None:
            with self.lock:
                if self.app is None:
                    if not is_installed():
                        self.installer = self.installer or create_installer()
                        return self.installer
                    self.app = create_app()
                    start_sentinel(self.app)
        return self.app

    def __call__(self, environ, start_response):
        return self.current()(environ, start_response)


app = DNSentinel()

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    # Flask reads it when the apps are created, on the first request.
    os.environ.setdefault('FLASK_DEBUG', '1')
    # The app is only built on a request, so the reloader's file watcher never runs the sentinel.
    run_simple('0.0.0.0', 5010, app, use_reloader=True, use_debugger=True, threaded=True)
