"""
Public IP detection and validation.

detect_public_ips() asks a few "what is my IP" services, in order, until one
answers with a valid public address of the right family, once for IPv4 and
once for IPv6. Results are cached briefly so the dashboard, the forms and
the sentinel share one lookup.
"""
import ipaddress
import threading
import time
from dataclasses import dataclass
from urllib.parse import urlsplit

import requests

PROVIDERS = {
    4: ('https://api.ipify.org', 'https://ipv4.icanhazip.com', 'https://checkip.amazonaws.com'),
    6: ('https://api6.ipify.org', 'https://ipv6.icanhazip.com'),
}
TIMEOUT = 5
CACHE_SECONDS = 60
# A failed lookup is retried sooner, so a connection that comes back shows up quickly.
FAILURE_CACHE_SECONDS = 15


@dataclass(frozen=True)
class DetectedIPs:
    ipv4: str | None
    ipv6: str | None
    # Host of the service that answered, shown in the UI.
    ipv4_source: str | None
    ipv6_source: str | None
    detected_at: float


class InvalidIP(ValueError):
    """`reason` is the suffix of a `sentinel.ip_error.*` i18n key."""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def parse_ip(value, version):
    """Normalized `value` if it is an IP of the given family (4 or 6), else InvalidIP."""
    try:
        ip = ipaddress.ip_address((value or '').strip())
    except ValueError:
        raise InvalidIP('invalid') from None
    if ip.version != version:
        raise InvalidIP('wrong_family')
    return str(ip)


def parse_public_ip(value, version):
    """Like parse_ip, but also rejects private, CG-NAT and other non-routable ranges."""
    normalized = parse_ip(value, version)
    if not ipaddress.ip_address(normalized).is_global:
        raise InvalidIP('not_public')
    return normalized


def same_ip(a, b):
    """True if both are the same address, whatever the notation (IPv6 compression…)."""
    try:
        return ipaddress.ip_address((a or '').strip()) == ipaddress.ip_address((b or '').strip())
    except ValueError:
        return False


def _ask(version):
    for url in PROVIDERS[version]:
        try:
            resp = requests.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            return parse_public_ip(resp.text, version), urlsplit(url).hostname
        except (requests.RequestException, InvalidIP):
            continue
    return None, None


_cache = None
_cache_lock = threading.Lock()


def detect_public_ips(max_age=CACHE_SECONDS):
    """The public IPv4/IPv6 this machine reaches the Internet with (None if unavailable)."""
    global _cache
    with _cache_lock:
        if _cache:
            ttl = max_age if (_cache.ipv4 or _cache.ipv6) else min(max_age, FAILURE_CACHE_SECONDS)
            if time.monotonic() - _cache.detected_at < ttl:
                return _cache
        ipv4, ipv4_source = _ask(4)
        ipv6, ipv6_source = _ask(6)
        _cache = DetectedIPs(ipv4, ipv6, ipv4_source, ipv6_source, time.monotonic())
        return _cache
