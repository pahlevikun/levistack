/* PROTOTYPE: throwaway switcher. One script, no libraries.
   Usage: add <script src="variant-switcher.js" data-variants="a,b,c"></script> at the end of the page,
   and mark each variant with <section data-variant="a" data-name="Quiet Ledger">. The URL param is ?v=a.
   Left and right arrow keys also cycle. Arrow keys are ignored while typing in a field.
   The bar shows only on a local page or a file. Add data-always to the script tag to show it on a shared host. */
(function () {
  var tag = document.currentScript;
  var keys = (tag.getAttribute('data-variants') || 'a,b,c').split(',');
  // Hide it in production. In an app, replace this check with the project's own dev flag.
  var local = location.protocol === 'file:' || /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  if (!local && !tag.hasAttribute('data-always')) return;

  var current = new URLSearchParams(location.search).get('v');
  if (keys.indexOf(current) < 0) current = keys[0];

  function show(k) {
    current = k;
    document.querySelectorAll('[data-variant]').forEach(function (el) { el.hidden = el.getAttribute('data-variant') !== k; });
    var u = new URL(location.href); u.searchParams.set('v', k); history.replaceState(null, '', u);
    label.textContent = k.toUpperCase() + (names[k] ? ' (' + names[k] + ')' : '');
  }
  function move(d) { show(keys[(keys.indexOf(current) + d + keys.length) % keys.length]); }

  var names = {};
  document.querySelectorAll('[data-variant]').forEach(function (el) { names[el.getAttribute('data-variant')] = el.getAttribute('data-name') || ''; });

  var bar = document.createElement('div');
  bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', 'Prototype variants');
  bar.style.cssText = 'position:fixed;left:50%;bottom:16px;transform:translateX(-50%);display:flex;align-items:center;gap:8px;' +
    'padding:6px 10px;border-radius:999px;background:#111;color:#fff;font:13px ui-monospace,Menlo,monospace;box-shadow:0 4px 16px rgba(0,0,0,.3);z-index:2147483647';
  function btn(txt, d) { var b = document.createElement('button'); b.textContent = txt; b.setAttribute('aria-label', d < 0 ? 'Previous variant' : 'Next variant');
    b.style.cssText = 'background:none;border:0;color:inherit;font:inherit;cursor:pointer;padding:2px 6px'; b.onclick = function () { move(d); }; return b; }
  var label = document.createElement('span'); label.setAttribute('aria-live', 'polite');
  bar.appendChild(btn('←', -1)); bar.appendChild(label); bar.appendChild(btn('→', 1));
  document.body.appendChild(bar);

  document.addEventListener('keydown', function (e) {
    var t = e.target, typing = t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable);
    if (typing || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === 'ArrowLeft') move(-1); else if (e.key === 'ArrowRight') move(1);
  });
  show(current);
})();
