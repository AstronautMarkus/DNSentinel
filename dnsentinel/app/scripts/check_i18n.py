"""
Checks the UI strings in app/i18n/strings/ against the code that uses them.

Errors (exit code 1):
  * an entry is missing a supported language, or mixes plain/plural forms
  * a translation has different {placeholders} than the English text
  * a t('...') call in a template, route or script uses an unknown key

Python code also passes keys around as plain strings, rendered later with
t(value) (form errors, sentinel failure reasons): any string literal in a
.py file that names a known key, or an f-string prefix like
f'sentinel.ip_error.{reason}', counts as a use.

Warnings:
  * a key is defined but never used

Usage: python app/scripts/check_i18n.py
"""
import os
import re
import string
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, os.path.abspath(os.path.join(app_dir, '..')))

from app.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from app.i18n.strings import STRINGS

# t('key'), t("key") — a key ending in '.' is a dynamic prefix: t('zones.status.' ~ status)
KEY_USAGE = re.compile(r"""\bt\(\s*['"]([a-z0-9_.]+)['"]""")
SCANNED = (('templates', '.html'), ('static/js', '.js'), ('', '.py'))
# The string tables themselves, and this script's examples, are not usages.
SKIPPED_DIRS = ('i18n', 'scripts')
# In .py files: 'records.form.error.ipv4' and f'sentinel.ip_error.{...}'
PY_KEY_LITERAL = re.compile(r"""(?<![\w.])['"]([a-z0-9_]+(?:\.[a-z0-9_]+)+)['"]""")
PY_KEY_PREFIX = re.compile(r"""\bf['"]([a-z0-9_]+(?:\.[a-z0-9_]+)*\.)\{""")


def placeholders(text):
    return {name for _, name, _, _ in string.Formatter().parse(text) if name}


def check_entries():
    errors = []
    for key, entry in STRINGS.items():
        missing = [lang for lang in SUPPORTED_LANGUAGES if not entry.get(lang)]
        if missing:
            errors.append(f'{key}: missing {", ".join(missing)}')
            continue

        forms = {lang: entry[lang] for lang in SUPPORTED_LANGUAGES}
        plural = {lang: isinstance(value, dict) for lang, value in forms.items()}
        if len(set(plural.values())) > 1:
            errors.append(f'{key}: mixes plain and plural forms')
            continue

        variants = {}
        for lang, value in forms.items():
            if plural[lang]:
                if set(value) != {'one', 'other'}:
                    errors.append(f'{key} [{lang}]: plural forms must be exactly one/other')
                    continue
                variants.update({f'{lang}.{form}': text for form, text in value.items()})
            else:
                variants[lang] = value

        expected = set().union(*(placeholders(v) for k, v in variants.items() if k.startswith(DEFAULT_LANGUAGE)))
        # A plural form may leave out the number itself ("one alert" -> "una alerta").
        optional = {'count'} if plural[DEFAULT_LANGUAGE] else set()
        for variant, text in variants.items():
            found = placeholders(text)
            if not (expected - optional <= found <= expected):
                errors.append(f'{key} [{variant}]: placeholders {sorted(found)} != {sorted(expected)}')
    return errors


def scan_usages():
    used = {}
    for folder, ext in SCANNED:
        root = os.path.normpath(os.path.join(app_dir, folder))
        for dirpath, dirnames, filenames in os.walk(root):
            if dirpath == app_dir:
                dirnames[:] = [d for d in dirnames if d not in SKIPPED_DIRS]
            for filename in filenames:
                if not filename.endswith(ext):
                    continue
                path = os.path.join(dirpath, filename)
                with open(path, encoding='utf-8') as fh:
                    for lineno, line in enumerate(fh, 1):
                        keys = KEY_USAGE.findall(line)
                        if ext == '.py':
                            keys += [key for key in PY_KEY_LITERAL.findall(line) if key in STRINGS]
                            keys += PY_KEY_PREFIX.findall(line)
                        for key in keys:
                            used.setdefault(key, []).append(f'{os.path.relpath(path, app_dir)}:{lineno}')
    return used


def main():
    errors = check_entries()
    used = scan_usages()

    prefixes = [key for key in used if key.endswith('.')]
    for key, locations in sorted(used.items()):
        if key in prefixes:
            if not any(k.startswith(key) for k in STRINGS):
                errors.append(f'unknown key prefix {key!r} used at {locations[0]}')
        elif key not in STRINGS:
            errors.append(f'unknown key {key!r} used at {", ".join(locations)}')

    unused = [k for k in STRINGS if k not in used and not any(k.startswith(p) for p in prefixes)]

    for warning in unused:
        print(f'warning: unused key {warning!r}')
    for error in errors:
        print(f'error: {error}')
    print(f'{len(STRINGS)} keys, {len(used)} used, {len(unused)} unused, {len(errors)} errors')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
