"""
The web installer end to end, on SQLite in a temporary config dir.

    cd dnsentinel && python -m unittest discover tests
"""
import os
import tempfile
import unittest
from unittest import mock

from werkzeug.test import Client

from app.config import config


class InstallTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.db_file = os.path.join(tmp.name, 'test.db')
        for patch in (
            mock.patch.object(config, 'CONFIG_DIR', os.path.join(tmp.name, 'config')),
            mock.patch.object(config, 'database_url', lambda database: f'sqlite:///{self.db_file}'),
        ):
            patch.start()
            self.addCleanup(patch.stop)

        import main
        self.client = Client(main.DNSentinel())
        self.form = {
            'db_host': 'localhost', 'db_port': '3306', 'db_name': 'dnsentinel', 'db_user': 'dnsentinel',
            'db_password': 'db-secret-pw', 'name': 'Admin', 'email': 'admin@example.com', 'password': 'admin-pw-123',
        }

    def test_install(self):
        # Every page leads to the installer, which wants a token first.
        self.assertEqual(self.client.get('/auth/login').headers['Location'], '/install')
        self.assertIn(b'manage.py install-token', self.client.get('/install').data)

        token = config.new_install_token()
        bad = self.client.post('/install', data={**self.form, 'token': 'guess'})
        self.assertEqual(bad.status_code, 200)
        self.assertFalse(config.is_installed())

        short = self.client.post('/install', data={**self.form, 'token': token, 'password': 'short'})
        self.assertEqual(short.status_code, 200)
        self.assertFalse(config.is_installed())

        done = self.client.post('/install', data={**self.form, 'token': token})
        self.assertEqual(done.headers['Location'], '/auth/login')
        self.assertTrue(config.is_installed())
        self.assertFalse(config.has_install_token())

        # Encrypted at rest, and read back as written.
        with open(config._path(config.CONFIG_FILE), 'rb') as f:
            self.assertNotIn(b'db-secret-pw', f.read())
        settings = config.load_settings()
        self.assertEqual(settings['database']['password'], 'db-secret-pw')
        self.assertFalse(settings['sentinel']['embedded'])

        # The app takes over: no installer, no sign-up, and the account works.
        self.assertEqual(self.client.get('/install').status_code, 404)
        self.assertEqual(self.client.get('/auth/register').status_code, 404)
        wrong = self.client.post('/auth/login', data={'email': 'admin@example.com', 'password': 'nope'})
        self.assertEqual(wrong.status_code, 200)
        login = self.client.post('/auth/login', data={'email': 'admin@example.com', 'password': 'admin-pw-123'})
        self.assertEqual(login.headers['Location'], '/dashboard/home')


class DatabaseUrlTest(unittest.TestCase):
    def test_escapes_credentials(self):
        url = config.database_url({'host': 'db', 'port': '3306', 'name': 'dns', 'user': 'u', 'password': 'p@ss:/word'})
        self.assertEqual(url, 'mysql+pymysql://u:p%40ss%3A%2Fword@db:3306/dns')


if __name__ == '__main__':
    unittest.main()
