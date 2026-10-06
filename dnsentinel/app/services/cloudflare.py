"""
Minimal Cloudflare API v4 client: only the zone and DNS record endpoints
DNSentinel uses. Authenticates with an API token (Bearer), and every call
raises CloudflareError on failure, carrying the HTTP status and the error
list Cloudflare returned.
"""
import re

import requests

API_BASE = 'https://api.cloudflare.com/client/v4'
TIMEOUT = 15
PAGE_SIZE = 500

# Zone and record identifiers are 32 lowercase hex characters.
_ID_RE = re.compile(r'^[0-9a-f]{32}$')


def is_cloudflare_id(value):
    return bool(value) and bool(_ID_RE.match(value))


class CloudflareError(Exception):
    def __init__(self, message, status=None, errors=None):
        super().__init__(message)
        # None when Cloudflare could not be reached at all.
        self.status = status
        self.errors = errors or []

    @property
    def codes(self):
        return {err.get('code') for err in self.errors}

    @property
    def is_auth_error(self):
        # 10000 "Authentication error" (token without the needed permission),
        # 6003/6111/9106/9109 malformed, unknown or expired token.
        return self.status in (401, 403) or bool(self.codes & {10000, 6003, 6111, 9106, 9109})

    @property
    def is_not_found(self):
        # 7003 "Could not route to …": the identifier in the URL does not exist.
        return self.status == 404 or bool(self.codes & {7000, 7003, 81044})


class CloudflareClient:
    def __init__(self, api_token):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        })

    def _request(self, method, path, **kwargs):
        try:
            resp = self.session.request(method, API_BASE + path, timeout=TIMEOUT, **kwargs)
        except requests.RequestException as exc:
            raise CloudflareError(str(exc)) from exc

        try:
            payload = resp.json()
        except ValueError:
            payload = {}

        if not resp.ok or not payload.get('success', False):
            errors = payload.get('errors') or []
            message = '; '.join(err.get('message', '') for err in errors if err.get('message'))
            raise CloudflareError(message or f'HTTP {resp.status_code}', status=resp.status_code, errors=errors)
        return payload

    # ---- Zones -------------------------------------------------------------

    def get_zone(self, zone_id):
        return self._request('GET', f'/zones/{zone_id}')['result']

    # ---- DNS records -------------------------------------------------------

    def dns_records_page(self, zone_id, page=1, per_page=PAGE_SIZE, **filters):
        """One page of DNS records: the raw payload, with `result` and `result_info`."""
        params = {'page': page, 'per_page': per_page, **filters}
        return self._request('GET', f'/zones/{zone_id}/dns_records', params=params)

    def list_dns_records(self, zone_id, **filters):
        """Every DNS record in the zone, following pagination. Filters: type=, name=, …"""
        records, page = [], 1
        while True:
            payload = self.dns_records_page(zone_id, page=page, **filters)
            records.extend(payload.get('result') or [])
            total_pages = (payload.get('result_info') or {}).get('total_pages') or 1
            if page >= total_pages:
                return records
            page += 1

    def get_dns_record(self, zone_id, record_id):
        return self._request('GET', f'/zones/{zone_id}/dns_records/{record_id}')['result']

    def create_dns_record(self, zone_id, data):
        return self._request('POST', f'/zones/{zone_id}/dns_records', json=data)['result']

    def update_dns_record(self, zone_id, record_id, data):
        """Partial update (PATCH): only the fields in `data` change."""
        return self._request('PATCH', f'/zones/{zone_id}/dns_records/{record_id}', json=data)['result']

    def delete_dns_record(self, zone_id, record_id):
        return self._request('DELETE', f'/zones/{zone_id}/dns_records/{record_id}')['result']
