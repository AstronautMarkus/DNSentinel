/* ==========================================================================
   DNSentinel — Landing page "dynamic IP" walkthrough

   A four-act story played on a pausable clock:
     1. Everything works      visitor → DNS → home server, page loads
     2. ISP changes your IP   router gets a new address, DNS records go stale
     3. Everything goes down  DNS sends visitors to the old IP, request is lost
     4. DNSentinel fixes it   agent pushes the new IP to Cloudflare, back online

   Packets travel along SVG wires drawn between the cards. Wire geometry is
   recomputed on resize, so the same story works side-by-side (desktop) and
   stacked (mobile). The clock stops while paused, off-screen or in a hidden
   tab; with prefers-reduced-motion, packets are skipped and only the state
   changes are shown.
   ========================================================================== */
(function () {
  'use strict';

  var root = document.getElementById('ip-demo');
  if (!root) return;

  var DOMAIN = 'example.com';
  var OLD_IP = '203.0.113.24';
  var NEW_IP = '198.51.100.77';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function q(selector) { return root.querySelector(selector); }
  function qa(selector) { return Array.prototype.slice.call(root.querySelectorAll(selector)); }

  var stage = q('[data-demo-stage]');
  var svg = q('[data-demo-wires]');
  var packetLayer = q('[data-demo-packets]');
  var internetLabel = q('[data-demo-internet]');
  var browser = q('[data-demo-browser]');
  var view = q('[data-demo-view]');
  var loadingText = q('[data-demo-loading]');
  var dns = q('[data-demo-dns]');
  var records = qa('[data-record]');
  var dnsNote = q('[data-demo-dns-note]');
  var home = q('[data-demo-home]');
  var isp = q('[data-demo-isp]');
  var router = q('[data-demo-router]');
  var routerIp = q('[data-demo-router-ip]');
  var server = q('[data-demo-server]');
  var agent = q('[data-demo-agent]');
  var agentText = q('[data-demo-agent-text]');
  var sites = qa('[data-demo-site]');
  var statusBadge = q('[data-demo-status]');
  var toggleBtn = q('[data-demo-toggle]');
  var stepBtns = qa('[data-demo-step]');

  var wires = {};
  qa('[data-wire]').forEach(function (wire) { wires[wire.dataset.wire] = wire; });

  /* ---- Clock ------------------------------------------------------------
     All waits and packet flights run on `clock`, which only advances while
     the demo is playing and visible — pausing freezes everything in place. */
  var clock = 0;
  var lastFrame = null;
  var playing = true;
  var onScreen = true;
  var waiters = [];
  var flights = [];

  function isRunning() {
    return playing && onScreen && !document.hidden;
  }

  function wait(ms) {
    return new Promise(function (resolve) {
      waiters.push({ at: clock + ms, resolve: resolve });
    });
  }

  function frame(timestamp) {
    var dt = lastFrame === null ? 0 : Math.min(timestamp - lastFrame, 50);
    lastFrame = timestamp;
    if (isRunning()) {
      clock += dt;
      var due = waiters.filter(function (w) { return w.at <= clock; });
      waiters = waiters.filter(function (w) { return w.at > clock; });
      due.forEach(function (w) { w.resolve(); });
      flights = flights.filter(advanceFlight);
      renderProgress();
    }
    requestAnimationFrame(frame);
  }

  /* ---- Packets ---------------------------------------------------------- */
  function ease(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function placeOnWire(el, wire, fraction) {
    var point = wire.getPointAtLength(wire.getTotalLength() * fraction);
    el.style.transform = 'translate(' + point.x + 'px, ' + point.y + 'px) translate(-50%, -50%)';
  }

  function advanceFlight(flight) {
    var t = Math.min(1, (clock - flight.start) / flight.duration);
    var progress = ease(t) * flight.stopAt;
    placeOnWire(flight.el, flight.wire, flight.reverse ? 1 - progress : progress);
    if (t < 1) return true;
    flight.resolve(flight.el);
    return false;
  }

  function setWire(name, state) {
    wires[name].classList.toggle('is-active', state === 'active');
    wires[name].classList.toggle('is-broken', state === 'broken');
  }

  /* Sends a labelled packet along a wire; resolves with the packet element
     when it arrives (null under reduced motion, where nothing travels). */
  function send(wireName, label, variant, opts) {
    opts = opts || {};
    setWire(wireName, 'active');

    if (reducedMotion.matches) {
      return wait(450).then(function () {
        if (!opts.keepWire) setWire(wireName, '');
        return null;
      });
    }

    var el = document.createElement('div');
    el.className = 'demo-packet demo-packet--' + variant;
    el.innerHTML = (opts.icon ? '<i class="fa-solid ' + opts.icon + '"></i>' : '') + '<span>' + label + '</span>';
    packetLayer.appendChild(el);
    placeOnWire(el, wires[wireName], opts.reverse ? 1 : 0);

    return new Promise(function (resolve) {
      flights.push({
        el: el,
        wire: wires[wireName],
        start: clock,
        duration: opts.duration || 1100,
        reverse: !!opts.reverse,
        stopAt: opts.stopAt || 1,
        resolve: resolve
      });
    }).then(function (packet) {
      if (!opts.keepWire) setWire(wireName, '');
      return packet;
    });
  }

  function land(packet) {
    if (!packet) return;
    packet.classList.add('is-landed');
    setTimeout(function () { packet.remove(); }, 300);
  }

  // A request that never reaches anyone: the packet fizzles and leaves a marker.
  function lose(packet, text, wireName, at) {
    var marker = document.createElement('div');
    marker.className = 'demo-lost';
    marker.dataset.wire = wireName;
    marker.dataset.at = String(at);
    marker.innerHTML = '<i class="fa-solid fa-xmark"></i><span>' + text + '</span>';
    placeOnWire(marker, wires[wireName], at);
    packetLayer.appendChild(marker);
    if (packet) {
      packet.classList.add('is-lost');
      setTimeout(function () { packet.remove(); }, 450);
    }
  }

  function flash(el, className, ms) {
    el.classList.remove(className);
    void el.offsetWidth; // restart the CSS animation
    el.classList.add(className);
    setTimeout(function () { el.classList.remove(className); }, ms || 900);
  }

  /* ---- Scene state ------------------------------------------------------ */
  var STATUS = {
    online: ['success', 'All sites online'],
    changed: ['warning', 'IP changed'],
    down: ['danger', 'Sites down'],
    fixing: ['info', 'Updating DNS']
  };

  function setStatus(key) {
    statusBadge.className = 'badge badge--dot badge--' + STATUS[key][0];
    statusBadge.textContent = STATUS[key][1];
  }

  function setView(state, text) {
    view.dataset.view = state;
    browser.classList.toggle('is-loading', state === 'loading');
    if (text) loadingText.textContent = text;
  }

  function setRouterIp(ip, isNew) {
    routerIp.textContent = ip;
    router.classList.toggle('is-new', !!isNew);
  }

  function setRecordIp(row, ip, stale) {
    row.querySelector('[data-record-ip]').textContent = ip;
    row.classList.toggle('is-stale', !!stale);
  }

  function setDnsNote(state) {
    dns.classList.toggle('is-stale', state === 'stale');
    var notes = {
      ok: ['fa-circle-check', 'Records match your IP'],
      stale: ['fa-triangle-exclamation', 'Records still point to ' + OLD_IP],
      updated: ['fa-circle-check', 'Updated by DNSentinel']
    };
    dnsNote.innerHTML = '<i class="fa-solid ' + notes[state][0] + '"></i> <span>' + notes[state][1] + '</span>';
  }

  function setSite(site, online) {
    site.classList.toggle('is-down', !online);
    site.querySelector('.demo-site__status').textContent = online ? 'Online' : 'Down';
  }

  // Staggered on the demo clock so a jump to another step cancels it.
  function setSites(online, stagger) {
    sites.forEach(function (site, i) {
      if (stagger) {
        wait(i * 180).then(function () { setSite(site, online); });
      } else {
        setSite(site, online);
      }
    });
  }

  function setAgent(state, text) {
    agent.classList.toggle('is-on', state !== 'off');
    agent.classList.toggle('is-working', state === 'working');
    agentText.textContent = text;
    wires.update.classList.toggle('is-dormant', state === 'off');
  }

  /* Each step starts from a known state, so any step can be jumped to. */
  var SCENES = [
    { view: 'idle', ip: OLD_IP, newIp: false, stale: false, sites: true, status: 'online' },
    { view: 'ok', ip: OLD_IP, newIp: false, stale: false, sites: true, status: 'online' },
    { view: 'ok', ip: NEW_IP, newIp: true, stale: true, sites: true, status: 'changed' },
    { view: 'error', ip: NEW_IP, newIp: true, stale: true, sites: false, status: 'down' }
  ];

  function applyScene(index) {
    var scene = SCENES[index];
    waiters = [];
    flights = [];
    packetLayer.innerHTML = '';
    Object.keys(wires).forEach(function (name) { setWire(name, ''); });
    isp.classList.remove('is-zapping');

    setView(scene.view);
    setRouterIp(scene.ip, scene.newIp);
    records.forEach(function (row) { setRecordIp(row, OLD_IP, scene.stale); });
    setDnsNote(scene.stale ? 'stale' : 'ok');
    setSites(scene.sites);
    setAgent('off', 'Not running');
    setStatus(scene.status);
  }

  /* ---- Story beats ------------------------------------------------------ */
  async function resolveDomain(answerIp, stale) {
    setView('loading', 'Looking up ' + DOMAIN + '…');
    land(await send('query', DOMAIN + '?', 'dns', { icon: 'fa-magnifying-glass' }));
    flash(records[0], 'is-hit', 900);
    await wait(250);
    land(await send('query', answerIp, stale ? 'stale' : 'dns', { reverse: true, icon: 'fa-location-dot' }));
  }

  async function loadPage(ip, speed) {
    setView('loading', 'Connecting to ' + ip + '…');
    land(await send('request', 'GET /', 'http', { duration: 1500 * speed }));
    flash(router, 'is-pulse');
    await wait(250 * speed);
    flash(server, 'is-pulse');
    await wait(350 * speed);
    land(await send('request', '200 OK', 'ok', { reverse: true, duration: 1500 * speed, icon: 'fa-check' }));
    setView('ok');
  }

  var ACTS = [
    {
      duration: 9000,
      run: async function () {
        await wait(700);
        await resolveDomain(OLD_IP, false);
        await loadPage(OLD_IP, 1);
      }
    },
    {
      duration: 5500,
      run: async function () {
        await wait(600);
        isp.classList.add('is-zapping');
        await wait(550);
        setStatus('changed');
        flash(router, 'is-shake', 600);
        flash(routerIp, 'is-swapping', 600);
        await wait(250);
        setRouterIp(NEW_IP, true);
        await wait(700);
        isp.classList.remove('is-zapping');
        for (var i = 0; i < records.length; i++) {
          setRecordIp(records[i], OLD_IP, true);
          await wait(160);
        }
        setDnsNote('stale');
      }
    },
    {
      duration: 8500,
      run: async function () {
        await wait(600);
        await resolveDomain(OLD_IP, true);
        setView('loading', 'Connecting to ' + OLD_IP + '…');
        var packet = await send('request', 'GET /', 'http', { duration: 1500, stopAt: 0.8, keepWire: true });
        setWire('request', 'broken');
        lose(packet, 'Nobody at ' + OLD_IP, 'request', 0.8);
        await wait(1300);
        setView('error');
        setStatus('down');
        setSites(false, true);
      }
    },
    {
      duration: 11500,
      run: async function () {
        await wait(500);
        setAgent('on', 'New IP detected: ' + NEW_IP);
        flash(agent, 'is-pulse');
        await wait(1100);
        setStatus('fixing');
        setAgent('working', 'Updating Cloudflare records…');
        land(await send('update', 'A → ' + NEW_IP, 'update', { icon: 'fa-arrows-rotate', duration: 1400 }));
        for (var i = 0; i < records.length; i++) {
          setRecordIp(records[i], NEW_IP, false);
          flash(records[i], 'is-updated', 1200);
          await wait(200);
        }
        setDnsNote('updated');
        setAgent('on', 'Cloudflare records updated');
        router.classList.remove('is-new');
        qa('.demo-lost').forEach(function (marker) { marker.remove(); });
        setWire('request', '');
        await wait(600);
        await resolveDomain(NEW_IP, false);
        await loadPage(NEW_IP, 0.8);
        setStatus('online');
        setSites(true, true);
      }
    }
  ];

  /* ---- Playback --------------------------------------------------------- */
  var runId = 0;
  var currentStep = 0;
  var stepStart = 0;

  // Starting a new run clears the pending waits of the previous one, which
  // leaves that run suspended forever — no explicit cancellation needed.
  function play(fromStep) {
    var id = ++runId;
    (async function () {
      var step = fromStep;
      while (id === runId) {
        currentStep = step;
        stepStart = clock;
        markStep(step);
        applyScene(step);
        await ACTS[step].run();
        await wait(Math.max(0, stepStart + ACTS[step].duration - clock));
        step = (step + 1) % ACTS.length;
      }
    })();
  }

  function markStep(index) {
    stepBtns.forEach(function (btn, i) {
      btn.classList.toggle('is-active', i === index);
      btn.classList.toggle('is-done', i < index);
      btn.style.setProperty('--progress', i < index ? '1' : '0');
      if (i === index) btn.setAttribute('aria-current', 'step');
      else btn.removeAttribute('aria-current');
    });
    renderProgress();
  }

  function renderProgress() {
    var progress = Math.min(1, (clock - stepStart) / ACTS[currentStep].duration);
    stepBtns[currentStep].style.setProperty('--progress', progress.toFixed(3));
  }

  function setPlaying(value) {
    playing = value;
    root.classList.toggle('is-paused', !playing);
    toggleBtn.querySelector('i').className = 'fa-solid ' + (playing ? 'fa-pause' : 'fa-play');
    toggleBtn.querySelector('span').textContent = playing ? 'Pause' : 'Play';
  }

  toggleBtn.addEventListener('click', function () { setPlaying(!playing); });

  stepBtns.forEach(function (btn) {
    btn.addEventListener('click', function () { play(Number(btn.dataset.demoStep)); });
  });

  /* ---- Wire geometry ---------------------------------------------------- */
  function box(el) {
    var s = stage.getBoundingClientRect();
    var b = el.getBoundingClientRect();
    return { l: b.left - s.left, t: b.top - s.top, r: b.right - s.left, b: b.bottom - s.top, w: b.width, h: b.height };
  }

  function sCurve(x1, y1, x2, y2) {
    var mx = (x1 + x2) / 2;
    return 'M' + x1 + ' ' + y1 + ' C' + mx + ' ' + y1 + ' ' + mx + ' ' + y2 + ' ' + x2 + ' ' + y2;
  }

  function layout() {
    var width = stage.clientWidth;
    var height = stage.clientHeight;
    svg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);

    var B = box(browser), D = box(dns), H = box(home), R = box(router), A = box(agent);
    var sideBySide = D.l >= B.r;

    if (sideBySide) {
      // Visitor ⇄ DNS across the top, DNSentinel → DNS from the right, and
      // the HTTP request arcs underneath the DNS card into the router.
      wires.query.setAttribute('d', sCurve(B.r, B.t + B.h * 0.3, D.l, D.t + D.h * 0.45));
      wires.update.setAttribute('d', sCurve(H.l, A.t + A.h / 2, D.r, D.t + D.h * 0.55));
      var y1 = B.t + B.h * 0.78;
      var y2 = R.t + R.h / 2;
      var low = Math.min(height - 18, Math.max(D.b, y1, y2) + 56);
      var control = (8 * low - y1 - y2) / 6; // puts the curve's lowest point at `low`
      wires.request.setAttribute('d',
        'M' + B.r + ' ' + y1 + ' C' + (B.r + 90) + ' ' + control + ' ' + (H.l - 90) + ' ' + control + ' ' + H.l + ' ' + y2);
    } else {
      // Stacked: visitor, DNS, home. The request detours through the left gutter.
      var x = B.l + B.w * 0.6;
      wires.query.setAttribute('d', 'M' + x + ' ' + B.b + ' L' + x + ' ' + D.t);
      wires.update.setAttribute('d', 'M' + x + ' ' + H.t + ' L' + x + ' ' + D.b);
      var gutter = Math.max(6, B.l - 20);
      var ry1 = B.t + B.h * 0.7;
      var ry2 = R.t + R.h / 2;
      wires.request.setAttribute('d',
        'M' + B.l + ' ' + ry1 + ' C' + gutter + ' ' + ry1 + ' ' + gutter + ' ' + ry2 + ' ' + H.l + ' ' + ry2);
    }

    internetLabel.hidden = !sideBySide;
    if (sideBySide) placeOnWire(internetLabel, wires.request, 0.5);

    qa('.demo-lost').forEach(function (marker) {
      placeOnWire(marker, wires[marker.dataset.wire], Number(marker.dataset.at));
    });
  }

  /* ---- Boot ------------------------------------------------------------- */
  layout();
  if (window.ResizeObserver) new ResizeObserver(layout).observe(stage);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      onScreen = entries[0].isIntersecting;
    }, { threshold: 0.15 }).observe(root);
  }

  setPlaying(true);
  play(0);
  requestAnimationFrame(frame);
})();
