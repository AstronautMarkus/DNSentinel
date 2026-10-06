import os
from app import create_app
from app.sentinel import start_sentinel

app = create_app()

if __name__ == '__main__':
    # In debug mode the reloader runs this file twice: a file watcher, and the
    # server itself (WERKZEUG_RUN_MAIN=true). Only the server runs the sentinel.
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        start_sentinel(app)
    app.run(debug=True, port=5010, host='0.0.0.0')
else:
    start_sentinel(app)
    gunicorn_app = app
