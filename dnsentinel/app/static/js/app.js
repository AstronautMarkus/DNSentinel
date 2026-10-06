/* ==========================================================================
   DNSentinel — Shared UI behaviour
   Declarative, attribute-driven helpers so templates don't need inline JS:

   [data-copy="value"]          copy the value to the clipboard
   [data-secret-toggle]         reveal / mask the sibling [data-secret] value
   [data-dropdown]              dropdown wrapper; [data-dropdown-toggle] opens it
   [data-sidebar-toggle]        desktop: collapse / expand the sidebar (remembered)
                                mobile: open / close the off-canvas sidebar
   [data-sidebar-close]         close the off-canvas sidebar (mobile)
   [data-dismiss]               remove the closest .toast / .alert
   [data-confirm="message"]     ask for confirmation before following a link
                                (optional: data-confirm-title, data-confirm-button,
                                data-confirm-icon = Font Awesome icon name)
   [data-current-year]          filled with the current year

   Also exposes window.t(key, vars) for localized UI strings (see i18n below).
   ========================================================================== */
(function () {
  'use strict';

  var MASK = '••••••••••••';
  var TOAST_TIMEOUT = 6000;
  var SIDEBAR_KEY = 'dnsentinel.sidebar';
  // Must match the breakpoint in layout.css
  var desktopQuery = window.matchMedia('(min-width: 1025px)');

  /* ---- i18n -------------------------------------------------------------
     The server embeds the js.* strings (app/i18n/strings/js.py), already in
     the page language, as JSON in <script id="i18n-data">. Placeholders
     look like {name}; plural entries are picked with vars.count. */
  var STRINGS = {};
  try {
    STRINGS = JSON.parse(document.getElementById('i18n-data').textContent);
  } catch (err) { /* no data: t() falls back to the key */ }

  function t(key, vars) {
    var text = STRINGS[key];
    if (text === undefined || text === null) return key;
    if (typeof text === 'object') text = vars && vars.count === 1 ? text.one : text.other;
    if (!vars) return text;
    return text.replace(/\{(\w+)\}/g, function (match, name) {
      return Object.prototype.hasOwnProperty.call(vars, name) ? String(vars[name]) : match;
    });
  }
  window.t = t;

  /* SweetAlert2 (admin pages load it before this file) gets localized
     default buttons, so every Swal.fire() in the templates inherits them. */
  if (window.Swal) {
    window.Swal = window.Swal.mixin({
      confirmButtonText: t('js.common.ok'),
      cancelButtonText: t('js.common.cancel')
    });
  }

  /* ---- Clipboard --------------------------------------------------------
     navigator.clipboard only exists in secure contexts (HTTPS / localhost).
     DNSentinel is often reached over plain HTTP on a LAN, so fall back to
     the legacy execCommand approach. */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.top = '-1000px';
      document.body.appendChild(area);
      area.select();
      try {
        document.execCommand('copy') ? resolve() : reject(new Error('Copy failed'));
      } catch (err) {
        reject(err);
      } finally {
        area.remove();
      }
    });
  }

  function showCopied(btn) {
    var icon = btn.querySelector('i');
    if (!icon) return;
    if (!btn.dataset.icon) btn.dataset.icon = icon.className;
    icon.className = 'fa-solid fa-check';
    btn.classList.add('is-copied');
    clearTimeout(btn._copyTimer);
    btn._copyTimer = setTimeout(function () {
      icon.className = btn.dataset.icon;
      btn.classList.remove('is-copied');
    }, 1200);
  }

  /* ---- Secrets ---------------------------------------------------------- */
  function toggleSecret(btn) {
    var wrapper = btn.closest('.copyable');
    var value = wrapper && wrapper.querySelector('[data-secret]');
    if (!value) return;
    var reveal = btn.getAttribute('aria-pressed') !== 'true';
    value.textContent = reveal ? value.dataset.secret : MASK;
    value.classList.toggle('is-masked', !reveal);
    btn.setAttribute('aria-pressed', String(reveal));
    var label = reveal ? t('js.common.hide_token') : t('js.common.show_token');
    btn.setAttribute('aria-label', label);
    btn.title = label;
    var icon = btn.querySelector('i');
    if (icon) icon.className = reveal ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye';
  }

  /* ---- Dropdowns -------------------------------------------------------- */
  function setDropdown(dropdown, open) {
    dropdown.classList.toggle('is-open', open);
    var toggle = dropdown.querySelector('[data-dropdown-toggle]');
    if (toggle) toggle.setAttribute('aria-expanded', String(open));
  }

  function closeDropdowns(except) {
    document.querySelectorAll('[data-dropdown].is-open').forEach(function (dropdown) {
      if (dropdown !== except) setDropdown(dropdown, false);
    });
  }

  /* ---- Sidebar ----------------------------------------------------------
     The collapsed state lives on <html> so the inline script in
     admin_base.html can restore it before first paint (no flash). */
  function isSidebarOpen() {
    return desktopQuery.matches
      ? !document.documentElement.classList.contains('sidebar-collapsed')
      : document.body.classList.contains('sidebar-open');
  }

  function syncSidebarToggles() {
    var open = isSidebarOpen();
    var label = open ? t('js.layout.hide_navigation') : t('js.layout.show_navigation');
    document.querySelectorAll('[data-sidebar-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', label);
      btn.title = label;
    });
  }

  function setSidebar(open) {
    if (desktopQuery.matches) {
      document.documentElement.classList.toggle('sidebar-collapsed', !open);
      try {
        localStorage.setItem(SIDEBAR_KEY, open ? 'expanded' : 'collapsed');
      } catch (err) { /* storage unavailable: state just won't persist */ }
    } else {
      document.body.classList.toggle('sidebar-open', open);
    }
    syncSidebarToggles();
  }

  function closeMobileSidebar() {
    if (!document.body.classList.contains('sidebar-open')) return;
    document.body.classList.remove('sidebar-open');
    syncSidebarToggles();
  }

  desktopQuery.addEventListener('change', function () {
    document.body.classList.remove('sidebar-open');
    syncSidebarToggles();
  });

  /* ---- Toasts ----------------------------------------------------------- */
  function dismiss(el) {
    if (!el || el.classList.contains('is-leaving')) return;
    el.classList.add('is-leaving');
    setTimeout(function () { el.remove(); }, 220);
  }

  /* ---- Confirmations ----------------------------------------------------
     Uses SweetAlert2 when the page loads it (admin pages), otherwise the
     native confirm() dialog. */
  function confirmNavigation(link) {
    var message = link.dataset.confirm;
    var go = function () { window.location.href = link.href; };

    if (!window.Swal) {
      if (window.confirm(message)) go();
      return;
    }

    var options = {
      title: link.dataset.confirmTitle || t('js.common.are_you_sure'),
      text: message,
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: link.dataset.confirmButton || t('js.common.confirm'),
      reverseButtons: true,
      focusCancel: true
    };
    if (link.dataset.confirmIcon) {
      options.iconHtml = '<i class="fa-solid ' + link.dataset.confirmIcon + '" aria-hidden="true"></i>';
    }
    window.Swal.fire(options).then(function (result) {
      if (result.isConfirmed) go();
    });
  }

  /* ---- Event delegation ------------------------------------------------- */
  document.addEventListener('click', function (event) {
    var target = event.target;

    var confirmLink = target.closest('a[data-confirm]');
    if (confirmLink) {
      event.preventDefault();
      closeDropdowns();
      confirmNavigation(confirmLink);
      return;
    }

    var copyBtn = target.closest('[data-copy]');
    if (copyBtn) {
      copyText(copyBtn.dataset.copy).then(function () { showCopied(copyBtn); });
      return;
    }

    var secretBtn = target.closest('[data-secret-toggle]');
    if (secretBtn) {
      toggleSecret(secretBtn);
      return;
    }

    var dismissBtn = target.closest('[data-dismiss]');
    if (dismissBtn) {
      dismiss(dismissBtn.closest('.toast, .alert'));
      return;
    }

    var dropdownToggle = target.closest('[data-dropdown-toggle]');
    if (dropdownToggle) {
      var dropdown = dropdownToggle.closest('[data-dropdown]');
      var open = !dropdown.classList.contains('is-open');
      closeDropdowns(dropdown);
      setDropdown(dropdown, open);
      return;
    }

    var dropdownItem = target.closest('[data-dropdown] .dropdown__item');
    if (dropdownItem) {
      setDropdown(dropdownItem.closest('[data-dropdown]'), false);
    } else if (!target.closest('[data-dropdown]')) {
      closeDropdowns();
    }

    if (target.closest('[data-sidebar-toggle]')) {
      setSidebar(!isSidebarOpen());
    } else if (target.closest('[data-sidebar-close]')) {
      closeMobileSidebar();
    }
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    closeDropdowns();
    closeMobileSidebar();
  });

  /* ---- Tables ------------------------------------------------------------
     Flags tables wider than their container so the pinned actions column
     can show a separator only while content scrolls underneath it. */
  function watchTableOverflow() {
    var wraps = document.querySelectorAll('.table-wrap');
    if (!wraps.length || !window.ResizeObserver) return;
    var observer = new ResizeObserver(function (entries) {
      entries.forEach(function (entry) {
        var wrap = entry.target;
        wrap.classList.toggle('is-scrollable', wrap.scrollWidth > wrap.clientWidth + 1);
      });
    });
    wraps.forEach(function (wrap) { observer.observe(wrap); });
  }

  /* ---- On load ---------------------------------------------------------- */
  function init() {
    syncSidebarToggles();
    watchTableOverflow();

    document.querySelectorAll('.toast[data-autohide="true"]').forEach(function (toast) {
      setTimeout(function () { dismiss(toast); }, TOAST_TIMEOUT);
    });

    var year = String(new Date().getFullYear());
    document.querySelectorAll('[data-current-year]').forEach(function (el) {
      el.textContent = year;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
