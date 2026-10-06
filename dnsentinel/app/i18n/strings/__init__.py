"""
UI strings, one module per area of the app. Each module exposes a STRINGS
dict of `key: {'en': ..., 'es': ...}`; a value can also be a plural entry,
`{'one': ..., 'other': ...}`, selected with t(key, count=n).

Keys are namespaced by area (`zones.create.title`, `records.api.zone_not_found`)
and `js.*` keys are also sent to the browser. Run app/scripts/check_i18n.py
after editing to catch missing translations and unknown keys.
"""
from . import auth, common, dashboard, js, records, sentinel, zones

MODULES = (common, auth, dashboard, zones, records, sentinel, js)


def _merge(modules):
    merged = {}
    for module in modules:
        for key, entry in module.STRINGS.items():
            if key in merged:
                raise ValueError(f'Duplicate i18n key {key!r} in {module.__name__}')
            merged[key] = entry
    return merged


STRINGS = _merge(MODULES)
