/* ==========================================================================
   DNSentinel — DNS record actions (records/list.html, records/detail.html)

   form[data-record-delete]     asks whether to delete the record in Cloudflare
                                or only stop tracking it, then submits with
                                mode=cloudflare | local (data-record-name)
   input[data-auto-update-url]  switch that turns sentinel IP tracking on/off
   ========================================================================== */
(function () {
  'use strict';

  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form.matches('form[data-record-delete]')) return;
    event.preventDefault();

    var name = form.dataset.recordName || '';
    Swal.fire({
      title: t('js.records.delete_title'),
      html: t('js.records.delete_text', { name: '<strong class="mono"></strong>' }),
      icon: 'warning',
      showCancelButton: true,
      showDenyButton: true,
      confirmButtonText: t('js.records.delete_cloudflare'),
      denyButtonText: t('js.records.delete_local'),
      customClass: { confirmButton: 'is-danger' },
      focusCancel: true,
      didOpen: function (popup) {
        // Set as text, so the record name is never parsed as HTML.
        popup.querySelector('.swal2-html-container strong').textContent = name;
      }
    }).then(function (result) {
      if (result.isDismissed) return;
      form.elements.mode.value = result.isConfirmed ? 'cloudflare' : 'local';
      form.submit();
    });
  });

  document.addEventListener('change', function (event) {
    var input = event.target;
    if (!input.matches('input[data-auto-update-url]')) return;

    var enabled = input.checked;
    input.disabled = true;
    postJSON(input.dataset.autoUpdateUrl, { enabled: enabled })
      .then(function (data) {
        if (!data.ok) throw new Error(data.msg || t('js.common.unexpected_error'));
        notify(data.msg, enabled && !data.sentinel_enabled ? 'warning' : 'success');
      })
      .catch(function (err) {
        input.checked = !enabled;
        notify(err.message || t('js.common.unexpected_error'), 'danger');
      })
      .finally(function () {
        input.disabled = false;
      });
  });
})();
