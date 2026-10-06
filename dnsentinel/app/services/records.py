"""
DNS record form: the record types DNSentinel can create and edit, and the
validation that turns the submitted form into a Cloudflare API payload.
"""
import re

from app.models.models import DYNAMIC_RECORD_TYPES
from app.services.ip import InvalidIP, parse_ip

# Types with a plain `content` value. Others (SRV, CAA…) use a structured
# `data` object: they can be imported and deleted, but are edited in Cloudflare.
EDITABLE_TYPES = ('A', 'AAAA', 'CNAME', 'TXT', 'MX', 'NS')
PROXIABLE_TYPES = ('A', 'AAAA', 'CNAME')
HOSTNAME_TYPES = ('CNAME', 'MX', 'NS')

# Same choices as the Cloudflare dashboard; 1 means "Auto".
TTL_CHOICES = (1, 60, 120, 300, 600, 900, 1800, 3600, 7200, 18000, 43200, 86400)

MAX_TXT_LENGTH = 2048
MAX_COMMENT_LENGTH = 500

_LABEL = r'[A-Za-z0-9_](?:[A-Za-z0-9_-]{0,61}[A-Za-z0-9_])?'
NAME_RE = re.compile(rf'^\*$|^(?:\*\.)?(?:{_LABEL}\.)*{_LABEL}$')
HOSTNAME_RE = re.compile(rf'^(?:{_LABEL}\.)*{_LABEL}$')


def relative_name(name, zone_name):
    """'www.example.com' -> 'www', 'example.com' -> '@' (for the form)."""
    if not name or name == zone_name:
        return '@'
    suffix = '.' + zone_name
    return name[:-len(suffix)] if name.endswith(suffix) else name


def absolute_name(name, zone_name):
    """'www' -> 'www.example.com', '@' -> 'example.com'; full names are kept."""
    name = name.strip().rstrip('.').lower()
    if name in ('', '@') or name == zone_name:
        return zone_name
    if name.endswith('.' + zone_name):
        return name
    return f'{name}.{zone_name}'


def form_values(record=None, zone_name=''):
    """Initial form values: empty for a new record, the record's own when editing."""
    if record is None:
        return {'type': 'A', 'name': '', 'content': '', 'ttl': 1, 'proxied': False,
                'priority': '10', 'comment': '', 'auto_update': False}
    return {
        'type': record.type,
        'name': relative_name(record.name, zone_name),
        'content': record.content or '',
        'ttl': record.ttl or 1,
        'proxied': bool(record.proxied),
        'priority': '' if record.priority is None else str(record.priority),
        'comment': record.comment or '',
        'auto_update': bool(record.auto_update),
    }


def parse_record_form(form, zone_name, record_type=None, current_ips=None):
    """
    Validate a submitted record form.

    `record_type` fixes the type when editing (it can't change). `current_ips`
    is a callable returning (ipv4, ipv6), used to fill in the content of an
    auto-update record left empty.

    Returns (values, payload, errors): the values to re-render the form with,
    the Cloudflare API payload, and {field: i18n key} for invalid fields.
    """
    rtype = record_type or (form.get('type') or '').upper()
    values = {
        'type': rtype,
        'name': (form.get('name') or '').strip(),
        'content': (form.get('content') or '').strip(),
        'ttl': form.get('ttl', type=int, default=1),
        'proxied': form.get('proxied') == 'on',
        'priority': (form.get('priority') or '').strip(),
        'comment': (form.get('comment') or '').strip(),
        'auto_update': form.get('auto_update') == 'on',
    }
    errors = {}

    if rtype not in EDITABLE_TYPES:
        errors['type'] = 'records.form.error.type'
        return values, None, errors

    if rtype not in PROXIABLE_TYPES:
        values['proxied'] = False
    if rtype not in DYNAMIC_RECORD_TYPES:
        values['auto_update'] = False

    name = values['name'].rstrip('.')
    if not name:
        errors['name'] = 'records.form.error.required'
    elif name != '@' and (len(name) > 253 or not NAME_RE.match(name)):
        errors['name'] = 'records.form.error.name'

    content = values['content']
    if rtype in DYNAMIC_RECORD_TYPES:
        if not content and values['auto_update'] and current_ips:
            ipv4, ipv6 = current_ips()
            content = values['content'] = (ipv4 if rtype == 'A' else ipv6) or ''
            if not content:
                errors['content'] = 'records.form.error.no_current_ip'
        if content:
            try:
                content = values['content'] = parse_ip(content, 4 if rtype == 'A' else 6)
            except InvalidIP:
                errors['content'] = 'records.form.error.ipv4' if rtype == 'A' else 'records.form.error.ipv6'
        elif 'content' not in errors:
            errors['content'] = 'records.form.error.required'
    elif rtype in HOSTNAME_TYPES:
        content = content.rstrip('.').lower()
        if not content:
            errors['content'] = 'records.form.error.required'
        elif content != '@' and (len(content) > 253 or not HOSTNAME_RE.match(content)):
            errors['content'] = 'records.form.error.hostname'
    else:  # TXT
        if not content:
            errors['content'] = 'records.form.error.required'
        elif len(content) > MAX_TXT_LENGTH:
            errors['content'] = 'records.form.error.too_long'

    priority = None
    if rtype == 'MX':
        try:
            priority = int(values['priority'])
            if not 0 <= priority <= 65535:
                raise ValueError
        except ValueError:
            errors['priority'] = 'records.form.error.priority'

    ttl = values['ttl'] if values['ttl'] in TTL_CHOICES else 1
    if values['proxied']:
        ttl = 1  # proxied records always use Auto TTL
    values['ttl'] = ttl

    if len(values['comment']) > MAX_COMMENT_LENGTH:
        errors['comment'] = 'records.form.error.too_long'

    if errors:
        return values, None, errors

    payload = {
        'type': rtype,
        'name': absolute_name(name, zone_name),
        'content': content,
        'ttl': ttl,
    }
    # Editing sends an empty comment too, so clearing the field clears it in Cloudflare.
    if values['comment'] or record_type:
        payload['comment'] = values['comment']
    if rtype in PROXIABLE_TYPES:
        payload['proxied'] = values['proxied']
    if priority is not None:
        payload['priority'] = priority
    return values, payload, errors
