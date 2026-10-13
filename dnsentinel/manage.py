"""
DNSentinel administration. Run it as the user that owns config/ (on a
server installed with deploy/install.sh: sudo -u dnsentinel .venv/bin/python manage.py ...).

    python manage.py install-token     # token for the web installer
    python manage.py config show       # print the decrypted settings
    python manage.py config edit       # edit them in $EDITOR; saved encrypted again
    python manage.py user EMAIL        # add a sign-in account, or reset its password

Restart DNSentinel after editing the settings:
    sudo systemctl restart dnsentinel-web dnsentinel-sentinel
"""
import argparse
import getpass
import json
import os
import pwd
import shlex
import subprocess
import sys
import tempfile

from app.config.config import CONFIG_DIR, flask_config, is_installed, load_settings, new_install_token, save_settings


def install_token(_):
    if is_installed():
        sys.exit('DNSentinel is already installed.')
    token = new_install_token()
    print(f'Install token: {token}')
    print('Open DNSentinel in your browser and paste it in the installer. It works once.')


def config_show(_):
    print(json.dumps(load_settings(), indent=2))


def config_edit(_):
    editor = shlex.split(os.environ.get('EDITOR', 'vi'))
    fd, path = tempfile.mkstemp(suffix='.json')  # 0600, removed below
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(load_settings(), f, indent=2)
        while True:
            subprocess.run([*editor, path], check=True)
            try:
                with open(path) as f:
                    settings = json.load(f)
                flask_config(settings)  # has what DNSentinel needs
                break
            except (ValueError, KeyError, TypeError, AttributeError) as exc:
                if input(f'Invalid settings ({exc!r}). Edit again? [Y/n] ').strip().lower() in ('n', 'no'):
                    sys.exit('Nothing was saved.')
        save_settings(settings)
        print('Saved. Restart DNSentinel to apply it: sudo systemctl restart dnsentinel-web dnsentinel-sentinel')
    finally:
        os.remove(path)


def user(args):
    from app import create_app
    from app.models.models import User

    with create_app().app_context():
        existing = User.query.filter_by(email=args.email).first()
        name = input(f'Name [{existing.name}]: ' if existing else 'Name: ').strip() or (existing.name if existing else '')
        if not name:
            sys.exit('A name is required.')
        password = getpass.getpass('Password: ')
        if len(password) < User.MIN_PASSWORD_LENGTH:
            sys.exit(f'The password needs at least {User.MIN_PASSWORD_LENGTH} characters.')
        if getpass.getpass('Repeat it: ') != password:
            sys.exit('The passwords do not match.')
        User.save_account(name, args.email, password)
        print(f'{"Updated" if existing else "Created"} {args.email}.')


def main():
    parser = argparse.ArgumentParser(description='DNSentinel administration.')
    commands = parser.add_subparsers(required=True)
    commands.add_parser('install-token', help='create a token for the web installer').set_defaults(run=install_token)
    config = commands.add_parser('config', help='show or edit the encrypted settings').add_subparsers(required=True)
    config.add_parser('show').set_defaults(run=config_show)
    config.add_parser('edit').set_defaults(run=config_edit)
    user_parser = commands.add_parser('user', help='add a sign-in account, or reset its password')
    user_parser.add_argument('email')
    user_parser.set_defaults(run=user)
    args = parser.parse_args()

    # Files written as anyone else (root) would be unreadable by the services.
    if os.path.isdir(CONFIG_DIR) and os.stat(CONFIG_DIR).st_uid != os.getuid():
        owner = pwd.getpwuid(os.stat(CONFIG_DIR).st_uid).pw_name
        sys.exit(f'Run this as {owner}, who owns {CONFIG_DIR}:\n  sudo -u {owner} {sys.executable} {shlex.join(sys.argv)}')

    try:
        args.run(args)
    except RuntimeError as exc:  # not installed, or settings that cannot be decrypted
        sys.exit(str(exc))


if __name__ == '__main__':
    main()
