"""
English / Spanish localization.

Two strategies, picked per page (same split as astronautmarkus.dev):

* UI strings — almost everything. Templates, routes and JS stay single files
  and pull short strings by key with `t()`; the strings live side by side in
  `app/i18n/strings/`, one module per area of the app.
* Whole templates — long-form prose (the landing page). `x.html` gets a
  `x_es.html` sibling and the route renders it with `render_localized_template`.

The language comes from the `lang` cookie (set by /lang/<code>), then the
browser's Accept-Language header, then English.
"""
from flask import g, has_app_context, redirect, render_template, request, url_for
from markupsafe import Markup

from .strings import STRINGS

SUPPORTED_LANGUAGES = ('en', 'es')
DEFAULT_LANGUAGE    = 'en'
LANG_COOKIE_NAME    = 'lang'
LANG_COOKIE_MAX_AGE = 60 * 60 * 24 * 365

# Endonyms: each language is always shown in its own language in the switcher.
LANGUAGE_NAMES = {'en': 'English', 'es': 'Español'}

# Keys with this prefix are also sent to the browser (see js_strings()).
JS_PREFIX = 'js.'


def get_current_language():
    """Return the active language for the current request, falling back to the default."""
    lang = getattr(g, 'current_lang', None) if has_app_context() else None
    if lang in SUPPORTED_LANGUAGES:
        return lang
    return DEFAULT_LANGUAGE


def t(key, count=None, default=None, **kwargs):
    """
    Look up a UI string in the current language and interpolate placeholders:

        t('auth.flash.login_success', name=user.name)
        t('js.dashboard.alerts', count=3)       # plural entry: {'one': ..., 'other': ...}
        t('zones.status.' + status, default=status.capitalize())

    Keys ending in `_html` contain markup: they return Markup, and the
    interpolated values are escaped, so they are safe to render as-is.

    Falls back to English, then to `default`, then to the raw key, so a
    missing translation degrades to visible-but-wrong rather than a crash.
    """
    entry = STRINGS.get(key)
    if entry is None:
        return key if default is None else default

    text = entry.get(get_current_language()) or entry.get(DEFAULT_LANGUAGE, key)
    if isinstance(text, dict):
        text = text['one' if count == 1 else 'other']
    if count is not None:
        kwargs.setdefault('count', count)

    if key.endswith('_html'):
        return Markup(text).format(**kwargs) if kwargs else Markup(text)
    return text.format(**kwargs) if kwargs else text


def js_strings():
    """The `js.*` strings in the current language, for static/js/app.js's t()."""
    lang = get_current_language()
    return {
        key: entry.get(lang) or entry.get(DEFAULT_LANGUAGE)
        for key, entry in STRINGS.items()
        if key.startswith(JS_PREFIX)
    }


def localized_template_names(template_name):
    """
    Candidate templates for the current language, most specific first:

        'index.html'  ->  ['index_es.html', 'index.html']   (lang = 'es')
        'index.html'  ->  ['index.html']                    (lang = 'en')
    """
    lang = get_current_language()
    if lang == DEFAULT_LANGUAGE:
        return [template_name]
    base, dot, ext = template_name.rpartition('.')
    candidate = f'{base}_{lang}.{ext}' if dot else f'{template_name}_{lang}'
    return [candidate, template_name]


def render_localized_template(template_name, **context):
    """Drop-in replacement for render_template that picks the `_<lang>` variant when it exists."""
    # Flask selects the first template in the list that exists (cached by Jinja).
    return render_template(localized_template_names(template_name), **context)


def language_switch_url(lang):
    """URL that switches to `lang` and comes back to the current page."""
    next_url = request.full_path if request.query_string else request.path
    return url_for('set_language', lang_code=lang, next=next_url)


def _safe_next(target):
    # Only same-site paths: '//host' and '/\host' are read by browsers as another host.
    if not target or not target.startswith('/') or target.startswith(('//', '/\\')):
        return '/'
    return target


def init_i18n(app):
    @app.before_request
    def detect_language():
        lang = request.cookies.get(LANG_COOKIE_NAME)
        if lang not in SUPPORTED_LANGUAGES:
            lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES) or DEFAULT_LANGUAGE
        g.current_lang = lang

    @app.get('/lang/<lang_code>')
    def set_language(lang_code):
        lang = lang_code.lower()
        if lang not in SUPPORTED_LANGUAGES:
            lang = DEFAULT_LANGUAGE

        response = redirect(_safe_next(request.args.get('next')))
        response.set_cookie(LANG_COOKIE_NAME, lang, max_age=LANG_COOKIE_MAX_AGE, samesite='Lax')
        return response

    # Globals (not a context processor) so macros imported without context
    # — `{% import 'base/partials/macros.html' as ui %}` — can use them too.
    app.jinja_env.globals.update(
        t=t,
        js_strings=js_strings,
        language_switch_url=language_switch_url,
        SUPPORTED_LANGUAGES=SUPPORTED_LANGUAGES,
        LANGUAGE_NAMES=LANGUAGE_NAMES,
    )

    @app.context_processor
    def inject_language():
        return {'current_lang': get_current_language()}
